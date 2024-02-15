# -*- coding: utf-8 -*-
"""Goal: improve the minimaxer configuration

Optimize the given configuration, by choosing the best set from
a set of neighbors.
Neighbors are only selected along the axies.

Choose more random starting points and optimize from each,
keeping the overall best set of parameters.

Created on Sun Oct 15 09:45:43 2023
@author: Ann"""

# %%  imports

import argparse
import enum
import os
import random
import sys

import tqdm

from context import ai_player
from context import man_config
from context import game_log

from game_interface import WinCond


# %% disable logger

game_log.game_log.active = False


# %%  constants

PATH = '../GameProps/'
BAD_CFG = 'all_params.txt'
INDEX = [fname[:-4] for fname in os.listdir(PATH) if fname != BAD_CFG]


PN_TEST_VALS = [-8, -4, -2, -1, 0, 1, 2, 4, 8]
POS_TEST_VALS = [0, 10, 20, 30, 40, 50, 60, 70, 80]

PARAMS_VALS = {'access_m': PN_TEST_VALS,
               'child_cnt_m': PN_TEST_VALS,
               'empties_m': PN_TEST_VALS,
               'evens_m':PN_TEST_VALS,
               'seeds_m': PN_TEST_VALS,
               'stores_m': PN_TEST_VALS,
               'repeat_turn': POS_TEST_VALS,
               }

# %% global variables

cargs = None
log_file = None
starts = []


# %%  command line args

def define_parser():
    """Define the command line arguements."""

    parser = argparse.ArgumentParser()

    parser.add_argument('game', action='store',
                        choices=list(INDEX),
                        help="""Select the game to optimize.""")

    parser.add_argument('--nbr_runs', action='store',
                        default=1_000, type=int,
                        help="""Select the number of games to simulate
                        for each test pair.
                        Default: %(default)s""")

    parser.add_argument('--nbr_steps', action='store',
                        default=20, type=int,
                        help="""Select the number of optimizations steps
                        to perform.
                        Default: %(default)s""")

    parser.add_argument('--nbr_starts', action='store',
                        default=10, type=int,
                        help="""Select the number of start points to
                        search from. Set 1 to only search from configuration
                        file start point (no random points).
                        Default: %(default)s""")

    parser.add_argument('--thresh', action='store',
                        default=0.02, type=float,
                        help="""Select the improvement threshold.
                        Default: %(default)s""")

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

    print(cargs)


# %%  print & saver

def dbl_print(*args, sep=' '):
    """Print the args with the specified separator.
    If log_file is not None, print it there too."""

    string = sep.join(str(arg) for arg in args)
    print(string)
    if log_file:
        print(string, file=log_file)


# %%  test pair of players

class GameResult(enum.Enum):
    """Game results.  Using 'values' to combine two enums."""

    WIN = WinCond.WIN.value
    TIE = WinCond.TIE.value
    MAX_TURNS = enum.auto()


def test_one_game(game, tplayer, fplayer):
    """Play one game with tplayer against fplayer"""

    for _ in range(2000 if game.info.rounds else 500):

        if game.turn:
            move = tplayer.pick_move()
        else:
            move = fplayer.pick_move()

        cond = game.move(move)
        if cond in (WinCond.WIN, WinCond.TIE, WinCond.ENDLESS):
            break
        if cond in (WinCond.ROUND_WIN, WinCond.ROUND_TIE):
            if game.new_game(cond, new_round_ok=True):
                break

        if game.info.mustpass:
            game.test_pass()

    else:
        return GameResult.MAX_TURNS.value, None
    return cond.value, game.turn


def get_win_percent(game, player1, player2):
    """Play a number of games of player1 against player2.
    Have each player start half of the games.
    Return the win percentages for player2:
        wins 1 point, ties 0.5 point
    Ignore any games that do not complete."""

    comp_games = p2_win_cnt = 0
    half_games = cargs.nbr_runs

    for cnt in tqdm.tqdm(range(cargs.nbr_runs)):
        game.new_game()

        if cnt < half_games:
            game.turn = True
        else:
            game.turn = False
        result, winner = test_one_game(game, player1, player2)

        if result == GameResult.MAX_TURNS.value:
            continue

        comp_games += 1
        if result == GameResult.WIN.value and not winner:
            p2_win_cnt += 1
        elif result == GameResult.TIE.value:
            p2_win_cnt += 0.5

    return p2_win_cnt / comp_games


# %% utility functions

def pname_list(pdict):
    """Get the list of parameter names to vary,
    use those listed in player dict, minus easy_rand."""

    pnames = list(pdict['scorer'].keys())
    if 'easy_rand' in pnames:
        pnames.remove('easy_rand')
    return pnames


def get_random_value(axis):
    """Choose a random parameter value."""

    if axis == 'repeat_turn':
        return random.choice(POS_TEST_VALS)
    return random.choice(PN_TEST_VALS)


def get_value_neighs(axis, cur_val):
    """Get the values that appear on either side of the cur_val.
    cur_val might not be in  PARAMS_VALS."""
    plist = PARAMS_VALS[axis]

    if cur_val < plist[0]:
        test_vals = [plist[0]]

    elif cur_val == plist[0]:
        test_vals = [plist[1]]

    elif plist[-1] < cur_val:
        test_vals = [plist[-1]]

    elif plist[-1] == cur_val:
        test_vals = [plist[-2]]

    else:
        for pidx, pval in enumerate(plist):
            if cur_val <= pval:
                break
        if cur_val == pval:
            test_vals = [plist[pidx - 1], plist[pidx + 1]]
        else:
            test_vals = [plist[pidx - 1], plist[pidx]]

    return test_vals


def update_player(player, new_params):
    """Update the scorer parameters in the player
    with values from new_params dictionary."""

    player.sc_params = ai_player.ScoreParams(**new_params)
    player.collect_scorers()


# %%    optimizers

def one_step(game, player1, player2, pnames):
    """Test some neighbors of player1's parameters (as player2)
    to see if any of them play significantly better than player1.

    Player1 is unchanged through these test so win % can be
    directly compared."""

    best_params = None
    better_pct = 0.5   # assume p1 v p1 is 50%
    p1_params = vars(player1.sc_params)

    for axis in pnames:
        for nval in get_value_neighs(axis, p1_params[axis]):

            pcopy = p1_params.copy()
            pcopy[axis] = nval
            update_player(player2, pcopy)

            win_pct = get_win_percent(game, player1, player2)

            if win_pct > better_pct + cargs.thresh:
                better_pct = win_pct
                best_params = pcopy

                dbl_print(f'One Step: Better Params: {win_pct:6.3%}\n',
                          best_params)

    return best_params


def optimize_from(game, player1, player2, pnames):
    """Use player1 as a starting point, use one_step to see if
    there is a neighboring param set that is better;
    if so, update player1 and continue (up to STEPS times)."""
    global starts

    local_best_params = None
    start_params = vars(player1.sc_params)

    for i in range(cargs.nbr_steps):

        dbl_print(f'\nOpt from: Step local {i}:')
        params = one_step(game, player1, player2, pnames)
        if params is None:
            break
        if params == start_params:
            dbl_print('\nOpt from: found a cycle - stopping.')
            local_best_params = None
            break

        # we've taken a step in better direction, update player1
        local_best_params = params
        update_player(player1, params)

    starts += [(start_params, params, i)]
    return local_best_params


def optimize():
    """Start from the player configuration in the game config file.
    Optimize from there to a local maximum,
    choose a new start point, and then optimize from there,
    test to see if the new point plays better than the
    previous best."""

    game, pdict = man_config.make_game(PATH + cargs.game + '.txt')
    pnames = pname_list(pdict)
    dbl_print('Parameters to optimize: ', pnames)

    player1 = ai_player.AiPlayer(game, pdict)
    player2 = ai_player.AiPlayer(game, pdict)
    best_params = vars(player1.sc_params)

    for i in range(cargs.nbr_starts):

        if i < 1:
            new_start = best_params
            dbl_print(f'\n{i}: Starting point: \n', best_params)
        else:
            new_start = {k: get_random_value(k) for k in pnames}
            update_player(player1, new_start)
            dbl_print(f'\n{i}: New random start:\n', new_start)

        params = optimize_from(game, player1, player2, pnames)

        if params:
            dbl_print('\nOptimize: Comparing best_params:\n', best_params)
            dbl_print(' to new param set:\n', params)

            update_player(player1, best_params)
            update_player(player2, params)
            win_pct = get_win_percent(game, player1, player2)

            if win_pct > 0.52:
                dbl_print(f'New Best Params: {win_pct:6.3%} over previous best.\n',
                      params)
                best_params = params.copy()
            else:
                dbl_print(f'Not better {win_pct:6.3%}.')
        log_file.flush()

    return best_params


# %%

if __name__ == '__main__':

    process_command_line()
    selected_params = optimize()

    dbl_print('\nStart points and best from there:')
    for start, best, steps in starts:
        dbl_print(start, best, steps, sep='\n')

    dbl_print('\nBest Overall Params: ')
    dbl_print(selected_params)

    if log_file:
        log_file.close()
