# -*- coding: utf-8 -*-
"""Goal: for a particular game(s) compare different choices
for a parameter against a base configuration.

exper_config is used to configure the base player.

One parameter can be varied at a time; the range parameters
are provided as input.

Created on Sat Oct  5 08:49:08 2024
@author: Ann"""


# %%  imports

import argparse
import logging
import os
import sys

import ana_logger
import exper_config
import param_ops
import play_game

from context import ai_player
from context import cfg_keys as ckey
from context import game_logger
from context import man_config


# %% loggers

logger = logging.getLogger()

# disable the game logger
game_logger.game_log.active = False


# %%  constants

PATH = '../GameProps/'
BAD_CFG = 'all_params.txt'
INDEX = [fname[:-4] for fname in os.listdir(PATH) if fname != BAD_CFG]

PARAM_KEYS = [ckey.ACCESS_M,
              ckey.CHILD_CNT_M,
              ckey.EMPTIES_M,
              ckey.EVENS_M,
              ckey.SEEDS_M,
              ckey.STORES_M,
              ckey.REPEAT_TURN,

              ckey.MCTS_BIAS,
              ckey.MCTS_NODES,
              ckey.MCTS_POUTS]

# %% global variables

cargs = None


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
                        choices=PARAM_KEYS,
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

    parser.add_argument('--restart', action='store_true',
                        help="""Do not append to the output file.""")

    return parser


def process_command_line():
    """Process the command line arguments."""

    global cargs

    parser = define_parser()
    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit()

    ana_logger.config(logger, cargs.output, cargs.restart)
    logger.info(cargs)


# %%

def parametrize():
    """Load the game, configure the players.
    Params are only changed for vary_player.
    Play the specified number of games for each parameter value
    in the spceified range."""

    game, pdict = man_config.make_game(PATH + cargs.game + '.txt')
    logger.info('Starting player dictionary %s\n.', pdict)

    base_player = exper_config.build_player(game, pdict, cargs.base_player)
    logger.info('Base %s', str(base_player) if base_player else 'random')

    vary_player = ai_player.AiPlayer(game, pdict)
    param_ops.add_algo_name(vary_player)
    params = param_ops.get_params(vary_player)
    logger.info('Starting params:\n %s', params)

    results = {}
    for pvalue in range(*cargs.range):

        params[cargs.vparam] = pvalue
        param_ops.update_player(vary_player, params)
        logger.info('Testing:\n %s', params)

        results[pvalue] = play_game.get_win_percent(game,
                                                    base_player,
                                                    vary_player,
                                                    cargs.nbr_runs)
        logger.info('True win= %8.3f%%', results[pvalue] * 100)

    return results


# %% main

if __name__ == '__main__':

    process_command_line()
    data_dict = parametrize()
    logger.info(data_dict)
    ana_logger.close(logger)
