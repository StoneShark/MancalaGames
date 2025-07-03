# -*- coding: utf-8 -*-
"""Test bechi

Tests blocks, multi capture with capt same direction, capt evens,
move unlocks, must pass, rounds, split sow, and sow start.
AI pass and player pass.

Created on Thu Aug 17 07:27:20 2023
@author: Ann"""


import pytest
pytestmark = pytest.mark.integtest

from context import game_info as gi
from context import man_config


class GameTestData:
    """allow passing move end cond between tests."""

    def __init__(self, game):
        self.game = game
        self.cond = None


@pytest.fixture(scope="class")
def gstate():
    """This fixture will maintain state between tests in the
    same class but will be reconstructed for each class."""

    game, _ = man_config.make_game('./GameProps/bechi.txt')
    gstate = GameTestData(game)
    return gstate


@pytest.mark.incremental
class TestBechiGame44:
    """5 rounds, both True and False wins, plus a tie.
    all rounds end when no moves. True wins game."""

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = False
        game.starter = False
        assert game.board == [6, 6, 6, 6, 6, 6, 6, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        """False unlock hole"""
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [6, 6, 1, 7, 7, 7, 7, 7]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, True, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        """True unlock hole"""
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [7, 7, 2, 8, 8, 7, 1, 8]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, True, False, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [8, 1, 2, 9, 9, 8, 2, 9]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, True, True, False, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        """True captures on own side"""
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [9, 2, 3, 10, 10, 9, 3, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, True, True, False, False, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        """No capture at 0, 10 is even but hole still locked"""
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [10, 1, 3, 10, 10, 9, 3, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, True, True, False, False, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [11, 1, 3, 10, 10, 9, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, True, True, False, False, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 2, 4, 11, 11, 10, 3, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, False, False, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        """True captures on False side"""
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 3, 0, 13, 2, 11, 4, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, False, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        """False does multi capt:
        sow & capt CCW, capt from 7, 0, 1 stopped by odd in 2"""
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 4, 13, 6, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [14, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 3, 4, 6, 2, 7, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [14, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 3, 1, 7, 3, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 3, 0, 8, 1, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [22, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 9, 1, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [22, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        """True does multi capt:
        sow & capt are CW, capt from 4, 3, 2 stopped by odd"""
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 0, 2, 1, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [22, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 2, 1, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [22, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 0, 0, 0, 0, 2, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [22, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 2, 1, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [25, 23]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [6, 6, 6, 6, 6, 0, 6, 6]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 5]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 6, 0, 1, 7]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [False, False, False, False, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 8, 8, 1, 7, 0, 2, 8]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [False, False, False, True, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [8, 8, 8, 1, 7, 0, 1, 9]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [False, False, False, True, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [1, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 9, 9, 2, 8, 0, 2, 10]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, False, False, True, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 9, 9, 2, 8, 0, 1, 11]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, False, False, True, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 9, 9, 1, 9, 0, 1, 11]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, False, False, True, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 10, 10, 3, 2, 0, 2, 12]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, False, False, True, True, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 10, 10, 1, 3, 0, 3, 12]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, False, False, True, True, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 10, 10, 1, 3, 0, 1, 13]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, False, False, True, True, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 2, 11, 2, 4, 0, 2, 15]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, False, True, True, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 2, 11, 2, 4, 0, 1, 16]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, False, True, True, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 2, 11, 1, 5, 0, 1, 16]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, False, True, True, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 3, 12, 2, 1, 0, 1, 16]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, False, True, True, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [3, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 3, 12, 2, 1, 0, 0, 17]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, False, True, True, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [5, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 0, 14, 4, 3, 0, 2, 3]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, False, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [5, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [6, 0, 0, 0, 5, 0, 4, 5]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [15, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_17(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [7, 1, 0, 0, 5, 0, 1, 6]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [15, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_18(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 6, 0, 2, 7]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [17, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 1, 2, 2, 1, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [17, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_20(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 2, 1, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [19, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_21(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [2, 1, 2, 1, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [19, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_22(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 1, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_23(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_24(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True             # manual changes
        assert game.mdata.winner is None
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, True, False, False]
        assert game.unlocked == [True, True, True, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [24, 24]
        assert cond.name == "ROUND_TIE"
        gstate.cond = cond

    def test_round_3_setup(self, gstate):
        """setup after tie, all holes in play"""
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [6, 6, 6, 6, 6, 6, 6, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]

    def test_round_3_move_1(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 1, 6, 6, 7, 7, 7, 7]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, True, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [8, 2, 7, 7, 8, 1, 7, 8]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, True, False, False, False, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [9, 2, 1, 8, 9, 2, 8, 9]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, True, True, False, False, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_4(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [10, 3, 2, 9, 0, 3, 9, 10]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, True, True, False, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_5(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [10, 3, 1, 10, 0, 3, 9, 10]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, True, True, False, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [10, 3, 1, 11, 1, 1, 9, 10]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, True, True, False, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_7(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [11, 4, 2, 2, 3, 3, 10, 11]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, True, True, True, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [11, 4, 3, 3, 1, 3, 10, 11]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, True, True, True, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 5, 4, 4, 2, 4, 12, 13]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 7, 6, 0, 3, 5, 13, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_11(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 7, 6, 0, 3, 0, 14, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [6, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 7, 7, 1, 1, 0, 14, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [6, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 7, 1, 2, 2, 1, 15, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [8, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 8, 0, 0, 0, 1, 15, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [8, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_15(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 1, 1, 1, 1, 2, 16, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [8, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_16(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 3, 3, 3, 3, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [8, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 3, 1, 4, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_18(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 3, 1, 4, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 3, 1, 1, 1, 1, 1, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_20(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 3, 1, 1, 1, 1, 1, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_21(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [16, 32]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_4_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [6, 0, 0, 6, 6, 6, 6, 6]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [4, 8]

    def test_round_4_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [7, 0, 0, 7, 1, 7, 7, 7]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, True, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [4, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_2(self, gstate):
        """multi capt starting at 3, 4 then stopped by lock in 5 containing 8 (an even)"""
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 0, 0, 0, 0, 8, 8, 8]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [False, False, False, True, True, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [8, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [9, 0, 0, 1, 1, 9, 2, 10]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [False, False, False, True, True, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [8, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 0, 0, 2, 2, 10, 0, 12]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [12, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 12, 0, 0]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [12, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_6(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 12, 0, 0]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [12, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [12, 36]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_5_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [6, 0, 0, 6, 6, 6, 6, 6]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 12]

    def test_round_5_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 0, 0, 1, 7, 7, 7, 7]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [False, False, False, True, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [8, 0, 0, 0, 0, 8, 8, 8]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [False, False, False, True, True, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 1, 9, 9, 10]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 10, 2, 12]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_5(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 10, 2, 12]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 12, 0, 0]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_7(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 12, 0, 0]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_8(self, gstate):
        """Captures proceed around blocked and locked holes.
        Game ends without seeds on the board."""
        game = gstate.game
        cond = game.move(2)
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, True, True, False, False, False, False, False]
        assert game.unlocked == [True, False, False, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 48]
        assert cond.name == "WIN"
        gstate.cond = cond


@pytest.mark.incremental
class TestBechi38:
    """Games ends with seeds on the board, but no moves.
    False wins all rounds and game. 3 holes blocked on True side."""

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = False
        game.starter = False
        assert game.board == [6, 6, 6, 6, 6, 6, 6, 6]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [6, 6, 1, 7, 7, 7, 7, 7]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, True, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [7, 7, 2, 8, 8, 7, 1, 8]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [False, False, True, False, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 7, 3, 9, 9, 8, 2, 9]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, False, False, False, True, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 8, 4, 10, 10, 9, 3, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, False, False, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 9, 5, 2, 12, 10, 4, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, False, False, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 10, 6, 3, 14, 2, 5, 2]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, False, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 10, 6, 3, 14, 2, 5, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, False, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 11, 6, 3, 14, 2, 5, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, False, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 11, 6, 1, 15, 3, 5, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, False, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [4, 13, 8, 3, 2, 4, 7, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 13, 8, 1, 3, 5, 7, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [4, 13, 9, 2, 1, 5, 7, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 13, 9, 1, 0, 5, 7, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 14, 10, 2, 1, 1, 7, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 14, 10, 2, 1, 0, 8, 4]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [4, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 15, 11, 2, 1, 0, 8, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [4, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 15, 11, 2, 1, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [14, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [1, 15, 11, 2, 1, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [14, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 15, 11, 1, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [16, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [1, 15, 11, 1, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [16, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 16, 2, 3, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [18, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [2, 16, 2, 3, 0, 1, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [18, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 16, 2, 1, 1, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [20, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [2, 16, 2, 1, 1, 0, 1, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, False, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [20, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 3, 2, 3, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [30, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 4, 1, 2, 3, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [30, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 2, 3, 0, 3]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [34, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 2, 3, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [34, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 2, 3, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [34, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 3, 1, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [34, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 3, 1, 0, 1]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [34, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, False, False, False, False]
        assert game.unlocked == [True, True, True, True, True, True, True, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [37, 11]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [6, 6, 6, 6, 0, 0, 0, 6]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [13, 5]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, False, False, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [13, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 8, 8, 2, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, False, False, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [15, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [8, 8, 8, 2, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, False, False, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [15, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [9, 9, 2, 4, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, False, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [17, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [9, 9, 2, 4, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, False, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [17, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 10, 0, 6, 0, 0, 0, 2]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, False, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [21, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 10, 0, 6, 0, 0, 0, 1]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, False, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [21, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 0, 0, 8, 0, 0, 0, 3]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [25, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 1, 0, 8, 0, 0, 0, 1]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [25, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 9, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [29, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 2, 1, 9, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [29, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 1, 9, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [29, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [1, 1, 1, 9, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [29, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 3, 2, 2, 0, 0, 0, 2]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [29, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 3, 2, 2, 0, 0, 0, 1]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [29, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_16(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [37, 11]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_3_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [6, 6, 6, 6, 0, 0, 0, 6]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [13, 5]

    def test_round_3_move_1(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 0, 7, 7, 0, 0, 0, 7]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, True, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [15, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [9, 1, 8, 8, 0, 0, 0, 2]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, True, False, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [15, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [10, 2, 2, 10, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, True, True, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [19, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_4(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [10, 2, 2, 10, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, True, True, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [19, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 4, 12, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [27, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_6(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 4, 12, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [27, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_7(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 2, 6, 3, 0, 0, 0, 3]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [27, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 3, 6, 3, 0, 0, 0, 1]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [27, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 3, 0, 0, 0, 0, 0, 2]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [37, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 3, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [37, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [41, 7]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_4_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [6, 6, 6, 6, 0, 0, 0, 6]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, False, False, False, False, False, False, False]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [17, 1]

    def test_round_4_move_1(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [False, False, False, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [17, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 8, 8, 8, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, False, False, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [19, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_3(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [2, 8, 8, 8, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, False, False, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [19, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 2, 9, 9, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, False, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [21, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_5(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [4, 2, 9, 9, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, False, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [21, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 2, 10, 10, 0, 0, 0, 1]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, False, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [21, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_7(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [1, 2, 10, 10, 0, 0, 0, 1]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, False, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [21, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_8(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 0, 0, 12, 0, 0, 0, 3]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [27, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 1, 0, 12, 0, 0, 0, 1]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, False, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [27, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 3, 2, 3, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [37, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_11(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 3, 2, 3, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [37, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_12(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 2, 3, 0, 0, 0, 1]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [37, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_13(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [1, 1, 2, 3, 0, 0, 0, 1]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [37, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [False, False, False, False, True, True, True, False]
        assert game.unlocked == [True, True, True, True, False, False, False, True]
        assert game.child == [None, None, None, None, None, None, None, None]
        assert game.store == [44, 4]
        assert cond.name == "WIN"
        gstate.cond = cond
