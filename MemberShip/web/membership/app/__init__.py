# -*- coding:utf-8 -*-

from flask import Flask
from flask import request

from config import MEMBERSHIP_SERVICE_NAME as SERVICE_NAME
from config import MEMBERSHIP_HOST as HOST
from config import MEMBERSHIP_PORT as PORT
from config import MEMBERSHIP_DEBUG as DEBUG
from config import MEMBERSHIP_SECRET_KEY as SECRET_KEY
from config import MEMBERSHIP_EXPIRE_TIME as EXPIRE_TIME
from config import MEMBERSHIP_UPDATE_INTERVAL as UPDATE_INTERVAL

from config import MEMBERSHIP_LOG_LEVEL as LOG_LEVEL
from config import MEMBERSHIP_LOG_FILENAME as LOG_FILENAME

from config import MEMBERSHIP_APP_ID as APP_ID
from config import MEMBERSHIP_APP_KEY as APP_KEY
from config import MEMBERSHIP_APP_SECRET as APP_SECRET

from config import PUSH_URL
GCM_SENDER_ID = None
GCM_SERVER_API_KEY = None

from config import MONGODB_HOST
from config import MONGODB_PORT
from config import MONGODB_DB

APP_NAME = None

import membership_pb2
PROTOCOL_VERSION = membership_pb2.Version().protocol

# for google and android
SUPPORT_ANDROID = None
SUPPORT_PLAYSTORE = None
PLAYSTORE_URL = None

# for apple and ios
SUPPORT_IOS = None
SUPPORT_APPSTORE = None
APPSTORE_URL = None

# for gamefiler
SUPPORT_GAMEFLIER = None
GAMEFLIER_URL = None

# for facebook
FACEBOOK_APP_ID = None
FACEBOOK_APP_NAME = None
FACEBOOK_APP_SECRET = None
FACEBOOK_API_VERSION = None

# for products
PRODUCTS = None


# initialize flask
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY


from logger import get_logger

# initialize logger
logger = get_logger(app, SERVICE_NAME, LOG_LEVEL, LOG_FILENAME,
                    MONGODB_HOST, MONGODB_PORT, MONGODB_DB, SERVICE_NAME)

import models
# load app info
models.load_app(force=True)
models.update_server()

# register update server scheduler
from apscheduler.scheduler import Scheduler

scheduler = Scheduler()

# update server infomation
@scheduler.interval_schedule(seconds=UPDATE_INTERVAL)
def update_server():
    models.update_server()

scheduler.print_jobs()
scheduler.start()

import views


