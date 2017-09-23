class Player():

    def __init__(self, idNum):
        self.id = idNum
        self.spriteID = -1
        self.computer = False

    def setSpriteID(self, spriteNum):
        self.spriteID = spriteNum

    def getSpriteID(self):
        return self.spriteID