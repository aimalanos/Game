from Square import Square
from Creature import Creature
import random

# def clear():
#     os.system('cls' if os.name == 'nt' else 'clear')

class World:
    def __init__(self):
        self.turn_count = 0
        self.weather = "clear"
        self.player = None
        self.squares = []
        self.terrains = ['grassy','grassy','desert','desert','mountainous','mountainous','tundra','forest']
        self.weathers = ["clear", "rainy", "hailing", "snowy", "drought"]
        self.possibleItems = ['stinkfruit', 'sticky sap', 'poison berries', 'big leaf', 'healing salve', 'flowers']
        self.possibleCreatures = ['wolf','tiger','monkey','dog','sheep','snake']
    def makeMap(self,x,y):
        for num in range(-x,x): #draw the grid
            for nums in range(-y,y):
                self.squares.append(Square(self,num,nums))
            for squ in self.squares: #assign squares' exits
                t = random.randint(0,7)
                squ.terrain = self.terrains[t]
                w = random.randint(0,4)
                squ.weather = self.weathers[w]
                for nei in self.squares:
                    if squ.coordinates[1] == nei.coordinates[1]: # To be east-west adjacent, they must have the same y-coordinate
                        if squ.coordinates[0] == nei.coordinates[0] - 1:
                            nei.exits['west'] = squ
                        elif squ.coordinates[0] == nei.coordinates[0] + 1:
                            nei.exits['west'] = squ
                    elif squ.coordinates[0] == nei.coordinates[0]: # To be north-south adjacent, they must have the same x-coordinate
                        if squ.coordinates[1] == nei.coordinates[1] - 1:
                            nei.exits['south'] = squ
                        elif squ.coordinates[1] == nei.coordinates[1] + 1:
                            nei.exits['north'] = squ

    def add_player(self, player):
        self.player = player
    #def reset(self): #remove this function?
#        self.healthLoss = 0
#        self.hungerLoss = 3
#        self.speedPenalty = 0
#        self.sociabilityPenalty = 0
    def gameOver(self):
        print("Your creature has died! Game over!")
        self.player = None
    def update(self):
        self.player.update()
        self.turn_count += 1
        if self.turn_count % 5 == 0:
            self.reset()
            self.weather = random.choice(["clear", "rainy", "hailing", "snowy", "drought"]) #remove
            # New creatures will spawn
            randomSquare = random.choice(self.squares)
            if randomSquare.creature == None:
                level = random.randint(1,3)
                Creature(self, randomSquare, level)
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
