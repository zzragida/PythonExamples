# -*- coding:utf-8 -*-

from flask.ext.paginate import Pagination
from config import PER_PAGE

import base64
import logging


def encode_base64(data):
    return base64.b64encode(data)


def decode_base64(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'='* missing_padding
    return base64.b64decode(data)


def from_utf8(s):
    return s.decode(encoding='UTF-8')


def to_utf8(s):
    return s.encode(encoding='UTF-8')


def escape(s):
    return s.replace("'", "\\'")


def zero_or_one(v):
    if v: return 1
    else: return 0


def get_support(data):
    return True if data == '1' else False


def set_support(data):
    return 1 if data == True else 0


def set_default(data):
    return 'NULL' if data == None else to_utf8(data)


def dict_item(data, value):
    return data.get(int(value), 'Undefined')

def dict_item_index(data, value):
    if not isinstance(data, dict): return
    for key, val in data.iteritems():
        if val == value:
            return key

def dict_item_choices(data):
    if not isinstance(data, dict): return []
    choices = []
    for key, val in data.iteritems():
        choices.append([key, val])
    return choices


def make_pagination(page, total, record_name, per_page=None):
    if not per_page: per_page = PER_PAGE
    return Pagination(page = page,
                      total = total,
                      per_page = per_page,
                      search = False,
                      link_size = '20px',
                      record_name = record_name)
