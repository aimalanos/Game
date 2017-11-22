from World import World
from Square import Square
from Player import Player
from Creature import Creature
import random

playing = True
w = World()
mapx = 4
mapy = 4
w.makeMap(mapx,mapy)
for i in range(-mapx,mapx+1):
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
        r.creature = Creature(r, 2)
for i in range(0,200):
    r = random.choice(w.squares)
    r.fruit += 1
def me():
    return p.stats()
def help():
    print("type 'me' for player stats")
    print("you may travel" + str(p.availabledirs) + "\n")

while playing and p.alive:
    command = input("What would you like to do next? \n help \n me \n go " + str(p.availabledirs) + " \n inventory \n")
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
