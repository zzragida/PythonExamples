# -*- coding:utf-8 -*-

import os
import sys
sys.path.insert(0, '../')

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

import sys
import socket
from config import load_membership as load_config

if __name__ == '__main__':
    # load config by name
    host = sys.argv[2].split('=')[1]
    port = int(sys.argv[3].split('=')[1])
    name = socket.gethostname() + '-membership'

    load_config(host, port, name)

    from app import app
    from app import logger
    from app import SERVICE_NAME

    from flask.ext.script import Manager

    logger.info('starting %s service' % (SERVICE_NAME))

    manager = Manager(app)
    manager.run()

