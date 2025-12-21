# -*- coding: utf-8 -*-
"""Goal: improve the game configuration

Optimize the given configuration, by choosing the best set from
a set of neighbors.
Neighbors are only selected along the axes not diagonals.

Choose more random starting points and optimize from each,
keeping the overall best set of parameters. New start points
are chosen near the current best point.

For minimaxer and negamaxer:
Only the scorer parameters listed in the game config file
will be explored, thus remove any that do not apply to the
game.

Created on Sun Oct 15 09:45:43 2023
@author: Ann"""

# %%  imports

import argparse
import logging
import random
import sys

import ana_logger
import param_ops
import play_game
from context import ai_player
from context import cfg_keys as ckey
from context import game_logger
from context import man_config
from context import man_path


# %% loggers

logger = logging.getLogger()

# disable the game logger
game_logger.game_log.active = False


# %%  constants

PATH = '../GameProps/'
INDEX = [fname[:-4] for fname in man_path.game_files()]


PN_TEST_VALS =  [-16, -12, -8, -4, -2, -1, 0, 1, 2, 4, 8, 12, 16]
POS_TEST_VALS = [0, 2, 4, 8, 12, 16, 32, 56, 64]

PARAMS_VALS = {ckey.MX_ACCESS_M: PN_TEST_VALS,
               ckey.MX_CHILD_CNT_M: PN_TEST_VALS,
               ckey.MX_EMPTIES_M: PN_TEST_VALS,
               ckey.MX_EVENS_M: PN_TEST_VALS,
               ckey.MX_SEEDS_M: PN_TEST_VALS,
               ckey.MX_STORES: PN_TEST_VALS,
               ckey.MX_RTURN_A: POS_TEST_VALS,

               ckey.MCTS_BIAS: list(range(100, 1000, 50)),
               ckey.MCTS_NODES: list(range(100, 3000, 100)),
               ckey.MCTS_POUTS: list(range(1, 5, 1))
               }

# the number of steps in above arrays that a parameter might
# be adjusted for
RANDOM_DIST = 3

# %% global variables

cargs = None
starts = []


# %%  command line args

def define_parser():
    """Define the command line arguements."""

    parser = argparse.ArgumentParser()

    parser.add_argument('game', action='store',
                        choices=list(INDEX),
                        help="""Select the game to optimize.""")

    parser.add_argument('--skip_start', action='store_true',
                        help="""Do not test the start configuration
                        The start location will still be used as the
                        focus for the random starts. This will not
                        test the points up/down each axis.""")

    parser.add_argument('--nbr_runs', action='store',
                        default=250, type=int,
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
                        default=0.12, type=float,
                        help="""Select the improvement threshold.
                        Default: %(default)s""")

    parser.add_argument('--param', action='append',
                        choices=list(PARAMS_VALS.keys()),
                        default=list(),
                        help="""Select the parameters to add to the
                        optimizer. Parameters set in the config will
                        automatically be included. Use multiple options
                        to select multiple parameters""")

    parser.add_argument('--depth', action='store',
                        default=5, type=float,
                        help="""Select minimaxer depth.
                        Default: %(default)s""")

    parser.add_argument('--output', action='store',
                        help="""Save the ouptut to the specified file.
                        Skip for output to console only.
                        Output file is always restarted.""")
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

    ana_logger.config(logger, cargs.output, True)
    logger.info(cargs)


# %%  neighbors


def get_closest_index(vlist, cur_val):
    """Return the index of the value closest to cur_val in vlist"""

    if cur_val in vlist:
        return vlist.index(cur_val)

    return min(enumerate(vlist),
               key=lambda idx_val: abs(cur_val - idx_val[1]))[0]


def get_random_neigh(axis, cur_val):
    """Pick a value that might be a small way away
    from the current value.

    Try to keep the likelihood of not moving the same
    even if on ends by wrapping the offsets when at
    an endpoint."""

    vlist = PARAMS_VALS[axis]
    vlen = len(vlist)
    idx = get_closest_index(vlist, cur_val)

    offset = random.randint(-RANDOM_DIST, RANDOM_DIST)
    if idx == 0:
        offset = abs(offset)
    elif idx == vlen:
        offset = -abs(offset)

    idx = max(0, min(idx + offset, vlen - 1))
    return vlist[idx]


def get_value_neighs(axis, cur_val):
    """Get the values that appear on either side of the cur_val.
    cur_val might not be in  PARAMS_VALS."""
    vlist = PARAMS_VALS[axis]

    if cur_val < vlist[0]:
        test_vals = [vlist[0]]

    elif cur_val == vlist[0]:
        test_vals = [vlist[1]]

    elif vlist[-1] < cur_val:
        test_vals = [vlist[-1]]

    elif vlist[-1] == cur_val:
        test_vals = [vlist[-2]]

    else:
        pidx = get_closest_index(vlist, cur_val)
        if cur_val == vlist[pidx]:
            test_vals = [vlist[pidx - 1], vlist[pidx + 1]]
        else:
            test_vals = [vlist[pidx - 1], vlist[pidx]]

    return test_vals


# %%    optimizers

def one_step(game, player1, player2, pnames):
    """Test some neighbors of player1's parameters (as player2)
    to see if any of them play significantly better than player1.

    Player1 is unchanged through these test so win % can be
    directly compared."""

    best_params = None
    better_pct = 0.5   # assume p1 v p1 is 50% i.e. fair
    p1_params = param_ops.get_params(player1)

    for axis in pnames:
        for nval in get_value_neighs(axis, p1_params[axis]):

            pcopy = p1_params.copy()
            pcopy[axis] = nval
            param_ops.update_player(player2, pcopy)

            logger.info('Param update %s %s', axis, nval)
            win_pct = play_game.get_win_percent(game, player1, player2,
                                                cargs.nbr_runs)

            if win_pct > better_pct + cargs.thresh:
                better_pct = win_pct
                best_params = pcopy

                logger.info('One Step: Better Params: %8.3f%%', win_pct * 100)
                logger.info(best_params)

    return best_params


def optimize_from(game, player1, player2, pnames):
    """Use player1 as a starting point, use one_step to see if
    there is a neighboring param set that is better;
    if so, update player1 and continue (up to STEPS times)."""
    global starts

    local_best_params = None
    start_params = param_ops.get_params(player1).copy()

    for i in range(cargs.nbr_steps):

        logger.info('\n\nOpt from: Step local %s:', i)
        params = one_step(game, player1, player2, pnames)
        if params is None:
            break
        if params == start_params:
            logger.info('\n\nOpt from: found a cycle - stopping.')
            local_best_params = None
            break

        # we've taken a step in better direction, update player1
        local_best_params = params.copy()
        param_ops.update_player(player1, params)

    starts += [(start_params, local_best_params, i+1)]
    return local_best_params


def optimize():
    """Start from the player configuration in the game config file.
    Optimize from there to a local maximum,
    choose a new start point, and then optimize from there,
    test to see if the new point plays better than the
    previous best."""

    game, pdict = man_config.make_game(PATH + cargs.game + '.txt')

    player1 = ai_player.AiPlayer(game, pdict)
    player2 = ai_player.AiPlayer(game, pdict)
    param_ops.add_algo_name(player1)
    param_ops.add_algo_name(player2)
    param_ops.set_depth(player1, cargs.depth)
    param_ops.set_depth(player2, cargs.depth)

    pnames = list(set(param_ops.get_pnames(player1, pdict)) |
                  set(cargs.param))
    logger.info('Parameters to optimize: %s', pnames)

    best_params = param_ops.get_params(player1)

    for i in range(cargs.nbr_starts):

        if not cargs.skip_start and i < 1:
            new_start = best_params.copy()
            logger.info('\n%d: Starting point: \n%s', i, best_params)
        else:
            new_start = {k: get_random_neigh(k, best_params[k]) for k in pnames}
            param_ops.update_player(player1, new_start)
            logger.info('\n%d: New random start:\n%s', i, new_start)

        params = optimize_from(game, player1, player2, pnames)

        if params:
            logger.info('\n\nOptimize: Comparing best_params:')
            logger.info(best_params)
            logger.info(' to new param set:')
            logger.info(params)

            param_ops.update_player(player1, best_params)
            param_ops.update_player(player2, params)
            win_pct = play_game.get_win_percent(game, player1, player2,
                                                cargs.nbr_runs)

            if win_pct > 0.50 + cargs.thresh:
                logger.info('New Best Params: %8.3f%% over previous best.',
                            win_pct * 100)
                logger.info(params)
                best_params = params.copy()
            else:
                logger.info('Not better %8.3f%%.', win_pct * 100)

    return best_params


# %%

if __name__ == '__main__':

    with ana_logger.trap_close(logger):

        process_command_line()
        selected_params = optimize()

        logger.info('\nStart points and best from there:')
        for start, best, steps in starts:
            logger.info('\n%s\n%s\n%s\n', start, best, steps)

        logger.info('\nBest Overall Params:\n%s', selected_params)
