'''
Caroline Canfield, Theresa Rumoro, Emily Walden
Where's Wumpus?

GameCell uses a constructor, setters, and getters to create a game cell.
'''


class GameCell:


    # Constructor
    def __init__(self):
        self.stench = False
        self.breeze = False
        self.wumpus = False
        self.gold = False
        self.pit = False
        self.visited = False
        self.safe_space = False
        self.occupied = False


    # Setters
    def set_pit(self):
        self.pit = True
    def set_breeze(self):
        self.breeze = True

    def set_wumpus(self):
        self.wumpus = True

    def set_stench(self):
        self.stench = True

    def set_gold(self):
        self.gold = True

    def set_visited(self):
        self.visited = True

    def set_safe_space(self):
        self.safe_space = True

    def set_occupied(self):
        self.occupied = True


    # Getters 
    def get_breeze(self):
        return self.breeze

    def get_stench(self):
        return self.stench

    def get_pit(self):
        return self.pit

    def get_wumpus(self):
        return self.wumpus

    def get_gold(self):
        return self.gold

    def get_visited(self):
        return self.visited

    def get_safe_space(self):
        return self.safe_space

    def get_occupied(self):
        return self.occupied

