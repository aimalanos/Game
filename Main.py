from World import World
from Square import Square
from Player import Player
from Creature import Creature

w = World()
for i in range(-8,9):
    for j in range(-8, 9):
        Square(w, i, j)
p = Player()
w.player = p
