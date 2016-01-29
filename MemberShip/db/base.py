# -*- coding:utf-8 -*-

import unittest
from datetime import datetime
from datetime import timedelta
from SQLRelay import PySQLRClient


SQLRELAY_HOST = 'localhost'
SQLRELAY_PORT = 9002
SQLRELAY_USER = 'sqlruser'
SQLRELAY_PASS = 'sqlrpass'
SQLRELAY_DEBUG = False


class SQLRelayTestCase(unittest.TestCase):
    """Base test case for SQLRelay"""
    con = None
    cur = None

    def setUp(self):
        self.con = PySQLRClient.sqlrconnection(
                       SQLRELAY_HOST,
                       SQLRELAY_PORT,
                       '',
                       SQLRELAY_USER,
                       SQLRELAY_PASS,
                       0, 1)
        if SQLRELAY_DEBUG: self.con.debugOn()
        self.cur = PySQLRClient.sqlrcursor(self.con)


    def tearDown(self):
        if self.cur:
            del self.cur
        if self.con:
            if SQLRELAY_DEBUG: self.con.debugOff()
            self.con.endSession()
            del self.con


    def call_member_info(self, 
                         app_id, 
                         udid, 
                         device_platform, 
                         service_platform, 
                         facebook_id = 0,
                         facebook_email = None, 
                         facebook_phone = None,
                         status = 1):
        self.cur.prepareQuery('CALL member_info(:app_id, :udid, :device_platform, :service_platform, :facebook_id, :facebook_email, :facebook_phone, :status)')
        self.cur.inputBind('app_id', app_id)
        self.cur.inputBind('udid', udid)
        self.cur.inputBind('device_platform', device_platform)
        self.cur.inputBind('service_platform', service_platform)
        self.cur.inputBind('facebook_id', facebook_id)
        self.cur.inputBind('facebook_email', facebook_email)
        self.cur.inputBind('facebook_phone', facebook_phone)
        self.cur.inputBind('status', status)
        self.cur.executeQuery()
        member_id = self.cur.getFieldAsInteger(0, 0)
        return member_id

