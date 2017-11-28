import random
import math

class Creature:
    def __init__(self, square, level, name):
        self.location = square
        self.location.creature = True
        self.world = self.location.world
        self.health = random.randint(self.level*(10-3), self.level*(10+3))
        self.strength = random.randint(self.level*(5-2), self.level*(5+2))
        self.hostility = random.randint(self.level*(5-2), self.level*(5+2))
        self.speed = random.randint(self.level*(5-2), self.level*(5+2))
        self.fleeRate = random.uniform(0, 0.2)
        self.allied = False
        self.experience = (self.health + self.strength + self.hostility + self.speed) // 4
        self.name = name
        self.level = level

class Wolf(Creature):
    def __init__(self):
        if self.name == 'wolf':
            #self.health = unchanged
            self.strength += 3*self.level
            self.hostility += 3*self.level
            self.speed -= 2*self.level
            self.fleeRate = self.fleeRate/2
        elif self.name == 'tiger':
            self.health += 4*self.level
            self.strength += 5*self.level
            self.hostility += 2*self.level
            self.speed -= 2*self.level
            self.fleeRate = self.fleeRate
        elif self.name == 'monkey':
            self.health -= math.floor(10/level)
            self.strength += 5*self.level
            self.hostility += 3*self.level
            self.speed -= 2*self.level
            self.fleeRate = self.fleeRate/2
