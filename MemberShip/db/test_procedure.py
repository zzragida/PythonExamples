# -*- coding:utf-8 -*-

import unittest
from datetime import datetime
from datetime import timedelta
from base import SQLRelayTestCase


class MemberShipStoredProcedureTestCase(SQLRelayTestCase):
    """MemberShip Stored Procedure Test Case"""

    def test_member_info(self):
        member_id = self.call_member_info(1, 'udid', 10, 10)
        assert member_id == 7

    def test_member_create(self):
        member_id = self.call_member_info(1, 'udid1', 10, 10)



if __name__ == '__main__':
    unittest.main()
