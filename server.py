#!/usr/bin/env python3
import API
import events
import json
import random
import time
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.protocols.basic import LineReceiver
class Tile:
    def __init__(self):
        self.occupant = None
        self.hit = False
    def __str__(self):
        if self.occupant:
            if self.hit:
                return "\033[31mx\033[0m"
            return "\033[33m{}\033[0m".format(repr(self.occupant))
        else:
            if self.hit:
                return '+'
            return " "
class Ship:
    def __init__(self, health, name):
        self.health = health
        self.name = name
        self.ship_dict = {
            "carrier": "C", "battleship": "B", 
            "cruiser": "U", "submarine": "S", 
            "destroyer": "D"}
    def __str__(self):
        return self.ship_dict[self.name]
    def __repr__(self):
        return self.ship_dict[self.name]
        
class ServerProtocol(LineReceiver):
    def __repr__(self):
        return self.randomname
    def __init__(self, game):
        self.game = game
        self.api = API.ServerAPI(self)
        self.randomname = ""
        for i in range(6):
            self.randomname += random.choice("abcdefghijklmnop")
    def connectionMade(self):
        self.game.add_player(self)
    def connectionLost(self, reason):
        pass
    def lineReceived(self, line):
        event = self.api.parse(line)
        self.game.react(event, self)
class GameFactory(ServerFactory):
    def __init__(self):
        self.game = Game()
    def buildProtocol(self, addr):
        return ServerProtocol(self.game)
class Game:
    def __init__(self):
        self.players = []
        self.games_won = {}
        self.which_game = -1
        self.react_dict = {
            events.ShootEvent: self.react_shoot,
            }
    def react_shoot(self, event, player):
        if not (0 <= event.y < 10 and 0 <= event.x < 10):
            self.prompt() 
            return False
            
        grid = self.grids[self.shootee]
        tile = grid[event.y][event.x]
        
        if tile.hit:
            self.prompt()
            return False
        tile.hit = True
        if tile.occupant:
            tile.occupant.health -= 1
            event = events.HitEvent(event.y, event.x, self.shooter.randomname)
            self.broadcast_event(event)
            if tile.occupant.health == 0:
                self.ships_left[self.shootee].remove(tile.occupant)
                event = events.SunkEvent(tile.occupant.name, self.shooter.randomname)
                self.broadcast_event(event)
                if len(self.ships_left[self.shootee]) == 0:
                    self.end_game()
                    return
        else:
            event = events.MissEvent(event.y, event.x, self.shooter.randomname)
            self.broadcast_event(event)
        self.next_turn()
    def end_game(self):
        self.draw_grids()
        self.games_won[self.shooter] += 1
        event = events.GameWonEvent(self.shooter.randomname, self.which_game)
        self.broadcast_event(event)
        if self.which_game < 10000:
            self.new_game()
        else:
            reactor.callFromThread(reactor.stop)
    def next_turn(self):
        self.draw_grids()
        self.turn += 1
        
        self.shooter = self.players[self.turn % 2]
        self.shootee = self.players[(self.turn-1)%2]
        self.prompt()

    def add_player(self, player):
        if len(self.players) >= 2:
            return
        self.players.append(player)
        self.games_won[player] = 0
        player.api.send_event(events.YouAreEvent(player.randomname))
        if len(self.players) == 2: 
            self.new_game()
    def react(self, event, player):
        if type(event) in self.react_dict.keys():
            self.react_dict[type(event)](event,  player)
    def new_game(self):
        self.which_game += 1
        self.grids = {}
        self.ships_left = {}
        self.turn = 0
        random.shuffle(self.players)
        self.shooter = self.players[0]
        self.shootee = self.players[1]
        self.start_game()
    def broadcast_event(self, event):
        for p in self.players:
            p.api.send_event(event)
    def prompt(self):
        event = events.PromptEvent()
        self.shooter.api.send_event(event)
    def place_ship_randomly(self, ship, player):
        grid = self.grids[player]
        size = ship.health
        direction = random.randrange(2)
        
        while True:
            positions = []
            tiles = []
            if direction == 0:
                x = random.randrange(10-size)
                y = random.randrange(10)
                tiles = [grid[y][x+a] for a in range(size)]
                
            else:
                x = random.randrange(10)
                y = random.randrange(10-size)
                tiles = [grid[y+a][x] for a in range(size)]
            valid = True
            for t in tiles:
                if t.occupant:
                    valid = False
            if not valid: continue
            break
        for t in tiles:
            t.occupant = ship
    def draw_grids(self):
        print(self.games_won)
        print("="*15)
        for grid in self.grids.values():
            for line in grid:
                print("".join([str(ch) for ch in line]))
            print("-"*15)
        
    def place_ships(self):
        for p in self.players:
            self.grids[p] = [[Tile() for i in range(10)] for i in range(10)]
            grid = self.grids[p]
            ships_to_place = [Ship(h, n) for n, h in events.ship_sizes.items()]
            self.ships_left[p] = ships_to_place
            for s in ships_to_place:
                self.place_ship_randomly(s, p)
        
    def start_game(self):
        self.place_ships()
        self.stage = "GAME"
        event = events.BeginGameEvent(self.which_game)
        self.broadcast_event(event)
        print("{}: ================NEW GAME {}=================".format("Server", self.which_game))
        
        self.prompt()

if __name__ == "__main__":        

    reactor.listenTCP(12345, GameFactory())
    reactor.run()

