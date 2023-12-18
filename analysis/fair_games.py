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

import argparse
import enum
import math
import os
import random
import sys
import time

import pandas as pd
import scipy
import tqdm

from context import ai_player
from context import man_config

from game_log import game_log
from game_interface import WinCond



# %%

ALL = 'all'


WIN_SCORE = 4
TIE_SCORE = 2

EXPECTED_VAL = WIN_SCORE * 0.5


# %% column names

# raw tally collumns

MAX_TURNS = 'max_turns'

# W_starter_winner
W_F_F = 'w_f_f'
W_F_T = 'w_f_t'
W_T_F = 'w_t_f'
W_T_T = 'w_t_t'

# in order by starter, winner
WINNER_COL = [W_F_F, W_F_T, W_T_F, W_T_T]

# TIE_starter
TIE_T = 'tie_t'
TIE_F = 'tie_f'

# in order by starter
TIE_COL = [TIE_F, TIE_T]

#  two sum columns
SCORE = 'score'
SCORE_2 = 'score_2'   # squared

ST_SCORE = 'st_score'
ST_SCORE_2 = 'st_score_2'

INT_COLUMNS = [MAX_TURNS] + WINNER_COL + TIE_COL + \
              [SCORE, SCORE_2, ST_SCORE, ST_SCORE_2]

MEAN = 'mean'
STDEV = 'stddev'

WIN_PCT = 'win_pct'
STR_PCT = 'str_pct'
TIE_PCT = 'tie_pct'
FLT_COLUMNS = [WIN_PCT, STR_PCT, TIE_PCT]

# fair columsn
WIN_FAIR = 'win_fair'
STARTER_FAIR = 'starter_fair'

BOOL_COLUMNS = [WIN_FAIR, STARTER_FAIR]


# %% files, fields and defaults

PATH = '../GameProps/'
BAD_CFG = 'all_params.txt'

INDEX = [fname[:-4] for fname in os.listdir(PATH) if fname != BAD_CFG]

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


# %%  score and collect

class GameResult(enum.Enum):
    """Game results."""

    WIN = WinCond.WIN.value
    TIE = WinCond.TIE.value
    MAX_TURNS = enum.auto()


def score_game(data, gname, starter, result, winner):
    """Collect sum and sum squared for scores for winner
    and for starter's wins."""

    score = 0
    if result == GameResult.WIN.value and winner:
        score = WIN_SCORE
    elif result == GameResult.TIE.value:
        score = TIE_SCORE
    data.loc[gname, SCORE] += score
    data.loc[gname, SCORE_2] += score * score

    score = 0
    if result == GameResult.WIN.value and winner == starter:
        score = WIN_SCORE
    elif result == GameResult.TIE.value:
        score = TIE_SCORE
    data.loc[gname, ST_SCORE] += score
    data.loc[gname, ST_SCORE_2] += score * score


def result_name(starter, result, winner):
    """Lookup the column name for the result."""

    if result == GameResult.WIN.value:
        return WINNER_COL[starter * 2 + winner]

    if result == GameResult.TIE.value:
        return TIE_COL[starter]

    if result == GameResult.MAX_TURNS.value:
        return MAX_TURNS

    assert f'Unexpedect game result {result}.'


# %%  build data frame


def build_data_frame():
    """Build a data frame with all the desired columns,
    Include key game data (optional), raw game result tallys, two sum values
    for win percents, and fairness columns."""

    if cargs.no_params:
        data = pd.DataFrame(index=cargs.game)

    else:
        ginfo = dict()
        for gname in cargs.game:
            gdict = man_config.read_game(PATH + gname + '.txt')
            cons_gd = dict(**gdict['game_constants'], **gdict['game_info'])
            del cons_gd['about']
            del cons_gd['name']
            ginfo[gname] = cons_gd
        data = pd.DataFrame.from_dict(ginfo).transpose()

        for name, dval in FIELDS.items():
            if name in data:
                data[name] = data[name].fillna(dval)

    dlen = len(cargs.game)

    for col in INT_COLUMNS:
        data[col] = [0] * dlen
    for col in FLT_COLUMNS:
        data[col] = [0.0] * dlen
    for col in BOOL_COLUMNS:
        data[col] = [False] * dlen

    return data


# %% fairness tests

def std_dev(xsum, x_sqr_sum, nbr):
    """Use two sum formula to compute standard deviation."""

    return math.sqrt((x_sqr_sum - ((xsum * xsum) / nbr)) / (nbr - 1))


def fail_to_reject(data, gname, tag, confidence=0.95):
    """H0:  prob of win = 0.5   Ha: prob of win != 0.5

    Failing to reject - means we didn't reject H0
    -- not enough evidence to prove it false"""

    nbr_games = cargs.nbr_runs - data.loc[gname, MAX_TURNS]
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


def evals(gname, data):
    """Compute win_fair and starter_fair."""

    data.loc[gname, WIN_FAIR] = fail_to_reject(data, gname, SCORE)
    data.loc[gname, STARTER_FAIR] = fail_to_reject(data, gname, ST_SCORE)

    nbr_games = cargs.nbr_runs - data.loc[gname, MAX_TURNS]
    data.loc[gname, WIN_PCT] = data.loc[gname, SCORE] / (WIN_SCORE * nbr_games)
    data.loc[gname, STR_PCT] = data.loc[gname, ST_SCORE] / (WIN_SCORE * nbr_games)
    data.loc[gname, TIE_PCT] = \
        (data.loc[gname, TIE_T] + data.loc[gname, TIE_F]) / nbr_games


# %%  play and collect

def test_one_game(game, pdict):
    """Play one game, return the result as
    outcome (win, tie, or max turns) and winner (if one)"""

    if cargs.ai_player:
        tplayer = ai_player.AiPlayer(game, pdict)
        fplayer = ai_player.AiPlayer(game, pdict)

    for _ in range(5000 if game.info.rounds else 500):

        if not cargs.ai_player:
            moves = game.get_moves()
            assert moves, "Game didn't end right."
            move = random.choice(moves)
        else:
            game_log.active = False
            if game.turn:
                move = tplayer.pick_move()
            else:
                move = fplayer.pick_move()
            game_log.active = cargs.save_logs

        cond = game.move(move)
        if cond in (WinCond.WIN, WinCond.TIE):
            break
        if cond in (WinCond.ROUND_WIN, WinCond.ROUND_TIE):
            if game.new_game(cond, new_round_ok=True):
                return cond.value, game.turn
            game_log.turn(0, 'Start Game', game)

        if game.info.mustpass:
            game.test_pass()

    else:
        return GameResult.MAX_TURNS.value, None

    return cond.value, game.turn


def play_one_config(gname, data):
    """For one game configuration, play cargs.nbr_runs number of games.
    Start half with True and half with False.
    Tally raw results and accumualte data for mean/std_dev (score)."""

    for cnt in tqdm.tqdm(range(cargs.nbr_runs)):

        game, pdict = man_config.make_game(PATH + gname + '.txt')
        if cnt < cargs.nbr_runs // 2:
            starter = game.turn = True
        else:
            starter = game.turn = False

        result, winner = test_one_game(game, pdict)

        # raw tally
        col = result_name(starter, result, winner)
        data.loc[gname, col] += 1

        score_game(data, gname, starter, result, winner)
        if cargs.save_logs:
            game_log.save(f'Fair Games Simulated.\n{cargs}\n'
                          + f'Starter: {starter}\n\n'
                          + game.params_str())
            game_log.new()
            time.sleep(1)

    # print(game.params_str())


def play_them_all(data):

    for gname in cargs.game:
        print(gname)
        play_one_config(gname, data)
        evals(gname, data)

    data.to_csv(f'data/{cargs.output}.csv')


# %%  command line args

def define_parser():
    """Define the command line arguements."""

    parser = argparse.ArgumentParser()

    parser.add_argument('--game', action='append',
                        choices=list(INDEX) + [ALL],
                        help="""Select the games to simulate. Use multiple
                        options to select multiple games.""")

    parser.add_argument('--nbr_runs', action='store',
                        default=10, type=int,
                        help="""Select the number of games to simulate.
                        Default: %(default)s""")

    parser.add_argument('--ai_player', action='store_true',
                        help="""Use the minimaxer ai_player.
                        Default: %(default)s""")

    parser.add_argument('--no_params', action='store_true',
                        help="""Don't game parameters in output file.
                        Default: %(default)s""")

    parser.add_argument('--save_logs', action='store_true',
                        help="""Save the game logs. Only one game maybe
                        selected and nbr_games must be < 50.
                        Games will be slowed to 1 per second.
                        Default: %(default)s""")

    parser.add_argument('--output', action='store',
                        default='junk',
                        help="""Output file. Default: %(default)s""")

    # TODO add confidence

    return parser


def process_command_line():

    global cargs

    parser = define_parser()
    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit()

    if not cargs.game:
        cargs.game = INDEX
    if cargs.save_logs and (len(cargs.game) > 1 or cargs.nbr_runs > 50):
        print("save_logs only valid for <= 1 game and <= 50 runs.")
        sys.exit()

    game_log.active = cargs.save_logs
    game_log.level = game_log.STEP

    print(cargs)

# %%

process_command_line()

data = build_data_frame()
play_them_all(data)
