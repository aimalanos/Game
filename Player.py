import random

class Player:
    def __init__(self, w):
        self.name = input("What is your creature's name? ")
        self.diet = input("Is your creature a carnivore or an herbivore? ").lower() # lower() puts it in lowercase, which eliminates the problem of whether the player types with capital or lowercase letters
        w.add_player(self)
        self.world = w
        self.location = random.choice(self.world.squares)
        self.home = self.location # The player's home base will be their starting location.
        self.alive = True
        self.hunger = 100 # If self.hunger reaches 0, the player's health will decrease at each update.
        self.maxHealth, self.health = 15, 15
        self.maxStrength, self.strength = 5, 5
        self.maxSociability, self.sociability = 5, 5
        self.maxSpeed, self.speed = 5, 5
        self.intelligence = 0
        self.experience = 0
        self.abilities = []
        self.inventory = []
        self.availabledirs = []
        self.defeated = 0 # to keep track of the number of enemies the player has defeated
        self.allies = 0
                
    def update(self):
        self.health -= self.world.healthLoss
        if health <= 0:
            self.die()
        if self.hunger > 0:
            self.hunger -= self.world.hungerLoss
        elif self.hunger == 0:
            r = random.randint(0,3) #player will randomly take damage to health, strength, sociability, speed, or intelligence
            if r == 0:
                self.health -= self.health/10
            elif r == 1:
                self.strength -= self.strength/10
            elif r == 2:
                self.sociability -= self.sociability/10
            elif r == 3:
                self.speed -= self.speed/10
        if self.hunger < 0:
            self.hunger = 0
        self.availabledirs = []
        for exit in self.location.exits:
            if exit != None:
                self.availabledirs.append(exit)
            
    def fillStats(self):
        self.health = self.maxHealth
        self.strength = self.maxStrength
        self.sociability = self.maxSociability
        self.speed = self.maxSpeed
        
    def die(self):
        world.gameOver()
        self.alive = False
        
    def eat(self):
        self.fillStats()
        self.hunger += 25
        
    #def drink(self): #did we decide to do this or nah? could be interesting when we implement aquatic skills and stuff
    
    def north(self):
        if self.location.exits['north'] != None:
            self.location = self.location.exits['north']
        else:
            print('You may not move North. Try again.')
    def east(self):
        if self.location.exits['east'] != None:
            self.location = self.location.exits['east']
        else:
            print('You may not move East. Try again.')
    def west(self):
        if self.location.exits['west'] != None:
            self.location = self.location.exits['west']
        else:
            print('You may not move West. Try again.')
    def south(self):
        if self.location.exits['south'] != None:
            self.location = self.location.exits['south']
        else:
            print('You may not move South. Try again.')
        
    def stats(self):
            print("You are a " + self.diet)
            print("Your location is " + str(self.location.coordinates))
            print("Your home is at " + str(self.home.coordinates))
            print("Hunger = " + str(self.hunger))
            print("Health = " + str(self.health))
            print("Strength = " + str(self.strength))
            print("Sociability = " + str(self.sociability))
            print("Speed = " + str(self.speed))
            print("Intelligence = " + str(self.intelligence))
            print("Experience = " + str(self.experience))
            print("Abilities = " + str(self.abilities))
            print("Inventory = " + str(self.inventory) + '\n')
            print(self.location.exits)
