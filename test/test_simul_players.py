# -*- coding: utf-8 -*-
"""Play each config file with each player.
If the game is played in rounds, only one round is played.

Created on Sun Jul 23 11:29:10 2023
@author: Ann"""

import os
import random
import sys

import pytest

sys.path.extend(['src'])

from game_log import game_log
import man_config
import minimax
# import montecarlo_ts

from game_interface import WinCond



PLAY_NBR = 10

PATH = './GameProps/'
FILES = os.listdir(PATH)

BAD_CFG = 'all_params.txt'
if BAD_CFG in FILES:
    FILES.remove(BAD_CFG)


@pytest.fixture(params=FILES)
def game(request):
    return man_config.make_game(PATH + request.param)


@pytest.fixture(params=[minimax.MiniMaxer])
def player_class(request):
    return request.param


def test_one_game(game, player_class):

    game_log.active = False

    player = player_class(game)
    game.set_player(player)

    for _ in range(500):

        if game.turn:
            move = game.player.pick_move()
        else:
            moves = game.get_moves()
            assert moves, "Game didn't end right."
            move = random.choice(moves)

        cond = game.move(move)
        if cond in (WinCond.WIN, WinCond.TIE, WinCond.ENDLESS,
                    WinCond.ROUND_WIN, WinCond.ROUND_TIE):
            break

        if game.info.flags.mustpass:
            game.test_pass()

    else:
        print("Loop maxed before game ended.", game.info.name)

    if cond == WinCond.ENDLESS:
        print('Abandoned due to endless mlaps.')
