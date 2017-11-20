import random

class Creature:
    def __init__(self, w, level):
        self.world = w
        self.health = random.randint(level*(10-3), level*(10+3))
        self.strength = random.randint(level*(5-2), level*(5+2))
        self.sociability = random.randint(level*(5-2), level*(5+2))
        self.speed = random.randint(level*(5-2), level*(5+2))
        self.experience = (self.health + self.strength + self.sociability + self.speed) // 4
