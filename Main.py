from World import World
from Square import Square
from Player import Player
from Player import asOrderedList
from Creature import Creature
import os
import random

def help():
    print('Use the "me" command to see an abridged list of stats.')
    print('Use the "allstats" command to see a full list of stats.')
    print('Use the "inventory" command to see your inventory.')
    print('Use the "location" command to see details on your location.')
    print('Use the "go __" command to move. Don\'t forget to say which direction!')
    print('Use the "eat __" command to eat.')
    print('Use the "pickup __" command to pick up an item.')
    print('Use the "drop __" command to drop an item.')
    print('Use the "use __" command to use an item. You must unlock the "Item use" ability first, though!')
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
    
def printSituation(w, p):
    clear()
    wc = '' # The flavor text for the weather
    if w.weather == 'rainy':
        wc = 'It slows you down.'
    elif w.weather == 'hailing':
        wc = 'You are being buffeted by hail.'
    elif w.weather == 'snowy':
        wc = 'The poor weather reduces your sociability.'
    elif w.weather == 'drought':
        wc = 'You are getting hungry very quickly.'
        
    tc = '' # The flavor text for the terrain
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
    # Tells the player if there is a creature here
    if p.location.creature != None:
        if p.ally == None or p.ally.location != p.location:
            if p.location.creature in p.friends:
                print("There is a creature here. It is your friend the " + str(p.location.creature.name) + ". Type 'recruit' to have the " + str(p.location.creature.name) + " follow you around and fight with you!")
            else:
                print("There is a creature here. It is a " + str(p.location.creature.name) + ".")
    else:
        print("You are alone here.")
    # Tells the player if there are items here
    if len(p.location.items) > 0:
        print('There are the following items:')
        orderedInventory = asOrderedList(p.location.items)
        for kvp in orderedInventory: # For the key-value pairs in the ordered inventory...
            print('\t' + kvp[0] + ' x' + str(kvp[1]))
    else:
        print("There is nothing of use to you here.")
        
    print()
    p.location.availableDirs() # Tells the player where they can go
    print()
    print("Health: " + str(p.health))
    print("Food meter: " + str(p.hunger))
    if p.hunger == 0:
        print('STARVING')
    print()
    print("Type 'help' for a list of commands.")
    print("Type 'show map' to show a map of the world.")
    print("Type 'evolve' to see a list of potential upgrades.")
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
print()
help()
print()
input('Press enter to continue. ')

# We spawn the creatures
for i in range(0,41):
    r = random.choice(w.squares)
    if not r.creature and r != p.home: # Only one creature per square, and creatures don't spawn at the player's home
        if r.terrain == 'lake': # Lakes get aquatic creatures
            creatureType = random.choice(w.aquaticCreatures)
        else:
            creatureType = random.choice(w.possibleCreatures)
        creatureType(r, 1)
for i in range(0,28):
    r = random.choice(w.squares)
    if not r.creature and r != p.home:
        if r.terrain == 'lake':
            creatureType = random.choice(w.aquaticCreatures)
        else:
            creatureType = random.choice(w.possibleCreatures)
        creatureType(r, 2)
for i in range(0,15):
    r = random.choice(w.squares)
    if not r.creature and r != p.home:
        if r.terrain == 'lake':
            creatureType = random.choice(w.aquaticCreatures)
        else:
            creatureType = random.choice(w.possibleCreatures)
        creatureType(r, 3)

# We spawn food
for i in range(0,60):
    r = random.choice(w.squares)
    if 'fruit' in r.items:
        r.items['fruit'] += 1
    else:
        r.items['fruit'] = 1

# We spawn items
for i in range(0,45):
    r = random.choice(w.squares)
    if r.terrain == 'lake':
        rItem = random.choice(w.waterItems)
    else:
        rItem = random.choice(w.landItems)
    if 'rItem' in r.items:
        r.items[rItem] += 1
    else:
        r.items[rItem] = 1

while playing and p.alive:
    timePasses = False
    #clear()
    printSituation(w,p)
    command = input('What will you do? ').lower()
    if command == '':
        print('Oops! Looks like you forgot to give a command.')
        input("Press enter to continue.")
        command = 'skip'
    commandWords = command.split()
    elem = commandWords[0]
    for key in w.possibleCommands: # This loop enables abbreviation
        if elem in w.possibleCommands[key]:
            commandWords[0] = key
            break
    if len(commandWords) > 1: # If the player uses a two-word variant of a command (e.g. "pick up" for "pickup"), then we change it to the one-word variant
        elem = commandWords[0] + ' ' + commandWords[1]
        for key in w.possibleCommands:
            if elem in w.possibleCommands[key]:
                commandWords[0] = key
                del commandWords[1]
                break
            
    if commandWords[0] == 'help':
        clear()
        help()
        
    elif commandWords[0] == 'me':
        clear()
        p.stats()
        
    elif commandWords[0] == 'allstats':
        clear()
        p.allstats()
    
    elif command == 'inventory':
        clear()
        p.showInventory()

    elif command == 'abilities':
        clear()
        p.showAbilities()

    elif commandWords[0] == 'cheat':
        stat = commandWords[1]
        if stat == 'health':
            p.health = p.maxHealth
        elif stat == 'strength':
            p.strength = 100
        elif stat == 'befriend':
            p.friends.append(p.location.creature)
        elif stat == 'experience':
            if len(commandWords) == 2:
                amt = int(input('how much? '))
            else:
                amt = int(commandWords[2])
            p.experience += amt
        elif stat == 'conch':
            p.location.items['conch shell'] = 1
        elif stat == 'all':
            p.experience = 100
            p.abilities.append('use items')
            p.abilities.append('semiaquatic')
        elif stat == 'drift':
            p.inventory['driftwood'] = 1
        elif stat == 'meat':
            p.location.items['meat'] = 1
        elif stat == 'stick':
            p.location.items['big stick'] = 1
      
    elif commandWords[0] == 'go':
        if len(commandWords) == 2:
            direction = commandWords[1]
        else:
            direction = input('What direction do you want to go in? ')
            direction = direction.lower()
        if p.go(direction):
            timePasses = True
            
    elif commandWords[0] == 'pickup':
        if len(commandWords) == 3: # i.e. if the player wants to pick up a two-word item
            item = commandWords[1] + ' ' + commandWords[2]
        elif len(commandWords) == 2: # i.e. if the player wants to pick up a one-word item
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
        if p.useItem(item):
            timePasses = True
        
    elif commandWords[0] == 'eat':
        clear()
        if len(commandWords) == 2: # i.e. if the player says what they want to eat
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
        else:
            i = input("Sorry, I don't understand. How many turns do you want to wait? ")
        j = 1
        while j <= i:
            w.update()
            if w.turn_count > 200:
                gameOver()
                break
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
                if comm in w.possibleCommands:
                    w.possibleCommands[comm].append(abbrev)
            else:
                print('Sorry, I don\'t understand. Use the format "abbreviate __ as __" to abbreviate.')
                    
    elif commandWords[0] == 'quit':
        playing = False
        break
        
    elif commandWords[0] == 'location':
        clear()
        p.locationDets()
        
    elif commandWords[0] == 'attack':
        if 'Flexible responding' in p.abilities:
            clear()
            if p.flexibleResponse(p.location.creature):
                timePasses = True
        else:
            clear()
            if p.attack(p.location.creature):
                timePasses = True
        if p.defeated >= 20 or len(p.friends) >= 20:
            victory(p)
            break
          
    elif commandWords[0] == 'befriend':
        if 'Flexible responding' in p.abilities:
            clear()
            if p.flexibleResponse(p.location.creature):
                timePasses = True
        else:
            clear()
            if p.befriend(p.location.creature):
                timePasses = True
        if p.defeated >= 20 or len(p.friends) >= 20:
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
            elif action == 'close' or action == 'close map':
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
