# I'm calling the rooms "squares" because they aren't proper rooms.

class Square:
    def __init__(self, w, xcoor, ycoor):
        self.world = w
        self.world.squares.append(self)
        self.coordinates = (xcoor,ycoor)
        self.exits = {}
        for squ in self.world.squares:
            if squ.coordinates[1] == self.coordinates[1]: # To be east-west adjacent, they must have the same y-coordinate
                if squ.coordinates[0] == self.coordinates[0] - 1:
                    self.exits[east] = squ
                elif squ.coordinates[0] == self.coordinates[0] + 1:
                    self.exits[west] = squ
            elif squ.coordinates[0] == self.coordinates[0]: # To be north-south adjacent, they must have the same x-coordinate
                if squ.coordinates[1] == self.coordinates[1] - 1:
                    self.exits[south] = squ
                elif squ.coordinates[1] == self.coordinates[1] + 1:
                    self.exits[north] = squ    
        self.creature = None # I think there should be a max of one NPC per square
        self.food = 0 # I think different squares should have different quantities of food
        self.items = []
    
