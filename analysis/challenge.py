# -*- coding: utf-8 -*-
"""Goal: test two ai configurations against eachother

Game config is hardcoded.

Created on Sun Oct 15 09:45:43 2023
@author: Ann"""

# %%  imports

import enum

import pandas as pd
import tqdm

from context import ai_player
from context import man_config
from context import game_log

from game_interface import WinCond

# %%

game_log.game_log.active = False


# %%

PATH = '../GameProps/Wari.txt'



# %% players


PLAYER1 = {"algorithm": "minimaxer",
           "difficulty": 1,
           "scorer": {
               "stores_m": 4,
               "access_m": 1,
               },
           "ai_params": {
               "mm_depth": [1, 3, 5, 8],
            }
          }


PLAYER2 = {"algorithm": "minimaxer",
           "difficulty": 1,
           "scorer": {
               "stores_m": 8,
               "access_m": 2,
               "seeds_m": 2,
               "empties_m": -1,
               },
           "ai_params": {
               "mm_depth": [1, 3, 5, 8],
            }
          }

# PLAYER2 = {"algorithm": "montecarlo_ts",
#            "difficulty": 1,
#            "ai_params": {
#                "mcts_nodes": [300, 500, 800, 1100],
#                "mcts_bias": [0.3, 0.3, 0.3, 0.3]
#             }
#           }



# %%

GAMES = 1000

class GameResult(enum.Enum):
    """Game results."""

    WIN = WinCond.WIN.value
    TIE = WinCond.TIE.value
    GAME_OVER = WinCond.GAME_OVER.value
    ENDLESS = WinCond.ENDLESS.value
    MAX_TURNS = enum.auto()


def test_one_game(game):

    tplayer = ai_player.AiPlayer(game, PLAYER1)
    fplayer = ai_player.AiPlayer(game, PLAYER2)

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


def result_name(starter, result, winner):

    if result == GameResult.WIN.value:
        return f'WIN-{starter}-{winner}'

    if result == GameResult.TIE.value:
        return f'TIE-{starter}'

    return GameResult(result).name


def index_name(filename):
    return filename.replace(' ', '_')[:-4]


def play_one_config(file, data):

    idx = index_name(file)

    for cnt in tqdm.tqdm(range(GAMES)):

        game, _ = man_config.make_game(PATH)

        if cnt < GAMES // 2:
            starter = game.turn = True
        else:
            starter = game.turn = False

        result, winner = test_one_game(game)
        col = result_name(starter, result, winner)
        data.loc[idx, col] += 1


def challenge():

    columns = sorted(list(set(result_name(start, result.value, winner)
                       for result in GameResult
                       for start in (False, True)
                       for winner in (False, True))))
    index = [index_name(file) for file in [PATH]]

    data = pd.DataFrame(0, index=index, columns=columns)

    play_one_config(PATH, data)

    data.to_csv('data/challenge.csv')

    return data


# %%

results = challenge()
print(results.loc[index_name(PATH)])
