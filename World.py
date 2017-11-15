class World:
    def __init__(self):
        self.turn_count = 0
        self.weather = None
        self.player = None
    def add_player(self, player):
        self.player = player
    def update(self):
        self.player.update()
        self.turn_count += 1
        # Weather may need to change
