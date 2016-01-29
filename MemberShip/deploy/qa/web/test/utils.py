# -*- coding: utf-8 -*-

import os
import unittest
import datetime
import hashlib
import base64
import requests
import membership_pb2
import models

URL = 'http://10.30.76.13:7200/api'
EPOCH = datetime.datetime(year=1970, month=1, day=1)

class TestCase(unittest.TestCase):

  def make_header(self, 
                  accept=None, 
                  content_type=None, 
                  user_agent=None, 
                  timestamp=None,
                  digest=None):
    headers = {}
    if not accept: accept = u'text/plain'
    headers['Accept'] = accept if accept else u'text/plain'

    if not content_type: content_type = u'application/json'
    headers['Content-Type'] = content_type

    if not user_agent: user_agent = ';'.join([self.APP_NAME, self.PROTOCOL_VERSION, self.SERVICE_PLATFORM])
    headers['User-Agent'] = user_agent

    if not timestamp:
      now = datetime.datetime.utcnow()
      timestamp = str(long((now - EPOCH).total_seconds()))
    headers['Timestamp'] = timestamp

    if not digest:
      h = hashlib.sha1()
      h.update(timestamp + self.APP_SECRET)
      digest = h.hexdigest()
    headers['Digest'] = digest
    return headers

  def make_request(self, request):
    return self.encode_base64(request.SerializeToString())

  def make_response(self, content):
    res = membership_pb2.Response()
    res.ParseFromString(self.decode_base64(content))
    return res

  def post(self, prefix, headers=None, data=None):
    url = URL + prefix
    if not headers: headers = self.make_header()
    return requests.post(url, data=data, headers=headers)

  def get(self, prefix, headers=None, params=None):
    url = URL + prefix
    if not headers: headers = self.make_header()
    return requests.get(url, params=params, headers=headers)

  def encode_base64(self, data):
    return base64.b64encode(data)

  def decode_base64(self, data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
      data += b'='* missing_padding
    return base64.b64decode(data)

  def protocol_members(self, app_key=None, udid=None, device=None, service=None, using_facebook=False):
    request = membership_pb2.Request()
    request.type = membership_pb2.MEMBERS
    if not app_key: app_key = self.APP_KEY
    request.members.app_key = app_key
    if not udid: udid = self.encode_base64(os.urandom(64))
    request.members.udid = udid
    if not device: device = membership_pb2.DEVICE_PLATFORM_ANDROID
    request.members.device_platform = device
    if not service: service = membership_pb2.SERVICE_PLATFORM_PLAYSTORE
    request.members.service_platform = service
    if using_facebook:
      graph = facebook.GraphAPI(access_token=self.FACEBOOK_ACCESS_TOKEN,
                                version=self.FACEBOOK_API_VERSION)
      user = graph.get_object('me')
      request.members.facebook.id = long(user['id'])
      request.members.facebook.access_token = self.FACEBOOK_ACCESS_TOKEN
    return request

  def protocol_token(self, app_key=None, udid=None, device=None, service=None):
    request = membership_pb2.Request()
    request.type = membership_pb2.TOKEN
    if not app_key: app_key = self.APP_KEY
    request.token.app_key = app_key
    if not udid: udid = self._encode_base64(os.urandom(64))
    request.token.udid = udid
    if not device: device = membership_pb2.DEVICE_PLATFORM_ANDROID
    request.token.device_platform = device
    if not service: service = membership_pb2.SERVICE_PLATFORM_PLAYSTORE
    request.token.service_platform = service
    return request

  def protocol_push_allow(self, access_token):
    request = membership_pb2.Request()
    request.type = membership_pb2.PUSH_ALLOW
    request.push_allow.access_token = access_token
    return request

  def protocol_payment(self, access_token, service_platform, inapp_id,
                       playstore = None, appstore = None, gameflier = None):
    request = membership_pb2.Request()
    request.type = membership_pb2.PAYMENT
    request.payment.access_token = access_token
    request.payment.service_platform = service_platform
    request.payment.inapp_id = inapp_id
    if playstore:
      request.payment.playstore.CopyFrom(playstore)
    if appstore:
      request.payment.appstore.CopyFrom(appstore)
    if gameflier:
      request.paymene.gameflier.CopyFrom(gameflier)
    return request


  def server_members_self(self, app_key, access_token):
    url = URL + '/members/self'
    payload = {'app_key':app_key, 'access_token':access_token}
    return requests.post(url, data=payload)

  def server_push(self, app_key, member_ids, message, time):
    url = URL + '/push'
    payload = {'app_key':app_key, 'member_ids':member_ids, 'message':message, 'time':time}
    return requests.post(url, data=payload)

  def server_payment_effectuate(self, app_key, effectuate):
    url = URL + '/payment/effectuate'
    payload = {'app_key': app_key, 
               'member_id': effectuate['member_id'],
               'payment_id': effectuate['payment_id'],
               'service_platform': effectuate['service_platform'],
               'order_id': effectuate['order_id'],
               'developer_payload': effectuate['developer_payload'],
               'purchase_token': effectuate['purchase_token'],
               'inapp_id': effectuate['inapp_id']}
    return requests.post(url, data=payload)



