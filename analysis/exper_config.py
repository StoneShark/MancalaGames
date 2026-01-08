# -*- coding: utf-8 -*-
"""Build command lines options that allow selecting games
and configuring players.

get_configuration is the intended interface to generate
    generator for: games tplayer fplayer
    other config options

The player's are recreated for each game because the
have links back to the game object and must be
recreated for each game.

The help message contains details on the options.

PLAYER_CONFIG_MSG and build_player are available to
accept player configurations where the rest of the
options are not wanted.

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
from context import cfg_keys as ckey
from context import man_config
from context import man_path


logger = logging.getLogger(__name__)


# %% contants

ALL = 'all'

PATH = '../GameProps/'

INDEX = [fname[:-4] for fname in man_path.game_files()]

# --params is loaded into this var -- a global because it's used
# in two places -- to create the dataframe index and to generate the games
param_sets = None


def short_name(gname, pname):
    """Short names for when a params file is used."""

    return gname[:5] + '_' + pname


# %%  player config

PLAYER_CONFIG_MSG = \
f"""\
Player configurations:
    as_config [algo <aname>] [diff <level>]   - config file player with substitions
    algo <aname> [params <values>]            - specified algo with either
                                                default params or those specified
                                                scorer config will be per config file
    pdict <filename>                          - specify a player dict file
                                                (in pdicts dir, see the README there)
    random                                    - player will make random moves (default)

where:
    <aname>    is one of {set(ai_player.ALGORITHM_DICT.keys())}
    <level>    is one of 0, 1, 2, 3 for difficulty
    <values>   is either
                   an integer, for depth of minimax or negamax search
                   bias (float), new_nodes (int), number play outs (int)
                      for the monte carlo tree search"""

# %% command line proc


def define_parser(log_options=False):
    """Define the command line arguements."""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=PLAYER_CONFIG_MSG)

    parser.add_argument('--game', action='append',
                        choices=[ALL] + INDEX,
                        help="""Select the games to simulate. Use multiple
                        options to select multiple games.""")

    parser.add_argument('--file', action='store',
                        help="""Select a game file run. Only 1.""")

    parser.add_argument('--params', action='store',
                        help="""Provide a file with a list of parameter-change
                        experiments to run. A JSON file where
                        each tag-value is an experiment-name and
                        a parameter dictionary to override the base
                        game definition.
                        The file should be formatted as the named variants tag
                        in a game definition file,
                        but the base game is not required.
                        If multiple games are included the same
                        experiments are run on each game.""")

    parser.add_argument('--nbr_runs', action='store',
                        default=10, type=int,
                        help="""Select the number of games to simulate.
                        Default: %(default)s""")

    parser.add_argument('--max_moves', action='store',
                        default=0, type=int,
                        help="""Select the maximum number of
                        moves to make per game.  If 0, value is computed
                        as 500, then x2 if repeat turn possible,
                        then x4 if played in rounds.
                        Default: %(default)s.""")

    parser.add_argument('--end_all', action='store_true',
                        help="""Score all games as WIN or TIE;
                        no LOOPED or MAX_TURNS will be reported.
                        If these were to be reported, call game.end_game.""")

    parser.add_argument('--no_endless', action='store_true',
                        help="""Do not allow endless sows.
                        Only use this option if you know that you want it.
                        It is very slow (every move is simulated
                        to determine which holes are allowable).""")

    if log_options:
        parser.add_argument('--save_logs', action='store_true',
                            help="""Save the game logs. Only one game maybe
                            selected and nbr_games must be < 50.
                            Games will be slowed to 1 per second.
                            Default: %(default)s""")

        parser.add_argument('--live_log', action='store_true',
                            help="""Show the game log on the console.
                            Any nbr_games is allowed and games are not slowed.
                            Default: %(default)s""")

    parser.add_argument('--output', action='store',
                        default=None,
                        help="""Output file. Default: console output only""")

    parser.add_argument('--dconfig', action='store_true',
                        default=False,
                        help="""Include the game configuration in the output.
                        Default: %(default)s""")

    parser.add_argument('--restart', action='store_true',
                        help="""Do not append to the output file.""")

    parser.add_argument('--tplayer', action='store',
                        type=str, nargs='+',
                        help="""Define player t. See below.""")
    parser.add_argument('--fplayer', action='store',
                        type=str, nargs='+',
                        help="""Define player f. See below""")

    return parser


def process_command_line(log_options=False):
    """Process the command line and look for some basic errors."""
    global param_sets

    parser = define_parser(log_options)
    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit()

    if not log_options:
        cargs.save_logs = False
        cargs.live_log = False

    if cargs.file and cargs.game:
        print("Don't use --file and --game together.")
        sys.exit()

    if not cargs.file and not cargs.game:
        print("No game specified use --file or --game.")
        sys.exit()

    if cargs.file:
        gname, _ = os.path.splitext(os.path.basename(cargs.file))
        cargs.game = [gname]

    elif not cargs.game or cargs.game == [ALL]:
        cargs.game = INDEX

    if cargs.save_logs and (len(cargs.game) > 1 or cargs.nbr_runs > 50):
        print("save_logs only valid for <= 1 game and <= 50 runs.")
        sys.exit()

    # create the game index for the data frame index
    if cargs.params:
        man_config.read_params_data()
        with open(cargs.params, 'r', encoding='utf-8') as file:
            param_sets = json.load(file)

        cargs.gindex = [short_name(gname, pname)
                        for gname in cargs.game
                        for pname in param_sets.keys()]
    else:
        cargs.gindex = cargs.game

    # configure the root logger
    out_file = cargs.output + '.txt' if cargs.output else None
    ana_logger.config(logging.getLogger(), out_file, cargs.restart)

    logger.info('Command line:')
    for var, val in vars(cargs).items():
        logger.info("   %s:   %s", var, val)
    return cargs


# %% build games and players

def build_player(game, pdict, arg_list):
    """Build and configure the player as spec'ed in the arg_list.
    Lots of things can go wrong ... not going to try to catch them
    ... exceptions will be be thrown.

    Parameters
    ----------
    game : Mancala
        The game the player will be used with.

    pdict : dict
        The base player dictionary, that is, a dictionary that could
        be the toplevel key "player" from a configuration file.
        see GameProps/all_params.txt

    arg_list : list, str
        The list of strings collected by argparse from the command
        line arguments. See PLAYER_CONFIG_MSG.

    Returns
    -------
    player : AiPlayer
        AI player configured as described.
    """
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


def next_params(cargs, gname, gfile):
    """If any params were provided on the command line,
    read the game dict, update per each param dict, and
    yield a game and player dict for each.
    If params were not provided make the game and
    yield it.

    Game names are always the names from the command line."""

    if not cargs.params:
        game, pdict = man_config.make_game(gfile)
        object.__setattr__(game.info, ckey.NAME, gname)
        yield game, pdict
        return

    for pname, pdict in param_sets.items():

        game_dict = man_config.read_game(gfile)

        for vname, value in pdict.items():
                param = man_config.PARAMS[vname]
                man_config.set_config_value(
                    game_dict, param.cspec, param.option,
                    man_config.convert_from_file('Experiment', vname, value))

        game_dict[ckey.GAME_INFO][ckey.NAME] = short_name(gname, pname)
        game = man_config.game_from_config(game_dict)

        yield game, game_dict[ckey.PLAYER]


def game_n_players_gen(cargs):
    """For each game specified on the command line,
    generate the game and players."""

    if cargs.file:
        games = [(cargs.game[0], cargs.file)]
    else:
        games = [(gname, PATH + gname + '.txt') for gname in cargs.game]

    for gname, gfile in games:
        for game, pdict in next_params(cargs, gname, gfile):

            if cargs.dconfig:
                logger.info(game.params_str())
            if cargs.no_endless:
                game.disallow_endless(True)

            tplayer = build_player(game, pdict, cargs.tplayer)
            fplayer = build_player(game, pdict, cargs.fplayer)

            yield game, fplayer, tplayer, game.info.name


def get_configuration(log_options=False):
    """Process the command line and return:
        a generator of tuples: game player1 player2 and
        a namespace with the rest of the configuration

    The root logger is configured so that output maybe
    started here."""

    cargs = process_command_line(log_options)
    return game_n_players_gen(cargs), cargs
