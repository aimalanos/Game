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
        self.name = input("What is your creature's name? ")
        self.diet = input("Is your creature a carnivore or an herbivore? ").lower() # lower() puts it in lowercase, which eliminates the problem of whether the player types with capital or lowercase letters
        while self.diet not in 'carnivore' and self.diet not in 'herbivore':
            self.diet = input('Invalid response. Choose "carnivore" or "herbivore." ')
        if self.diet in 'carnivore':
            self.diet = 'carnivore'
        elif self.diet in 'herbivore':
            self.diet = 'herbivore'
        w.add_player(self)
        self.world = w
        self.location = random.choice(self.world.squares)
        self.home = self.location # The player's home base will be their starting location.
        self.alive = True
        self.hunger = 100 # If self.hunger reaches 0, the player's health will decrease at each update.
        self.maxHealth, self.health = 50, 50
        self.maxStrength, self.strength = 5, 5
        self.maxSociability, self.sociability = 5, 5
        self.maxSpeed, self.speed = 5, 5
        self.healthLoss = 2
        self.hungerLoss = 20
        self.speedPenalty = 1
        self.socPenalty = 1
        self.intelligence = 0
        self.experience = 0
        self.abilities = []
#         self.startItems = ['matches','flashlight']
        self.inventory = {}
#         self.startInv()
        self.inventorySize = 0
        self.inventoryCap = 10
        self.invweight = 0
        self.maxinvweight = 20
        self.availabledirs = []
        self.dirstring = ''
        self.defeated = 0
        self.allies = []
        self.ally = None
        self.m = 0

    def startInv(self): #function to give the player a few starting items
        l = []
        for i in range(3):
            l.append(random.choice(self.startItems))
        for elem in l:
            if elem in self.inventory:
                self.inventory[elem] += 1
            else:
                self.inventory[elem] = 1
        if 'matches' in self.inventory:
            self.inventory['matches'] = 4
            
    def update(self):
        self.dirstring = ''
        for elem in self.availabledirs:
            if self.dirstring == '':
                self.dirstring = elem
            else:
                self.dirstring += ', ' + elem
                
        self.healthLoss = 2
        self.hungerLoss = 15
        self.speedPenalty = 1
        self.socPenalty = 1
        
        if self.location.terrain == "desert":
            self.hungerLoss *= 2
        elif self.location.terrain == "mountainous":
            self.speedPenalty *= 2
        elif self.location.terrain == "tundra":
            self.healthLoss *= 2
        elif self.location.terrain == "grassy":
            self.healthLoss = 1
            self.hungerLoss = 10
            self.speedPenalty = 0
            self.socPenalty = 0
            
        if self.location.weather == "rainy":
            self.speedPenalty *= 3
        elif self.location.weather == "hailing":
            self.healthLoss *= 2
        elif self.location.weather == "snowy":
            self.socPenalty *= 2
        elif self.location.weather == "drought":
            self.hungerLoss *= 2

        if self.location == self.home:
            self.health += self.maxHealth // 2
            if self.health > self.maxHealth:
                self.health = self.maxHealth
        else: #no health loss at home
            self.health -= self.healthLoss
        if self.health <= 0:
            self.die()
            
        if self.hunger > 0:
            if 'Improved metabolism' in self.abilities:
                self.hunger -= 5
            self.hunger -= self.hungerLoss
            if self.hunger < 0:
                self.hunger = 0
        elif self.hunger == 0:
            r = random.randint(0,3) #player will randomly take damage to health, strength, sociability, speed, or intelligence
            if r == 0:
                self.health -= self.health//10
            elif r == 1:
                self.strength -= self.strength//10
            elif r == 2:
                self.sociability -= self.sociability//10
            elif r == 3:
                self.speed -= self.speed//10
        if self.hunger < 0:
            self.hunger = 0
            
        self.availabledirs = []
        for exit in self.location.exits:
            if exit != None:
                self.availabledirs.append(exit)
                
        if 'meat' in self.inventory:
            self.m += 1
            if self.m == 4:
                del self.inventory['fruit']
                del self.inventory['meat']
                self.m = 0
                print('Oh no! You carried meat in your bag for too long. All of your food has gone rotten.')
        else:
            self.m = 0
            
    def fillStats(self, n):
        self.health += self.maxHealth // n
        if self.health > self.maxHealth:
            self.health = self.maxHealth
        self.strength += self.maxStrength // n
        if self.strength > self.maxStrength:
            self.strength = self.maxStrength
        self.sociability += self.maxSociability // n
        if self.sociability > self.maxSociability:
            self.sociability = self.maxSociability
        self.speed += self.maxSpeed // n
        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
        
    def die(self):
        self.alive = False
        
    def eat(self, food):
        if food == 'fruit':
            if self.diet == 'herbivore' or self.diet == 'omnivore':
                if 'fruit' in self.location.items:
                    self.fillStats(2)
                    self.hunger += 25
                    self.location.items['fruit'] -= 1
                    if self.location.items['fruit'] <= 0:
                        del self.location.items['fruit']
                elif 'fruit' in self.inventory:
                    self.fillStats(2)
                    self.hunger += 25
                    self.inventory['fruit'] -= 1
                    self.inventorySize -= 1
                    self.invweight -= 1
                    if self.inventory['fruit'] <= 0:
                        del self.inventory['fruit']
                print('You eat the fruit.')
                input()
                return True
            else:
                return False
        elif food == 'meat':
            if self.diet == 'carnivore' or self.diet == 'omnivore':
                if 'meat' in self.location.items:
                    self.fillStats(1)
                    self.hunger += 25
                    self.location.items['meat'] -= 1
                    if self.location.items['meat'] <= 0:
                        del self.location.items['meat']
                elif 'meat' in self.inventory:
                    self.fillStats(1)
                    self.hunger += 25
                    self.inventory['meat'] -= 1
                    self.inventorySize -= 1
                    self.invweight -= 1
                    if self.inventory['meat'] <= 0:
                        del self.inventory['meat']
                print('You eat the meat.')
                input()
                return True
            else:
                return False
        
    def pickup(self, item):
        f = 0
        if item == 'fruit':
            f = 1
        elif item == 'stinkfruit':
            f = 2
        elif item == 'sticky sap':
            f = 5
        elif item == 'poison berries':
            f = 5
        elif item == 'big leaf':
            f = 3
        elif item == 'healing salve':
            f = 4
        elif item == 'flowers':
            f = 1
        elif item == 'meat':
            f = 1
        if self.inventorySize < self.inventoryCap and self.invweight <= self.maxinvweight + f:
            if item in self.location.items:
                if item in self.inventory:
                    self.inventory[item] += 1
                    self.invweight += f
                else:
                    self.inventory[item] = 1
                    self.invweight += f
                self.location.items[item] -= 1
                if self.location.items[item] <= 0:
                    del self.location.items[item]
                    self.invweight += f
                print('You pick up the ' + item + '.')
            return True
        else:
            return f
        
    def drop(self,item):
        f = 0
        if item == 'fruit':
            f = 1
        elif item == 'stinkfruit':
            f = 2
        elif item == 'sticky sap':
            f = 5
        elif item == 'poison berries':
            f = 5
        elif item == 'big leaf':
            f = 3
        elif item == 'healing salve':
            f = 4
        elif item == 'flowers':
            f = 1
        elif item == 'meat':
            f = 1
        if item in self.inventory:
            if item in self.location.items:
                self.location.items[item] += 1
            else:
                self.location.items[item] = 1
            self.inventory[item] -= 1
            self.invweight -= f
            if self.inventory[item] <= 0:
                del self.inventory[item]
            print('You drop the ' + item + '.')
        else:
            print('There is no such item in your inventory. Try again.')
                
    def inspect(self, item):
        if item in self.location.items or item in self.inventory:
            if item == 'stinkfruit':
                print('A hard, smelly fruit. Use it during an encounter to make the other creature flee.')
            elif item == 'sticky sap':
                print("Sticky sap from a tree. Use it during an encounter to decrease the other creature's speed.")
            elif item == 'poison berries':
                print("Poisonous berries. Use them during an encounter to decrease the other creature's health and strength.")
            elif item == 'big leaf':
                print('A large, surprisingly sturdy leaf. It could protect you from the weather.')
            elif item == 'healing salve':
                print('A healing salve from a plant. Use it to restore your stats.')
            elif item == 'flowers':
                print("Pretty flowers. Use them during an encounter to decrease the other creature's hostility.")
            elif item == 'fruit':
                print('A fruit. If you are herbivore or omnivore, then eating this will reduce hunger and restore your stats.')
            elif item == 'meat':
                print('A piece of meat. If you are carnivore or omnivore, then eating this will reduce hunger and restore your stats.')
        elif item == 'creature':
            creat = self.location.creature
            print("The creature is a " + creat.name + '!')
            print("It has " + str(creat.health) + " health, " + str(creat.speed) + " speed, " + str(creat.strength) + " strength, and " + str(creat.hostility) + " hostility.")
                    
    def useItem(self, item):
        if item in self.inventory:
            print('You use the ' + item + '.')
            if item == 'fruit':
                if self.diet == 'herbivore' or self.diet == 'omnivore':
                    a = self.eat(item)
            elif item == 'meat':
                if self.diet == 'herbivore' or self.diet == 'omnivore':
                    self.eat(item)
            elif item == 'healing salve':
                print('All your stats have been restored!')
                self.fillStats()
                self.inventory['healing salve'] -= 1
                self.inventorySize -= 1
                self.invweight -= 4
                if self.inventory['healing salve'] <= 0:
                    del self.inventory['healing salve']
            elif item == 'big leaf':
                print('You are now protected from the weather!')
                self.location.weather = 'clear'
                self.inventory['big leaf'] -= 1
                self.inventorySize -= 1
                self.invweight -= 3
                if self.inventory['big leaf'] <= 0:
                    del self.inventory['big leaf']
            else:
                print("Now's not the time to use that!")
                return False
            return True
        print("There's no item by that name in your inventory.")
        return False
                    
    def useBattleItem(self, item, target):
        if item in self.inventory:
            if item == 'stinkfruit':
               # break # I have no idea if this will work #what were you trying to do?
                self.inventory['stinkfruit'] -= 1
                self.inventorySize -= 1
                if self.inventory['stinkfruit'] <= 0:
                    del self.inventory['stinkfruit']
            elif item == 'sticky sap':
                target.speed -= target.speed // 4
                self.inventory['sticky sap'] -= 1
                self.inventorySize -= 1
                if self.inventory['sticky sap'] <= 0:
                    del self.inventory['sticky sap']
            elif item == 'poison berries':
                target.health -= target.health // 5
                target.strength -= target.strength // 5
                self.inventory['poison berries'] -= 1
                self.inventorySize -= 1
                if self.inventory['poison berries'] <= 0:
                    del self.inventory['poison berries']
            elif item == 'healing salve':
                self.fillStats()
                self.inventory['healing salve'] -= 1
                self.inventorySize -= 1
                if self.inventory['healing salve'] <=0:
                    del self.inventory['healing salve']
            elif item == 'flowers':
                target.hostility -= target.hostility // 3
                self.inventory['flowers'] -= 1
                self.inventorySize -= 1
                if self.inventory['flowers'] <=0:
                    del self.inventory['flowers']
                    
    
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
        print("Allies: " + str(len(self.allies)))
        print("Defeated: " + str(self.defeated))
        
              
    def attack(self, creature):
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
                    creature.health -= self.strength
                    creature.hostility += 3
                elif 'item' in choice.lower():
                    print("Items: ")
                    orderedInventory = asOrderedList(self.inventory)
                    for kvp in orderedInventory:
                        print('\t' + kvp[0] + ' x' + str(kvp[1]))
                    itemChoice = input('Pick an item. ')
                    self.useBattleItem('item')
                elif choice.lower() in 'flee':
                    print("You flee!")
                    break

                creatureAttackChance = creature.hostility * .1
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
                creatureAttackChance = creature.hostility * .1
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
                    self.useBattleItem('item')
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

                input()

        if creature.health <= 0 and self.health > 0:
            print("You gain " + str(creature.experience) + " experience!")
            self.experience += creature.experience
            self.defeated += 1
            self.location.creature = False
            self.location.items['meat'] = random.randint(1,3)
            if random.random() < .15:
                itemDrop = random.choice(self.world.possibleItems)
                print('The creature dropped an item!')
                if itemDrop in self.location.items:
                    self.location.items[itemDrop] += 1
                else:
                    self.location.items[itemDrop] = 1
            input()
        elif self.health <= 0:
            self.die()


    def befriend(self, creature):
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
                if 'item use' in self.abilities:
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
                    self.useBattleItem('item')
                elif choice.lower() in 'flee':
                    print("You flee!")
                    break

                creatureAttackChance = creature.hostility * .1
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
                creatureAttackChance = creature.hostility * .1
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
                    self.useBattleItem('item')
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
                input()

        if creature.hostility <= 0 and self.health > 0:
            print("You gain " + str(creature.experience) + " experience!")
            self.experience += creature.experience
            self.allies.append(creature)
            creature.befriended = True
            if random.random() < .15:
                itemDrop = random.choice(self.world.possibleItems)
                print('The creature dropped an item!')
                if itemDrop in self.location.items:
                    self.location.items[itemDrop] += 1
                else:
                    self.location.items[itemDrop] = 1
            input()
        elif self.health <= 0:
            self.die()



    def flexibleResponse(self, creature):
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
                    self.useBattleItem('item')
                elif choice.lower() in 'flee':
                    print("You flee!")
                    break

                creatureAttackChance = creature.hostility * .1
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
                creatureAttackChance = creature.hostility * .1
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
                    self.useBattleItem('item')
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
                input()

        if creature.health <= 0 and self.health > 0:
            print("You gain " + str(creature.experience) + " experience!")
            self.experience += creature.experience
            self.defeated += 1
            self.location.creature = False
            self.location.items['meat'] = random.randint(1,3)
            if random.random() < .15:
                itemDrop = random.choice(self.world.possibleItems)
                print('The creature dropped an item!')
                if itemDrop in self.location.items:
                    self.location.items[itemDrop] += 1
                else:
                    self.location.items[itemDrop] = 1
            input()
        elif creature.hostility <= 0 and self.health > 0:
            print("You gain " + str(creature.experience) + " experience!")
            self.experience += creature.experience
            self.allies.append(creature)
            creature.befriended = True
            if random.random() < .15:
                itemDrop = random.choice(self.world.possibleItems)
                print('The creature dropped an item!')
                if itemDrop in self.location.items:
                    self.location.items[itemDrop] += 1
                else:
                    self.location.items[itemDrop] = 1
            input()
        elif self.health <= 0:
            self.die()

    def ally(self, creature):
        if creature in self.allied:
            self.ally = creature
            return True
        else:
            return False
                
                
    def locationDets(self):
        print('Location coordinates: ' + str(self.location.coordinates))
        print('Terrain: ' + self.location.terrain)
        print('Weather: ' + self.location.weather)
        print('You may travel: ' + self.location.listdirs())
        
