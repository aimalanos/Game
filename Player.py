import random

class Player:
    def __init__(self, w):
        self.name = input("What is your creature's name? ")
        self.diet = input("Is your creature a carnivore or an herbivore? ").lower() # lower() puts it in lowercase, which eliminates the problem of whether the player types with capital or lowercase letters
        while self.diet != 'carnivore' and self.diet != 'herbivore':
            self.diet = input('Invalid response. Choose "carnivore" or "herbivore." ')
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
        if self.health <= 0:
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
        self.world.gameOver()
        self.alive = False
        
    def eat(self):
        if self.diet == 'herbivore' or self.diet == 'omnivore':
            if 'fruit' in self.location.items and self.location.items['fruit'] > 0:
                self.fillStats()
                self.hunger += 25
                self.location.fruit -= 1
            elif 'fruit' in self.inventory:
                self.fillStats()
                self.hunger += 25
                self.inventory['fruit'] -= 1
        elif self.diet == 'carnivore' or self.diet == 'omnivore':
            if 'meat' in self.location.items and self.location.items['meat'] > 0:
                self.fillStats()
                self.hunger += 25
                self.location.items['meat'] -= 1
            elif 'meat' in self.inventory:
                self.fillStats()
                self.hunger += 25
                self.inventory['fruit'] -= 1
        
    def pickup(self, item):
        if item in self.location.items and self.location.items[item] > 0:
            if item in self.inventory:
                self.inventory[item] += 1
            else:
                self.inventory[item] = 1
            self.location.items[item] -= 1
        
        
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
            print('availabledirs = ' + str(self.availabledirs))
            
    def attack(self, creature):
        while self.health > 0 and creature.health > 0:
            print('Creature health = ' + str(creature.health))
            print('Creature strength = ' + str(creature.strength))
            print('Creature hostility = ' + str(creature.hostility))
            print()
            print('You may:')
            print('\t attack')
            print('\t flee')
            choice = input('What will you do? ')
            while choice.lower() != 'attack' and choice.lower() != 'flee':
                print('Invalid command. Choose "attack" or "flee."')
                choice = input('What will you do? ')
            if self.speed >= creature.speed:
                # If the player is faster, the player goes first
                if choice.lower() == 'attack':
                    attackStrength = random.randint(self.strength // 2, self.strength)
                    print("You attack!")
                    print("The creature takes " + str(attackStrength) + " damage!")
                    print("The creature's hostility increases!")
                    creature.health -= self.strength
                    creature.hostility += 3
                elif choice.lower() == 'flee':
                    print("You flee!")
                    break
                creatureAttackChance = creature.hostility * .01
                creatureChoice = random.random()
                if creatureChoice < creature.fleeRate:
                    print("The creature flees!")
                    break
                elif creatureChoice < creatureAttackChance + creature.fleeRate:
                    creatureAttackStrength = random.randint(creature.strength // 2, creature.strength)
                    print("The creature attacks!")
                    print("You take " + str(creatureAttackStrength) + " damage!")
                    self.health -= creatureAttackStrength
                else:
                    print(random.choice(['The creature does nothing!', 'The creature awaits your next move.', 'The creature is watching you closely...']))
            else:
                # If the creature is faster, the creature goes first
                creatureAttackChance = creature.hostility * .01
                creatureChoice = random.random()
                if creatureChoice < creature.fleeRate:
                    print("The creature flees!")
                    break
                elif creatureChoice < creatureAttackChance + creature.fleeRate:
                    creatureAttackStrength = random.randint(creature.strength // 2, creature.strength)
                    print("The creature attacks!")
                    print("You take " + str(creatureAttackStrength) + " damage!")
                    self.health -= creatureAttackStrength
                else:
                    creatureChoice = random.choice(['The creature does nothing!', 'The creature awaits your next move.', 'The creature is watching you closely...'])
                if choice.lower() == 'attack':
                    attackStrength = random.randint(self.strength // 2, self.strength)
                    print("You attack!")
                    print("The creature takes " + str(attackStrength) + " damage!")
                    print("The creature's hostility increases!")
                    creature.health -= self.strength
                    creature.hostility += 3
                elif choice.lower() == 'flee':
                    print("You flee!")
                    break
                if type(creatureChoice) == str:
                    # If the creature does nothing, we say so at the end of the turn.
                    print(creatureChoice)
            if creature.health <= 0 and self.health > 0:
                self.experience += creature.experience
                self.defeated += 1
                self.location.creature = False
                self.location.items['meat'] = random.randint(1,3)
            elif self.health <= 0:
                self.die()

    def ally(self, creature):
        while self.health > 0 and creature.hostility > 0:
            print('Creature health = ' + str(creature.health))
            print('Creature strength = ' + str(creature.strength))
            print('Creature hostility = ' + str(creature.hostility))
            print()
            print('You may:')
            print('\t befriend')
            print('\t flee')
            choice = input('What will you do? ')
            while choice.lower() != 'befriend' and choice.lower() != 'flee':
                print('Invalid command. Choose "befriend" or "flee."')
                choice = input('What will you do? ')
            if self.speed >= creature.speed:
                # If the player is faster, the player goes first
                if choice.lower() == 'befriend':
                    befriendSuccess = random.randint(self.sociability // 2, self.sociability)
                    print("You try to befriend the creature!")
                    print("The creature's hostility decreases!")
                    creature.hostility -= befriendSuccess
                elif choice.lower() == 'flee':
                    print("You flee!")
                    break
                creatureAttackChance = creature.hostility * .01
                creatureChoice = random.random()
                if creatureChoice < creature.fleeRate:
                    print("The creature flees!")
                    break
                elif creatureChoice < creatureAttackChance + creature.fleeRate:
                    creatureAttackStrength = random.randint(creature.strength // 2, creature.strength)
                    print("The creature attacks!")
                    print("You take " + str(creatureAttackStrength) + " damage!")
                    self.health -= creatureAttackStrength
                else:
                    print(random.choice(['The creature does nothing!', 'The creature awaits your next move.', 'The creature is watching you closely...']))
            else:
                # If the creature is faster, the creature goes first
                creatureAttackChance = creature.hostility * .01
                creatureChoice = random.random()
                if creatureChoice < creature.fleeRate:
                    print("The creature flees!")
                    break
                elif creatureChoice < creatureAttackChance + creature.fleeRate:
                    creatureAttackStrength = random.randint(creature.strength // 2, creature.strength)
                    print("The creature attacks!")
                    print("You take " + str(creatureAttackStrength) + " damage!")
                    self.health -= creatureAttackStrength
                else:
                    creatureChoice = random.choice(['The creature does nothing!', 'The creature awaits your next move.', 'The creature is watching you closely...'])
                if choice.lower() == 'befriend':
                    befriendSuccess = random.randint(self.sociability // 2, self.sociability)
                    print("You try to befriend the creature!")
                    print("The creature's hostility decreases!")
                    creature.hostility -= befriendSuccess
                elif choice.lower() == 'flee':
                    print("You flee!")
                    break
                if type(creatureChoice) == str:
                    # If the creature does nothing, we say so at the end of the turn.
                    print(creatureChoice)
            if creature.hostility <= 0 and self.health > 0:
                self.experience += creature.experience
                self.allies += 1
                creature.allied = True
            elif self.health <= 0:
                self.die()

    def flexibleResponse(self, creature):
        while self.health > 0 and (creature.hostility > 0 or creature.health > 0):
            print('Creature health = ' + str(creature.health))
            print('Creature strength = ' + str(creature.strength))
            print('Creature hostility = ' + str(creature.hostility))
            print()
            print('You may:')
            print('\t attack')
            print('\t befriend')
            print('\t flee')
            choice = input('What will you do? ')
            while choice.lower() != 'befriend' and choice.lower() != 'flee':
                print('Invalid command. Choose "attack," "befriend" or "flee."')
                choice = input('What will you do? ')
            if self.speed >= creature.speed:
                # If the player is faster, the player goes first
                if choice.lower() == 'attack':
                    attackStrength = random.randint(self.strength // 2, self.strength)
                    print("You attack!")
                    print("The creature takes " + str(attackStrength) + " damage!")
                    print("The creature's hostility increases!")
                    creature.health -= self.strength
                    creature.hostility += 3
                elif choice.lower() == 'befriend':
                    befriendSuccess = random.randint(self.sociability // 2, self.sociability)
                    print("You try to befriend the creature!")
                    print("The creature's hostility decreases!")
                    creature.hostility -= befriendSuccess
                elif choice.lower() == 'flee':
                    print("You flee!")
                    break
                creatureAttackChance = creature.hostility * .01
                creatureChoice = random.random()
                if creatureChoice < creature.fleeRate:
                    print("The creature flees!")
                    break
                elif creatureChoice < creatureAttackChance + creature.fleeRate:
                    creatureAttackStrength = random.randint(creature.strength // 2, creature.strength)
                    print("The creature attacks!")
                    print("You take " + str(creatureAttackStrength) + " damage!")
                    self.health -= creatureAttackStrength
                else:
                    print(random.choice(['The creature does nothing!', 'The creature awaits your next move.', 'The creature is watching you closely...']))
            else:
                # If the creature is faster, the creature goes first
                creatureAttackChance = creature.hostility * .01
                creatureChoice = random.random()
                if creatureChoice < creature.fleeRate:
                    print("The creature flees!")
                    break
                elif creatureChoice < creatureAttackChance + creature.fleeRate:
                    creatureAttackStrength = random.randint(creature.strength // 2, creature.strength)
                    print("The creature attacks!")
                    print("You take " + str(creatureAttackStrength) + " damage!")
                    self.health -= creatureAttackStrength
                else:
                    creatureChoice = random.choice(['The creature does nothing!', 'The creature awaits your next move.', 'The creature is watching you closely...'])
                if choice.lower() == 'attack':
                    attackStrength = random.randint(self.strength // 2, self.strength)
                    print("You attack!")
                    print("The creature takes " + str(attackStrength) + " damage!")
                    print("The creature's hostility increases!")
                    creature.health -= self.strength
                    creature.hostility += 3
                elif choice.lower() == 'befriend':
                    befriendSuccess = random.randint(self.sociability // 2, self.sociability)
                    print("You try to befriend the creature!")
                    print("The creature's hostility decreases!")
                    creature.hostility -= befriendSuccess
                elif choice.lower() == 'flee':
                    print("You flee!")
                    break
                if type(creatureChoice) == str:
                    # If the creature does nothing, we say so at the end of the turn.
                    print(creatureChoice)
            if creature.health <= 0 and self.health > 0:
                self.experience += creature.experience
                self.defeated += 1
                self.location.creature = False
                self.location.items['meat'] = random.randint(1,3)
            elif creature.hostility <= 0 and self.health > 0:
                self.experience += creature.experience
                self.allies += 1
                creature.allied = True
            elif self.health <= 0:
                self.die()
