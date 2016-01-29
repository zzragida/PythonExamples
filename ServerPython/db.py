# -*- coding: utf-8 -*-

from logger import logger
from collections import OrderedDict, defaultdict
from redis_cache import SimpleCache, cache_it
from datetime import datetime

from protocol import common_pb2
from util import from_utf8, to_utf8
from properties import Properties

import sqlrelay


CACHE_LIMIT=1024
CACHE_EXPIRE=10

cache = SimpleCache(limit=CACHE_LIMIT,
                    expire=CACHE_EXPIRE,
                    hashkeys=True,
                    host='localhost',
                    port=6379,
                    db=0,
                    namespace='M3ARPG')

#----------------------------------------------------------------#

def make_pp_user(game_id, kakao_id, hashed_kakao_id):
  con, cur = sqlrelay.client_cursor()
  cur.prepareQuery("""
BEGIN
  ARPG.MAKE_PP_USER(
    :game_id,
    :kakao_id,
    :inventory_size,
    :heart,
    :hashed_kakao_id,
    :user_id
  );
END;
""")
  cur.inputBind("game_id", game_id)
  cur.inputBind("kakao_id", kakao_id)
  cur.inputBind("inventory_size", Properties.MAX_INVENTORY_SIZE)
  cur.inputBind("heart", Properties.MAX_HEART)
  cur.inputBind("hashed_kakao_id", hashed_kakao_id)
  cur.defineOutputBindInteger("user_id")
  cur.executeQuery()

  sqlrelay.client_close(cur, con)

  user_id = cur.getOutputBindInteger("user_id")
  return user_id

#----------------------------------------------------------------#

def change_nickname(user_id, nickname):
  nickname = to_utf8(nickname)

  con, cur = sqlrelay.client_cursor()
  cur.prepareQuery("""
BEGIN
  ARPG.CHANGE_NICKNAME(
    :user_id,
    :nickname
  );
END;
""")
  cur.inputBind("user_id", user_id)
  cur.inputBind("nickname", nickname)
  cur.executeQuery()

  sqlrelay.client_close(cur, con)
  return True

#----------------------------------------------------------------#

def select_hero(user_id, selected_hero):
  return sqlrelay.execute("UPDATE ARPG_GT_USER SET SELECTED_HERO = %d WHERE USER_ID = %d" % (selected_hero, user_id))

#----------------------------------------------------------------#

def make_hero(user_id, job):
  con, cur = sqlrelay.client_cursor()
  cur.prepareQuery("""
BEGIN
  ARPG.MAKE_HERO(
    :user_id,
    :job,
    :hero_id,
    :button_a,
    :button_b,
    :button_c,
    :costume_id,
    :costume_level,
    :talisman
  );
END;
""")

  cur.inputBind("user_id", user_id)
  cur.inputBind("job", job)
  cur.defineOutputBindInteger("hero_id")
  cur.defineOutputBindInteger("button_a")
  cur.defineOutputBindInteger("button_b")
  cur.defineOutputBindInteger("button_c")
  cur.defineOutputBindInteger("costume_id")
  cur.defineOutputBindInteger("costume_level")
  cur.defineOutputBindInteger("talisman")
  cur.executeQuery()

  sqlrelay.client_close(cur, con)

  r = OrderedDict()
  r['hero_id'] = cur.getOutputBindInteger("hero_id")
  r['button_a'] = cur.getOutputBindInteger("button_a")
  r['button_b'] = cur.getOutputBindInteger("button_b")
  r['button_c'] = cur.getOutputBindInteger("button_c")
  r['costume_id'] = cur.getOutputBindInteger("costume_id")
  r['costume_level'] = cur.getOutputBindInteger("costume_level")
  r['tailsman'] = cur.getOutputBindInteger("talisman")

  h = None

  if r['hero_id'] > 0:
    h = hero(r['hero_id'])

  return h

#----------------------------------------------------------------#

def user_coupons(user_id):
  pass

#----------------------------------------------------------------#

def user_gifts(user_id):
  results = sqlrelay.execute_results("""
SELECT 
   PRESENT_ID
 , P_ID
 , TO_CHAR(ON_RECEIVE, 'YYYY/MM/DD HH24:MI:SS') 
FROM
   ARPG_GT_PRESENT 
WHERE
   USER_ID = %d 
ORDER BY
   ON_RECEIVE DESC
""" % (user_id))

  gift_list = OrderedDict()
  remove_list = []
  for idx, r in enumerate(results):
    present_id = int(r[0])
    p_id = int(r[1])
    on_receive = datetime.strptime(r[2], "%Y/%m/%d %H:%M:%S")

    if idx < Properties.PRESENT_BOX_SIZE:
      gift_list[present_id] = {
        'p_id': p_id,
        'on_receive': on_receive,
      }
    else:
      remove_list.append(present_id)

  if len(remove_list) > 0:
    remove_sql = "DELETE ARPG_GT_PRESENT WHERE PRESENT_ID IN ("
    remove_sql += remove_list[0]
    for p in remove_list[1:]:
      remove_sql += "," + p
    remove_sql += ")"
    sqlrelay.execute(remove_sql)
  
  return gift_list 

#----------------------------------------------------------------#

def user_payments(user_id):
  pass

#----------------------------------------------------------------#

def user_friends(user_id):
  pass

#----------------------------------------------------------------#

def user_kakao_friends(user_id):
  pass

#----------------------------------------------------------------#

def user_items(user_id):
  results = sqlrelay.execute_results("""
SELECT 
   ITEM_ID
 , E_ID
 , STACK
 , HERO_ID
 , LV
 , BROKEN 
FROM 
   ARPG_GT_INVENTORY 
WHERE 
   USER_ID = %d 
""" % (user_id))

  item_list = []
  for r in results:
    item_id = int(r[0])
    item_no = int(r[1])
    stack = int(r[2])
    hero_id = None if r[3] == '' else int(r[3])
    level = int(r[4])
    broken = True if r[5] == '1' else False

    item_list.append({
      'item_id': item_id,
      'item_no': item_no,
      'stack': stack,
      'hero_id': hero_id,
      'level': level,
      'broken': broken
    })

  return item_list

#----------------------------------------------------------------#

def user_rankings(user_id):
  pass

#----------------------------------------------------------------#

@cache_it(cache=cache)
def user(user_id):
  con, cur = sqlrelay.client_cursor()
  cur.prepareQuery("""
BEGIN
  ARPG.USER_INFO(
    :user_id
  , :nickname
  , :honbul
  , :cash
  , :talisman
  , :stone
  , :coin
  , :selected_hero
  , :heart
  , :heart_date
  , :current_date
  , :inventory_size
  , :searchable
  , :tutorial1
  , :tutorial2
  , :tutorial3
  , :tutorial4
  , :tutorial5
  , :tutorial6
  , :tutorial7
  , :terminate_abnormally
  , :dailystamp
  , :dailystamp_update
  , :today_quest
  , :today_quest_count
  , :material_count
  , :material_reset_count
  , :material_date
  , :promoted
  , :promotion_count
  , :break_up_count
  , :break_up_date
  , :kakao_heart_count
  , :kakao_heart_date
  , :kakao_id
  , :reg_date
  , :no_kakao_message
  , :no_kakao_profile
  , :review
  , :by_kakao_invitation
  );
END;
""")

  cur.inputBind("user_id", user_id)
  cur.defineOutputBindString("nickname", 256)
  cur.defineOutputBindInteger("honbul")
  cur.defineOutputBindInteger("cash")
  cur.defineOutputBindInteger("talisman")
  cur.defineOutputBindInteger("stone")
  cur.defineOutputBindInteger("coin")
  cur.defineOutputBindInteger("selected_hero")
  cur.defineOutputBindInteger("heart")
  cur.defineOutputBindString("heart_date", 20)
  cur.defineOutputBindString("current_date", 20)
  cur.defineOutputBindInteger("inventory_size")
  cur.defineOutputBindInteger("searchable")
  cur.defineOutputBindInteger("tutorial1")
  cur.defineOutputBindInteger("tutorial2")
  cur.defineOutputBindInteger("tutorial3")
  cur.defineOutputBindInteger("tutorial4")
  cur.defineOutputBindInteger("tutorial5")
  cur.defineOutputBindInteger("tutorial6")
  cur.defineOutputBindInteger("tutorial7")
  cur.defineOutputBindInteger("terminate_abnormally")
  cur.defineOutputBindInteger("dailystamp")
  cur.defineOutputBindInteger("dailystamp_update")
  cur.defineOutputBindInteger("today_quest")
  cur.defineOutputBindInteger("today_quest_count")
  cur.defineOutputBindInteger("material_count")
  cur.defineOutputBindInteger("material_reset_count")
  cur.defineOutputBindString("material_date", 20)
  cur.defineOutputBindInteger("promoted")
  cur.defineOutputBindInteger("promotion_count")
  cur.defineOutputBindInteger("break_up_count")
  cur.defineOutputBindString("break_up_date", 20)
  cur.defineOutputBindInteger("kakao_heart_count")
  cur.defineOutputBindString("kakao_heart_date", 20)
  cur.defineOutputBindInteger("kakao_id")
  cur.defineOutputBindString("reg_date", 20)
  cur.defineOutputBindInteger("no_kakao_message")
  cur.defineOutputBindInteger("no_kakao_profile")
  cur.defineOutputBindInteger("review")
  cur.defineOutputBindInteger("by_kakao_invitation")
  cur.executeQuery()

  sqlrelay.client_close(cur, con)

  nickname = cur.getOutputBindString("nickname")
  if nickname: nickname = from_utf8(nickname)
  honbul = cur.getOutputBindInteger("honbul")
  cash = cur.getOutputBindInteger("cash")
  talisman = cur.getOutputBindInteger("talisman")
  stone = cur.getOutputBindInteger("stone")
  coin = cur.getOutputBindInteger("coin")
  selected_hero = cur.getOutputBindInteger("selected_hero")
  heart = cur.getOutputBindInteger("heart")
  inventory_size = cur.getOutputBindInteger("inventory_size")
  searchable = True if cur.getOutputBindInteger("searchable") == 1 else False
  tutorial1 = True if cur.getOutputBindInteger("tutorial1") == 1 else False
  tutorial2 = True if cur.getOutputBindInteger("tutorial2") == 1 else False
  tutorial3 = True if cur.getOutputBindInteger("tutorial3") == 1 else False
  tutorial4 = True if cur.getOutputBindInteger("tutorial4") == 1 else False
  tutorial5 = True if cur.getOutputBindInteger("tutorial5") == 1 else False
  tutorial6 = True if cur.getOutputBindInteger("tutorial6") == 1 else False
  tutorial7 = True if cur.getOutputBindInteger("tutorial7") == 1 else False
  dailystamp = cur.getOutputBindInteger("dailystamp")
  kakao_id = cur.getOutputBindInteger("kakao_id")
  no_kakao_message = True if cur.getOutputBindInteger("no_kakao_message") == 1 else False
  no_kakao_profile = True if cur.getOutputBindInteger("no_kakao_profile") == 1 else False
  review = True if cur.getOutputBindInteger("review") == 1 else False
  by_kakao_invitation = True if cur.getOutputBindInteger("by_kakao_invitation") == 1 else False
 
  user = {
    'kakao_id': kakao_id,
    'nickname': nickname,
    'honbul': honbul,
    'cash': cash,
    'talisman': talisman,
    'stone': stone,
    'coin': coin,
    'heart': heart,
    'selected_hero': selected_hero,
    'inventory_size': inventory_size,
    'searchable': searchable,
    'dailystamp': dailystamp,
    'review': review,
    'by_kakao_invitation': by_kakao_invitation,
    'tutorial1': tutorial1,
    'tutorial2': tutorial2,
    'tutorial3': tutorial3,
    'tutorial4': tutorial4,
    'tutorial5': tutorial5,
    'tutorial6': tutorial6,
    'tutorial7': tutorial7,
    'no_kakao_message': no_kakao_message,
    'no_kakao_profile': no_kakao_profile,
    'review': review,
  } 

  return user   

#----------------------------------------------------------------#

def user_heroes(user_id):
  results = sqlrelay.execute_results("""
SELECT 
   HERO_ID
 , JOB
 , LV
 , EXP
 , TO_CHAR(REG_DATE, 'YYYY/MM/DD HH24:MI:SS')
 , PLAYING_TIME
 , LAST_COSTUME_ID
 , BUTTON_A
 , BUTTON_B
 , BUTTON_C
 , EXPAND_BUTTON
 , SKILL_POINT
 , UNLOCK_STAGE_COUNT
 , TO_CHAR(UNLOCK_STAGE_COUNT_DATE, 'YYYY/MM/DD HH24:MI:SS') 
FROM
   ARPG_GT_HERO 
WHERE
   USER_ID = %d 
""" % (user_id))

  hero_list = []
  for r in results:
		hero_id = int(r[0])
		job = int(r[1])
		level = int(r[2])
		exp = int(r[3])
		reg_date = r[4]
		playing_time = int(r[5])
		last_costume_id = int(r[6])
		button_a = int(r[7])
		button_b = int(r[8])
		button_c = int(r[9])
		expand_button = True if r[10] == '1' else False
		skill_point = int(r[11])
		unlock_stage_count = int(r[12])
		unlock_stage_count_date = r[13]

		hero_list.append({
			'hero_id': hero_id,
			'job': job,
			'level': level,
			'exp': exp,
			'reg_date': reg_date,
			'playing_time': playing_time,
			'last_costume_id': last_costume_id,
			'button_a': button_a,
			'button_b': button_b,
			'button_c': button_c,
			'expand_button': expand_button,
			'skill_point': skill_point,
			'unlock_stage_count': unlock_stage_count,
			'unlock_stage_count_date': unlock_stage_count_date,
		})
  
  return hero_list

#----------------------------------------------------------------#

def hero(hero_id):
  r = sqlrelay.execute_results("""
SELECT 
   HERO_ID
 , JOB
 , LV
 , EXP
 , TO_CHAR(REG_DATE, 'YYYY/MM/DD HH24:MI:SS')
 , PLAYING_TIME
 , LAST_COSTUME_ID
 , BUTTON_A
 , BUTTON_B
 , BUTTON_C
 , EXPAND_BUTTON
 , SKILL_POINT
 , UNLOCK_STAGE_COUNT
 , TO_CHAR(UNLOCK_STAGE_COUNT_DATE, 'YYYY/MM/DD HH24:MI:SS') 
FROM
   ARPG_GT_HERO 
WHERE
   HERO_ID = %d 
""" % (hero_id), multiple=False)

  if not r:
    return None

  hero_id = int(r[0])
  job = int(r[1])
  level = int(r[2])
  exp = int(r[3])
  reg_date = r[4]
  playing_time = int(r[5])
  last_costume_id = int(r[6])
  button_a = int(r[7])
  button_b = int(r[8])
  button_c = int(r[9])
  expand_button = True if r[10] == '1' else False
  skill_point = int(r[11])
  unlock_stage_count = int(r[12])
  unlock_stage_count_date = r[13]

  hero = {
    'hero_id': hero_id,
    'job': job,
    'level': level,
    'exp': exp,
    'reg_date': reg_date,
    'playing_time': playing_time,
    'last_costume_id': last_costume_id,
    'button_a': button_a,
    'button_b': button_b,
    'button_c': button_c,
    'expand_button': expand_button,
    'skill_point': skill_point,
    'unlock_stage_count': unlock_stage_count,
    'unlock_stage_count_date': unlock_stage_count_date,
  }
  
  return hero

#----------------------------------------------------------------#

def user_costumes(user_id):
  results = sqlrelay.execute_results("""
SELECT 
   a.COSTUME_ID
 , a.LV
 , b.JOB 
 , b.COSTUME_ID 
FROM 
   ARPG_GT_COSTUME a
 , ARPG_BT_COSTUME b
WHERE
     a.BASE_COSTUME_ID = b.COSTUME_ID
 AND USER_ID = %d 
""" % (user_id))

  costume_list = []
  for r in results:
    costume_id = int(r[0])
    level = int(r[1])
    job = int(r[2])
    costume_no = int(r[3])

    costume_list.append({
      'costume_id': costume_id,
      'level': level,
      'job': job,
      'costume_no': costume_no,
    })

  return costume_list

#----------------------------------------------------------------#

def user_achivements(user_id):
  results = sqlrelay.execute_results("""
SELECT 
   A_ID
 , REPEAT
 , REWARD_REPEAT
FROM 
   ARPG_GT_ACHIVEMENT 
WHERE 
   USER_ID = %d
""" % (user_id))

  achivement_list = OrderedDict()
  for r in results:
    a_id = int(r[0])
    repeat = int(r[1])
    reward_repeat = int(r[2])

    achivement_list[str(a_id)] = {
      'a_id': a_id,
      'repeat': repeat,
      'reward_repeat': reward_repeat
    }

  return achivement_list

#----------------------------------------------------------------#

def execute(sql):
  sqlrelay.execute(sql)

#----------------------------------------------------------------#

def dungeons():
  results = sqlrelay.execute_results("""
SELECT 
   DUNGEON_ID
 , NAME
 , NEXT_DUNGEON
 , TYPE
 , MULTIPLAY
 , WDAY
 , LV_MIN
 , LV_MAX 
FROM 
  ARPG_BT_DUNGEON 
ORDER BY
  DUNGEON_ID
""")

  dungeon_list = defaultdict()
  dungeon_list[common_pb2.DUNGEON_TUTORIAL] = OrderedDict()
  dungeon_list[common_pb2.DUNGEON_EPIC] = OrderedDict()
  dungeon_list[common_pb2.DUNGEON_DAILY] = OrderedDict()
  dungeon_list[common_pb2.DUNGEON_SURVIVAL] = OrderedDict()
  dungeon_list[common_pb2.DUNGEON_EVENT] = OrderedDict()

  for r in results:
    dungeon_id = int(r[0])
    name = r[1]
    next_dungeon = int(r[2])
    type = int(r[3])
    multiplay = True if r[4] == '1' else False
    wday = int(r[5])
    lv_min = int(r[6])
    lv_max = int(r[7])

    dungeon = dungeon_list[type]
    dungeon[dungeon_id] = {
      'dungeon_id': dungeon_id,
      'name': name,
      'next_dungeon': next_dungeon,
      'type': type,
      'multiplay': multiplay,
      'wday': wday,
      'lv_min': lv_min,
      'lv_max': lv_max
    }

  return dungeon_list

#----------------------------------------------------------------#

def stages():
  results = sqlrelay.execute_results("""
SELECT 
   STAGE_ID
 , NAME
 , NEXT_STAGE_ID
 , DUNGEON_ID
 , MAX_PLAYER
 , TYPE
 , UNLOCK_CASH
 , UNLOCKED
 , SCENE
 , HEART
 , COOLTIME
 , COOLTIME_COUNT
 , COOLTIME_RESET_CASH
 , REWARD_HONBUL
 , REWARD_MATERIAL
 , REWARD_BOX_EASY
 , REWARD_BOX_NORMAL
 , REWARD_BOX_HARD 
FROM
   ARPG_BT_STAGE 
ORDER BY
   STAGE_ID
""")

  stage_list = OrderedDict()
  for r in results:
    stage_id = int(r[0])
    name = from_utf8(r[1])
    next_stage_id = int(r[2])
    dungeon_id = int(r[3])
    max_player = int(r[4])
    type = int(r[5])
    unlock_cash = int(r[6])
    unlocked = True if r[7] == '1' else False
    scene = r[8]
    heart = int(r[9])
    cooltime = int(r[10])
    cooltime_count = int(r[11])
    cooltime_cash = int(r[12])
    reward_honbul = r[13]
    reward_material = r[14]
    reward_box_easy = r[15]
    reward_box_normal = r[16]
    reward_box_hard = r[17]

    stage_list[stage_id] = {
      'stage_id': stage_id,
      'name': name,
      'next_stage_id': next_stage_id,
      'dungeon_id': dungeon_id,
      'max_player': max_player,
      'type': type,
      'unlock_cash': unlock_cash,
      'unlocked': unlocked,
      'scene': scene,
      'heart': heart,
      'cooltime': cooltime,
      'cooltime_count': cooltime_count,
      'cooltime_cash': cooltime_cash,
      'reward_honbul': reward_honbul,
      'reward_material': reward_material,
      'reward_box_easy': reward_box_easy,
      'reward_box_normal': reward_box_normal,
      'reward_box_hard': reward_box_hard,
    }

  return stage_list

#----------------------------------------------------------------#

def stage_waves():
  results = sqlrelay.execute_results("""
SELECT 
   a.STAGE_ID
 , a.WAVE_SEQ
 , b.DIFFICULTY
 , a.TIME_LIMIT
 , a.DESCRIPTION
 , b.MONSTERS
 , b.REGION 
FROM
   ARPG_BT_WAVE a 
   LEFT JOIN ARPG_BT_SPAWN b ON a.SPAWN_ID = b.SPAWN_ID 
ORDER BY 
   a.STAGE_ID, a.WAVE_SEQ, b.DIFFICULTY
""")

  stage_wave_list = OrderedDict()
  for r in results:
    stage_id = int(r[0])
    wave_seq = int(r[1])
    difficulty = int(r[2])
    time_limit = int(r[3])
    description = from_utf8(r[4])
    monsters = []
    for infos in r[5].split(','):
      mon = infos.split('|')
      monsters.append({
        'monster_id': int(mon[0]),
        'level': int(mon[1]),
        'count': int(mon[2]),
      })
    region = r[6]

    stage_wave_list[stage_id] = {
      'stage_id': stage_id,
      'wave_seq': wave_seq,
      'description': description,
      'time_limit': time_limit,
      'monsters': monsters,
      'region': region,
    }

  return stage_wave_list

#----------------------------------------------------------------#

def monsters():
  results = sqlrelay.execute_results("""
SELECT
   a.MONSTER_ID
 , a.NAME
 , b.LV
 , b.HP
 , b.MP
 , b.ATK
 , b.DEF
 , b.EXP
 , b.HIT_RATE
 , b.CTR
 , b.CTD
 , b.HONBUL
 , b.EVASION_RATE
 , b.COUNTER_RATE
 , b.EVASION_SKILL
 , b.COUNTER_SKILL
 , b.AI_0
 , b.AI_1
 , b.AI_2
 , b.AI_3
 , b.AI_4
 , b.AI_5
 , b.AI_6
 , b.AI_7
 , b.AI_8
 , b.AI_9
 , b.AI_10
 , b.ITEM 
FROM
   ARPG_BT_MONSTER a 
   LEFT JOIN ARPG_BT_MONSTER_LEVEL b ON a.MONSTER_ID = b.MONSTER_ID
""")

  monster_list = OrderedDict()
  for r in results:
    if r[2] == '': continue
    monster_id = int(r[0])
    name = from_utf8(r[1])
    level = int(r[2])
    hp = int(r[3])
    mp = int(r[4])
    atk = int(r[5])
    attr_def = int(r[6])
    exp = int(r[7])
    hit_rate = float(r[8])
    ctr = float(r[9])
    ctd = float(r[10])
    honbul = int(r[11])
    evasion_rate = float(r[12])
    counter_rate = float(r[13])
    evasion_skill = int(r[14])
    counter_skill = int(r[15])
    ai_0 = float(r[16])
    ai_1 = float(r[17])
    ai_2 = float(r[18])
    ai_3 = float(r[19])
    ai_4 = float(r[20])
    ai_5 = float(r[21])
    ai_6 = float(r[22])
    ai_7 = float(r[23])
    ai_8 = float(r[24])
    ai_9 = float(r[25])
    ai_10 = float(r[26])
    item = int(r[27])

    monster_list[monster_id] = {
      'name': name,
      'level': level,
      'hp': hp,
      'mp': mp,
      'atk': atk,
      'def': attr_def,
      'exp': exp,
      'hit_rate': hit_rate,
      'ctr': ctr,
      'ctd': ctd,
      'honbul': honbul,
      'evasion_rate': evasion_rate,
      'counter_rate': counter_rate,
      'evasion_skill': evasion_skill,
      'counter_skill': counter_skill,
      'ai_0': ai_0,
      'ai_1': ai_1,
      'ai_2': ai_2,
      'ai_3': ai_3,
      'ai_4': ai_4,
      'ai_5': ai_5,
      'ai_6': ai_6,
      'ai_7': ai_7,
      'ai_8': ai_8,
      'ai_9': ai_9,
      'ai_10': ai_10,
      'item': item,
    }

  return monster_list

#----------------------------------------------------------------#

def survival_waves():
  results = sqlrelay.execute_results("""
SELECT 
   WAVE_ID
 , MONSTERS
 , REGION
 , TIME_LIMIT
 , REWARD_GROUP_ID
 , DESCRIPTION
 , SCENE 
FROM
   ARPG_BT_SURVIVAL_WAVE 
ORDER BY 
   WAVE_ID
""")

  survival_wave_list = OrderedDict()
  for r in results:
    wave_id = int(r[0])
    monsters = []
    for infos in r[1].split(','):
      mon = infos.split('|')
      monsters.append({
        'monster_id': int(mon[0]),
        'level': int(mon[1]),
        'count': int(mon[2]),
      })
    region = r[2]
    time_limit = int(r[3])
    reward_group_id = int(r[4])
    description = from_utf8(r[5])
    scene = r[6]

    survival_wave_list[wave_id] = {
      'monsters': monsters,
      'region': region,
      'time_limit': time_limit,
      'reward_group_id': reward_group_id,
      'description': description,
      'scene': scene,
    }

  return survival_wave_list

#----------------------------------------------------------------#

def event_dungeons():
  results = sqlrelay.execute_results("""
SELECT 
   FEVER_ID 
 , DUNGEON_ID
 , DUNGEON_TYPE
 , TO_CHAR(START_DATE, 'YYYY/MM/DD HH24:MI:SS')
 , TO_CHAR(FINISH_DATE, 'YYYY/MM/DD HH24:MI:SS') 
FROM
   ARPG_GT_FEVER 
WHERE
   SYSTIMESTAMP <= FINISH_DATE 
ORDER BY
   DUNGEON_TYPE, FEVER_ID
""")

  event_dungeon_list = defaultdict()
  event_dungeon_list[common_pb2.DUNGEON_EVENT] = defaultdict()
  event_dungeon_list[common_pb2.DUNGEON_SURVIVAL] = defaultdict()

  for r in results:
    fever_id = int(r[0])
    dungeon_id = int(r[1])
    dungeon_type = int(r[2])
    start_date = datetime.strptime(r[3], "%Y/%m/%d %H:%M:%S")
    finish_date = datetime.strptime(r[4], "%Y/%m/%d %H:%M:%S")

    event_dungeon = event_dungeon_list[dungeon_type]
    event_dungeon[fever_id] = {
      'dungeon_id': dungeon_id,
      'start_date': start_date,
      'finish_date': finish_date,
    }

  return event_dungeon_list 

#----------------------------------------------------------------#

def costumes():
  results = sqlrelay.execute_results("""
SELECT
   COSTUME_ID
 , NAME
 , JOB
 , TO_CHAR(PROMOTION_START, 'YYYY/MM/DD HH24:MI:SS')
 , TO_CHAR(PROMOTION_END, 'YYYY/MM/DD HH24:MI:SS')
 , UG_PROPERTIES
 , UG_HONBUL
 , UG_CASH
 , MATERIAL
 , MARKET_PRICE
 , MAKE_HONBUL 
FROM
   ARPG_BT_COSTUME 
ORDER BY
   COSTUME_ID
""")

  costume_list = defaultdict()
  costume_list[common_pb2.JOB_SWORD] = OrderedDict()
  costume_list[common_pb2.JOB_ARCHER] = OrderedDict()
  costume_list[common_pb2.JOB_SHAMAN] = OrderedDict()

  for r in results:
    costume_id = int(r[0])
    name = from_utf8(r[1])
    job = int(r[2])
    promotion_start = None if r[3] == '' else datetime.strptime(r[3], "%Y/%m/%d %H:%M:%S")
    promotion_end = None if r[4] == '' else datetime.strptime(r[4], "%Y/%m/%d %H:%M:%S")
    ug_properties = r[5]
    ug_honbul = r[6]
    ug_cash = int(r[7])
    material = []
    for infos in r[8].split(','):
      parts = infos.split('|')
      if len(parts) == 2:
        material.append({
          'parts_id': int(parts[0]),
          'stage_id': int(parts[1]),
        })
    market_price = int(r[9])
    make_honbul = int(r[10])

    costume = costume_list[job]
    costume[costume_id] = {
      'name': name,
      'promotion_start': promotion_start,
      'promotion_end': promotion_end,
      'ug_properties': ug_properties,
      'ug_honbul': ug_honbul,
      'ug_cash': ug_cash,
      'material': material,
      'market_price': market_price,
      'make_honbul': make_honbul,
    }

  return costume_list

#----------------------------------------------------------------#

def items():
  results = sqlrelay.execute_results("""
SELECT
   E_ID
 , TYPE
 , STONE
 , JOB
 , REQ_LV
 , COMBI
 , PROPERTIES
 , STACK
 , NAME
 , UG_SUCCESS
 , UG_STONE
 , UG_STONE_SAFE
 , CRASH
 , UG_PROPERTIES
 , FIX
 , HONBUL
 , UG_HONBUL
 , SORT_ORDER 
FROM
   ARPG_BT_EQUIPMENT
""")

  item_list = OrderedDict()
  for r in results:
    item_no = int(r[0])
    type = int(r[1])
    stone_rate = int(r[2])
    job = int(r[3])
    required_lv = int(r[4])
    combi = int(r[5])
    properties = r[6].split(',')
    stack = True if r[7] == '1' else False
    name = from_utf8(r[8])
    ug_success = r[9]
    ug_stone = r[10]
    ug_stone_safe = r[11]
    crash = r[12]
    ug_properties = r[13]
    fix = r[14]
    honbul = r[15]
    ug_honbul = r[16]
    sort_order = int(r[17])

    item_list[item_no] = {
      'type': type,
      'stone_rate': stone_rate,
      'job': job,
      'required_lv': required_lv,
      'combi': combi,
      'properties': properties,
      'stack': stack,
      'name': name,
      'ug_success': ug_success,
      'ug_stone': ug_stone,
      'ug_stone_safe': ug_stone_safe,
      'crash': crash,
      'ug_properties': ug_properties,
      'fix': fix,
      'honbul': honbul,
      'ug_honbul': ug_honbul,
      'sort_order': sort_order,
    }

  return item_list

#----------------------------------------------------------------#

def combinations():
  results = sqlrelay.execute_results("""
SELECT
   COMBI_ID
 , NAME
 , PROPERTIES 
FROM
   ARPG_BT_ITEM_COMBI
""")

  combination_list = defaultdict()
  for r in results:
    combi_id = int(r[0])
    name = from_utf8(r[1])
    properties = r[2].split(',')

    combination_list[combi_id] = {
      'name': name,
      'properties': properties,
    }
  
  return combination_list

#----------------------------------------------------------------#

def blueprints():
  results = sqlrelay.execute_results("""
SELECT
   BP_ID
 , NAME
 , ITEMS
 , MATERIALS 
FROM
   ARPG_BT_BLUEPRINT
""")

  blueprint_list = OrderedDict()
  for r in results:
    bp_id = int(r[0])
    name = from_utf8(r[1])
    items = []
    for infos in r[2].split(','):
      item = infos.split('|')
      items.append({
        'item_id': int(item[0]),
        'count': int(item[1]),
      })
    materials = []
    for infos in r[3].split(','):
      material = infos.split('|')
      materials.append({
        'item_id': int(material[0]),
        'count': int(material[1]),
        'stage_id': int(material[2]),
      })

    blueprint_list[bp_id] = {
      'name': name,
      'items': items,
      'materials': materials,
    }
  
  return blueprint_list

#----------------------------------------------------------------#

def levels():
  results = sqlrelay.execute_results("""
SELECT
   JOB
 , LV
 , HP
 , MP
 , ATK
 , DEF
 , CTR
 , CTD
 , EXP 
 , CCM
 , DEX
 , HPR
 , HPT
 , MPR
 , MPT 
FROM
   ARPG_BT_LEVEL 
""")

  level_list = defaultdict()
  level_list[common_pb2.JOB_SWORD] = OrderedDict()
  level_list[common_pb2.JOB_ARCHER] = OrderedDict()
  level_list[common_pb2.JOB_SHAMAN] = OrderedDict()

  for r in results:
    job = int(r[0])
    lv = int(r[1])
    hp = int(r[2])
    mp = int(r[3])
    atk = int(r[4])
    attr_def = int(r[5])
    ctr = float(r[6])
    ctd = float(r[7])
    next_exp = int(r[8])
    ccm = int(r[9])
    dex = int(r[10])
    hpr = int(r[11])
    hpt = float(r[12])
    mpr = int(r[13])
    mpt = float(r[14])
    hb = 0
    ctm = 0
    mov = 100.0
    atr = 0
    dfr = 0
    exp = 0

    level = level_list[job]
    level[lv] = {
      'hp': hp,
      'mp': mp,
      'atk': atk,
      'def': attr_def,
      'ctr': ctr,
      'ctd': ctd,
      'next_exp': exp,
      'ccm': ccm,
      'dex': dex,
      'hpr': hpr,
      'hpt': hpt,
      'mpr': mpr,
      'mpt': mpt,
      'hb': hb,
      'ctm': ctm,
      'mov': mov,
      'atr': atr,
      'dfr': dfr,
      'exp': exp,
    }

  return level_list

#----------------------------------------------------------------#

def lotterys():
  lottery_list = defaultdict()
  # 의상조각
  lottery_list[common_pb2.LOTTERY_COSTUME_PART] = [{
    'count': common_pb2.LOTTERY_COUNT_ONE,
    'cash': Properties.CASH_FOR_LOTTERY_COSTUME_PART_1,
    'talisman': 0,
  }, {
    'count': common_pb2.LOTTERY_COUNT_TEN,
    'cash': Properties.CASH_FOR_LOTTERY_COSTUME_PART_10,
    'talisman': 0,
  }]

  # 도면
  lottery_list[common_pb2.LOTTERY_BLUEPRINT] = [{
    'count': common_pb2.LOTTERY_COUNT_ONE,
    'cash': 0,
    'talisman': Properties.TALISMAN_FOR_LOTTERY_BLUEPRINT_1,
  }, {
    'count': common_pb2.LOTTERY_COUNT_TEN,
    'cash': 0,
    'talisman': Properties.TALISMAN_FOR_LOTTERY_BLUEPRINT_10,
  }]

  # 일반무기
  lottery_list[common_pb2.LOTTERY_WEAPON] = [{
    'count': common_pb2.LOTTERY_COUNT_ONE,
    'cash': 0,
    'talisman': Properties.TALISMAN_FOR_LOTTERY_WEAPON_1,
  }, {
    'count': common_pb2.LOTTERY_COUNT_TEN,
    'cash': 0,
    'talisman': Properties.TALISMAN_FOR_LOTTERY_WEAPON_10,
  }]

  return lottery_list

#----------------------------------------------------------------#

def lottery_items():
  results = sqlrelay.execute_results("""
SELECT
   LOTTERY_ID
 , GIFT
 , FREQUENCY
 , GRADE
 , LV_TIER
 , JOB 
FROM
   ARPG_BT_LOTTERY 
WHERE
   FREQUENCY > 0
""")

  lottery_item_list = defaultdict()
  lottery_item_list[common_pb2.LOTTERY_ADVANCE_WEAPON] = OrderedDict()
  lottery_item_list[common_pb2.LOTTERY_WEAPON] = OrderedDict()
  lottery_item_list[common_pb2.LOTTERY_ADVANCE_SHIELD] = OrderedDict()
  lottery_item_list[common_pb2.LOTTERY_SHIELD] = OrderedDict()
  lottery_item_list[common_pb2.LOTTERY_ADVANCE_ACCESSORY] = OrderedDict()
  lottery_item_list[common_pb2.LOTTERY_ACCESSORY] = OrderedDict()
  lottery_item_list[common_pb2.LOTTERY_COSTUME_PART] = OrderedDict()
  lottery_item_list[common_pb2.LOTTERY_BLUEPRINT] = OrderedDict()

  for r in results:
    lottery_id = int(r[0])
    gift = int(r[1])
    frequency = int(r[2])
    grade = int(r[3])
    lv_tier = int(r[4])
    job = int(r[5])

    lottery_item = lottery_item_list[(lottery_id / 10000) - 22000]
    lottery_item[lottery_id] = {
      'gift': gift,
      'frequency': frequency,
      'grade': grade,
      'lv_tier': lv_tier,
      'job': job,
    }
  
  return lottery_item_list

#----------------------------------------------------------------#

def lottery_tiers():
  results = sqlrelay.execute_results("""
SELECT
   LV_TIER
 , LV_START
 , LV_END 
FROM
   ARPG_BT_LOTTERY_TIER 
""")

  lottery_tier_list = OrderedDict()
  for r in results:
    lv_tier = int(r[0])
    lv_start = int(r[1])
    lv_end = int(r[2])

    lottery_tier_list[lv_tier] = {
      'lv_start': lv_start,
      'lv_end': lv_end,
    }

  return lottery_tier_list

#----------------------------------------------------------------#

def skills():
  results = sqlrelay.execute_results("""
SELECT 
   a.SKILL_ID
 , a.BUTTON
 , a.MAX_LV
 , a.MIN_LV
 , a.JOB
 , b.REQUIRED_LV 
FROM
   ARPG_BT_SKILL a, ARPG_BT_SKILL_REINFORCE b 
WHERE
   a.JOB = b.JOB AND b.LV = 1 AND a.SKILL_ID = b.SKILL_ID 
""")

  skill_list = defaultdict()
  skill_list[common_pb2.JOB_SWORD] = OrderedDict()
  skill_list[common_pb2.JOB_ARCHER] = OrderedDict()
  skill_list[common_pb2.JOB_SHAMAN] = OrderedDict()

  for r in results:
    skill_id = int(r[0])
    button = True if r[1] == '1' else False
    max_lv = int(r[2])
    min_lv = int(r[3])
    job = int(r[4])
    required_lv = int(r[5])

    skill = skill_list[job]
    skill[skill_id] = {
      'button': button,
      'max_lv': max_lv,
      'min_lv': min_lv,
      'required_lv': required_lv,
    }

  for skill in skill_list.values():
    total_level = 0
    for s in skill.values():
      total_level = s['max_lv']
    skill['total_leve'] = total_level

  return skill_list

#----------------------------------------------------------------#

def skill_costs():
  results = sqlrelay.execute_results("""
SELECT
   SKILL_ID
 , JOB
 , LV
 , HONBUL
 , REQUIRED_LV
 , SKILL_POINT 
FROM
   ARPG_BT_SKILL_REINFORCE 
""")

  skill_cost_list = defaultdict()
  skill_cost_list[common_pb2.JOB_SWORD] = OrderedDict()
  skill_cost_list[common_pb2.JOB_ARCHER] = OrderedDict()
  skill_cost_list[common_pb2.JOB_SHAMAN] = OrderedDict()

  for r in results:
    skill_id = int(r[0])
    job = int(r[1])
    level = int(r[2])
    honbul = int(r[3])
    required_lv = int(r[4])
    skill_point = int(r[5])

    skill_cost = skill_cost_list[job]
    if skill_cost.has_key(skill_id):
      skill_cost_id = skill_cost[skill_id]
    else:
      skill_cost_id = OrderedDict()
      skill_cost[skill_id] = skill_cost_id

    skill_cost_id[level] = {
      'honbul': honbul,
      'required_lv': required_lv,
      'skill_point': skill_point,
    }

  return skill_cost_list

#----------------------------------------------------------------#

def eshops():
  results = sqlrelay.execute_results("""
SELECT 
   CASH
 , PRODUCT_ID
 , PMANG_ID
 , SALE_MARK
 , MESSAGE
 , MARKET 
 , SALE 
FROM
  ARPG_BT_ESHOP 
""")

  eshop_list = OrderedDict()
  event_eshop_list = OrderedDict()

  for r in results:
    cash = int(r[0])
    product_id = r[1]
    pmang_id = r[2]
    sale_mark = int(r[3])
    message = from_utf8(r[4])
    market = int(r[5])
    sale = True if r[6] == '1' else False

    if sale:
      event_eshop_list[product_id] = {
        'cash': cash,
        'pmang_id': pmang_id,
        'sale_mark': sale_mark,
        'message': message,
        'market': market,
      }
    else:
      eshop_list[product_id] = {
        'cash': cash,
        'pmang_id': pmang_id,
        'sale_mark': sale_mark,
        'message': message,
        'market': market,
      }

  return (eshop_list, event_eshop_list)

#----------------------------------------------------------------#

def cash_shops():
  results = sqlrelay.execute_results("""
SELECT 
   CATEGORY
 , CASH
 , TALISMAN
 , STONE
 , COIN
 , HEART
 , HONBUL
 , SALE_MARK
 , MESSAGE 
FROM
  ARPG_BT_CASH_SHOP 
ORDER BY
  CATEGORY
""")

  cash_shop_list = OrderedDict()
  for r in results:
    category = int(r[0])
    cash = int(r[1])
    talisman = int(r[2])
    stone = int(r[3])
    coin = int(r[4])
    heart = int(r[5])
    honbul = int(r[6])
    sale_mark = int(r[7])
    message = from_utf8(r[8])

    if cash_shop_list.has_key(category):
      cash_shop = cash_shop_list[category]
    else:
      cash_shop = OrderedDict()
      cash_shop_list[category] = cash_shop

    cash_shop[cash] = {
      'talisman': talisman,
      'stone': stone,
      'coin': coin,
      'heart': heart,
      'honbul': honbul,
      'sale_mark': sale_mark,
      'message': message,
    }

  return cash_shop_list

#----------------------------------------------------------------#

def keyword_coupons():
  results = sqlrelay.execute_results("""
SELECT
   a.COUPON_ID
 , a.COUPON_AVL_START
 , a.COUPON_AVL_END
 , b.COUPON_CODE
 , a.DUP_USER_CNT 
FROM
   ARPG_BT_COUPON a, ARPG_BT_COUPON_CODE b 
WHERE
   a.type = %d AND a.COUPON_START_SRL = b.COUPON_SRL
""" % (common_pb2.COUPON_KEYWORD))

  keyword_coupon_list = OrderedDict()
  for r in results:
    coupon_id = int(r[0])
    coupon_avl_start = datetime.strptime(r[1], "%Y%m%d%H%M%S")
    coupon_avl_end = datetime.strptime(r[2], "%Y%m%d%H%M%S")
    keyword = r[3]
    reuse = True if r[4] == '1' else False

    keyword_coupon_list[coupon_id] = {
      'coupon_avl_start': coupon_avl_start,
      'coupon_avl_end': coupon_avl_end,
      'keyword': keyword,
      'reuse': reuse,
    }

  return keyword_coupon_list

#----------------------------------------------------------------#

def oni_shops():
  results = sqlrelay.execute_results("""
SELECT 
   GOODS_ID
 , ITEM_ID
 , HONBUL
 , CASH
 , JOB
 , REQUIRED_LV 
 , SORT_ORDER 
FROM
  ARPG_BT_ONI_SHOP 
ORDER BY
  GOODS_ID
""")

  oni_shop_list = defaultdict()
  oni_shop_list[common_pb2.ONI_GOODS_HONBUL_WEAPON] = OrderedDict()
  oni_shop_list[common_pb2.ONI_GOODS_HONBUL_SHIELD] = OrderedDict()
  oni_shop_list[common_pb2.ONI_GOODS_HONBUL_ACCESSORY] = OrderedDict()
  oni_shop_list[common_pb2.ONI_GOODS_HONBUL_REST] = OrderedDict()
  oni_shop_list[common_pb2.ONI_GOODS_CASH_WEAPON] = OrderedDict()
  oni_shop_list[common_pb2.ONI_GOODS_CASH_SHIELD] = OrderedDict()
  oni_shop_list[common_pb2.ONI_GOODS_CASH_ACCESSORY] = OrderedDict()
  oni_shop_list[common_pb2.ONI_GOODS_CASH_REST] = OrderedDict()

  for r in results:
    goods_id = int(r[0])
    item_id = int(r[1])
    honbul = int(r[2])
    cash = int(r[3])
    job = int(r[4])
    required_lv = int(r[5])
    sort_order = int(r[6])
    price = 0
    oni_shop = None
    
    if honbul > 0:  price = honbul
    elif cash > 0:  price = cash

    oni_shop = oni_shop_list[goods_id / 100000]
    oni_shop[goods_id] = {
      'item_id': item_id,
      'price': price,
      'job': job,
      'required_lv': required_lv,
      'sort_order': sort_order
    }

  return oni_shop_list

#----------------------------------------------------------------#

def treasures():
  results = sqlrelay.execute_results("""
SELECT
   GROUP_ID
 , ITEM_ID
 , FREQUENCY
FROM
   ARPG_BT_TREASURE
""")

  treasure_list = OrderedDict()
  for r in results:
    group_id = int(r[0])
    item_id = int(r[1])
    frequency = int(r[2])

    if treasure_list.has_key(group_id):
      treasure = treasure_list[group_id]
    else:
      treasure = OrderedDict()
      treasure_list[group_id] = treasure

    treasure[item_id] = {
      'frequency': frequency,
    }

  # 토탈 확률계산
  for treasure in treasure_list.values():
    total = 0
    for item in treasure.values():
      total += item['frequency']
    treasure['total'] = total

  return treasure_list
  

#----------------------------------------------------------------#

def gifts():
  results = sqlrelay.execute_results("""
SELECT
   P_ID
 , TYPE
 , VALUE
 , TITLE
 , MESSAGE 
FROM
   ARPG_BT_PRESENT 
""")

  gift_list = OrderedDict()
  for r in results:
    p_id = int(r[0])
    type = int(r[1])
    value = int(r[2])
    title = from_utf8(r[3])
    message = from_utf8(r[4])

    gift_list[p_id] = {
      'type': type,
      'value': value,
      'title': title,
      'message': message,
    }

  return gift_list

#----------------------------------------------------------------#

def level_up_gifts():
  results = sqlrelay.execute_results("""
SELECT
   LV
 , JOB
 , E_ID
 , P_ID 
FROM 
   ARPG_BT_EVENT 
WHERE
   TYPE = %d AND USE = 1
""" % (common_pb2.EVENT_LEVEL_UP))

  level_up_gift_list = defaultdict()
  level_up_gift_list[common_pb2.JOB_SWORD] = OrderedDict()
  level_up_gift_list[common_pb2.JOB_ARCHER] = OrderedDict()
  level_up_gift_list[common_pb2.JOB_SHAMAN] = OrderedDict()

  for r in results:
    level = int(r[0])
    job = int(r[1])
    e_id = int(r[2])
    p_id = r[3].split(',')

    level_up_gift = level_up_gift_list[job]
    level_up_gift[level] = {
      'e_id': e_id,
      'p_id': p_id,
    }
  
  return level_up_gift_list

#----------------------------------------------------------------#

def recommend_gifts():
  results = sqlrelay.execute_results("""
SELECT
   COUNT
 , E_ID
 , P_ID 
FROM 
   ARPG_BT_EVENT 
WHERE
   TYPE = %d AND USE = 1
""" % (common_pb2.EVENT_RECOMMEND))

  recommend_gift_list = defaultdict()

  for r in results:
    count = int(r[0])
    e_id = int(r[1])
    p_id = r[2].split(',')

    recommend_gift_list[count] = {
      'e_id': e_id,
      'p_id': p_id,
    }
  
  return recommend_gift_list

#----------------------------------------------------------------#

def login_events():
  results = sqlrelay.execute_results("""
SELECT
   E_ID
 , TO_CHAR(START_DATE, 'YYYY/MM/DD HH24:MI:SS')
 , TO_CHAR(END_DATE, 'YYYY/MM/DD HH24:MI:SS')
 , REPEAT
 , DURATION
 , P_ID 
FROM
   ARPG_BT_EVENT
WHERE
   TYPE = %d AND USE = 1 AND SYSTIMESTAMP <= END_DATE
""" % (common_pb2.EVENT_LOGIN))

  login_event_list = defaultdict()
  for r in results:
    e_id = int(r[0])
    start_date = datetime.strptime(r[1], "%Y/%m/%d %H:%M:%S")
    end_date = datetime.strptime(r[2], "%Y/%m/%d %H:%M:%S")
    repeat = int(r[3])
    duration = int(r[4])
    p_id = r[5].split(',')

    login_event_list[e_id] = {
      'start_date': start_date,
      'end_date': end_date,
      'repeat': repeat,
      'duration': duration,
      'p_id': p_id,
    }

  return login_event_list

#----------------------------------------------------------------#

def periodic_events():
  results = sqlrelay.execute_results("""
SELECT
   E_ID
 , TO_CHAR(START_DATE, 'YYYY/MM/DD HH24:MI:SS')
 , TO_CHAR(END_DATE, 'YYYY/MM/DD HH24:MI:SS')
 , REPEAT
 , P_ID 
FROM
   ARPG_BT_EVENT
WHERE
   TYPE = %d AND USE = 1 AND SYSTIMESTAMP <= END_DATE
""" % (common_pb2.EVENT_PERIOD))

  periodic_event_list = defaultdict()
  for r in results:
    e_id = int(r[0])
    start_date = datetime.strptime(r[1], "%Y/%m/%d %H:%M:%S")
    end_date = datetime.strptime(r[2], "%Y/%m/%d %H:%M:%S")
    repeat = int(r[3])
    p_id = r[4].split(',')

    periodic_event_list[e_id] = {
      'start_date': start_date,
      'end_date': end_date,
      'repeat': repeat,
      'p_id': p_id,
    }

  return periodic_event_list

#----------------------------------------------------------------#

def eshop_events():
  results = sqlrelay.execute_results("""
SELECT
   E_ID
 , TO_CHAR(START_DATE, 'YYYY/MM/DD HH24:MI:SS')
 , TO_CHAR(END_DATE, 'YYYY/MM/DD HH24:MI:SS')
 , PURCHASE
FROM
   ARPG_BT_EVENT
WHERE
   TYPE = %d AND USE = 1 AND PURCHASE > 0 AND SYSTIMESTAMP <= END_DATE
""" % (common_pb2.EVENT_ESHOP))

  eshop_event_list = defaultdict()
  for r in results:
    e_id = int(r[0])
    start_date = datetime.strptime(r[1], "%Y/%m/%d %H:%M:%S")
    end_date = datetime.strptime(r[2], "%Y/%m/%d %H:%M:%S")
    purchase = int(r[3])

    eshop_event_list[e_id] = {
      'start_date': start_date,
      'end_date': end_date,
      'purchase': purchase,
    }

  return eshop_event_list

#----------------------------------------------------------------#

def costume_events():
  results = sqlrelay.execute_results("""
SELECT
   E_ID
 , TO_CHAR(START_DATE, 'YYYY/MM/DD HH24:MI:SS')
 , TO_CHAR(END_DATE, 'YYYY/MM/DD HH24:MI:SS')
 , JOB
 , P_ID 
FROM 
   ARPG_BT_EVENT 
WHERE
   TYPE = %d AND USE = 1 AND SYSTIMESTAMP <= END_DATE
""" % (common_pb2.EVENT_COSTUME))

  costume_event_list = defaultdict()
  costume_event_list[common_pb2.JOB_SWORD] = OrderedDict()
  costume_event_list[common_pb2.JOB_ARCHER] = OrderedDict()
  costume_event_list[common_pb2.JOB_SHAMAN] = OrderedDict()

  for r in results:
    e_id = int(r[0])
    start_date = datetime.strptime(r[1], "%Y/%m/%d %H:%M:%S")
    end_date = datetime.strptime(r[2], "%Y/%m/%d %H:%M:%S")
    job = int(r[3])
    p_id = r[4].split(',')

    costume_event = costume_event_list[job]
    costume_event[e_id] = {
      'start_date': start_date,
      'end_date': end_date,
      'p_id': p_id,
    }
  
  return costume_event_list

#----------------------------------------------------------------#

def dailystamps():
  results = sqlrelay.execute_results("""
SELECT
   YEAR_MONTH
 , DAYS
 , E_ID
 , P_ID 
FROM 
   ARPG_BT_EVENT 
WHERE
   TYPE = %d AND USE = 1
""" % (common_pb2.EVENT_DAILYSTAMP))

  dailystamp_list = defaultdict()
  for r in results:
    year_month = int(r[0])
    days = int(r[1])
    e_id = int(r[2])
    p_id = [int(n) for n in r[3].split(',')]

    if dailystamp_list.has_key(year_month):
      dailystamp = dailystamp_list[year_month]
    else:
      dailystamp = OrderedDict()
      dailystamp_list[year_month] = dailystamp

    dailystamp[days] = {
      'e_id': e_id,
      'p_id': p_id,
    }

  return dailystamp_list

#----------------------------------------------------------------#

def achivements():
  results = sqlrelay.execute_results("""
SELECT
   A_ID
 , FINISH_LV
 , REPEAT
 , REWARD
 , REWARD_AMOUNT 
FROM
   ARPG_BT_ACHIVEMENT
""")

  achivement_list = OrderedDict()
  for r in results:
    a_id = int(r[0])
    finish_lv = int(r[1])
    repeat = int(r[2])
    reward = int(r[3])
    reward_amount = r[4]

    achivement_list[a_id] = {
      'finish_lv': finish_lv,
      'repeat': repeat,
      'reward': reward,
      'reward_amount': reward_amount,
    }

  return achivement_list

#----------------------------------------------------------------#

def daily_achivements():
  results = sqlrelay.execute_results("""
SELECT
   A_ID
 , REQUIRED_LV
 , REPEAT
 , REWARD
 , REWARD_AMOUNT 
FROM
   ARPG_BT_DAILY_ACHIVEMENT
""")

  daily_achivement_list = OrderedDict()
  for r in results:
    a_id = int(r[0])
    required_lv = int(r[1])
    repeat = int(r[2])
    reward = int(r[3])
    reward_amount = r[4]

    daily_achivement_list[a_id] = {
      'required_lv': required_lv,
      'repeat': repeat,
      'reward': reward,
      'reward_amount': reward_amount,
    }

  return daily_achivement_list

#----------------------------------------------------------------#

def material_prices():
  results = sqlrelay.execute_results("""
SELECT
   MATERIAL_ID
 , PRICE
 , AMOUNT
FROM
   ARPG_BT_MATERIAL_PRICE
""")

  material_price_list = OrderedDict()
  for r in results:
    material_id = int(r[0])
    price = int(r[1])
    amount = r[2]

    material_price_list[material_id] = {
      'price': price,
      'amount': amount,
    }

  return material_price_list

#----------------------------------------------------------------#

def survival_buffs():
  results = sqlrelay.execute_results("""
SELECT 
   BUFF_ID
 , UNLOCK_WAVE
 , NAME
 , PRICE
 , BOOST
 , START_WAVE 
FROM
  ARPG_BT_SURVIVAL_BUFF
""")

  survival_buff_list = OrderedDict()
  for r in results:
    buff_id = int(r[0])
    unlock_wave = int(r[1])
    name = from_utf8(r[2])
    price = int(r[3])
    boost = r[4]
    start_wave = int(r[5])

    survival_buff_list[buff_id] = {
      'unlock_wave': unlock_wave,
      'name': name,
      'price': price,
      'boost': boost,
      'start_wave': start_wave
    }

  return survival_buff_list

#----------------------------------------------------------------#
