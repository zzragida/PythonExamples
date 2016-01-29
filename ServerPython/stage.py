# -*- coding:utf-8 -*-

from logger import logger


class Stage:
  """ Stage class """

  def __inif__(self, info):
    pass

#----------------------------------------------------------------#

  def stage_id(self): return self._info['stage_id']
  def dungeon_id(self): return self._info['dungeon_id']
  def next_stage_id(self): return self._info['next_stage_id']
  def type(self): return self._info['type']
  def is_multi(self): return (self.max_player() > 1)
  def reset_count(self): return self._info['reset_count']
  def heart(self): return self._info['heart']

#----------------------------------------------------------------#

  def level(self):
    pass

  def is_clear(self, difficulty):
    pass

  def set_level(self, difficulty, level):
    pass

  def get_last_level(self):
    pass

  def cooltime(self):
    pass

  def update_cooltime(self):
    pass

  def reset_cooltime(self):
    pass

  def reset_cooltime_count(self):
    pass

  def best_score(self):
    pass

  def is_boss_stage(self):
    pass

  def get_star(self, difficulty):
    pass

#----------------------------------------------------------------#
