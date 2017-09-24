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

## How It Works
The program uses a combination of python modules, specifically curses and threading in order to create a real time Zelda
style dungeon crawler game, albeit a very primitive one.

### Threading
The program runs with three distinct threads: the main thread, a thread for user input, and a thread for computer input.
The user thread has a handle to control its own sprite (@) while the computer thread handles an array of sprites that it
commands virtually simultaneously. 

The threads (contained within the _game_ module) issue requests to the _board_, in which a lock is enabled to ensure 
only one request it made at a time, and the board returns a result and updates the global state accordingly.

### Modules / Objects

__game__- Handles the global state and user inputs to allow the user to interact with the maze as well as spawning a 
thread for the computer to control all of its sprites within the maze. 

__maze__- Contains all the sprites and tiles inside of a one dimensional array. Handles user input to manipulate the
sprites within the maze.

__sprite__- Defines individual characters within the maze and how they may interact with eachother and how they appear
to the user.