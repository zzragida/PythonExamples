# -*- coding:utf-8 -*-

import os
import sys
sys.path.insert(0, '../')

import unittest
import membership_pb2
import utils
import models


class HeaderTest(utils.TestCase):

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


  # 잘못된 Accept 헤더
  def test_headers_invalid_accept(self):
    headers = self.make_header(accept=u'Invalid Accept')
    response = self.get('/ping/access_token=access_token', headers=headers)
    assert response.status_code == 404


  # 잘못된 Content-Type 헤더
  def test_headers_invalid_content_type(self):
    headers = self.make_header(content_type=u'application/text')
    response = self.get('/ping/access_token=access_token', headers=headers)
    assert response.status_code == 404


  # 잘못된 User-Agent 헤더
  def test_headers_invalid_user_agent(self):
    headers = self.make_header(user_agent=self.APP_NAME)
    response = self.get('/ping/access_token=access_token', headers=headers)
    assert response.status_code == 404


  # 프로토콜 버전이 일치하지 않음
  def test_headers_mismatch_protocol_version(self):
    headers = self.make_header(user_agent=';'.join([self.APP_NAME, '10000', self.SERVICE_PLATFORM]))
    request = self.protocol_members()
    response = self.post('/members', headers=headers, data=self.make_request(request))
    assert response.status_code == 406 # Not Acceptable


  # 잘못된 digest 정보
  def test_headers_invalid_digest(self):
    headers = self.make_header(digest=u'digest')
    response = self.get('/ping/access_token=access_token', headers=headers)
    assert response.status_code == 404

