# -*- coding:utf-8 -*-

from twisted.internet import protocol
from struct import *


# 프로토콜 버퍼를 사용할 경우의 프로토콜 처리
class ProtobufProtocol(protocol.Protocol):

  def __init__(self):
    self.buffer = ""

  def dataReceived(self, data):
    self.buffer += data
    while len(self.buffer) >= 4:
      (size,) = unpack('I', self.buffer[0:4])
      size += 4
      if len(self.buffer) >= size:
        req = self.buffer[4:size]
        self.process(req)
        self.buffer = self.buffer[size:]
      else:
        break

  def process(self, request):
    raise NotImplementedError

  def send(self, res):
    body = res.SerializeToString()
    header = pack('I', len(body))
    self.transport.write(header + body)


