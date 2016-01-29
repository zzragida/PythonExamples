# -*- coding:utf-8 -*-

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from app import app
from app import logger

from flask.ext.script import Manager

if __name__ == '__main__':
    logger.info('starting admin service')

    manager = Manager(app)
    manager.run()

