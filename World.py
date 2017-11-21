class World:
    def __init__(self):
        self.turn_count = 0
        self.weather = "clear"
        self.player = None
        self.squares = []
        self.healthLoss = 0 # Determines how much health is lost when updating
        self.hungerLoss = 3 # Determines how much the player's hunger increases when updating
        self.speedPenalty = 0 # The penalties will be applied depending on the weather
        self.sociabilityPenalty = 0
    def makeMap(self,x,y):
        for num in range(-x,x): #draw the grid
            for nums in range(-y,y):
                self.squares.append(Square(self,num,nums))
        for squ in self.squares: #more efficient square exit assignment
            if squ.coordinates[0] == x:
                if squ.coordinates[1] == y:
                    
                elif squ.coordinates[1] == -y: ##check for edges and corners
                
                else:
                    
            elif squ.coordinates[0] == -x:
                if squ.coordinates[1] == y:
                    
                elif squ.coordinates[1] == -y:
                
                else:
                    
        for squ in self.world.squares: #assign squares' exits
            if squ.coordinates[1] == self.coordinates[1]: # To be east-west adjacent, they must have the same y-coordinate
                if squ.coordinates[0] == self.coordinates[0] - 1:
                    self.exits[east] = squ
                elif squ.coordinates[0] == self.coordinates[0] + 1:
                    self.exits[west] = squ
            elif squ.coordinates[0] == self.coordinates[0]: # To be north-south adjacent, they must have the same x-coordinate
                if squ.coordinates[1] == self.coordinates[1] - 1:
                    self.exits[south] = squ
                elif squ.coordinates[1] == self.coordinates[1] + 1:
                    self.exits[north] = squ 
    def add_player(self, player):
        self.player = player
    def reset(self):
        self.healthLoss = 0
        self.hungerLoss = 3
        self.speedPenalty = 0
        self.sociabilityPenalty = 0
    def gameOver(self):
        self.player = None
    def update(self):
        self.player.update()
        self.turn_count += 1
        if turn_count % 5 == 0:
            self.weather = random.choice("clear", "rainy", "hailing", "snowy", "drought")
            if self.weather == "rainy":
                self.speedPenalty = self.player.speed // 10
            elif self.weather == "hailing":
                self.healthLoss = self.player.health // 15 #wow this is savage
            elif self.weather == "snowy":
                self.sociabilityPenalty = self.player.sociability // 10
            elif self.weather == "drought":
                self.hungerLoss = 6
