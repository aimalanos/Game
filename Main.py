from World import World
from Square import Square
from Player import Player
from Creature import Creature

w = World()
for i in range(0,26):
    for j in range(0, 26):
        Square(w, i, j)
p = Player()
w.player = p
