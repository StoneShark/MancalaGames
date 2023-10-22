# -*- coding: utf-8 -*-
"""Goal:  determine if the fair

For every config file, play 10_000 games with random moves.
Collect game ending data.

Created on Sun Jul 23 11:29:10 2023
@author: Ann"""

import enum
import os
import random

import pandas as pd
import tqdm

from context import ai_player
from context import man_config
from context import game_log

from game_interface import WinCond

# %%

game_log.game_log.active = False


# %%

PATH = '../GameProps/'
FILES = os.listdir(PATH)

BAD_CFG = 'all_params.txt'
if BAD_CFG in FILES:
    FILES.remove(BAD_CFG)


RANDOM = False
GAMES = 200


# %%


class GameResult(enum.Enum):
    """Game results."""

    WIN = WinCond.WIN.value
    TIE = WinCond.TIE.value
    GAME_OVER = WinCond.GAME_OVER.value
    ENDLESS = WinCond.ENDLESS.value
    MAX_TURNS = enum.auto()


def test_one_game(game, pdict):

    if not RANDOM:
        tplayer = ai_player.AiPlayer(game, pdict)
        fplayer = ai_player.AiPlayer(game, pdict)

    for _ in range(5000 if game.info.rounds else 500):

        if RANDOM:
            moves = game.get_moves()
            assert moves, "Game didn't end right."
            move = random.choice(moves)
        else:
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

        game, pdict = man_config.make_game(PATH + file)
        if cnt < GAMES // 2:
            starter = game.turn = True
        else:
            starter = game.turn = False

        result, winner = test_one_game(game, pdict)
        col = result_name(starter, result, winner)
        data.loc[idx, col] += 1


def play_them_all():

    columns = sorted(list(set(result_name(start, result.value, winner)
                              for result in GameResult
                              for start in (False, True)
                              for winner in (False, True))))
    index = [index_name(file) for file in FILES]

    data = pd.DataFrame(0, index=index, columns=columns)

    for file in FILES:
        print(file)
        play_one_config(file, data)

    if RANDOM:
        data.to_csv('data/random.csv')
    else:
        data.to_csv('data/minimaxer.csv')

    return data


# %%

results = play_them_all()
