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
        self.maxStrength = self.strength
        self.sociability = 5
        self.maxSociability =  self.sociability
        self.speed = 5
        self.maxSpeed = self.speed
        self.intelligence = 0
        self.maxIntelligence = self.intelligence
        self.experience = 0
        self.abilities = []
        self.inventory = []
    def update(self):
        self.health -= self.world.healthLoss
        if health == 0 or health < 0:
            self.die()
        if self.hunger == 0:
            self.health -= self.health // 10
        else:
            r = random.randint(0,4) #player will randomly takes to health, strength, sociability, speed, or intelligence
                if r == 0:
                    self.health -= self.health/10
                elif r == 1:
                    self.strength -= self.strength/10
                elif r == 2:
                    self.sociability -= self.sociability/10
                elif r == 3:
                    self.speed -= self.speed/10
                elif r == 4:
                    self.intelligence -= self.intelligence/10
            if self.hunger < 0:
                self.hunger = 0
    def fillStats(self):
        self.health = self.maxHealth
        self.strength = self.maxStrength
        self.sociability = self.sociability
        self.speed = self.maxSpeed
    def die(self):
        w.gameOver()
    def eat(self):
        self.fillStats()
        self.hunger += 25
    #def drink(self): #did we decide to do this or nah? could be interesting when we implement aquatic skills and stuff
        
def stats(self):
        print("You are a " + self.diet)
        print("Your location is " + str(self.location))
        print("Your home is at " + str(self.home))
        print("Hunger = " + str(self.hunger))
        print("Health = " + str(self.health))
        print("Strength = " + str(self.strength))
        print("Sociability = " + str(self.sociability))
        print("Speed = " + str(self.speed))
        print("Intelligence = " + str(self.intelligence))
        print("Experience = " + str(self.experience))
        print("Abilities = " + str(self.abilities))
        print("Inventory = " + str(self.inventory))
