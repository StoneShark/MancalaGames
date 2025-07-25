# -*- coding: utf-8 -*-
"""Test each AI Player against each game.

This test will only be run when --run_slow is provided
as a command line option.

First, test the AI Player as configured. A configuration error
is treated as a test failure.

Second, swap in each of the AI algorithms. If there's an error
generating the player, assume that the game is not suitable
for the configuration and skip the test.

AI player is played as False, which is different than UI play.
The first player is True, this avoids most issues with
move number not being right in the Monte Carlo Tree Search
algorithm:
    - prescribed openings will not be by AI player
    - allowable OnlyRightTwo only applies to the first move
    - nocaptmoves only applies to the first N turn

All games are limited to 50 moves;
that'll be about 25 for the ai player.
If the game is played in rounds, only one round is played.
Goal is to give the AI Players a solid amount of exerice
but not delay the tests too much.

Games are also timed, game taking longer than TESTLIMIT are failed.
Note that each move is completed in it's entirety; timeouts are
only checked between moves.
pytest-timeout was tried but could not find a way to cancel a
test gracefully.

Created on Sun Jul 23 11:29:10 2023
@author: Ann"""

import os
import random
import time

import pytest

from context import ai_player
from context import cfg_keys as ckey
from context import game_info as gi
from context import game_logger

# limit the length of these tests, exceeding TESTLIMIT is a test failure

NBR_MOVES = 50
SEC_PER_MOVE = 2
TESTLIMIT = NBR_MOVES * SEC_PER_MOVE


PATH = './GameProps/'
FILES = os.listdir(PATH)

BAD_CFG = '_all_params.txt'
if BAD_CFG in FILES:
    FILES.remove(BAD_CFG)


CONFIGED = 'configed'

ALGOS = [CONFIGED] + list(ai_player.ALGORITHM_DICT.keys())


@pytest.fixture(autouse=True)
def no_logger():
    """Make certain that no other test left the logger active."""
    game_logger.game_log.active = False


@pytest.mark.no_seed
@pytest.mark.slow
@pytest.mark.filterwarnings('ignore:Monte Carlo')
@pytest.mark.parametrize('algo', ALGOS)
@pytest.mark.parametrize('game_pdict', FILES, indirect=True)
def test_one_game(game_pdict, algo):
    """Play a shortend game to exercise the Ai players."""

    game, pdict = game_pdict

   # for test repeatability AND avoids move MCTS/move nbr issues
    game.turn = True

    if algo != CONFIGED:
        pdict[ckey.ALGORITHM] = algo

    # build the AiPlayer checking the rules, catch failures
    try:
        player = ai_player.AiPlayer(game, pdict)
    except gi.GameInfoError as error:

        if (algo == 'negamaxer'
                and ai_player.negamax_no_repeat_turn(game)):
            # negamaxer cannot be used with games that do not alternate turns
            pytest.skip("negamaxer requires alternate turns")

        elif (algo == 'montecarlo_ts'
                  and ai_player.mcts_no_hidden_state(game)):
            # mcts assumes no hidden state data (see function and rule)
            pytest.skip("montecarlo_ts assumes no hidden state data")

        else:
            emsg = error.__class__.__name__ + ':  ' + str(error)
            msg = "\nAI config conflict:\n" + emsg
            pytest.fail(msg)

    start = time.monotonic()
    for mnbr in range(NBR_MOVES):

        if game.turn:
            moves = game.get_moves()
            assert moves, "Game didn't end right."
            move = random.choice(moves)
        else:
            move = player.pick_move()

        cond = game.move(move)
        if cond and cond.is_ended():
            return

        if game.info.mustpass:
            game.test_pass()

        now = time.monotonic()
        duration = now - start
        if duration > TESTLIMIT:
            msg = f"Time limit exeeded {duration:6.3} seconds at move {mnbr}."
            pytest.fail(msg)
