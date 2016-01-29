# -*- coding:utf-8 -*-

from twisted.internet import protocol, threads, defer
from protocol import ProtobufProtocol, gateway_pb2, common_pb2, dump
from logger import logger
from user import User
from hero import Hero

import random


global instances


class Gateway(ProtobufProtocol):

  _checksum = 0
  _version_checked = False
  _user = None


  def __init__(self):
    ProtobufProtocol.__init__(self)

    self.messages = {
      gateway_pb2.VERSION: self.handle_version,
      gateway_pb2.LOGIN: self.handle_login,
      gateway_pb2.LOGOUT: self.handle_logout,

      gateway_pb2.INFO: self.handle_info,
      gateway_pb2.PROPERTIES: self.handle_properties,
      gateway_pb2.BADGES: self.handle_badges,
      gateway_pb2.NICKNAME: self.handle_nickname,
      gateway_pb2.MAKE_HERO: self.handle_make_hero,
      gateway_pb2.SELECT_HERO: self.handle_select_hero,
      gateway_pb2.HEROES: self.handle_heroes,

      gateway_pb2.START_GAME: self.handle_start_game,
      gateway_pb2.FINISH_GAME: self.handle_finish_game,
      gateway_pb2.SECOND_TREASURE: self.handle_second_treasure,
      gateway_pb2.FINISH_MULTI_GAME: self.handle_finish_multi_game,
      gateway_pb2.BATTLE_SKIP: self.handle_battle_skip,
      gateway_pb2.START_SURVIVAL_GAME: self.handle_start_survival_game,
      gateway_pb2.FINISH_SURVIVAL_GAME: self.handle_finish_survival_game,

      gateway_pb2.WAVE: self.handle_wave,
      gateway_pb2.LEVEL_UP: self.handle_level_up,
      gateway_pb2.RESURRECTION: self.handle_resurrection,

      gateway_pb2.MAKE_PUBLIC_ROOM: self.handle_make_public_room,
      gateway_pb2.MAKE_PRIVATE_ROOM: self.handle_make_private_room,
      gateway_pb2.CHANGE_PUBLIC_ROOM: self.handle_change_public_room,

      gateway_pb2.DROP_OUT: self.handle_drop_out,
      gateway_pb2.CONFIRM_TO_DROP_OUT: self.handle_confirm_to_drop_out,

      gateway_pb2.DUNGEONS: self.handle_dungeons,
      gateway_pb2.EPIC_DUNGEONS: self.handle_epic_dungeons,
      gateway_pb2.STAGES: self.handle_stages,
      gateway_pb2.UNLOCK_STAGE: self.handle_unlock_stage,
      gateway_pb2.RESET_STAGE: self.handle_reset_stage,
      gateway_pb2.QUERY_STAGE: self.handle_query_stage,

      gateway_pb2.GIFTS: self.handle_gifts,
      gateway_pb2.TAKE_GIFT: self.handle_take_gift,
      gateway_pb2.TUTORIAL: self.handle_tutorial,

      gateway_pb2.ESHOP: self.handle_eshop,
      gateway_pb2.BUY_IN_ESHOP: self.handle_buy_in_eshop,
      gateway_pb2.CASH_SHOP: self.handle_cash_shop,
      gateway_pb2.BUY_IN_CASH_SHOP: self.handle_buy_in_cash_shop,
      gateway_pb2.ONI_SHOP: self.handle_oni_shop,
      gateway_pb2.BUY_IN_ONI_SHOP: self.handle_buy_in_oni_shop,

      gateway_pb2.COSTUMES: self.handle_costumes,
      gateway_pb2.SELECT_COSTUME: self.handle_select_costume,
      gateway_pb2.COSTUMES_TO_MAKE: self.handle_costumes_to_make,
      gateway_pb2.BUY_COSTUME: self.handle_buy_costume,
      gateway_pb2.MAKE_COSTUME: self.handle_make_costume,
      gateway_pb2.COSTUMES_TO_REINFORCE: self.handle_costumes_to_reinforce,
      gateway_pb2.REINFORCE_COSTUME: self.handle_reinforce_costume,

      gateway_pb2.INVENTORY: self.handle_inventory,
      gateway_pb2.DROP_ITEM: self.handle_drop_item,
      gateway_pb2.PUT_ON: self.handle_put_on,
      gateway_pb2.TAKE_OFF: self.handle_take_off,
      gateway_pb2.FIX_ITEM: self.handle_fix_item,
      gateway_pb2.REINFORCE_ITEM: self.handle_reinforce_item,
      gateway_pb2.EXPAND_INVENTORY: self.handle_expand_inventory,
      gateway_pb2.MAKE_ITEM: self.handle_make_item,

      gateway_pb2.LOTTERYS: self.handle_lotterys,
      gateway_pb2.TAKE_LOTTERY: self.handle_take_lottery,

      gateway_pb2.SKILLS: self.handle_skills,
      gateway_pb2.EXPAND_SKILL_BUTTON: self.handle_expand_skill_button,
      gateway_pb2.SKILL_BUTTON: self.handle_skill_button,
      gateway_pb2.REINFORCE_SKILL: self.handle_reinforce_skill,
      gateway_pb2.SKILL_AUTO_ASSIGN: self.handle_skill_auto_assign,
      gateway_pb2.RESET_SKILL: self.handle_reset_skill,

      gateway_pb2.HEART: self.handle_heart,
      gateway_pb2.BUDDIES: self.handle_buddies,
      gateway_pb2.EXFRIEND: self.handle_exfriend,
      gateway_pb2.SEND_HEART: self.handle_send_heart,
      gateway_pb2.RECEIVE_HEART: self.handle_receive_heart,
      gateway_pb2.RECEIVE_HEART_ALL: self.handle_receive_heart_all,
      gateway_pb2.ASK_FRIENDSHIPS: self.handle_ask_friendships,
      gateway_pb2.PROPOSE_BUDDY: self.handle_propose_buddy,
      gateway_pb2.ACCEPT_FRIENDSHIP: self.handle_accept_friendship,
      gateway_pb2.REJECT_FRIENDSHIP: self.handle_reject_friendship,
      gateway_pb2.FIND_BUDDY: self.handle_find_buddy,
      gateway_pb2.SEARCHABLE: self.handle_searchable,
      gateway_pb2.RECOMMEND_FRIENDSHIPS: self.handle_recommend_friendships,
      gateway_pb2.FRIEND_PROFILE: self.handle_friend_profile,

      gateway_pb2.KAKAO_INVITATION: self.handle_kakao_invitation,
      gateway_pb2.INVITED_KAKAO_FRIENDS: self.handle_invited_kakao_friends,
      gateway_pb2.KAKAO_FRIENDS: self.handle_kakao_friends,
      gateway_pb2.LINK_KAKAO_FRIENDS: self.handle_link_kakao_friends,
      gateway_pb2.UNLINK_KAKAO_FRIENDS: self.handle_unlink_kakao_friends,
  
      gateway_pb2.BUDDIES_TO_INVITE_GAME: self.handle_buddies_to_invite_game,
      gateway_pb2.INVITE_BUDDY_TO_PLAY_GAME: self.handle_invite_buddy_to_play_game,
      gateway_pb2.BE_INVITED_TO_PLAY_GAME: self.handle_be_invited_to_play_game,
      gateway_pb2.ACCEPT_GAME_INVITATION: self.handle_accept_game_invitation,
      gateway_pb2.DECLINE_GAME_INVITATION: self.handle_decline_game_invitation,
      gateway_pb2.CANCEL_GAME_INVITATION: self.handle_cancel_game_invitation,

      gateway_pb2.RANKING: self.handle_ranking,
      gateway_pb2.RANKER: self.handle_ranker,

      gateway_pb2.DAILYSTAMP: self.handle_dailystamp,

      gateway_pb2.ASK_EXCHANGE_HEART: self.handle_ask_exchange_heart,
      gateway_pb2.EXCHANGE_HEART: self.handle_exchange_heart,

      gateway_pb2.ACHIVEMENT: self.handle_achivement,
      gateway_pb2.ACHIVEMENT_REWARD: self.handle_achivement_reward,

      gateway_pb2.MATERIAL_COOLTIME: self.handle_material_cooltime,
      gateway_pb2.COLLECT_MATERIAL: self.handle_collect_material,
      gateway_pb2.RESET_MATERIAL_COOLTIME: self.handle_reset_material_cooltime,

      gateway_pb2.QUERY_PROMOTION: self.handle_query_promotion,
      gateway_pb2.PROMOTER: self.handle_promoter,
      gateway_pb2.PROMOTION_COUNT: self.handle_promotion_count,

      gateway_pb2.COUPON: self.handle_coupon,
      gateway_pb2.KEYWORD_COUPON: self.handle_keyword_coupon,
      gateway_pb2.COUPON_HISTORY: self.handle_coupon_history,

      gateway_pb2.KAKAO_OPTIONS: self.handle_kakao_options,
      gateway_pb2.QUERY_KAKAO_OPTIONS: self.handle_query_kakao_options,

      gateway_pb2.REVIEW: self.handle_review,

      gateway_pb2.MENU_ACCESS: self.handle_menu_access,
      gateway_pb2.NOTIFY_MESSAGE: self.handle_notify_message,
      gateway_pb2.BADGES: self.handle_badges,

      gateway_pb2.REFILL_SURVIVAL_CHALLENGE: self.handle_refill_survival_challenge,
      gateway_pb2.SURVIVAL_BUFF: self.handle_survival_buff,

      gateway_pb2.REVIVAL: self.handle_revival,

      gateway_pb2.TEST_PARAM: self.handle_test_param,
    }

    param_type = gateway_pb2.Request().test_param
    self.test_param_messages = {
      param_type.SET_CASH: self.handle_set_cash,
      param_type.SET_HONBUL: self.handle_set_honbul,
      param_type.SET_SKILL_POINT: self.handle_set_skill_point,
      param_type.SET_LEVEL: self.handle_set_level,
      param_type.SET_TALISMAN: self.handle_set_talisman,
      param_type.SET_STONE: self.handle_set_stone,
      param_type.SET_COIN: self.handle_set_coin,
      param_type.SET_HEART: self.handle_set_heart,
      param_type.ADD_ITEM: self.handle_add_item,
      param_type.GET_USER_ID: self.handle_get_user_id,
      param_type.SET_EXP: self.handle_set_exp,
      param_type.SET_PLAYING_TIME: self.handle_set_playing_time,
      param_type.SET_UNLOCK_STAGE_COUNT: self.handle_set_unlock_stage_count,
    }


  def connectionMade(self):
    logger.debug("connectionMade")

  def connectionLost(self, reason):
    logger.debug("connectionLost")
    if self._user:
      del self._user
      self._user = None

  def _send(self, msg):
    self._checksum = random.randint(1, 999999)
    msg.checksum = self._checksum
    # dump
    dump.dump_response(msg)
    # 데이터 전송
    ProtobufProtocol.send(self, msg)

  def send(self, msg):
    def _success(result):
      logger.debug("Send async success")

    def _failure(result):
      logger.error("Send async failed")

    d = self.make_defer(_success, _failure)
    d.callback(self._send(msg))


  def process(self, message):
    request = gateway_pb2.Request()
    request.ParseFromString(message)
    self._checksum = request.checksum

    # dump
    dump.dump_request(request)

    # handle request
    handler = self.messages.get(request.type, None)
    if not handler:
      logger.error("unknown message")
    else:
      if request.type > gateway_pb2.VERSION and self._version_checked is False:
        return self.error(self.make_response(request), gateway_pb2.EC_VERSION, 'Need version check')
      handler(request)

  def validate_request(self, request):
    pass

  def error(self, response, code, reason):
    response.error.code = code
    response.error.reason = reason
    self.send(response)

  def make_response(self, request):
    response = gateway_pb2.Response()
    response.type = request.type
    response.sequence = request.sequence
    return response

  def make_defer(self, success_callback, failure_callback):
    d = defer.Deferred()
    d.addCallback(success_callback)
    d.addErrback(failure_callback)
    return d


#----------------------------------------------------------------#

  def handle_version(self, request):
    response = self.make_response(request)

    if not request.version:
      return self.error(response, gateway_pb2.EC_VERSION, 'Invalid version request')

    version = gateway_pb2.Request.Version()
    if request.version.protocol != version.protocol:
      return self.error(response, gateway_pb2.EC_VERSION, 'Protocol number is not match')

    if request.version.service != '0.1-test':
      return self.error(response, gateway_pb2.EC_VERSION, 'Service is not match')

    self._version_checked = True
    self.send(response)


  def handle_login(self, request):
    response = self.make_response(request)

    if not request.login:
      return self.error(response, gateway_pb2.EC_UNABLE_TO_OPERATE, 'Invalid login request')

    game_id = request.login.game_id
    hashed_kakao_id = ''
    kakao_id = -1

    if request.login.kakao_id:
      kakao_id = request.login.kakao_id
      if request.login.hashed_kakao_id:
        hashed_kakao_id = request.login.hashed_kakao_id

    def _success(user):
      logger.info('%d user login' % user.user_id())
      self._user = user

      response.login.plug_ip = ''
      response.login.plug_port = 5001
      response.login.passwd = ''
      self.send(response)

    def _failure(ex):
      code, reason = ex.value
      return self.error(response, code, reason)

    d = self.make_defer(_success, _failure)
    d.callback(User.get_user_id(game_id, hashed_kakao_id, kakao_id))


  def handle_logout(self, request):
    if self.transport:
      self.transport.loseConnection()


  def handle_info(self, request):
    assert(self._user)
    response = self.make_response(request)

    def _success(ignore):
      self.send(response)

    def _failure(ex):
      code, reason = ex.value
      return self.error(response, code, reason)

    d = self.make_defer(_success, _failure)
    d.callback(self._user.fill_info(response.info))


  def handle_properties(self, request):
    assert(self._user)
    response = self.make_response(request)

    def _success(ignore):
      self.send(response)

    def _failure(ex):
      code, reason = ex.value
      return self.error(response, code, reason)

    d = self.make_defer(_success, _failure)
    d.callback(self._user.fill_properties(response.properties))


  def handle_badges(self, request):
    assert(self._user)
    response = self.make_response(request)

    def _success(ignore):
      self.send(response)

    def _failure(ex):
      code, reason = ex.value
      return self.error(response, code, reason)
   
    d = self.make_defer(_success, _failure) 
    d.callback(self._user.fill_badges(response.badges))


  def handle_nickname(self, request):
    assert(self._user)
    response = self.make_response(request)

    if not request.nickname:
      return self.error(response, gateway_pb2.EC_UNABLE_TO_OPERATE, 'Invalid request')

    if self._user.has_nickname():
      return self.error(response, gateway_pb2.EC_UNABLE_TO_OPERATE, 'Already has nickname')

    def _success(ignore):
      self.send(response)

    def _failure(ex):
      code, reason = ex.value
      return self.error(response, code, reason)

    d = self.make_defer(_success, _failure)
    d.callback(self._user.change_nickname(request.nickname))


  def handle_make_hero(self, request):
    assert(self._user)
    response = self.make_response(request)

    if not request.make_hero:
      return self.error(response, gateway_pb2.EC_UNABLE_TO_OPERATE, 'Invalid request')

    job = request.make_hero.job
    if self._user.has_hero(job):
      return self.error(response, gateway_pb2.EC_UNABLE_TO_OPERATE, 'Already opened hero')

    def _success(hero):
      hero.fill_hero(response.make_hero)
      self.send(response)

    def _failure(ex):
      code, value = ex.value
      return self.error(response, code, value)

    d = self.make_defer(_success, _failure)
    d.callback(self._user.make_hero(job))


  def handle_select_hero(self, request):
    assert(self._user)
    response = self.make_response(request)

    if not request.select_hero:
      return self.error(response, gateway_pb2.EC_UNABLE_TO_OPERATE, 'Invalid request')

    job = request.select_hero.job
    if not self._user.has_hero(job):
      return self.error(response, gateway_pb2.EC_UNABLE_TO_OPERATE, 'Dont have hero by job')
   
    def _success(hero):
      hero.fill_hero(response.select_hero)
      self.send(response)

    def _failure(ex):
      code, value = ex.value
      return self.error(response, code, value)
    
    d = self.make_defer(_success, _failure)
    d.callback(self._user.select_hero(job))


  def handle_heroes(self, request):
    assert(self._user)
    response = self.make_response(request)

    def _success(ignore):
      self.send(response)

    def _failure(ex):
      code, value = ex.value
      return self.error(response, code, value)

    d = self.make_defer(_success, _failure)
    d.callback(self._user.fill_heroes(response))

  
  def handle_start_game(self, request):
    assert(self._user)


  def handle_finish_game(self, request):
    assert(self._user)


  def handle_second_treasure(self, request):
    assert(self._user)


  def handle_finish_multi_game(self, request):
    assert(self._user)


  def handle_battle_skip(self, request):
    assert(self._user)


  def handle_start_survival_game(self, request):
    assert(self._user)


  def handle_finish_survival_game(self, request):
    assert(self._user)


  def handle_wave(self, request):
    assert(self._user)


  def handle_level_up(self, request):
    assert(self._user)


  def handle_resurrection(self, request):
    assert(self._user)


  def handle_make_public_room(self, request):
    assert(self._user)


  def handle_make_private_room(self, request):
    assert(self._user)


  def handle_change_public_room(self, request):
    assert(self._user)


  def handle_drop_out(self, request):
    assert(self._user)


  def handle_confirm_to_drop_out(self, request):
    assert(self._user)


  def handle_dungeons(self, request):
    assert(self._user)
    response = self.make_response(request)

    def _success(ignore):
      self.send(response)

    def _failure(ex):
      code, reason = ex.value
      return self.error(response, code, reason)

    d = self.make_defer(_success, _failure)
    d.callback(self._user.fill_dungeons(response.dungeons))


  def handle_epic_dungeons(self, request):
    assert(self._user)
    response = self.make_response(request)

    def _success(ignore):
      self.send(response)

    def _failure(ex):
      code, reason = ex.value
      return self.error(response, code, reason)

    d = self.make_defer(_success, _failure)
    d.callback(self._user.fill_epic_dungeons(response.epic_dungeons))


  def handle_stages(self, request):
    assert(self._user)


  def handle_unlock_stage(self, request):
    assert(self._user)


  def handle_reset_stage(self, request):
    assert(self._user)


  def handle_query_stage(self, request):
    assert(self._user)


  def handle_gifts(self, request):
    assert(self._user)


  def handle_take_gift(self, request):
    assert(self._user)


  def handle_tutorial(self, request):
    assert(self._user)


  def handle_eshop(self, request):
    assert(self._user)


  def handle_buy_in_eshop(self, request):
    assert(self._user)


  def handle_cash_shop(self, request):
    assert(self._user)


  def handle_buy_in_cash_shop(self, request):
    assert(self._user)


  def handle_oni_shop(self, request):
    assert(self._user)
    response = self.make_response(request)

    selected_hero = self._user.selected_hero()
    if not selected_hero:
      return self.error(response, gateway_pb2.EC_NO_HERO, 'No hero')

    def _success(result):
      self.send(response)

    def _failure(result):
      return self.error(response, gateway_pb2.EC_DATABASE, 'Database execute failed')

    method = request.oni_shop.method
    category = request.oni_shop.category

    d = self.make_defer(_success, _failure)

    if method == common_pb2.ONI_SHOP_METHOD_RESET_SKILL:
      # 스킬초기화 구매정보
      d.callback(self._user.fill_reset_skill(response.oni_shop.reset_skill))
    else:
      # 혼불/캐쉬 구매정보
      d.callback(self._user.fill_oni_shop(method, category, response.oni_shop))


  def handle_buy_in_oni_shop(self, request):
    assert(self._user)


  def handle_costumes(self, request):
    assert(self._user)


  def handle_select_costume(self, request):
    assert(self._user)


  def handle_costumes_to_make(self, request):
    assert(self._user)


  def handle_buy_costume(self, request):
    assert(self._user)


  def handle_make_costume(self, request):
    assert(self._user)


  def handle_costumes_to_reinforce(self, request):
    assert(self._user)


  def handle_reinforce_costume(self, request):
    assert(self._user)


  def handle_inventory(self, request):
    assert(self._user)


  def handle_drop_item(self, request):
    assert(self._user)


  def handle_put_on(self, request):
    assert(self._user)


  def handle_take_off(self, request):
    assert(self._user)


  def handle_fix_item(self, request):
    assert(self._user)


  def handle_reinforce_item(self, request):
    assert(self._user)


  def handle_expand_inventory(self, request):
    assert(self._user)


  def handle_make_item(self, request):
    assert(self._user)


  def handle_lotterys(self, request):
    assert(self._user)


  def handle_take_lottery(self, request):
    assert(self._user)


  def handle_skills(self, request):
    assert(self._user)


  def handle_expand_skill_button(self, request):
    assert(self._user)


  def handle_skill_button(self, request):
    assert(self._user)


  def handle_reinforce_skill(self, request):
    assert(self._user)


  def handle_skill_auto_assign(self, request):
    assert(self._user)


  def handle_reset_skill(self, request):
    assert(self._user)


  def handle_heart(self, request):
    assert(self._user)


  def handle_send_heart(self, request):
    assert(self._user)


  def handle_receive_heart(self, request):
    assert(self._user)


  def handle_receive_heart_all(self, request):
    assert(self._user)


  def handle_buddies(self, request):
    assert(self._user)


  def handle_exfriend(self, request):
    assert(self._user)


  def handle_ask_friendships(self, request):
    assert(self._user)


  def handle_propose_buddy(self, request):
    assert(self._user)


  def handle_accept_friendship(self, request):
    assert(self._user)


  def handle_reject_friendship(self, request):
    assert(self._user)


  def handle_find_buddy(self, request):
    assert(self._user)


  def handle_searchable(self, request):
    assert(self._user)


  def handle_recommend_friendships(self, request):
    assert(self._user)

 
  def handle_friend_profile(self, request):
    assert(self._user)


  def handle_kakao_invitation(self, request):
    assert(self._user)


  def handle_invited_kakao_friends(self, request):
    assert(self._user)


  def handle_kakao_friends(self, request):
    assert(self._user)


  def handle_link_kakao_friends(self, request):
    assert(self._user)


  def handle_unlink_kakao_friends(self, request):
    assert(self._user)


  def handle_buddies_to_invite_game(self, request):
    assert(self._user)


  def handle_invite_buddy_to_play_game(self, request):
    assert(self._user)


  def handle_be_invited_to_play_game(self, request):
    assert(self._user)


  def handle_accept_game_invitation(self, request):
    assert(self._user)


  def handle_decline_game_invitation(self, request):
    assert(self._user)


  def handle_cancel_game_invitation(self, request):
    assert(self._user)


  def handle_ranking(self, request):
    assert(self._user)


  def handle_ranker(self, request):
    assert(self._user)


  def handle_dailystamp(self, request):
    assert(self._user)


  def handle_ask_exchange_heart(self, request):
    assert(self._user)


  def handle_exchange_heart(self, request):
    assert(self._user)


  def handle_achivement(self, request):
    assert(self._user)


  def handle_achivement_reward(self, request):
    assert(self._user)


  def handle_collect_material(self, request):
    assert(self._user)
    response = self.make_response(request)

    def _success(ignore):
      self.send(response)

    def _failure(ex):
      code, reason = ex.value
      return self.error(response, code, reason)

    material_id = request.collect_material.material_id
  
    d = self.make_defer(_success, _failure)
    d.callback(self._user.collect_material(material_id, response.collect_material))


  def handle_material_cooltime(self, request):
    assert(self._user)
    response = self.make_response(request)

    def _success(ignore):
      self.send(response)

    def _failure(ex):
      code, reason = ex.value
      return self.error(response, code, reason)

    d = self.make_defer(_success, _failure)
    d.callback(self._user.material_cooltime(response.material_cooltime))


  def handle_reset_material_cooltime(self, request):
    assert(self._user)


  def handle_query_promotion(self, request):
    assert(self._user)

 
  def handle_promoter(self, request):
    assert(self._user)


  def handle_promotion_count(self, request):
    assert(self._user)


  def handle_coupon(self, request):
    assert(self._user)


  def handle_keyword_coupon(self, request):
    assert(self._user)


  def handle_coupon_history(self, request):
    assert(self._user)


  def handle_kakao_options(self, request):
    assert(self._user)


  def handle_query_kakao_options(self, request):
    assert(self._user)


  def handle_review(self, request):
    assert(self._user)


  def handle_menu_access(self, request):
    assert(self._user)


  def handle_notify_message(self, request):
    assert(self._user)


  def handle_refill_survival_challenge(self, request):
    assert(self._user)


  def handle_survival_buff(self, request):
    assert(self._user)
    response = self.make_response(request)

    def _success(result):
      self.send(response)

    def _failure(result):
      return self.error(response, gateway_pb2.EC_DATABASE, 'Database execute failed')

    d = self.make_defer(_success, _failure)
    d.callback(self._user.fill_survival_buff(response.survival_buff))


  def handle_revival(self, request):
    assert(self._user)
    response = self.make_response(request)

    def _success(result):
      self.send(response)

    def _failure(result):
      return self.error(response, gateway_pb2.EC_DATABASE, 'Database execute failed')

    d = self.make_defer(_success, _failure)


#----------------------------------------------------------------#

  def handle_test_param(self, request):
    assert(self._user)
    response = self.make_response(request)

    for param in request.test_param.params:
      handler = self.test_param_messages.get(param.type, None)
      if not handler:
        logger.error("unknown message")
      else:
        handler(param, response)
    self.send(response)

  def handle_set_cash(self, param, response):
    assert(self._user)
    self._user.set_cash(param.int_data)
 
  def handle_set_honbul(self, param, response):
    assert(self._user)
    self._user.set_honbul(param.int_data)

  def handle_set_skill_point(self, param, response):
    assert(self._user)
    selected_hero = self._user.selected_hero()
    selected_hero.set_skill_point(param.int_data)

  def handle_set_level(self, param, response):
    assert(self._user)
    selected_hero = self._user.selected_hero()
    selected_hero.set_level(param.int_data)

  def handle_set_talisman(self, param, response):
    assert(self._user)
    self._user.set_talisman(param.int_data)

  def handle_set_stone(self, param, response):
    assert(self._user)
    self._user.set_stone(param.int_data)

  def handle_set_coin(self, param, response):
    assert(self._user)
    self._user.set_coin(param.int_data)

  def handle_set_heart(self, param, response):
    assert(self._user)
    self._user.set_heart(param.int_data)

  def handle_add_item(self, param, response):
    assert(self._user)
    item_id = self._user.add_item(param.int_data)
    response.sequence = item_id

  def handle_get_user_id(self, param, response):
    assert(self._user)
    response.sequence = self._user.user_id()

  def handle_set_exp(self, param, response):
    assert(self._user)
    selected_hero = self._user.selected_hero()
    selected_hero.set_exp(param.int_data)

  def handle_set_playing_time(self, param, response):
    assert(self._user)
    selected_hero = self._user.selected_hero()
    selected_hero.set_playing_time(param.int_data)

  def handle_set_unlock_stage_count(self, param, response):
    assert(self._user)
    selected_hero = self._user.selected_hero()
    selected_hero.set_unlock_stage_count(0)
    

#----------------------------------------------------------------#

class GatewayFactory(protocol.Factory):
  def buildProtocol(self, addr):
    logger.debug("New client is connected : %s" % addr)
    return Gateway()

#----------------------------------------------------------------#
