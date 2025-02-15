Mancala Games Distribution Files:

mancala_games.exe       Starts the mancala games engine. 
                        Load, edit and save game config files.
                        Play any game configuration.
                        Always runs from a command window to support live log display.

play_mancala.exe        Pops-up a menu of all preconfigured games (GameProps), allowing 
			selection of any to play.
                        
play.exe                A command line interface to play game configuration files.
			Windows short cuts can be created to directly launch any
			specific game with this executable.
                        Usage:     play.exe <game>
                        Example:   play.exe Wari

mancala.ini		Define parameters to control Mancala UI. This is intended to be 
			user edited--there is no in game way to change most of the 
			parameters. If this file does not exist, it will be created with
			default values, but the comments will be missing. The difficulty 
			option is not included by default, because any difficulty set in
			this file will override the difficulty in the game files.

GameProps		The configuration files for the pre-configured games.
			Edit or rename these as you like or create a parallel directory
			with your favorites and own games. 
			
			mancala_games starts in this directory when loading an initial 
			game; it does look in the current and parent directories for the 
			GameProps (a few other places are checked too: docs, help, src).

help                    Help files. Start with mancala_help.html

logs                    Saved game logs are stored here.

game_params.txt         Used by mancala_games. Editing these file is not recommended.
game_param_descs.txt

_internal               Dragons here. Don't touch.
                        It's the python runtime support files.
