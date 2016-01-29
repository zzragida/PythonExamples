# -*- coding:utf-8 -*-

from logger import logger
from cache import Cache


class Item:
  """ Item class """

  def __init__(self, info):
    self._info = info
    self._info.update(Cache.item(info['item_no']))

#----------------------------------------------------------------#

  def item_id(self): return self._info['item_id']
  def item_no(self): return self._info['item_no']
  def type(self): return self._info['type']
  def count(self): return self._info['count']
  def hero_id(self): return self._info['hero_id']
  def level(self): return self._info['level']
  def max_count(self): return self._info['max_stack']
  def job(self): return self._info['job']
  def broken(self): return self._info['broken']
  def required_level(self): return self._info['required_level']
  def combi(self): return self._info['combi']
  def sort_order(self): return self._info['sort_order']
  

#----------------------------------------------------------------#

  def max_level(self):
    pass

  def set_hero_id(self, hero_id):
    pass

  def overcom_honbul(self, calc):
    pass

  def reinforce_cash(self, calc):
    pass

  def reinforce_stone(self, calc):
    pass

  def repair_cost(self, calc):
    pass

  def reinforce_probability(self, calc):
    pass

  def crash_probability(self, calc):
    pass

  def drop(self, calc):
    pass

  def remove(self):
    pass

  def crash(self):
    pass

  def fix(self):
    pass

  def level_up(self):
    pass

  def increase_count(self):
    pass

  def decrease_count(self):
    pass

  def change_count(self, count):
    pass

#----------------------------------------------------------------#
