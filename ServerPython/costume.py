# -*- coding:utf-8 -*-

from logger import logger
from cache import Cache

import db

class Costume:
  """ Costume class """

  def __init__(self, costume_id, job, level):
    self._info = Cache.costume(job, costume_id)
    self._info['costume_id'] = costume_id
    self._info['job'] = job
    self._info['level'] = level

#----------------------------------------------------------------#    

#----------------------------------------------------------------#    

  def costume_id(self): return self._info['costume_id']
  def job(self): return self._info['job']
  def level(self): return self._info['level']
  def market_price(self): return self._info['market_price']
  def make_honbul(selF): return self._info['make_honbul']

#----------------------------------------------------------------#    

  def ug_honbul(self):
    pass

  def level_up(self, user_id):
    pass

  def get_attrs(self):
    pass

#----------------------------------------------------------------#    
