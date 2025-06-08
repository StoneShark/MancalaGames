# Mancala Games #
The goal of Mancala Games is to create a means to play a variety of mancala games allowing easy adjustment of game rules. Once a favorite set of game rules is selected, be able to easily return to those rules and play games against a reasonably competent and efficient computer opponent.

## Overview ##

Mancala Games only supports two row mancala games. Stores are optional and there are 50 or so other game parameters (see [Mancala Game Parameters](https://html-preview.github.io/?url=https://github.com/StoneShark/MancalaGames/blob/main/docs/game_params.html)).  Many preconfigured games are provided (see [Mancala Game Configurations](https://html-preview.github.io/?url=https://github.com/StoneShark/MancalaGames/blob/main/docs/about_games.html)). 

Three computer players are provided: Negamaxer can only be used in games with alternating turns and is a slightly optimized version of the MiniMaxer. The Monte Carlo Tree Search works best for games in which it is hard to configure the MiniMaxer scorer.

There are 3 ways to startup Mancala Games:

1. **man_games_editor.pyw** - allows adjustment of all parameters, does some error checking, game configurations can be loaded, saved, edited and played.
1. **play_mancala.pyw** - allows any preconfigure game to be selected and play. Filter options control which game appear in the game list. Game parameters may not edited.
1. **play.py** - allows starting a preconfigured game from a command line or via short cut.

Game configurations are stored in plain-text, json-string formatted files. They may be edited directly. Parameters with default values need not be included.

## Distribution Files ##

To download and play Mancala Games on Windows, get the [MancalaGames.tgz](https://github.com/StoneShark/MancalaGames/blob/main/MancalaGames.tgz) file. It is a 
self contained set of executables and all required files. No installation is
required, just expand the zip file which requires 34MB.

## Code Overview ##
I’ve read that code is more testable if it is organized in a complex network of simple objects instead of a small set of complex objects. The evolution of Mancala Games has embraced the complex network of simple objects concept; possibly, it’s gone too far (see [GameClasses.pdf](https://github.com/StoneShark/MancalaGames/blob/main/docs/GameClasses.pdf)).

Game play is broken up into small steps and each step is implemented as a decorator chain of operations. Each decorator chain is created when the game class is initialized, minimizing the number of flags that need to be checked during game play[^1]. All steps are controlled by game parameters:


* New Game - initializes a game or round
* Allowables - determines what holes may be played
* Moves - determines valid moves for computer player
* Incrementer - increments clockwise, counter-clockwise, past blocks, etc.
* Drawer - start a move by taking the seeds from the selected hole, determining the number of seeds to sow possibly leaving one seed, possibly unlocking the hole
* Make Child - stops sowing when a child should be made and is the test for making a child in the capturer
* Get Direction - determines which specific direction to sow 
* Sower - sows the seeds (uses incrementer)
* Capt_Ok - determines if the contents of a single hole can be captured
* Capturer - executes the capture operations (uses capt_ok and incrementer)
* Ender - ends a move, determines if the next player must pass, if the game is over, etc.
* Quitter - when the user chooses to end the game, do something fair to determine winner
* Game String - used for the game logger to prepare text formatted game state messages (utf-8)

## Compatibility ##
Mancala games can be run under Windows 10 & 11. Only standard python 3.12 (including Tk) is required so running from the source files is likely supported in other operating systems.

Development of Mancala Games uses many specialized tools: The MancalaGames UI parameter definition table is in Excel. GNU-WIN32 make, grep and core utilities are used to script the build and test processes. Pytest is the test framework (Excel files are used to create test cases which are converted to CSV files by Pandas for actual test code). Pyinstaller is used to create standalone executables. Documentation diagrams were created in LibreOffice Draw with pdf versions saved.


[^1]: Speed isn't an issue for moves by human players but the computer players simulate very many moves to choose one. One profiling experiment noted nearly a second deciding to return a constant (for direction); the decorator chain resolved it to basically zero.

