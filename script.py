# Unless you know what you're doing, do not delete or
# edit the lines followed by "do not delete". 
# Besides that, do what you want!
import random
import events
class myscript: # do not delete
    def __init__(self, my_api): # do not delete
        self.my_api = my_api    # do not delete
        self.all_to_guess = []
        for y in range(10):
            for x in range(10):
                self.all_to_guess.append((y, x))
        self.current = 0
    def random_guess(self):
        x = random.randrange(10)
        y = random.randrange(10)
        return y, x

    def tick(self): # do not delete
        if self.current >= 100:
            self.current = 0
        to_shoot = self.all_to_guess[self.current]

        self.current += 1
        print(to_shoot[0], to_shoot[1])
        return (to_shoot[0], to_shoot[1])
#        self.my_api.shoot(to_shoot[0], to_shoot[1])
