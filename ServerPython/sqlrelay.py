# -*- coding: utf-8 -*-

import gevent
import gevent.monkey
gevent.monkey.patch_all()

from config import SQLRELAY
from SQLRelay import PySQLRDB, PySQLRClient
from logger import logger


global instances
instances = []
for info in SQLRELAY:
  instances.append([0, info])


def cursor():
  def _execute():
    info = sorted(instances, key=lambda x: x[0])[0]
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
      logger.error(e)
      raise
    info[0] += 1
    return con, cur
  spawnner = gevent.spawn(_execute)
  gevent.joinall([spawnner])
  return spawnner.value


def close(cur, con):
  def _execute(cur, con):
    if cur: cur.close()
    if con: con.close()
    import gc; gc.collect()
  gevent.spawn(_execute, cur, con)



def client_cursor(buffer_size=10):
  def _execute(buffer_size):
    info = sorted(instances, key=lambda x: x[0])[0]
    try:
      con = PySQLRClient.sqlrconnection(
              info[1]['host'],
              info[1]['port'],
              '',
              info[1]['user'],
              info[1]['pass'],
              0, 1)
      cur = PySQLRClient.sqlrcursor(con)
      cur.setResultSetBufferSize(buffer_size)
    except PySQLRDB.DatabaseError, e:
      logger.error(e)
      raise
    info[0] += 1
    return con, cur
  spawnner = gevent.spawn(_execute, buffer_size)
  gevent.joinall([spawnner])
  return spawnner.value


def client_close(cur, con):
  def _execute(cur, con):
    if con: con.endSession()
    import gc; gc.collect()
  gevent.spawn(_execute, cur, con)


def execute(sql):
  logger.debug(sql)
  def _execute(sql):
    try:
      con, cur = cursor()
      cur.execute(sql)
      close(cur, con)
    except PySQLRDB.DatabaseError, e:
      logger.error(e)
      return False
    return True
  spawnner = gevent.spawn(_execute, sql)
  gevent.joinall([spawnner])
  return spawnner.value


def execute_results(sql, multiple = True):
  logger.debug(sql)
  def _execute(sql, multiple):
    results = {}
    try:
      con, cur = cursor()
      cur.execute(sql)
      if multiple:
        results = cur.fetchall()
      else:
        results = cur.fetchone()
      close(cur, con)
    except PySQLRDB.DatabaseError, e:
      logger.error(e)
    return results
  spawnner = gevent.spawn(_execute, sql, multiple)
  gevent.joinall([spawnner])
  return spawnner.value


