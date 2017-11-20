import random

class Creature:
    def __init__(self, square, level):
        self.location = square
        self.world = self.location.world
        self.health = random.randint(level*(10-3), level*(10+3))
        self.strength = random.randint(level*(5-2), level*(5+2))
        self.hostility = random.randint(level*(5-2), level*(5+2))
        self.speed = random.randint(level*(5-2), level*(5+2))
        self.experience = (self.health + self.strength + self.sociability + self.speed) // 4
