# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 12:29:13 2024
@author: Ann"""


import pytest
pytestmark = pytest.mark.integtest

from context import man_config


T = True
F = False
N = None



class GameTestData:
    """allow passing move end cond between tests."""

    def __init__(self, game):
        self.game = game
        self.cond = None


@pytest.fixture(scope="class")
def gstate():
    """This fixture will maintain state between tests in the
    same class but will be reconstructed for each class."""

    game, _ = man_config.make_game('./GameProps/pandi.txt')
    gstate = GameTestData(game)
    return gstate


@pytest.mark.incremental
class TestPandi:
    """True wins 2 rounds, one TIE, False wins the game.
    4 rounds."""

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = True
        game.starter = True
        assert game.board == [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        """True mlap sow ends 13, 0 is empty,
        capture from 1, pick cross at 12"""

        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 7, 7, 7, 7, 0, 1, 7, 2, 8, 0, 8]
        assert game.store == [0, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        """pick while sowing True: 10, 8
        mlap sow ends at 0, capture 2 and pick cross at 11"""
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 0, 0, 0, 10, 0, 1, 3, 0, 10, 1, 0, 3, 11]
        assert game.store == [5, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        """Pick while sowing 0 by False and 12 & 7 by True"""
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 11, 1, 0, 0, 0, 0, 2, 1, 0, 12]
        assert game.store == [9, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 0, 2, 1, 1, 1, 1, 0, 2, 1, 13]
        assert game.store == [14, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 3, 1, 1, 1, 3, 2, 2, 2, 2, 1, 3, 2, 0]
        assert game.store == [14, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 2, 2, 2, 0, 0, 0, 3, 0, 2, 0, 0, 1]
        assert game.store == [20, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 0, 0, 2, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0]
        assert game.store == [20, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [24, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [24, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [25, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [25, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [25, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [25, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [26, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [28, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 42]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        """Holes filled from left, right side holes empty.
        Round start is False (prev was True)."""
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.store == [3, 7]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 6, 6, 0, 0, 0, 0, 6, 6, 0, 6, 0, 6, 6]
        assert game.store == [15, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 8, 8, 0, 2, 0, 0, 2, 9, 0, 0, 0, 8, 0]
        assert game.store == [15, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 9, 0, 1, 3, 0, 0, 3, 10, 1, 1, 1, 9, 0]
        assert game.store == [15, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 10, 0, 2, 0, 0, 0, 0, 11, 2, 0, 0, 0, 1]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 11, 1, 1, 0, 0, 0, 2, 0, 0, 1, 1, 1, 2]
        assert game.store == [24, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 12, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 3]
        assert game.store == [24, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 12, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 3]
        assert game.store == [24, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 12, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0]
        assert game.store == [24, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 2]
        assert game.store == [29, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3]
        assert game.store == [29, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3]
        assert game.store == [29, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [29, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0]
        assert game.store == [29, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_14(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [29, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_15(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [30, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 40]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_3_setup(self, gstate):
        """Round start is True (prev was False)."""
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.store == [0, 5]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]

    def test_round_3_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [7, 0, 1, 0, 7, 7, 0, 7, 7, 0, 0, 7, 7, 7]
        assert game.store == [0, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_2(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 3, 0, 0, 10, 0, 0, 0, 0, 1, 3, 1, 10, 10]
        assert game.store == [17, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 0, 1, 1, 11, 1, 0, 1, 1, 1, 1, 0, 0, 0]
        assert game.store == [21, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 2, 2, 0]
        assert game.store == [32, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 3, 3, 0]
        assert game.store == [32, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 3, 3, 0]
        assert game.store == [32, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [32, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [32, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [32, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [33, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_11(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [33, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [33, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_13(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [33, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [33, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [33, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [35, 35]
        assert cond.name == "ROUND_TIE"
        gstate.cond = cond

    def test_round_4_setup(self, gstate):
        """Previous round was tie, all holes and seeds and in play.
        No blocks.
        Round starter is False (prev was True)."""
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]

    def test_round_4_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [7, 7, 0, 0, 7, 2, 8, 8, 8, 0, 0, 1, 7, 7]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 2, 2, 12, 3, 12, 0, 0, 0, 0, 1]
        assert game.store == [16, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 1, 2, 0, 1, 14, 0, 0, 1, 1, 1, 1, 2]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_4(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 3, 0, 0, 14, 0, 0, 1, 0, 2, 0, 3]
        assert game.store == [20, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_5(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 14, 0, 0, 1, 0, 2, 0, 3]
        assert game.store == [24, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_6(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 14, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [24, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 14, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [24, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 14, 0, 0, 0, 0, 1, 0, 1]
        assert game.store == [24, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1]
        assert game.store == [38, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [38, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_11(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [38, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [38, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_13(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [39, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_14(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [39, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [39, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [39, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_17(self, gstate):
        """Check the unused fields unlocked, child & owner."""
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [40, 30]
        assert cond.name == "WIN"
        gstate.cond = cond
