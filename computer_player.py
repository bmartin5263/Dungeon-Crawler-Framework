from player import Player
import random
import curses


class ComputerPlayer(Player):
    MOVEMENTS = (curses.KEY_UP, curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_LEFT)

    def __init__(self, idNum):
        Player.__init__(self, idNum)
        self.computer = True
        self.computerSpriteIDs = []

    def setActiveSpriteIDs(self, spriteLst):
        self.computerSpriteIDs = list(spriteLst)

    def getActiveSpriteIDs(self):
        return list(self.computerSpriteIDs)

    def think(self, spriteNum, maze):
        spriteLocation = maze.getSpriteLocation(spriteNum)
        if spriteLocation == None:
            return None
        elif spriteLocation != -1:
            sprite = maze.mazeSprites[spriteLocation]
            if sprite.canAct():
                behavior = sprite.getBehavior()
                if behavior == None:
                    maze.mazeSprites[spriteLocation].hasActed()
                    return random.choice(ComputerPlayer.MOVEMENTS)
                elif behavior == 'travel':
                    maze.mazeSprites[spriteLocation].hasActed()
                    return ComputerPlayer.MOVEMENTS[sprite.getDirection()]