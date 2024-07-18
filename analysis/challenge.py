# -*- coding: utf-8 -*-
"""Goal: test two ai configurations against eachother

Game config is hardcoded.

Created on Sun Oct 15 09:45:43 2023
@author: Ann"""

# %%  imports

import argparse
import collections
import enum
import random
import sys

import pandas as pd
import tqdm

from context import ai_player
from context import man_config
from context import game_logger

from game_interface import WinCond


# %%

game_logger.game_log.active = False


# %% players


PLAYER1 = {"algorithm": "minimaxer",
           "difficulty": 1,
           "scorer": {
               "stores_m": 4,
               "access_m": 2,
               "seeds_m": 1,
               "empties_m": 0,
               "easy_rand": 0
               },
           "ai_params": {
               "mm_depth": [1, 3, 5, 8],
            }
          }


PLAYER2 = {"algorithm": "montecarlo_ts",
            "difficulty": 1,
            "ai_params": {
                "mcts_pouts": [1, 2, 1, 1],
                "mcts_nodes": [100, 300, 500, 800],
                "mcts_bias": [100, 100, 100, 100]
            }
          }



# %%  helper classes


class GameResult(enum.Enum):
    """Game results."""

    WIN = WinCond.WIN.value
    TIE = WinCond.TIE.value
    GAME_OVER = WinCond.GAME_OVER.value
    ENDLESS = WinCond.ENDLESS.value
    MAX_TURNS = enum.auto()


class FindLoops:
    """A class to help find cycles in games."""

    def __init__(self, max_cycle=15, max_loop=20):
        """
        max_cycle =  number of states to keep in the deque
        max_loop = error, if we haven't changed the deque
        contents in this many moves
        """

        self.max_loop = max_loop
        self.game_states = collections.deque(maxlen=max_cycle)
        self.dupl_cnt = 0

    # TODO implement chess rule for repeated states 3 repeats is draw

    def game_state_loop(self, game):

        gstate = game.state
        object.__setattr__(gstate, 'mcount', 0)

        if gstate in self.game_states:
            self.dupl_cnt += 1

            if self.dupl_cnt > self.max_loop:
                print(f"Game cycle found {len(self.game_states)}")
                return True
        else:
            self.game_states.append(game.state)
            self.dupl_cnt = 0

        return False


# %%


tplayer = fplayer = None

def test_one_game(game, pdict):

    global tplayer, fplayer

    fplayer = tplayer = None
    if cargs.t_minimaxer:
        tplayer = ai_player.AiPlayer(game, pdict)
    if cargs.f_mcts:
        fplayer = ai_player.AiPlayer(game, PLAYER2)

    stuck = FindLoops()

    for _ in range(2000 if game.info.rounds else 500):


        if game.turn and tplayer:
            move = tplayer.pick_move()
        elif not game.turn and fplayer:
            move = fplayer.pick_move()
        else:
            moves = game.get_moves()
            assert moves, "Game didn't end right."
            move = random.choice(moves)

        cond = game.move(move)
        if cond in (WinCond.WIN, WinCond.TIE, WinCond.ENDLESS):
            break
        if cond in (WinCond.ROUND_WIN, WinCond.ROUND_TIE):
            if game.new_game(cond, new_round_ok=True):
                return cond.value, game.turn

        if stuck.game_state_loop(game):
            return GameResult.MAX_TURNS.value, None

        if game.info.mustpass:
            game.test_pass()
            if stuck.game_state_loop(game):
                return GameResult.MAX_TURNS.value, None

    else:
        return GameResult.MAX_TURNS.value, None

    return cond.value, game.turn


def result_name(starter, result, winner):

    if result == GameResult.WIN.value:
        return f'WIN-{starter}-{winner}'

    if result == GameResult.TIE.value:
        return f'TIE-{starter}'

    return GameResult(result).name


def play_one_config(data):

    idx = cargs.game

    for cnt in tqdm.tqdm(range(cargs.nbr_runs)):

        game, pdict = man_config.make_game('../GameProps/' + cargs.game + '.txt')

        if cnt < cargs.nbr_runs // 2:
            starter = game.turn = True
        else:
            starter = game.turn = False

        result, winner = test_one_game(game, pdict)
        col = result_name(starter, result, winner)
        data.loc[idx, col] += 1


def challenge():

    columns = sorted(list(set(result_name(start, result.value, winner)
                       for result in GameResult
                       for start in (False, True)
                       for winner in (False, True))))
    index = [file for file in [cargs.game]]

    data = pd.DataFrame(0, index=index, columns=columns)

    play_one_config(data)

    data.to_csv('data/challenge.csv')

    return data



# %%  command line args

def define_parser():
    """Define the command line arguements."""

    parser = argparse.ArgumentParser()

    parser.add_argument('game')

    parser.add_argument('--nbr_runs', action='store',
                        default=10, type=int,
                        help="""Select the number of games play.
                        Default: %(default)s""")

    parser.add_argument('--t_minimaxer', action='store_true',
                        help="""Use the minimaxer for player true; moves
                        are made randomly otherwise.
                        Default: %(default)s""")

    parser.add_argument('--f_mcts', action='store_true',
                        help="""Use the montecarlo_ts for player false; moves
                        are made randomly otherwise.
                        Default: %(default)s""")

    return parser


def process_command_line():
    """Process the command line arguements."""

    global cargs

    parser = define_parser()
    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit()

    print(cargs)


# %%

if __name__ == '__main__':

    process_command_line()

    results = challenge()
    print(results.loc[cargs.game])
