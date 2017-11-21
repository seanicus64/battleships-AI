import random
import time

class myscript:
    def __init__(self, api):
        self.api = api
        self.target = False
        self.seed = (
            random.randrange(3, 7), 
            random.randrange(3, 7))
        self.grid = []
        self.othergrid = []
        self.target_neighbors = []
        for y in range(10):
            for x in range(10):
                if (sum((y, x)) % 2) == (sum(self.seed) % 2):
                    self.grid.append((y, x))
                else:
                    self.othergrid.append((y, x))
        random.shuffle(self.grid)
        random.shuffle(self.othergrid)
        self.stack = []

    def draw(self):
        string = " 0123456789\n"
        for y in range(10):
            string += str(y)
            for x in range(10):
                tile = (y, x)
                if tile in self.api.tried:
                    string += "@"
                else:
                    string += " "
            string += "\n"

    def random_guess(self):
        x = random.randrange(10)
        y = random.randrange(10)
        return y, x

    def check_valid(self, tile):
        if ((0 <= tile[0] < 10) and (0 <= tile[1] < 10)):
            return True
        return False

    def check_tried(self, tile):
        if tile in self.api.tried:
            return True
        return False

    def get_neighbors(self, tile):
        temp = [
            (tile[0] - 1, tile[1]),
            (tile[0], tile[1] - 1),
            (tile[0] + 1, tile[1]),
            (tile[0], tile[1] + 1)
            ]
        neighbors = []
        for direction in temp:
            if ((not self.check_tried(direction)) and self.check_valid(direction)):
                neighbors.append(direction)
        random.shuffle(neighbors)
        return neighbors

    def tick(self):
        # delete tile from lists of tiles you havent checked yet
        if self.api.last_tried:
            tried = self.api.last_tried
            if tried in self.grid:
                self.grid.remove(tried)
            if tried in self.othergrid:
                self.othergrid.remove(tried)

        # If the last shot hit something, add it to the potential targets stack
        if self.api.last_tried == self.api.last_hit and self.api.last_tried:
            self.stack.append(self.api.last_hit)
        
        # remove elements from stack that are invalid
        temp_stack = []
        for t in self.stack:
            neighbors = self.get_neighbors(t)
            if neighbors:
                temp_stack.append(t)
        self.stack = temp_stack

        if self.target not in self.stack:
            self.target = False

        # get target if we don't have one
        if not self.target and self.stack:
            self.target = self.stack[-1]

        if self.target:
            neighbors = self.get_neighbors(self.target)
            return neighbors.pop()
        if self.grid:
            return self.grid.pop()
        # These last two probably should never run, but just in case...
        elif self.othergrid:
            return self.othergrid.pop()
        return self.random_guess()

