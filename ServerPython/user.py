# -*- coding:utf-8 -*-

from twisted.python import failure
from collections import OrderedDict
from logger import logger

from hero import Hero
from costume import Costume
from item import Item
from properties import Properties
from cache import Cache
from protocol import gateway_pb2

import db
import random
import math


class User:
  """ User class """

  _selected_hero = None
  _heroes = OrderedDict()
  _costumes = OrderedDict()
  _items = OrderedDict()
  _events = OrderedDict()
  _payments = OrderedDict()
  _friends = OrderedDict()
  _kakao_friends = OrderedDict()
  _gifts = OrderedDict()
  _achivements = OrderedDict()


  @staticmethod
  def get_user_id(game_id, hashed_kakao_id, kakao_id=-1):
    user_id = db.make_pp_user(game_id, kakao_id, hashed_kakao_id)
    if user_id > 0: return User(user_id)
    return failure.Failure((gateway_pb2.EC_UNABLE_TO_OPERATE, 'User not found'))

#----------------------------------------------------------------#
  def __init__(self, user_id):
    self._user_id = user_id
    self._load()

  def __del__(self):
    pass

  def _load(self):
    assert(self._user_id > 0)
    self._load_user()
    self._load_heroes()
    self._load_costumes()
    self._load_items()
    for hero in self._heroes.values():
      hero.load_stage()
      hero.load_skills()
      hero.update_attributes()
      hero.update_unlock_stage_count()
    self._load_rankings()
    self._load_events()
    self._load_coupons()
    self._load_gifts()
    self._load_payments()
    self._load_friends()
    self._load_achivements()
    self._load_kakao_friends()

  def _load_user(self):
    assert(self._user_id > 0)
    info = db.user(self._user_id)
    if not info: return failure.Failure((gateway_pb2.EC_DATABASE, 'Database failed'))
    self._info = info

  def _load_heroes(self):
    assert(self._user_id > 0)
    self._heroes.clear()
    for info in db.user_heroes(self._user_id):
      job = info['job']
      self._heroes[job] = Hero(info)

  def _load_costumes(self):
    assert(self._user_id > 0)
    self._costumes.clear()
    for info in db.user_costumes(self._user_id):
      costume_id = info['costume_id']
      costume_no = info['costume_no']
      job = info['job']
      level = info['level']
      costume = Costume(costume_no, job, level)
      self._costumes[costume_id] = costume
      if self._heroes.has_key(job):
        hero = self._heroes[job]
        hero.add_costume(costume)

  def _load_items(self):
    assert(self._user_id > 0)
    self._items.clear()
    for info in db.user_items(self._user_id):
      item_id = info['item_id']
      hero_id = info['hero_id']
      item = Item(info)
      self._items[item_id] = Item(info)
      if hero_id:
        for hero in self._heroes.values():
          if hero_id == hero.hero_id():
            hero.attach_equip(item)
            break
      
  def _load_rankings(self):
    assert(self._user_id > 0)
    assert(self._info)

  def _load_events(self):
    assert(self._user_id > 0)
    assert(self._info)

  def _load_coupons(self):
    assert(self._user_id > 0)
    assert(self._info)

  def _load_gifts(self):
    self._gifts.clear()
    self._gifts = db.user_gifts(self._user_id)

  def _load_payments(self):
    assert(self._user_id > 0)
    assert(self._info)

  def _load_friends(self):
    assert(self._user_id > 0)
    assert(self._info)

  def _load_achivements(self):
    assert(self._user_id > 0)
    assert(self._info)

  def _load_kakao_friends(self):
    assert(self._user_id > 0)
    assert(self._info)


#----------------------------------------------------------------#

# 키관련
  def online_key(self, user_id=-1):
    pass

  def personal_key(self, user_id=-1):
    pass

  def ranker_key(self, user_id=-1):
    pass

  def story_key_(self, difficulty=-1):
    pass

  def story_detail_key_(self, difficulty=-1, user_id=-1):
    pass

#----------------------------------------------------------------#

  def user_id(self): return self._user_id
  def kakao_id(self): return self._info['kakao_id']
  def nickname(self): return self._info['nickname']
  def honbul(self): return self._info['honbul']
  def cash(self): return self._info['cash']
  def talisman(self): return self._info['talisman']
  def stone(self): return self._info['stone']
  def coin(self): return self._info['coin']
  def heart(self): return self._info['heart']
  def searchable(self): return self._info['searchable']
  def inventory_size(self): return self._info['inventory_size']
  def hero_count(self): return len(self._heroes)
  def no_kakao_message(self): return self._info['no_kakao_message']
  def no_kakao_profile(self): return self._info['no_kakao_profile']
  def review(self): return self._info['review']

#----------------------------------------------------------------#

  def fill_info(self, info):
    if not self._selected_hero:
      return failure.Failure((gateway_pb2.EC_NO_HERO, "No hero"))
    if not self._info and not self._info.has_key('nickname'):
      return failure.Failure((gateway_pb2.EC_NO_NICKNAME, "Need nickname"))
    info.honbul = self.honbul()
    info.cash = self.cash()
    info.talisman = self.talisman()
    info.stone = self.stone()
    info.coin = self.coin()
    info.heart = self.heart()
    info.inventory_size = self.inventory_size()
    info.searchable = self.searchable()
    info.no_kakao_message = self.no_kakao_message()
    info.no_kakao_profile = self.no_kakao_profile()
    info.review = self.review()
    info.nickname = self.nickname()
    info.ranking = 0
    info.terminate_abnormally = False
    if self._selected_hero:
      self._selected_hero.fill_hero(info.selected)
      self._selected_hero.fill_dungeons(info.dungeons)
    self.fill_badges(info.badges)


  def fill_properties(self, properties):
    properties.honbul_for_expand_skill_button = Properties.HONBUL_FOR_EXPAND_SKILL_BUTTON
    properties.cash_for_expand_skill_button = Properties.CASH_FOR_EXPAND_SKILL_BUTTON
    properties.reset_cash_for_material_cooltime = Properties.RESET_CASH_FOR_MATERIAL_COOLTIME
    properties.collect_material_multiplier = Properties.COLLECT_MATERIAL_MULTIPLIER
    properties.max_reset_material_cooltime = Properties.MAX_RESET_MATERIAL_COOLTIME
    properties.cash_for_resurrection = Properties.CASH_FOR_RESURRECTION
    properties.coin_for_resurrection = Properties.COIN_FOR_RESURRECTION
    properties.needs_resurrection_by_cash = self.needs_resurrection_by_cash()
    properties.needs_resurrection_by_coin = self.needs_resurrection_by_coin()

    properties.hero_level_for_multiplay = Properties.HERO_LEVEL_FOR_MULTIPLAY
    properties.level_for_new_archer = Properties.LEVEL_FOR_NEW_ARCHER
    properties.honbul_for_new_hero = Properties.HONBUL_FOR_NEW_HERO
    properties.cash_for_inventory_slot = Properties.CASH_FOR_INVENTORY_SLOT

    properties.max_hero_level = Properties.MAX_HERO_LEVEL
    properties.send_heart_amount = Properties.SEND_HEART_AMOUNT
    properties.reward_of_send_heart = Properties.REWARD_OF_SEND_HEART
    properties.max_friend_count = Properties.MAX_FRIEND_COUNT
    properties.reward_of_kakao_invitation = Properties.REWARD_OF_KAKAO_INVITATION

    properties.battle_skip_star1 = Properties.BATTLE_SKIP_STAR1
    properties.battle_skip_star2 = Properties.BATTLE_SKIP_STAR2
    properties.battle_skip_star3 = Properties.BATTLE_SKIP_STAR3
    properties.battle_skip_star4 = Properties.BATTLE_SKIP_STAR4
    properties.battle_skip_star5 = Properties.BATTLE_SKIP_STAR5
    properties.honbul_for_battle_skip = Properties.HONBUL_FOR_BATTLE_SKIP
    properties.battle_skip_exp = Properties.BATTLE_SKIP_EXP
    properties.battle_skip_probability = Properties.BATTLE_SKIP_PROBABILITY

    properties.discount_for_oni_shop_honbul = Properties.DISCOUNT_FOR_ONI_SHOP_HONBUL
    properties.discount_for_oni_shop_cash = Properties.DISCOUNT_FOR_ONI_SHOP_CASH
    properties.discount_for_reset_skill = Properties.DISCOUNT_FOR_RESET_SKILL

    properties.closing_dungeon_timeout = Properties.CLOSING_DUNGEON_TIMEOUT
    properties.select_stage_timeout = Properties.SELECT_STAGE_TIMEOUT


  def fill_badges(self, badges):
    pass



#----------------------------------------------------------------#

# 접속/로그인
  def login(self, user_id):
    pass

  def logout(self):
    pass

  def online(self):
    pass

  def offline(self):
    pass

#----------------------------------------------------------------#

# 게임관련
  def start_game(self):
    pass

  def end_game(self):
    pass

  def leave_in_game(self, play_time, exp, honbul):
    pass

  def finish_game(self, honbul):
    pass

  def finish_single_game(self, stage, finish):
    pass

  def finish_survival_game(self, wave, score, honbul, play_time):
    pass

  def needs_resurrection_by_cash(self):
    return 0

  def needs_resurrection_by_coin(self):
    return 0

#----------------------------------------------------------------#

# 닉네임/캐릭터
  def has_nickname(self):
    assert(self._info)
    if not self._info.has_key('nickname'): return False
    if self._info['nickname'] is None: return False
    return True

  def change_nickname(self, new_nickname):
    if not db.change_nickname(self._user_id, new_nickname):
      return failure.Failure((gateway_pb2.EC_DATABASE, "Database failed"))
    self._info['nickname'] = new_nickname

  def has_hero(self, job):
    return self._heroes.has_key(job)


  def make_hero(self, job):
    hero_info = db.make_hero(self.user_id(), job)
    if not hero_info:
      return failure.Failure((gateway_pb2.EC_DATABASE, "Database failed"))
    hero = Hero(hero_info)
    self._heroes[job] = hero
    self._selected_hero = hero
    return self._selected_hero

  def select_hero(self, job):
    hero = self._heroes[job]
    self._selected_hero = hero
    return self._selected_hero

  def hero_by_job(self, job):
    pass

  def hero_by_id(self, hero_id):
    pass

  def selected_hero(self):
    return self._selected_hero

  def max_hero_level(self):
    assert(self._heroes)
    max_level = 0
    for hero in self._heroes.values():
      if hero.level() > max_level:
        max_level = hero.level()
    return max_level

  def fill_heroes(self, response):
    assert(self._heroes)
    for h in self._heroes.values():
      hero = response.heroes.add()
      hero.job = h.job()
      hero.level = h.level()

#----------------------------------------------------------------#

# 스테이지관련
  def fill_dungeons(self, dungeons):
    if not self._selected_hero:
      return failure.Failure((gateway_pb2.EC_NO_HERO, "No Hero"))
    return self._selected_hero.fill_dungeons(dungeons)

  def fill_epic_dungeons(self, epic_dungeons):
    if not self._selected_hero:
      return failure.Failure((gateway_pb2.EC_NO_HERO, "No Hero"))
    return self._selected_hero.fill_epic_dungeons(epic_dungeons)

#----------------------------------------------------------------#

# 의상관련 
  def has_costume(self, costume_id):
    pass

  def add_costume(self, type):
    pass

  def buy_costume(self, costume_id, cost):
    pass

  def make_costume(self, costume_id, cost):
    pass

  def reinforce_costume(self, costume_id, honbul, cash):
    pass

  def fetch_costume(self, hero):
    pass


#----------------------------------------------------------------#

# 인벤토리/아이템
  def fill_inventory(self, inventory):
    inventory.limit = self.inventory_size()
    inventory.honbul = self.honbul()
    inventory.cash = self.cash()
    for item in self._items().values():
      if item.hero_id() > 0: continue
      entry = inventory.entries.add()
      entry.item_id = item.item_id()
      entry.type = item.type()

  def add_inventory_slot(self, count):
    pass

  def empty_slot_in_inventory(self):
    pass

  def has_excessing_inventory(self):
    pass

  def put_on(self, item):
    pass

  def take_off(self, item):
    pass

  def reinforce_item(self, item, honbul, cash, stone, success=True, crash=False):
    pass

  def fix_item(self, item, cost):
    pass

  def get_item_by_id(self, item_id):
    pass

  def get_item_by_no(self, item_no):
    pass

  def get_item_count_by_no(self, item_no):
    pass

  def has_item(self, item_no, count):
    pass

  def drop_item(self, item, count):
    pass

  def remove_item(self, item):
    pass

  def make_item(self, item_no, blueprint):
    pass

  def add_item(self, item_no):
    pass

#----------------------------------------------------------------#

# 선물함
  def add_gift(self, gift_id):
    pass

  def delete_gift(self, gift):
    pass

#----------------------------------------------------------------#

# 빠른수집
  def collect_material(self, material_id, collect_material):
    if self.material_cooltime() > 0:
      return failure.Failure((gateway_pb2.EC_UNABLE_TO_OPERATE, 'Exist cooltime'))

    material_price = Cache.material_price(material_id)
    if not material_price:
      return failure.Failure((gateway_pb2.EC_UNABLE_TO_OPERATE, 'Material is not exist'))

    if self.honbul() < material_price['price']:
      return failure.Failure((gateway_pb2.EC_NOT_ENOUGH_HONBUL, 'Need more honbul'))

    # 재료생성
    RND = random.randint
    R = round
    C = math.ceil
    F = math.floor
    amount = eval(material_price['amount'])
    amount *= Properties.COLLECT_MATERIAL_MULTIPIER

    # 응답저장
    collect_material.material_id = material_id
    collect_material.amount = amount
    collect_material.honbul = self.honbul()


  def material_cooltime(self, material_cooltime):
    material_cooltime.cooltime = self.material_cooltime()
    max_count = Properties.COLLECT_MATERIAL_PER_DAY
    material_cooltime.current_count = max_count - self.material_count()
    material_cooltime.max_count = max_count
    material_cooltime.reset_count = self.material_reset_count()

  def reset_material_cooltime(self):
    pass

#----------------------------------------------------------------#

# 캐쉬상점
  def fill_eshop(self, market, eshop):
    pass

  def buy_in_eshop(self, pay_id, payment):
    pass

  def has_eshop_event(self):
    pass

#----------------------------------------------------------------#

# 충전소 
  def fill_cash_shop(self, market, cash_shop):
    pass

  def buy_in_cash_shop(self, goods, cash_shop):
    pass

#----------------------------------------------------------------#

# 도깨비상점
  def fill_reset_skill(self, reset_skill):
    price = Properties.HONBUL_FOR_RESET_SKILL
    discount = Properties.DISCOUNT_FOR_RESET_SKILL
    if discount > 0:
      price -= int(price * (discount/100.0))
    reset_skill.skill_point = self._selected_hero.reset_skill_point()
    reset_skill.price = price


  def fill_oni_shop(self, method, category, oni_shop):
    pass


  def buy_in_oni_shop(self, price, discount, goods, oni_shop):
    pass

#----------------------------------------------------------------#

# 서바이벌던전

  def check_survival_try(self):
    pass

  def spend_survival_try(self):
    pass

  def reset_survival_try(self):
    pass

  def update_survival_wave_record(self, wave):
    pass

  def fill_survival_buff(self, survival_buff):
    assert(self._info)
    survival_buff.survival_try_count = 0
    survival_buff.survival_try_per_day = 0
    survival_buff.reset_cooltime = 0
    survival_buff.wave = 0
    survival_buff.ranking = 0
    for key, val in Cache.survival_buffs().iteritems():
      buff = survival_buff.buffs.add()
      buff.buff_id = key
      buff.price = val['price']
      buff.name = val['name']
      buff.lock = True


#----------------------------------------------------------------#

# 사용자이력

#----------------------------------------------------------------#

# for test
  def set_cash(self, cash):
    db.execute("UPDATE ARPG_GT_USER SET CASH = %d WHERE USER_ID = %d" % (cash, self._user_id))
    self._info['cash'] = cash

  def set_honbul(self, honbul):
    db.execute("UPDATE ARPG_GT_USER SET HONBUL = %d WHERE USER_ID = %d" % (honbul, self._user_id))
    self._info['honbul'] = honbul

  def set_talisman(self, talisman):
    db.execute("UPDATE ARPG_GT_USER SET TALISMAN = %d WHERE USER_ID = %d" % (talisman, self._user_id))
    self._info['talisman'] = talisman

  def set_stone(self, stone):
    db.execute("UPDATE ARPG_GT_USER SET STONE = %d WHERE USER_ID = %d" % (stone, self._user_id))
    self._info['stone'] = stone

  def set_coin(self, coin):
    db.execute("UPDATE ARPG_GT_USER SET COIN = %d WHERE USER_ID = %d" % (coin, self._user_id))
    self._info['coin'] = coin

  def set_heart(self, heart):
    db.execute("UPDATE ARPG_GT_USER SET HEART = %d WHERE USER_ID = %d" % (heart, self._user_id))
    self._info['heart'] = heart

#----------------------------------------------------------------#
