from World import World
from Square import Square
from Player import Player
from Creature import Creature
import random

#clear()

playing = True
w = World()
mapx = 4
mapy = 4
w.makeMap(mapx,mapy)
for i in range(-mapx,mapx+1): # Isn't make map doing the same thing as these loops?
    for j in range(-mapy, mapy+1):
        Square(w, i, j)
p = Player(w)
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
    r.plantFood += 1
    
    
def me():
    return p.stats()
    print(p.location.exits)

def help():
    print("Type 'me' for player stats.")
    print("You may travel" + str(p.availabledirs) + "\n")
    
#def clear():
 #   os.system('cls' if os.name == 'nt' else 'clear')
    
#def printSituation():
    #clear()
    #print("Your coordinates are " + str(p.location.coordinates))
    # if p.location.
    # need to finish this
    #how will this be different from me()
    
    
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
    if p.intelligence >= 8 and 'Tool use' not in p.abilities:
        print('Tool use: 10 exp')
    if p.intelligence >= 13 and 'Tool use' in p.abilities and 'Flexible responding' not in p.abilities:
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
        elif choice.lower() in 'tool use':
            if p.experience >= 15:
                p.abilities.append('Tool use') # Will implement this later
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
                
                
                
    def victory():
        #clear()
        if 'fire' in p.inventory:
            print('You have discovered fire! You have successfully set yourself on the path to civilization! Congratulations!')
        elif self.defeated >= 30:
            print('You have defeated enough enemies that you are now at the top of the food chain! Congratulations!')
        elif self.allies >= 30:
            print('You have enough allies to be protected wherever you go! That means you win! Congratulations!')
        # We should put some fireworks in here

    

while playing and p.alive:
    w.update()
    command = input("You are at " + str(p.location) + "\nWhat would you like to do next? \n help \n me \n go " + str(p.availabledirs) + " \n inventory \n").lower()
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
        x = input('x-coordinate?')
        y = input('y-coordinate?')
        for squ in w.squares:
            if squ.coordinates[0] == x and squ.coordinates[1] == y:
                p.location = squ
    #pick up and drop
