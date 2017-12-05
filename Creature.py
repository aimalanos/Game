import random
import math

class Creature:
    def __init__(self,square,level):
        self.location = square
        self.location.creature = self
        self.originalLocation = self.location
        self.level = level
        self.world = self.location.world
        self.health = random.randint(self.level*(10-3), self.level*(10+3))
        self.strength = random.randint(self.level*(5-2), self.level*(5+2))
        self.hostility = random.randint(self.level*(5-2), self.level*(5+2))
        self.speed = random.randint(self.level*(5-2), self.level*(5+2))
        self.fleeRate = random.uniform(0, 0.2)
        self.befriended = False
        self.experience = (self.health + self.strength + self.hostility + self.speed) // 4

class Wolf(Creature):
    def __init__(self,square,level):
        Creature.__init__(self,square,level)
        self.strength += 3*self.level
        self.hostility += 3*self.level
        self.speed -= 2*self.level
        if self.speed < 0:
            self.speed = 0
        self.fleeRate = self.fleeRate/2
        self.name = 'wolf'
class Tiger(Creature):
    def __init__(self,square,level):
        Creature.__init__(self,square,level)
        self.health += 4*self.level
        self.strength += 3*self.level
        self.hostility += 2*self.level
        self.speed += self.level
        self.name = 'tiger'
class Monkey(Creature):
    def __init__(self,square,level):
        Creature.__init__(self,square,level)
        self.health -= math.floor(10/level)
        self.strength += 2*self.level
        self.hostility += 3*self.level
        self.speed += 2*self.level
        self.fleeRate = self.fleeRate/2
        self.name = 'monkey'
class Dog(Creature):
    def __init__(self,square,level):
        Creature.__init__(self,square,level)
        self.strength += self.level
        self.hostility += random.randint(1,4)*self.level
        self.speed += self.level
        self.name = 'dog'
class Sheep(Creature):
    def __init__(self,square,level):
        Creature.__init__(self,square,level)
        self.health = math.floor(self.health*0.5)
        self.strength -= 15
        if self.strength < 0:
            self.strength = 0
        self.hostility -= 15
        if self.hostility < 0:
            self.hostility = 0
        self.speed = 5
        self.fleeRate = 0.8
        self.name = 'sheep'
class Snake(Creature):
    def __init__(self,square,level):
        Creature.__init__(self,square,level)
        self.location = square
        self.location.creature = self
        self.level = level
        self.health = math.ceil(0.3*self.health)
        self.strength += 5*self.level
        self.hostility += 4*self.level
        self.speed *= 5
        self.fleeRate = self.fleeRate/2
        self.name = 'snake'
