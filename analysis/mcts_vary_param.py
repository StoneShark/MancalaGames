# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 08:49:08 2024
@author: Ann"""


# %%  imports

import argparse
import os
import sys

import play_game
import exper_config

from context import ai_player
from context import cfg_keys as ckey
from context import man_config
from context import game_logger


# %% disable game logger

game_logger.game_log.active = False


# %%  constants

PATH = '../GameProps/'
BAD_CFG = 'all_params.txt'
INDEX = [fname[:-4] for fname in os.listdir(PATH) if fname != BAD_CFG]

# keys in config file
MKEYS = [ckey.MCTS_BIAS, ckey.MCTS_NODES, ckey.MCTS_POUTS]

# param name
MCTS_KEYS = ['bias', 'nodes', 'pouts']


# %% global variables

cargs = None
log_file = None


# %%  command line args

def define_parser():
    """Define the command line arguements."""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=exper_config.PLAYER_CONFIG_MSG)

    parser.add_argument('game', action='store',
                        choices=list(INDEX),
                        help="""Select the game parametrize.""")

    parser.add_argument('--nbr_runs', action='store',
                        default=250, type=int,
                        help="""Select the number of games to simulate
                        for each test pair.
                        Default: %(default)s""")

    parser.add_argument('--vparam', action='store', required=True,
                        choices=MCTS_KEYS,
                        help='Parameter to vary.')

    parser.add_argument('--range', nargs=3, type=int, required=True,
                        help="""Vary the parameter as range(a, b, c).
                        Bias values / 1000.""")

    parser.add_argument('--base_player', action='store',
                        type=str, nargs='+',
                        help="""Define player to compare against. See below.""")

    parser.add_argument('--output', action='store',
                        help="""Save the ouptut to the specified file.
                        Skip for output to console only.""")
    return parser


def process_command_line():
    """Process the command line arguments."""

    global cargs, log_file

    parser = define_parser()
    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit()

    if cargs.output:
        log_file = open(cargs.output, 'w', encoding='utf-8')

    dbl_print(cargs)


# %%  print & saver

def dbl_print(*args, sep=' '):
    """Print the args with the specified separator.
    If log_file is not None, print it there too."""

    string = sep.join(str(arg) for arg in args)
    print(string)
    if log_file:
        print(string, file=log_file)


# %%



def parametrize():
    """."""

    game, pdict = man_config.make_game(PATH + cargs.game + '.txt')

    if ckey.ALGORITHM not in pdict or pdict[ckey.ALGORITHM] != 'montecarlo_ts':
        dbl_print("Overriding config'ed algorithm to montecarlo_ts.")
        pdict[ckey.ALGORITHM] = 'montecarlo_ts'
    if (ckey.AI_PARAMS not in pdict
            or any(key not in pdict[ckey.AI_PARAMS] for key in MKEYS)):
        dbl_print('Not all MCTS params in config, using default(s).')

    base_player = exper_config.build_player(game, pdict, cargs.base_player)
    vary_player = ai_player.AiPlayer(game, pdict)

    dbl_print('Base', str(base_player) if base_player else 'random')

    pidx = MCTS_KEYS.index(cargs.vparam)
    params = [vary_player.algo.bias,
              vary_player.algo.new_nodes,
              vary_player.algo.nbr_pouts]

    results = {}
    for pvalue in range(*cargs.range):

        params[pidx] = pvalue if pidx else pvalue / 1000
        vary_player.algo.set_params(*params)
        dbl_print('Testing:', str(vary_player.algo))

        results[pvalue] = play_game.get_win_percent(game,
                                                    base_player,
                                                    vary_player,
                                                    cargs.nbr_runs)
        dbl_print(f'True win= {results[pvalue]:8.3%}')

    return results


# %% main

if __name__ == '__main__':

    process_command_line()
    data_dict = parametrize()
    dbl_print(data_dict)

    if log_file:
        log_file.close()
