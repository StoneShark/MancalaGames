# -*- coding: utf-8 -*-
"""Goal:  determine the fairness of the games.

Compute win percentage for true and for the starter such that:
        t_win_% == 1 - f_win_%
        start_win_% == 1 - second_win_%
and decide if they are fair.

Detailed approach:
For every config file, play a bunch of games.
Collect game ending data.
Compute intermediate data so mean and standard dev can be computed.

Created on Sun Jul 23 11:29:10 2023
@author: Ann"""

# %% imports

import functools as ft
import math

import pandas as pd
import scipy

import exper_config
import play_game

from context import game_logger

from play_game import GameResult


# %% column names and types

TIE_T = play_game.result_name(True, GameResult.TIE, None)
TIE_F = play_game.result_name(False, GameResult.TIE, None)

#  two sum columns
SCORE = 'score'
SCORE_2 = 'score_2'   # squared

ST_SCORE = 'st_score'
ST_SCORE_2 = 'st_score_2'

NO_RESULT = 'no_result'

INT_COLUMNS = play_game.GAME_RESULTS + \
              [NO_RESULT, SCORE, SCORE_2, ST_SCORE, ST_SCORE_2]

MEAN = 'mean'
STDEV = 'stddev'

WIN_PCT = 'win_pct'
STR_PCT = 'str_pct'
TIE_PCT = 'tie_pct'
FLT_COLUMNS = [WIN_PCT, STR_PCT, TIE_PCT]

# fair columns
WIN_FAIR = 'win_fair'
STARTER_FAIR = 'starter_fair'

BOOL_COLUMNS = [WIN_FAIR, STARTER_FAIR]


# %%  score and collect

WIN_SCORE = 4
TIE_SCORE = 2

EXPECTED_VAL = WIN_SCORE * 0.5


def score_game(gname, starter, result, winner):
    """Collect game results including sum and sum squared
    for scores for winner and for starter's wins."""

    col = play_game.result_name(starter, result, winner)
    data.loc[gname, col] += 1

    if result.name[:3] not in ('WIN', 'TIE'):
        data.loc[gname, NO_RESULT] += 1

    score = 0
    if result == GameResult.WIN and winner:
        score = WIN_SCORE
    elif result == GameResult.TIE:
        score = TIE_SCORE
    data.loc[gname, SCORE] += score
    data.loc[gname, SCORE_2] += score * score

    score = 0
    if result == GameResult.WIN and winner == starter:
        score = WIN_SCORE
    elif result == GameResult.TIE:
        score = TIE_SCORE
    data.loc[gname, ST_SCORE] += score
    data.loc[gname, ST_SCORE_2] += score * score


# %%  build data frame

def build_data_frame():
    """Build a data frame with all the desired columns."""

    dframe = pd.DataFrame(index=config.game)

    dlen = len(config.game)
    for col in INT_COLUMNS:
        dframe[col] = [0] * dlen
    for col in FLT_COLUMNS:
        dframe[col] = [0.0] * dlen
    for col in BOOL_COLUMNS:
        dframe[col] = [False] * dlen

    return dframe

# %% fairness tests

def std_dev(xsum, x_sqr_sum, nbr):
    """Use two sum formula to compute standard deviation."""

    return math.sqrt((x_sqr_sum - ((xsum * xsum) / nbr)) / (nbr - 1))


def fail_to_reject(gname, nbr_runs, tag, confidence=0.95):
    """H0:  prob of win = 0.5   Ha: prob of win != 0.5

    Failing to reject - means we didn't reject H0
    -- not enough evidence to prove it false"""

    nbr_games = nbr_runs - data.loc[gname, NO_RESULT]
    if nbr_games <= 1:
        return False

    mean = data.loc[gname, tag] / nbr_games
    stdev = std_dev(data.loc[gname, tag], data.loc[gname, tag + '_2'],
                    nbr_games)
    if abs(stdev) < 0.00001:
        return False

    test_stat = (mean - EXPECTED_VAL) / (stdev / math.sqrt(nbr_games))
    crit_value = scipy.stats.norm.ppf(1 - (1 - confidence) / 2)

    return test_stat < crit_value


def eval_game(gname, nbr_runs):
    """Compute win_fair and starter_fair for one game configuration."""

    data.loc[gname, WIN_FAIR] = fail_to_reject(gname, nbr_runs, SCORE)
    data.loc[gname, STARTER_FAIR] = fail_to_reject(gname, nbr_runs, ST_SCORE)

    nbr_games = nbr_runs - data.loc[gname, NO_RESULT]
    data.loc[gname, WIN_PCT] = data.loc[gname, SCORE] / (WIN_SCORE * nbr_games)
    data.loc[gname, STR_PCT] = data.loc[gname, ST_SCORE] / (WIN_SCORE * nbr_games)
    data.loc[gname, TIE_PCT] = \
        (data.loc[gname, TIE_T] + data.loc[gname, TIE_F]) / nbr_games


# %%  play and collect


def play_them_all():

    for game, fplayer, tplayer, gname in game_players_gen:
        print(game.info.name)
        play_game.play_games(game, fplayer, tplayer,
                             config.nbr_runs, config.save_logs,
                             ft.partial(score_game, gname))

        eval_game(gname, config.nbr_runs)

    if config.output:
        data.to_csv(f'data/{config.output}.csv')
    else:
        print(data.to_string())


# %%

if __name__ == '__main__':

    game_logger.game_log.level = game_logger.game_log.STEP

    game_players_gen, config = exper_config.get_configuration()
    data = build_data_frame()

    play_them_all()
