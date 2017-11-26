class Square:
    def __init__(self, w, xcoor, ycoor):
        self.world = w
        self.world.squares.append(self)
        self.coordinates = (xcoor,ycoor) # I had it as parentheses so that it would be a tuple, which is immutable
        self.exits = {'east': None, 'west': None, 'north': None, 'south': None}
        self.creature = None # I think there should be a max of one NPC per square
        self.items = {}
    
