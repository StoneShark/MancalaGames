# Mancala Games #
The goal of Mancala Games is to create a means to play a variety of mancala games allowing easy adjustment of game rules. Once a favorite set of game rules is selected, be able to easily return to those rules and play games against a reasonably competent and efficient computer opponent.

## Overview ##

Mancala Games only supports two row mancala games. Stores are optional and there are 50 or so other game parameters. Three computer players are provided: Negamaxer can only be used in games with alternating turns and is a slightly optimized version of the MiniMaxer. The Monte Carlo Tree Search doesn't play well[^1].

There are 3 ways to startup Mancala Games:


1. **mancala_games.pyw** - allows adjustment of all parameters, does some error checking, game configurations can loaded, saved and played.
1. **play_mancala.pyw** - opens a window showing all games that are preconfigured, shows a tool tip of the About description for each game and allows it to be launched.
1. **play.py** - allows starting a preconfigured game from a command line or via short cut.

Game configurations are stored in plain-text, json-string formatted files. They may be edited directly. Parameters with default values need not be included.

## Code Overview ##
I’ve read that code is more testable if it is organized in a complex network of simple objects instead of a small set of complex objects. The evolution of Mancala Games has embraced the complex network of simple objects concept; possibly, it’s gone too far.

Game play is broken up into small steps and each step is implemented as a decorator chain of operations. Each decorator chain is created when the game class is initialized, minimizing the number of flags that need to be checked during game play[^2]. All steps are controlled by game rules:


* New Game - initializes a game or round
* Allowables - determines what holes may be played
* Moves - determines valid moves for computer player
* Incrementer - increments clockwise, counter-clockwise, past blocks, etc.
* Sow Starter - processes start hole by determining the number of seeds to sow possibly leaving one seed
* Get Direction - determines which specific direction to sow 
* Sower - sows the seeds (uses incrementer)
* Capt_Ok - determines if the contents of a single hole can be captured
* Capturer - executes the capture operations (uses capt_ok and incrementer)
* Ender - ends a move, determines if the next player must past, if the game is over, etc.
* Quitter - when the user chooses to end the game, do something fair to determine winner
* Game String - used for the game logger to prepare text formatted game state messages (utf-8)

## Compatibility ##
Mancala games can be run under Windows 10 & 11 and requires standard python 11 (including Tk)[^3].

Development of Mancala Games uses many specialized tools: The UI definition table is in Excel (an open-source alternative crashed on the large table in Window 11 too often). GNU-WIN32 make, grep and core utilities are used to script the build and test processes. Pytest is the test framework (Excel files with macros are used to create test cases stored as CSV files for actual test code). Pyinstaller is used to create standalone executables. Documentation diagrams were created in LibreOffice Draw with pdf versions saved.

[^1]: Perhaps the default parameters are bad. There could also be an implementation error.

[^2]: Speed isn't an issue for moves by human players but the computer players simulate very many moves to choose one. One profiling experiment noted nearly a second deciding to return a constant (for direction).

[^3]: Pyinstaller creates a nice playable directory, but Windows doesn't seem to support relative-path shortcuts so it currently isn't in the repo. 
