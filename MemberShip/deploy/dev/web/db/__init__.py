# -*- coding:utf-8 -*-

from SQLRelay import PySQLRClient
from SQLRelay import PySQLRDB
from config import SQLRELAYS


INSTANCES = []
for sqlrelay in SQLRELAYS:
    INSTANCES.append([0, sqlrelay])


def sqlrelay_cursor():
    ''' Connect sqlrelay rdb '''
    info = sorted(INSTANCES, key=lambda x: x[0])[0]

    try:
        con = PySQLRDB.connect(
                info[1]['host'],
                info[1]['port'],
                '',
                info[1]['user'],
                info[1]['pass'],
                0, 1)
        cur = con.cursor()
    except PySQLRDB.DatabaseError, e:
        raise
    
    info[0] += 1
    return con, cur


def sqlrelay_close(cur, con):
    ''' Close sqlrelay rdb '''
    if cur:
        cur.close()
        del cur
    if con:
        con.close()
        del con
    import gc; gc.collect()


def sqlrelay_client_cursor(debug=False):
    ''' Connect sqlrelay client '''
    info = sorted(INSTANCES, key=lambda x: x[0])[0]

    try:
        con = PySQLRClient.sqlrconnection(
                info[1]['host'],
                info[1]['port'],
                '',
                info[1]['user'],
                info[1]['pass'],
                0, 1)
        cur = PySQLRClient.sqlrcursor(con)
        if debug:
            con.debugOn()
    except Exception, e:
        raise
    
    info[0] += 1
    return con, cur


def sqlrelay_client_close(cur, con):
    ''' Close sqlrelay client '''
    if cur:
        del cur
    if con:
        con.debugOff()
        con.endSession()
        del con
    import gc; gc.collect()

