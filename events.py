ship_sizes = {"carrier": 5, "battleship": 4, "cruiser": 3, "submarine": 3, "destroyer": 2}
class PromptEvent:
    def __init__(self):
        self.type = type(self).__name__
        
class YouAreEvent:
    def __init__(self, you):
        self.you = you
        self.type = type(self).__name__
class BaseEvent:
    def __init__(self, amount):
        self.type = type(self).__name__
class ShootEvent(BaseEvent):
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.type = type(self).__name__
class HitEvent:
    def __init__(self, y, x, player):
        self.y = y
        self.x = x
        self.player = player
        self.type = type(self).__name__
class MissEvent:
   def __init__(self, y, x, player):
       self.y = y
       self.x = x
       self.player = player
       self.type = type(self).__name__
   def __repr__(self):
       return "{} \033[32mMISS\033[0m: {}, {}".format(self.player, self.y, self.x)

class JoinEvent:
    def __init__(self):
        self.type = "JoinEvent"
class YourTurnEvent:
    def __init__(self):
        self.type = type(self).__name__
class EndTurnEvent:
    def __init__(self):
        self.type = type(self).__name__
class BeginGameEvent(BaseEvent):
    def __init__(self, which):
        self.which = which
        self.type = type(self).__name__
class GameWonEvent(BaseEvent):
    def __init__(self, player, which):
        self.player = player
        self.which = which
        self.type = type(self).__name__
class SunkEvent:
    def __init__(self, shipname, player):
        self.player = player
        self.shipname = shipname
        self.type = type(self).__name__
