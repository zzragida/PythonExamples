# -*- coding:utf-8 -*-

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

import sys
import socket
from config import load_push as load_config

if __name__ == '__main__':
    # load config by name
    host = sys.argv[1].split('=')[1]
    port = int(sys.argv[2].split('=')[1])
    name = socket.gethostname() + '-push'

    load_config(host, port, name)

    from app import app
    from app import logger
    from app import SERVICE_NAME

    logger.info('starting %s service (%s:%d)' % (SERVICE_NAME, host, port))

    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()

