# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 20:27:56 2023

@author: Ann
"""

# %% imports

import sys

import pytest

sys.path.extend(['src'])

import game_constants as gc
import game_interface as gi
from game_interface import GameFlags
from game_interface import WinCond
from game_interface import Direct
import mancala
import utils


# %%

class TestMinimaxIF:

    @pytest.fixture
    def ccw_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(name='my name',
                                help_file='None',
                                nbr_holes=game_consts.holes,
                                about='about text',
                                difficulty=0,
                                capt_on=[2],
                                flags=GameFlags(sow_direct=Direct.CCW))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def pass_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(name='my name',
                                help_file='None',
                                nbr_holes=game_consts.holes,
                                about='about text',
                                difficulty=0,
                                capt_on=[2],
                                min_move=2,
                                flags=GameFlags(mustpass=True,
                                                sow_direct=Direct.CCW))

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
                                                sow_direct=Direct.SPLIT)
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

        game_info = gi.GameInfo(name='my name',
                                help_file='None',
                                nbr_holes=game_consts.holes,
                                about='about text',
                                difficulty=0,
                                scorer=gi.Scorer(easy_rand=0),
                                capt_on=[2],
                                flags=GameFlags(sow_direct=Direct.CCW))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

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

    @pytest.mark.skip(reason='easy_rand and access are not tested')
    def test_scorer(self):
        pass
