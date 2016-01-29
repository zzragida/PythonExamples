# -*- coding:utf-8 -*-

import os
import sys
sys.path.insert(0, '../')

import unittest
import membership_pb2
import utils
import models


class TokenTest(utils.TestCase):

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

  # 이미 등록된 사용자의 Token정보 갱신
  def test_token_exist_member(self):
    request = self.protocol_members(udid='meRRnWrYWKvIgLgRLcUzULqe03MjzYEVWl+rHPa63NlVtCILyPvFe4M4TnvzJKcPDxmGPqBv17Bb/DT/udOzGg==')
    response = self.post('/members', data=self.make_request(request))
    assert response.status_code == 200

    res = self.make_response(response.content)
    assert res.expire_time > 0
    assert res.access_token

    request = self.protocol_token(udid=request.members.udid)
    response = self.post('/token', data=self.make_request(request))
    assert response.status_code == 200


  # 새로운 멤버의 Token정보 갱신
  def test_token_new_member(self):
    request = self.protocol_members()
    response = self.post('/members', data=self.make_request(request))
    assert response.status_code == 200

    res = self.make_response(response.content)
    assert res.expire_time > 0
    assert res.access_token

    request = self.protocol_token(udid=request.members.udid)
    response = self.post('/token', data=self.make_request(request))
    assert response.status_code == 200

