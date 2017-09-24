import curses
import threading
from player import Player
from computer_player import ComputerPlayer
from maze import Maze

class Game():
    HUMAN = 0
    COMPUTER = 1
    LEGAL_INPUT = (ord('k'),
                   ord(' '),
                   ord('q'),
                   ord('w'),
                   ord('a'),
                   ord('s'),
                   ord('d'),
                   curses.KEY_UP,
                   curses.KEY_RIGHT,
                   curses.KEY_DOWN,
                   curses.KEY_LEFT)

    def __init__(self, screen, maze):
        self.maze = Maze(maze)
        self.mazeColumns = 0
        self.mazeRows = 0
        self.mazeSpaces = 0
        self.playerID = 0
        self.computerIDs = []
        self.players = []
        self.threads = []
        self.lock = threading.RLock()
        self.isComplete = False
        self.usingScreen = False
        self.screen = screen
        self.player = Player(0)
        self.computer = ComputerPlayer(1)

        curses.curs_set(0)
        curses.start_color()
        ### No Backgrounds ###
        curses.init_pair(1, 15, curses.COLOR_BLACK)  # white
        curses.init_pair(2, 7, curses.COLOR_BLACK)  # gray
        curses.init_pair(3, 8, curses.COLOR_BLACK)  # dark gray
        curses.init_pair(4, 9, curses.COLOR_BLACK)  # red
        curses.init_pair(5, 11, curses.COLOR_BLACK)  # yellow
        curses.init_pair(6, 10, curses.COLOR_BLACK)  # green
        curses.init_pair(7, 12, curses.COLOR_BLACK)  # blue
        curses.init_pair(8, 14, curses.COLOR_BLACK)  # cyan
        curses.init_pair(9, 13, curses.COLOR_BLACK)  # purple
        ### Blue ###
        curses.init_pair(10, 15, curses.COLOR_BLUE)  # white
        curses.init_pair(11, 10, curses.COLOR_BLUE)  # green
        curses.init_pair(12, 9, curses.COLOR_BLUE)  # red
        curses.init_pair(13, 11, curses.COLOR_BLUE)  # yellow

        self.CURSES_COLOR_DICT = {
            'white': {None: curses.color_pair(1), 'blue': curses.color_pair(10)},

            'gray': {None: curses.color_pair(2)},

            'dark gray': {None: curses.color_pair(3)},

            'red': {None: curses.color_pair(4), 'blue': curses.color_pair(12)},

            'yellow': {None: curses.color_pair(5), 'blue': curses.color_pair(13)},

            'green': {None: curses.color_pair(6), 'blue': curses.color_pair(11)},

            'blue': {None: curses.color_pair(7)},

            'cyan': {None: curses.color_pair(8)},

            'purple': {None: curses.color_pair(9)},

            None: {'blue': curses.color_pair(10)},
        }

    def waitForInput(self, pType):
        while not self.isComplete:
            if pType == Game.COMPUTER:
                idList = list(self.computer.getActiveSpriteIDs())
                for idNum in idList:
                    if not self.isComplete:
                        command = self.computer.think(idNum, self.maze)
                        if command is None:
                            continue
                        else:
                            self.makeRequest(idNum, command)

            elif pType == Game.HUMAN:
                command = self.recievePlayerInput()
                if command in Game.LEGAL_INPUT:
                    if command == ord('q'):
                        self.isComplete = True
                        return
                    self.makeRequest(self.player.getSpriteID(), command)

    def makeRequest(self, idNum, command):
        self.lock.acquire()

        changes = self.maze.request(idNum, command)

        if changes is not None:

            if 'update' in changes.keys():
                self.updateScreen(changes['update'])
            if 'computer sprite' in changes.keys():
                self.computer.setActiveSpriteIDs(list(self.maze.getComputerActiveSprites()))
            if 'gameover' in changes.keys():
                self.isComplete = True

        self.lock.release()

    def recievePlayerInput(self):
        while not self.isComplete:
            k = self.screen.getch()
            return k

    def updateScreen(self, changes):
        self.lock.acquire()
        for change in changes:
            if change is not None:
                spriteInformation = self.maze.getSpace(change)
                self.screen.addstr(change // self.mazeColumns, change % self.mazeColumns, spriteInformation[0],
                                   self.CURSES_COLOR_DICT[spriteInformation[1]][spriteInformation[2]])
        self.screen.move(self.mazeRows, 0)
        self.screen.clrtobot()
        self.screen.addstr(self.mazeRows,0,"Comp Sprite IDs: {}".format(str(self.computer.getActiveSpriteIDs())))
        self.screen.addstr(self.mazeRows+1,0,"Player Sprite ID: {}".format(str(self.player.getSpriteID())))
        self.screen.refresh()
        self.lock.release()

    def drawEntireMaze(self):
        for i in range(self.mazeSpaces):
            spriteInformation = self.maze.getSpace(i)
            self.screen.addstr(i // self.mazeColumns, i % self.mazeColumns, spriteInformation[0],
                               self.CURSES_COLOR_DICT[spriteInformation[1]][spriteInformation[2]])
        self.screen.refresh()

    def initializeMaze(self):
        self.mazeColumns = self.maze.getColumns()
        self.mazeRows = self.maze.getRows()
        self.mazeSpaces = self.maze.getTotalSpaces()

        playerID = self.maze.getPlayerSpriteID()
        computerIDs = list(self.maze.getComputerActiveSprites())

        self.player.setSpriteID(playerID)
        self.computer.setActiveSpriteIDs(computerIDs)

    def createThreads(self):
        self.threads = []
        humanThread = threading.Thread(target=self.waitForInput, args=(Game.HUMAN,))
        computerThread = threading.Thread(target=self.waitForInput, args=(Game.COMPUTER,))
        self.threads.append(humanThread)
        self.threads.append(computerThread)

    def play(self):
        self.screen.clear()
        self.screen.refresh()
        self.initializeMaze()
        self.createThreads()
        self.drawEntireMaze()
        for t in self.threads:
            t.start()
        for t in self.threads:
            t.join()