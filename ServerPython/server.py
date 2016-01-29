#!/usr/bin/env python
# -*- coding:utf-8 -*-

from logger import logger

try:
  from twisted.internet import iocpreactor
  iocpreactor.install()
  logger.debug("using iocp reactor")
except Exception:
  try:
    from twisted.internet import epollreactor
    epollreactor.install()
    logger.debug("using epoll reactor")
  except Exception:
    logger.debug("using select reactor")

from twisted.internet import reactor, endpoints
from gateway import GatewayFactory


# 서버구동
def main():
  bind_address = '0.0.0.0'
  gateway_port = 5001
  logger.debug("start gateway server(%s:%d)" % (bind_address, gateway_port))

  #reactor.listenTCP(gateway_port, GatewayFactory(), 100, bind_address)
  endpoints.serverFromString(reactor, "tcp:%d" % gateway_port).listen(GatewayFactory())
  
  try:
    reactor.run()	
  except KeyboardInterrupt:
    logger.error("stop gateway server")



if __name__ == "__main__":
  main()
 
