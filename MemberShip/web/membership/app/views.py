# -*- coding: utf-8 -*-

from flask import abort
from flask import request
from flask import jsonify

from app import logger
from app import membership_pb2
from app import models

import app

from util import decode_base64
from util import encode_base64
from util import to_utf8
from util import from_utf8

from itsdangerous import JSONWebSignatureSerializer
from itsdangerous import BadSignature
from itsdangerous import BadData

import hashlib
import facebook
import simplejson as json
import datetime
import requests
import string
import random

# initialize serializer
_serializer = JSONWebSignatureSerializer(app.SECRET_KEY)

# initialize service_platforms
_service_platforms = [membership_pb2.SERVICE_PLATFORM_PLAYSTORE,
                      membership_pb2.SERVICE_PLATFORM_APPSTORE,
                      membership_pb2.SERVICE_PLATFORM_GAMEFLIER]

_service_platform_urls = {
  membership_pb2.SERVICE_PLATFORM_PLAYSTORE: app.PLAYSTORE_URL,
  membership_pb2.SERVICE_PLATFORM_APPSTORE: app.APPSTORE_URL,
  membership_pb2.SERVICE_PLATFORM_GAMEFLIER: app.GAMEFLIER_URL,
}

_random_string = string.ascii_letters + string.digits

# initialize PlayStore PUBLIC_KEY
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

PLAYSTORE_PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs01V/72JCxylb8REj6jlRBvsjmx/VfTs1nIX4lQY6sinzJYrz07x0Ven9GD6xTQboXGH2Dk2hmu4XsiZDu8CxKWcR5Kx/8BqtE6IrLWSAD4J2iB1P4ELZRGoLWIraZ/oidxLGKk0RgohPw/EjNFtVveXlgHrvY3NECMZ75n/t8wNivp+nEKqWAtPd0gCTxtp3hDOe8n70aiw9MtCV2t0BaAyFXYiVtkBCAyjDh7k0RKo7TgCR+IA21rfs5i2Fv6S8H0I1o+1rfNyRG9jnqhtHI4Wi+CfcXf7uO+oVECl2Pq21rrcBSzIOZqfwdZTrnK/pXD1Hb891KLRIUk9DdkRcQIDAQAB'
PLAYSTORE_VERIFY_KEY = RSA.importKey(decode_base64(PLAYSTORE_PUBLIC_KEY))
_signature_verifier = PKCS1_v1_5.new(PLAYSTORE_VERIFY_KEY)


def _verify_access_token(request, access_token):
    member = None
    # access_token
    if not access_token:
        _error(request, 'Can not verify access_token;{access_token:%s}' % (access_token), 404)

    # verify access_token
    try:
        member = _serializer.loads(access_token)
    except BadSignature as err:
        _error(request, 'Can not verify access_token;{access_token:%s}' % (access_token), 404, err)

    if not models.verify_member(member['member_id'], access_token):
        _error(request, 'Verify access_token failed;{access_token:%s}' % (access_token), 404)

    return member


def _generate_access_token(request, member_id):
    if not member_id:
        _error(request, 'Member is not exist;{member_id:%d}' % (member_id), 404)

    member = {'member_id': member_id}
    access_token = to_utf8(_serializer.dumps(member))

    if not models.register_member(member_id, access_token):
        _error(request, 'Register member failed;{member_id:%d}' % (member_id), 404)

    return access_token


def _debug(request, message):
    logger.debug('%s;{remote_addr:%s}' % (message, request.remote_addr))

def _info(request, message):
    logger.info('%s;{remote_addr:%s}' % (message, request.remote_addr))

def _warn(request, message):
    logger.warning('%s;{remote_addr:%s}' % (message, request.remote_addr))

def _error(request, message, code=None, err=None):
    if err:
        logger.error('%s;{remote_addr:%s};%s' % (message, request.remote_addr, err))
    else:
        logger.error('%s;{remote_addr:%s}' % (message, request.remote_addr))
    if code:
        abort(code, message)



def _verify_request_header(request):
    if not request or not request.headers:
        _error(request, 'Invalid request', 404)

    # verify Accept
    accept = request.headers.get('Accept')
    if accept != u'text/plain': 
        _error(request, 'Header accept is not match;{accept:%s}' % (accept), 404)

    # verify Content-Type
    content_type = request.headers.get('Content-Type')
    if content_type != u'application/json':
        _error(request, 'Header content-type is not match;{content_type:%s}' % (content_type), 404)

    # verify digest
    timestamp = request.headers.get('Timestamp')
    if not timestamp:
        _error(request, 'Timestamp is not exist', 404)

    digest = request.headers.get('Digest')
    if not digest:
        _error(request, 'Digest is not exist', 404)

    h = hashlib.sha1()
    h.update(timestamp + app.APP_SECRET)
    if digest != h.hexdigest():
        _error(request, 'Digest is not match;{digest:%s}' % (digest), 404)

    # verify User-Agent: <Application Name>;<Protocol Version>;<Service Platform>
    user_agent = request.headers.get('User-Agent')
    if not user_agent:
        _error(request, 'User-Agent is not exist', 404)

    user_agent = user_agent.split(';')
    if len(user_agent) != 3:
        _error(request, 'Invalid User-Agent format;{user_agent:%s}' % (','.join(user_agent)), 404)

    if user_agent[0] != app.APP_NAME:
        _error(request, 'Invalid application name;{app_name:%s}' % (user_agent[0]), 404)

    # verify service_platform
    try:
        service_platform = int(user_agent[2])
    except ValueError as err:
        _error(request, 'Invalid service platform;{service_platform:%s}' % (user_agent[2]), 404, err)

    if not service_platform in _service_platforms:
        _error(request, 'Invalid Service Platform;{user_agent:%s}' % (','.join(user_agent)), 404)

    mismatch = False
    if user_agent[1] != str(app.PROTOCOL_VERSION):
        _warn(request, 'Protocol version is not match;{protocol_version:%s}' % (user_agent[1]))
        mismatch = True

    return mismatch, service_platform


def _verify_request_body(request, type):
    if not request.data:
        _error(request, 'Invalid request', 404)

    # decode base64
    try:
        decode_data = decode_base64(request.data)
    except Exception as err:
        _error(request, 'Invalid decode string;{data:%s}' % (request.data), 404, err)

    req = membership_pb2.Request()

    try:
        req.ParseFromString(decode_data)
    except Exception as err:
        _error(request, 'Invalid massage format;{data:%s}' % (request.data), 404, err)

    if type != req.type:
        _error(request, 'Invalid request type;{type:%d}' % (type), 404)
    return req



def _verify_app_key(app_key):
    if not app_key:
        _error(request, 'Application key is not found', 404)

    if app_key != app.APP_KEY:
        _error(request, 'Application key is not match;{app_key:%s}' % (app_key), 404)


def _verify_push(request):
    # app_key
    _verify_app_key(request.form['app_key'])

    # member_ids
    member_ids = request.form['member_ids']
    if not member_ids:
        _error(request, 'Member Ids is not found', 404)

    # verify member_ids
    if len(member_ids.split(',')) == 0:
        _error(request, 'Member Ids is required;{member_ids:%s}' % (member_ids), 404)

    # TODO: reconstruct member_ids is valid

    # message
    message = request.form['message']
    if not message:
        _error(request, 'Message is not found', 404)

    # verify message json format
    try:
        json.loads(message)
    except ValueError as err:
        _error(request, 'Invalid message format;{message:%s}' % (message), 404, err)

    # time
    time = request.form['time']
    if not time:
        _error(request, 'Time is not found', 404)

    # verify time format (YYYY-MM-DD HH:mm:SS)
    try:
        datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    except ValueError as err:
        _error(request, 'Invalid time format;{time:%s}' % (time), 404, err)

    return member_ids, message, time


def _make_response(request, member_id):
    response = membership_pb2.Response()
    response.type = request.type
    response.access_token = _generate_access_token(request, member_id)
    response.expire_time = app.EXPIRE_TIME
    return response


def _make_error(message, status_code):
    response = jsonify(message=message)
    response.status_code = status_code
    return response

@app.app.errorhandler(400)
def bad_request(error):
    message = error.description if hasattr(error, 'description') else 'Bad request'
    return _make_error(message, 400)


@app.app.errorhandler(401)
def unauthorized(error):
    message = error.description if hasattr(error, 'description') else 'Unauthroized'
    return _make_error(message, 401)


@app.app.errorhandler(404)
def not_found(error):
    message = error.description if hasattr(error, 'description') else 'Not found'
    return _make_error(message, 404)


@app.app.errorhandler(406)
def not_acceptable(error):
    message = error.description if hasattr(error, 'description') else 'Not acceptable'
    return _make_error(message, 406)


@app.app.errorhandler(500)
def internal_server_error(error):
    message = error.description if hasattr(error, 'description') else 'Internal Server Error'
    return _make_error(message, 500)


@app.app.route('/api/members', methods=['POST'])
def members():
    _debug(request, 'members api requested')

    # version check
    mismatch, service_platform = _verify_request_header(request)
    if mismatch:
        store_url = _service_platform_urls.get(service_platform, None)
        if store_url:
            response = jsonify(store_url=store_url)
            response.status_code = 406
            return response
        _error(request, 'Protocol version is not match', 406)

    req = _verify_request_body(request, membership_pb2.MEMBERS)
    members = req.members

    _verify_app_key(members.app_key)

    facebook_id = 0
    facebook_email = ''

    # TODO: async
    # facebook access_token verification
    if members.facebook and members.facebook.id > 0 and members.facebook.access_token != u'':
        # TODO: facebook connect exception handling
        graph = facebook.GraphAPI(access_token=members.facebook.access_token, 
                                  version=app.FACEBOOK_API_VERSION)
        user = graph.get_object('me')

        # verify facebook_id
        if user['id'] and members.facebook.id == long(user['id']):
            facebook_id = members.facebook.id
            facebook_email = members.facebook.email

    # create or get member
    member_id, payments = models.member_info(udid = members.udid,
                                   device_platform = members.device_platform,
                                   service_platform = members.service_platform,
                                   gcm_token = members.gcm_token,
                                   facebook_id = facebook_id,
                                   facebook_email = facebook_email)
    if not member_id:
        _error(request, 'Can not find member;{udid:%s}' % (members.udid), 404)

    # make response
    developer_payload = ''.join(random.choice(_random_string) for _ in range(64))

    response = _make_response(req, member_id)
    response.members.member_id = member_id
    response.members.developer_payload = developer_payload
    for p in payments:
        payment = response.members.payments.add()
        payment.service_platform = p['service_platform']
        payment.payment_id = p['payment_id']
        payment.order_id = p['order_id']
        payment.developer_payload = p['developer_payload']
        payment.purchase_token = p['purchase_token']
        payment.inapp_id = p['inapp_id']

    return encode_base64(response.SerializeToString())




@app.app.route('/api/ping/access_token=<access_token>', methods=['GET'])
def ping(access_token):
    _debug(request, 'ping api requested')

    _verify_request_header(request)
    _verify_access_token(request, access_token)
    return jsonify(result='OK')



@app.app.route('/api/token', methods=['POST'])
def token():
    _debug(request, 'token api requested')

    # 헤더정보 검증
    _verify_request_header(request)
  
    # 데이터정보 검증
    req = _verify_request_body(request, membership_pb2.TOKEN)
    token = req.token

    # app_key 검증
    _verify_app_key(token.app_key)

    # select member id
    member_id = models.member_id(token.udid, 
                                 token.device_platform,
                                 token.service_platform)
    if not member_id:
        _error(request, 'Member is not exist;{udid:%s}' % (token.udid), 404)

    # make response
    response = _make_response(req, member_id)
    return encode_base64(response.SerializeToString())


def _verify_signature(payment):
    if payment.service_platform == membership_pb2.SERVICE_PLATFORM_PLAYSTORE:
        # verify playstore purchase signature
        h = SHA.new(payment.playstore.original_json)
        signature = decode_base64(payment.playstore.signature)
        return _signature_verifier.verify(h, signature)

    elif payment.service_platform == membership_pb2.SERVICE_PLATFORM_APPSTORE:
        # TODO: verify appstore purchase reciept
        pass

    elif payment.service_platform == membership_pb2.SERVICE_PLATFORM_GAMFLIER:
        # TODO: verify gameflier purchase information
        pass

    return False


def _verify_payment(request, member_id, service_platform, payment):
    # verify service platform
    if service_platform != payment.service_platform:
        _error(request, 'Service platform mismatch;{member_id:%d,service_platform:%d}' % (member_id, service_platform), 404)

    product = None
    for p in app.PRODUCTS[service_platform]:
        if payment.inapp_id == p['inapp_id']:
            product = p
            break

    if not product:
        _error(request, 'Not found inapp_id;{member_id:%d,inapp_id:%s}' % (member_id, payment.inapp_id), 404)

    # verify signature
    if not _verify_signature(payment):
        _error(request, 'Failed to purchase verification;{member_id:%d,inapp_id:%s}' % (member_id, payment.inapp_id), 404)

    return product


@app.app.route('/api/payment', methods=['POST'])
def payment():
    _debug(request, 'payment api requested')

    # verify request headers
    mismatch, service_platform = _verify_request_header(request)

    # verify request body
    req = _verify_request_body(request, membership_pb2.PAYMENT)
    payment = req.payment

    # verify access token
    member = _verify_access_token(request, payment.access_token)
    member_id = member['member_id']

    # verify payment
    product = _verify_payment(request, member_id, service_platform, payment)

    # insert purchase
    payment_id = models.purchase(member_id, product, payment)
    if not payment_id:
        _error(request, 'Purchase failed;{member_id:%d,inapp_id:%s}' % (member_id, payment.inapp_id), 404)

    # make response
    response = _make_response(req, member_id)
    response.payment.service_platform = payment.service_platform
    response.payment.payment_id = payment_id
    response.payment.inapp_id = product['inapp_id']
    if payment.service_platform == membership_pb2.SERVICE_PLATFORM_PLAYSTORE:
        response.payment.order_id = payment.playstore.order_id
        response.payment.developer_payload = payment.playstore.developer_payload
        response.payment.purchase_token = payment.playstore.purchase_token
    elif payment.service_platform == membership_pb2.SERVICE_PLATFORM_APPSTORE:
        pass
    elif payment.service_platform == membership_pb2.SERVICE_PLATFORM_GAMEFLIER:
        pass

    _debug(request, 'payment api responsed')
    return encode_base64(response.SerializeToString())


@app.app.route('/api/push/allow/access_token=<access_token>', methods=['GET'])
def query_push_allow(access_token):
    _debug(request, 'query_push_allow api requested')

    # verify request headers
    _verify_request_header(request)

    # verify access token
    member = _verify_access_token(request, access_token)
    if not member:
        _error(request, 'Can not verify access_token;{access_token:%s}' % (access_token), 404)
    member_id = member['member_id']

    # get push notification by member_id
    push_notification = models.push_notification(member_id)
    if not push_notification in [True, False]:
        _error(request, 'Can not found push notification;{member_id:%d}' % (member_id), 404)
    
    return jsonify(push_notification=push_notification)



@app.app.route('/api/push/allow', methods=['POST'])
def push_allow():
    _debug(request, 'push_allow api requested')

    # verify request headers
    _verify_request_header(request)

    # verify request body
    req = _verify_request_body(request, membership_pb2.PUSH_ALLOW)
    push_allow = req.push_allow

    # verify access token
    member = _verify_access_token(request, push_allow.access_token)
    member_id = member['member_id']

    # toggle push notification by member_id
    push_notification = models.toggle_push_notification(member_id)
    if not push_notification in [True, False]:
        _error(request, 'Can not found push notification;{member_id:%d}' % (member_id), 404)

    return jsonify(push_notification=push_notification)




# 설정정보 재로딩
@app.app.route('/api/reload')
def reload():
    _debug(request, 'reload api requested')

    models.load_app(True)
    return jsonify(result='OK')


# 멤버 access_token 정보 확인(Gateway -> MemberShip)
@app.app.route('/api/members/self', methods=['POST'])
def members_self():
    # verify app_key
    _verify_app_key(request.form['app_key'])

    # verify access_token
    access_token = request.form['access_token']
    if not access_token:
        _error(request, 'Access Token is not found', 404)

    member = _verify_access_token(request, access_token)
    return jsonify(member=member)


# 멤버 정보 병합(Gateway -> MemberShip)
@app.app.route('/api/members/merge', methods=['POST'])
def members_merge():
    pass


# 푸시메시지 발송(Gateway/GM툴 -> MemberShip)
@app.app.route('/api/push', methods=['POST'])
def push():
    _debug(request, 'push api requested')

    # verify push informations
    member_ids, message, time = _verify_push(request)

    # make payload
    payload = {'gcm_sender_id': app.GCM_SENDER_ID,
               'gcm_server_api_key': app.GCM_SERVER_API_KEY,
               'app_id': app.APP_ID,
               'member_ids': member_ids,
               'message': message,
               'time': time}

    # validate push response
    response = None
    try:
        response = requests.post(app.PUSH_URL + '/push', data=payload)
    except requests.ConnectionError:
        _error(request, 'Can not connect push service', 500)

    if response.status_code == 200:
        return jsonify(result='OK')

    return _make_error('failed', 500)
    


def _verify_payment_effectuate(request):
    _verify_app_key(request.form['app_key'])

    member_id = request.form['member_id']
    if not member_id:
        _error(request, 'Can not found member id', 404)
    member_id = int(member_id)

    payment_id = request.form['payment_id']
    if not payment_id:
        _error(request, 'Can not found payment id;{member_id:%d}' % (member_id), 404)
    payment_id = int(payment_id)
 
    service_platform = request.form['service_platform']
    if not service_platform:
        _error(request, 'Can not found service platform', 404)
    service_platform = int(service_platform)
    if not service_platform in _service_platforms:
        _error(request, 'Invalid Service Platform;{member_id:%d}' % (member_id), 404)

    order_id = request.form['order_id']
    if not order_id:
        _error(request, 'Can not found order id;{member_id:%d}' % (member_id), 404)

    if not request.form['developer_payload']:
        _error(request, 'Can not found developer payload;{member_id:%d}' % (member_id), 404)

    if not request.form['purchase_token']:
        _error(request, 'Can not found purchase token;{member_id:%d}' % (member_id), 404)

    inapp_id = request.form['inapp_id']
    if not inapp_id:
        _error(request, 'Can not found inapp id;{member_id:%d}' % (member_id), 404)

    return {'member_id': member_id,
            'service_platform': service_platform,
            'inapp_id': inapp_id,
            'payment_id': payment_id,
            'order_id': order_id}


# 결제 효력 지급(Gateway -> MemberShip)
@app.app.route('/api/payment/effectuate', methods=['POST'])
def payment_effectuate():
    _debug(request, 'payment effectuate api requested')
   
    # verify payment information
    effectuate = _verify_payment_effectuate(request)

    # payment effectuate
    payment_id = models.purchase_effectuate(effectuate)

    # TODO: effetuate verify

    # response
    return jsonify(result='OK', payment_id=payment_id)


