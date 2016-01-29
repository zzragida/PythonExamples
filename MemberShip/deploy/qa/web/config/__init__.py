# -*- coding:utf-8 -*-

import yaml

CONFIG_FILE = '/home/kjs/projects/M3ARPG/MemberShip/web/config/settings.yaml'

config = yaml.load(file(CONFIG_FILE, 'r'))

# for db
SQLRELAYS = config['sqlrelays']


# for nosql
REDIS_MONITOR = config['redis-monitor']
REDIS_MEMBERS = config['redis-members']


# for mongodb
MONGODB_HOST = config['mongodb']['host']
MONGODB_PORT = config['mongodb']['port']
MONGODB_DB = config['mongodb']['db']


# for push
PUSH_URL = config['push']['url']


# for celery
CELERY_BROKER_URL = config['celery']['broker_url']
CELERY_BACKEND_URL = config['celery']['backend_url']
CELERY_RESULT_BACKEND = config['celery']['result_backend']
CELERY_TASK_SERIALIZER = config['celery']['task_serializer']
CELERY_ACCEPT_CONTENT = config['celery']['accept_content']
CELERY_TIMEZONE = config['celery']['timezone']
CELERY_ENABLE_UTC = config['celery']['enable_utc']
CELERY_REDIS_MAX_CONNECTIONS = config['celery']['redis_max_connections']


# for admin service
ADMIN_SERVICE_NAME = 'admin'
ADMIN_HOST = config['admin']['host']
ADMIN_PORT = config['admin']['port']
ADMIN_UPLOAD_PATH = config['admin']['upload_path']
ADMIN_SECRET_KEY = config['admin']['secret_key']
ADMIN_DEBUG = config['admin']['debug']
ADMIN_LOG_LEVEL = config['admin']['log']['level']
ADMIN_LOG_FILENAME = config['admin']['log']['filename']

PER_PAGE = 50


# for membership service
MEMBERSHIP_SERVICE_NAME = None
MEMBERSHIP_HOST = None
MEMBERSHIP_PORT = None
MEMBERSHIP_DEBUG = None
MEMBERSHIP_SECRET_KEY = None
MEMBERSHIP_EXPIRE_TIME = None
MEMBERSHIP_UPDATE_INTERVAL = None

MEMBERSHIP_LOG_LEVEL = None
MEMBERSHIP_LOG_FILENAME = None

MEMBERSHIP_APP_ID = None
MEMBERSHIP_APP_KEY = None
MEMBERSHIP_APP_SECRET = None


def load_membership(host, port, name=None):
    global MEMBERSHIP_SERVICE_NAME
    global MEMBERSHIP_HOST
    global MEMBERSHIP_PORT
    global MEMBERSHIP_DEBUG
    global MEMBERSHIP_SECRET_KEY
    global MEMBERSHIP_EXPIRE_TIME
    global MEMBERSHIP_UPDATE_INTERVAL
    global MEMBERSHIP_LOG_LEVEL
    global MEMBERSHIP_LOG_FILENAME
    global MEMBERSHIP_APP_ID
    global MEMBERSHIP_APP_KEY
    global MEMBERSHIP_APP_SECRET

    if not name: name = 'test-membership' 
    MEMBERSHIP_SERVICE_NAME = name + ':' + str(port)

    MEMBERSHIP_HOST = host
    MEMBERSHIP_PORT = port
    MEMBERSHIP_DEBUG = config[name]['debug']
    MEMBERSHIP_SECRET_KEY = config[name]['secret_key']
    MEMBERSHIP_EXPIRE_TIME = config[name]['expire_time']
    MEMBERSHIP_UPDATE_INTERVAL = config[name]['update_interval']

    MEMBERSHIP_LOG_LEVEL = config[name]['log']['level']
    MEMBERSHIP_LOG_FILENAME = config[name]['log']['filename']

    MEMBERSHIP_APP_ID = config[name]['app']['id']
    MEMBERSHIP_APP_KEY = config[name]['app']['key']
    MEMBERSHIP_APP_SECRET = config[name]['app']['secret']


# for push service
PUSH_SERVICE_NAME = None
PUSH_HOST = None
PUSH_PORT = None
PUSH_DEBUG = None
PUSH_SECRET_KEY = None
PUSH_UPDATE_INTERVAL = None

PUSH_LOG_LEVEL = None
PUSH_LOG_FILENAME = None

PUSH_GCM_URL = None


def load_push(host, port, name=None):
    global PUSH_SERVICE_NAME
    global PUSH_HOST
    global PUSH_PORT
    global PUSH_DEBUG
    global PUSH_SECRET_KEY
    global PUSH_UPDATE_INTERVAL
    global PUSH_LOG_LEVEL
    global PUSH_LOG_FILENAME
    global PUSH_GCM_URL

    if not name: name = 'test-push'
    PUSH_SERVICE_NAME = name + ':' + str(port)

    PUSH_HOST = host
    PUSH_PORT = port
    PUSH_DEBUG = config[name]['debug']
    PUSH_SECRET_KEY = config[name]['secret_key']
    PUSH_UPDATE_INTERVAL = config[name]['update_interval']

    PUSH_LOG_LEVEL = config[name]['log']['level']
    PUSH_LOG_FILENAME = config[name]['log']['filename']

    PUSH_GCM_URL = config[name]['gcm']['url']

