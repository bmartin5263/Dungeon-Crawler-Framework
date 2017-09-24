# Dungeon Crawler Framework Concept
A proof of concept for a text-based dungeon crawler/Zelda style game written in Python using curses and Threading. 
The purpose for this POC is to experiment with curses on creating text-based games and threading to enable computer controlled
sprites acting within the dungeon.

## Getting Started
__Language Version:__ Python 3.5

__Usage:__
```
$ python3 main.py <maze_text_file>
```
The Tetris repository includes the following python modules:
* main.py
* computer_player.py
* game.py
* maze.py
* player.py
* sprite.py

This repository also includes text files that defines mazes to test the framework with.

This module does not require the download of any third-party modules and only uses standard Python library modules.

## How To Play
### Controls
* __arrow keys -__ Move left, right, up, down
* __w, a, s, d__ - Fire laser left, right, up, down
* __space bar__ - Fire laser in facing direction
* __q -__ Quit 