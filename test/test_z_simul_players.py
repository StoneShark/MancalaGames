# -*- coding: utf-8 -*-
"""Test each AI Player against each game.

This test will only be run when --run_slow is provided
as a command line option.


First, test the AI Player as configured.
Second, swap in each of the AI algorithms. If there's an error
generating the player don't run the test --
assume that the game is not suitable for the configuration.

AI player is played as False, which is different than UI play.

All games are limited to 50 moves;
that'll be about 25 for the ai player.
If the game is played in rounds, only one round is played.
Goal is to give the AI Players a solid amount of exerice
but not delay the tests too much.

Created on Sun Jul 23 11:29:10 2023
@author: Ann"""

import os
import random

import pytest

from context import ai_player
from context import cfg_keys as ckey
from context import game_interface as gi
from context import game_log
from context import man_config

from game_interface import WinCond


PATH = './GameProps/'
FILES = os.listdir(PATH)

BAD_CFG = 'all_params.txt'
if BAD_CFG in FILES:
    FILES.remove(BAD_CFG)


CONFIGED = 'configed'

ALGOS = [CONFIGED] + list(ai_player.ALGORITHM_DICT.keys())


@pytest.fixture(params=FILES)
def game_data(request):
    return man_config.make_game(PATH + request.param)

@pytest.mark.slow
@pytest.mark.parametrize('algo', ALGOS)
def test_one_game(game_data, algo):
    """Play a shortend game to exercise the Ai players."""

    game_log.game_log.active = False
    game, pdict = game_data

    if algo != CONFIGED:
        pdict[ckey.ALGORITHM] = algo

    # build the AiPlayer checking the rules, catch failures
    try:
        player = ai_player.AiPlayer(game, pdict)
    except gi.GameInfoError as error:
        emsg = error.__class__.__name__ + ':  ' + str(error)
        msg = "AI config conflict:\n" + emsg

        if algo == CONFIGED:
            assert False, msg
        else:
            print(msg)
            return

    for _ in range(50):

        if game.turn:
            move = player.pick_move()
        else:
            moves = game.get_moves()
            assert moves, "Game didn't end right."
            move = random.choice(moves)

        cond = game.move(move)
        if cond in (WinCond.WIN, WinCond.TIE,
                    WinCond.ROUND_WIN, WinCond.ROUND_TIE):
            return

        if game.info.mustpass:
            game.test_pass()
