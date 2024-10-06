# -*- coding: utf-8 -*-
"""Build command lines options that allow selecting games
and configuring players.

get_configuration is intended interface to generate
    generator for: games tplayer fplayer
    other config options

Created on Sun Jul 28 13:41:27 2024
@author: Ann"""

# %% imports

import argparse
import itertools as it
import json
import logging
import os
import sys

import ana_logger
from context import ai_player
from context import man_config


logger = logging.getLogger(__name__)


# %% contants

ALL = 'all'

PATH = '../GameProps/'
BAD_CFG = 'all_params.txt'

INDEX = [fname[:-4] for fname in os.listdir(PATH) if fname != BAD_CFG]


# %%  player config

PLAYER_CONFIG_MSG = \
f"""\
Player configurations:
    as_config [algo <aname>] [diff <level>]   - config file player with substitions
    algo <aname> [params <values>]            - specified algo with either
                                                default params or those specified
                                                scorer config will be per config file
    pdict <filename>                          - specify a player dict file (in pdicts dir)
    random                                    - player will make random moves (default)

where:
    <aname>    is one of {set(ai_player.ALGORITHM_DICT.keys())}
    <level>    is one of 1, 2, 3, 4 for difficulty
    <values>   is either
                   an integer, for depth of minimax or negamax search
                   bias (float), new_nodes (int), number play outs (int)
                      for the monte carlo tree search"""

# %% command line proc


def define_parser():
    """Define the command line arguements."""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=PLAYER_CONFIG_MSG)

    parser.add_argument('--game', action='append',
                        choices=[ALL] + INDEX, required=True,
                        help="""Select the games to simulate. Use multiple
                        options to select multiple games.""")

    parser.add_argument('--nbr_runs', action='store',
                        default=10, type=int,
                        help="""Select the number of games to simulate.
                        Default: %(default)s""")

    parser.add_argument('--save_logs', action='store_true',
                        help="""Save the game logs. Only one game maybe
                        selected and nbr_games must be < 50.
                        Games will be slowed to 1 per second.
                        Default: %(default)s""")

    parser.add_argument('--output', action='store',
                        default=None,
                        help="""Output file. Default: console output only""")

    parser.add_argument('--restart', action='store_true',
                        help="""Do not append to the output file.""")

    parser.add_argument('--tplayer', action='store',
                        type=str, nargs='+',
                        help="""Define player t. See below.""")
    parser.add_argument('--fplayer', action='store',
                        type=str, nargs='+',
                        help="""Define player f. See below""")

    return parser


def process_command_line():
    """Process the command line and look for some basic errors."""

    parser = define_parser()
    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit()

    if not cargs.game or cargs.game == [ALL]:
        cargs.game = INDEX

    if cargs.save_logs and (len(cargs.game) > 1 or cargs.nbr_runs > 50):
        print("save_logs only valid for <= 1 game and <= 50 runs.")
        sys.exit()

    # configure the root logger
    ana_logger.config(logging.getLogger(), cargs.output, cargs.restart)

    logger.info('Command line:')
    for var, val in vars(cargs).items():
        logger.info("   %s:   %s", var, val)
    return cargs


# %% build games and players

def build_player(game, pdict, arg_list):
    """Build and configure the player as spec'ed in the arg_list.
    Lots of things can go wrong ... not going to try to catch them
    ... exceptions will be be thrown."""
    # pylint: disable=too-many-branches

    player = None

    if not arg_list:
        pass

    elif arg_list[0] == 'as_config':

        player = ai_player.AiPlayer(game, pdict)

        for keyw, value in it.batched(arg_list[1:], n=2):
            if keyw == 'algo':
                player.set_algorithm(value)
            elif keyw == 'diff':
                player.difficulty = int(value)
            else:
                logger.info("Got confused in 'as_config'. Try --help.")
                sys.exit()

    elif arg_list[0] == 'algo':

        tdict = {}
        tdict['scorer'] = pdict['scorer']  # default minimaxer scorers are bad
        tdict['algorithm'] = arg_list[1]
        player = ai_player.AiPlayer(game, {'algorithm': arg_list[1]})

        nargs = len(arg_list)
        if nargs == 2:
            pass

        elif nargs == 3:
            player.algo.set_params(int(arg_list[2]))

        elif nargs == 6:
            player.algo.set_params(float(arg_list[3]),
                                   int(arg_list[4]),
                                   int(arg_list[5]))
        else:
            logger.info("Got confused in 'algo'. Try --help")
            sys.exit()

    elif arg_list[0] == 'pdict':

        with open('pdicts/' + arg_list[1], 'r', encoding='utf-8') as file:
            pdict = json.load(file)

        player = ai_player.AiPlayer(game, pdict)

    else:
        logger.info("Unknown player config: %s", arg_list[0])

    return player


def game_n_players_gen(cargs):
    """for each game specified on the command line,
    generate the game and players."""

    for gname in cargs.game:

        game, pdict = man_config.make_game(PATH + gname + '.txt')

        tplayer = build_player(game, pdict, cargs.tplayer)
        fplayer = build_player(game, pdict, cargs.fplayer)

        yield game, fplayer, tplayer, gname


def get_configuration():
    """Process the command line and return:
        a generator of tuples: game player1 player2
        an ExperConfig with the rest of the configuration"""

    cargs = process_command_line()

    return game_n_players_gen(cargs), cargs
