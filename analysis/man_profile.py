# -*- coding: utf-8 -*-
"""Do timing experiments.

Don't call this module profile, it causes import issues.

Created on Mon Aug  7 06:18:19 2023
@author: Ann"""

import argparse
import cProfile
import os
import random
import sys
import timeit

import exper_config
from game_logger import game_log
import play_game     # used indirectly in profile command, needs to be globals


# %% constants

PATH = '../GameProps/'
BAD_CFG = '_all_params.txt'
INDEX = [fname[:-4] for fname in os.listdir(PATH) if fname != BAD_CFG]


SORT_OPTS = ['calls', 'cumulative', 'cumtime', 'file', 'filename',
             'module', 'ncalls', 'pcalls', 'line',
             'name', 'nfl', 'stdname', 'time', 'tottime']


ACTIONS = {'pick_move': 'tplayer.pick_move()',
           'allows': 'game.get_allowable_holes()',
           'play_game': 'game.new_game() ; ' \
                        'play_game.play_one_game(game, fplayer, tplayer)',
           'random_move': 'game.move(random.choice(game.get_moves()))'
           }

PROFILE = 'profile'
TIMEIT = 'timeit'

TIMERS = [PROFILE, TIMEIT]


PARAMS = 'g'
DECOS = 'd'
AICONFIG = 'p'

REPORTS = PARAMS + DECOS + AICONFIG


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

    parser.add_argument('--timer', action='store',
                        choices=TIMERS, default=PROFILE,
                        help="""Choose a timer operation.
                        Default: %(default)s""")

    parser.add_argument('--raw', action='store',
                        default=None,
                        help="""File for Stats data. Default: None""")

    parser.add_argument('--sort', action='store',
                        choices=SORT_OPTS,
                        default='cumtime',
                        help="""Sort option (only applies to
                        --timer profile). Default: %(default)s""")

    parser.add_argument('--nbr_runs', action='store',
                        default=10, type=int,
                        help="""Select the number of actions to perform
                        (only applies to --timer timeit).
                        Default: %(default)s""")

    parser.add_argument('--report', action='store',
                        default='',
                        help="""Include details about the test
                        configuration:
                            g--game param string;
                            d--deco chain print; and
                            p--ai player configurations.""")

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

    if cargs.action == 'random_move':
        if cargs.nbr_runs > 10:
            print("Random moves are made sequentially. "
                  f"The game might end before {cargs.nbr_runs} "
                  "moves (crash).")


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

    print('\nCommand line:')
    for var, val in vars(cargs).items():
        print(f"   {var}:   {val}")
    print()

    return cargs


# %% main

if __name__ == '__main__':

    cargs = process_command_line()
    game, fplayer, tplayer, _ = next(exper_config.game_n_players_gen(cargs))

    game_log.active = False

    if cargs.timer == PROFILE:
        cProfile.run(ACTIONS[cargs.action],
                     filename=cargs.raw,
                     sort=cargs.sort)

    elif cargs.timer == TIMEIT:

        result = timeit.timeit(ACTIONS[cargs.action],
                               number=cargs.nbr_runs,
                               globals=globals())

        per_exe = result / cargs.nbr_runs
        print(f'Run time (x{cargs.nbr_runs}):',
              f'    {result:10.6} seconds   total ',
              f'    {per_exe:10.6} per execution.', sep='\n')


    print()
    if PARAMS in cargs.report:
        print(game.params_str(), '\n')
    if DECOS in cargs.report:
        print(game.deco)
    if AICONFIG in cargs.report:
        print(fplayer)
        print(tplayer)
