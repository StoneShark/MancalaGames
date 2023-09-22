# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 20:27:56 2023

@author: Ann
"""

# %% imports

import pytest
pytestmark = pytest.mark.integtest

import utils

from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import GameFlags
from game_interface import WinCond
from game_interface import Direct


# %% constants

T = True
F = False
N = None

# %%

class TestMinimaxIF:

    @pytest.fixture
    def ccw_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                flags=GameFlags(sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def pass_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                min_move=2,
                                flags=GameFlags(mustpass=True,
                                                sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def upass_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                min_move=2,
                                udir_holes=[1],
                                flags=GameFlags(mustpass=True,
                                                udirect=True,
                                                sow_direct=Direct.SPLIT),
                                rules=mancala.Mancala.rules
                                )

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    def test_ccw_moves(self, ccw_game):

        # false turn
        moves = ccw_game.get_moves()
        assert moves == list(range(4))
        assert ccw_game.move(moves[0]) is None

        # true turn
        moves = ccw_game.get_moves()
        assert moves == list(range(4))
        assert ccw_game.move(moves[-1]) is None

        # false turn 2
        ccw_game.board = utils.build_board([0, 1, 0, 1],
                                           [0, 0, 0, 0])
        assert ccw_game.get_moves() == []

    def test_pass_moves(self, pass_game):

        assert pass_game.turn is False
        pass_game.board = utils.build_board([1, 2, 1, 1],
                                            [0, 3, 1, 2])
        assert pass_game.get_moves() == [1, 3]

        pass_game.board = utils.build_board([1, 2, 1, 1],
                                            [0, 0, 0, 0])
        assert pass_game.get_moves() == [mancala.PASS_TOKEN]

        # this would never get to the get_moves, it's not valid
        # pass_game.board = utils.build_board([0, 1, 0, 1],
        #                                     [0, 0, 0, 0])
        # assert pass_game.get_moves() == []

    def test_upass_moves(self, upass_game):

        # this would never get to the get_moves, it's not valid
        # upass_game.board = utils.build_board([0, 1, 0],
        #                                      [0, 0, 0])
        # assert upass_game.get_moves() == []

        upass_game.board = utils.build_board([2, 1, 0],
                                             [2, 3, 1])
        assert upass_game.get_moves() == [
            (0, None), (1, Direct.CCW), (1, Direct.CW)]

        upass_game.board = utils.build_board([2, 1, 0],
                                             [0, 1, 1])
        assert upass_game.get_moves() == [(mancala.PASS_TOKEN, None)]

    def test_maxer(self, ccw_game):

        assert ccw_game.turn == False
        assert ccw_game.is_max_player() == True

        ccw_game.turn = True
        assert ccw_game.is_max_player() == False

    def test_score_endgame(self, ccw_game):

        assert ccw_game.turn == False
        assert ccw_game.score(WinCond.WIN) == 1000
        assert ccw_game.score(WinCond.TIE) == 5
        assert ccw_game.score(WinCond.ENDLESS) == 0

        ccw_game.turn = True
        assert ccw_game.score(WinCond.WIN) == -1000
        assert ccw_game.score(WinCond.TIE) == -5
        assert ccw_game.score(WinCond.ENDLESS) == 0


class TestScorer:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                scorer=gi.Scorer(easy_rand=0),
                                capt_on=[2],
                                flags=GameFlags(sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_sc_end_store(self, game):

        object.__setattr__(game.info.scorer, 'stores_m', 0)
        object.__setattr__(game.info.scorer, 'repeat_turn', 10)

        assert game.score(None) == 0
        game.turn = False
        assert game.score(WinCond.END_STORE) == 10
        game.turn = True
        assert game.score(WinCond.END_STORE) == -10


    def test_sc_evens(self, game):

        object.__setattr__(game.info.scorer, 'evens_m', 2)
        object.__setattr__(game.info.scorer, 'stores_m', 0)

        assert game.info.scorer.evens_m == 2
        assert sum(vars(game.info.scorer).values()) == 2

        game.board = utils.build_board([2, 4, 0, 1],
                                       [0, 5, 4, 1])
        assert game.score(None) == (1 - 2) * 2


    def test_sc_seeds(self, game):

        object.__setattr__(game.info.scorer, 'seeds_m', 3)
        object.__setattr__(game.info.scorer, 'stores_m', 0)

        assert game.info.scorer.seeds_m == 3
        assert sum(vars(game.info.scorer).values()) == 3

        game.board = utils.build_board([2, 4, 0, 1],
                                       [0, 5, 4, 1])
        assert game.score(None) == (10 - 7) * 3


    def test_sc_empties(self, game):

        object.__setattr__(game.info.scorer, 'empties_m', 2)
        object.__setattr__(game.info.scorer, 'stores_m', 0)

        assert game.info.scorer.empties_m == 2
        assert sum(vars(game.info.scorer).values()) == 2

        game.board = utils.build_board([2, 4, 0, 0],
                                       [0, 5, 4, 1])
        assert game.score(None) == (1 - 2) * 2



    def test_sc_stores(self, game):
        assert game.info.scorer.stores_m == 4
        assert sum(vars(game.info.scorer).values()) == 4

        game.store = [5, 3]
        assert game.score(None) == (5 - 3) * 4


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
    def test_sc_stores_child(self, game, board, store, child, escore):

        object.__setattr__(game.info.flags, 'child', True)

        assert game.info.scorer.stores_m == 4
        assert sum(vars(game.info.scorer).values()) == 4

        game.board = board
        game.store = store
        game.child = child
        assert game.score(None) == escore


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
    def test_sc_child_cnt(self, game, child, escore):

        object.__setattr__(game.info.scorer, 'stores_m', 0)
        object.__setattr__(game.info.flags, 'child', True)
        object.__setattr__(game.info.scorer, 'child_cnt_m', 15)

        game.child = child
        assert game.score(None) == escore


    def test_sc_easy(self, game):

        object.__setattr__(game.info.scorer, 'stores_m', 0)
        object.__setattr__(game.info.scorer, 'easy_rand', 26)

        game.set_difficulty(1)
        assert all(game.score(None) for _ in range(10)) == 0

        game.set_difficulty(0)
        assert any(game.score(None) for _ in range(10)) != 0


    def test_sc_access(self, game):

        object.__setattr__(game.info.scorer, 'stores_m', 0)
        object.__setattr__(game.info.scorer, 'access_m', 10)

        game.set_difficulty(1)
        assert all(game.score(None) for _ in range(10)) == 0

        game.set_difficulty(2)
        game.board = [1, 1, 1, 0, 4, 4, 4, 4]
        assert game.score(None) == -40

        game.board = [4, 4, 4, 4, 1, 1, 1, 0]
        assert game.score(None) == 40

        game.board = [1, 1, 1, 0, 1, 1, 4, 3]
        assert game.score(None) == -10

        object.__setattr__(game.info.flags, 'mlaps', True)
        assert game.score(None) == 0


class TestMove:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                scorer=gi.Scorer(easy_rand=0),
                                capt_on=[2],
                                flags=GameFlags(sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_move_ifs(self, game, mocker):

        pick_move = mocker.spy(game.player, 'pick_move')
        move_desc = mocker.spy(game.player, 'get_move_desc')

        game.get_ai_move()
        assert pick_move.call_count == 1
        assert move_desc.call_count == 0
        mocker.resetall()

        game.get_ai_move_desc()
        assert pick_move.call_count == 0
        assert move_desc.call_count == 1
