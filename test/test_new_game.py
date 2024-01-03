# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 13:38:12 2023
@author: Ann"""

import pytest
pytestmark = pytest.mark.unittest

import utils

from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import Goal
from game_interface import RoundFill
from game_interface import RoundStarter
from game_interface import WinCond


TEST_COVERS = ['src\\new_game.py']

T = True
F = False
N = None

class TestNewGame:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                stores=True,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def rgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                rounds=True,
                                blocks=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        game.starter = False
        return game

    @pytest.fixture
    def nb_rgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                rounds=True,
                                stores=True,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        game.starter = False
        return game


    def test_no_rounds_start(self, game):

        game.unlocked = [False, True, True] * 2
        game.blocked = [True, False, True] * 2
        game.board = utils.build_board([1, 0, 0],
                                       [0, 0, 1])
        game.store = [7, 3]

        assert game.new_game()
        assert game.board == [2] * 6
        assert game.store == [0, 0]
        assert game.turn in [False, True]   # random
        assert game.starter == game.turn
        assert game.unlocked == [True] * 6
        assert game.blocked == [False] * 6


    def test_rounds_start_force(self, rgame):

        rgame.unlocked = [False, True, True] * 2
        rgame.blocked = [True, False, True] * 2
        rgame.board = utils.build_board([0, 0, 0],
                                        [0, 0, 0])
        rgame.store = [8, 4]

        assert rgame.new_game()
        assert rgame.board == [2] * 6
        assert rgame.store == [0, 0]
        assert rgame.turn in [False, True]   # random
        assert rgame.starter == rgame.turn
        assert rgame.unlocked == [True] * 6
        assert rgame.blocked == [False] * 6


    @pytest.mark.parametrize(
        'start_method, starter, winner, estarter',
        [(RoundStarter.ALTERNATE, True, False, False),
         (RoundStarter.ALTERNATE, True, True, False),
         (RoundStarter.ALTERNATE, False, False, True),
         (RoundStarter.ALTERNATE, False, True, True),
         (RoundStarter.LOSER, True, False, True),
         (RoundStarter.LOSER, False, True, False),
         (RoundStarter.WINNER, True, False, False),
         (RoundStarter.WINNER, True, True, True),
          ])
    def test_rounds_start(self, rgame,
                          start_method, starter, winner, estarter):

        object.__setattr__(rgame.info, 'round_starter', start_method)

        rgame.unlocked = [False, True, True] * 2
        rgame.blocked = [True, False, True] * 2
        rgame.board = utils.build_board([0, 0, 0],
                                        [0, 0, 0])
        rgame.starter  = starter
        if winner:
            rgame.store = [4, 8]
        else:
            rgame.store = [8, 4]
        rgame.turn = winner

        assert not rgame.new_game(win_cond=WinCond.ROUND_WIN,
                                  new_round_ok=True)

        assert rgame.turn == estarter
        assert rgame.starter == rgame.turn
        assert rgame.unlocked == [True] * rgame.cts.dbl_holes
        if winner:
            assert rgame.board == utils.build_board([2, 2, 2],
                                                    [2, 0, 2])
            assert rgame.store == [0, 2]
            assert rgame.blocked == utils.build_board([False, False, False],
                                                      [False, True, False])
        else:
            assert rgame.board == utils.build_board([2, 0, 2],
                                                    [2, 2, 2])
            assert rgame.store == [2, 0]
            assert rgame.blocked == utils.build_board([False, True, False],
                                                      [False, False, False])


    @pytest.mark.parametrize(
        'store, left_fill, blocks, estore',
        [([4, 8], False, utils.build_board([False, False, False],
                                           [False, True, False]), [0, 2]),
         ([8, 4], False, utils.build_board([False, True, False],
                                           [False, False, False]), [2, 0]),
         ([2, 10], False, utils.build_board([False, False, False],
                                            [False, True, True]), [0, 4]),
         ([10, 2], False, utils.build_board([False, True, True],
                                            [False, False, False]), [4, 0]),

         ([4, 8], True, utils.build_board([False, False, False],
                                          [False, False, True]), [0, 2]),
         ([8, 4], True, utils.build_board([True, False, False],
                                          [False, False, False]), [2, 0]),
         ([2, 10], True, utils.build_board([False, False, False],
                                           [False, True, True]), [0, 4]),
         ([10, 2], True, utils.build_board([True, True, False],
                                           [False, False, False]), [4, 0]),
          ])
    def test_fill_patterns(self, rgame, store, left_fill, blocks, estore):

        object.__setattr__(rgame.info, 'round_fill',
                           RoundFill.LEFT_FILL if left_fill else RoundFill.OUTSIDE_FILL)

        rgame.deco = mancala.ManDeco(rgame)

        rgame.unlocked = [False, True, True] * 2
        rgame.blocked = [True, False, True] * 2
        rgame.board = utils.build_board([0, 0, 0],
                                        [0, 0, 0])
        rgame.store = store

        assert not rgame.new_game(win_cond=WinCond.ROUND_WIN,
                                  new_round_ok=True)

        assert rgame.unlocked == [True] * rgame.cts.dbl_holes
        assert rgame.blocked == blocks
        assert all(rgame.blocked[loc] or
                   rgame.board[loc] == 2 for loc in range(rgame.cts.dbl_holes))
        assert rgame.store == estore


    @pytest.mark.parametrize('left_fill', [True, False])
    @pytest.mark.parametrize(
        'store, estore',
        [([4, 8], [0, 2]),
         ([8, 4], [2, 0]),
         ([2, 10], [0, 4]),
         ([10, 2], [4, 0]),
       ])
    def test_no_blocks(self, nb_rgame, left_fill, store, estore):

        object.__setattr__(nb_rgame.info, 'round_fill',
                           RoundFill.LEFT_FILL if left_fill
                           else RoundFill.OUTSIDE_FILL)
        nb_rgame.deco = mancala.ManDeco(nb_rgame)

        nb_rgame.blocked = [True, False, True] * 2
        nb_rgame.board = utils.build_board([0, 0, 0],
                                           [0, 0, 0])
        nb_rgame.store = store.copy()

        assert not nb_rgame.new_game(win_cond=WinCond.ROUND_WIN,
                                     new_round_ok=True)

        assert not any(nb_rgame.blocked)
        assert all(nb_rgame.board[loc] in [0, 2]
                   for loc in range(nb_rgame.cts.dbl_holes))
        assert nb_rgame.store == estore


def test_patterns():
    """test_patterns does most of the testing,
    here create which uses new_game."""

    game_consts = gc.GameConsts(nbr_start=4, holes=4)
    game_info = gi.GameInfo(start_pattern=2,
                            capt_on=[2],
                            nbr_holes=game_consts.holes,
                            rules=mancala.Mancala.rules)

    game = mancala.Mancala(game_consts, game_info)
    game.turn = False

    assert game.board == [0, 4] * 4


class TestTerritory:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=3)
        game_info = gi.GameInfo(capt_on = [2],
                                stores=True,
                                gparam_one=5,
                                goal=Goal.TERRITORY,
                                rounds=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    @pytest.mark.parametrize('fseeds, win, eowners',
                             [(15, T, [F, F, F, T, T, T]),
                              (14, T, [F, F, F, T, T, T]),
                              (13, F, [F, F, F, F, T, T]),
                              (12, F, [F, F, F, F, T, T]),
                              (11, F, [F, F, F, F, T, T]),
                              (10, F, [F, F, F, T, T, T]),
                              ( 6, F, [T, F, F, T, T, T]),
                              ( 5, F, [T, F, F, T, T, T]),
                              ( 4, F, [T, T, F, T, T, T]),
                              ( 4, T, [F, F, F, T, T, T]),
                              ( 3, T, [F, F, F, T, T, T]),

                              ])
    def test_territory(self, game, fseeds, win, eowners):

        game.board = [0] * game.cts.dbl_holes
        game.store = [fseeds, game.cts.total_seeds - fseeds]
        print(game)

        cond = WinCond.WIN if win else WinCond.ROUND_WIN
        game.new_game(cond, new_round_ok=True)
        print(game)
        assert game.owner == eowners
