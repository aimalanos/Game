class Square:
    def __init__(self, w, xcoor, ycoor):
        self.world = w
        self.world.squares.append(self)
        self.coordinates = (xcoor,ycoor)
        self.exits = {'east': None, 'west': None, 'north': None, 'south': None}
        self.creature = None
        self.items = {}
        self.terrain = ''
        self.weather = ''

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
        
        
        
        
#     def listdirs(self):
#         s = ''
#         l = []
#         for exit in self.exits:
#             if self.exits[exit] != None:
#                 l.append(exit)
#                 if len(l) == 2:
#                     s = l[0] + " or " + l[1]
#                 elif len(l) == 3:
#                     s = l[0] + ", " + l[1] + ", or " + l[2]
#                 elif len(l) == 4:
#                     s = l[0] + ", " + l[1] + ", " + l[2] + ", or " + l[3]
#                 else:
#                     print('where the dirs at')
#         return s
