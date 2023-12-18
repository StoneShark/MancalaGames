# -*- coding: utf-8 -*-
"""Collect raw data on game play.
Record a record for each round end and game end.

Game end records will always have rnd_turns equal to 0.
Round end records will have rnd_turns > 0.

At the end of a game that is played in rounds two records
are collected:
    - the round end with the correct round starter with round turns
    - the game end with the correct game starter and rnd_turns == 0

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
                        choices=list(INDEX),
                        help="""Select the games to simulate. Use multiple
                        options to select multiple games. Don't use the option
                        to include all defined games.""")

    parser.add_argument('--nbr_runs', action='store',
                        default=100, type=int,
                        help="""Select the number of games to simulate.
                        Default: %(default)s""")

    parser.add_argument('--ai_player', action='store_true',
                        help="""Use the minimaxer ai_player.
                        Default: %(default)s""")

    parser.add_argument('--no_rounds', action='store_true',
                        help="""Don't output round data.
                        Default: %(default)s""")

    parser.add_argument('--output', action='store',
                        help="""Output file.
                        Month, day and time are always appended
                        to keep accidentally overwritting a valuable file.""")

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

    if not cargs.game:
        cargs.game = INDEX

    if not cargs.output:
        game_cnt = len(cargs.game)
        gname = cargs.game[0] if game_cnt == 1 else str(game_cnt)
        cargs.output = f'gstats_{gname}_{cargs.nbr_runs}'
    cargs.output += datetime.datetime.now().strftime('_%m%d_%H%M')

    print(cargs)


# %% data record and frame

@dc.dataclass
class GameRecord:
    """Use a dataclass to facilitate making the dictionary."""

    name: str
    starter: bool
    turns: int
    outcome: WinCond
    winner: bool

    passes: int = 0
    repeats: int = 0
    rounds: int = 0
    rnd_turns: int = 0


def build_data_frame():
    """Build a data frame with all the desired columns."""

    global data
    data = pd.DataFrame(columns=[f.name for f in dc.fields(GameRecord)])


# %%  play and collect

def test_one_game(game, pdict):
    """Play one game, talling the round and game results."""

    round_count = round_start = repeats = passes = 0
    starter = game.starter

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
            if not cargs.no_rounds:
                data.loc[len(data)] = dc.asdict(GameRecord(
                    game.info.name, game.starter, turns, cond.name, game.turn,
                    passes, repeats, round_count, turns - round_start))
            round_start = turns
            repeats = passes = 0

            if game.new_game(cond, new_round_ok=True):
                # shouldn't get here because WIN/TIE were already addressed
                assert False, 'Unexpected new game (not new round).'

        if game.info.mustpass:
            if game.test_pass():
                passes += 1

    end_cond = cond.name if cond else 'MAX_LOOP'
    if round_count:
        # end of round record
        data.loc[len(data)] = dc.asdict(GameRecord(
            game.info.name, game.starter, turns, end_cond, game.turn,
            passes, repeats, round_count, turns - round_start))

    #end of game record
    data.loc[len(data)] = dc.asdict(GameRecord(
            game.info.name, starter, turns, end_cond, game.turn,
            passes, repeats, round_count, 0))


def play_one_config(gname):
    """For one game configuration, play cargs.nbr_runs number of games."""

    for cnt in tqdm.tqdm(range(cargs.nbr_runs)):

        game, pdict = man_config.make_game(PATH + gname + '.txt')
        if cnt < cargs.nbr_runs // 2:
            game.starter = game.turn = True
        else:
            game.starter = game.turn = False

        test_one_game(game, pdict)


def play_them_all():
    """Play all the games and then write the output file."""

    for gname in cargs.game:
        print(gname)
        play_one_config(gname)

    data.to_csv(f'data/{cargs.output}.csv')


# %%   main

if __name__ == '__main__':

    process_command_line()
    build_data_frame()

    play_them_all()
