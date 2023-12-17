# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 23:10:58 2023
@author: Ann"""


# %% imports

import numpy as np
import pandas as pd
import scipy


# %% load data

data = pd.read_csv('data/gstats_44_1000_1216_1608.csv',
                   dtype={'name': str,
                          'starter': bool,
                          'turns': int,
                          'outcome': str,
                          'winner': bool,
                          'passes': int,
                          'repeats': int,
                          'rounds': int,
                          'rnd_turns': int},
                   header=0,
                   index_col='name')


# %%  fairness


WIN_SCORE = 4
TIE_SCORE = 2
EXPECTED_VAL = WIN_SCORE * 0.5

CONFIDENCE = 0.95
CRIT_VALUE = scipy.stats.norm.ppf(1 - (1 - CONFIDENCE) / 2)


def win_cnt_agg(outcomes):
    return sum(1 for val in outcomes if val == 'WIN')

cltd = pd.pivot_table(data[data.rnd_turns == 0],
                      index='name',
                      columns=['starter', 'winner'],
                      values='outcome',
                      aggfunc=win_cnt_agg)

cltd.columns = [f's{str(col[0])[0]}_win{str(col[1])[0]}'
                for col in cltd.columns.values]
cltd = cltd.fillna(0)

def tie_cnt_agg(outcomes):
    return sum(1 for val in outcomes if val == 'TIE')

ties = pd.pivot_table(data[data.rnd_turns == 0],
                      index='name',
                      columns=['starter'],
                      values='outcome',
                      aggfunc=tie_cnt_agg)

cltd['sT_tie'] = ties[True]
cltd['sF_tie'] = ties[False]

cltd['nbr_runs'] = [sum(cltd.loc[game]) for game in cltd.index]


# Determine if each game is symetrically fair,
#   H0: prob(True win) == 0.5
#   e.g. player=True wins as often as player=False
#   False (not fair) likely means that there is a game implementation error

cltd['score'] = (cltd['sT_winT'] + cltd['sF_winT']) * WIN_SCORE \
              + (cltd['sT_tie'] + cltd['sF_tie']) * TIE_SCORE
cltd['score_2'] = (cltd['sT_winT'] + cltd['sF_winT']) * (WIN_SCORE ** 2) \
              + (cltd['sT_tie'] + cltd['sF_tie']) * (TIE_SCORE ** 2)

cltd['t_win_pct'] = cltd['score'] / (WIN_SCORE * cltd['nbr_runs'])

cltd['mean'] = cltd['score'] / cltd['nbr_runs']
cltd['stddev'] = \
    np.sqrt((cltd['score_2']
             - ((cltd['score'] * cltd['score']) / cltd['nbr_runs']))
            / (cltd['nbr_runs'] - 1))

cltd['fair'] = (((cltd['mean'] - EXPECTED_VAL)
                  / (cltd['stddev'] / np.sqrt(cltd['nbr_runs'])))
                 < CRIT_VALUE)


# Determine if each game is fair in terms of the starter,
#  starter is equally likely win versus non-starter

cltd['st_score'] = (cltd['sT_winT'] + cltd['sF_winF']) * WIN_SCORE \
                + (cltd['sT_tie'] + cltd['sF_tie']) * TIE_SCORE
cltd['st_score_2'] = (cltd['sT_winT'] + cltd['sF_winF']) * (WIN_SCORE ** 2) \
                + (cltd['sT_tie'] + cltd['sF_tie']) * (TIE_SCORE ** 2)

cltd['st_win_pct'] = cltd['st_score'] / (WIN_SCORE * cltd['nbr_runs'])

cltd['st_mean'] = cltd['st_score'] / cltd['nbr_runs']
cltd['st_stddev'] = \
    np.sqrt((cltd['st_score_2']
             - ((cltd['st_score'] * cltd['st_score']) / cltd['nbr_runs']))
            / (cltd['nbr_runs'] - 1))

cltd['st_fair'] = (((cltd['st_mean'] - EXPECTED_VAL)
                  / (cltd['st_stddev'] / np.sqrt(cltd['nbr_runs'])))
                 < CRIT_VALUE)

cltd.to_csv('data/collected.csv')



# %%

adata = pd.read_csv('data/gstats_44_1000_1211_0933.csv',
                   dtype={'name': str,
                          'starter': bool,
                          'turns': int,
                          'outcome': str,
                          'winner': bool,
                          'passes': int,
                          'repeats': int,
                          'rounds': int,
                          'rnd_turns': int},
                   header=0,
                   index_col='name')


def score(outcome):
    if outcome == 'WIN':
        return WIN_SCORE
    if outcome == 'TIE':
        return TIE_SCORE
    return 0

adata['score'] = [score(out) for out in adata.outcome]

# need to drop rows with mlap and turn == 9990 and not mlap and turn == 998

for name, group in  adata[adata.rnd_turns == 0].groupby('name'):
    print('{:15}  {:6}  {:12.8}'.format(
            name, len(group),
            scipy.stats.skew(group.score)))
