# -*- coding: utf-8 -*-
"""Goal: for given game(s), test two players against eachother.

Created on Sun Oct 15 09:45:43 2023
@author: Ann"""

import sys

import play_game
import exper_config


def print_data(file):
    print('\n', game.info.name, sep='', file=file)
    print('True algo:', tplayer.algo if tplayer else 'Random',
          file=file)
    print('False algo:', fplayer.algo if fplayer else 'Random', '\n',
          file=file)
    print('\n', gstats, sep='', file=file)

    win_pct = ((gstats.stats['WINt-Sf'] + gstats.stats['WINt-St'])
               / gstats.total)
    print(f'\n{gname:20} True win %={win_pct:10.2%}', file=file)


# %% main

game_players_gen, config = exper_config.get_configuration()

# start the file (also clears an existing one)
with open(f'data/{config.output}.txt', 'w') as file:
    print('Challenge:\n', config, sep='', file=file)


for game, tplayer, fplayer, gname in game_players_gen:

    print(gname)
    gstats = play_game.play_games(game, tplayer, fplayer,
                                  config.nbr_runs, config.save_logs)

    if config.output:
        with open(f'data/{config.output}.txt', 'a') as file:
            print_data(file)
    else:
        print_data(sys.stdout)
