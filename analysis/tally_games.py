# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 15:58:04 2023
@author: Ann"""

import argparse
import enum
import os
import random
import sys
import time
import traceback

import pandas as pd
import tqdm

from context import ai_player
from context import man_config

from game_log import game_log
from game_interface import WinCond


# %%  tally collumns

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

INIT_COLUMNS = [MAX_TURNS] + WINNER_COL + TIE_COL


# %% files, fields and defaults

PATH = '../GameProps/'
BAD_CFG = 'all_params.txt'

INDEX = [fname[:-4] for fname in os.listdir(PATH) if fname != BAD_CFG]

FIELDS = {
          'holes': 0,
          'nbr_start': 0,
          'allow_rule': 0,
          'blocks': False,
          'capsamedir': False,
          'capt_max': 0,
          'capt_min': 0,
          'capt_on_t': 0,              # changed field
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
          'udirect': 0,              # changed field
          'visit_opp': False,
          'xc_sown': False,
          'xcpickown': 0,
         }


# %%  global variables

data = None
cargs = None


# %%  score and collect

class GameResult(enum.Enum):
    """Game results."""

    WIN = WinCond.WIN.value
    TIE = WinCond.TIE.value
    MAX_TURNS = enum.auto()


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

def convert_list(info, field, new_field):

    if field in info:
        info[new_field] = int(bool(info[field]))
        del info[field]


def build_data_frame():
    """Build a data frame with the desired columns."""

    global data

    if cargs.no_params:
        data = pd.DataFrame(index=cargs.game)

    else:
        data = pd.DataFrame(index=cargs.game, columns=FIELDS.keys())

        for gname in cargs.game:
            gdict = man_config.read_game(PATH + gname + '.txt')

            info = gdict['game_info']
            del info['about']
            del info['name']
            convert_list(info, 'udir_holes', 'udirect')
            convert_list(info, 'capt_on', 'capt_on_t')
            info = {key: info[key] for key in sorted(info.keys())}

            data.loc[gname] = dict(**gdict['game_constants'], **info)

        for name, dval in FIELDS.items():
            if name in data:
                data[name] = data[name].fillna(0)
            if isinstance(dval, bool):
                data[name] = data[name].astype(int)

    dlen = len(cargs.game)
    for col in INIT_COLUMNS:
        data[col] = [0] * dlen



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


def play_one_config(gname):
    """For one game configuration, play cargs.nbr_runs number of games.
    Start half with True and half with False. Tally game results."""

    for cnt in tqdm.tqdm(range(cargs.nbr_runs)):

        game_log.new()
        game, pdict = man_config.make_game(PATH + gname + '.txt')
        if cnt < cargs.nbr_runs // 2:
            starter = game.turn = True
        else:
            starter = game.turn = False

        result, winner = test_one_game(game, pdict)

        # raw tally
        col = result_name(starter, result, winner)
        data.loc[gname, col] += 1

        if cargs.save_logs:
            game_log.save(f'Fair Games Simulated.\n{cargs}\n'
                          + f'Starter: {starter}\n\n'
                          + game.params_str())
            time.sleep(1)


def play_them_all():

    for gname in cargs.game:
        print(gname)

        if cargs.trap_ex:
            try:
                play_one_config(gname)
            except AssertionError as err:
                game_log.save(f'Trapped exception:  {gname}')
                traceback.print_exception(err)
                break
        else:
            play_one_config(gname)

    data.to_csv(f'data/{cargs.output}.csv')


# %%  command line args

def define_parser():
    """Define the command line arguements."""

    parser = argparse.ArgumentParser()

    parser.add_argument('--game', action='append',
                        choices=list(INDEX),
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

    parser.add_argument('--trap_ex', action='store_true',
                        help="""Trap exceptions and save the log.
                        Simulation ends when exception trapped.
                        Default: %(default)s""")

    parser.add_argument('--output', action='store',
                        default='junk',
                        help="""Output file. Default: %(default)s""")

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

    game_log.active = cargs.save_logs | cargs.trap_ex
    game_log.level = game_log.STEP

    print(cargs)


# %%  main

if __name__ == '__main__':

    process_command_line()
    build_data_frame()
    play_them_all()
