# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stage.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import common_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='stage.proto',
  package='m3.stage',
  serialized_pb='\n\x0bstage.proto\x12\x08m3.stage\x1a\x0c\x63ommon.proto\"\x83\t\n\x0bStageToRoom\x12/\n\x04type\x18\x01 \x02(\x0e\x32!.m3.stage.StageToRoom.MessageType\x12*\n\x05ready\x18\x03 \x01(\x0b\x32\x1b.m3.stage.StageToRoom.Ready\x12*\n\x05leave\x18\x04 \x01(\x0b\x32\x1b.m3.stage.StageToRoom.Leave\x12?\n\x10player_connected\x18\x05 \x01(\x0b\x32%.m3.stage.StageToRoom.PlayerConnected\x12,\n\x06\x66inish\x18\x06 \x01(\x0b\x32\x1c.m3.stage.StageToRoom.Finish\x12/\n\x08level_up\x18\x07 \x01(\x0b\x32\x1d.m3.stage.StageToRoom.LevelUp\x12\x38\n\x0cresurrection\x18\x08 \x01(\x0b\x32\".m3.stage.StageToRoom.Resurrection\x12\x35\n\x0b\x63lear_cache\x18\x1e \x01(\x0b\x32 .m3.stage.StageToRoom.ClearCache\x1a\x33\n\x05Ready\x12\n\n\x02ip\x18\x01 \x02(\t\x12\x0c\n\x04port\x18\x02 \x02(\x05\x12\x10\n\x08group_id\x18\x03 \x02(\x05\x1a\xc8\x01\n\x06\x46inish\x12\x34\n\x07players\x18\x01 \x03(\x0b\x32#.m3.stage.StageToRoom.Finish.Player\x1a\x87\x01\n\x06Player\x12,\n\x05\x63lear\x18\x01 \x01(\x0b\x32\x1d.m3.common.FinishGame.Cleared\x12*\n\x04\x66\x61il\x18\x02 \x01(\x0b\x32\x1c.m3.common.FinishGame.Failed\x12\x11\n\tplayer_id\x18\x03 \x02(\x03\x12\x10\n\x08nickname\x18\x04 \x02(\t\x1a_\n\x05Leave\x12\x11\n\tplayer_id\x18\x01 \x02(\x03\x12\x11\n\tplay_time\x18\x02 \x02(\x05\x12\x0b\n\x03\x65xp\x18\x03 \x02(\x05\x12\x13\n\x0btotal_score\x18\x04 \x02(\x05\x12\x0e\n\x06honbul\x18\x05 \x02(\x03\x1a$\n\x0fPlayerConnected\x12\x11\n\tplayer_id\x18\x01 \x02(\x03\x1aZ\n\x07LevelUp\x12\x11\n\tplayer_id\x18\x01 \x02(\x03\x12\x13\n\x0binitial_exp\x18\x02 \x02(\x03\x12\x15\n\rinitial_level\x18\x03 \x02(\x05\x12\x10\n\x08\x63urr_exp\x18\x04 \x02(\x03\x1a!\n\x0cResurrection\x12\x11\n\tplayer_id\x18\x01 \x02(\x03\x1a@\n\nClearCache\x12\"\n\x04type\x18\x01 \x02(\x0e\x32\x14.m3.common.CacheType\x12\x0e\n\x06\x61\x63tion\x18\x02 \x02(\x05\"\x91\x01\n\x0bMessageType\x12\t\n\x05READY\x10\x64\x12\t\n\x05START\x10\x66\x12\n\n\x06\x46INISH\x10g\x12\t\n\x05LEAVE\x10h\x12\x14\n\x10PLAYER_CONNECTED\x10i\x12\r\n\tPING_PONG\x10j\x12\x0c\n\x08LEVEL_UP\x10k\x12\x10\n\x0cRESURRECTION\x10l\x12\x10\n\x0b\x43LEAR_CACHE\x10\xac\x02\"\xa1\x05\n\x0bRoomToStage\x12/\n\x04type\x18\x01 \x02(\x0e\x32!.m3.stage.RoomToStage.MessageType\x12*\n\x05start\x18\n \x01(\x0b\x32\x1b.m3.stage.RoomToStage.Start\x12*\n\x05leave\x18\x0b \x01(\x0b\x32\x1b.m3.stage.RoomToStage.Leave\x12\"\n\x04info\x18\x0c \x01(\x0b\x32\x14.m3.common.StageInfo\x12#\n\x08level_up\x18\r \x01(\x0b\x32\x11.m3.common.Player\x12\x38\n\x0cresurrection\x18\x0e \x01(\x0b\x32\".m3.stage.RoomToStage.Resurrection\x1a\x1a\n\x05Leave\x12\x11\n\tplayer_id\x18\x01 \x02(\x03\x1a=\n\x0cResurrection\x12\x11\n\tplayer_id\x18\x01 \x02(\x03\x12\x0c\n\x04\x63oin\x18\x02 \x01(\x03\x12\x0c\n\x04\x63\x61sh\x18\x03 \x01(\x03\x1a\xc6\x01\n\x05Start\x12\x1d\n\x04room\x18\x01 \x02(\x0b\x32\x0f.m3.common.Room\x12\x16\n\x0e\x65xp_multiplier\x18\x02 \x02(\x01\x12\x1d\n\x15monster_health_factor\x18\x03 \x02(\x01\x12\x1d\n\x15monster_attack_factor\x18\x04 \x02(\x01\x12\x1e\n\x16monster_defence_factor\x18\x05 \x02(\x01\x12(\n\nstage_info\x18\x06 \x02(\x0b\x32\x14.m3.common.StageInfo\"b\n\x0bMessageType\x12\n\n\x05START\x10\xc9\x01\x12\n\n\x05LEAVE\x10\xca\x01\x12\x0e\n\tPING_PONG\x10\xcb\x01\x12\t\n\x04INFO\x10\xcc\x01\x12\r\n\x08LEVEL_UP\x10\xcd\x01\x12\x11\n\x0cRESURRECTION\x10\xce\x01')



_STAGETOROOM_MESSAGETYPE = _descriptor.EnumDescriptor(
  name='MessageType',
  full_name='m3.stage.StageToRoom.MessageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='READY', index=0, number=100,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='START', index=1, number=102,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FINISH', index=2, number=103,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEAVE', index=3, number=104,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PLAYER_CONNECTED', index=4, number=105,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PING_PONG', index=5, number=106,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEVEL_UP', index=6, number=107,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESURRECTION', index=7, number=108,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLEAR_CACHE', index=8, number=300,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1050,
  serialized_end=1195,
)

_ROOMTOSTAGE_MESSAGETYPE = _descriptor.EnumDescriptor(
  name='MessageType',
  full_name='m3.stage.RoomToStage.MessageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='START', index=0, number=201,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEAVE', index=1, number=202,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PING_PONG', index=2, number=203,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INFO', index=3, number=204,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEVEL_UP', index=4, number=205,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESURRECTION', index=5, number=206,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1773,
  serialized_end=1871,
)


_STAGETOROOM_READY = _descriptor.Descriptor(
  name='Ready',
  full_name='m3.stage.StageToRoom.Ready',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='m3.stage.StageToRoom.Ready.ip', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='port', full_name='m3.stage.StageToRoom.Ready.port', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='group_id', full_name='m3.stage.StageToRoom.Ready.group_id', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=465,
  serialized_end=516,
)

_STAGETOROOM_FINISH_PLAYER = _descriptor.Descriptor(
  name='Player',
  full_name='m3.stage.StageToRoom.Finish.Player',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='clear', full_name='m3.stage.StageToRoom.Finish.Player.clear', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fail', full_name='m3.stage.StageToRoom.Finish.Player.fail', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='player_id', full_name='m3.stage.StageToRoom.Finish.Player.player_id', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nickname', full_name='m3.stage.StageToRoom.Finish.Player.nickname', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=584,
  serialized_end=719,
)

_STAGETOROOM_FINISH = _descriptor.Descriptor(
  name='Finish',
  full_name='m3.stage.StageToRoom.Finish',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='players', full_name='m3.stage.StageToRoom.Finish.players', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_STAGETOROOM_FINISH_PLAYER, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=519,
  serialized_end=719,
)

_STAGETOROOM_LEAVE = _descriptor.Descriptor(
  name='Leave',
  full_name='m3.stage.StageToRoom.Leave',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='m3.stage.StageToRoom.Leave.player_id', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='play_time', full_name='m3.stage.StageToRoom.Leave.play_time', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='exp', full_name='m3.stage.StageToRoom.Leave.exp', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_score', full_name='m3.stage.StageToRoom.Leave.total_score', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='honbul', full_name='m3.stage.StageToRoom.Leave.honbul', index=4,
      number=5, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=721,
  serialized_end=816,
)

_STAGETOROOM_PLAYERCONNECTED = _descriptor.Descriptor(
  name='PlayerConnected',
  full_name='m3.stage.StageToRoom.PlayerConnected',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='m3.stage.StageToRoom.PlayerConnected.player_id', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=818,
  serialized_end=854,
)

_STAGETOROOM_LEVELUP = _descriptor.Descriptor(
  name='LevelUp',
  full_name='m3.stage.StageToRoom.LevelUp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='m3.stage.StageToRoom.LevelUp.player_id', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='initial_exp', full_name='m3.stage.StageToRoom.LevelUp.initial_exp', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='initial_level', full_name='m3.stage.StageToRoom.LevelUp.initial_level', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='curr_exp', full_name='m3.stage.StageToRoom.LevelUp.curr_exp', index=3,
      number=4, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=856,
  serialized_end=946,
)

_STAGETOROOM_RESURRECTION = _descriptor.Descriptor(
  name='Resurrection',
  full_name='m3.stage.StageToRoom.Resurrection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='m3.stage.StageToRoom.Resurrection.player_id', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=948,
  serialized_end=981,
)

_STAGETOROOM_CLEARCACHE = _descriptor.Descriptor(
  name='ClearCache',
  full_name='m3.stage.StageToRoom.ClearCache',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='m3.stage.StageToRoom.ClearCache.type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='action', full_name='m3.stage.StageToRoom.ClearCache.action', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=983,
  serialized_end=1047,
)

_STAGETOROOM = _descriptor.Descriptor(
  name='StageToRoom',
  full_name='m3.stage.StageToRoom',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='m3.stage.StageToRoom.type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=100,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ready', full_name='m3.stage.StageToRoom.ready', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='leave', full_name='m3.stage.StageToRoom.leave', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='player_connected', full_name='m3.stage.StageToRoom.player_connected', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='finish', full_name='m3.stage.StageToRoom.finish', index=4,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='level_up', full_name='m3.stage.StageToRoom.level_up', index=5,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='resurrection', full_name='m3.stage.StageToRoom.resurrection', index=6,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='clear_cache', full_name='m3.stage.StageToRoom.clear_cache', index=7,
      number=30, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_STAGETOROOM_READY, _STAGETOROOM_FINISH, _STAGETOROOM_LEAVE, _STAGETOROOM_PLAYERCONNECTED, _STAGETOROOM_LEVELUP, _STAGETOROOM_RESURRECTION, _STAGETOROOM_CLEARCACHE, ],
  enum_types=[
    _STAGETOROOM_MESSAGETYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=40,
  serialized_end=1195,
)


_ROOMTOSTAGE_LEAVE = _descriptor.Descriptor(
  name='Leave',
  full_name='m3.stage.RoomToStage.Leave',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='m3.stage.RoomToStage.Leave.player_id', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=721,
  serialized_end=747,
)

_ROOMTOSTAGE_RESURRECTION = _descriptor.Descriptor(
  name='Resurrection',
  full_name='m3.stage.RoomToStage.Resurrection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='m3.stage.RoomToStage.Resurrection.player_id', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='coin', full_name='m3.stage.RoomToStage.Resurrection.coin', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cash', full_name='m3.stage.RoomToStage.Resurrection.cash', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1509,
  serialized_end=1570,
)

_ROOMTOSTAGE_START = _descriptor.Descriptor(
  name='Start',
  full_name='m3.stage.RoomToStage.Start',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='room', full_name='m3.stage.RoomToStage.Start.room', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='exp_multiplier', full_name='m3.stage.RoomToStage.Start.exp_multiplier', index=1,
      number=2, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='monster_health_factor', full_name='m3.stage.RoomToStage.Start.monster_health_factor', index=2,
      number=3, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='monster_attack_factor', full_name='m3.stage.RoomToStage.Start.monster_attack_factor', index=3,
      number=4, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='monster_defence_factor', full_name='m3.stage.RoomToStage.Start.monster_defence_factor', index=4,
      number=5, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stage_info', full_name='m3.stage.RoomToStage.Start.stage_info', index=5,
      number=6, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1573,
  serialized_end=1771,
)

_ROOMTOSTAGE = _descriptor.Descriptor(
  name='RoomToStage',
  full_name='m3.stage.RoomToStage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='m3.stage.RoomToStage.type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=201,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='start', full_name='m3.stage.RoomToStage.start', index=1,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='leave', full_name='m3.stage.RoomToStage.leave', index=2,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='info', full_name='m3.stage.RoomToStage.info', index=3,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='level_up', full_name='m3.stage.RoomToStage.level_up', index=4,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='resurrection', full_name='m3.stage.RoomToStage.resurrection', index=5,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_ROOMTOSTAGE_LEAVE, _ROOMTOSTAGE_RESURRECTION, _ROOMTOSTAGE_START, ],
  enum_types=[
    _ROOMTOSTAGE_MESSAGETYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1198,
  serialized_end=1871,
)

_STAGETOROOM_READY.containing_type = _STAGETOROOM;
_STAGETOROOM_FINISH_PLAYER.fields_by_name['clear'].message_type = common_pb2._FINISHGAME_CLEARED
_STAGETOROOM_FINISH_PLAYER.fields_by_name['fail'].message_type = common_pb2._FINISHGAME_FAILED
_STAGETOROOM_FINISH_PLAYER.containing_type = _STAGETOROOM_FINISH;
_STAGETOROOM_FINISH.fields_by_name['players'].message_type = _STAGETOROOM_FINISH_PLAYER
_STAGETOROOM_FINISH.containing_type = _STAGETOROOM;
_STAGETOROOM_LEAVE.containing_type = _STAGETOROOM;
_STAGETOROOM_PLAYERCONNECTED.containing_type = _STAGETOROOM;
_STAGETOROOM_LEVELUP.containing_type = _STAGETOROOM;
_STAGETOROOM_RESURRECTION.containing_type = _STAGETOROOM;
_STAGETOROOM_CLEARCACHE.fields_by_name['type'].enum_type = common_pb2._CACHETYPE
_STAGETOROOM_CLEARCACHE.containing_type = _STAGETOROOM;
_STAGETOROOM.fields_by_name['type'].enum_type = _STAGETOROOM_MESSAGETYPE
_STAGETOROOM.fields_by_name['ready'].message_type = _STAGETOROOM_READY
_STAGETOROOM.fields_by_name['leave'].message_type = _STAGETOROOM_LEAVE
_STAGETOROOM.fields_by_name['player_connected'].message_type = _STAGETOROOM_PLAYERCONNECTED
_STAGETOROOM.fields_by_name['finish'].message_type = _STAGETOROOM_FINISH
_STAGETOROOM.fields_by_name['level_up'].message_type = _STAGETOROOM_LEVELUP
_STAGETOROOM.fields_by_name['resurrection'].message_type = _STAGETOROOM_RESURRECTION
_STAGETOROOM.fields_by_name['clear_cache'].message_type = _STAGETOROOM_CLEARCACHE
_STAGETOROOM_MESSAGETYPE.containing_type = _STAGETOROOM;
_ROOMTOSTAGE_LEAVE.containing_type = _ROOMTOSTAGE;
_ROOMTOSTAGE_RESURRECTION.containing_type = _ROOMTOSTAGE;
_ROOMTOSTAGE_START.fields_by_name['room'].message_type = common_pb2._ROOM
_ROOMTOSTAGE_START.fields_by_name['stage_info'].message_type = common_pb2._STAGEINFO
_ROOMTOSTAGE_START.containing_type = _ROOMTOSTAGE;
_ROOMTOSTAGE.fields_by_name['type'].enum_type = _ROOMTOSTAGE_MESSAGETYPE
_ROOMTOSTAGE.fields_by_name['start'].message_type = _ROOMTOSTAGE_START
_ROOMTOSTAGE.fields_by_name['leave'].message_type = _ROOMTOSTAGE_LEAVE
_ROOMTOSTAGE.fields_by_name['info'].message_type = common_pb2._STAGEINFO
_ROOMTOSTAGE.fields_by_name['level_up'].message_type = common_pb2._PLAYER
_ROOMTOSTAGE.fields_by_name['resurrection'].message_type = _ROOMTOSTAGE_RESURRECTION
_ROOMTOSTAGE_MESSAGETYPE.containing_type = _ROOMTOSTAGE;
DESCRIPTOR.message_types_by_name['StageToRoom'] = _STAGETOROOM
DESCRIPTOR.message_types_by_name['RoomToStage'] = _ROOMTOSTAGE

class StageToRoom(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType

  class Ready(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STAGETOROOM_READY

    # @@protoc_insertion_point(class_scope:m3.stage.StageToRoom.Ready)

  class Finish(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType

    class Player(_message.Message):
      __metaclass__ = _reflection.GeneratedProtocolMessageType
      DESCRIPTOR = _STAGETOROOM_FINISH_PLAYER

      # @@protoc_insertion_point(class_scope:m3.stage.StageToRoom.Finish.Player)
    DESCRIPTOR = _STAGETOROOM_FINISH

    # @@protoc_insertion_point(class_scope:m3.stage.StageToRoom.Finish)

  class Leave(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STAGETOROOM_LEAVE

    # @@protoc_insertion_point(class_scope:m3.stage.StageToRoom.Leave)

  class PlayerConnected(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STAGETOROOM_PLAYERCONNECTED

    # @@protoc_insertion_point(class_scope:m3.stage.StageToRoom.PlayerConnected)

  class LevelUp(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STAGETOROOM_LEVELUP

    # @@protoc_insertion_point(class_scope:m3.stage.StageToRoom.LevelUp)

  class Resurrection(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STAGETOROOM_RESURRECTION

    # @@protoc_insertion_point(class_scope:m3.stage.StageToRoom.Resurrection)

  class ClearCache(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _STAGETOROOM_CLEARCACHE

    # @@protoc_insertion_point(class_scope:m3.stage.StageToRoom.ClearCache)
  DESCRIPTOR = _STAGETOROOM

  # @@protoc_insertion_point(class_scope:m3.stage.StageToRoom)

class RoomToStage(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType

  class Leave(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ROOMTOSTAGE_LEAVE

    # @@protoc_insertion_point(class_scope:m3.stage.RoomToStage.Leave)

  class Resurrection(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ROOMTOSTAGE_RESURRECTION

    # @@protoc_insertion_point(class_scope:m3.stage.RoomToStage.Resurrection)

  class Start(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ROOMTOSTAGE_START

    # @@protoc_insertion_point(class_scope:m3.stage.RoomToStage.Start)
  DESCRIPTOR = _ROOMTOSTAGE

  # @@protoc_insertion_point(class_scope:m3.stage.RoomToStage)


# @@protoc_insertion_point(module_scope)