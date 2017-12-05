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
    print('Use the "location" command to see details on your location.')
    print('Use the "friends" command to see a list of creatures you have befriended.')
    print('Use the "go __" command to move. Don\'t forget to say which direction!')
    print('Use the "pickup __" command to pick up an item.')
    print('Use the "drop __" command to drop an item.')
    if 'Item use' in p.abilities:
        print('Use the "use __" command to use an item.')
    print('Use the "show map" command to see a map of the world.')
    print('Use the "inspect __" command to learn more about your environment.')
    print('Use the "attack" command to attack a creature.')
    print('Use the "befriend" command to try to befriend a creature.')
    print('Use the "recruit" command to make a befriended creature your ally.')
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
    elif len(p.friends) >= 30:
        print('You have enough allies to be protected wherever you go! That means you win! Congratulations!')
    # We should put some fireworks in here
                      
def gameOver(w):
    playing = False
    print('GAME OVER')
    print()
    if w.turn_count >= 200:
        print('You took too long! Another creature has become dominant.')
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
        if w.turn_count >= 200:
            gameOver(w)
            playing = False
            break
        printSituation(w,p)
        commandSuccess = True
        command = input('What will you do? ').lower()
        if command == '':
            print('Oops! Looks like you forgot to give a command.')
            command = 'skip'
        commandWords = command.split()
        elem = commandWords[0]
        for key in w.possibleCommands:
            if elem in w.possibleCommands[key]:
                commandWords[0] = key
                break
                
        if commandWords[0] == 'help':
            help(p)
            
        elif commandWords[0] == 'me':
            clear()
            p.stats()
            
        elif commandWords[0] == 'allstats':
            clear()
            p.allstats()
        
        elif 'inventory' in commandWords[0]:
            showInventory(p)

        elif commandWords[0] == 'cheat':
            stat = commandWords[1]
            if stat == 'health':
                p.health = p.maxHealth
            elif stat == 'strength':
                p.strength = 100
            elif stat == 'befriend':
                p.friends.append(p.location.creature)
            elif stat == 'map':
                count = 0
                print('squares:')
                for elem in w.squares:
                    print('\t' + str(elem.coordinates),elem.terrain,elem)
                    count += 1
                print('total = ' + str(count))
          
        elif commandWords[0] == 'go':
            timePasses = True
            direction = commandWords[1]
            if not p.go(direction):
                commandSuccess = False
                timePasses = False
                
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
            if len(commandWords) == 2:
                if commandWords[1] == 'meat' or commandWords[1] == 'fruit':
                    food = commandWords[1]
                else:
                    commandSuccess = False
                    print("Sorry, I didn't catch that. Please try again.")
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

                    
        elif commandWords[0] == 'wait':
            if len(commandWords) == 3:
                if commandWords[0] == 'wait' and commandWords[2] == 'turns' or commandWords[2] == 'turn':
                    i = int(commandWords[1])
            elif len(commandWords) == 1:
                i = 1
            j = 1
            while j <= i:
                w.update()
                if w.turn_count > 200:
                    gameOver()
                j += 1
            print('You wait ' + str(i) + ' turns.')
                
        elif commandWords[0] == 'inspect':
            if len(commandWords) == 3:
                item = commandWords[1] + ' ' + commandWords[2]
            elif len(commandWords) == 2:
                item = commandWords[1]
            else:
                commandSuccess = False
                print("Sorry, I didn't catch that. Please try again.")
                item = None
            if item:
                if item in p.location.items or item in p.inventory or item == 'creature':
                    p.inspect(item)
                else:
                    print('There is nothing by that name here. Try again.')
                    commandSuccess = False
                
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
                        
        elif commandWords[0] == 'quit':
            playing = False
            break
            
        elif commandWords[0] == 'location':
            clear()
            p.locationDets()
            
        elif commandWords[0] == 'attack':
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
              
        elif commandWords[0] == 'befriend':
            if p.location.creature != None:
                if 'Flexible responding' in p.abilities:
                    clear()
                    p.flexibleResponse(p.location.creature)
                else:
                    clear()
                    p.befriend(p.location.creature)
                if len(p.friends) >= 30:
                    victory(p)
                    break
                timePasses = True
            else:
                print('There is no creature here.')
                commandSuccess = False
        
        elif commandWords[0] == 'recruit':
            print(p.friends)
            if p.friends == []:
                print("You don't have any friends who can become your ally.")
                commandSuccess = False
            elif commandWords[1] in p.friends:
                for elem in p.friends:
                    if elem.name == commandWords[1]:
                        p.ally = elem
                print('You have allied your friend the ' + commandWords[1] + '! Your ally will follow you around and fight with you.')
                commandSuccess = False
            else:
                print('You do not have a ' + commandWords[1] + ' friend. Type \'friends\' to see a list of your friends.')
                
        elif commandWords[0] == 'dismiss':
            if self.ally == None:
                print('You have no ally to dismiss!')
                commandSuccess = False
            else:
                self.ally = None

                
        elif commandWords[0] == 'evolve':
            evolve(p)

        elif command == 'test':
            w.turn_count = 199

        elif command == 'skip':
            x=3

        elif commandWords[0] == 'friends':
            print('Your friends are:')
            for elem in p.friends:
                print('\t' + elem.name)

        elif command == 'show map':
            sWidth = 8 #square width
            sHeight = 4
            print('|' + ('-'*sWidth + '|')*mapx*2) #top border
            row = mapy #start here to get proper north/south orientation
            while row >= -mapy: #go from 4 to -4
                curr = [] #keeps track of all square objects in current row
                minirow = 0 #aka sub-row; tracks lines within the square
                while minirow < sHeight:
                    if minirow == 0: #top line of each square states terrain
                        for elem in w.squares:
                            if elem.coordinates[1] == row: #all squares with y-coord equal to current row are relevant
                                curr.append(elem)          #add these squares to curr
                        i = 1
                        while i < len(curr): #compensate for the fact that each square was being added twice(??)
                            del curr[i]
                            i += 2
                        print('| ' + curr[0].terrain + ' '*(sWidth-len(curr[0].terrain)-1) + '| ' + curr[1].terrain + ' '*(sWidth-len(curr[1].terrain)-1) + '| ' + curr[2].terrain + ' '*(sWidth-len(curr[2].terrain)-1) + '| ' + curr[3].terrain + ' '*(sWidth-len(curr[3].terrain)-1) + '| ' + curr[4].terrain + ' '*(sWidth-len(curr[4].terrain)-1) + '| ' + curr[5].terrain + ' '*(sWidth-len(curr[5].terrain)-1) + '| ' + curr[6].terrain + ' '*(sWidth-len(curr[6].terrain)-1) + '| ' + curr[7].terrain + ' '*(sWidth-len(curr[7].terrain)-1) + '|')
                        minirow += 1
                    elif minirow == 1 or minirow == 2: #minirows 1 and 2 are just spaces
                        print('|' + (' '*sWidth + '|')*mapx*2)
                        minirow += 1
                    else: #minirow 3 is the bottom border of each square
                        print('|' + ('-'*sWidth + '|')*mapx*2)
                        minirow += 1
                        if minirow == 4:
                            row += 1
                            break

        else:
            print()
            print('Sorry, I don\'t understand. Type "help" for available options. ')
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
