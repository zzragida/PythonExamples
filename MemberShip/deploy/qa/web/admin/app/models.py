# -*- coding: utf-8 -*-

import hashlib
import uuid
import os
from itertools import cycle

from db import sqlrelay_cursor
from db import sqlrelay_close
from db import sqlrelay_client_cursor
from db import sqlrelay_client_close

from nosql import redis_members
from nosql import redis_monitor

from util import from_utf8
from util import to_utf8
from util import escape
from util import zero_or_one
from util import encode_base64
from util import decode_base64
from util import get_support
from util import set_support
from util import set_default
from util import dict_item
from util import dict_item_index
from util import dict_item_choices

from config import ADMIN_UPLOAD_PATH as UPLOAD_PATH
from config import PER_PAGE

import app
import membership_pb2
import requests
import simplejson as json

APP_STATUS = {
  membership_pb2.APP_STATUS_DISABLE: 'Disable',
  membership_pb2.APP_STATUS_ENABLE: 'Enable',
}

def _app_status(status):
    return dict_item(APP_STATUS, status)

def app_status_index(status):
    return dict_item_index(APP_STATUS, status)

def app_status_choices():
    return dict_item_choices(APP_STATUS)


PRODUCT_STATUS = {
  membership_pb2.PRODUCT_STATUS_DISABLE: 'Disable',
  membership_pb2.PRODUCT_STATUS_ENABLE: 'Enable',
}

def _product_status(status):
    return dict_item(PRODUCT_STATUS, status)

def product_status_index(status):
    return dict_item_index(PRODUCT_STATUS, status)

def product_status_choices():
    return dict_item_choices(PRODUCT_STATUS)


PAYMENT_STATUS = {
  membership_pb2.PAYMENT_STATUS_PURCHASED: 'Purchased',
  membership_pb2.PAYMENT_STATUS_CANCELED: 'Canceled',
  membership_pb2.PAYMENT_STATUS_EFFECTUATED: 'Effectuated',
}

def _payment_status(status):
    return dict_item(PAYMENT_STATUS, status)

def payment_status_index(status):
    return dict_item_index(PAYMENT_STATUS, status)

def payment_status_choices():
    return dict_item_choices(PAYMENT_STATUS)


FACEBOOK_API_VERSIONS = {
  0: '2.0',
  1: '2.1',
  2: '2.2',
  3: '2.3',
}

def facebook_api_version_value(choice):
    return dict_item(FACEBOOK_API_VERSIONS, choice)

def facebook_api_version_index(version):
    return dict_item_index(FACEBOOK_API_VERSIONS, version)

def facebook_api_version_choices():
    return dict_item_choices(FACEBOOK_API_VERSIONS)


CURRENCY_TYPES = {
  membership_pb2.CURRENCY_USD: u"USD",
  membership_pb2.CURRENCY_KRW: u"KRW",
  membership_pb2.CURRENCY_JPY: u"JPY",
  membership_pb2.CURRENCY_TWD: u"TWD",
}

def _currency_type(currency):
    return dict_item(CURRENCY_TYPES, currency)

def currency_type_index(currency):
    return dict_item_index(CURRENCY_TYPES, currency)

def currency_type_choices():
    return dict_item_choices(CURRENCY_TYPES)


MEMBER_STATUS = {
  membership_pb2.MEMBER_STATUS_INIT: 'Initialized',
  membership_pb2.MEMBER_STATUS_NORMAL: 'Normal',
  membership_pb2.MEMBER_STATUS_BLOCKED: 'Blocked',
  membership_pb2.MEMBER_STATUS_DROP_OUT: 'Drop Out',
}

def _member_status(status):
    return dict_item(MEMBER_STATUS, status)

def member_status_index(status):
    return dict_item_index(MEMBER_STATUS, status)

def member_status_choices():
    return dict_item_choices(MEMBER_STATUS)


DEVICE_PLATFORMS = {
  membership_pb2.DEVICE_PLATFORM_ANDROID: 'Android',
  membership_pb2.DEVICE_PLATFORM_IOS: 'iOS',
}

def _device_platform(device):
    return dict_item(DEVICE_PLATFORMS, device)

def device_platform_index(device):
    return dict_item_index(DEVICE_PLATFORMS, device)

def device_platform_choices():
    return dict_item_choices(DEVICE_PLATFORMS)


SERVICE_PLATFORMS = {
  membership_pb2.SERVICE_PLATFORM_PLAYSTORE: 'PlayStore',
  membership_pb2.SERVICE_PLATFORM_APPSTORE: 'AppStore',
  membership_pb2.SERVICE_PLATFORM_GAMEFLIER: 'GameFlier',
}

def _service_platform(service):
    return dict_item(SERVICE_PLATFORMS, service)

def service_platform_index(service):
    return dict_item_index(SERVICE_PLATFORMS, service)

def service_platform_choices():
    return dict_item_choices(SERVICE_PLATFORMS)


def auto_created():
    return 'Auto Created'



def admins():
    con, cur = sqlrelay_cursor()
    cur.execute("""
SELECT
   admin_id
 , password
 , access_apps 
 , DATE_FORMAT(reg_date, '%Y/%m/%d/ %H:%i:%s') 
FROM 
   ms_admin 
ORDER BY 
   reg_date
""")
    results = cur.fetchall()
    sqlrelay_close(cur, con)

    admins = []
    for r in results:
        admins.append({
          'admin_id': r[0],
          'password': r[1],
          'access_apps': r[2],
          'reg_date': r[3],
        })
    return admins



def avaliable_admin(admin_id, password):
    admin = None
    con, cur = sqlrelay_cursor()
    cur.execute("""
SELECT 
   COUNT(0) 
FROM
   ms_admin 
WHERE
   admin_id = '%s' AND PASSWORD = PASSWORD('%s')
""" % (escape(from_utf8(admin_id)), escape(from_utf8(password))))

    if int(cur.fetchone()[0]) == 1:
        admin = admin_id

    sqlrelay_close(cur, con)
    return admin



def apps():
    con, cur = sqlrelay_cursor()
    cur.execute("""
SELECT 
   app_id
 , app_key
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
 , gcm_config_path
 , facebook_app_name
 , facebook_app_id
 , facebook_app_secret
 , facebook_api_version
 , status
 , DATE_FORMAT(reg_date, '%Y/%m/%d/ %H:%i:%s') 
FROM
   ms_app 
ORDER BY
   app_id
""")
    results = cur.fetchall()
    sqlrelay_close(cur, con)

    apps = []
    for r in results:
        apps.append(_app_make_result(r))
    return apps


def apps_detail(app_id):
    con, cur = sqlrelay_cursor()
    cur.execute("""
SELECT 
   app_id
 , app_key
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
 , gcm_config_path
 , facebook_app_name
 , facebook_app_id
 , facebook_app_secret
 , facebook_api_version
 , status
 , DATE_FORMAT(reg_date, '%%Y/%%m/%%d/ %%H:%%i:%%s') 
FROM
   ms_app 
WHERE
   app_id = %d
""" % (app_id))
    r = cur.fetchone()
    sqlrelay_close(cur, con)

    if not r:
        return None

    return _app_make_result(r)


def _hash_app_key(app_name):
    ''' 
       Hash application key 
       SHA1
       - update application name
       - update uuid
    '''
    h = hashlib.sha1()
    h.update(app_name)
    h.update(str(uuid.uuid4()))
    return h.hexdigest()


def _hash_app_secret(app_key):
    '''
       Hash application secret
       SHA256
       - update application key
       - update uuid
    '''
    h = hashlib.sha256()
    h.update(app_key)
    h.update(str(uuid.uuid4()))
    return h.hexdigest()


def apps_new(form):
    app_key = _hash_app_key(form.app_name.data)
    app_secret = _hash_app_secret(app_key)
    app_name = set_default(form.app_name.data)
    support_android = set_support(form.support_android.data)
    support_ios = set_support(form.support_ios.data)
    support_playstore = set_support(form.support_playstore.data)
    support_appstore = set_support(form.support_appstore.data)
    support_gameflier = set_support(form.support_gameflier.data)
    playstore_url = set_default(form.playstore_url.data)
    appstore_url = set_default(form.appstore_url.data)
    gameflier_url = set_default(form.gameflier_url.data)
    gcm_sender_id = set_default(form.gcm_sender_id.data)
    gcm_server_api_key = set_default(form.gcm_server_api_key.data)
    gcm_config_path = ''
    if form.gcm_config_path.data:
        gcm_config_path = to_utf8(form.gcm_config_path.data.filename)
    facebook_app_name = set_default(form.facebook_app_name.data)
    facebook_app_id = set_default(form.facebook_app_id.data)
    facebook_app_secret = set_default(form.facebook_app_secret.data)
    facebook_api_version = facebook_api_version_value(form.facebook_api_version.data)
    status = form.status.data

    con, cur = sqlrelay_client_cursor()
    cur.prepareQuery('CALL create_app(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
    cur.inputBind("1", app_key)
    cur.inputBind("2", app_secret)
    cur.inputBind("3", app_name)
    cur.inputBind("4", support_android)
    cur.inputBind("5", support_ios)
    cur.inputBind("6", support_playstore)
    cur.inputBind("7", support_appstore)
    cur.inputBind("8", support_gameflier)
    cur.inputBind("9", playstore_url)
    cur.inputBind("10", appstore_url)
    cur.inputBind("11", gameflier_url)
    cur.inputBind("12", gcm_sender_id)
    cur.inputBind("13", gcm_server_api_key)
    cur.inputBind("14", gcm_config_path)
    cur.inputBind("15", facebook_app_id)
    cur.inputBind("16", facebook_app_name)
    cur.inputBind("17", facebook_app_secret)
    cur.inputBind("18", facebook_api_version)
    cur.inputBind("19", status)
    cur.executeQuery()
    app_id = cur.getField(0,0)
    sqlrelay_client_close(cur, con)

    if form.gcm_config_path.data:
        # GCM Config 파일저장
        _app_save_file(form.gcm_config_path.data, app_id)


def apps_edit(form):
    app_id = form.app_id.data
    app_name = set_default(form.app_name.data)
    support_android = set_support(form.support_android.data)
    support_ios = set_support(form.support_ios.data)
    support_playstore = set_support(form.support_playstore.data)
    support_appstore = set_support(form.support_appstore.data)
    support_gameflier = set_support(form.support_gameflier.data)
    playstore_url = set_default(form.playstore_url.data)
    appstore_url = set_default(form.appstore_url.data)
    gameflier_url = set_default(form.gameflier_url.data)
    gcm_sender_id = set_default(form.gcm_sender_id.data)
    gcm_server_api_key = set_default(form.gcm_server_api_key.data)
    gcm_config_path = _app_save_file(form.gcm_config_path.data, app_id)
    facebook_app_name = set_default(form.facebook_app_name.data)
    facebook_app_id = set_default(form.facebook_app_id.data)
    facebook_app_secret = set_default(form.facebook_app_secret.data)
    facebook_api_version = facebook_api_version_value(form.facebook_api_version.data)
    status = form.status.data

    con, cur = sqlrelay_client_cursor()
    cur.prepareQuery('CALL update_app(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
    cur.inputBind("1", app_id)
    cur.inputBind("2", app_name)
    cur.inputBind("3", support_android)
    cur.inputBind("4", support_ios)
    cur.inputBind("5", support_playstore)
    cur.inputBind("6", support_appstore)
    cur.inputBind("7", support_gameflier)
    cur.inputBind("8", playstore_url)
    cur.inputBind("9", appstore_url)
    cur.inputBind("10", gameflier_url)
    cur.inputBind("11", gcm_sender_id)
    cur.inputBind("12", gcm_server_api_key)
    cur.inputBind("13", gcm_config_path)
    cur.inputBind("14", facebook_app_id)
    cur.inputBind("15", facebook_app_name)
    cur.inputBind("16", facebook_app_secret)
    cur.inputBind("17", facebook_api_version)
    cur.inputBind("18", status)
    cur.executeQuery()
    sqlrelay_client_close(cur, con)


def apps_delete(app_id):
    con, cur = sqlrelay_cursor()
    cur.execute("DELETE FROM ms_app WHERE app_id = %d" % (app_id))
    sqlrelay_close(cur, con)



def _app_make_result(result):
    r = cycle(result)
    return {
       'app_id': r.next(),
       'app_key': r.next(),
       'app_secret': r.next(),
       'app_name': from_utf8(r.next()),
       'support_android': get_support(r.next()),
       'support_ios': get_support(r.next()),
       'support_playstore': get_support(r.next()),
       'support_appstore': get_support(r.next()),
       'support_gameflier': get_support(r.next()),
       'playstore_url': r.next(),
       'appstore_url': r.next(),
       'gameflier_url': r.next(),
       'gcm_sender_id': r.next(),
       'gcm_server_api_key': r.next(),
       'gcm_config_path': r.next(),
       'facebook_app_name': r.next(),
       'facebook_app_id': r.next(),
       'facebook_app_secret': r.next(),
       'facebook_api_version': r.next(),
       'status': _app_status(r.next()),
       'reg_date': r.next(),
    }


def _app_save_file(upload_file, app_id):
    if not upload_file: return ''
    upload_path = os.path.join(UPLOAD_PATH, str(app_id))
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    file = upload_file
    file.save(os.path.join(upload_path, file.filename))
    return to_utf8(file.filename)


def products(app_id):
    con, cur = sqlrelay_cursor()
    cur.execute("""
SELECT 
   app_id
 , product_id
 , product_name
 , product_detail
 , product_price
 , inapp_id
 , service_platform
 , currency
 , status
 , DATE_FORMAT(reg_date, '%%Y/%%m/%%d/ %%H:%%i:%%s') 
FROM
   ms_app_product 
WHERE 
   app_id = %d 
ORDER BY
   product_id
""" % (app_id))
    results = cur.fetchall()
    sqlrelay_close(cur, con)

    products = []
    for r in results:
        products.append(_product_make_result(r))
    return products


def products_detail(app_id, product_id):
    con, cur = sqlrelay_cursor()
    cur.execute("""
SELECT 
   app_id
 , product_id
 , product_name
 , product_detail
 , product_price
 , inapp_id
 , service_platform
 , currency
 , status
 , DATE_FORMAT(reg_date, '%%Y/%%m/%%d/ %%H:%%i:%%s') 
FROM
   ms_app_product 
WHERE 
   product_id = %d AND app_id = %d
""" % (product_id, app_id))
    r = cur.fetchone()
    sqlrelay_close(cur, con)

    if not r:
        return None

    return _product_make_result(r)


def products_new(form):
    app_id = int(form.app_id.data)
    product_name = set_default(form.product_name.data)
    product_detail = set_default(form.product_detail.data)
    product_price = set_default(form.product_price.data)
    inapp_id = set_default(form.inapp_id.data)
    service_platform = int(form.service_platform.data)
    currency = int(form.currency.data)
    status = int(form.status.data)

    con, cur = sqlrelay_cursor()
    cur.execute("""
INSERT INTO ms_app_product (
   app_id
 , product_name
 , product_detail
 , product_price
 , inapp_id
 , service_platform
 , currency
 , status
) VALUES (
   %d
 , '%s'
 , '%s'
 , '%s'
 , '%s'
 , %d
 , %d
 , %d
)""" % (app_id, product_name, product_detail, product_price, inapp_id, service_platform, currency, status))
    sqlrelay_close(cur, con)


def products_edit(form):
    app_id = int(form.app_id.data)
    product_id = int(form.product_id.data)
    product_name = set_default(form.product_name.data)
    product_detail = set_default(form.product_detail.data)
    product_price = set_default(form.product_price.data)
    inapp_id = set_default(form.inapp_id.data)
    service_platform = int(form.service_platform.data)
    currency = int(form.currency.data)
    status = int(form.status.data)

    con, cur = sqlrelay_cursor()
    cur.execute("""
UPDATE ms_app_product SET
   product_name = '%s'
 , product_detail = '%s'
 , product_price = '%s'
 , inapp_id = '%s'
 , service_platform = %d
 , currency = %d
 , status = %d 
WHERE 
   product_id = %d AND app_id = %d
""" % (product_name, product_detail, product_price, inapp_id, service_platform, currency, status, product_id, app_id))
    sqlrelay_close(cur, con)


def products_delete(app_id, product_id):
    con, cur = sqlrelay_cursor()
    cur.execute("DELETE FROM ms_app_product WHERE product_id = %d AND app_id = %d" % (product_id, app_id))
    sqlrelay_close(cur, con)


def _product_make_result(result):
    r = cycle(result)
    return {
       'app_id': r.next(),
       'product_id': r.next(),
       'product_name': from_utf8(r.next()),
       'product_detail': from_utf8(r.next()),
       'product_price': from_utf8(r.next()),
       'inapp_id': from_utf8(r.next()),
       'service_platform': _service_platform(r.next()),
       'currency': _currency_type(r.next()),
       'status': _product_status(r.next()),
       'reg_date': r.next(),
    }


def payments(app_id, page, member_id=None, product_id=None):
    condition = 'app_id = %d' % (app_id)
    if member_id:
        condition += ' AND member_id = %d' % (member_id)
    if product_id:
        condition += ' AND product_id = %d' % (product_id)

    con, cur = sqlrelay_cursor()
    cur.execute('SELECT COUNT(0) FROM ms_app_payment WHERE %s' % (condition))
    total = int(cur.fetchone()[0])
    cur.execute("""
SELECT 
   app_id
 , member_id
 , product_id
 , payment_id
 , service_platform
 , product_price
 , inapp_order_id
 , inapp_package_name
 , inapp_product_sku
 , inapp_purchase_time
 , inapp_purchase_state
 , inapp_purchase_token
 , inapp_developer_payload
 , inapp_signature
 , inapp_appstore_name
 , inapp_receipt
 , status
 , DATE_FORMAT(reg_date, '%%Y/%%m/%%d/ %%H:%%i:%%s') 
FROM
   ms_app_payment 
WHERE 
   %s 
ORDER BY
   reg_date DESC 
LIMIT
   %d, %d 
""" % (condition, (page*PER_PAGE), ((page+1)*PER_PAGE)))
    results = cur.fetchall()
    sqlrelay_close(cur, con)

    payments = []
    for r in results:
        payments.append(_payment_make_result(r))
    return total, payments


def payments_detail(app_id, payment_id):
    con, cur = sqlrelay_cursor()
    cur.execute("""
SELECT 
   app_id
 , member_id
 , product_id
 , payment_id
 , service_platform
 , product_price
 , inapp_order_id
 , inapp_package_name
 , inapp_product_sku
 , inapp_purchase_time
 , inapp_purchase_state
 , inapp_purchase_token
 , inapp_developer_payload
 , inapp_signature
 , inapp_appstore_name
 , inapp_receipt
 , status
 , DATE_FORMAT(reg_date, '%%Y/%%m/%%d/ %%H:%%i:%%s') 
FROM
   ms_app_payment 
WHERE 
   payment_id = %d AND app_id = %d
""" % (payment_id, app_id))
    r = cur.fetchone()
    sqlrelay_close(cur, con)

    if not r:
        return None

    return _payment_make_result(r)


def _payment_make_result(result):
    r = cycle(result)
    return {
       'app_id': r.next(),
       'member_id': r.next(),
       'product_id': r.next(),
       'payment_id': r.next(),
       'service_platform': _service_platform(r.next()),
       'product_price': r.next(),
       'inapp_order_id': r.next(),
       'inapp_package_name': r.next(),
       'inapp_product_sku': r.next(),
       'inapp_purchase_time': r.next(),
       'inapp_purchase_state': r.next(),
       'inapp_purchase_token': r.next(),
       'inapp_developer_payload': r.next(),
       'inapp_signature': r.next(),
       'inapp_appstore_name': r.next(),
       'inapp_receipt': r.next(),
       'status': _payment_status(r.next()),
       'reg_date': r.next(),
    }


def members(app_id, page, member_id=None, facebook_id=None):
    condition = 'app_id = %d' % (app_id)
    if member_id:
        condition += ' AND member_id = %d' % (member_id)
    if facebook_id:
        condition += ' AND facebook_id = %d' % (facebook_id)

    con, cur = sqlrelay_cursor()
    cur.execute('SELECT COUNT(0) FROM ms_member WHERE %s' % (condition))
    total = int(cur.fetchone()[0])
    cur.execute("""
SELECT 
   app_id
 , member_id
 , udid
 , device_platform
 , service_platform
 , push_notification
 , gcm_token
 , facebook_id
 , facebook_email
 , status
 , DATE_FORMAT(reg_date, '%%Y/%%m/%%d/ %%H:%%i:%%s') 
 , last_device_platform
 , last_service_platform
 , DATE_FORMAT(last_login_date, '%%Y/%%m/%%d/ %%H:%%i:%%s') 
FROM 
   ms_member 
WHERE
   %s
ORDER BY 
   member_id 
LIMIT
   %d, %d
""" % (condition, (page*PER_PAGE), ((page+1)*PER_PAGE)))
    results = cur.fetchall()

    members = []
    for r in results:
        members.append(_member_make_result(r))
    return total, members


def members_detail(app_id, member_id):
    con, cur = sqlrelay_cursor()
    cur.execute("""
SELECT 
   app_id
 , member_id
 , udid
 , device_platform
 , service_platform
 , push_notification
 , gcm_token
 , facebook_id
 , facebook_email
 , status
 , DATE_FORMAT(reg_date, '%%Y/%%m/%%d/ %%H:%%i:%%s') 
 , last_device_platform
 , last_service_platform
 , DATE_FORMAT(last_login_date, '%%Y/%%m/%%d/ %%H:%%i:%%s') 
FROM 
   ms_member 
WHERE
   member_id = %d AND app_id = %d 
""" % (member_id, app_id))
    r = cur.fetchone()
    sqlrelay_close(cur, con)

    if not r:
        return None

    return _member_make_result(r)



def members_history(app_id, member_id):
    con, cur = sqlrelay_cursor()
    # 시스템 접근
    access = member_history_category(app_id, member_id, membership_pb2.HISTORY_MEMBER_ACCESS, cur)

    # 결제정보
    payment = member_history_category(app_id, member_id, membership_pb2.HISTORY_MEMBER_PAYMENT, cur)

    # 푸시설정
    push = member_history_category(app_id, member_id, membership_pb2.HISTORY_MEMBER_PUSH, cur)

    sqlrelay_close(cur, con)
    return access, payment, push


def member_history_category(app_id, member_id, category, cur):
    cur.execute("""
SELECT 
   `int0`
 , `int1`
 , `int2` 
 , `int3`
 , `int4`
 , str0 
 , reg_date 
FROM
  ms_member_history 
WHERE
  member_id = %d AND app_id = %d AND category = %d
""" % (member_id, app_id, category))
    results = cur.fetchall()

    historys = []
    for r in results:
        historys.append(_member_history_make_result(category, r))
    return historys


def _member_history_make_result(category, r):
    if category == membership_pb2.HISTORY_MEMBER_ACCESS:
        return {
           'int0': _device_platform(int(r[0])),
           'int1': _service_platform(int(r[1])),
           'int2': r[2],
           'str0': r[5],
           'reg_date': r[6]
        }

    elif category == membership_pb2.HISTORY_MEMBER_PAYMENT:
        return {
           'int0': _service_platform(int(r[0])),
           'int1': _payment_status(int(r[1])),
           'str0': r[5],
           'reg_date': r[6]
        }

    elif category == membership_pb2.HISTORY_MEMBER_PUSH:
        return {
           'int0': True if r[0] == '1' else False,
           'reg_date': r[6]
        }

    return {}


def _facebook_id(facebook_id):
    if not facebook_id: return ''
    facebook_id = int(facebook_id)
    return facebook_id if facebook_id > 0 else ''


def _member_make_result(result):
    r = cycle(result)
    return {
       'app_id': r.next(),
       'member_id': r.next(),
       'udid': r.next(),
       'device_platform': _device_platform(r.next()),
       'service_platform': _service_platform(r.next()),
       'push_notification': get_support(r.next()),
       'gcm_token': r.next(),
       'facebook_id': _facebook_id(r.next()),
       'facebook_email': r.next(),
       'status': _member_status(r.next()),
       'reg_date': r.next(),
       'last_device_platform': _device_platform(r.next()),
       'last_service_platform': _service_platform(r.next()),
       'last_login_date': r.next(),
    }


# 멤버쉽 서버정보
def get_memberships():
    memberships = {}

    r = redis_monitor()
    count = r.zcard('AVAIL:MEMBERSHIP')
    if count > 0:
        scores = r.zrange('AVAIL:MEMBERSHIP', 0, count - 1, withscores=True)

        for ms in scores:
            membership = {'name': ms[0], 'usage': ms[1]}
            name = 'MEMBERSHIP:' + ms[0]
            fields = r.hmget(name, 'ip', 'port', 'protocol_version')
            if not fields[0]:
                r.zrem('AVAIL:MEMBERSHIP', ms[0])
                continue

            membership['ip'] = fields[0]
            membership['port'] = fields[1]
            membership['protocol_version'] = fields[2]

            memberships[ms[0]] = membership

    return memberships


# 푸시 서버정보
def get_pushs():
    pushs = {}

    r = redis_monitor()
    count = r.zcard('AVAIL:PUSH')
    if count > 0:
        scores = r.zrange('AVAIL:PUSH', 0, count - 1, withscores=True)

        for ps in scores:
            push = {'name': ps[0], 'usage': ps[1]}
            name = 'PUSH:' + ps[0]
            fields = r.hmget(name, 'ip', 'port')
            if not fields[0]:
                r.zrem('AVAIL:PUSH', ps[0])
                continue

            push['ip'] = fields[0]
            push['port'] = fields[1]

            pushs[ps[0]] = push

    return pushs


# 모니터링 서버정보
def get_monitor():
    from config import REDIS_MONITOR
    r = redis_monitor()
    info = r.info()
    info.update(REDIS_MONITOR)
    return info


# 멤버 서버정보
def get_members():
    from config import REDIS_MEMBERS
    from redis import Redis
    members = []
    for member in REDIS_MEMBERS:
        r = Redis(**member)
        info = r.info()
        info.update(member)
        members.append(info)
    return members


# 푸시정보
def push_list():
    servers = []

    r = redis_monitor()
    count = r.zcard('AVAIL:PUSH')
    if count > 0:
        scores = r.zrange('AVAIL:PUSH', 0, count - 1, withscores=True)

        for ps in scores:
            name = 'PUSH:' + ps[0]
            fields = r.hmget(name, 'ip', 'port')
            if not fields[0]:
                r.zrem('AVAIL:PUSH', ps[0])
                continue
            servers.append({'ip':fields[0], 'port':fields[1]})

    push_list = []
    for server in servers:
        url = 'http://%s:%s/api/monitor' % (server['ip'], server['port'])
        r = requests.get(url)
        push_list.extend(json.loads(r.content))
    return push_list


# 멤버쉽 서비스 리로딩
def reload():
    results = []
    memberships = get_memberships()

    for key, value in memberships.iteritems():
        url = 'http://' + value['ip'] + ':' + value['port'] + '/api/reload'
        response = None
        try:
            response = requests.get(url)
        except requests.ConnectionError, e:
            app.logger.error(e)

        status_code = 500 if not response else response.status_code
        results.append({
           'name': key,
           'url': url,
           'status_code': status_code
        })

    return results

