# -*- coding: utf-8 -*-
"""Find an ENDLESS sow game setup for testing.

Created on Thu Jul 20 13:05:05 2023
@author: Ann
"""

import itertools as it

from context import game_info as gi
from context import game_constants as gconsts
from context import mancala

from game_info import WinCond
from game_info import Direct
from game_info import Goal
from game_info import LapSower

HOLES = 4

def build_game():

    # game_consts = gconsts.GameConsts(nbr_start=4, holes=HOLES)
    # game_info = gi.GameInfo(mlaps=LapSower.LAPPER,
    #                         crosscapt=True,
    #                         mustshare=True,
    #                         nbr_holes=game_consts.holes,
    #                         rules=mancala.Mancala.rules)


    game_consts = gconsts.GameConsts(nbr_start=4, holes=HOLES)
    game_info = gi.GameInfo(sow_direct=Direct.CW,
                            goal=Goal.DEPRIVE,
                            sow_blkd_div=True,
                            blocks=True,
                            goal_param=3,
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)
    return mancala.Mancala(game_consts, game_info)


def find_endless():

    for board in it.product(range(5), repeat=HOLES * 2):
        for turn in (False, True):
            for start_pos in range(HOLES):

                game = build_game()
                game.turn = turn
                game.board = list(board)

                game.store[0] = game.cts.total_seeds - sum(game.board)
                if game.store[0] < 0:
                    continue

                cond = game.move(start_pos)

                if cond == WinCond.ENDLESS:
                    print(turn, start_pos, board)
                    return



def find_endless_for_mustshare():

    # found some with holes = 4

    for board in it.product(range(24), repeat=HOLES):
        for start_pos in range(HOLES):

            game = build_game()
            game.turn = True
            game.board = [0] * HOLES + list(board)

            game.store[0] = game.cts.total_seeds - sum(game.board)
            if game.store[0] < 0:
                continue

            cond = game.move(start_pos)

            if cond == WinCond.ENDLESS:
                print(start_pos, board)
                return

RUN_FUNC = find_endless
RUN_FUNC()
