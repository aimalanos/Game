from Square import Square
import random

class World:
    def __init__(self):
        self.turn_count = 0
        self.weather = "clear"
        self.player = None
        self.squares = []
        self.healthLoss = 0 # Determines how much health is lost when updating
        self.hungerLoss = 3 # Determines how much the player's hunger increases when updating
        self.speedPenalty = 0 # The penalties will be applied depending on the weather
        self.sociabilityPenalty = 0
    def makeMap(self,x,y):
        for i in range(-x, x+1):
            for j in range(-y, y+1):
                Square(self, i, j)
        for squ in self.squares:
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
    def reset(self):
        self.healthLoss = 0
        self.hungerLoss = 3
        self.speedPenalty = 0
        self.sociabilityPenalty = 0
    def gameOver(self):
        print("Your creature has died! Game over!")
        self.player = None
    def update(self):
        self.player.update()
        self.turn_count += 1
        if self.turn_count % 5 == 0:
            self.weather = random.choice(["clear", "rainy", "hailing", "snowy", "drought"])
            if self.weather == "rainy":
                self.speedPenalty = self.player.speed // 10
            elif self.weather == "hailing":
                self.healthLoss = self.player.health // 15
            elif self.weather == "snowy":
                self.sociabilityPenalty = self.player.sociability // 10
            elif self.weather == "drought":
                self.hungerLoss = 6
