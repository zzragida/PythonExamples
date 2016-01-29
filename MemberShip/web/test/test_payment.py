# -*- coding:utf-8 -*-

import os
import sys
sys.path.insert(0, '../')

import unittest
import membership_pb2
import utils
import models


class PaymentTest(utils.TestCase):

  SERVICE_PLATFORM = models.service_platform()
  PROTOCOL_VERSION = models.protocol_version()

  def setUp(self):
    app = models.app(app_id=1)
    self.APP_NAME = app['app_name']
    self.APP_KEY = app['app_key']
    self.APP_SECRET = app['app_secret']
    self.FACEBOOK_APP_ID = app['facebook_app_id']
    self.FACEBOOK_APP_SECRET = app['facebook_app_secret']
    self.FACEBOOK_API_VERSION = app['facebook_api_version']

  def tearDown(self):
    pass


  # 잘못된 inapp_id
  def test_payment_invalid_inapp_id(self):
    request = self.protocol_members()
    response = self.post('/members', data=self.make_request(request))
    assert response.status_code == 200

    res = self.make_response(response.content)
    assert res.expire_time > 0
    assert res.access_token

    # 결제진행
    inapp_id = 'ii.google.1000'
    service_platform = membership_pb2.SERVICE_PLATFORM_PLAYSTORE
    order_id = 'order_id'
    package_name = 'package_name'
    purchase_time = 1000
    purchase_state = 0
    purchase_token = 'purchase_token'
    developer_payload = 'developer_payload'
    signature = 'c2FtcGxl'

    playstore = membership_pb2.Request.Payment.PlayStore()
    playstore.order_id = order_id
    playstore.package_name = package_name
    playstore.purchase_time = purchase_time
    playstore.purchase_state = purchase_state
    playstore.purchase_token = purchase_token
    playstore.developer_payload = developer_payload
    playstore.signature = signature

    request = self.protocol_payment(res.access_token,
                                    service_platform,
                                    inapp_id,
                                    playstore = playstore)
    response = self.post('/payment', data=self.make_request(request))
    assert response.status_code != 200


  # 결제검증
  def test_payment(self):
    request = self.protocol_members()
    response = self.post('/members', data=self.make_request(request))
    assert response.status_code == 200

    res = self.make_response(response.content)
    assert res.expire_time > 0
    assert res.access_token

    # 결제진행
    inapp_id = 'sh.google.1000'
    service_platform = membership_pb2.SERVICE_PLATFORM_PLAYSTORE
    order_id = 'order_id'
    package_name = 'package_name'
    purchase_time = 1000
    purchase_state = 0
    purchase_token = 'purchase_token'
    developer_payload = 'developer_payload'
    signature = 'c2FtcGxl'

    playstore = membership_pb2.Request.Payment.PlayStore()
    playstore.order_id = order_id
    playstore.package_name = package_name
    playstore.purchase_time = purchase_time
    playstore.purchase_state = purchase_state
    playstore.purchase_token = purchase_token
    playstore.developer_payload = developer_payload
    playstore.signature = signature

    request = self.protocol_payment(res.access_token,
                                    service_platform,
                                    inapp_id,
                                    playstore = playstore)
    response = self.post('/payment', data=self.make_request(request))
    assert response.status_code == 200

    res = self.make_response(response.content)
    assert res.expire_time > 0
    assert res.access_token
    assert res.payment.payment_id > 0
    assert res.payment.inapp_id == inapp_id
    assert res.payment.developer_payload == developer_payload
    assert res.payment.purchase_token == purchase_token


  # 결제효력 지급검증
  def test_payment_effectuate(self):
    request = self.protocol_members()
    response = self.post('/members', data=self.make_request(request))
    assert response.status_code == 200

    res = self.make_response(response.content)
    assert res.expire_time > 0
    assert res.access_token
    member = res.members

    # 결제진행
    inapp_id = 'sh.google.1000'
    service_platform = membership_pb2.SERVICE_PLATFORM_PLAYSTORE
    order_id = 'order_id'
    package_name = 'package_name'
    product_sku = 'product_sku'
    purchase_time = 1000
    purchase_state = 0
    purchase_token = 'purchase_token'
    developer_payload = 'developer_payload'
    signature = 'c2FtcGxl'

    playstore = membership_pb2.Request.Payment.PlayStore()
    playstore.order_id = order_id
    playstore.package_name = package_name
    playstore.purchase_time = purchase_time
    playstore.purchase_state = purchase_state
    playstore.purchase_token = purchase_token
    playstore.developer_payload = developer_payload
    playstore.signature = signature

    request = self.protocol_payment(res.access_token,
                                    service_platform,
                                    inapp_id,
                                    playstore = playstore)
    response = self.post('/payment', data=self.make_request(request))
    assert response.status_code == 200

    res = self.make_response(response.content)
    assert res.expire_time > 0
    assert res.access_token
    payment = res.payment
    assert payment.payment_id > 0
    assert payment.inapp_id == inapp_id
    assert payment.developer_payload == developer_payload
    assert payment.purchase_token == purchase_token

    # 결제 효력지급
    effectuate = {'member_id': member.member_id,
                  'payment_id': payment.payment_id,
                  'service_platform': payment.service_platform,
                  'order_id': payment.order_id,
                  'developer_payload': payment.developer_payload,
                  'purchase_token': payment.purchase_token,
                  'inapp_id': payment.inapp_id}
    response = self.server_payment_effectuate(self.APP_KEY, effectuate)
    assert response.status_code == 200



