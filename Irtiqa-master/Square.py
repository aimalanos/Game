# I'm calling the rooms "squares" because they aren't proper rooms.

class Square:
    def __init__(self, w, xcoor, ycoor):
        self.world = w
        self.world.squares.append(self)
        self.coordinates = (xcoor,ycoor) # I had it as parentheses so that it would be a tuple, which is immutable
        self.exits = {}
        #self.exits['north'] = None
        #self.exits['east'] = None
        #self.exits['west'] = None
        #self.exits['south'] = None
        #put the for loop into World.py   
        self.creature = None # I think there should be a max of one NPC per square
        self.plantFood = 0 # I think different squares should have different quantities of food
        self.items = []
    