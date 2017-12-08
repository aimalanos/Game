from World import World
from Square import Square
from Player import Player
from Player import asOrderedList
from Creature import Creature
import os
import random

def help(p):
    print('Use the "me" command to see an abbridged list of stats.')
    print('Use the "allstats" command to see a full list of stats.')
    print('Use the "inventory" command to see your inventory.')
    print('Use the "location" command to see details on your location.')
#     print('Use the "friends" command to see a list of creatures you have befriended.')
    print('Use the "go __" command to move. Don\'t forget to say which direction!')
    print('Use the "eat __" command to eat.')
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
    print('Use the "help" command to see this menu again.')
    print('Use the "quit" command to leave the game.')
    
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def showInventory(p):
    clear()
    print('Your inventory contains the following items:')
    orderedInventory = asOrderedList(p.inventory)
    for kvp in orderedInventory:
        weight = p.world.itemWeights[kvp[0]] * kvp[1]
        print('\t' + kvp[0] + ' x' + str(kvp[1]) + ', ' + str(weight) + 'weight')
    
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
        tc = "All the items here are in trees! You'll need a stick to get them out."
    elif p.location.terrain == 'grassy':
        tc = 'It\'s very nice here.'
    print("Turn " + str(w.turn_count))
    print()
    print("Your coordinates are " + str(p.location.coordinates) + ".")
    if p.location == p.home:
        print('You\'re at home!')
    print("The weather is " + w.weather + ". " + wc)
    print("The terrain is " + p.location.terrain + ". " + tc)
    if p.location.creature != None:
        if p.ally == None or p.ally.location != p.location:
            if p.location.creature in p.friends:
                print("There is a creature here. It is your friend the " + str(p.location.creature.name) + ".")
            else:
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
    if p.hunger == 0:
        print('STARVING')
    print()
    
def victory(p):
    clear()
    if 'Fire' in p.abilities:
        print('You have discovered fire! You have successfully set yourself on the path to civilization! Congratulations!')
    elif p.defeated >= 20:
        print('You have defeated enough enemies that you are now at the top of the food chain! Congratulations!')
    elif len(p.friends) >= 20:
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
        

clear()

playing = True
w = World()
w.makeMap(w.mapx,w.mapy)
            
print('Welcome to Irtiqa! In this turn-based game, you act as an animal within a world full of other animals and objects.')
print()
print('Your health will decrease and your hunger will increase steadily with time. You may recharge both by eating or by returning to your home (starting location).')
print()
print('Your goal is to become the dominant creature in your environment, however you choose to do so.')
print()
print('You can fight with creatures or befriend them. Either one will bring you experience points, and each has its risks and benefits.')
print()
print('You may win the game by becoming every creature\'s best friend...or their biggest fear.')
print()
print('Use the "help" command at any time to see a list of commands available to you.')
print()
p = Player(w)
clear()
print('Before you get started, you may want to see a list of commands!')
help(p)
print()
input('Press enter to continue. ')

for i in range(0,41):
    r = random.choice(w.squares)
    if r == p.location:
        if random.randint(0,1) == 1: #player should start with level 1 creature or no creature at home
            creatureType = random.choice(w.possibleCreatures)
    if not r.creature:
        if r.terrain == 'lake':
            creatureType = random.choice(w.aquaticCreatures)
        else:
            creatureType = random.choice(w.possibleCreatures)
        creatureType(r, 1)
for i in range(0,28):
    r = random.choice(w.squares)
    if not r.creature:
        if r.terrain == 'lake':
            creatureType = random.choice(w.aquaticCreatures)
        else:
            creatureType = random.choice(w.possibleCreatures)
        creatureType(r, 2)
for i in range(0,15):
    r = random.choice(w.squares)
    if not r.creature:
        if r.terrain == 'lake':
            creatureType = random.choice(w.aquaticCreatures)
        else:
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

while playing and p.alive:
    timePasses = False
    clear()
    printSituation(w,p)
    command = input('What will you do? ').lower()
    if command == '':
        print('Oops! Looks like you forgot to give a command.')
        input("Press enter to continue.")
        command = 'skip'
    commandWords = command.split()
    elem = commandWords[0]
    for key in w.possibleCommands:
        if elem in w.possibleCommands[key]:
            commandWords[0] = key
            break
    if len(commandWords) > 1:
        elem = commandWords[0] + ' ' + commandWords[1]
        for key in w.possibleCommands:
            if elem in w.possibleCommands[key]:
                commandWords[0] = key
                del commandWords[1]
                break
            
    if commandWords[0] == 'help':
        help(p)
        
    elif commandWords[0] == 'me':
        clear()
        p.stats()
        
    elif commandWords[0] == 'allstats':
        clear()
        p.allstats()
    
    elif commandWords[0] == 'inventory':
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
                print('\t' + str(elem.coordinates),elem.terrain)
                count += 1
            print('total = ' + str(count))
        elif stat == 'experience':
            if len(commandWords) == 2:
                amt = int(input('how much? '))
            else:
                amt = int(commandWords[2])
            p.experience += amt
        elif stat == 'soc':
            if len(commandWords) == 3:
                amt = int(commandWords[2])
            else:
                amt = int(input('How much? '))
            p.maxSociability,p.sociability = amt,amt
        
      
    elif commandWords[0] == 'go':
        direction = commandWords[1]
        if p.go(direction):
            timePasses = True
            
    elif commandWords[0] == 'pickup':
        if len(commandWords) == 3:
            item = commandWords[1] + ' ' + commandWords[2]
        elif len(commandWords) == 2:
            item = commandWords[1]
        else:
            item = input('What do want to pick up? ')
        item = item.lower()
        p.pickup(item)
            
    elif commandWords[0] == 'drop':
        if len(commandWords) == 3:
            item = commandWords[1] + ' ' + commandWords[2]
        elif len(commandWords) == 2:
            item = commandWords[1]
        else:
            item = input('What do you want to drop? ')
        item = item.lower()
        p.drop(item)
        
    elif commandWords[0] == 'use':
        if len(commandWords) == 3:
            item = commandWords[1] + ' ' + commandWords[2]
        elif len(commandWords) == 2:
            item = commandWords[1]
        else:
            item = input('What do you want to use? ')
        item = item.lower()
        if p.useItem():
            timePasses = True
        
    elif commandWords[0] == 'eat':
        clear()
        if len(commandWords) == 2:
            food = commandWords[1]
        elif len(commandWords) == 1:
            food = input("What would you like to eat? ")
        if p.eat(food):
            timePasses = True
              
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
        clear()
        if len(commandWords) == 3:
            item = commandWords[1] + ' ' + commandWords[2]
        elif len(commandWords) == 2:
            item = commandWords[1]
        else:
            item = input("Sorry, I didn't catch that. What would you like to inspect? ")
        p.inspect(item)

            
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
                if p.flexibleResponse(p.location.creature):
                    timePasses = True
            else:
                clear()
                if p.attack(p.location.creature):
                    timePasses = True
            if p.defeated >= 20:
                victory(p)
                break
            if len(p.friends) >= 20:
                victory(p)
                break
          
    elif commandWords[0] == 'befriend':
        if p.location.creature != None:
            if 'Flexible responding' in p.abilities:
                clear()
                if p.flexibleResponse(p.location.creature):
                    timePasses = True
            else:
                clear()
                if p.befriend(p.location.creature):
                    timePasses = True
            if p.defeated >= 20:
                victory(p)
                break
            if len(p.friends) >= 20:
                victory(p)
                break
    
    elif commandWords[0] == 'recruit':
        p.recruit()
            
    elif commandWords[0] == 'dismiss':
        if self.ally == None:
            print('You have no ally to dismiss!')
        else:
            self.ally = None

    elif commandWords[0] == 'evolve':
        p.evolve()

    elif command == 'test':
        w.turn_count = 199

    elif command == 'skip':
        pass

    elif command == 'show map':
        close = False
        while close == False:
            w.showMap()
            action = input("Type close to close the map, or \"go ___ \" to move. ")
            if action == '':
                pass
            elif action.split()[0] == 'go':
                p.go(action.split()[1])
            elif action == 'close':
                close = True

    else:
        print()
        print('Sorry, I don\'t understand. Type "help" for available options. ')
        
    if not timePasses:
        print()
        input('Press enter to continue. ')
    else:
        w.update()
        if w.turn_count > 200:
            gameOver(w)
        print()
        input('Press enter to continue. ')
if not p.alive:
    gameOver(w)
