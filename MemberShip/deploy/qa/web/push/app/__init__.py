# -*- coding:utf-8 -*-

import os
import sys
sys.path.insert(0, '../')

from flask import Flask
from flask import request

from config import PUSH_SERVICE_NAME as SERVICE_NAME
from config import PUSH_HOST as HOST
from config import PUSH_PORT as PORT
from config import PUSH_DEBUG as DEBUG
from config import PUSH_SECRET_KEY as SECRET_KEY
from config import PUSH_UPDATE_INTERVAL as UPDATE_INTERVAL

from config import PUSH_LOG_LEVEL as LOG_LEVEL
from config import PUSH_LOG_FILENAME as LOG_FILENAME

from config import PUSH_GCM_URL as GCM_URL

from config import MONGODB_HOST
from config import MONGODB_PORT
from config import MONGODB_DB

from config import CELERY_BROKER_URL
from config import CELERY_BACKEND_URL
from config import CELERY_RESULT_BACKEND
from config import CELERY_TASK_SERIALIZER
from config import CELERY_ACCEPT_CONTENT
from config import CELERY_TIMEZONE
from config import CELERY_ENABLE_UTC
from config import CELERY_REDIS_MAX_CONNECTIONS

from celery import Celery


# initialize flask
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY


from logger import get_logger

# initialize logger
logger = get_logger(app, SERVICE_NAME, LOG_LEVEL, LOG_FILENAME,
                    MONGODB_HOST, MONGODB_PORT, MONGODB_DB, SERVICE_NAME)

# initialize Celery
def make_celery(app):
    celery = Celery(__name__, broker=CELERY_BROKER_URL)
    celery.conf.update(
        CELERY_BACKEND_URL = CELERY_BACKEND_URL,
        CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND,
        CELERY_TASK_SERIALIZER = CELERY_TASK_SERIALIZER,
        CELERY_ACCEPT_CONTENT = CELERY_ACCEPT_CONTENT,
        CELERY_TIMEZONE = CELERY_TIMEZONE,
        CELERY_ENABLE_UTC = CELERY_ENABLE_UTC,
        CELERY_REDIS_MAX_CONNECTIONS = CELERY_REDIS_MAX_CONNECTIONS,
    )
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

import tasks
import models
import views
