import random
import math

class Creature:
    def __init__(self,square,level):
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
        self.level = level

class Wolf(Creature):
    def __init__(self,square,level):
        Creature.__init__(square,level)
        #self.health = unchanged
        self.strength += 3*self.level
        self.hostility += 3*self.level
        self.speed -= 2*self.level
        self.fleeRate = self.fleeRate/2
class Tiger(Creature):
    def __init__(self,square,level):
        Creature.__init__(square,level)
        self.health += 4*self.level
        self.strength += 5*self.level
        self.hostility += 2*self.level
        self.speed += self.level
        self.fleeRate = self.fleeRate
class Monkey(Creature):
    def __init__(self,square,level):
        Creature.__init__(square,level)
        self.health -= math.floor(10/level)
        self.strength += 5*self.level
        self.hostility += 3*self.level
        self.speed -= 2*self.level
        self.fleeRate = self.fleeRate/2
class Dog(Creature):
    def __init__(self,square,level):
        Creature.__init__(square,level)
        #self.health = unchanged
        self.strength += self.level
        self.hostility += random.randint(1,4)*self.level
        self.speed += self.level
        #self.fleeRate = unchanged
class Sheep(Creature):
    def __init__(self,square,level):
        Creature.__init__(square,level)
        self.health *= 
        self.strength -= 15
        self.hostility -= 15
        self.speed = 5
        self.fleeRate = 0.8
class Snake(Creature):
    def __init__(self,square,level):
        Creature.__init__(square,level)
        self.health = math.ceil(0.3*self.health)
        self.strength += 5*self.level
        self.hostility += 4*self.level
        self.speed *= 5
        self.fleeRate = self.fleeRate/2
