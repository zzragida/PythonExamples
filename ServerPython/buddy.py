# -*- coding:utf-8 -*-

from logger import logger


class Buddy:
  """ Buddy class """

  def __init__(self, info):
    self._info = info


  def user_id(self): return self._info['user_id']
  def name(self): return self._info['name']
  def can_receive_heart(self): return (self._info['heart'] == 1)
  def can_sending_heart(self): return (self._info['heart'] == 0)
  def job(self): return self._info['job']
  def level(self): return self._info['level']
  def playing(self): return self._info['playing']
  def online(self): return self._info['online']
  def last_login(self): return self._info['last_login']
  def max_level(self): return self._info['max_level']
  def hero_count(self): return self._info['hero_count']
  def reg_timestamp(self): return self._info['reg_timestamp']
  def no_kakao_message(self): return self._info['no_kakao_message']
  def no_kakao_profile(self): return self._info['no_kakao_profile']
  def story_score(self): return self._info['story_score']
