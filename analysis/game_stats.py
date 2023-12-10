# -*- coding: utf-8 -*-
"""Goal:  compute stats on game lengths

Created on Sun Jul 23 11:29:10 2023
@author: Ann"""

import argparse
import dataclasses as dc
import datetime
import os
import random
import sys

import pandas as pd
import tqdm

from context import ai_player
from context import game_log
from context import man_config

from game_interface import WinCond


game_log.game_log.active = False


# %%  game index list

ALL = 'all'

PATH = '../GameProps/'
BAD_CFG = 'all_params.txt'

INDEX = [fname[:-4] for fname in os.listdir(PATH) if fname != BAD_CFG]


# %%  command line args

def define_parser():
    """Define the command line arguements."""

    parser = argparse.ArgumentParser()

    parser.add_argument('--game', action='append',
                        choices=list(INDEX) + [ALL],
                        help="""Select the games to simulate. Use multiple
                        options to select multiple games.""")

    parser.add_argument('--nbr_runs', action='store',
                        default=100, type=int,
                        help="""Select the number of games to simulate.
                        Default: %(default)s""")

    parser.add_argument('--ai_player', action='store_true',
                        help="""Use the minimaxer ai_player.
                        Default: %(default)s""")

    parser.add_argument('--output', action='store',
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

    if not cargs.output:
        game_cnt = len(cargs.game)
        gname = cargs.game[0] if game_cnt == 1 else str(game_cnt)
        cargs.output = f'gstats_{gname}_{cargs.nbr_runs}'
        # cargs.output += '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    print(cargs)


# %% data record and frame

@dc.dataclass
class GameRecord:

    name: str
    starter: bool
    turns: int
    outcome: WinCond
    winner: object      # True, False or None

    passes: int = dc.field(default=0, kw_only=True)
    repeats: int = dc.field(default=0, kw_only=True)
    rounds: int = dc.field(default=0, kw_only=True)
    rnd_turns: int = dc.field(default=0, kw_only=True)


def build_data_frame():
    """Build a data frame with all the desired columns,
    Include key game data (optional), raw game result tallys, two sum values
    for win percents, and fairness columns."""

    global data
    data = pd.DataFrame(columns=[f.name for f in dc.fields(GameRecord)])


# %%  play and collect

def test_one_game(game, pdict):
    """Play one game, tally the counts in gstats"""

    round_count = round_start = repeats = passes = 0

    if cargs.ai_player:
        tplayer = ai_player.AiPlayer(game, pdict)
        fplayer = ai_player.AiPlayer(game, pdict)

    for turns in range(10000 if game.info.rounds else 1000):

        if not cargs.ai_player:
            moves = game.get_moves()
            assert moves, "Game didn't end right."
            move = random.choice(moves)
        else:
            if game.turn:
                move = tplayer.pick_move()
            else:
                move = fplayer.pick_move()

        cond = game.move(move)

        if cond == WinCond.REPEAT_TURN:
            repeats += 1
        if cond in (WinCond.WIN, WinCond.TIE):
            break
        if cond in (WinCond.ROUND_WIN, WinCond.ROUND_TIE):
            round_count += 1
            data.loc[len(data)] = dc.asdict(GameRecord(
                game.info.name, game.starter, turns, cond.name, game.turn,
                passes=passes,
                repeats=repeats,
                rounds=round_count,
                rnd_turns=turns - round_start if round_count else 0))
            round_start = turns
            repeats = passes = 0

            if game.new_game(cond, new_round_ok=True):
                break

        if game.info.mustpass:
            if game.test_pass():
                passes += 1

    end_cond = cond.name if cond else None
    data.loc[len(data)] = dc.asdict(GameRecord(
        game.info.name, game.starter, turns, end_cond, game.turn,
        passes=passes,
        repeats=repeats,
        rounds=round_count,
        rnd_turns=turns - round_start if round_count else 0))


def play_one_config(gname):
    """For one game configuration, play cargs.nbr_runs number of games.
    Collect data in the associated GameStats."""

    for cnt in tqdm.tqdm(range(cargs.nbr_runs)):

        game, pdict = man_config.make_game(PATH + gname + '.txt')
        if cnt < cargs.nbr_runs // 2:
            game.starter = game.turn = True
        else:
            game.starter = game.turn = False

        test_one_game(game, pdict)


def play_them_all():

    for gname in cargs.game:
        print(gname)
        play_one_config(gname)

    data.to_csv(f'data/{cargs.output}.csv')


# %%

process_command_line()
build_data_frame()

play_them_all()
