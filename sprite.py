import random
import curses
import time

class Sprite():
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    MOVEMENTS = (curses.KEY_UP, curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_LEFT)
    TYPES = {
        ' ': 'blank',
        '@': 'player',
        'S': 'snake',
        'O': 'wall',
        '■': 'wall',
        '?': 'unknown'
    }
    COLORS = ('white', 'red', 'blue', 'cyan', 'purple', 'green', 'yellow', 'gray')
    VIBRANTS = ('red', 'blue', 'cyan', 'purple', 'green', 'yellow')
    CYCLES = {'white': 'red', 'red': 'yellow', 'yellow': 'green', 'green': 'blue', 'blue': 'red'}
    LASER = {'red': 'yellow', 'yellow': 'red'}

    DEFAULTS = {
        '@': {'symbol': '@', 'type': 'player', 'role': 'sprite', 'fore color': 'white', 'behavior': None, 'delay': 0,
              'health': 1
            , 'human': True, 'back color': None},

        'S': {'symbol': 'S', 'type': 'snake', 'role': 'sprite', 'fore color': 'yellow', 'behavior': None, 'delay': 1,
              'health': 1
            , 'human': False, 'back color': None},

        '-': {'symbol': '-', 'type': 'bullet', 'role': 'projectile', 'fore color': 'red', 'behavior': 'travel',
              'delay': .04, 'health': 1
            , 'human': False, 'back color': None},

        'O': {'symbol': 'O', 'type': 'wall', 'role': 'tile', 'fore color': 'purple', 'behavior': None, 'delay': 0,
              'health': 1
            , 'human': False, 'back color': None},

        '■': {'symbol': '■', 'type': 'wall', 'role': 'tile', 'fore color': 'gray', 'behavior': None, 'delay': 0,
              'health': 1
            , 'human': False, 'back color': None},

        '?': {'symbol': '?', 'type': 'unknown', 'role': 'unknown', 'fore color': 'red', 'behavior': None, 'delay': 0,
              'health': 0
            , 'human': False, 'back color': None},

        'W': {'symbol': ' ', 'type': 'water', 'role': 'tile', 'fore color': None, 'behavior': None, 'delay': 0,
              'health': 0
            , 'human': False, 'back color': 'blue'},
    }

    def __init__(self, idNum=None, symbol='?', position=-1):
        ## IDENTIFICATION ##
        self.id = idNum
        self.type = Sprite.DEFAULTS[symbol]['type']
        self.role = Sprite.DEFAULTS[symbol]['role']

        ## AI INFORMATION ##
        self.playerControlled = Sprite.DEFAULTS[symbol]['human']
        self.behavior = Sprite.DEFAULTS[symbol]['behavior']  # How Sprite will think
        self.health = Sprite.DEFAULTS[symbol]['health']  # Health
        self.alive = True  # Denotes sprite is still able to act
        self.delay = Sprite.DEFAULTS[symbol]['delay']  # Minimum Time to wait before action
        self.lastMove = time.time()  # Time of last move
        self.facing = Sprite.EAST

        ## GUI ##
        self.symbol = Sprite.DEFAULTS[symbol]['symbol']  # Symbol to appear in maze
        self.position = position  # Denotes sprite is a background object
        self.initialColor = Sprite.DEFAULTS[symbol]['fore color']
        self.foreground = Sprite.DEFAULTS[symbol]['fore color']
        self.background = Sprite.DEFAULTS[symbol]['back color']

    def __repr__(self):
        return self.symbol

    def getID(self):
        return self.id

    def setSymbol(self, symbol):
        self.symbol = str(symbol[0])

    def setColor(self, color):
        if color == 'random':
            self.foreground = random.choice(Sprite.VIBRANTS)
        elif color == 'cycle':
            self.foreground = Sprite.CYCLES[self.foreground]
        elif color == 'laser':
            self.foreground = Sprite.LASER[self.foreground]
        elif color in Sprite.COLORS:
            self.foreground = color
        else:
            self.foreground = 'purple'

    def setDelay(self, delay):
        self.delay = delay

    def setDirection(self, movementCommand):
        self.facing = Sprite.MOVEMENTS.index(movementCommand)

    def canAct(self):
        t = time.time()
        if t - self.lastMove >= self.delay:
            return True
        return False

    def hasActed(self):
        self.lastMove = time.time()

    def getSymbol(self):
        return self.symbol

    def getType(self):
        return self.type

    def getColor(self):
        return self.initialColor

    def getForeground(self):
        return self.foreground

    def getBackground(self):
        return self.background

    def getBehavior(self):
        return self.behavior

    def getRole(self):
        return self.role

    def setPosition(self, position):
        self.position = position

    def getDirection(self):
        return self.facing