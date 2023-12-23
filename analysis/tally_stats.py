# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 11:29:10 2023
@author: Ann"""


# %% imports

import numpy as np
import pandas as pd
import scipy


# %%  constants

WIN_SCORE = 1
TIE_SCORE = 0.5

EXPECTED_VAL = WIN_SCORE * 0.5

CONFIDENCE = 0.95
CRIT_VALUE = scipy.stats.norm.ppf(1 - (1 - CONFIDENCE) / 2)


# W_starter_winner
W_F_F = 'w_f_f'
W_F_T = 'w_f_t'
W_T_F = 'w_t_f'
W_T_T = 'w_t_t'
TIE_T = 'tie_t'
TIE_F = 'tie_f'
MAX_TURNS = 'max_turns'

TALLIES = [MAX_TURNS, W_F_F, W_F_T, W_T_F, W_T_T, TIE_F, TIE_T]

NBR_RUNS = 'nbr_runs'

SCORE = 'score'
SCORE_2 = 'score_2'   # squared
MEAN = 'mean'
STDEV = 'stddev'

ST_SCORE = 'st_score'
ST_SCORE_2 = 'st_score_2'
ST_MEAN = 'st_mean'
ST_STDEV = 'st_stddev'

WIN_PCT = 'win_pct'
STR_PCT = 'str_pct'
TIE_PCT = 'tie_pct'

Z_SCORE = 'z_score'
WIN_FAIR = 'win_fair'

ST_Z_SCORE = 'st_z_score'
STARTER_FAIR = 'starter_fair'


# %% read

files = ['mlaps_rounds.csv', 'no_mlaps_rounds.csv', 'no_rounds.csv', 'sadeqa.csv']

data = pd.concat(
    [pd.read_csv('data/run30000/' + file, header=0, index_col=0)
     for file in files])


# %%  add stats columns


data[NBR_RUNS] = data[TALLIES[1:]].sum(axis=1)

# create and init these now, they'll be filled later
dlen = len(data.index)
for col in [WIN_PCT, STR_PCT]:
    data[col] = [0] * dlen

data[TIE_PCT] = (data[TIE_F] + data[TIE_T]) / data[NBR_RUNS]


# Determine if each game is symetrically fair,
#   H0: prob(True win) == 0.5
#   e.g. player=True wins as often as player=False
#   False (not fair) likely means that there is a game implementation error

data[SCORE] = (data[W_T_T] + data[W_F_T]) * WIN_SCORE \
              + (data[TIE_T] + data[TIE_F]) * TIE_SCORE
data[SCORE_2] = (data[W_T_T] + data[W_F_T]) * (WIN_SCORE ** 2) \
              + (data[TIE_T] + data[TIE_F]) * (TIE_SCORE ** 2)

data[MEAN] = data[SCORE] / data[NBR_RUNS]
data[STDEV] = \
    np.sqrt((data[SCORE_2]
             - ((data[SCORE] * data[SCORE]) / data[NBR_RUNS]))
            / (data[NBR_RUNS] - 1))

data[Z_SCORE] = ((data[MEAN] - EXPECTED_VAL)
                 / (data[STDEV] / np.sqrt(data[NBR_RUNS])))
data[WIN_FAIR] = np.abs(data[Z_SCORE]) < CRIT_VALUE

# Determine if each game is fair in terms of the starter,
#  starter is equally likely win versus non-starter

data[ST_SCORE] = (data[W_T_T] + data[W_F_F]) * WIN_SCORE \
                + (data[TIE_T] + data[TIE_F]) * TIE_SCORE
data[ST_SCORE_2] = (data[W_T_T] + data[W_F_F]) * (WIN_SCORE ** 2) \
                + (data[TIE_T] + data[TIE_F]) * (TIE_SCORE ** 2)

data[ST_MEAN] = data[ST_SCORE] / data[NBR_RUNS]
data[ST_STDEV] = \
    np.sqrt((data[ST_SCORE_2]
             - ((data[ST_SCORE] * data[ST_SCORE]) / data[NBR_RUNS]))
            / (data[NBR_RUNS] - 1))

data[ST_Z_SCORE] = ((data[ST_MEAN] - EXPECTED_VAL)
                 / (data[ST_STDEV] / np.sqrt(data[NBR_RUNS])))
data[STARTER_FAIR] = np.abs(data[ST_Z_SCORE]) < CRIT_VALUE


data[WIN_PCT] = data[SCORE] / (WIN_SCORE * data[NBR_RUNS])
data[STR_PCT] = data[ST_SCORE] / (WIN_SCORE * data[NBR_RUNS])


# %%

data.to_csv('data/tally_30K_games_1222.csv')
