# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 13:38:12 2023
@author: Ann"""

import pytest

import utils

from context import game_constants as gc
from context import game_interface as gi
from context import mancala

from game_interface import WinCond
from game_interface import RoundStarter


TEST_COVERS = ['src\\new_game.py']


class TestNewGame:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                flags=gi.GameFlags(stores=True),
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def rgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on = [2],
                                flags=gi.GameFlags(rounds=True,
                                                   blocks=True,
                                                   stores=True),
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

        object.__setattr__(rgame.info.flags, 'round_starter', start_method)

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

        object.__setattr__(rgame.info.flags, 'rnd_left_fill', left_fill)
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


    def test_rounds_start_nat(self, rgame):

        rgame.unlocked = [False, True, True] * 2
        rgame.blocked = [True, False, True] * 2
        rgame.board = utils.build_board([0, 0, 0],
                                        [0, 0, 0])
        rgame.store = [11, 1]

        assert rgame.new_game(new_round_ok=True)
        assert rgame.board == [2] * 6
        assert rgame.store == [0, 0]
        assert rgame.turn in [False, True]
        assert rgame.starter == rgame.turn
        assert rgame.unlocked == [True] * 6
        assert rgame.blocked == [False] * 6
