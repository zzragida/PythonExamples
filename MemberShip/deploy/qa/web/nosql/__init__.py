# -*- coding:utf-8 -*-

import redis
from config import REDIS_MONITOR
from config import REDIS_MEMBERS


MONITOR_POOL = redis.ConnectionPool(**REDIS_MONITOR)
MEMBERS_POOL = []
for member in REDIS_MEMBERS:
    MEMBERS_POOL.append(redis.ConnectionPool(**member))


def redis_monitor():
    ''' Access Monitor StrictRedis '''
    return redis.StrictRedis(connection_pool=MONITOR_POOL)


def redis_members():
    ''' Access Members StrictRedis '''
    ret = []
    for pool in MEMBERS_POOL:
        ret.append(redis.StrictRedis(connection_pool=pool))
    return ret


def redis_member(member_id):
    ''' Access Member StrictRedis by MemberID '''
    idx = long(member_id) % len(MEMBERS_POOL)
    pool = MEMBERS_POOL[idx]
    return redis.StrictRedis(connection_pool=pool)



