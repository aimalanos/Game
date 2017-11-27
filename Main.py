from World import World
from Square import Square
from Player import Player
from Creature import Creature
import os
import random

def me():
    clear()
    p.stats()

def help():
    clear()
    print("Type 'me' for player stats.")
    print("You may travel" + str(p.availabledirs) + "\n")
    
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def printSituation():
    clear()
    print("Turn " + str(w.turn_count))
    print()
    print("Your coordinates are " + str(p.location.coordinates) + ".")
    print("The weather is " + w.weather + ".")
    print("The terrain is " + p.location.terrain + ".")
    if p.location.creature:
        print("There is a creature here.")
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
for i in range(-mapx,mapx+1): # Isn't make map doing the same thing as these loops?
    for j in range(-mapy, mapy+1):
        Square(w, i, j)
for i in range(0,80):
    r = random.choice(w.squares)
    if not r.creature:
        r.creature = Creature(r, 1)
for i in range(0,80):
    r = random.choice(w.squares)
    if not r.creature:
        r.creature = Creature(r, 2)
for i in range(0,80):
    r = random.choice(w.squares)
    if not r.creature:
        r.creature = Creature(r, 3)
for i in range(0,200):
    r = random.choice(w.squares)
    if 'fruit' in r.items:
        r.items['fruit'] += 1
    else:
        r.items['fruit'] = 1

p = Player(w)       

while playing and p.alive:
    w.update()
    command = input("You are at " + str(p.location.coordinates) + "\n What would you like to do next? \n <help> \n <me> \n <go ...> " + str(p.availabledirs) + " \n").lower()
    if command == 'help':
        help()
    elif command == 'me':
        me()
    elif command == 'go north':
        p.north()
    elif command == 'go south':
        p.south()
    elif command == 'go west':
        p.west()
    elif command == 'go east':
        p.east()
    elif command == 'change location':
        x = input('x-coordinate? ')
        y = input('y-coordinate? ')
        for squ in w.squares:
            if squ.coordinates[0] == x and squ.coordinates[1] == y:
                p.location = squ
    elif command == 'inventory':
        inv = ''
        for elem in self.inventory:
            inv += elem
        for elem in self.abilities:
            abi += elem
        print('Inventory: ' + inv + '\n Abilities: ' + abi)
    elif command == 'location':
        pickups = []
        for item in p.location.items:
            pickups.append(item)
        print('coordinates: ' + str(p.location.coordinates) + '\n items available for pickup: ' + str(pickups))
    elif command[:6] == 'pickup' and command[7:] in p.location.items:
        item = command[7:]
        p.pickup(item)
        print('here')
    else:
        clear()
        r = command[:6]
        item = command[7:]
        #player.pickup(item)
        print(r,item)
        command = input('Sorry, I don\'t understand. What would you like to do? Type "options" for available options.')
