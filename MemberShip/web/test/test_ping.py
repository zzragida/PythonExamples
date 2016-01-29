# -*- coding:utf-8 -*-

import os
import sys
sys.path.insert(0, '../')

import unittest
import membership_pb2
import utils
import models


class PingTest(utils.TestCase):

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


  def test_ping_valid_access_token(self):
    request = self.protocol_members()
    response = self.post('/members', data=self.make_request(request))
    assert response.status_code == 200

    res = self.make_response(response.content)
    assert res.expire_time > 0

    response = self.get('/ping/access_token=%s' % (res.access_token))
    assert response.status_code == 200


  def test_ping_invalid_access_token(self):
    response = self.get('/ping/access_token=invalid_token')
    assert response.status_code == 404


