# -*- coding: utf-8 -*-
"""Goal:  determine the fairness of the games

For every config file, play a bunch of games.
Collect game ending data.

Created on Sun Jul 23 11:29:10 2023
@author: Ann"""

import enum
import math
import os
import random

import pandas as pd
import scipy
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


TFAIR = 'true_fair'
FFAIR = 'false_fair'
STARTERFAIR = 'starter_fair'

RANDOM = True
GAMES = 1000

FIELDS = {
          'allow_rule': 0,
          'blocks': False,
          'capsamedir': False,
          'capt_max': 0,
          'capt_min': 0,
          'capt_on': '',
          'capt_rturn': False,
          'capttwoout': False,
          'child_cvt': 0,
          'child_rule': 0,
          'child_type': 0,
          'crosscapt': False,
          'evens': False,
          'goal': 0,
          'gparam_one': 0,
          'grandslam': 0,
          'min_move': 1,
          'mlaps': 0,
          'move_one': False,
          'moveunlock': False,
          'multicapt': False,
          'mustpass': False,
          'mustshare': False,
          'no_sides': False,
          'nocaptfirst': False,
          'oppsidecapt': False,
          'pickextra': 0,
          'prescribed': 0,
          'round_fill': 0,
          'round_starter': 0,
          'rounds': False,
          'skip_start': False,
          'sow_direct': 1,
          'sow_own_store': False,
          'sow_rule': 0,
          'sow_start': False,
          'start_pattern': 0,
          'stores': False,
          'udir_holes': '',
          'visit_opp': False,
          'xc_sown': False,
          'xcpickown': 0,
         }


# %%

class GameResult(enum.Enum):
    """Game results."""

    WIN = WinCond.WIN.value
    TIE = WinCond.TIE.value
    MAX_TURNS = enum.auto()


def result_name(starter, result, winner):

    if result == GameResult.WIN.value:
        return f'W-{str(starter)[0]}-{str(winner)[0]}'

    if result == GameResult.TIE.value:
        return f'TIE-{str(starter)[0]}'

    if result == GameResult.MAX_TURNS.value:
        return 'MAX_TURNS'

    assert f'Unexpedect game result {result}.'


def index_name(filename):
    return filename[:-4]


# %%  build data frame

def build_data_frame():

    ginfo = dict()
    for file in FILES:
        gdict = man_config.read_game(PATH + file)
        cons_gd = dict(**gdict['game_constants'], **gdict['game_info'])
        del cons_gd['about']
        del cons_gd['name']
        ginfo[index_name(file)] = cons_gd
    data = pd.DataFrame.from_dict(ginfo).transpose()

    for name, dval in FIELDS.items():
            data[name] = data[name].fillna(dval)

    dlen = len(FILES)
    columns = sorted(list(set(result_name(start, result.value, winner)
                              for result in GameResult
                              for start in (False, True)
                              for winner in (False, True))))
    for col in columns:
        data[col] = [0] * dlen

    columns = [TFAIR, FFAIR, STARTERFAIR]
    for col in columns:
        data[col] = [False] * dlen


    return data


# %% some tests

def fail_to_reject(wins, total, confidence=0.90):
    """H0:  prob of win = 0.5   Ha: prob of win != 0.5

    Failing to reject - means we didn't reject H0
    -- not enough evidence to prove it false

    This is the test for a bernouli trial:
        1. exactly two outcomes
        2. outcomes are equally likely (but aren't we testing this?)
        3. trials are independent
        """

    prob = 0.5
    mean = total * prob
    std_dev = math.sqrt(mean * (1 - prob))
    z = scipy.stats.norm.ppf(1-(1-confidence)/2)

    normalized = abs((wins - mean)  / std_dev)

    return normalized < z


def evals(game, data):

    #  True has equal likelihood of win versus loss
    t_wins_indep_starter = \
        data.loc[game, 'W-T-T'] + data.loc[game, 'W-F-T']
    data.loc[game, TFAIR] = fail_to_reject(t_wins_indep_starter, GAMES)

    #  False has equal likelihood of win versus loss
    f_wins_indep_starter = \
        data.loc[game, 'W-T-F'] + data.loc[game, 'W-F-F']
    data.loc[game, FFAIR] = fail_to_reject(f_wins_indep_starter, GAMES)

    # starter is not more likely to win
    wins_starter = \
        data.loc[game, 'W-T-T'] + data.loc[game, 'W-F-F']
    data.loc[game, STARTERFAIR] = fail_to_reject(wins_starter, GAMES)


# %%  play and collect

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
        if cond in (WinCond.WIN, WinCond.TIE):
            break
        if cond in (WinCond.ROUND_WIN, WinCond.ROUND_TIE):
            if game.new_game(cond, new_round_ok=True):
                return cond.value, game.turn

        if game.info.mustpass:
            game.test_pass()

    else:
        return GameResult.MAX_TURNS.value, None

    return cond.value, game.turn


def play_one_config(file, index, data):

    for cnt in tqdm.tqdm(range(GAMES)):

        game, pdict = man_config.make_game(PATH + file)
        if cnt < GAMES // 2:
            starter = game.turn = True
        else:
            starter = game.turn = False

        result, winner = test_one_game(game, pdict)
        col = result_name(starter, result, winner)
        data.loc[index, col] += 1


def play_them_all(data):

    for file in FILES:
        index = index_name(file)
        print(index)
        play_one_config(file, index, data)
        evals(index, data)

    if RANDOM:
        data.to_csv('data/random.csv')
    else:
        data.to_csv('data/minimaxer.csv')



# %%

data = build_data_frame()
play_them_all(data)
