# -*- coding:utf-8 -*-

from app import logger
from util import to_utf8
import simplejson as json
import requests

def _headers(server_api_key):
  headers = {}
  headers['Content-Type'] = u'application/json; charset=utf-8'
  headers['Authorization'] = u'key=%s' % (server_api_key)
  return headers


def send_message(gcm_url, server_api_key, token, message):
  data = '{"to":"%s","data":%s}' % (token, message)
  r = requests.post(gcm_url, headers=_headers(server_api_key), data=to_utf8(data))
  logger.debug(r.content)
  if r.status_code != 200:
    logger.error('Error to GCM Message')
  else:
    response = json.loads(r.content)
    if response['success'] == 1:
      logger.info('Success to GCM Message')
    else:
      logger.error('Failed to GCM Message')

