# -*- coding: utf-8 -*-
"""Goal: for given game(s), test two players against eachother.

Created on Sun Oct 15 09:45:43 2023
@author: Ann"""

# %%  imports


import play_game
import exper_config


# %% experiment

game_players_gen, config = exper_config.get_configuration()

if config.output:
    print("challenge doesn't yet handle output files")


for game, tplayer, fplayer in game_players_gen:

    gstats = play_game.play_games(game, tplayer, fplayer,
                                  config.nbr_runs, config.save_logs)
    print(gstats)
