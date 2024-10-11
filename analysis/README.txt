Top level analysis scripts:

challenge.py     Use exper_config to select game and configure players
                 useful for creating log files with different players
                  manually testing one player configuration against another
                  win percentage is reported for the tplayer

fair_games.py    Uses hypothesis testing to determine if games are likely
                 fair. Considers both 
                        false against true and 
                        game starter against non-starter.

optimize.py       Attempts to optimize the ai parameters for a game.
                  see the command line options (via --help) for details.

                  For minimaxer/negamaxer, the parameters considered 
                  are those listed  in the game configuration file, 
                  player, scorer keys (without easy_rand).

                  For montecarlo_ts, all three game parameters are
                  considered: bias, new nodes and play outs.

vary_param.py     Vary's one parameter through a range of values.
                  A base player configuration is provided and 
                  the range for the parameter are provided.
                  see the command line option (via --help) for details.


Support modules:

ana_logger.py     Python's logger is used to report most analysis results
                  a simple date/time stamp is added to each entry.
                  Output is always to the console, but also may be written
                  to a file.
                  This file provides the configuration and clean-up
                  functions used.

exper_config.py   Main command line options and game and player generator
                  for the analysis scripts. Player configuration may be used
                  without the rest.

param_ops.py      Support functions that isolate the differences between
                  where the parameters are stored in the AiAlgorithms.

play_game.py      The game player used for all analysis scripts. 
                  Key interfaces:
                      play_games
                      get_win_percent
                      play_one_game
                      GameStats - class of collected results
