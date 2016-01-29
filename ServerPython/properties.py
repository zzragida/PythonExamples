# -*- coding:utf-8 -*-

from logger import logger
from util import singleton, from_utf8

import sqlrelay


@singleton
class Properties:
  """ Properties class """

  def __init__(self):
    self.load()

  def load(self):
    for k, v in self._load().items():
      setattr(self, k, v)

  def _load(self):
    results = sqlrelay.execute_results("""
SELECT
   NAME
 , VALUE
FROM
   ARPG_BT_PROPERTIES
""")

    properties = {}
    for r in results:
      name = from_utf8(r[0])
      if r[1].isdigit():
        value = int(r[1])
      else:
        try:
          value = float(r[1])
        except ValueError:
          value = r[1]
      properties[name] = value
    return properties
    
