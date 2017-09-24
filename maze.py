import curses
from sprite import Sprite

class Maze():
    MOVEMENTS = (curses.KEY_UP, curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_LEFT)
    VALID_SPRITES = ('@', 'S')
    COMPUTER_SPRITES = ('S', '-')
    VALID_TILES = ('O', '■', 'W')
    MOVEABLE_TILES = ('water')

    def __init__(self, mazeName):
        self.columns = 0
        self.rows = 0
        self.totalSpaces = 0

        self.mazeSprites = []  # Map of all sprites
        self.mazeTiles = []  # Map of all tiles

        self.spriteID = 0  # ID of next sprite to be added
        self.spriteCount = 0  # Number of sprites
        self.spriteLocations = []  # Location of each sprite by ID

        ## Sprite ID Lists ##
        self.playerControlledSprite = 0
        self.computerActiveSprites = []
        self.computerSignalSprites = []
        self.tileSprites = []
        self.projectileSprites = []

        self.createMaze(mazeName)

    def mapCoordinates(self, i, j):
        return j * self.columns + i

    def unMapCoordinates(self, n):
        j = n // self.columns
        return (n - (4 * j), j)

    def createMaze(self, filename):
        f = open(filename, 'r')
        filelines = f.readlines()
        self.getMazeDimensions(filelines)
        mazePosition = 0
        for line in filelines:
            line = line.rstrip()
            linePosition = 0
            for character in line:
                if character in Maze.VALID_SPRITES:
                    self.addSprite(character, mazePosition)
                elif character in Maze.VALID_TILES:
                    self.addTile(character, mazePosition)
                else:
                    self.mazeTiles.append(None)
                    self.mazeSprites.append(None)
                linePosition += 1
                mazePosition += 1
            while linePosition < self.columns:
                self.mazeTiles.append(None)
                self.mazeSprites.append(None)
                mazePosition += 1

    def getMazeDimensions(self, fileLines):
        self.rows = len(fileLines)
        for line in fileLines:
            line = line.rstrip()
            if len(line) > self.columns:
                self.columns = len(line)
        self.totalSpaces = self.columns * self.rows

    def addSprite(self, symbol, position, spawnedFrom=None):
        for i, pos in enumerate(self.spriteLocations):
            if pos == None:
                spriteID = i
                self.spriteLocations[i] = position
                break
        else:
            spriteID = self.spriteID
            self.spriteLocations.append(position)
            self.spriteID += 1

        sprite = Sprite(spriteID, symbol, position)
        if symbol in Maze.COMPUTER_SPRITES:
            self.computerActiveSprites.append(spriteID)
        else:
            self.playerControlledSprite = spriteID

        if position == len(self.mazeSprites):
            self.mazeSprites.append(sprite)
            self.mazeTiles.append(None)
        else:
            self.mazeSprites[position] = sprite
            # self.mazeTiles[position] = None

    def addTile(self, symbol, position):
        for i, pos in enumerate(self.spriteLocations):
            if pos == None:
                spriteID = i
                self.spriteLocations[i] = position
                break
        else:
            spriteID = self.spriteID
            self.spriteLocations.append(position)
            self.spriteID += 1

        tile = Sprite(spriteID, symbol, position)
        self.tileSprites.append(spriteID)

        if position == len(self.mazeTiles):
            self.mazeTiles.append(tile)
            self.mazeSprites.append(None)
        else:
            self.mazeTiles[position] = tile
            # self.mazeSprites[position] = None

    def addProjectile(self, shootingSprite, shootingSpriteLocation, direction=None):
        if direction == None:
            initialDirection = shootingSprite.getDirection()
            spawnPoint = shootingSpriteLocation + self.getMovementNum(initialDirection, False)
        else:
            initialDirection = direction
            spawnPoint = shootingSpriteLocation + self.getMovementNum(direction, False)
        if self.mazeTiles[spawnPoint] == None and self.mazeSprites[spawnPoint] == None:
            self.addSprite('-', spawnPoint)
            self.mazeSprites[spawnPoint].setDirection(Maze.MOVEMENTS[initialDirection])
            if initialDirection in (1, 3):
                self.mazeSprites[spawnPoint].setSymbol('-')
            else:
                self.mazeSprites[spawnPoint].setSymbol('|')
            return {'update': [spawnPoint], 'computer sprite': True}
        return None

    def killSprite(self, spriteNum):
        spriteLocation = self.spriteLocations[spriteNum]
        self.spriteLocations[spriteNum] = None
        self.mazeSprites[spriteLocation] = None
        self.computerActiveSprites.remove(spriteNum)
        return spriteLocation

    def getComputerCommand(self, spriteNum):
        spriteLocation = self.spriteLocations[spriteNum]
        return self.mazeSprites[spriteLocation].think(self.mazeSprites)

    def request(self, spriteNum, command):
        spriteLocation = self.spriteLocations[spriteNum]
        try:

            if command in self.MOVEMENTS:
                sprite = self.mazeSprites[spriteLocation]
                peekedSprite = self.peek(command, spriteLocation)

                if peekedSprite == None or peekedSprite.getType() in Maze.MOVEABLE_TILES:

                    if sprite.getType() == 'bullet':
                        self.mazeSprites[spriteLocation].setColor('laser')

                    changes = self.moveSprite(command, spriteNum)
                    return changes

                elif sprite.getType() == 'bullet' and peekedSprite != None:
                    killPosition = None
                    if peekedSprite.getType() == 'snake':
                        killPosition = self.killSprite(peekedSprite.getID())
                    bulletPosition = self.killSprite(sprite.getID())
                    return {'update': [bulletPosition, killPosition], 'computer sprite': True}

            elif command == ord(" "):
                sprite = self.mazeSprites[spriteLocation]
                return self.addProjectile(sprite, spriteLocation)

            elif command == ord("w"):
                sprite = self.mazeSprites[spriteLocation]
                return self.addProjectile(sprite, spriteLocation, 0)

            elif command == ord("a"):
                sprite = self.mazeSprites[spriteLocation]
                return self.addProjectile(sprite, spriteLocation, 3)

            elif command == ord("s"):
                sprite = self.mazeSprites[spriteLocation]
                return self.addProjectile(sprite, spriteLocation, 2)

            elif command == ord("d"):
                sprite = self.mazeSprites[spriteLocation]
                return self.addProjectile(sprite, spriteLocation, 1)

                # return {}

        except:
            self.mazeTiles[0] = Sprite()
            return {'update': [0]}
        return {}

    def peek(self, direction, start):
        spaceSprite = self.mazeSprites[start + self.getMovementNum(direction)]
        if spaceSprite == None:
            spaceTile = self.mazeTiles[start + self.getMovementNum(direction)]
            if spaceTile == None:
                return None
            else:
                return spaceTile
        else:
            return spaceSprite

    def moveSprite(self, command, spriteNum):
        spriteLocation = self.spriteLocations[spriteNum]
        destination = spriteLocation + self.getMovementNum(command)
        self.mazeSprites[destination] = self.mazeSprites[spriteLocation]
        self.mazeSprites[spriteLocation] = None
        self.mazeSprites[destination].setPosition(destination)
        self.mazeSprites[destination].setDirection(command)
        self.spriteLocations[spriteNum] = destination
        return {'update': [spriteLocation, destination]}

    def getMovementNum(self, direction, indexMovements=True):
        if indexMovements:
            index = self.MOVEMENTS.index(direction)
        else:
            index = direction
        if index == 0:
            return -self.columns
        elif index == 1:
            return 1
        elif index == 2:
            return self.columns
        elif index == 3:
            return -1

    def printMaze(self):
        print(self.mazeTiles)
        for i in range(self.totalSpaces):
            if i % self.columns == 0:
                print()
            sprite = self.mazeSprites[i]
            if sprite == None:
                tile = self.mazeTiles[i]
                if tile == None:
                    print(" ", end='')
                else:
                    print(tile.getSymbol(), end='')
            else:
                print(sprite.getSymbol(), end='')
        print()

    def getSpace(self, index):
        foreground = None
        background = None
        sprite = self.mazeSprites[index]
        tile = self.mazeTiles[index]
        if sprite == None:
            if tile == None:
                return (" ", "white", None)
            else:
                return (tile.getSymbol(), tile.getForeground(), tile.getBackground())
        else:
            foreground = sprite.getForeground()
            background = sprite.getBackground()
            if background == None and tile != None:
                background = tile.getBackground()
            return (sprite.getSymbol(), foreground, background)

    def getColumns(self):
        return self.columns

    def getRows(self):
        return self.rows

    def getTotalSpaces(self):
        return self.totalSpaces

    def getMaze(self):
        return self.mazeTiles

    def getComputerActiveSprites(self):
        return self.computerActiveSprites

    def getPlayerSpriteID(self):
        return self.playerControlledSprite

    def getSprites(self):
        return self.sprites

    def getSpriteLocation(self, spriteNum):
        return self.spriteLocations[spriteNum]