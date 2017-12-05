from World import World
from Square import Square
from Player import Player
from Player import asOrderedList
from Creature import Creature
import os
import random

def help(p):
    clear()
    print('Use the "me" command to see an abbridged list of stats.')
    print('Use the "allstats" command to see a full list of stats.')
    print('Use the "inventory" command to see your inventory.')
    print('Use the "go __" command to move. Don\'t forget to say which direction!')
    print('Use the "pickup __" command to pick up an item.')
    print('Use the "drop __" command to drop an item.')
    if 'Item use' in p.abilities:
        print('Use the "use __" command to use an item.')
    print('Use the "inspect __" command to learn more about your environment.')
    print('Use the "attack" command to attack a creature.')
    print('Use the "befriend" command to try to befriend a creature.')
    print('Use the "ally" command to make a befriended creature your ally.'
    print('Use the "dismiss" command to dismiss your ally.')
    print('Use the "evolve" command to purchase upgrades for your creature.')
    print('Use the "wait __ turn(s)" command to wait.')
    print('Use the "abbreviate __ as __" command to make shortcuts for commands.')
    print('Use the "quit" command to leave the game.')
    
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def showInventory(p):
    clear()
    print('Your inventory contains the following items:')
    orderedInventory = asOrderedList(p.inventory)
    for kvp in orderedInventory:
        print('\t' + kvp[0] + ' x' + str(kvp[1]))
    
def printSituation(w, p):
    wc = ''
    if w.weather == 'rainy':
        wc = 'It slows you down.'
    elif w.weather == 'hailing':
        wc = 'You are being buffeted by hail.'
    elif w.weather == 'snowy':
        wc = 'The poor weather reduces your sociability.'
    elif w.weather == 'drought':
        wc = 'You are getting hungry very quickly.'
    tc = ''
    if p.location.terrain == 'mountainous':
        tc = 'The difficult terrain slows you down.'
    elif p.location.terrain == 'desert':
        tc = 'You are getting hungry very quickly.'
    elif p.location.terrain == 'tundra':
        tc = 'The harsh conditions damage your health!'
    elif p.location.terrain == 'forest':
        tc = 'It\'s very nice here.'
    print("Turn " + str(w.turn_count))
    print()
    print("Your coordinates are " + str(p.location.coordinates) + ".")
    print("The weather is " + w.weather + ". " + wc)
    print("The terrain is " + p.location.terrain + ". " + tc)
    if p.location.creature != None:
        if (p.ally != None and p.ally.location == p.location) or p.ally == None:
            print("There is a creature here. It is a " + str(p.location.creature.name) + ".")
    else:
        print("You are alone here.")
    if len(p.location.items) > 0:
        print('There are the following items:')
        orderedInventory = asOrderedList(p.location.items)
        for kvp in orderedInventory: # For the key-value pairs in the ordered inventory...
            print('\t' + kvp[0] + ' x' + str(kvp[1]))
    else:
        print("There is nothing of use to you here.")
    print()
    p.location.availableDirs()
    print()
    print("Health: " + str(p.health))
    print("Food meter: " + str(p.hunger))
    print()
    
def victory(p):
    clear()
    if 'fire' in p.inventory:
        print('You have discovered fire! You have successfully set yourself on the path to civilization! Congratulations!')
    elif p.defeated >= 30:
        print('You have defeated enough enemies that you are now at the top of the food chain! Congratulations!')
    elif len(p.allies) >= 30:
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
          
def evolve(p):
    clear()
    print('Health increase: 5 exp')
    print('Stomach size increase: 5 exp')
    print('Strength increase: 5 exp')
    print('Sociability increase: 5 exp')
    print('Speed increase: 5 exp')
    print('Intelligence increase: 5 exp')
    print('Pouches – can carry more items: 5 exp')
    print('Stronger back – can carry heaver items: 5 exp')
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
    print()
    print('Go back.')
    print()
    print('You have ' + str(p.experience) + ' experience points.')
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
        elif choice.lower() in 'pouches':
            if p.experience >= 5:
                p.self.inventoryCap += 3
                self.experience -= 5
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'stronger back':
            if p.experience >= 5:
                p.self.maxinvweight += 3
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
                p.abilities.append('Item use')
                self.experience -= 15
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'flexible responding':
            if p.experience >= 30:
                p.abilities.append('Fat reserves')
                self.experience -= 30
                transactionCompleted = True
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'fire':
            if p.experience >= 50:
                victory()
            else:
                ('Not enough experience. Try again.')
        elif choice.lower() in 'go back':
            transactionCompleted = True
    print()
    input('Press enter to continue.')
        

clear()

playing = True
w = World()
mapx = 4
mapy = 4
w.makeMap(mapx,mapy)
for i in range(0,28):
    r = random.choice(w.squares)
    if not r.creature:
        creatureType = random.choice(w.possibleCreatures)
        creatureType(r, 1)
for i in range(0,28):
    r = random.choice(w.squares)
    if not r.creature:
        creatureType = random.choice(w.possibleCreatures)
        creatureType(r, 2)
for i in range(0,28):
    r = random.choice(w.squares)
    if not r.creature:
        creatureType = random.choice(w.possibleCreatures)
        creatureType(r, 3)
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
    commandSuccess = False
    timePasses = False
    while not commandSuccess:
        clear()
        printSituation(w,p)
        commandSuccess = True
        command = input('What will you do? ').lower()
        commandWords = command.split()
        elem = commandWords[0]
        for key in w.possibleCommands:
            if elem in w.possibleCommands[key]:
                commandWords[0] = key
                break
                
        if command == 'help':
            help(p)
            
        elif command == 'me':
            clear()
            p.stats()
            
        elif command == 'all stats':
            clear()
            p.allstats()
        
        elif 'inventory' in commandWords and 'abbreviate' not in commandWords:
            showInventory(p)
#             print()
#             input('Press enter to continue.')
          
        elif commandWords[0] == 'go':
            direction = commandWords[1]
            if not p.go(direction):
                commandSuccess = 0
            
#         elif 'north' in commandWords and 'abbreviate' not in commandWords:
#             if p.location.exits['north'] == None:
#                 print('You may not go north. Try again.')
#                 commandSuccess = False
#             elif p.location.exits['north'].terrain == 'water':
#                 if 'semiaquatic' not in player.abilities:
#                     print('There is water in that direction, and you cannot swim. Try again.')
#                     commandSuccess = False
#             else:
#                 print('You go north.')
#                 p.north()
#                 timePasses = True
# #             print()
# #             input('Press enter to continue.')
                
#         elif 'south' in commandWords and 'abbreviate' not in commandWords:
#             if p.location.exits['south'] == None:
#                 print('You may not go south. Try again.')
#                 commandSuccess = False
#             elif p.location.exits['south'].terrain == 'water':
#                 if 'semiaquatic' not in player.abilities:
#                     print('There is water in that direction, and you cannot swim. Try again.')
#                     commandSuccess = False
#             else:
#                 print('You go south.')
#                 p.south()
#                 timePasses = True
# #             print()
# #             input('Press enter to continue.')
                
#         elif 'west' in commandWords and 'abbreviate' not in commandWords:
#             if p.location.exits['west'] == None:
#                 print('You may not go west. Try again.')
#                 commandSuccess = False
#             elif p.location.exits['west'].terrain == 'water':
#                 if 'semiaquatic' not in player.abilities:
#                     print('There is water in that direction, and you cannot swim. Try again.')
#                     commandSuccess = False
#             else:
#                 print('You go west.')
#                 p.west()
#                 timePasses = True
# #             print()
# #             input('Press enter to continue.')
                
#         elif 'east' in commandWords and 'abbreviate' not in commandWords:
#             if p.location.exits['east'] == None:
#                 print('You may not go east. Try again.')
#                 commandSuccess = False
#             elif p.location.exits['east'].terrain == 'water':
#                 if 'semiaquatic' not in player.abilities:
#                     print('There is water in that direction, and you cannot swim. Try again.')
#                     commandSuccess = False
#             else:
#                 print('You go east.')
#                 p.east()
#                 timePasses = True
# #             print()
# #             input('Press enter to continue.')
                
        elif commandWords[0] == 'pickup':
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
#             print()
#             input('Press enter to continue.')
                
        elif commandWords[0] == 'drop':
            if len(commandWords) == 3:
                item = commandWords[1] + ' ' + commandWords[2]
            else:
                item = commandWords[1]
            if item in p.inventory:
                p.drop(item)
            else:
                print('You don\'t have any such item. Try again.')
                commandSuccess = False
#             print()
#             input('Press enter to continue.')
            
        elif commandWords[0] == 'use':
            if len(commandWords) == 3:
                item = commandWords[1] + ' ' + commandWords[2]
            elif len(commandWords) == 2:
                item = commandWords[1]
            else:
                item = input('What do you want to use?')
            if not p.useItem():
                commandSuccess = False
            
        elif commandWords[0] == 'eat':
            else:
                if len(commandWords) == 2:
                    if commandWords[1] == 'meat' or commandWords[1] == 'fruit':
                        food = commandWords[1]
                    else:
                        commandSuccess = False
                        print("Sorry, I didn't catch that. Please try again.")
#                         break
                elif len(commandWords) == 1:
                    food = input("What would you like to eat?")
                    if food != 'meat' and food != 'fruit':
                        print("Sorry, I didn't catch that. Please try again.")
                if food in p.location.items or food in p.inventory:
                    if not p.eat(food):
                        commandSuccess = False
                        print('You can\'t eat that! Bleh!')
                    else:
                        timePasses = True
                else:
                    print('There is no ' + food + ' for you to eat.')
                    commandSuccess = False
#             print()
#             input('Press enter to continue.')
                    
        elif 'wait' in command:
            if len(commandWords) == 3:
                if commandWords[0] == 'wait' and commandWords[2] == 'turns' or commandWords[2] == 'turn':
                    i = int(commandWords[1])
            elif len(commandWords) == 1:
                i = 1
            j = 1
            while j <= i:
                w.update()
                if w.turn_count > 200:
                    game_over()
                j += 1
            print('You wait ' + str(i) + ' turns.')
#             print()
#             print('Press enter to continue.')
                
        elif 'inspect' in commandWords and 'abbreviate' not in commandWords:
            if len(commandWords) == 3:
                item = commandWords[1] + ' ' + commandWords[2]
            elif len(commandWords) == 2:
                item = commandWords[1]
            else:
                commandSuccess = False
                print("Sorry, I didn't catch that. Please try again.")
                item = None
#                 print()
#                 input('Press enter to continue.')
#                 break
            if item:
                if item in p.location.items or item in p.inventory or item == 'creature':
                    p.inspect(item)
                else:
                    print('There is nothing by that name here. Try again.')
                    commandSuccess = False
#             print()
#             input('Press enter to continue.')
                
        elif commandWords[0] == 'abbreviate':
            if 'as' in commandWords:
                if commandWords[2] == 'as':
                    comm = commandWords[1]
                    abbrev = commandWords[3]
                    if comm in w.possibleCommands: #make this dict
                        w.possibleCommands[comm].append(abbrev)
                elif commandWords[3] == 'as':
                    comm = commandWords[1] + ' ' + commandWords[2]
                    abbrev = commandWords[4]
                    if comm in w.possibleCommands: #make this dict
                        w.possibleCommands[comm].append(abbrev)
                        
        elif command == 'quit':
            playing = False
            break
            
        elif command == 'location':
            clear()
            p.locationDets()
#             print()
#             input('Press enter to continue.')
            
        elif 'attack' in commandWords and 'abbreviate' not in commandWords:
            if p.location.creature != None:
                if 'Flexible responding' in p.abilities:
                    clear()
                    p.flexibleResponse(p.location.creature)
                else:
                    clear()
                    p.attack(p.location.creature)
                if p.defeated >= 30:
                    victory(p)
                    break
                timePasses = True
            else:
                print('There is no creature here.')
                commandSuccess = False
#             print()
#             input('Press enter to continue.')
              
        elif 'befriend' in commandWords and 'abbreviate' not in commandWords:
            if p.location.creature != None:
                if 'Flexible responding' in p.abilities:
                    clear()
                    p.flexibleResponse(p.location.creature)
                else:
                    clear()
                    p.befriend(p.location.creature)
                if len(p.allies) >= 30:
                    victory(p)
                    break
                timePasses = True
            else:
                print('There is no creature here.')
                commandSuccess = False
#             print()
#             input('Press enter to continue.')
        
        elif 'ally' in commandWords and 'abbreviate' not in commandWords:
            if p.location.creature == None:
                print('There is no creature here.')
                commandSuccess = False
            elif not p.ally(p.location.creature):
                print('You need to befriend a creature before it will be your ally!')
                commandSuccess = False
#             print()
#             input('Press enter to continue.')
                
        elif 'dismiss' in commandWords and 'abbreviate' not in commandWords:
            if self.ally == None:
                print('You have no ally to dismiss!')
                commandSuccess = False
            else:
                self.ally = None
#             print()
#             input('Press enter to continue.')
                
        elif command == 'evolve':
            evolve(p)
                
        else:
            print()
            print('Sorry, I don\'t understand. Type "help" for available options. ')
#             print()
#             input('Press enter to continue.')
            commandSuccess = False
            
        print()
        input('Press enter to continue.')
    if timePasses:
        clear()
        w.update()
        if w.turn_count > 200:
            gameOver(w)
        print()
        print('Press enter to continue.')
if not p.alive:
    gameOver(w)
