import random

class Player:
    def __init__(self, w):
        self.name = input("What is your creature's name? ")
        self.diet = input("Is your creature a carnivore or an herbivore? ").lower()
        w.add_player(self)
        self.world = w
        self.location = random.choice(self.world.squares) # If we want the player to start at a random location on the map.
        self.home = self.location # The player's home base will be their starting location.
        self.hunger = 100 # If self.hunger reaches 0, the player's health will decrease at each update
        self.maxHealth = 15
        self.health = 15
        self.strength = 5
        self.sociability = 5
        self.speed = 5
        self.intelligence = 0
        self.experience = 0
        self.abilities = []
        self.inventory = []
    def update(self):
        self.health -= self.world.healthLoss
        if self.hunger == 0:
            self.health -= self.health // 10
        else:
            self.hunger -= self.world.hungerLoss
            if self.hunger < 0:
                self.hunger = 0
