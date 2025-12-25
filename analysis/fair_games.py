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

import logging

import pandas as pd
import scipy

import ana_logger
import exper_config
import play_game

from context import game_logger

from play_game import GameResult


logger = logging.getLogger()


# %% column names and types

TRUE_WIN = 't_wins'
STRT_WIN = 'str_wins'
NO_RESULT = 'no_result'
ENDLESS = 'endless'

WIN_PCT = 't_win_pct'
STR_PCT = 'str_w_pct'
TIE_PCT = 'tie_pct'

WINR_PVAL = 'win_pval'
STRT_PVAL = 'starter_pval'

WINR_FAIR = 'win_fair'
STRT_FAIR = 'starter_fair'

INT_COLUMNS = play_game.GAME_RESULTS + [NO_RESULT, ENDLESS, TRUE_WIN, STRT_WIN]
FLT_COLUMNS = [WIN_PCT, STR_PCT, TIE_PCT, WINR_PVAL, STRT_PVAL]
BOOL_COLUMNS = [WINR_FAIR, STRT_FAIR]

MAX_TURNS = play_game.GameResult.MAX_TURNS.name
LOOPED = play_game.GameResult.LOOPED.name


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

def compute_pvalues(total, wins):

    res = scipy.stats.chisquare([wins, total - wins],
                                [total / 2] * 2)
    return res.pvalue


def eval_game(gname, nbr_runs, game_res):
    """Copy the values from game_res into the data frame
    and compute win_fair and starter_fair for one game configuration."""

    # copy data and count wins
    total_wins = 0
    for starter in (False, True):
        for winner in (False, True):
            rname = play_game.result_name(starter, GameResult.WIN, winner)
            data.loc[gname, rname] = game_res.stats[rname]
            total_wins += game_res.stats[rname]

        rname = play_game.result_name(starter, GameResult.TIE, None)
        data.loc[gname, rname] = game_res.stats[rname]

    data.loc[gname, LOOPED] = game_res.stats[LOOPED]
    data.loc[gname, MAX_TURNS] = game_res.stats[MAX_TURNS]

    data.loc[gname, TRUE_WIN] = game_res.wins[True]
    data.loc[gname, STRT_WIN] = game_res.starter_wins[0]

    # do eval
    data.loc[gname, NO_RESULT] = sum([game_res.stats[LOOPED],
                                      game_res.stats[MAX_TURNS]])
    data.loc[gname, ENDLESS] = game_res.endless

    data.loc[gname, WINR_PVAL] = compute_pvalues(total_wins,
                                                 data.loc[gname, TRUE_WIN])
    data.loc[gname, STRT_PVAL] = compute_pvalues(total_wins,
                                                 data.loc[gname, STRT_WIN])

    data.loc[gname, WINR_FAIR] = data.loc[gname, WINR_PVAL] > 0.05
    data.loc[gname, STRT_FAIR] = data.loc[gname, STRT_PVAL] > 0.05

    if not total_wins:
        data.loc[gname, WIN_PCT] = 0
        data.loc[gname, STR_PCT] = 0
        data.loc[gname, TIE_PCT] = 0
        return

    data.loc[gname, WIN_PCT] = data.loc[gname, TRUE_WIN] / total_wins
    data.loc[gname, STR_PCT] = data.loc[gname, STRT_WIN] / total_wins
    data.loc[gname, TIE_PCT] = game_res.ties / nbr_runs


# %%  play and collect

def play_them_all():

    for game, fplayer, tplayer, gname in game_players_gen:
        logger.info(game.info.name)
        logger.info(f'False {str(fplayer)}')
        logger.info(f'True {str(tplayer)}')

        game_res = play_game.play_games(game, fplayer, tplayer,
                                        config.nbr_runs,
                                        move_limit=config.max_moves,
                                        end_all=config.end_all)
        logger.info('\n' + str(game_res))

        eval_game(gname, config.nbr_runs, game_res)
        logger.info('Win Fair:    ' + str(data.loc[gname, WINR_FAIR]))
        logger.info('StarterFair: ' + str(data.loc[gname, STRT_FAIR]))

    if len(data) < 6:
        header = ' ' * 13
        for gname in data.index:
            header += f'{gname[:12]:>13}'
        logger.info(header)

        for key in data.keys():
            line = f'{key:13}'
            for gname in data.index:
                if 'pct' in key:
                    line += f'{data.loc[gname, key]:13.3%}'
                elif 'pval' in key:
                    line += f'{data.loc[gname, key]:13.6}'
                elif 'fair' in key:
                    line += f'{str(data.loc[gname, key]):>13}'
                else:
                    line += f'{data.loc[gname, key]:13}'
            logger.info(line)
    else:
        logger.info(data.to_string())


# %%

if __name__ == '__main__':

    with ana_logger.trap_close(logger):

        game_logger.game_log.level = game_logger.game_log.STEP
        game_players_gen, config = exper_config.get_configuration()
        data = build_data_frame()

        play_them_all()

    # output whatever is in the data frame, even if there was an exception
    if config.output:
        data.to_csv(config.output + '.csv')
