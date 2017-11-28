from World import World
from Square import Square
from Player import Player
from Creature import Creature
import os
import random

def me():
    p.stats()

def help():
    print("Type 'me' for player stats.")
    print("You may travel" + str(p.availabledirs) + "\n")
    
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def asOrderedList(d):
    ordered = []
    for key in d:
        ordered.append([key, d[key]])
        ordered.sort()
    return ordered
    
def printSituation():
    print("Turn " + str(w.turn_count))
    print()
    print("Your coordinates are " + str(p.location.coordinates) + ".")
    print("The weather is " + w.weather + ".")
    print("The terrain is " + p.location.terrain + ".")
    if p.location.creature:
        print("There is a creature here.")
    else:
        print("You are alone here.")
    if len(p.location.items) > 0:
        print('There are the following items:')
        orderedInventory = asOrderedList(p.location.items)
        for kvp in orderedInventory: # For the key-value pairs in the ordered inventory...
            if kvp[1] > 0: # if there are actually items...
                print('\t' + kvp[0] + ': ' + str(kvp[1]))
    else:
        print("There is nothing of use to you here.")
    print()
    print("Health: " + str(p.health))
    
def victory(self):
    clear()
    if 'fire' in self.player.inventory:
        print('You have discovered fire! You have successfully set yourself on the path to civilization! Congratulations!')
    elif self.player.defeated >= 30:
        print('You have defeated enough enemies that you are now at the top of the food chain! Congratulations!')
    elif self.player.allies >= 30:
        print('You have enough allies to be protected wherever you go! That means you win! Congratulations!')
    # We should put some fireworks in here
                      
def gameOver(w):
    playing = False
    print('GAME OVER')
    print()
    if w.turn_count > 200:
        print('You took too long! Another creature has become dominant!')
    elif not w.player.alive:
        print('Your creature has died!')
    print()
    print('Better luck next time!')
          
def evolve():
    #clear()
    print('Health increase: 5 exp')
    print('Stomach size increase: 5 exp')
    print('Strength increase: 5 exp')
    print('Sociability increase: 5 exp')
    print('Speed increase: 5 exp')
    print('Intelligence increase: 5 exp')
    if 'Metabolism increase' not in p.abilities:
        print('Metabolism increase – hunger increase more slowly: 10 exp')
    if 'Fat reserves' not in p.abilities:
        print('Fat reserves – reduced penalty when starving: 10 exp')
    if 'Semiaquatic' not in p.abilities:
        print('Semiaquatic – access watery terrain: 10 exp')
    if p.intelligence >= 8 and 'Item use' not in p.abilities:
        print('Tool use: 10 exp')
    if p.intelligence >= 13 and 'Item use' in p.abilities and 'Flexible responding' not in p.abilities:
        print('Flexible responding – more options when you engage with other creatures: 20 exp') # Idk, maybe players will be able to change whether they want to socialize or attack. Also, I just thought that if the player attacks a creature, then the creature's hostility should go up
    if p.intelligence >= 20 and 'Flexible responding' in p.abilities:
        print('Fire: 30 exp')
    print('Go back.')
    print()
    transactionCompleted = False
    while not transactionCompleted:
        choice = input('What would you like to improve? ')
        if choice.lower() in 'health increase':
            if p.experience >= 5:
                p.maxHealth += 5
                self.experience -= 5
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'stomach size increase':
            if p.experience >= 5:
                p.maxHunger += 5
                self.experience -= 5
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'strength increase':
            if p.experience >= 5:
                p.maxStrength += 3
                self.experience -= 5
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'sociability increase':
            if p.experience >= 5:
                p.maxSociability += 3
                self.experience -= 5
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'speed increase':
            if p.experience >= 5:
                p.maxSpeed += 3
                self.experience -= 5
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'intelligence increase':
            if p.experience >= 5:
                p.intelligence += 4
                self.experience -= 5
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'metabolism increase':
            if p.experience >= 15:
                p.abilities.append('Improved metabolism') # Will implement this later
                self.experience -= 15
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'fat reserves':
            if p.experience >= 15:
                p.abilities.append('Fat reserves') # Will implement this later
                self.experience -= 15
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'semiaquatic':
            if p.experience >= 15:
                p.abilities.append('Semiaquatic') # Will implement this later
                self.experience -= 15
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'item use':
            if p.experience >= 15:
                p.abilities.append('Item use') # Will implement this later
                self.experience -= 15
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'flexible responding':
            if p.experience >= 30:
                p.abilities.append('Fat reserves') # Will implement this later
                self.experience -= 30
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'fire':
            if p.experience >= 50:
                victory()
            else:
                ('Not enough experience. Try again.')

clear()

playing = True
w = World()
mapx = 4
mapy = 4
w.makeMap(mapx,mapy)
# for i in range(-mapx,mapx+1): # Isn't make map doing the same thing as these loops?
#     for j in range(-mapy, mapy+1):
#         Square(w, i, j)
for i in range(0,28):
    r = random.choice(w.squares)
    if not r.creature:
        r.creature = Creature(r, 1)
for i in range(0,28):
    r = random.choice(w.squares)
    if not r.creature:
        r.creature = Creature(r, 2)
for i in range(0,28):
    r = random.choice(w.squares)
    if not r.creature:
        r.creature = Creature(r, 3)
for i in range(0,60):
    r = random.choice(w.squares)
    if 'fruit' in r.items:
        r.items['fruit'] += 1
    else:
        r.items['fruit'] = 1
for i in range(0,50):
    r = random.choice(w.squares)
    rItem = random.choice(w.possibleItems)
    if 'rItem' in r.items:
        r.items[rItem] += 1
    else:
        r.items[rItem] = 1

                      
p = Player(w)       
clear()

while playing and p.alive:
    #clear()
    printSituation()
    commandSuccess = False
    timePasses = False
    while not commandSuccess:
        commandSuccess = True
        command = input('What will you do? ').lower()
        commandWords = command.split()
        if command == 'help':
            clear()
            help()
        elif command == 'me':
            clear()
            me()
        elif command == 'all stats':
            clear()
            p.allstats()
        elif 'north' in command:
            if p.location.exits['north'] == None:
                print('You may not go north. Try again.')
                commandSuccess = False
            elif p.location.exits['north'].terrain == 'water':
                if 'semiaquatic' not in player.abilities:
                    print('There is water in that direction, and you cannot swim. Try again.')
                    commandSuccess = False
            else:
                p.north()
                timePasses = True
        elif 'south' in command:
            if p.location.exits['south'] == None:
                print('You may not go south. Try again.')
                commandSuccess = False
            elif p.location.exits['south'].terrain == 'water':
                if 'semiaquatic' not in player.abilities:
                    print('There is water in that direction, and you cannot swim. Try again.')
                    commandSuccess = False
            else:
                p.south()
                timePasses = True
        elif 'west' in command:
            if p.location.exits['west'] == None:
                print('You may not go west. Try again.')
                commandSuccess = False
            elif p.location.exits['west'].terrain == 'water':
                if 'semiaquatic' not in player.abilities:
                    print('There is water in that direction, and you cannot swim. Try again.')
                    commandSuccess = False
            else:
                p.west()
                timePasses = True
        elif 'east' in command:
            if p.location.exits['east'] == None:
                print('You may not go east. Try again.')
                commandSuccess = False
            elif p.location.exits['east'].terrain == 'water':
                if 'semiaquatic' not in player.abilities:
                    print('There is water in that direction, and you cannot swim. Try again.')
                    commandSuccess = False
            else:
                p.east()
                timePasses = True
        elif 'pickup' in command:
            if len(commandWords) == 3:
                item = commandWords[1] + ' ' + commandWords[2]
            else:
                item = commandWords[1]
            if item in p.location.items:
                s = p.pickup(item)
            else:
                print('There is no such item. Try again.')
                commandSuccess = False
            if not s:
                print("This item is too heavy for you to pick up! Leave it behind or free up " + str(s) + " kg in your inventory. ")
        elif 'drop' in command:
            if len(commandWords) == 3:
                item = commandWords[1] + ' ' + commandWords[2]
            else:
                item = commandWords[1]
            if item in p.inventory:
                p.drop(item)
            else:
                print('You don\'t have any such item. Try again.')
                commandSuccess = False
        elif 'inventory' in command:
            clear()
            inv = ''
            for elem in self.inventory:
                inv += elem
            for elem in self.abilities:
                abi += elem
            print('Inventory: ' + inv + '\n Abilities: ' + abi)
            input('Press enter to continue.')
        elif 'eat' in command:
            if len(commandWords) == 2:
                food = commandWords[1]
            #else:
                #food = commandWords[1] + ' ' + commandWords[2]
            if food in p.location.items:
                if not p.eat(food):
                    commandSuccess = False
                    print('You can\'t eat that! Bleh!')
        elif 'wait' in command:
            if len(commandWords) == 3:
                if commandWords[0] == 'wait' and commandWords[2] == 'turns' or commandWords[2] == 'turn':
                    i = int(commandWords[1])
            elif len(commandWords) == 1:
                i = 1
            j = 1
            while j <= i:
                w.update()
                j += 1
        else:
            print('Sorry, I don\'t understand. Type "options" for available options. ')
            command = input('What will you do? ')
            printSituation()
            commandSuccess = False
    if timePasses:
        w.update()
        if w.turn_count > 200:
            gameOver(w)
if not p.alive:
    gameOver(w)
