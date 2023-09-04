# -*- coding: utf-8 -*-
"""The purpose of this code is to gain some
statistical confidence in each game by playing
a bunch of random games and trapping egregious
errors.

There are asserts in the mancala code that catches
some errors.

Several errors are detected below:
    1. A game gets to 'move' but there are no valid moves.
       The previous move turn should have detected an
       end game condition.

    2. A game doesn't end in a set number of moves.
       This could be normal or an actual error.
       Only raises an error in > 20% of the games
       had bad endings (for each game config)>

A game log is created and output on detected
error conditions. Note the normal game log is created
by the Mancala_UI (because it knows if an AI is
playing).

Created on Sun Jul 23 11:29:10 2023
@author: Ann"""

import os
import random
import sys

import pytest

sys.path.extend(['src'])

from game_log import game_log
import man_config

from game_interface import WinCond

# pytest.skip(reason="Random play. Hueristic eval.", allow_module_level=True)


PLAY_NBR = 10

PATH = './GameProps/'
FILES = os.listdir(PATH)

BAD_CFG = 'all_params.txt'
if BAD_CFG in FILES:
    FILES.remove(BAD_CFG)


@pytest.fixture(params=FILES)
def game(request):
    return man_config.make_game(PATH + request.param)


@pytest.mark.parametrize('play_nbr', range(PLAY_NBR))
def test_one_game(game, request, play_nbr):

    game_log.active = False

    max_turns = 1000 if game.info.flags.rounds else 500
    for _ in range(max_turns):
        moves = game.get_moves()
        assert moves, "Game didn't end right."

        move = random.choice(moves)

        cond = game.move(move)
        if cond in (WinCond.WIN, WinCond.TIE, WinCond.ENDLESS):
            break
        if cond in (WinCond.ROUND_WIN, WinCond.ROUND_TIE):
            if game.new_game(new_round_ok=True):
                return

        if game.info.flags.mustpass:
            game.test_pass()

    else:
        key_name = game.info.name + '/loop_max'
        cnt = request.config.cache.get(key_name, 0)
        request.config.cache.set(key_name, cnt + 1)
        print("Loop maxed before game ended.", game.info.name)

    if cond == WinCond.ENDLESS:
        key_name = game.info.name + '/endless'
        cnt = request.config.cache.get(key_name, 0)
        request.config.cache.set(key_name, cnt + 1)
        print('Abandoned due to endless mlaps.')


def test_game_stats(game, request):

    key_name = game.info.name + '/loop_max'
    maxed = request.config.cache.get(key_name, 0)

    key_name = game.info.name + '/endless'
    stuck = request.config.cache.get(key_name, 0)

    assert maxed + stuck <= PLAY_NBR * 0.2, \
        f'Bad endings too high for {game.info.name}: ' + \
            f'loop_max= {maxed}  endless= {stuck}'
