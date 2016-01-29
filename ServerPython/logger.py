# -*- coding:utf-8 -*-

from colorlog import ColoredFormatter
import logging
global logger
logger = logging.getLogger('M3ARPG')
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler('M3ARPG.log')
streamHandler = logging.StreamHandler()
fileHandler.setLevel(logging.DEBUG)
streamHandler.setLevel(logging.DEBUG)

#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter = ColoredFormatter(
               '%(log_color)s%(asctime)s %(levelname)s %(white)s%(message)s',
               reset=True,
               log_colors={
                  'DEBUG':   'green',
                  'INFO':    'yellow',
                  'WARNING': 'cyan',
                  'ERROR':   'red',
                  'CRITICAL':'red',
               })

fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)
