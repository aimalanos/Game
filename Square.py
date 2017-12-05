class Square:
    def __init__(self, w, xcoor, ycoor):
        self.world = w
        self.world.squares.append(self)
        self.coordinates = (xcoor,ycoor)
        self.exits = {'east': None, 'west': None, 'north': None, 'south': None}
        self.creature = None
        self.items = {}
        self.terrain = ''

    def availableDirs(self):
        dirs = ['north','south','east','west']
        availableDirs = []
        for direction in dirs:
            if self.exits[direction] != None:
                if self.exits[direction].terrain == 'lake':
                    if 'semiaquatic' in self.world.player.abilities:
                        availableDirs.append(direction)
                else:
                    availableDirs.append(direction)
        print('You may go:')
        for direction in availableDirs:
            print('\t' + direction)
