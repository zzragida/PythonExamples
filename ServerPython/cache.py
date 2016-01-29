# -*- coding:utf-8 -*-

from logger import logger
from twisted.internet.defer import DeferredLock
from collections import OrderedDict, defaultdict
from datetime import datetime
from util import singleton

from protocol import common_pb2

import db


@singleton
class Cache:
  """ Cache class """

  _attr_codes = {
    "HP": common_pb2.ATTR_HP,
    "MP": common_pb2.ATTR_MP,
    "ATK": common_pb2.ATTR_ATK,
    "ATR": common_pb2.ATTR_ATR,
    "DEF": common_pb2.ATTR_DEF,
    "DFR": common_pb2.ATTR_DFR,
    "CTR": common_pb2.ATTR_CTR,
    "CTD": common_pb2.ATTR_CTD,
    "CCM": common_pb2.ATTR_CCM,
    "DEX": common_pb2.ATTR_DEX,
    "HPR": common_pb2.ATTR_HPR,
    "HPT": common_pb2.ATTR_HPT,
    "MPR": common_pb2.ATTR_MPR,
    "MPT": common_pb2.ATTR_MPT,
    "HB": common_pb2.ATTR_HB,
    "CTM": common_pb2.ATTR_CTM,
    "MOV": common_pb2.ATTR_MOV,
    "EXP": common_pb2.ATTR_EXP,
  }

  # 던전
  _dungeons = None
  _stages = None
  _stage_waves = None
  _monsters = None
  _survival_waves = None
  _lock_dungeons = DeferredLock()

  # 던전이벤트
  _event_dungeons = None
  _lock_event_dungeons = DeferredLock()

  # 의상
  _costumes = None
  _lock_costumes = DeferredLock()

  # 스킬
  _skills = None
  _skill_costs = None
  _lock_skills = DeferredLock()

  # 아이템
  _items = None
  _combinations = None
  _blueprints = None
  _lock_items = DeferredLock()

  # 레벨
  _levels = None
  _lock_levels = DeferredLock()

  # 뽑기
  _lotterys = None
  _lottery_items = None
  _lottery_tiers = None
  _lock_lotterys = DeferredLock()

  # 보물상자
  _treasures = None
  _lock_treasures = DeferredLock()

  # 상점
  _eshops = None
  _event_eshops = None
  _cash_shops = None
  _lock_shops = DeferredLock()

  # 선물함
  _gifts = None
  _level_up_gifts = None
  _recommend_gifts = None
  _lock_gifts = DeferredLock()

  # 이벤트
  _login_events = None
  _periodic_events = None
  _eshop_events = None
  _costume_events = None
  _lock_events = DeferredLock()

  # 일일보상
  _dailystamps = None
  _lock_dailystamps = DeferredLock()

  # 업적
  _achivements = None
  _daily_achivements = None
  _lock_achivements = DeferredLock()

  # 빠른수집
  _material_prices = None
  _lock_material_prices = DeferredLock()

  # 쿠폰
  _keyword_coupons = None
  _lock_coupons = DeferredLock()

  # 서바이벌버프
  _survival_buffs = None
  _lock_survival_buffs = DeferredLock()

  # 도깨비상점
  _oni_shops = None
  _lock_oni_shops = DeferredLock()


  def __init__(self):
    self.reset()

  def __del__(self):
    self._clear_dungeons()
    self._clear_event_dungeons()
    self._clear_costumes()
    self._clear_skills()
    self._clear_items()

  def reset(self, type=common_pb2.CACHE_ALL):
    # 던전정보
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_DUNGEON:
      self._lock_dungeons.acquire()
      self._clear_dungeons()
      self._load_dungeons()
      self._load_stages()
      self._load_stage_waves()
      self._load_monsters()
      self._load_survival_waves()
      self._lock_dungeons.release()

    # 의상정보
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_COSTUME:
      self._lock_costumes.acquire()
      self._clear_costumes()
      self._load_costumes()
      self._lock_costumes.release()

    # 스킬정보
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_SKILL:
      self._lock_skills.acquire()
      self._clear_skills()
      self._load_skills()
      self._load_skill_costs()
      self._lock_skills.release()

    # 아이템정보
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_ITEM:
      self._lock_items.acquire()
      self._clear_items()
      self._load_items()
      self._load_combinations()
      self._load_blueprints()
      self._lock_items.release()

    # 레벨정보
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_LEVEL:
      self._lock_levels.acquire()
      self._clear_levels()
      self._load_levels()
      self._lock_levels.release()

    # 게임설정
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_PROPERTIES:
      from properties import Properties
      Properties.load()

    # 뽑기정보
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_LOTTERY:
      self._lock_lotterys.acquire()
      self._clear_lotterys()
      self._load_lotterys()
      self._load_lottery_items()
      self._load_lottery_tiers()
      self._lock_lotterys.release()

    # 보물상자
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_TREASURE_BOX:
      self._lock_treasures.acquire()
      self._clear_treasures()
      self._load_treasures()
      self._lock_treasures.release()

    # 상점정보
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_SHOP:
      self._lock_shops.acquire()
      self._clear_shops()
      self._load_eshops()
      self._load_cash_shops()
      self._lock_shops.release()

    # 선물함정보
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_GIFT_BOX:
      self._lock_gifts.acquire()
      self._clear_gifts()
      self._load_gifts()
      self._lock_gifts.release()

    # 이벤트정보
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_EVENT:
      self._lock_events.acquire()
      self._clear_events()
      self._lock_events.release()

    # 일일보상
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_DAILYSTAMP:
      self._lock_dailystamps.acquire()
      self._clear_dailystamps()
      self._load_dailystamps()
      self._lock_dailystamps.release()

    # 업적정보
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_ACHIVEMENT:
      self._lock_achivements.acquire()
      self._clear_achivements()
      self._load_achivements()
      self._load_daily_achivements()
      self._lock_achivements.release()

    # 빠른재료
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_MATERIAL_PRICE:
      self._lock_material_prices.acquire()
      self._clear_material_prices()
      self._load_material_prices()
      self._lock_material_prices.release()

    # 쿠폰정보
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_COUPON:
      self._lock_coupons.acquire()
      self._clear_coupons()
      self._load_keyword_coupons()
      self._lock_coupons.release()

    # 서바이벌버프
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_SURVIVAL_BUFF:
      self._lock_survival_buffs.acquire()
      self._clear_survival_buffs()
      self._lock_survival_buffs.release()

    # 도깨비상점
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_ONI_SHOP:
      self._lock_oni_shops.acquire()
      self._clear_oni_shops()
      self._load_oni_shops()
      self._lock_oni_shops.release()

    # 이벤트던전
    if type == common_pb2.CACHE_ALL or type == common_pb2.CACHE_EVENT_DUNGEON:
      self._lock_event_dungeons.acquire()
      self._clear_event_dungeons()
      self._load_event_dungeons()
      self._lock_event_dungeons.release()

#----------------------------------------------------------------#

  def _clear_dungeons(self):
    if self._dungeons:
      del self._dungeons
      self._dungeons = None
    if self._stages: 
      del self._stages
      self._stages = None

  def _clear_event_dungeons(self):
    pass

  def _clear_costumes(self):
    pass

  def _clear_skills(self):
    pass

  def _clear_items(self):
    pass

  def _clear_levels(self):
    pass

  def _clear_lotterys(self):
    pass

  def _clear_treasures(self):
    pass

  def _clear_shops(self):
    pass

  def _clear_gifts(self):
    pass

  def _clear_events(self):
    pass

  def _clear_dailystamps(self):
    pass

  def _clear_achivements(self):
    pass

  def _clear_material_prices(self):
    pass

  def _clear_coupons(self):
    pass

  def _clear_survival_buffs(self):
    pass

  def _clear_oni_shops(self):
    pass

#----------------------------------------------------------------#

# 아이템정보
  def _load_items(self):
    if self._items: return
    self._items = db.items()

  def _load_combinations(self):
    if self._combinations: return
    self._combinations = db.combinations()

  def _load_blueprints(self):
    if self._blueprints: return
    self._blueprints = db.blueprints()

  def item(self, item_no):
    self._lock_items.acquire()
    item = {}
    item = self._items[item_no]
    self._lock_items.release()
    return item

  def combination(self, type):
    pass

  def blueprint(self, type):
    pass

#----------------------------------------------------------------#

# 레벨정보
  def _load_levels(self):
    if self._levels: return
    self._levels = db.levels()

  def level(self, job, level):
    pass

#----------------------------------------------------------------#

# 가챠정보
  def _load_lotterys(self):
    if self._lotterys: return
    self._lotterys = db.lotterys()

  def _load_lottery_items(self):
    if self._lottery_items: return
    self._lottery_items = db.lottery_items()

  def _load_lottery_tiers(self):
    if self._lottery_tiers: return
    self._lottery_tiers = db.lottery_tiers()

  def lotterys(self):
    pass

  def lottery_price(self, type, count):
    pass

  def take_lottery(self, type, lv_tier, random, job=common_pb2.JOB_COMMON):
    pass

#----------------------------------------------------------------#

# 스킬정보
  def _load_skills(self):
    if self._skills: return
    self._skills = db.skills()

  def _load_skill_costs(self):
    if self._skill_costs: return
    self._skill_costs = db.skill_costs()

  def skills(self, job):
    pass

  def skill_rate(self, job, level):
    pass

  def get_skill(self, job, skill_id):
    pass

  def skill_is_maximum_level(self, job, skill_id, level):
    pass

  def skill_costs(self, skill_id):
    pass

  def reinforce_skill_cost(self, job, skill_id, level):
    pass

#----------------------------------------------------------------#

# 의상정보
  def _load_costumes(self):
    if self._costumes: return
    self._costumes = db.costumes()

  def costumes(self, job):
    pass

  def costume(self, job, costume_id):
    self._lock_costumes.acquire()
    self._load_costumes()
    costume = None
    if self._costumes.has_key(job):
      costume_job = self._costumes[job]
      if costume_job.has_key(costume_id):
        costume = costume_job[costume_id].copy()
    self._lock_costumes.release()
    return costume

  def costumes_to_make(self, job):
    pass

  def costumes_to_reinforce(self, job):
    pass

  def default_costume_id(self, job):
    pass

#----------------------------------------------------------------#

# 던전정보
  def _load_dungeons(self):
    if self._dungeons: return
    self._dungeons = db.dungeons()

  def _load_stages(self):
    if self._stages: return
    self._stages = db.stages()

  def _load_stage_waves(self):
    if self._stage_waves: return
    self._stage_waves = db.stage_waves()

  def _load_monsters(self):
    if self._monsters: return
    self._monsters = db.monsters()

  def _load_survival_waves(self):
    if self._survival_waves: return
    self._survival_wave = db.survival_waves()

  def _load_event_dungeons(self):
    if self._event_dungeons: return
    self._event_dungeons = db.event_dungeons()

  def get_daily_dungeon_id(self):
    self._lock_dungeons.acquire()
    self._load_dungeons()
    dungeon_id = 0
    if self._dungeons.has_key(common_pb2.DUNGEON_DAILY):
      dungeon_id = self._dungeons[common_pb2.DUNGEON_DAILY].values()[0]['dungeon_id']
    self._lock_dungeons.release()
    return dungeon_id

  def get_survival_dungeon_id(self):
    self._lock_dungeons.acquire()
    dungeon_id = 0
    if self._dungeons.has_key(common_pb2.DUNGEON_SURVIVAL):
      dungeon_id = self._dungeons[common_pb2.DUNGEON_SURVIVAL].values()[0]['dungeon_id']
    self._lock_dungeons.release()
    return dungeon_id

  def get_event_dungeon_id(self):
    self._lock_dungeons.acquire()
    dungeon_id = 0
    if self._dungeons.has_key(common_pb2.DUNGEON_EVENT):
      dungeon_id = self._dungeons[common_pb2.DUNGEON_EVENT].values()[0]['dungeon_id']
    self._lock_dungeons.release()
    return dungeon_id

  def epic_dungeons(self):
    dungeons = defaultdict()
    self._lock_dungeons.acquire()
    if self._dungeons.has_key(common_pb2.DUNGEON_EPIC):
      dungeons = self._dungeons[common_pb2.DUNGEON_EPIC].copy()
    self._lock_dungeons.release()
    return dungeons

  def unlocked_stages(self):
    pass

  def get_stage_info(self, stage_id):
    pass

  def get_dungeon_info(self, dungeon_id):
    pass

  def get_dungeon_info_by_stage_id(self, stage_id):
    pass

  def get_monster(self, monster_id, level):
    pass

  def total_survival_wave(self):
    pass

  def copy_survival_waves(self):
    pass

  def get_survival_wave_reward(self, wave):
    pass

  def get_multi_stage_spend_heart(self, stage_id):
    pass


#----------------------------------------------------------------#

# 캐쉬상점정보
  def _load_eshops(self):
    if self._eshops and self._event_eshops: return
    (self._eshops, self._event_eshops) = db.eshops()

  def eshop(self, market, last_payment):
    pass

  def eshop_pmang_id(self, event, market, cash, product_id):
    pass

#----------------------------------------------------------------#

# 충전소정보
  def _load_cash_shops(self):
    if self._cash_shops: return
    self._cash_shops = db.cash_shops()

  def cash_shop(self):
    pass

  def cash_shop_goods(self, category, cash):
    pass

#----------------------------------------------------------------#

# 보물상자정보
  def _load_treasures(self):
    if self._treasures: return
    self._treasures = db.treasures()

  def treasure_box(self, group, random):
    pass

  def copy_treasure_box(self, group, box):
    pass

#----------------------------------------------------------------#

# 선물함정보
  def _load_gifts(self):
    if self._gifts: return
    self._gifts = db.gifts()

  def _load_level_up_gifts(self):
    if self._level_up_gifts: return
    self._level_up_gifts = db.level_up_gifts()

  def _load_recommend_gifts(self):
    if self._recommend_gifts: return
    self._recommend_gifts = db.recommend_gifts()

  def gift(self, gift_id):
    pass

  def level_up_gift(self, level, job):
    pass

  def recommend_gift(self, recommend_count):
    pass

#----------------------------------------------------------------#

# 이벤트정보
  def _load_login_events(self):
    if self._login_events: return
    self._login_events = db.login_events()

  def _load_periodic_events(self):
    if self._periodic_events: return
    self._periodic_events = db.periodic_events()

  def _load_eshop_events(self):
    if self._eshop_events: return
    self._eshop_events = db.eshop_events()

  def _load_costume_events(self):
    if self._costume_events: return
    self._costume_events = db.costume_events()

  def login_event(self):
    pass

  def periodic_event(self):
    pass

  def is_eshop_event(self, last_payment):
    pass

  def eshop_event(self, last_payment):
    pass

  def costume_event(self, job):
    pass

#----------------------------------------------------------------#

# 일일보상정보
  def _load_dailystamps(self):
    if self._dailystamps: return
    self._dailystamps = db.dailystamps()

  def dailystamps(self, year_month):
    self._lock_dailystamps.acquire()
    self._load_dailystamps()
    dailystamps = self._dailystamps.copy()
    self._lock_dailystamps.release()
    return dailystamps

  def dailystamp_gift(self, year_month, days):
    self._lock_dailystamps.acquire()
    self._load_dailystamps()
    gifts = self._dailystamps[year_month][days]
    self._lock_dailystamps.release()
    return gifts

#----------------------------------------------------------------#

# 업적정보
  def _load_achivements(self):
    if self._achivements: return
    self._achivements = db.achivements()

  def _load_daily_achivements(self):
    if self._daily_achivements: return
    self._daily_achivements = db.daily_achivements()

  def achivement(self, type):
    self._lock_achivements.acquire()
    self._load_achivements()
    achivement = self._achivements[type].copy()
    self._lock_achivements.release()
    return achivement

  def daily_achivement(self, type):
    self._lock_achivements.acquire()
    self._load_daily_achivements()
    daily_achivement = self._daily_achivements[type]
    self._lock_achivements.release()
    return daily_achivement

  def achivement_list(self):
    self._lock_achivements.acquire()
    self._load_achivements()
    achivements = self._achivements.copy()
    self._lock_achivements.release()
    return achivements

  def daily_achivement_list(self):
    self._lock_achivements.acquire()
    self._load_daily_achivements()
    daily_achivements = self._daily_achivements.copy()
    self._lock_achivements.release()
    return daily_achivements

#----------------------------------------------------------------#

# 재료수집정보
  def _load_material_prices(self):
    if self._material_prices: return
    self._material_prices = db.material_prices()

  def material_price(self, material_id):
    self._lock_material_prices.acquire()
    self._load_material_prices()
    material_price = self._material_prices[material_id].copy()
    self._lock_material_prices.release()
    return material_price

#----------------------------------------------------------------#

# 키워드쿠폰정보
  def _load_keyword_coupons(self):
    if self._keyword_coupons: return
    self._keyword_coupons = db.keyword_coupons()

  def keyword_coupon(self, keyword):
    now = datetime.now()
    coupon = None

    self._lock_coupons.acquire()
    self._load_keyword_coupons()
    for key, val in self._keyword_coupons.iteritems():
      if keyword != val['keyword']: continue
      if val['coupon_avl_start'] <= now and now <= val['coupon_avl_end']:
        coupon = {
          'coupon_id': key,
          'reuse': val['reuse'],
        }
        break
    self._lock_coupons.release()

    return coupon

#----------------------------------------------------------------#

# 도깨비상점정보
  def _load_oni_shops(self):
    if self._oni_shops: return
    self._oni_shops = db.oni_shops()

  def oni_shop_goods(self, goods_id):
    self._lock_oni_shops.acquire()
    self._load_oni_shops()
    oni_shop_goods = self._oni_shops[goods_id / 100000].copy()
    self._lock_oni_shops.release()
    return oni_shop_goods

  def oni_goods(self, method, category, job, level):
    self._lock_oni_shops.acquire()
    self._load_oni_shops()
    oni_goods = self._oni_shops[category].copy()
    self._lock_oni_shops.release()

    goods = defaultdict()
    for key, good in oni_goods.iteritems():
      if good['required_level'] > level:
        continue
      if good['job'] == common_pb2.JOB_COMMON or good['job'] == job:
        goods[key] = good
      
    return goods

#----------------------------------------------------------------#

# 서바이벌버프정보
  def _load_survival_buffs(self):
    if self._survival_buffs: return
    self._survival_buffs = db.survival_buffs()

  def survival_buffs(self):
    self._lock_survival_buffs.acquire()
    self._load_survival_buffs()
    buffs = self._survival_buffs.copy()
    self._lock_survival_buffs.release()
    return buffs

  def survival_buff(self, buff_id):
    self._lock_survival_buffs.acquire()
    self._load_survival_buffs()
    buff = {}
    if self._survival_buffs.has_key(buff_id):
      buff = self._survival_buffs[buff_id]
    self._lock_survival_buffs.release()
    return buff

#----------------------------------------------------------------#


