#!/usr/bin/env python3
import server
import client
from twisted.internet import reactor
reactor.listenTCP(12345, server.GameFactory())
#reactor.connectTCP("", 12345, client.Factory(1))

#reactor.connectTCP("", 12345, client.Factory(2))
reactor.connectTCP("", 12345, client.run_factory(1))
reactor.connectTCP("", 12345, client.run_factory(2))
reactor.run()
