# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 09:52:21 2023
@author: Ann"""

# %% imports

import numpy as np
import pandas as pd
import scipy.stats


# %% constants

WIN_SCORE = 1
TIE_SCORE = 0.5

EXPECTED_VAL = WIN_SCORE * 0.5

CONFID = 0.05

W_F_F = 'w_f_f'
W_F_T = 'w_f_t'
W_T_F = 'w_t_f'
W_T_T = 'w_t_t'
TIE_T = 'tie_t'
TIE_F = 'tie_f'
MAX_TURNS = 'max_turns'

# %% read data

files = ['mlaps_rounds.csv', 'no_mlaps_rounds.csv', 'no_rounds.csv', 'sadeqa.csv']

data = pd.concat(
    [pd.read_csv('data/run30000/' + file, header=0, index_col=0)
     for file in files])

data = data.sort_index()

# %%

# gname = 'Wari'


print('GAME                   Symmetric                     ',
      '           Starter                            ')
print('                       Win %       Variance     p-value  ',
      '       Start %     Variance   p-value')

for gname in data.index:

    wins = np.array(
        [WIN_SCORE] * (data.loc[gname][W_T_T] + data.loc[gname][W_F_T]) + \
        [0]         * (data.loc[gname][W_T_F] + data.loc[gname][W_F_F]) + \
        [TIE_SCORE] * (data.loc[gname][TIE_T] + data.loc[gname][TIE_F]))

    starter_wins = np.array(
        [WIN_SCORE] * (data.loc[gname][W_T_T] + data.loc[gname][W_F_F]) + \
        [0]         * (data.loc[gname][W_T_F] + data.loc[gname][W_F_T]) + \
        [TIE_SCORE] * (data.loc[gname][TIE_T] + data.loc[gname][TIE_F]))


    win_desc = scipy.stats.describe(wins)
    win_res = scipy.stats.ttest_1samp(wins, popmean=0.5)

    str_desc = scipy.stats.describe(starter_wins)
    str_res = scipy.stats.ttest_1samp(starter_wins, popmean=0.5)

    print(f'{gname:20}',
          f'{win_desc.mean:10.4%}  {win_desc.variance:12.8f}', f'{win_res.pvalue:12.8f}',
          '***' if win_res.pvalue < CONFID else '   ',
          f'{str_desc.mean:10.4%}  {str_desc.variance:12.8f}', f'{str_res.pvalue:12.8f}',
          '***' if str_res.pvalue < CONFID else '   ',
          )
