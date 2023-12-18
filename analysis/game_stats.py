# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 23:10:58 2023
@author: Ann"""


# %% imports

import argparse
import sys

import numpy as np
import pandas as pd
import scipy


# %% constants

WIN_SCORE = 1
TIE_SCORE = 0.5
EXPECTED_VAL = WIN_SCORE * 0.5

CONFIDENCE = 0.95
CRIT_VALUE = scipy.stats.norm.ppf(1 - (1 - CONFIDENCE) / 2)



# %%  command line args

def define_parser():
    """Define the command line arguements."""

    parser = argparse.ArgumentParser()

    parser.add_argument('--input', action='store',
                        required=True,
                        help="""Input file.""")

    parser.add_argument('--output', action='store',
                        help="""Output file. Default is 'cltd_' + input.""")

    return parser


def process_command_line():
    """Process the command line. Store data in cargs."""

    global cargs

    parser = define_parser()
    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit()

    if not cargs.output:
        cargs.output = 'cltd_' + cargs.input

    print(cargs)


# %%  read data

def read_data():

    global data

    data = pd.read_csv('data/' + cargs.input + '.csv',
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


# %% compute status

def win_cnt_agg(outcomes):
    return sum(1 for val in outcomes if val == 'WIN')

def tie_cnt_agg(outcomes):
    return sum(1 for val in outcomes if val == 'TIE')


def build_table():

    global data, cltd

    cltd = pd.pivot_table(data[data.rnd_turns == 0],
                          index='name',
                          columns=['starter', 'winner'],
                          values='outcome',
                          aggfunc=win_cnt_agg)

    cltd.columns = [f's{str(col[0])[0]}_win{str(col[1])[0]}'
                    for col in cltd.columns.values]
    cltd = cltd.fillna(0)


    # collect the tie data and add it to collected (cltd)
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




# %%

if __name__ == '__main__':

    process_command_line()

    read_data()
    build_table()
    cltd.to_csv('data/' + cargs.output + '.csv')
