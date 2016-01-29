# -*- coding:utf-8 -*-

from db import sqlrelay_cursor
from db import sqlrelay_close
from db import sqlrelay_client_cursor
from db import sqlrelay_client_close

from itertools import cycle
import membership_pb2


def protocol_version():
  return str(membership_pb2.Version().protocol)

def service_platform():
  return str(membership_pb2.SERVICE_PLATFORM_PLAYSTORE)

def app(app_id):
  con, cur = sqlrelay_cursor()
  cur.execute("""
SELECT
   app_name
 , app_key
 , app_secret
 , facebook_app_id
 , facebook_app_secret
 , facebook_api_version 
FROM
   ms_app 
WHERE 
   app_id = %d 
""" % (app_id))
  r = cur.fetchone()
  sqlrelay_close(cur, con)
  if not r: return None
  r = cycle(r)
  return {
    'app_name': r.next(),
    'app_key': r.next(),
    'app_secret': r.next(),
    'facebook_app_id': r.next(),
    'facebook_app_secret': r.next(),
    'facebook_api_version': r.next(),
  }


