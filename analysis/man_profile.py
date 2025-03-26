# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 06:18:19 2023
@author: Ann"""

import argparse
import cProfile
import os
import sys

import exper_config
import play_game               # used indirectly in profile command


# %% constants

PATH = '../GameProps/'
BAD_CFG = '_all_params.txt'
INDEX = [fname[:-4] for fname in os.listdir(PATH) if fname != BAD_CFG]


SORT_OPTS = ['calls', 'cumulative', 'cumtime', 'file', 'filename',
             'module', 'ncalls', 'pcalls', 'line',
             'name', 'nfl', 'stdname', 'time', 'tottime']


ACTIONS = {'pick_move': 'tplayer.pick_move()',
           'allows': 'game.get_allowable_holes()',
           'play_game': 'play_game.play_one_game(game, fplayer, tplayer)',
           }


# %%  command line proc

def define_parser():
    """Define the command line arguements."""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=exper_config.PLAYER_CONFIG_MSG)

    parser.add_argument('--game', action='store',
                        choices=INDEX,
                        help="""Select the game to profile
                        from the GameProps folder.""")

    parser.add_argument('--file', action='store',
                        help="""Select a game configuration file to profile.
                        Use either --game or --file, not both.""")

    parser.add_argument('--tplayer', action='store',
                        type=str, nargs='+',
                        help="""Define player t.
                        t player is used for AI experiments. See below.""")

    parser.add_argument('--fplayer', action='store',
                        type=str, nargs='+',
                        help="""Define player f. See below""")

    parser.add_argument('--action', action='store',
                        choices=ACTIONS.keys(),
                        default='pick_move',
                        help="""Select the action to profile.
                        Default: %(default)s""")

    parser.add_argument('--raw', action='store',
                        default=None,
                        help="""File for Stats data. Default: None""")

    parser.add_argument('--sort', action='store',
                        choices=SORT_OPTS,
                        default='cumtime',
                        help="""Sort option. Default: %(default)s""")

    return parser


def check_game(cargs):
    """Check the --file and --game options to assure
    that we have one game to profile. Adjust as needed."""

    if not cargs.file and not cargs.game:
        print("No game specified. Use --file or --game.")
        sys.exit()

    if cargs.file and cargs.game:
        print("Don't use --file and --game together.")
        sys.exit()

    if cargs.game:
        # experimenter expects a list
        cargs.game = [cargs.game]

    if cargs.file:
        gname, _ = os.path.splitext(os.path.basename(cargs.file))
        cargs.game = [gname]


def check_action(cargs):
    """Check that we have the options needed to perform
    the profile on the action. Adjust as needed."""

    if cargs.action == 'pick_move':
        if not cargs.tplayer:
            cargs.tplayer = ['as_config']
            print("Using as_config for tplayer "
                  "(cannot be random for pick_move).")
        return


def process_command_line():
    """Process the command line and look for some basic errors."""

    parser = define_parser()
    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit()

    check_game(cargs)
    check_action(cargs)

    print('Command line:')
    for var, val in vars(cargs).items():
        print(f"   {var}:   {val}")

    return cargs


# %% main

if __name__ == '__main__':

    cargs = process_command_line()
    game, fplayer, tplayer, _ = next(exper_config.game_n_players_gen(cargs))

    cProfile.run(ACTIONS[cargs.action],
                 filename=cargs.raw,
                 sort=cargs.sort)
