# -*- coding: utf-8 -*-
"""Goal:  compute stats on game lengths

Created on Sun Jul 23 11:29:10 2023
@author: Ann"""

import argparse
import dataclasses as dc
import math
import os
import random
import statistics
import sys

import pandas as pd
import scipy
import tqdm

from context import ai_player
from context import game_log
from context import man_config

from game_interface import WinCond


game_log.game_log.active = False


# %%

ALL = 'all'

PATH = '../GameProps/'
BAD_CFG = 'all_params.txt'

INDEX = [fname[:-4] for fname in os.listdir(PATH) if fname != BAD_CFG]


# %%  data

@dc.dataclass
class GameStats:

    turns_per_game: list[int] = dc.field(default_factory=list)
    rounds_per_game: list[int] = dc.field(default_factory=list)
    turns_per_round: list[int] = dc.field(default_factory=list)



# %%

def one_stat(intro, values):

    if not values:
        return

    sumv = sum(values)
    mean = sumv / cargs.nbr_runs
    median = statistics.median(values)
    stdd = statistics.stdev(values, mean)
    skew = scipy.stats.skew(values)

    print(f'{intro:12}  {sumv:10}  {median:10}  {mean:12.4}  {stdd:12.4}  {skew:12.4}')


def print_stats(gstats):

    print('\n                   Total      Median          Mean       Std Dev          Skew')
    one_stat('Turns:', gstats.turns_per_game)
    one_stat('Rounds:', gstats.rounds_per_game)
    one_stat('T per Rnd:', gstats.turns_per_round)



# %%  play and collect

def test_one_game(game, pdict, gstats):
    """Play one game, tally the counts in gstats"""

    round_cnt = 0
    round_start = 0

    if cargs.ai_player:
        tplayer = ai_player.AiPlayer(game, pdict)
        fplayer = ai_player.AiPlayer(game, pdict)

    for turns in range(10000 if game.info.rounds else 100):

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
            round_cnt += 1
            gstats.turns_per_round += [turns - round_start]
            round_start = turns

            if game.new_game(cond, new_round_ok=True):
                break

        if game.info.mustpass:
            game.test_pass()

    gstats.turns_per_game += [turns]
    if round_cnt > 0:
        gstats.rounds_per_game += [round_cnt]


def play_one_config(gname):
    """For one game configuration, play cargs.nbr_runs number of games.
    Collect data in the associated GameStats."""

    for cnt in range(cargs.nbr_runs):

        game, pdict = man_config.make_game(PATH + gname + '.txt')
        if cnt < cargs.nbr_runs // 2:
            game.turn = True
        else:
            game.turn = False

        test_one_game(game, pdict, all_data[gname])


def play_them_all():

    for gname in cargs.game:
        print(gname)
        play_one_config(gname)
        print_stats(all_data[gname])


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

    return parser


def process_command_line():

    global cargs, all_data

    parser = define_parser()
    try:
        cargs = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit()

    if not cargs.game:
        cargs.game = INDEX
    all_data = {gname: GameStats() for gname in cargs.game}

    print(cargs)


# %%

process_command_line()

play_them_all()
