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
       had bad endings (for each game config).

Created on Sun Jul 23 11:29:10 2023
@author: Ann"""

import atexit
import os
import random

import pytest
pytestmark = pytest.mark.integtest

from context import game_logger

from game_interface import WinCond

# uncomment, if you should wish to skip this test
# pytest.skip(reason="Random play. Heuristic eval.", allow_module_level=True)


PATH = './GameProps/'
FILES = os.listdir(PATH)

BAD_CFG = '_all_params.txt'
if BAD_CFG in FILES:
    FILES.remove(BAD_CFG)


# games that generally fail and the reason

XFAIL_GAMES = {
    'Urim': "10 points can't generally be achieved within test limits.",
    'Ohojichi': "Random play is very bad; games don't finish.",
    'Bule Perga': "Easy for game to reach cycling state."
    }


@pytest.fixture(autouse=True)
def no_logger():
    """Make certain that no other test left the logger active."""
    game_logger.game_log.active = False


@pytest.mark.no_seed
@pytest.mark.stresstest
@pytest.mark.parametrize('game_pdict', FILES, indirect=True)
def test_one_game(request, game_pdict):

    game, _ = game_pdict

    nbr_moves = 500
    if game.info.rounds:
        nbr_moves *= 4
    if game.info.capt_rturn or game.info.sow_own_store:
        nbr_moves *= 2

    for _ in range(nbr_moves):
        moves = game.get_moves()
        if not moves:
            pytest.fail("Game didn't end right.")

        cond = game.move(random.choice(moves))
        if cond and cond.is_game_over():
            return

        if cond and cond.is_round_over():
            game.new_game(new_round=True)

        if game.info.mustpass:
            game.test_pass()

    key_name = game.info.name + '_loop_max'
    cnt = request.config.cache.get(key_name, 0)
    request.config.cache.set(key_name, cnt + 1)


@pytest.fixture
def known_game_fails(request):

    game, _ = request.getfixturevalue('game_pdict')
    if game.info.name in XFAIL_GAMES:
        request.node.add_marker(
            pytest.mark.xfail(reason=XFAIL_GAMES[game.info.name],
                              strict=False))


@pytest.mark.usefixtures('known_game_fails')
@pytest.mark.parametrize('game_pdict', FILES, indirect=True)
def test_game_stats(pytestconfig, request, game_pdict, nbr_runs):

    def report_bad(maxed, total):
        print(f'Bad endings for {game.info.name:12}: loop_max= {maxed:4}  ',
              f' {maxed/total:>6.1%}')

    game, _ = game_pdict
    key_name = game.info.name + '_loop_max'
    maxed = request.config.cache.get(key_name, 0)

    if maxed:
        atexit.register(report_bad, maxed, nbr_runs)

    # don't record test failures when running on github
    if not pytestconfig.getoption('--sim_fails'):
        return

    if game.info.mlaps:
        thresh = 0.50
    else:
        thresh = 0.25

    assert maxed <= nbr_runs * thresh, \
        f'Bad endings too high for {game.info.name}: loop_max= {maxed}'
