# -*- coding: utf-8 -*-
"""Goal: for given game(s), test two players against eachother.
See --help or exper_config for how to configure the players.

Created on Sun Oct 15 09:45:43 2023
@author: Ann"""

import sys

import play_game
import exper_config


def print_data(ofile):
    """Print the configuration and outcome data"""

    print('\n', game.info.name, sep='', file=ofile)
    print('True', tplayer if tplayer else 'Random', file=ofile)
    print('False', fplayer if fplayer else 'Random', file=ofile)
    print('\n', gstats, sep='', file=ofile)

    win_pct = gstats.wins[True] / gstats.total
    print(f'\n{gname:20} True win %={win_pct:10.2%}', file=ofile)



game_players_gen, config = exper_config.get_configuration()

if config.output:
    # start the file (also clears an existing one)
    with open(f'data/{config.output}.txt', 'w', encoding='utf-8') as file:
        print('Challenge:\n', config, sep='', file=file)


for game, fplayer, tplayer, gname in game_players_gen:

    print('\n', gname, sep='')
    print('True', tplayer if tplayer else 'Random')
    print('False', fplayer if fplayer else 'Random')

    gstats = play_game.play_games(game, fplayer, tplayer,
                                  config.nbr_runs, config.save_logs)

    if config.output:
        with open(f'data/{config.output}.txt', 'a', encoding='utf-8') as file:
            print_data(file)
    else:
        print_data(sys.stdout)
