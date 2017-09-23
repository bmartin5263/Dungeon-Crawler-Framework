from curses import wrapper
from game import Game

def main(stdscr):
    game = Game(stdscr)
    game.playMaze("Arena.txt")


if __name__ == '__main__':
    wrapper(main)
