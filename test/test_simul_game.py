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

import atexit
import os
import random

import pytest
pytestmark = pytest.mark.integtest

from context import man_config
from context import game_log

from game_interface import WinCond

# pytest.skip(reason="Random play. Heuristic eval.", allow_module_level=True)


PATH = './GameProps/'
FILES = os.listdir(PATH)

BAD_CFG = 'all_params.txt'
if BAD_CFG in FILES:
    FILES.remove(BAD_CFG)


@pytest.fixture(params=FILES)
def game_data(request):
    return man_config.make_game(PATH + request.param)

@pytest.mark.stresstest
def test_one_game(game_data, request):

    game, _ = game_data
    game_log.game_log.active = False

    for _ in range(3000 if game.info.rounds else 500):
        moves = game.get_moves()
        assert moves, "Game didn't end right."

        cond = game.move(random.choice(moves))
        if cond in (WinCond.WIN, WinCond.TIE, WinCond.ENDLESS):
            break
        if cond in (WinCond.ROUND_WIN, WinCond.ROUND_TIE):
            if game.new_game(cond, new_round_ok=True):
                return

        if game.info.mustpass:
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


@pytest.fixture
def known_game_fails(request):

    game, _ = request.getfixturevalue('game_data')
    if game.info.name in ['Bao', 'Congklak', 'Erherhe', 'Eson Xorgol',
                          'Gabata', 'NamNam', 'Pallam Kuzhi', 'Weg']:
        request.node.add_marker(
            pytest.mark.xfail(
                reason='Many seeds; heuristic test; occasionally fails.',
                strict=False))


@pytest.mark.usefixtures('known_game_fails')
def test_game_stats(game_data, request, nbr_runs):

    def report_bad(maxed, stuck):
        print(f'Bad endings for {game.info.name:12}: ' + \
              f'loop_max= {maxed}  endless= {stuck}')

    game, _ = game_data
    key_name = game.info.name + '/loop_max'
    maxed = request.config.cache.get(key_name, 0)

    key_name = game.info.name + '/endless'
    stuck = request.config.cache.get(key_name, 0)

    if maxed or stuck:
        atexit.register(report_bad, maxed, stuck)

    assert maxed + stuck <= nbr_runs * 0.2, \
        f'Bad endings too high for {game.info.name}: ' + \
            f'loop_max= {maxed}  endless= {stuck}'
