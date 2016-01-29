# -*- coding:utf-8 -*-

import gateway_pb2
import common_pb2

import logging
logger = logging.getLogger('M3ARPG')
logger.setLevel(logging.DEBUG)


def dump_request(request):
  logger.debug("request: \n%s" % request)


def dump_response(response):
  logger.debug("response: \n%s" % response)
