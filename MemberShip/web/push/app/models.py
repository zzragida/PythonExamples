# -*- coding: utf-8 -*-

from itertools import cycle

from db import sqlrelay_cursor
from db import sqlrelay_close

from nosql import redis_monitor

from util import from_utf8
from util import to_utf8
from util import escape
from util import zero_or_one
from util import encode_base64
from util import decode_base64
from util import get_support
from util import set_support
from util import set_default

from app import logger
import app

from apscheduler.scheduler import Scheduler

def update_server():
    logger.info('Update server information')

    r = redis_monitor()
    if not r:
        logger.error('Can not connect monitor redis')
        return

    name = 'PUSH:' + app.SERVICE_NAME
    info = {'ip': app.HOST, 'port': app.PORT}

    pipe = r.pipeline()
    pipe.zadd('AVAIL:PUSH', app.SERVICE_NAME, 0)
    pipe.hmset(name, info)
    pipe.expire(name, app.UPDATE_INTERVAL)
    pipe.execute()


# intialize update server scheduler
if hasattr(app, 'SERVICE_NAME') and app.SERVICE_NAME:
    scheduler = Scheduler()
    scheduler.start()
    scheduler.add_interval_job(update_server, seconds=app.UPDATE_INTERVAL)
    update_server()

# initialize push scheduler
push_scheduler = Scheduler()
push_scheduler.start()


def push(gcm_sender_id, gcm_server_api_key, app_id, member_ids, message, time):
    # /topics/global 메세지 등록
    if member_ids == '/topics/global':
        push_scheduler.add_date_job(app.tasks.push, time,
           kwargs = dict(gcm_url = app.GCM_URL,
                         gcm_sender_id = gcm_sender_id,
                         gcm_server_api_key = gcm_server_api_key,
                         member_id = member_ids,
                         token = member_ids,
                         message = message))
    else:
        con, cur = sqlrelay_cursor()
        cur.execute("""
           SELECT 
              gcm_token
            , member_id 
           FROM 
              ms_member 
           WHERE
              app_id = %d AND 
              push_notification = 1 AND
              status = 1 AND
              member_id IN (%s)
        """ % (app_id, member_ids))
        results = cur.fetchall()
        sqlrelay_close(cur, con)

        # 사용자별 푸시 스케쥴러 등록
        for r in results:
            gcm_token = r[0]
            member_id = r[1]
            push_scheduler.add_date_job(app.tasks.push, time, 
              kwargs = dict(gcm_url = app.GCM_URL, 
                            gcm_sender_id = gcm_sender_id, 
                            gcm_server_api_key = gcm_server_api_key, 
                            member_id = member_id, 
                            token = gcm_token, 
                            message = message))



def monitor():
    # TODO: 모니터 데이터가 많다면 token은 제거하는것도 좋을듯
    push_list = []
    for job in push_scheduler.get_jobs():
        push_list.append({
           'gcm_sender_id': job.kwargs['gcm_sender_id'],
           'gcm_server_api_key': job.kwargs['gcm_server_api_key'],
           'member_id': job.kwargs['member_id'],
           'token': job.kwargs['token'],
           'message': job.kwargs['message'],
           'time': str(job.next_run_time)
        })
    return push_list


