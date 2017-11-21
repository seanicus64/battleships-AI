import json
import events
class API:
    def __init__(self, protocol):
        self.protocol = protocol
    def send_event(self, event):
        string = event.__dict__
        string = json.dumps(string).encode("utf-8")
        self.protocol.sendLine(string)
    def parse(self, line):
        line = json.loads(line.decode("utf-8"))
        the_class = getattr(events, line["type"])
        del line["type"]
        reconstructed = the_class(**line)
        if the_class in self.react_dict:
            self.react_dict[the_class](reconstructed)
        else:
            return reconstructed
class ServerAPI(API):
    def __init__(self, protocol):
        super().__init__(protocol)
        self.react_dict = {}


class ClientAPI(API):
    def __init__(self, protocol):
        super().__init__(protocol)
        self.react_dict = {
            events.YourTurnEvent: self.react_yourturn,
            events.EndTurnEvent: self.react_endturn,
            events.YouAreEvent: self.react_youare,
            events.PromptEvent: self.react_prompt,
            events.HitEvent: self.react_hit,
            events.MissEvent: self.react_miss,
            events.SunkEvent: self.react_sunk,
            events.BeginGameEvent: self.react_new_game,
            events.GameWonEvent: self.react_game_won,
            }
        self.name = ""
        self.new_game()
    def react_game_won(self, event):
        pass
    def react_new_game(self, event):
        self.is_new_game = True
        self.new_game()
        
    def new_game(self):
        self.is_new_game = True
        self.received = []
        self.player_events = {}
        self.my_turn = False
        self.is_turn = False
        self.hits = []
        self.missed = []
        self.tried = []
        self.ships_left = ["carrier", "cruiser", "battleship", "submarine", "destroyer"]
        self.last_hit = None
        self.last_missed = None
        self.last_tried = None
    def shoot(self, y, x):
        event = events.ShootEvent(y, x)
        self.send_event(event)
    def react_yourturn(self, event):
        pass
    def react_endturn(self, event):
        pass
    def react_youare(self, event):
        self.name = event.you
    def react_prompt(self, event):
        self.is_turn = True
    def react_hit(self, event):
        if event.player == self.name:
            self.hits.append((event.y, event.x))
            self.last_hit = (event.y, event.x)
            self.last_tried = (event.y, event.x)
            self.tried.append((event.y, event.x))
    def react_miss(self, event):
        if event.player == self.name:
            self.missed.append((event.y, event.x))
            self.last_missed = (event.y, event.x)
            self.last_tried = (event.y, event.x)
            self.tried.append((event.y, event.x))
    def react_sunk(self, event):
        if event.player == self.name:
            self.ships_left.remove(event.shipname)
    def react_newgame(self, event):
        self.new_game()
