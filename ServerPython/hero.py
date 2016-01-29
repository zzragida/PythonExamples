# -*- coding:utf-8 -*-

from logger import logger
from collections import OrderedDict
from cache import Cache

import db

class Hero:
  """ Hero class """

  _costumes = OrderedDict()
  _last_epic_stage = None

  _weapon = None
  _helmet = None
  _shirt = None
  _pants = None
  _gloves = None
  _boots = None
  _ring = None
  _necklece = None
  
#----------------------------------------------------------------#

  def __init__(self, info):
    logger.debug(info)
    self._info = info
    # for test
    self._info['curr_exp'] = 0
    self._info['next_exp'] = 0
    self._info['playing_time'] = 0
    self._info['epic_progress'] = 0
    self._info['skill_rate'] = 0
    self._info['hp'] = 0
    self._info['mp'] = 0
    self._info['atk'] = 0
    self._info['atr'] = 0
    self._info['def'] = 0
    self._info['dfr'] = 0
    self._info['ctr'] = 0
    self._info['ctd'] = 0
    self._info['ccm'] = 0
    self._info['dex'] = 0
    self._info['hpr'] = 0
    self._info['hpt'] = 0
    self._info['mpr'] = 0
    self._info['mpt'] = 0
    self._info['hb'] = 0
    self._info['ctm'] = 0
    self._info['mov'] = 0

  def hero_id(self): return self._info['hero_id']
  def user_id(self): return self._info['user_id']
  def job(self): return self._info['job']
  def level(self): return self._info['level']
  def curr_exp(self): return self._info['curr_exp']
  def next_exp(self): return self._info['next_exp']
  def playing_time(self): return self._info['playing_time']
  def epic_progress(self): return self._info['epic_progress']
  def skill_rate(self): return self._info['skill_rate']
  def skill_point(self): return self._info['skill_point']
  def unlock_stage_count(self): return self._info['unlock_stage_count']

  def costume_id(self): return self._info['last_costume_id']
  def button_a(self): return self._info['button_a']
  def button_b(self): return self._info['button_b']
  def button_c(self): return self._info['button_c']

  def hp(self): return self._info['hp']
  def mp(self): return self._info['mp']
  def atk(self): return self._info['atk']
  def atr(self): return self._info['atr']
  #def def(self): return self._info['def']
  def dfr(self): return self._info['dfr']
  def ctr(self): return self._info['ctr']
  def ctd(self): return self._info['ctd']
  def ccm(self): return self._info['ccm']
  def dex(self): return self._info['dex']
  def hpr(self): return self._info['hpr']
  def hpt(self): return self._info['hpt']
  def mpr(self): return self._info['mpr']
  def mpt(self): return self._info['mpt']
  def hb(self): return self._info['hb']
  def ctm(self): return self._info['ctm']
  def mov(self): return self._info['mov']
  def exp(self): return self._info['exp']

  def weapon(self): return self._weapon
  def helmet(self): return self._helmet
  def shirt(self): return self._shirt
  def pants(self): return self._pants
  def gloves(self): return self._gloves
  def boots(self): return self._boots
  def ring(self): return self._ring
  def necklece(self): return self._necklece


#----------------------------------------------------------------#

  def fill_hero(self, hero):
    hero.job = self.job()
    hero.level = self.level()
    hero.curr_exp = self.curr_exp()
    hero.next_exp = self.next_exp()
    hero.playing_time = self.playing_time()
    hero.costume_id = self.costume_id()
    hero.button_a = self.button_a()
    hero.button_b = self.button_b()
    hero.button_c = self.button_c()
    hero.expand_skill_button = self.is_expand_skill_button()
    hero.epic_progress = self.epic_progress()
    hero.skill_rate = self.skill_rate()
    hero.skill_point = self.skill_point()
    hero.unlock_stage_count = self.unlock_stage_count()
    self.fill_attributes(hero.attributes)


  def fill_attributes(self, attributes):
    attributes.hp = self.hp()
    attributes.mp = self.mp()
    attributes.atk = self.atk()
    attributes.atr = self.atr()
    setattr(attributes, 'def', self._info['def'])
    attributes.dfr = self.dfr()
    attributes.ctr = self.ctr()
    attributes.ctd = self.ctd()
    attributes.ccm = self.ccm()
    attributes.dex = self.dex()
    attributes.hpr = self.hpr()
    attributes.hpt = self.hpt()
    attributes.mpr = self.mpr()
    attributes.mpt = self.mpt()
    attributes.hb = self.hb()
    attributes.ctm = self.ctm()
    attributes.mov = self.mov()
    attributes.exp = self.exp()

#----------------------------------------------------------------#

# 의상관련
  def has_costume(self, costume_id):
    return self._costumes.has_key(costume_id)

  def add_costume(self, costume):
    key = costume.costume_id()
    self._costumes[key] = costume

  def costume_level_up(self, costume_id):
    if not self._costumes.has_key(costume_id): return False
    costume = self._costumes[costume_id]
    return costume.level_up()

  def costume_level(self, costume_id):
    if not self._costumes.has_key(costume_id): return -1
    costume = self._costumes[costume_id]
    return costume.level()

  def get_costume(self, costume_id):
    if not self._costumes.has_key(costume_id): return None
    return self._costumes[costume_id]

  def is_unlocked_costume(self, costume_id):
    if not self._costumes.has_key(costume_id): return False
    costume = self._costumes[costume_id]
    return costume.unlock()

  def select_costume(self, costume_id):
    pass

  def select_first_costume(self):
    pass

  def fill_costumes(self, costumes):
    assert(self._info)
    costumes.job = self.job()
    costumes.selected_costume_id = self.costume_id()

    for info in self._costumes:
      costume = costumes.add_costumes()
      costume.costume_id = info.costume_id()
      costume.selected = (self.costume_id() == info.costume_id())
      
#----------------------------------------------------------------#

# 게임관련

  def finish_game(self, play_time, exp):
    pass

  def clear_stage(self, stage_id, difficulty, star, perfect, score):
    pass

  def fail_stage(self, stage_id, difficulty):
    pass

  def update_epic_progress(self):
    pass

  def update_attributes(self):
    pass

  def challenge_battle_skip(self, stage_id, difficulty):
    pass

  def level_up(self, exp):
    pass

#----------------------------------------------------------------#

# 스킬관련

  def load_skills(self):
    pass

  def get_skills(self):
    pass

  def is_expand_skill_button(self): return self._info['expand_button']

  def expand_skill_button(self):
    pass

  def update_skill_rate(self):
    pass

  def set_button(self, button_a, button_b, button_c, db_update=True):
    pass

  def has_skill(self, skill_id):
    pass

  def skill_auto_assign(self):
    pass

  def reinforce_skill(self, skill_id, skill_point):
    pass

  def get_skill_level(self, skill_id):
    pass

  def reset_skill(self):
    pass

  def reset_skill_point(self):
    pass

  def fill_skills(self, skills):
    pass

#----------------------------------------------------------------#

# 장비관련

  def attach_equip(self, item, db_update=False):
    pass

  def detach_equip(self, item, db_update=True):
    pass

  def get_equip(self, type):
    pass

#----------------------------------------------------------------#

# 스테이지관련

  def load_stage(self):
    pass

  def can_enter_dungeon(self, dungeon_id):
    pass

  def is_open_stage(self, stage_id):
    pass

  def is_clear_stage(self, stage_id, difficulty):
    pass

  def get_stage(self, stage_id):
    pass

  def unlock_stage(self, stage_id):
    pass

  def open_stage(self, stage_id):
    pass

  def stage_star(self, stage_id, difficulty):
    pass

  def spend_unlock_stage_count(self):
    pass

  def update_unlock_stage_count(self):
    pass

  def fill_dungeons(self, dungeons):
    assert(self._info)
    dungeon_id = Cache.get_daily_dungeon_id()
    if dungeon_id > 0: dungeons.daily = dungeon_id

    dungeon_id = Cache.get_survival_dungeon_id()
    if dungeon_id > 0: dungeons.survival = dungeon_id

    dungeon_id = Cache.get_event_dungeon_id()
    if dungeon_id > 0: dungeons.event = dungeon_id

    dungeons.epic_progress = self.epic_progress()

    if self._last_epic_stage:
      dungeons.last_epic_stage_id = self._last_epic_stage.stage_id()
      dungeons.last_epic_stage_difficulty = self._last_epic_stage.last_level()


  def fill_epic_dungeons(self, epic_dungeons):
    for dungeon in Cache.epic_dungeons().values():
      d = epic_dungeons.dungeons.add()
      d.dungeon_id = dungeon['dungeon_id']
      lock = True
      new_stage = True
      going_stage = True

      d.lock = lock
      d.new_stage = new_stage
      d.going_stage = going_stage


  def fill_stages(self, dungeon_id, stages):
    pass

#----------------------------------------------------------------#

# 랭킹관련

  # 스토리
  def load_story_ranking(self, nickname):
    pass

  def update_story_ranking(self, nickname):
    pass

  def fill_story_ranking(self, type, first, count, ranking):
    pass

  # 서바이벌
  def load_survival_ranking(self, nickname):
    pass

  def update_survival_ranking(self, score, wave, play_time, nickname):
    pass

  def fill_survival_ranking(self, first, count, ranking):
    pass

  def _encode_ranking_detail(self):
    pass

  def _decode_ranking_detail(self):
    pass

#----------------------------------------------------------------#

# 키관련

  def _lock_key(self):
    pass

  def _ranker_key(self):
    pass

  def _story_key(self, job=-1):
    pass

  def _story_detail_key(self, job=-1, hero_id=-1):
    pass

  def _survival_key(self):
    pass

  def _survival_detail_key(self, hero_id=-1):
    pass

#----------------------------------------------------------------#

# for test

  def set_skill_point(self, skill_point):
    db.execute("UPDATE ARPG_GT_HERO SKILL_POINT = %d WHERE HERO_ID = %d" % (skill_point, self._info['hero_id']))
    self._info['skill_point'] = skill_point

  def set_level(self, level):
    db.execute("UPDATE ARPG_GT_HERO LEVEL = %d WHERE HERO_ID = %d" % (level, self._info['hero_id']))
    self._info['level'] = level

  def set_exp(self, exp):
    db.execute("UPDATE ARPG_GT_HERO EXP = %d WHERE HERO_ID = %d" % (exp, self._info['hero_id']))
    self._info['exp'] = exp

  def set_playing_time(self, playing_time):
    db.execute("UPDATE ARPG_GT_HERO PLAYING_TIME = %d WHERE HERO_ID = %d" % (playing_time, self._info['hero_id']))
    self._info['playing_time'] = playing_time

  def set_unlock_stage_count(self, count):
    db.execute("UPDATE ARPG_GT_HERO UNLOCK_STAGE_COUNT = %d WHERE HERO_ID = %d" % (count, self._info['hero_id']))
    self._info['unlock_stage_count'] = count


#----------------------------------------------------------------#
