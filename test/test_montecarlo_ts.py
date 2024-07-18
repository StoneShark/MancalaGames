# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:09:31 2023

@author: Ann
"""
# %% imports

import enum

import pytest
pytestmark = pytest.mark.unittest

from context import ai_interface
from context import ai_player
from context import cfg_keys as ckey
from context import game_logger
from context import man_config
from context import montecarlo_ts


# %%

TEST_COVERS = ['src\\montecarlo_ts.py']


# %%

game_logger.game_log.active = False


# %%

BIAS_x1000 = 100
NODES = 100
POUTS = 1

class TestMonteCarloTS:


    @pytest.mark.parametrize('board, store, enodes',
                             [
                                 # no loops, make all the nodes
                                 ([4] * 12, [0, 0], NODES + 1),

                                 # game loops, stop searching when found
                                 ([0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                  [23, 23],
                                  12),
                              ],
                             ids=['no_loop', 'loop_12'])
    def test_tree_policy_loops(self, board, store, enodes):

        game, pdict = man_config.make_game('./GameProps/Wari.txt')

        game.turn = True
        game.board = board
        game.store = store

        pdict[ckey.ALGORITHM] = 'montecarlo_ts'
        pdict[ckey.AI_PARAMS][ckey.MCTS_BIAS] = [BIAS_x1000] * 4
        pdict[ckey.AI_PARAMS][ckey.MCTS_NODES] = [NODES] * 4
        pdict[ckey.AI_PARAMS][ckey.MCTS_POUTS] = [POUTS] * 4

        player = ai_player.AiPlayer(game, pdict)
        player.difficulty = 1

        algo = player.algo

        move = player.pick_move()
        game.move(move)

        assert len(algo.game_nodes) == enodes
