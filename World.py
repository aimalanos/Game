from Square import Square
import Creature
import random

class World:
    terrains = ['forest','forest','desert','desert','hills','hills','lake','tundra','grassy']
    possibleItems = ['stinkfruit', 'sticky sap', 'poison berries', 'big leaf', 'healing salve', 'flowers', 'big stick', 'nesting materials']
    itemWeights = {'fruit': 2, 'meat': 2, 'stinkfruit': 2, 'sticky sap': 3, 'poison berries': 3, 'big leaf': 3, 'healing salve': 3, 'flowers': 2, 'big stick': 3, 'nesting materials': 5}
    possibleCreatures = [Creature.Wolf,Creature.Tiger,Creature.Monkey,Creature.Dog,Creature.Sheep,Creature.Snake]
    aquaticCreatures = [Creature.Fish,Creature.Eel,Creature.Leviathan]
    def __init__(self):
        self.turn_count = 0
        self.weather = "clear"
        self.player = None
        self.squares = [[None,None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None,None]]
        self.possibleCommands = {'me':['me'],'help':['help'],'allstats':['allstats','all stats'],'pickup':['pickup'],'go':['go'],'inspect':['inspect'], 'attack': ['attack'], 'befriend': ['befriend'], 'recruit': ['recruit'], 'dismiss':['dismiss'], 'evolve': ['evolve'], 'use': ['use'], 'inventory': ['inventory'], 'use': ['use'], 'drop': ['drop']}
        self.weatherlist = ["clear", "rainy", "hailing", "snowy", "drought"]
        self.weather = random.choice(self.weatherlist)
        
    def makeMap(self,x,y):
        for i in range(0,x):
            for j in range(0,y):
                self.squares[j][i] = Square(self, i, j)
        col = 0
        while col < len(self.squares)-1:
            row = 0
            while row < len(self.squares[col])-1:
                if self.squares[col][row].coordinates[0] == 0:
                    if self.squares[col][row].coordinates[1] == 0:
                        self.squares[col][row].exits['north'] = col[row+1]
                        self.squares[col][row].exits['east'] = self.squares[column+1][row]
                    elif self.squares[col][row].coordinates[1] == y:
                        self.squares[col][row].exits['south'] = col[row-1]
                        self.squares[col][row].exits['east'] = self.squares[column+1][row]
                    else:
                        self.squares[col][row].exits['north'] = col[row+1]
                        self.squares[col][row].exits['south'] = col[row-1]
                        self.squares[col][row].exits['east'] = self.squares[column+1][row]
                elif self.squares[col][row].coordinates[0] == x:
                    if self.squares[col][row].coordinates[1] == 0:
                        self.squares[col][row].exits['north'] = col[row+1]
                        self.squares[col][row].exits['west'] = self.squares[column-1][row]
                    elif self.squares[col][row].coordinates[1] == y:
                        self.squares[col][row].exits['south'] = col[row-1]
                        self.squares[col][row].exits['west'] = self.squares[column-1][row]
                    else:
                        self.squares[col][row].exits['north'] = col[row+1]
                        self.squares[col][row].exits['south'] = col[row-1]
                        self.squares[col][row].exits['west'] = self.squares[column-1][row]
                elif self.squares[col][row].coordinates[1] == 0:
                    self.squares[col][row].exits['west'] = self.squares[column-1][row]
                    self.squares[col][row].exits['south'] = col[row-1]
                    self.squares[col][row].exits['east'] = self.squares[column+1][row]
                elif self.squares[col][row].coordinates[1] == y:
                    self.squares[col][row].exits['west'] = self.squares[column-1][row]
                    self.squares[col][row].exits['north'] = col[row+1]
                    self.squares[col][row].exits['east'] = self.squares[column+1][row]
                else:
                    self.squares[col][row].exits['north'] = col[row+1]
                    self.squares[col][row].exits['south'] = col[row-1]
                    self.squares[col][row].exits['east'] = self.squares[column+1][row]
                    self.squares[col][row].exits['west'] = self.squares[column-1][row]
###############
        for squ in self.squares:
            t = random.randint(0,7)
            squ.terrain = self.terrains[t]
            if squ.exits['east'] == None:
                if squ.coordinates[0] != x:
                    for squ2 in self.squares:
                        if squ2.coordinates[0] == squ.coordinates[0] + 1:
                            if squ2.coordinates[1] == squ.coordinates[1]:
                                squ.exits['east'] = squ2
                                squ2.exits['west'] = squ
            if squ.exits['west'] == None:
                if squ.coordinates[0] != -x:
                    for squ2 in self.squares:
                        if squ2.coordinates[0] == squ.coordinates[0] - 1:
                            if squ2.coordinates[1] == squ.coordinates[1]:
                                squ.exits['west'] = squ2
                                squ2.exits['east'] = squ
            if squ.exits['north'] == None:
                if squ.coordinates[1] != y:
                    for squ2 in self.squares:
                        if squ2.coordinates[1] == squ.coordinates[0] + 1:
                            if squ2.coordinates[0] == squ.coordinates[0]:
                                squ.exits['north'] = squ2
                                squ2.exits['south'] = squ
            if squ.exits['south'] == None:
                if squ.coordinates[0] != -y:
                    for squ2 in self.squares:
                        if squ2.coordinates[1] == squ.coordinates[1] - 1:
                            if squ2.coordinates[0] == squ.coordinates[0]:
                                squ.exits['south'] = squ2
                                squ2.exits['north'] = squ

    def add_player(self, player):
        self.player = player
        
    def update(self):
        self.player.update()
        self.turn_count += 1
        if self.turn_count % 5 == 0:
            # New creatures will spawn
            randomSquare = random.choice(self.squares)
            if randomSquare.creature == None:
                level = random.randint(1,3)
                creatureType = random.choice(self.possibleCreatures)
                creatureType(self, randomSquare, level)
            # New items will appear
            for i in range(3):
                randomSquare = random.choice(self.squares)
                if 'fruit' in randomSquare.items:
                    randomSquare.items['fruit'] += 1
                else:
                    randomSquare.items['fruit'] = 1
            for i in range(2):
                randomSquare = random.choice(self.squares)
                newItem = random.choice(self.possibleItems)
                if newItem in randomSquare.items:
                    randomSquare.items[newItem] += 1
                else:
                    randomSquare.items[newItem] = 1
            self.weather = random.choice(self.weatherlist)
            print('here')
