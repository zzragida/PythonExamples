# -*- coding:utf-8 -*-

import logging
from logging import Formatter
from colorlog import ColoredFormatter
from mongolog.handlers import MongoHandler

logger = None

def get_logger(app, 
               name, 
               log_level=None, 
               log_file=None,
               mongo_host=None,
               mongo_port=None,
               mongo_db=None,
               mongo_collection=None):
    global logger
    if logger: return logger

    # initialize flask access log
    werkzeug_logger = logging.getLogger('werkzeug')

    # initialize logging log_level
    if not log_level: 
        log_level = logging.DEBUG
    else: 
        log_level = get_log_level(log_level)

    # initialize logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # initialize stream log
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

    stream_formatter = ColoredFormatter(
           '%(log_color)s%(asctime)s %(white)s[pid:%(process)d] [%(levelname)s] (%(pathname)s:%(lineno)d) %(message)s',
           reset=True,
           log_colors={
              'DEBUG':   'green',
              'INFO':    'yellow',
              'WARNING': 'cyan',
              'ERROR':   'red',
              'CRITICAL':'red',
           })
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    # initialize file log
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_formatter = Formatter('%(asctime)s;%(levelname)s;%(pathname)s:%(lineno)d;%(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        werkzeug_logger.addHandler(file_handler)
        app.logger.addHandler(file_handler)

    # initialize remote log
    if mongo_collection and mongo_db and mongo_host and mongo_port:
       mongo_handler = MongoHandler.to(db=mongo_db,
                                       collection=mongo_collection,
                                       host=mongo_host,
                                       port=mongo_port,
                                       level=log_level)
       logger.addHandler(mongo_handler)

    return logger


LOG_LEVEL = {
  'debug': logging.DEBUG,
  'info': logging.INFO,
  'warning': logging.WARNING,
  'error': logging.ERROR,
  'critical': logging.CRITICAL
}


def get_log_level(level):
    return LOG_LEVEL.get(level, logging.DEBUG)
