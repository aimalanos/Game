from World import World
from Square import Square
from Player import Player
from Creature import Creature
import random

w = World()
w.makeMap(8,8)
for i in range(-8,9):
    for j in range(-8, 9):
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
    print("you may travel" + str(p.availabledirs))
