import random
import os

def asOrderedList(d):
    ordered = []
    for key in d:
        ordered.append([key, d[key]])
        ordered.sort()
    return ordered

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self, w):
        self.world = w
        self.name = input("What is your creature's name? ")
        print("Is your creature a carnivore or an herbivore?")
        self.diet = input("Herbivores need only find fruit to survive, while carnivores must kill their prey to have meat. ").lower()
        while self.diet != 'carnivore' and self.diet!= 'c' and self.diet != 'herbivore' and self.diet != 'h':
            self.diet = input('Invalid response. Choose "carnivore" or "herbivore." ')
        if self.diet == 'h':
            self.diet = 'herbivore'
        elif self.diet == 'c':
            self.diet = 'carnivore'

        w.add_player(self)

        self.location = random.choice(self.world.squares)
        while self.location.terrain == 'lake':
            self.location = random.choice(self.world.squares)
        self.home = self.location # The player's home base will be their starting location.

        self.alive = True
        
        self.hunger = 100 # If self.hunger reaches 0, the player's health will decrease at each update.
        self.maxHealth, self.health = 50, 50
        self.maxStrength, self.strength = 5, 5
        self.maxSociability, self.sociability = 5, 5
        self.maxSpeed, self.speed = 5, 5
        
        self.healthLoss = 2
        self.hungerLoss = 5
        self.speedPenalty = 0
        self.socPenalty = 0
        
        self.intelligence = 0
        self.experience = 0
        
        self.abilities = []
        self.inventory = {}
        self.inventorySize = 0
        self.inventoryCap = 10
        self.invweight = 0
        self.maxinvweight = 20
        
        self.availabledirs = []
        self.dirstring = ''
        
        self.defeated = 0
        self.friends = []
        self.ally = None
        
        self.m = 0
        self.going = ''

        self.conch = True
        self.conchUses = 0
            
    def update(self):
        if self.conchUses >= 2:
            self.conch = False
            self.conchUses = 0
            del self.inventory['conch shell']
            input('Unfortunately, you dropped your conch shell while using it. It is destroyed.')
        if self.going != '':
            print('You go ' + self.going + '.')
            self.going = ''
        self.dirstring = ''
        for elem in self.availabledirs:
            if self.dirstring == '':
                self.dirstring = elem
            else:
                self.dirstring += ', ' + elem
                
        # We reset the penalties in order to implement the terrain and weather effects
        self.healthLoss = 2
        self.hungerLoss = 5
        self.speedPenalty = 0
        self.socPenalty = 0
        if self.hunger > 100:
            self.hunger = 100
        
        # Terrain effects
        #@@@@@@@@@@@@@@@@@@@@@@@@@import pdb; pdb.set_trace()
        if self.location.terrain == "desert":
            self.hungerLoss += 5
        elif self.location.terrain == "hills":
            self.speedPenalty += self.maxSpeed // 4
        elif self.location.terrain == "tundra":
            self.healthLoss += 3
        
        # Weather effects
        if self.world.weather == "rainy":
            self.speedPenalty += self.maxSpeed // 4
        elif self.world.weather == "hailing":
            self.healthLoss += 3
        elif self.world.weather == "snowy":
            self.socPenalty += self.maxSociability // 4
        elif self.world.weather == "drought":
            self.hungerLoss += 5

        # You gain health at home
        if self.location == self.home:
            healthGained = self.maxHealth // 2
            self.health += healthGained
            if self.health > self.maxHealth:
                self.health = self.maxHealth
                healthGained -= self.health - self.maxHealth
            print('You gain ' + str(healthGained) + ' health at your home base!')
        else: # Your stats (may) go down elsewhere
            self.health -= self.healthLoss
            self.sociability -= self.socPenalty
            if self.sociability < 0: # No negative stats
                self.sociability = 0
            self.speed -= self.speedPenalty
            if self.speed < 0:
                self.speed = 0
            print('You lose ' + str(self.healthLoss) + ' health from the terrain and weather.')
            print('Your sociability decreases by ' + str(self.socPenalty) + ' points.')
            print('Your speed decreases by ' + str(self.speedPenalty) + ' points.')
        if self.health <= 0:
            self.die()
            
        if self.hunger > 0:
            if 'Improved metabolism' in self.abilities: # The "Improved metabolism" ability makes you become hungrier less quickly
                self.hunger -= 5
            else:
                self.hunger -= self.hungerLoss
            if self.hunger < 0:
                self.hunger = 0
        elif self.hunger == 0: # If they player is starving...
            r = random.randint(0,3) # then they will randomly take damage to health, strength, sociability, or speed
            if r == 0:
                hungerPenalty = self.health // 10
                self.health -= hungerPenalty
                print("You're starving! You lose " + str(hungerPenalty) + " health!")
            elif r == 1:
                hungerPenalty = self.strength // 10
                self.strength -= hungerPenalty
                print("You're starving! You lose " + str(hungerPenalty) + " strength!")
            elif r == 2:
                hungerPenalty = self.sociability // 10
                self.sociability -= hungerPenalty
                print("You're starving! You lose " + str(hungerPenalty) + " sociability!")
            elif r == 3:
                hungerPenalty = self.speed // 10
                self.speed -= hungerPenalty
                print("You're starving! You lose " + str(hungerPenalty) + " speed!")
        if self.hunger < 0: # You can't have negative hunger!
            self.hunger = 0
            
        self.availabledirs = []
        for exit in self.location.exits:
            if exit != None:
                self.availabledirs.append(exit)
                
        if 'meat' in self.inventory:
            self.m += 1
            if self.m == 6: # If you go long enough with meat in your inventory, then it will rot all your food
                self.invweight -= self.inventory['fruit'] * self.world.itemWeights['fruit']
                self.invweight -= self.inventory['meat'] * self.world.itemWeights['meat']
                del self.inventory['fruit']
                del self.inventory['meat']
                self.m = 0
                print('Oh no! You carried meat in your bag for too long. All of your food has gone rotten.')
        else:
            self.m = 0

    def showInventory(self):
        #clear()
        print('Your inventory contains the following items:')
        orderedInventory = asOrderedList(self.inventory)
        for kvp in orderedInventory:
            weight = self.world.itemWeights[kvp[0]] * kvp[1]
            print('\t' + kvp[0] + ' x' + str(kvp[1]) + ', ' + str(weight) + ' weight')

    def showAbilities(self):
        print('You have the following abilities:')
        for ab in self.abilities:
            print('\t' + ab)
            
    def evolve(self):
        clear()
        print('Health increase: 5 exp')
        print('Stomach size increase: 5 exp')
        print('Strength increase: 5 exp')
        print('Sociability increase: 5 exp')
        print('Speed increase: 5 exp')
        print('Intelligence increase – unlock new upgrades: 5 exp')
        print('Pouches – can carry more items: 5 exp')
        print('Stronger back – can carry heaver items: 5 exp')
        if self.diet != 'omnivore':
            print('Omnivorous diet — eat any food you find: 10 exp')
        if 'Metabolism increase' not in self.abilities:
            print('Metabolism increase – hunger increases more slowly: 10 exp')
        if 'Fat reserves' not in self.abilities:
            print('Fat reserves – reduced penalty when starving: 10 exp')
        if 'Semiaquatic' not in self.abilities:
            print('Semiaquatic – access watery terrain: 10 exp')
        if 'use items' not in self.abilities:
            print('Use items: 10 exp')
        if self.intelligence >= 8 and 'Item use' not in self.abilities:
            print('Item use: 10 exp')
        if self.intelligence >= 13 and 'Item use' in self.abilities and 'Flexible responding' not in self.abilities:
            print('Flexible responding – more options when you engage with other creatures: 20 exp') # Idk, maybe players will be able to change whether they want to socialize or attack. Also, I just thought that if the player attacks a creature, then the creature's hostility should go up
        if self.intelligence >= 20 and 'Flexible responding' in self.abilities:
            print('Fire: 30 exp')
            
        print()
        print('Go back.')
        print()
        print('You have ' + str(self.experience) + ' experience points.')
        print()
        transactionCompleted = False
        while not transactionCompleted:
            choice = input('What would you like to improve? ')
            if choice.lower() == 'health increase':
                if self.experience >= 5:
                    self.maxHealth += 8
                    self.health = self.maxHealth
                    self.experience -= 5
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'use items':
                if self.experience >= 10:
                    self.abilities.append('use items')
                    self.abilities.append('Item use')
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'stomach size increase':
                if self.experience >= 5:
                    self.maxHunger += 5
                    self.hunger = self.maxHunger
                    self.experience -= 5
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'strength increase':
                if self.experience >= 5:
                    self.maxStrength += 3
                    self.strength = self.maxStrength
                    self.experience -= 5
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'sociability increase':
                if self.experience >= 5:
                    self.maxSociability += 3
                    self.sociability = self.maxSociability
                    self.experience -= 5
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'speed increase':
                if self.experience >= 5:
                    self.maxSpeed += 3
                    self.speed = self.maxSpeed
                    self.experience -= 5
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'intelligence increase':
                if self.experience >= 5:
                    self.intelligence += 4
                    self.experience -= 5
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'pouches':
                if self.experience >= 5:
                    self.inventoryCap += 3
                    self.experience -= 5
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'stronger back':
                if self.experience >= 5:
                    self.maxinvweight += 3
                    self.experience -= 5
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'omnivore':
                if self.experience >= 10:
                    self.diet = 'omnivore'
                    self.abilities.append('omnivore')
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'metabolism increase':
                if self.experience >= 15:
                    self.abilities.append('improved metabolism')
                    self.experience -= 15
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'fat reserves':
                if self.experience >= 15:
                    self.abilities.append('fat reserves')
                    self.experience -= 15
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'semiaquatic':
                if self.experience >= 15:
                    self.abilities.append('semiaquatic')
                    self.experience -= 15
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'item use':
                if self.experience >= 15:
                    self.abilities.append('item use')
                    self.experience -= 15
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'flexible responding':
                if self.experience >= 25:
                    self.abilities.append('flexible responding')
                    self.experience -= 30
                    transactionCompleted = True
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'fire':
                if self.experience >= 35:
                    self.abilities.append('fire')
                    victory()
                else:
                    print('Not enough experience. Try again.')
            elif choice.lower() == 'go back':
                transactionCompleted = True
            
    def fillStats(self, n):
        healthGained = self.maxHealth // n
        self.health += healthGained
        if self.health > self.maxHealth:
            self.health = self.maxHealth
            print('Your health is now at max!')
        else:
            print('You gain ' + str(healthGained) + ' health.')
         
        strengthGained = self.maxStrength // n
        self.strength += strengthGained
        if self.strength > self.maxStrength:
            self.strength = self.maxStrength
            print('Your strength is now at max!')
        else:
            print('You gain ' + str(strengthGained) + ' strength.')
            
        
        sociabilityGained = self.maxSociability // n
        self.sociability += sociabilityGained
        if self.sociability > self.maxSociability:
            self.sociability = self.maxSociability
            print('Your sociability is now at max!')
        else:
            print('You gain ' + str(sociabilityGained) + ' sociability.')
            
        speedGained = self.maxSpeed // n
        self.speed += speedGained
        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
            print('Your speed is now at max!')
        else:
            print('You gain ' + str(sociabilityGained) + ' speed.')
        
    def die(self):
        self.alive = False
        
    def eat(self, food):
        while food != 'fruit' and food != 'meat':
            food = input("Sorry, I didn't catch that. Do you want to eat fruit or meat? ")
        print()
        if food not in self.location.items and food not in self.inventory:
            print("There's no " + food + " for you to eat here!")
            return
        if food == 'fruit':
            if self.diet == 'herbivore' or self.diet == 'omnivore':
                if 'fruit' in self.location.items:
                    self.location.items['fruit'] -= 1
                    if self.location.items['fruit'] <= 0:
                        del self.location.items['fruit']
                elif 'fruit' in self.inventory:
                    self.inventory['fruit'] -= 1
                    self.inventorySize -= 1
                    self.invweight -= self.world.itemWeights['fruit']
                    if self.inventory['fruit'] <= 0:
                        del self.inventory['fruit']
                print('You eat the fruit.')
                print()
                self.fillStats(2)
                self.hunger += 20
                return True
            else:
                print("You can't eat that! Bleh!")
                return
        elif food == 'meat':
            if self.diet == 'carnivore' or self.diet == 'omnivore':
                if 'meat' in self.location.items:
                    self.location.items['meat'] -= 1
                    if self.location.items['meat'] <= 0:
                        del self.location.items['meat']
                elif 'meat' in self.inventory:
                    self.inventory['meat'] -= 1
                    self.inventorySize -= 1
                    self.invweight -= self.world.itemWeights['meat']
                    if self.inventory['meat'] <= 0:
                        del self.inventory['meat']
                print('You eat the meat.')
                self.fillStats(1)
                self.hunger += 30
                return True
            else:
                print("You can't eat that! Bleh!")
                return
        
    def pickup(self, item):
        if self.location.terrain == 'forest':
            if 'big stick' not in self.inventory:
                print("You'll need a stick or something to get the item out of the trees.")
                return
            elif 'big stick' in self.inventory and 'Item use' not in p.abilities:
                print('You need to unlock the "item use" ability before that stick will help you!')
                return
        if item in self.location.items:
            if self.invweight + self.world.itemWeights[item] > self.maxinvweight:
                s = self.invweight + self.world.itemWeights[item] - self.maxinvweight
                print("This item is too heavy for you to pick up! Leave it behind or free up " + str(s) + " points of weight in your inventory. ")
            elif self.inventorySize < self.inventoryCap:
                if item in self.location.items:
                    if item in self.inventory:
                        self.inventory[item] += 1
                        self.invweight += self.world.itemWeights[item]
                    else:
                        self.inventory[item] = 1
                        self.invweight += self.world.itemWeights[item]
                    self.location.items[item] -= 1
                    if self.location.items[item] <= 0:
                        del self.location.items[item]
                    print('You pick up the ' + item + '.')
            else:
                print('Your inventory is already full!')
        else:
            print('There is no such item here.')
        
    def drop(self,item):
        if item in self.inventory:
            if item in self.location.items:
                self.location.items[item] += 1
            else:
                self.location.items[item] = 1
            self.inventory[item] -= 1
            self.invweight -= self.world.itemWeights[item]
            if self.inventory[item] <= 0:
                del self.inventory[item]
            print('You drop the ' + item + '.')
        else:
            print('There is no such item in your inventory.')
                
    def inspect(self, item):
        if item == 'creature' or item in self.world.creatureNames:
            if self.location.creature == None:
                print('There is no creature here.')
            else:
                print("The creature is a " + self.location.creature.name + '!')
                print("It has " + str(self.location.creature.health) + " health, " + str(self.location.creature.speed) + " speed, " + str(self.location.creature.strength) + " strength, and " + str(self.location.creature.hostility) + " hostility.")
            #$$$
        elif item in self.location.items or item in self.inventory:
            if item == 'sticky sap':
                print("Sticky sap from a tree. Use it during an encounter to decrease the other creature's speed.")
            elif item == 'poison berries':
                print("Poisonous berries. Use them during an encounter to decrease the other creature's health and strength.")
            elif item == 'big leaf':
                print('A large, surprisingly sturdy leaf. It could protect you from the weather.')
            elif item == 'healing salve':
                print('A healing salve from a plant. Use it to restore your stats.')
            elif item == 'flowers':
                print("Pretty flowers. Use them during an encounter to decrease the other creature's hostility.")
            elif item == 'big stick':
                print('A large stick. It will let you get items out of trees.')
            elif item == 'nesting materials':
                print('Materials for building a nest. Use them to move your home base.')
            elif item == 'fruit':
                print('A fruit. If you are an herbivore or omnivore, then eating this will reduce hunger and restore your stats.')
            elif item == 'meat':
                print('A piece of meat. If you are a carnivore or omnivore, then eating this will reduce hunger and restore your stats.')
            elif item == 'seaweed':
                print('A big nasty ball of seaweed. Use it during a fight to distract an animal and reduce its strength.')
            elif item == 'driftwood':
                print('A large piece of driftwood. Use it during a fight to try to block your opponent\'s attacks.')
            elif item == 'conch shell':
                print('A conch shell. Use it on land to calm the creatures around you and temporarily decrease their hostility.')
        else:
            print('There is nothing by that name here.')
                    
    def useItem(self, item):
        if 'Item use' not in self.abilities and 'use items' not in self.abilities:
            print('You need to unlock the "Item use" ability before you can use items!')
            return False
        else:
            if item in self.inventory:
                if item != 'conch shell':
                    print('You use the ' + item + '.')
                if item == 'fruit':
                    self.eat(item)
                elif item == 'meat':
                    self.eat(item)
                elif item == 'healing salve':
                    print('All your stats have been restored!')
                    self.fillStats(1)
                    self.inventory['healing salve'] -= 1
                    self.inventorySize -= 1
                    self.invweight -= self.world.itemWeights['healing salve']
                    if self.inventory['healing salve'] <= 0:
                        del self.inventory['healing salve']
                elif item == 'big leaf':
                    print('You are now protected from the weather!')
                    self.world.weather = 'clear'
                    self.inventory['big leaf'] -= 1
                    self.inventorySize -= 1
                    self.invweight -= self.world.itemWeights['big leaf']
                    if self.inventory['big leaf'] <= 0:
                        del self.inventory['big leaf']
                elif item == 'nesting materials':
                    if self.location == self.home:
                        print("You're already at home!")
                    else:
                        print('You have established a new home at the current location!')
                        self.home = self.location
                        self.inventory['nesting materials'] -= 1
                        self.inventorySize -= 1
                        self.invweight -= self.world.itemWeights['nesting materials']
                        if self.inventory['nesting materials'] <= 0:
                            del self.inventory['nesting materials']
                elif item == 'conch shell':
                    if self.location.terrain == 'lake':
                        input("You can't use that here! Sea animals don't care for conch shells. Go to land to use this.")
                    else:
                        print('The sound of the conch calms the creatures around you, and briefly decreases their hostility!')
                        self.world.hostilityDec = True
                        self.conchUses += 1
                else:
                    print("Now's not the time to use that!")
                    return False
                return True
            elif item in self.location.items:
                print('You must pick an item up before you can use it!')
            else:
                print("There's no item by that name in your inventory.")
            return False
                    
    def useBattleItem(self, item, target):
        if item in self.inventory:
            if item == 'sticky sap':
                target.speed -= target.speed // 2
                self.inventory['sticky sap'] -= 1
                self.inventorySize -= 1
                self.invWeight -= self.world.itemWeights['sticky sap']
                if self.inventory['sticky sap'] <= 0:
                    del self.inventory['sticky sap']
            elif item == 'poison berries':
                target.health -= target.health // 4
                target.strength -= target.strength // 4
                self.inventory['poison berries'] -= 1
                self.inventorySize -= 1
                self.invWeight -= self.world.itemWeights['poison berries']
                if self.inventory['poison berries'] <= 0:
                    del self.inventory['poison berries']
            elif item == 'healing salve':
                self.fillStats()
                self.inventory['healing salve'] -= 1
                self.inventorySize -= 1
                self.invWeight -= self.world.itemWeights['healing salve']
                if self.inventory['healing salve'] <=0:
                    del self.inventory['healing salve']
            elif item == 'flowers':
                target.hostility -= target.hostility // 3
                self.inventory['flowers'] -= 1
                self.inventorySize -= 1
                self.invWeight -= self.world.itemWeights['flowers']
                if self.inventory['flowers'] <=0:
                    del self.inventory['flowers']
            elif item == 'seaweed':
                target.strength -= random.randint(2,5)
                self.inventory['seaweed'] -= 1
                self.inventorySize -= 1
                self.invWeight -= self.world.itemWeights['seaweed']
                if self.inventory['seaweed'] <=0:
                    del self.inventory['seaweed']
            elif item == 'driftwood':
                self.inventory['driftwood'] -= 1
                self.inventorySize -= 1
                self.invWeight -= self.world.itemWeights['driftwood']
                if self.inventory['driftwood'] <=0:
                    del self.inventory['driftwood']
                return True
            elif item == 'seaweed':
                target.strength -= 2*target.level
                self.inventory['seaweed'] -= 1
                self.inventorySize -= 1
                self.invWeight -= self.world.itemWeights['seaweed']
                if self.inventory['seaweed'] <=0:
                    del self.inventory['seaweed']
                    
    def go(self, dir):
        if dir.lower() == 'north':
            if self.location.exits['north'] == None:
                print('You may not go north. Try again.')
                return False
            elif self.location.exits['north'].terrain == 'lake':
                if 'semiaquatic' not in self.abilities: # You have to have the "Semiaquatic" skill to access lake terrain
                    print('There is water in that direction, and you cannot swim. Try again.')
                    return False
                else:
                    self.location = self.location.exits['north']
                    return True
            else:
                self.going = 'north'
                self.location = self.location.exits['north']
                return True
        if dir.lower() == 'south':
            if self.location.exits['south'] == None:
                print('You may not go south. Try again.')
                return False
            elif self.location.exits['south'].terrain == 'lake':
                if 'semiaquatic' not in self.abilities:
                    print('There is water in that direction, and you cannot swim. Try again.')
                    return False
                else:
                    self.location = self.location.exits['south']
                    return True
            else:
                self.going = 'south'
                self.location = self.location.exits['south']
                return True
        if dir.lower() == 'east':
            if self.location.exits['east'] == None:
                print('You may not go east. Try again.')
                return False
            elif self.location.exits['east'].terrain == 'lake':
                if 'semiaquatic' not in self.abilities:
                    print('There is water in that direction, and you cannot swim. Try again.')
                    return False
                else:
                    self.location = self.location.exits['east']
                    return True
            else:
                self.going = 'east'
                self.location = self.location.exits['east']
                return True
        if dir.lower() == 'west':
            if self.location.exits['west'] == None:
                print('You may not go north. Try again.')
                return False
            elif self.location.exits['west'].terrain == 'lake':
                if 'semiaquatic' not in self.abilities:
                    print('There is water in that direction, and you cannot swim. Try again.')
                    return False
                else:
                    self.location = self.location.exits['west']
                    return True
            else:
                self.going = 'west'
                self.location = self.location.exits['west']
                return True
        else:
            print("Sorry, I don't understand. Choose north, south, east or west.")
            return False
        
              
    def stats(self):
        if self.diet == 'herbivore':
            print("You are an herbivore.")
        elif self.diet == 'carnivore':
            print("You are a carnivore.")
        print("Your location is " + str(self.location.coordinates))
        print("Hunger = " + str(self.hunger))
        print("Health = " + str(self.health))
        print('Type: \n \t "all stats" for all stats; \n \t "inventory" for abilities and inventory; \n \t "location" for details on location')
              
    def allstats(self):
        if self.diet == 'herbivore':
            print("You are an herbivore.")
        elif self.diet == 'carnivore':
            print("You are a carnivore.")
        #print("Location: " + str(self.location.coordinates))
        print("You may travel " + self.dirstring +".")
        print("You may travel " + str(self.inventorySize))
        print("Hunger = " + str(self.hunger))
        print("Health = " + str(self.health))
        print("Sociability = " + str(self.sociability))
        print("Speed = " + str(self.speed))
        print("Intelligence = " + str(self.intelligence))
        print("Sociability = " + str(self.sociability))
        print("Abilities = " + str(self.abilities))
        print("Inventory = " + str(self.inventory))
        print("Sociability = " + str(self.sociability))
        print("Inventory size = " + str(self.inventorySize))
        print("Inventory cap = " + str(self.inventoryCap))
        print("Inventory weight = " + str(self.invweight))
        print("Inventory max weight = " + str(self.maxinvweight))
        print("Friends: " + str(len(self.friends)))
        print("Defeated: " + str(self.defeated))
        
              
    def attack(self, creature):
        if self.location.creature == None:
            print('There is no creature here.')
            return
        else:
            fleeing = False
            defense = False
            while self.health > 0 and creature.health > 0:
                clear()
                print('Creature health: ' + str(creature.health))
                print('Creature strength: ' + str(creature.strength))
                print('Creature hostility: ' + str(creature.hostility))
                print()
                print('Health: ' + str(self.health))
                print('Strength: ' + str(self.strength))
                print('You may:')
                print('\t attack')
                if 'item use' in self.abilities:
                    print('\t use item')
                print('\t flee')
                choice = input('What will you do? ')
                choice = choice.lower()
                while choice not in 'attack' and choice not in 'flee' and 'item' not in choice:
                    if 'item use' in self.abilities:
                        print('Invalid command. Choose "attack," "item" or "flee."')
                    else:
                        print('Invalid command. Choose "attack" or "flee."')
                    choice = input('What will you do? ')
                while 'item' in choice.lower() and len(self.inventory) == 0:
                    print('Your inventory is empty!')
                    choice = input('What will you do? ')
                while 'item' in choice.lower() and 'item use' not in self.abilities == 0:
                    print('You can\'t do that!')
                    choice = input('What will you do? ')

                print()

                if self.speed >= creature.speed:
                    # If the player is faster, the player goes first
                    if choice.lower() in 'attack':
                        attackStrength = random.randint(self.strength // 2, self.strength)
                        print("You attack!")
                        print("The creature takes " + str(attackStrength) + " damage!")
                        print("The creature's hostility increases!")
                        creature.health -= self.strength
                        creature.hostility += 3
                    elif 'item' in choice.lower():
                        print("Items: ")
                        orderedInventory = asOrderedList(self.inventory)
                        for kvp in orderedInventory:
                            print('\t' + kvp[0] + ' x' + str(kvp[1]))
                        itemChoice = input('Pick an item. ')
                        if self.useBattleItem(itemChoice, creature):
                            defense = True
                    elif choice.lower() in 'flee':
                        print("You flee!")
                        break

                    creatureAttackChance = creature.hostility * .1
                    creatureChoice = random.random()
                    if creatureChoice < creature.fleeRate:
                        print("The creature flees!")
                        fleeing = True
                        break
                    elif creatureChoice < creatureAttackChance + creature.fleeRate:
                        creatureAttackStrength = random.randint(creature.strength // 2, creature.strength)
                        print("The creature attacks!")
                        if defense = True:
                            if random.random() < 0.5:
                                creatureAttackStrength = 0
                                print('Your driftwood barrier protects you!')
                        print("You take " + str(creatureAttackStrength) + " damage!")
                        self.health -= creatureAttackStrength
                    else:
                        print(random.choice(['The creature does nothing!', 'The creature awaits your next move.', 'The creature is watching you closely...']))

                else:
                    # If the creature is faster, the creature goes first
                    creatureAttackChance = creature.hostility * .1
                    creatureChoice = random.random()
                    if creatureChoice < creature.fleeRate:
                        print("The creature flees!")
                        fleeing = True
                        break
                    elif creatureChoice < creatureAttackChance + creature.fleeRate:
                        creatureAttackStrength = random.randint(creature.strength // 2, creature.strength)
                        print("The creature attacks!")
                        if defense = True:
                            if random.random() < 0.5:
                                creatureAttackStrength = 0
                                print('Your driftwood barrier protects you!')
                        print("You take " + str(creatureAttackStrength) + " damage!")
                        self.health -= creatureAttackStrength
                    else:
                        creatureChoice = random.choice(['The creature does nothing!', 'The creature awaits your next move.', 'The creature is watching you closely...'])

                    if choice.lower() in 'attack':
                        attackStrength = random.randint(self.strength // 2, self.strength)
                        print("You attack!")
                        print("The creature takes " + str(attackStrength) + " damage!")
                        print("The creature's hostility increases!")
                        creature.health -= self.strength
                        creature.hostility += 3
                    elif 'item' in choice.lower():
                        print("Items: ")
                        orderedInventory = asOrderedList(self.inventory)
                        for kvp in orderedInventory:
                            print('\t' + kvp[0] + ' x' + str(kvp[1]))
                        itemChoice = input('Pick an item. ')
                        if self.useBattleItem(itemChoice, creature):
                            defense = True
                    elif choice.lower() in 'flee':
                        print("You flee!")
                        break
                    if type(creatureChoice) == str:
                        # If the creature does nothing, we say so at the end of the turn.
                        print(creatureChoice)

                    print()

                    if self.ally != None:
                        if random.choice([True, False]):
                            if choice.lower() in 'attack':
                                attackStrength = random.randint(self.ally.strength // 2, self.ally.strength)
                                print("Your ally attacks!")
                                print("The creature takes " + str(attackStrength) + " damage!")
                                print("The creature's hostility increases!")
                                creature.health -= attackStrength
                                creature.hostility += 3

                input('Press enter to continue.')

            print()
            if fleeing == True:
                r = random.choice(self.world.squares)
                if creature in self.world.aquaticCreatures:
                    while r.creature != None and r.terrain != 'lake':
                        r.random.choice(self.world.squares)
                    r.creature = creature
                    creature.location = r
                    self.location.creature = None
                else:
                    while r.creature != None:
                        r = random.choice(self.world.squares)
                    r.creature = creature
                    creature.location = r
                    self.location.creature = None
            elif creature.health <= 0 and self.health > 0:
                print("You've defeated the creature!")
                print("You gain " + str(creature.experience) + " experience!")
                self.experience += creature.experience
                self.defeated += 1
                self.location.creature = None
                self.location.items['meat'] = random.randint(1,3)
                if random.random() < .15:
                    itemDrop = random.choice(self.world.possibleItems)
                    print('The creature dropped an item!')
                    if itemDrop in self.location.items:
                        self.location.items[itemDrop] += 1
                    else:
                        self.location.items[itemDrop] = 1
            elif self.health <= 0:
                self.die()
            return True

#######################################################################################

    def befriend(self, creature):
        if self.location.creature == None:
            print('There is no creature here.')
            return
        else:
            fleeing = False
            defense = False
            while self.health > 0 and creature.hostility > 0:
                clear()
                print('Creature health: ' + str(creature.health))
                print('Creature strength: ' + str(creature.strength))
                print('Creature hostility: ' + str(creature.hostility))
                print()
                print('Health: ' + str(self.health))
                print('Sociability: ' + str(self.sociability))
                print('You may:')
                print('\t befriend')
                if 'item use' in self.abilities:
                    print('\t use item')
                print('\t flee')
                choice = input('What will you do? ')
                while choice.lower() not in 'befriend' and choice.lower() not in 'flee' and 'item' not in choice.lower():
                    if 'item use' in self.abilities: #why say "not in 'befriend'?
                        print('Invalid command. Choose "befriend," "item" or "flee."')
                    else:
                        print('Invalid command. Choose "befriend" or "flee."')
                    choice = input('What will you do? ')
                if 'item' in choice.lower() and len(self.inventory) == 0:
                    print('Your inventory is empty!')
                    choice = input('What will you do? ')
                if 'item' in choice.lower() and 'item use' not in self.abilities == 0:
                    print('You can\'t do that!')
                    choice = input('What will you do? ')

                print()

                if self.speed >= creature.speed:
                    # If the player is faster, the player goes first
                    if choice.lower() in 'befriend' and choice.lower() != 'f':
                        befriendSuccess = random.randint(self.sociability // 2, self.sociability)
                        print("You try to befriend the creature!")
                        print("The creature's hostility decreases!")
                        creature.hostility -= befriendSuccess
                    elif 'item' in choice.lower():
                        print("Items: ")
                        orderedInventory = asOrderedList(self.inventory)
                        for kvp in orderedInventory:
                            print('\t' + kvp[0] + ' x' + str(kvp[1]))
                        itemChoice = input('Pick an item. ')
                        if self.useBattleItem(itemChoice, creature):
                            defense = True
                    elif choice.lower() in 'flee':
                        print("You flee!")
                        break

                    creatureAttackChance = creature.hostility * .1
                    creatureChoice = random.random()
                    if creatureChoice < creature.fleeRate:
                        print("The creature flees!")
                        fleeing = True
                        break
                    elif creatureChoice < creatureAttackChance + creature.fleeRate:
                        creatureAttackStrength = random.randint(creature.strength // 2, creature.strength)
                        print("The creature attacks!")
                        if defense = True:
                            if random.random() < 0.5:
                                creatureAttackStrength = 0
                                print('Your driftwood barrier protects you!')
                        print("You take " + str(creatureAttackStrength) + " damage!")
                        self.health -= creatureAttackStrength
                    else:
                        print(random.choice(['The creature does nothing!', 'The creature awaits your next move.', 'The creature is watching you closely...']))

                else:
                    # If the creature is faster, the creature goes first
                    creatureAttackChance = creature.hostility * .1
                    creatureChoice = random.random()
                    if creatureChoice < creature.fleeRate:
                        print("The creature flees!")
                        break
                        fleeing = True
                    elif creatureChoice < creatureAttackChance + creature.fleeRate:
                        creatureAttackStrength = random.randint(creature.strength // 2, creature.strength)
                        print("The creature attacks!")
                        if defense = True:
                            if random.random() < 0.5:
                                creatureAttackStrength = 0
                                print('Your driftwood barrier protects you!')
                        print("You take " + str(creatureAttackStrength) + " damage!")
                        self.health -= creatureAttackStrength
                    else:
                        creatureChoice = random.choice(['The creature does nothing!', 'The creature awaits your next move.', 'The creature is watching you closely...'])

                    if choice.lower() in 'befriend' and choice.lower() != 'f':
                        befriendSuccess = random.randint(self.sociability // 2, self.sociability)
                        print("You try to befriend the creature!")
                        print("The creature's hostility decreases!")
                        creature.hostility -= befriendSuccess
                    elif 'item' in choice.lower():
                        print("Items: ")
                        orderedInventory = asOrderedList(self.inventory)
                        for kvp in orderedInventory:
                            print('\t' + kvp[0] + ' x' + str(kvp[1]))
                        itemChoice = input('Pick an item. ')
                        if self.useBattleItem(itemChoice, creature):
                            defense = True
                    elif choice.lower() in 'flee':
                        print("You flee!")
                        break
                    if type(creatureChoice) == str:
                        # If the creature does nothing, we say so at the end of the turn.
                        print(creatureChoice)

                    print()

                    if self.ally != None:
                        if random.choice([True, False]):
                            if choice.lower() in 'befriend':
                                allySociability = 100 // self.ally.hostility
                                if allySociability < 0:
                                    allySociability = 0
                                befriendSuccess = random.randint(allySociability // 2, allySociability)
                                print("Your ally helps befriend the creature!")
                                print("The creature's hostility decreases!")
                                creature.hostility -= befriendSuccess
                input('Press enter to continue.')

            print()
            if fleeing == True:
                r = random.choice(self.world.squares)
                if creature in self.world.aquaticCreatures:
                    while r.creature != None and r.terrain != 'lake':
                        r.random.choice(self.world.squares)
                    r.creature = creature
                    creature.location = r
                    self.location.creature = None
                else:
                    while r.creature != None:
                        r = random.choice(self.world.squares)
                    r.creature = creature
                    creature.location = r
                    self.location.creature = None
            elif creature.hostility <= 0 and self.health > 0:
                print("You've befriended the creature!")
                print("You gain " + str(creature.experience) + " experience!")
                self.experience += creature.experience
                self.friends.append(creature)
                creature.befriended = True
                if random.random() < .15:
                    itemDrop = random.choice(self.world.possibleItems)
                    print('The creature dropped an item!')
                    if itemDrop in self.location.items:
                        self.location.items[itemDrop] += 1
                    else:
                        self.location.items[itemDrop] = 1
            elif self.health <= 0:
                self.die()
            return True

#######################################################################################

    def flexibleResponse(self, creature):
        if self.location.creature == None:
            print('There is no creature here.')
            return
        else:
            fleeing = False
            defense = False
            while self.health > 0 and (creature.hostility > 0 or creature.health > 0):
                clear()
                print('Creature health: ' + str(creature.health))
                print('Creature strength: ' + str(creature.strength))
                print('Creature hostility: ' + str(creature.hostility))
                print()
                print('Health: ' + str(self.health))
                print('Strength: ' + str(self.strength))
                print('Sociability: ' + str(self.sociability))
                print('You may:')
                print('\t attack')
                print('\t befriend')
                if 'item use' in self.abilities:
                    print('\t use item')
                print('\t flee')
                choice = input('What will you do? ')
                while choice.lower() not in 'attack' and choice.lower() not in 'befriend' and choice.lower() not in 'flee' and 'item' not in choice.lower():
                    if 'item use' in self.abilities:
                        print('Invalid command. Choose "attack," "befriend," "item" or "flee."')
                    else:
                        print('Invalid command. Choose "attack," "befriend," or "flee."')
                    choice = input('What will you do? ')
                if 'item' in choice.lower() and len(self.inventory) == 0:
                    print('Your inventory is empty!')
                    choice = input('What will you do? ')
                if 'item' in choice.lower() and 'item use' not in self.abilities == 0:
                    print('You can\'t do that!')
                    choice = input('What will you do? ')

                print()

                if self.speed >= creature.speed:
                    # If the player is faster, the player goes first
                    if choice.lower() in 'attack':
                        attackStrength = random.randint(self.strength // 2, self.strength)
                        print("You attack!")
                        print("The creature takes " + str(attackStrength) + " damage!")
                        print("The creature's hostility increases!")
                        creature.health -= attackStrength
                        creature.hostility += 3
                    elif choice.lower() in 'befriend' and choice.lower() != 'f':
                        befriendSuccess = random.randint(self.sociability // 2, self.sociability)
                        print("You try to befriend the creature!")
                        print("The creature's hostility decreases!")
                        creature.hostility -= befriendSuccess
                    elif 'item' in choice.lower():
                        print("Items: ")
                        orderedInventory = asOrderedList(self.inventory)
                        for kvp in orderedInventory:
                            print('\t' + kvp[0] + ' x' + str(kvp[1]))
                        itemChoice = input('Pick an item. ')
                        if self.useBattleItem(itemChoice, creature):
                            defense = True
                    elif choice.lower() in 'flee':
                        print("You flee!")
                        break

                    creatureAttackChance = creature.hostility * .1
                    creatureChoice = random.random()
                    if creatureChoice < creature.fleeRate:
                        print("The creature flees!")
                        fleeing = True
                        break
                    elif creatureChoice < creatureAttackChance + creature.fleeRate:
                        creatureAttackStrength = random.randint(creature.strength // 2, creature.strength)
                        print("The creature attacks!")
                        if defense = True:
                            if random.random() < 0.5:
                                creatureAttackStrength = 0
                                print('Your driftwood barrier protects you!')
                        print("You take " + str(creatureAttackStrength) + " damage!")
                        self.health -= creatureAttackStrength
                    else:
                        print(random.choice(['The creature does nothing!', 'The creature awaits your next move.', 'The creature is watching you closely...']))

                else:
                    # If the creature is faster, the creature goes first
                    creatureAttackChance = creature.hostility * .1
                    creatureChoice = random.random()
                    if creatureChoice < creature.fleeRate:
                        print("The creature flees!")
                        fleeing = True
                        break
                    elif creatureChoice < creatureAttackChance + creature.fleeRate:
                        creatureAttackStrength = random.randint(creature.strength // 2, creature.strength)
                        print("The creature attacks!")
                        if defense = True:
                            if random.random() < 0.5:
                                creatureAttackStrength = 0
                                print('Your driftwood barrier protects you!')
                        print("You take " + str(creatureAttackStrength) + " damage!")
                        self.health -= creatureAttackStrength
                    else:
                        creatureChoice = random.choice(['The creature does nothing!', 'The creature awaits your next move.', 'The creature is watching you closely...'])

                    if choice.lower() in 'attack':
                        attackStrength = random.randint(self.strength // 2, self.strength)
                        print("You attack!")
                        print("The creature takes " + str(attackStrength) + " damage!")
                        print("The creature's hostility increases!")
                        creature.health -= attackStrength
                        creature.hostility += 3
                    elif choice.lower() in 'befriend' and choice.lower() != 'f':
                        befriendSuccess = random.randint(self.sociability // 2, self.sociability)
                        print("You try to befriend the creature!")
                        print("The creature's hostility decreases!")
                        creature.hostility -= befriendSuccess
                    elif 'item' in choice.lower():
                        print("Items: ")
                        orderedInventory = asOrderedList(self.inventory)
                        for kvp in orderedInventory:
                            print('\t' + kvp[0] + ' x' + str(kvp[1]))
                        itemChoice = input('Pick an item. ')
                        if self.useBattleItem(itemChoice, creature):
                            defense = True
                    elif choice.lower() in 'flee':
                        print("You flee!")
                        break
                    if type(creatureChoice) == str:
                        # If the creature does nothing, we say so at the end of the turn.
                        print(creatureChoice)

                    print()

                    if self.ally != None:
                        if random.choice([True, False]):
                            if choice.lower() in 'attack':
                                attackStrength = random.randint(self.ally.strength // 2, self.ally.strength)
                                print("Your ally attacks!")
                                print("The creature takes " + str(attackStrength) + " damage!")
                                print("The creature's hostility increases!")
                                creature.health -= attackStrength
                                creature.hostility += 3
                            elif choice.lower() in 'befriend':
                                allySociability = 100 // self.ally.hostility
                                if allySociability < 0:
                                    allySociability = 0
                                befriendSuccess = random.randint(allySociability // 2, allySociability)
                                print("Your ally helps befriend the creature!")
                                print("The creature's hostility decreases!")
                                creature.hostility -= befriendSuccess
                input('Press enter to continue.')

            print()
            if fleeing == True:
                r = random.choice(self.world.squares)
                if creature in self.world.aquaticCreatures:
                    while r.creature != None and r.terrain != 'lake':
                        r.random.choice(self.world.squares)
                    r.creature = creature
                    creature.location = r
                    self.location.creature = None
                else:
                    while r.creature != None:
                        r = random.choice(self.world.squares)
                    r.creature = creature
                    creature.location = r
                    self.location.creature = None
            elif creature.health <= 0 and self.health > 0:
                print("You've defeated the creature!")
                print("You gain " + str(creature.experience) + " experience!")
                self.experience += creature.experience
                self.defeated += 1
                self.location.creature = None
                self.location.items['meat'] = random.randint(1,3)
                if random.random() < .15:
                    if self.location.terrain == 'lake':
                        itemDrop = random.choice(self.world.waterItems)
                    else:
                        itemDrop = random.choice(self.world.landItems)
                    print('The creature dropped an item!')
                    if itemDrop in self.location.items:
                        self.location.items[itemDrop] += 1
                    else:
                        self.location.items[itemDrop] = 1
                input()
            elif creature.hostility <= 0 and self.health > 0:
                print("You've befriended the creature!")
                print("You gain " + str(creature.experience) + " experience!")
                self.experience += creature.experience
                self.friends.append(creature)
                creature.befriended = True
                if random.random() < .15:
                    if self.location.terrain == 'lake':
                        itemDrop = random.choice(self.world.waterItems)
                    else:
                        itemDrop = random.choice(self.world.landItems)
                    print('The creature dropped an item!')
                    if itemDrop in self.location.items:
                        self.location.items[itemDrop] += 1
                    else:
                        self.location.items[itemDrop] = 1
            elif self.health <= 0:
                self.die()
            return True

    def recruit(self):
        if self.location.creature == None:
            print('There is no creature here for you to befriend!')
        elif self.ally != None:
            print('You need to dismiss your ally before you recruit a new one!')
        else:
            if self.location.creature in self.friends:
                self.ally = self.location.creature
                print('You have allied your friend the ' + self.ally.name + '! Your ally will follow you around and fight with you.')
            else:
                print('You must befriend a creature before it will be your ally!')
                
                
    def locationDets(self):
        print('Location coordinates: ' + str(self.location.coordinates))
        print('Terrain: ' + self.location.terrain)
        print('Weather: ' + self.location.weather)
        self.location.availableDirs()
        
