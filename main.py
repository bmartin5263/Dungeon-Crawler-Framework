from curses import wrapper
from game import Game
import sys

def main(stdscr):
    maze = "GenericMaze.txt"

    if len(sys.argv) > 1:
        try:
            maze = str(sys.argv[1])
        except:
            pass

    game = Game(stdscr, maze)
    game.play()


if __name__ == '__main__':
    wrapper(main)
