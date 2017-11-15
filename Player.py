class Player:
    def __init__(self, w):
        self.name = input("What is your creature's name? ")
        self.diet = input("Is your creature a carnivore or an herbivore? ")
        w.add_player(self)
        self.world = w      # Still unsure about implementation of the map
        self.location = 0.0
        self.hunger = 100
        self.health = 10
        self.strength = 5
        self.sociability = 5
        self.speed = 5
        self.intelligence = 0
        self.experience = 0
        self.abilities = []
        self.inventory = []
