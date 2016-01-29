# -*- coding: utf-8 -*-

from itertools import cycle

from db import sqlrelay_cursor
from db import sqlrelay_close
from db import sqlrelay_client_cursor
from db import sqlrelay_client_close

from util import from_utf8
from util import to_utf8
from util import escape
from util import zero_or_one
from util import encode_base64
from util import decode_base64
from util import get_support
from util import set_support
from util import set_default

from app import logger
from app import membership_pb2

import app

from nosql import redis_monitor
from nosql import redis_member


def update_server():
    logger.info('Update server information')

    r = redis_monitor()
    if not r:
        logger.error('Can not connect monitor redis')
        return

    name = 'MEMBERSHIP:' + app.SERVICE_NAME
    info = {'ip': app.HOST, 
            'port': app.PORT, 
            'protocol_version': app.PROTOCOL_VERSION}

    pipe = r.pipeline()
    pipe.zadd('AVAIL:MEMBERSHIP', app.SERVICE_NAME, 0)
    pipe.hmset(name, info)
    pipe.expire(name, app.UPDATE_INTERVAL)
    pipe.execute()



def verify_member(member_id, access_token):
    r = redis_member(member_id)
    if not r:
        logger.error('Can not access member redis')
        return False

    # matching access_token by member_id
    if access_token != r.get(member_id):
        logger.error('Mismatch access_token and member;{member_id:%d}' % (member_id))
        return False

    # update expire time
    r.expire(member_id, app.EXPIRE_TIME)
    return True
    

def register_member(member_id, access_token):
    r = redis_member(member_id)
    if not r:
        logger.error('Can not access member redis')
        return False

    pipe = r.pipeline()
    pipe.set(member_id, to_utf8(access_token))
    pipe.expire(member_id, app.EXPIRE_TIME)
    pipe.execute()
    return True
    


def load_app(force=False):
    if app.APP_NAME and force == False: return
    # load app
    con, cur = sqlrelay_cursor()
    cur.execute("""
SELECT
   app_key
 , app_secret
 , app_name
 , support_android
 , support_ios
 , support_playstore
 , support_appstore
 , support_gameflier
 , playstore_url
 , appstore_url
 , gameflier_url
 , gcm_sender_id
 , gcm_server_api_key
 , facebook_app_id
 , facebook_app_name
 , facebook_app_secret
 , facebook_api_version
 , status 
FROM
   ms_app 
WHERE
   app_id = %d
""" % (app.APP_ID))
    result = cur.fetchone()
    assert result

    r = cycle(result)
    # validate APP_KEY and APP_SECRET
    assert app.APP_KEY == r.next()
    assert app.APP_SECRET == r.next()
    app.APP_NAME = r.next()

    # validate information by support option
    app.SUPPORT_ANDROID = get_support(r.next())
    app.SUPPORT_IOS = get_support(r.next())
    app.SUPPORT_PLAYSTORE = get_support(r.next())
    app.SUPPORT_APPSTORE = get_support(r.next())
    app.SUPPORT_GAMEFLIER = get_support(r.next())
    app.PLAYSTORE_URL = r.next()
    app.APPSTORE_URL = r.next()
    app.GAMEFLIER_URL = r.next()
    app.GCM_SENDER_ID = r.next()
    app.GCM_SERVER_API_KEY = r.next()
    app.FACEBOOK_APP_ID = r.next()
    app.FACEBOOK_APP_NAME = r.next()
    app.FACEBOOK_APP_SECRET = r.next()
    app.FACEBOOK_API_VERSION = r.next()

    # load product
    cur.execute("""
SELECT
   product_id
 , product_name
 , product_price
 , inapp_id
 , service_platform
 , currency 
FROM 
   ms_app_product 
WHERE
   app_id = %d AND status = %d 
ORDER BY
   service_platform
""" % (app.APP_ID, membership_pb2.PRODUCT_STATUS_ENABLE))
    results = cur.fetchall()
    sqlrelay_close(cur, con)

    products = {
      membership_pb2.SERVICE_PLATFORM_PLAYSTORE: [],
      membership_pb2.SERVICE_PLATFORM_APPSTORE: [],
      membership_pb2.SERVICE_PLATFORM_GAMEFLIER: [],
    }
    for r in results:
        product_id = r[0]
        product_name = r[1]
        product_price = r[2]
        inapp_id = r[3]
        service_platform = int(r[4])
        currency = int(r[5])
        products[service_platform].append({
           'product_id': product_id,
           'product_name': product_name,
           'product_price': product_price,
           'inapp_id': inapp_id,
           'currency': currency,
        })

    logger.info(products)
    app.PRODUCTS = products


def member_info(udid, 
                device_platform, 
                service_platform, 
                gcm_token = '',
                facebook_id = 0, 
                facebook_email = ''):
    con, cur = sqlrelay_client_cursor(app.DEBUG)
    cur.prepareQuery('CALL member_info(?, ?, ?, ?, ?, ?, ?, ?)')
    cur.inputBind('1', app.APP_ID)
    cur.inputBind('2', to_utf8(udid))
    cur.inputBind('3', device_platform)
    cur.inputBind('4', service_platform)
    cur.inputBind('5', gcm_token)
    cur.inputBind('6', facebook_id)
    cur.inputBind('7', to_utf8(facebook_email))
    cur.inputBind('8', membership_pb2.MEMBER_STATUS_NORMAL)
    cur.executeQuery()
    member_id = cur.getFieldAsInteger(0, 0)
    if member_id <= 0: 
        sqlrelay_client_close(cur, con)
        return None

    cur.clearBinds()

    # 로그인 로그저장
    cur.sendQuery("""
INSERT INTO ms_member_history (
   app_id
 , member_id
 , category
 , `int0`
 , `int1`
 , `int2`
 , str0 
) VALUES (
   %d
 , %d
 , %d
 , %d
 , %d
 , %d
 , '%s'
)""" % (app.APP_ID, member_id, membership_pb2.HISTORY_MEMBER_ACCESS,
        device_platform, service_platform, facebook_id, udid))

    # 미완료 결제정보
    cur.sendQuery("""
SELECT
   service_platform
 , payment_id
 , inapp_order_id
 , inapp_developer_payload
 , inapp_purchase_token
 , inapp_product_sku 
FROM
   ms_app_payment 
WHERE 
   member_id = %d AND app_id = %d AND status = %d
""" % (member_id, app.APP_ID, membership_pb2.PAYMENT_STATUS_PURCHASED))
    sqlrelay_client_close(cur, con)

    payments = []
    for row in range(0, cur.rowCount()):
        payments.append({
           'service_platform': cur.getFieldAsInteger(row, 0),
           'payment_id': cur.getFieldAsInteger(row, 1),
           'order_id': cur.getField(row, 2),
           'developer_payload': cur.getField(row, 3),
           'purchase_token': cur.getField(row, 4),
           'inapp_id': cur.getField(row, 5)
        })
    return member_id, payments



def member_id(udid, device_platform, service_platform):
    con, cur = sqlrelay_cursor()
    cur.execute("""
SELECT 
   member_id 
FROM
   ms_member 
WHERE 
   app_id = %d AND 
   udid = '%s' AND 
   device_platform = %d AND
   service_platform = %d
""" % (app.APP_ID, udid, device_platform, service_platform))
    r = cur.fetchone()
    sqlrelay_close(cur, con)
    if not r:
        return None
    return r[0]


def purchase(member_id, product, payment):
    inapp_id = payment.inapp_id
    service_platform = payment.service_platform
    appstore_name = ''
    receipt = ''

    if payment.playstore:
        order_id = payment.playstore.order_id
        package_name = payment.playstore.package_name
        purchase_time = payment.playstore.purchase_time
        purchase_state = payment.playstore.purchase_state
        purchase_token = payment.playstore.purchase_token
        developer_payload = payment.playstore.developer_payload
        signature = payment.playstore.signature
    elif payment.appstore:
        # TODO: setting for appstore
        return None
    elif payment.gameflier:
        # TODO: setting for gameflier
        return None
    else:
        return None

    con, cur = sqlrelay_client_cursor(app.DEBUG)
    cur.prepareQuery('CALL purchase(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
    cur.inputBind('1', app.APP_ID)
    cur.inputBind('2', member_id)
    cur.inputBind('3', product['product_id'])
    cur.inputBind('4', service_platform)
    cur.inputBind('5', product['product_price'])
    cur.inputBind('6', order_id)
    cur.inputBind('7', package_name)
    cur.inputBind('8', inapp_id)
    cur.inputBind('9', purchase_time)
    cur.inputBind('10', purchase_state)
    cur.inputBind('11', purchase_token)
    cur.inputBind('12', developer_payload)
    cur.inputBind('13', signature)
    cur.inputBind('14', appstore_name)
    cur.inputBind('15', receipt)
    cur.inputBind('16', membership_pb2.PAYMENT_STATUS_PURCHASED)
    cur.executeQuery()
    payment_id = cur.getFieldAsInteger(0, 0)

    cur.clearBinds()

    # 구매이력 저장
    cur.sendQuery("""
INSERT INTO ms_member_history (
   app_id
 , member_id
 , category
 , `int0`
 , `int1`
 , `int2`
 , str0
) VALUES (
   %d
 , %d
 , %d
 , %d
 , %d
 , %d
 , '%s'
)""" % (app.APP_ID, member_id, membership_pb2.HISTORY_MEMBER_PAYMENT,
        service_platform, membership_pb2.PAYMENT_STATUS_PURCHASED, payment_id,
        inapp_id))

    sqlrelay_client_close(cur, con)
    return payment_id if payment_id > 0 else None


def purchase_effectuate(effectuate):
    member_id = effectuate['member_id']
    payment_id = effectuate['payment_id']
    order_id = effectuate['order_id']
    service_platform = effectuate['service_platform']
    inapp_id = effectuate['inapp_id']

    con, cur = sqlrelay_client_cursor(app.DEBUG)
    cur.prepareQuery('CALL purchase_effectuate(?,?,?,?,?,?)')
    cur.inputBind('1', app.APP_ID)
    cur.inputBind('2', member_id)
    cur.inputBind('3', payment_id)
    cur.inputBind('4', order_id)
    cur.inputBind('5', membership_pb2.PAYMENT_STATUS_PURCHASED)
    cur.inputBind('6', membership_pb2.PAYMENT_STATUS_EFFECTUATED)
    cur.executeQuery()
    payment_id = cur.getFieldAsInteger(0, 0)

    cur.clearBinds()
    
    # 효력지급이력 저장
    cur.sendQuery("""
INSERT INTO ms_member_history (
   app_id
 , member_id
 , category
 , `int0`
 , `int1`
 , `int2`
 , str0
) VALUES (
   %d
 , %d
 , %d
 , %d
 , %d
 , %d
 , '%s'
)""" % (app.APP_ID, member_id, membership_pb2.HISTORY_MEMBER_PAYMENT,
        service_platform, membership_pb2.PAYMENT_STATUS_EFFECTUATED, payment_id,
        inapp_id))

    sqlrelay_client_close(cur, con)
    return payment_id if payment_id > 0 else None


def push_notification(member_id):
    # TODO: query member push notification with cache
    con, cur = sqlrelay_cursor()
    cur.execute("""
SELECT 
  push_notification 
FROM 
  ms_member 
WHERE 
  member_id = %d AND app_id = %d
""" % (member_id, app.APP_ID))
    r = cur.fetchone()
    sqlrelay_close(cur, con)
    if not r:
        return None
    return True if r[0] == '1' else False


def toggle_push_notification(member_id):
    con, cur = sqlrelay_client_cursor(app.DEBUG)
    cur.prepareQuery('CALL member_push_notification(?,?)')
    cur.inputBind('1', app.APP_ID)
    cur.inputBind('2', member_id)
    cur.executeQuery()
    push_notification = cur.getField(0, 0)

    cur.clearBinds()

    # 푸시설정이력 저장
    cur.sendQuery("""
INSERT INTO ms_member_history (
   app_id
 , member_id
 , category
 , `int0` 
) VALUES (
   %d
 , %d
 , %d
 , %d
)""" % (app.APP_ID, member_id, 
        membership_pb2.HISTORY_MEMBER_PUSH, int(push_notification)))

    sqlrelay_client_close(cur, con)
    if not push_notification:
        return None
    return True if push_notification == '1' else False




