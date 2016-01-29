# -*- coding:utf-8 -*-

from app import celery
import gcm

@celery.task()
def push(gcm_url, gcm_sender_id, gcm_server_api_key, member_id, token, message):
    #logger.info('Push registration;{gcm_sender_id:%s,gcm_server_api_key:%s,member_id:%d,token:%s,message:%s}' % (gcm_sender_id, gcm_serer_api_key, member_id, token, message))
    gcm.send_message(gcm_url, gcm_server_api_key, token, message)
