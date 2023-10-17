# -*- coding: utf-8 -*-
"""Goal: improve the minimaxer configuration

Optimize the given configuration, by choosing the best set from
a set of neighbors, until we get back to a previous set.
Neighbors are only selected along the axies.

Choose 19 more random starting points an optimize from each,
keeping the overall best set of parameters.

Created on Sun Oct 15 09:45:43 2023
@author: Ann"""

# %%  imports

import enum
import random

import tqdm

from context import ai_player
from context import man_config
from context import game_log

from game_interface import WinCond

# %%

game_log.game_log.active = False


# %%

PATH = '../GameProps/XCaptSowOwn.txt'



# %% players


PSTART = {"algorithm": "minimaxer",
           "difficulty": 1,
           "scorer": {
              "stores_m": 4,
              "access_m": 0,
              "seeds_m": 1,
              "empties_m": 1,
              "child_cnt_m": 0,
              "evens_m": 0,
              "easy_rand": 0,
              "repeat_turn": 50
           },
           "ai_params": {
               "mm_depth": [1, 3, 5, 8],
            }
          }




# %%

GAMES = 100
STEPS = 20

class GameResult(enum.Enum):
    """Game results."""

    WIN = WinCond.WIN.value
    TIE = WinCond.TIE.value
    GAME_OVER = WinCond.GAME_OVER.value
    ENDLESS = WinCond.ENDLESS.value
    MAX_TURNS = enum.auto()

def test_one_game(game, tplayer, fplayer):

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
                return cond.value, game.turn

        if game.info.mustpass:
            game.test_pass()

    else:
        return GameResult.MAX_TURNS.value, None

    return cond.value, game.turn


def get_win_percent(game, player1, player2):

    p2_win_cnt = 0

    for cnt in tqdm.tqdm(range(GAMES)):
        game.new_game()

        if cnt < GAMES // 2:
            game.turn = True
        else:
            game.turn = False

        result, winner = test_one_game(game, player1, player2)

        if result == GameResult.WIN.value and not winner:
            p2_win_cnt += 1

    return p2_win_cnt / GAMES


def get_dict(player):

    params = vars(player.sc_params).copy()
    del params['child_cnt_m']
    del params['evens_m']
    del params['easy_rand']

    return params


def one_step(game, player1, player2):
    """Compare player1 playing (params) to some of it's neighbors
    by setuping player2 and playing."""

    params = get_dict(player1)
    best_params = params.copy()
    better_pct = 0

    for axis in params:

        if axis == 'repeat_turn':
            val =  params[axis]
            if val == 0:
                test_vals = [10]
            elif val == 80:
                test_vals = [70]
            else:
                test_vals = [val - 10, val + 10]
        else:
            val = params[axis]
            if val == 0:
                test_vals = [-1, 1]
            elif val == 8:
                test_vals = [4]
            elif val == -8:
                test_vals = [-4]
            else:
                test_vals = [val // 2, val * 2]

        for nval in test_vals:

            pcopy = params.copy()
            pcopy[axis] = nval

            player2.sc_params = ai_player.ScoreParams(**pcopy)
            player2.collect_scorers()

            win_pct = get_win_percent(game, player1, player2)

            if win_pct > better_pct:
                better_pct = win_pct
                best_params = pcopy

                print('Better Params: ', win_pct)
                print(best_params)
                print()

    return best_params


def optimize_new_start(game, player1, player2):
    """Player 1 is a new starting point:
        1. search some neightbors for the next best point (one_step)
        2. if we end up back where we were, have found a local max
        3. else update player1 with new param set (and loop)"""

    local_best_params = prev_params = get_dict(player1)

    for i in range(STEPS):

        print(f'\nStep local {i}: :', local_best_params)
        params = one_step(game, player1, player2)

        if params == prev_params:
            break

        else:
            # we've taken a step in better direction, keep going
            local_best_params = params

            player1.sc_params = ai_player.ScoreParams(**params)
            player1.collect_scorers()
            prev_params = params.copy()

    return local_best_params


TEST_VALS = [-8, -4, -2, -1, 0, 1, 2, 4, 8]

def optimize():

    game, _ = man_config.make_game(PATH)
    player1 = ai_player.AiPlayer(game, PSTART)
    player2 = ai_player.AiPlayer(game, PSTART)

    print('Depths: ', player1.algo.max_depth, player2.algo.max_depth)

    best_params = params = get_dict(player1)

    for i in range(STEPS):

        print(f'\n\nNew Start {i}:  ', params)
        params = optimize_new_start(game, player1, player2)

        # compare local best to overal best
        print('Comparing best_params')
        print(best_params)
        player1.sc_params = ai_player.ScoreParams(**best_params)
        player1.collect_scorers()
        print(' to new param set ')
        print(params)
        player2.sc_params = ai_player.ScoreParams(**params)
        player2.collect_scorers()

        win_pct = get_win_percent(game, player1, player2)

        if win_pct > 0.5:
            # new params beat old best_params
            print(f"New Best Params: {win_pct:%} over previous best.")
            print(params)
            print()

            best_params = params.copy()


        #  choose a new random spot
        params = {'stores_m': random.choice(TEST_VALS),
                  'access_m': random.choice(TEST_VALS),
                  'seeds_m': random.choice(TEST_VALS),
                  'empties_m': random.choice(TEST_VALS)}

        player1.sc_params = ai_player.ScoreParams(**params)
        player1.collect_scorers()

    return best_params


# %%

best_params = optimize()

print('Best Params: ')
print(best_params)
