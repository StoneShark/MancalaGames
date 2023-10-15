# -*- coding: utf-8 -*-
"""Play each config file with each player.
If the game is played in rounds, only one round is played.

Created on Sun Jul 23 11:29:10 2023
@author: Ann"""

import os
import random

import pytest
pytestmark = pytest.mark.integtest

from context import game_log
from context import man_config
# from context import minimax
from context import ai_player

from game_interface import WinCond


PATH = './GameProps/'
FILES = os.listdir(PATH)

BAD_CFG = 'all_params.txt'
if BAD_CFG in FILES:
    FILES.remove(BAD_CFG)


@pytest.fixture(params=FILES)
def game_data(request):
    return man_config.make_game(PATH + request.param)

# TODO fix when alt players integrated again
# @pytest.fixture(params=[minimax.MiniMaxer])
# def player_class(request):
#     return request.param


@pytest.mark.stresstest
def test_one_game(game_data):

    game_log.game_log.active = False

    game, pdict = game_data
    player = ai_player.AiPlayer(game, pdict)

    for _ in range(500):

        if game.turn:
            move = player.pick_move()
        else:
            moves = game.get_moves()
            assert moves, "Game didn't end right."
            move = random.choice(moves)

        cond = game.move(move)
        if cond in (WinCond.WIN, WinCond.TIE, WinCond.ENDLESS,
                    WinCond.ROUND_WIN, WinCond.ROUND_TIE):
            break

        if game.info.mustpass:
            game.test_pass()

    else:
        print("Loop maxed before game ended.", game.info.name)

    if cond == WinCond.ENDLESS:
        print('Abandoned due to endless mlaps.')
