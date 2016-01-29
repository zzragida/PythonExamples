# -*- coding:utf-8 -*-

from logger import logger


def singleton(cls):
  instance = cls()
  instance.__call__ = lambda: instance
  return instance


def from_utf8(s):
  return s.decode(encoding='UTF-8')


def to_utf8(s):
  return s.encode(encoding='UTF-8')
