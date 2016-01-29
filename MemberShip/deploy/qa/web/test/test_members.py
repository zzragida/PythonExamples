# -*- coding:utf-8 -*-

import os
import sys
sys.path.insert(0, '../')

import unittest
import simplejson as json
import membership_pb2
import utils
import models


class MembersTest(utils.TestCase):

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


  # 이미 등록된 사용자로 로그인
  def test_members_exist_member(self):
    request = self.protocol_members(udid='meRRnWrYWKvIgLgRLcUzULqe03MjzYEVWl+rHPa63NlVtCILyPvFe4M4TnvzJKcPDxmGPqBv17Bb/DT/udOzGg==')
    response = self.post('/members', data=self.make_request(request))
    assert response.status_code == 200

    res = self.make_response(response.content)
    assert res.expire_time > 0
    assert res.access_token


  # 새로운 사용자로 로그인
  def test_members_new_member(self):
    request = self.protocol_members()
    response = self.post('/members', data=self.make_request(request))
    assert response.status_code == 200

    res = self.make_response(response.content)
    assert res.expire_time > 0
    assert res.access_token
    assert res.members.member_id > 0

 
  # 새로운 사용자로그인, 서버인증 확인
  def test_members_new_member_server(self):
    request = self.protocol_members()
    response = self.post('/members', data=self.make_request(request))
    assert response.status_code == 200

    res = self.make_response(response.content)
    assert res.expire_time > 0
    assert res.access_token
    assert res.members.member_id > 0

    response = self.server_members_self(self.APP_KEY, res.access_token)
    assert response.status_code == 200
    member_id = int(json.loads(response.content)['member']['member_id'])
    assert member_id == res.members.member_id


  # 페이스북으로 로그인
  @unittest.skip(u'Need facebook access_token')
  def test_members_with_facebook(self):
    request = self.protocol_members(using_facebook=True)
    response = self.post('/members', data=self.make_request(request))
    assert response.status_code == 200

    res = self.make_response(response.content)
    assert res.expire_time > 0
    assert res.access_token
