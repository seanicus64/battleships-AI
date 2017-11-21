#!/usr/bin/env python3
import sys
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
import API
import events
class ClientProtocol(LineReceiver):
    def __init__(self, script):
        self.i = 0
        self.script = script
        
    def lineReceived(self, line):
        self.api.parse(line)
        if self.api.is_new_game:
            self.userscript = self.script.myscript(self.api)
        self.api.is_new_game = False
        if self.api.is_turn:
            self.tick()
            self.api.is_turn = False
    def connectionMade(self):
        self.api = API.ClientAPI(self)
        self.userscript = self.script.myscript(self.api)
    def tick(self):
        guess = self.userscript.tick()
        self.api.shoot(guess[0], guess[1])
    def connectionLost(self, reason):
        pass

class Factory(ClientFactory):
    def __init__(self, script):
        self.script = script
    def buildProtocol(self, addr):
        return ClientProtocol(self.script)
def run_factory(which_script):
    if which_script == 1:
        import script as script
    if which_script == 2:
        import script2 as script
    return Factory(script)
if __name__ == "__main__":
    reactor.connectTCP("", 12345, Factory())
    reactor.run()
