from World import World
from Square import Square
from Player import Player
from Creature import Creature

w = World()
for i in range(-10,11):
    for j in range(-10, 11):
        Square(w, i, j)
p = Player()
w.player = p
