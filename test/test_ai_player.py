# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:30:04 2023

@author: Ann
"""


import pytest
pytestmark = pytest.mark.unittest

import utils

from context import ai_player
# from context import cfg_keys as ckey
from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import WinCond


TEST_COVERS = ['src\\ai_player.py']

# %% constants

T = True
F = False
N = None


# %% ai interface and scorers

# TODO test setup & rules

class TestScorer:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def player(self, game):
        return ai_player.AiPlayer(game, {})


    def test_score_endgame(self, game, player):

        assert player.difficulty == 1
        assert game.turn == False
        assert player.is_max_player()

        assert player.score(WinCond.WIN) == 1000
        assert player.score(WinCond.TIE) == 5
        assert player.score(WinCond.ENDLESS) == 0

        game.turn = True
        assert player.score(WinCond.WIN) == -1000
        assert player.score(WinCond.TIE) == -5
        assert player.score(WinCond.ENDLESS) == 0


    def test_sc_end_store(self, game, player):

        player.sc_params.stores_m = 0
        player.sc_params.repeat_turn = 10
        player.collect_scorers()

        assert player.score(None) == 0
        game.turn = False
        assert player.score(WinCond.END_STORE) == 10
        game.turn = True
        assert player.score(WinCond.END_STORE) == -10


    def test_sc_evens(self, game, player):

        player.sc_params.evens_m = 2
        player.sc_params.stores_m = 0
        player.sc_params.easy_rand = 0
        player.collect_scorers()

        assert player.sc_params.evens_m == 2
        assert sum(vars(player.sc_params).values()) == 2

        game.board = utils.build_board([2, 4, 0, 1],
                                       [0, 5, 4, 1])
        assert player.score(None) == (1 - 2) * 2


    def test_sc_seeds(self, game, player):

        player.sc_params.seeds_m = 3
        player.sc_params.stores_m = 0
        player.sc_params.easy_rand = 0
        player.collect_scorers()

        assert player.sc_params.seeds_m == 3
        assert sum(vars(player.sc_params).values()) == 3

        game.board = utils.build_board([2, 4, 0, 1],
                                       [0, 5, 4, 1])
        assert player.score(None) == (10 - 7) * 3


    def test_sc_empties(self, game, player):

        player.sc_params.empties_m =  2
        player.sc_params.stores_m = 0
        player.sc_params.easy_rand = 0
        player.collect_scorers()

        assert player.sc_params.empties_m == 2
        assert sum(vars(player.sc_params).values()) == 2

        game.board = utils.build_board([2, 4, 0, 0],
                                       [0, 5, 4, 1])
        assert player.score(None) == (1 - 2) * 2



    def test_sc_stores(self, game, player):

        player.sc_params.easy_rand = 0
        player.collect_scorers()

        assert player.sc_params.stores_m == 4
        assert sum(vars(player.sc_params).values()) == 4

        game.store = [5, 3]
        assert player.score(None) == (5 - 3) * 4


    @pytest.mark.parametrize(
        'board, store, child, escore',
        [(utils.build_board([0, 0, 0, 0],
                            [0, 0, 0, 0]), [5, 3],
          utils.build_board([N, N, N, N],
                            [N, N, N, N]), (5 - 3) * 4),

         (utils.build_board([1, 2, 3, 4],
                            [1, 2, 3, 4]), [5, 3],
          utils.build_board([N, F, N, N],
                            [N, N, T, N]), ((5+2) - (3+3)) * 4),

         (utils.build_board([1, 2, 3, 4],
                            [1, 2, 3, 4]), [5, 3],
          utils.build_board([N, F, T, N],
                            [N, N, T, F]), ((5+2+4) - (3+3+3)) * 4),
         ])
    def test_sc_stores_child(self, game, player, board, store, child, escore):

        object.__setattr__(game.info, 'child', True)

        player.sc_params.easy_rand = 0
        player.collect_scorers()

        assert player.sc_params.stores_m == 4
        assert sum(vars(player.sc_params).values()) == 4

        game.board = board
        game.store = store
        game.child = child
        assert player.score(None) == escore


    @pytest.mark.parametrize(
        'child, escore',
        [(utils.build_board([N, N, N, N],
                            [N, N, N, N]), 0),

         (utils.build_board([N, F, N, N],
                            [N, N, N, N]), 15),

         (utils.build_board([N, T, N, N],
                            [N, N, N, N]), -15),

         (utils.build_board([N, T, F, F],
                            [N, F, N, N]), (3-1) * 15),

         (utils.build_board([N, F, T, T],
                            [N, T, N, N]), (1-3) * 15),

         ])
    def test_sc_child_cnt(self, game, player, child, escore):

        object.__setattr__(game.info, 'child', True)

        player.sc_params.stores_m = 0
        player.sc_params.child_cnt_m = 15
        player.collect_scorers()

        game.child = child
        assert player.score(None) == escore


    def test_sc_easy(self, game, player):

        player.sc_params.stores_m = 0
        player.sc_params.easy_rand = 26
        player.collect_scorers()

        player.difficulty = 1
        assert all(player.score(None) == 0 for _ in range(10))

        player.difficulty = 0
        assert any(player.score(None) > 0 for _ in range(10))


    def test_sc_access(self, game, player):

        player.sc_params.stores_m = 0
        player.sc_params.access_m = 10
        player.collect_scorers()

        player.difficulty = 1
        assert player.score(None) == 0

        player.difficulty = 2
        game.board = [1, 1, 1, 0, 4, 4, 4, 4]
        assert player.score(None) == -40

        game.board = [4, 4, 4, 4, 1, 1, 1, 0]
        assert player.score(None) == 40

        game.board = [1, 1, 1, 0, 1, 1, 4, 3]
        assert player.score(None) == -10
