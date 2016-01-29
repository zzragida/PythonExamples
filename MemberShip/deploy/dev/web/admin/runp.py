# -*- coding:utf-8 -*-

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from app import app
from app import logger
from app import HOST
from app import PORT

if __name__ == '__main__':
    host = (HOST, PORT)
    logger.info('starting admin service (%s:%d)' % (HOST, PORT))

    http_server = WSGIServer(host, app)
    http_server.serve_forever()

