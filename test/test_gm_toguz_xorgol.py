# -*- coding: utf-8 -*-
"""Integration testing of Toguz Xorgol.
Tuzdek!

Two tests.
Neither tests prevention of left-most hole tuzdek.

Created on Wed Oct  9 09:24:54 2024
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

    game, _ = man_config.make_game('./GameProps/Toguz_Xorgol.txt')
    gstate = GameTestData(game)
    return gstate


@pytest.mark.incremental
class TestTuzdekGame27:

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = True
        game.starter = True
        assert game.board == [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        """Opening move capture by True in 7"""
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [9, 9, 9, 9, 9, 9, 9, 0, 10, 10, 10, 10, 10, 10, 10, 1, 9, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [10, 10, 10, 10, 10, 10, 1, 0, 10, 10, 10, 10, 10, 10, 10, 1, 0, 10]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [10, 11, 11, 11, 11, 11, 2, 1, 11, 11, 1, 10, 10, 10, 10, 1, 0, 10]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [11, 12, 1, 11, 11, 11, 2, 1, 11, 11, 2, 11, 11, 11, 11, 2, 1, 11]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [11, 13, 2, 12, 12, 12, 3, 2, 12, 12, 3, 1, 11, 11, 11, 2, 1, 11]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        """False capture 4 seeds (minimum even for capture)."""
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [12, 14, 3, 1, 12, 12, 3, 2, 12, 12, 0, 2, 12, 12, 12, 3, 2, 12]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        """True sow ended with 3 at 16, but wrong side: no tuzdek"""
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [13, 15, 4, 2, 13, 13, 4, 3, 13, 1, 0, 2, 12, 12, 12, 3, 3, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [13, 15, 4, 3, 14, 14, 1, 3, 13, 1, 0, 2, 12, 12, 12, 3, 3, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [13, 15, 4, 3, 14, 14, 1, 3, 13, 1, 0, 2, 12, 12, 13, 4, 1, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [13, 16, 5, 1, 14, 14, 1, 3, 13, 1, 0, 2, 12, 12, 13, 4, 1, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [13, 17, 6, 2, 15, 15, 2, 4, 14, 2, 1, 3, 1, 12, 13, 4, 1, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [14, 18, 7, 3, 16, 16, 3, 5, 1, 2, 1, 3, 1, 13, 14, 5, 2, 14]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [14, 19, 8, 4, 17, 17, 4, 6, 2, 3, 2, 4, 2, 1, 14, 5, 2, 14]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [14, 19, 9, 5, 18, 18, 5, 1, 2, 3, 2, 4, 2, 1, 14, 5, 2, 14]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        """a 20 seed capture!!"""
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [14, 0, 10, 6, 19, 19, 6, 2, 3, 4, 3, 5, 3, 2, 1, 5, 2, 14]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        """False makes tuzdek in 16"""
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [15, 1, 11, 1, 19, 19, 6, 2, 3, 4, 3, 5, 3, 2, 1, 5, 3, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [15, 1, 11, 1, 19, 19, 6, 2, 3, 4, 3, 5, 4, 1, 1, 5, 3, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [15, 1, 11, 1, 19, 19, 7, 1, 3, 4, 3, 5, 4, 1, 1, 5, 3, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [15, 1, 11, 1, 19, 19, 7, 2, 4, 5, 4, 1, 4, 1, 1, 5, 3, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [15, 1, 11, 1, 19, 20, 8, 3, 1, 5, 4, 1, 4, 1, 1, 5, 3, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        """True moved one seed from hole 3 to 4 (index 14 to 13)"""
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [15, 1, 11, 1, 19, 20, 8, 3, 1, 5, 4, 1, 4, 2, 0, 5, 3, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        """False moved one seed from hole 1 to 0"""
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [16, 0, 11, 1, 19, 20, 8, 3, 1, 5, 4, 1, 4, 2, 0, 5, 3, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [16, 0, 11, 1, 19, 20, 8, 3, 1, 5, 4, 2, 5, 3, 1, 1, 3, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [16, 0, 11, 1, 19, 20, 8, 4, 0, 5, 4, 2, 5, 3, 1, 1, 3, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [16, 0, 11, 1, 19, 21, 9, 5, 1, 1, 4, 2, 5, 3, 1, 1, 3, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [16, 0, 12, 0, 19, 21, 9, 5, 1, 1, 4, 2, 5, 3, 1, 1, 3, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [16, 0, 12, 0, 19, 21, 9, 5, 1, 1, 4, 2, 5, 4, 0, 1, 3, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [17, 1, 13, 1, 2, 22, 10, 6, 2, 2, 5, 3, 6, 5, 1, 2, 4, 16]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [17, 1, 13, 1, 2, 22, 10, 6, 2, 2, 5, 3, 6, 6, 0, 2, 4, 16]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [17, 1, 14, 2, 3, 23, 11, 1, 2, 2, 5, 3, 6, 6, 0, 2, 4, 16]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [17, 1, 14, 2, 3, 23, 11, 2, 3, 3, 6, 4, 1, 6, 0, 2, 4, 16]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [17, 1, 14, 2, 3, 23, 12, 1, 3, 3, 6, 4, 1, 6, 0, 2, 4, 16]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [17, 1, 14, 2, 3, 23, 12, 1, 3, 3, 6, 4, 1, 6, 1, 1, 4, 16]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [18, 3, 16, 4, 5, 2, 13, 2, 4, 4, 7, 5, 2, 7, 2, 2, 5, 17]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [18, 3, 16, 4, 0, 3, 14, 3, 5, 5, 1, 5, 2, 7, 2, 2, 5, 17]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [18, 3, 16, 4, 0, 4, 15, 1, 5, 5, 1, 5, 2, 7, 2, 2, 5, 17]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_37(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [18, 3, 16, 4, 0, 4, 15, 1, 5, 6, 0, 5, 2, 7, 2, 2, 5, 17]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_38(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [19, 4, 1, 4, 0, 5, 16, 2, 6, 7, 1, 6, 3, 8, 3, 3, 6, 18]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_39(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [19, 4, 1, 4, 0, 5, 16, 2, 6, 7, 1, 6, 4, 9, 1, 3, 6, 18]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_40(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [19, 4, 1, 4, 0, 5, 17, 1, 6, 7, 1, 6, 4, 9, 1, 3, 6, 18]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_41(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [19, 4, 1, 4, 0, 5, 17, 1, 6, 8, 2, 7, 1, 9, 1, 3, 6, 18]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_42(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [19, 4, 1, 4, 0, 5, 18, 0, 6, 8, 2, 7, 1, 9, 1, 3, 6, 18]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_43(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 5, 2, 5, 1, 6, 19, 1, 7, 9, 3, 8, 2, 10, 2, 4, 7, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_44(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [0, 5, 2, 5, 1, 6, 20, 0, 7, 9, 3, 8, 2, 10, 2, 4, 7, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_45(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 5, 2, 5, 1, 6, 20, 0, 0, 10, 1, 8, 2, 10, 2, 4, 7, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_46(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 6, 3, 6, 2, 1, 20, 0, 0, 10, 1, 8, 2, 10, 2, 4, 7, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_47(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [1, 6, 3, 6, 2, 1, 20, 0, 0, 11, 0, 8, 2, 10, 2, 4, 7, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_48(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 6, 3, 6, 2, 1, 20, 0, 0, 11, 0, 8, 2, 10, 2, 4, 7, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_49(self, gstate):
        """True makes a tuzdek, not opp Falses."""
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 6, 3, 6, 3, 2, 21, 1, 1, 12, 1, 9, 3, 1, 2, 4, 7, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_50(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [0, 6, 3, 6, 3, 2, 22, 0, 1, 12, 1, 9, 3, 1, 2, 4, 7, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_51(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [1, 7, 4, 7, 4, 3, 23, 1, 2, 1, 1, 9, 3, 1, 2, 4, 8, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_52(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [1, 7, 4, 7, 4, 3, 24, 0, 2, 1, 1, 9, 3, 1, 2, 4, 8, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_53(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 7, 4, 7, 4, 3, 24, 0, 2, 1, 1, 9, 4, 2, 3, 1, 8, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_54(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 1, 4, 7, 4, 3, 24, 0, 2, 1, 1, 9, 4, 3, 4, 2, 9, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_55(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 1, 4, 7, 4, 3, 24, 0, 2, 1, 1, 10, 5, 4, 1, 2, 9, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_56(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 1, 4, 7, 4, 3, 24, 0, 2, 1, 1, 10, 5, 4, 1, 2, 9, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_57(self, gstate):
        """True prevented from making a second tuzdek in 8"""
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 4, 7, 4, 3, 24, 0, 3, 2, 2, 11, 1, 4, 1, 2, 9, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_58(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 2, 5, 1, 4, 3, 24, 0, 3, 2, 2, 11, 1, 4, 1, 3, 10, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_59(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 2, 5, 1, 4, 3, 24, 0, 3, 2, 2, 11, 1, 5, 0, 3, 10, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_60(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 2, 5, 2, 5, 1, 24, 0, 3, 2, 2, 11, 1, 5, 0, 3, 10, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_61(self, gstate):
        """True sowed to 3 on False side, opp False's tuzdek but True already
        has a tuzdek."""
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [2, 3, 6, 3, 6, 2, 25, 1, 4, 3, 3, 1, 1, 5, 0, 3, 10, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_62(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 4, 1, 3, 6, 2, 25, 1, 4, 3, 3, 1, 1, 5, 0, 0, 11, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_63(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [3, 4, 1, 3, 6, 2, 25, 1, 4, 3, 4, 0, 1, 5, 0, 0, 11, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_64(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 4, 1, 3, 6, 2, 25, 1, 4, 3, 4, 0, 1, 5, 0, 0, 12, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_65(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 4, 1, 3, 6, 2, 25, 1, 4, 4, 5, 1, 2, 1, 0, 0, 12, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_66(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [3, 6, 3, 5, 8, 4, 2, 2, 5, 5, 6, 2, 3, 2, 1, 1, 13, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_67(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 6, 3, 5, 8, 4, 2, 2, 5, 6, 7, 3, 4, 3, 2, 2, 14, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_68(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [3, 6, 4, 6, 9, 1, 2, 2, 5, 6, 7, 3, 4, 3, 2, 2, 14, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_69(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [3, 6, 4, 6, 9, 1, 2, 2, 5, 7, 8, 1, 4, 3, 2, 2, 14, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_70(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [3, 6, 4, 6, 9, 1, 3, 1, 5, 7, 8, 1, 4, 3, 2, 2, 14, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_71(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 6, 4, 6, 9, 1, 3, 1, 5, 7, 8, 2, 5, 1, 2, 2, 14, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_72(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 6, 4, 6, 9, 1, 3, 1, 5, 7, 8, 2, 5, 1, 2, 2, 15, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_73(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 6, 4, 6, 9, 1, 3, 1, 5, 7, 9, 1, 5, 1, 2, 2, 15, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_74(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 6, 4, 6, 10, 0, 3, 1, 5, 7, 9, 1, 5, 1, 2, 2, 15, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_75(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 6, 4, 6, 10, 0, 3, 1, 0, 8, 10, 2, 1, 1, 2, 2, 15, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 70]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_76(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [1, 6, 4, 6, 11, 1, 1, 1, 0, 8, 10, 2, 1, 1, 2, 2, 15, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 70]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_77(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 6, 4, 6, 11, 1, 1, 1, 0, 8, 10, 2, 2, 0, 2, 2, 15, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 70]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_78(self, gstate):
        """Both players have moves, but True has 85 seeds (half is 81).
        Game ends, True wins."""
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 6, 4, 6, 12, 0, 1, 1, 0, 8, 10, 2, 2, 0, 2, 2, 15, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, T, N, N, N, N, N, N, N, N, N, N, N, F, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 70]
        assert cond.name == "WIN"
        gstate.cond = cond


@pytest.mark.incremental
class TestTuzdek31:
    """True never makes a tuzdek, condition almost met on turn 20,
    but it's opposite False's Tuzdek"""

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = False
        game.starter = False
        assert game.board == [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [10, 10, 10, 10, 10, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 10, 10]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [10, 10, 10, 10, 10, 1, 9, 0, 10, 10, 10, 10, 10, 10, 10, 1, 1, 10]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [10, 10, 10, 10, 11, 0, 9, 0, 10, 10, 10, 10, 10, 10, 10, 1, 1, 10]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [10, 10, 10, 11, 12, 1, 10, 1, 11, 11, 11, 11, 1, 10, 10, 1, 1, 10]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [11, 11, 11, 1, 12, 1, 10, 1, 11, 11, 11, 0, 2, 11, 11, 2, 2, 11]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [11, 11, 11, 1, 13, 2, 11, 2, 12, 12, 12, 1, 3, 12, 1, 2, 2, 11]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [12, 12, 12, 2, 14, 3, 12, 3, 1, 12, 12, 1, 3, 12, 1, 3, 3, 12]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [13, 13, 13, 3, 15, 4, 13, 4, 2, 1, 12, 1, 3, 12, 1, 3, 4, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [13, 13, 14, 4, 16, 1, 13, 4, 2, 1, 12, 1, 3, 12, 1, 3, 4, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [13, 13, 15, 5, 17, 2, 14, 5, 3, 2, 13, 2, 4, 1, 1, 3, 4, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [14, 14, 16, 6, 18, 3, 1, 5, 3, 2, 13, 3, 5, 2, 2, 4, 5, 14]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [14, 14, 16, 6, 18, 3, 1, 5, 0, 3, 14, 4, 1, 2, 2, 4, 5, 14]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [15, 15, 1, 6, 18, 4, 2, 6, 1, 4, 15, 5, 2, 3, 3, 5, 6, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [15, 15, 1, 6, 18, 4, 2, 7, 2, 5, 16, 1, 2, 3, 3, 5, 6, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [15, 16, 0, 6, 18, 4, 2, 7, 2, 5, 16, 1, 2, 3, 3, 5, 6, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [15, 16, 0, 6, 18, 4, 2, 7, 2, 5, 16, 2, 3, 4, 4, 6, 1, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [15, 16, 0, 6, 18, 4, 2, 8, 1, 5, 16, 2, 3, 4, 4, 6, 1, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [16, 17, 1, 7, 19, 5, 3, 9, 2, 6, 1, 2, 3, 5, 5, 7, 2, 16]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [16, 18, 2, 8, 20, 1, 3, 9, 2, 6, 1, 2, 3, 5, 5, 7, 2, 16]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        """True prevented from making a tuzdek opposite of False's"""
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [16, 18, 3, 9, 21, 2, 4, 10, 3, 7, 2, 3, 4, 6, 6, 8, 3, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [16, 18, 3, 9, 22, 1, 4, 10, 3, 7, 2, 3, 4, 6, 6, 8, 3, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [16, 18, 3, 9, 22, 1, 4, 10, 3, 7, 2, 3, 4, 6, 7, 9, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [17, 19, 4, 1, 22, 1, 4, 10, 3, 7, 2, 3, 4, 7, 8, 10, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [17, 19, 4, 1, 22, 1, 4, 10, 3, 8, 3, 4, 1, 7, 8, 10, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [17, 19, 4, 1, 22, 1, 5, 11, 1, 8, 3, 4, 1, 7, 8, 10, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [17, 19, 4, 1, 22, 1, 5, 11, 1, 8, 3, 4, 1, 7, 8, 10, 3, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [17, 19, 5, 2, 23, 2, 1, 11, 1, 8, 3, 4, 1, 7, 8, 10, 3, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [17, 19, 5, 2, 23, 2, 1, 11, 2, 9, 4, 1, 1, 7, 8, 10, 3, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [17, 19, 5, 2, 23, 2, 1, 12, 1, 9, 4, 1, 1, 7, 8, 10, 3, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [17, 19, 5, 2, 23, 2, 1, 13, 2, 10, 5, 2, 2, 8, 1, 10, 3, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [18, 20, 1, 2, 23, 2, 1, 13, 2, 10, 5, 2, 2, 8, 1, 10, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [18, 20, 1, 2, 23, 2, 1, 13, 2, 10, 6, 1, 2, 8, 1, 10, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [20, 22, 3, 4, 2, 3, 2, 14, 3, 11, 7, 2, 3, 9, 2, 11, 1, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [21, 23, 4, 5, 3, 4, 3, 15, 4, 1, 7, 2, 3, 9, 2, 11, 1, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [22, 24, 5, 6, 4, 5, 4, 1, 4, 1, 7, 3, 4, 10, 3, 12, 2, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [22, 24, 5, 6, 4, 5, 4, 1, 4, 1, 7, 3, 4, 10, 3, 13, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [22, 25, 6, 7, 5, 1, 4, 1, 4, 1, 7, 3, 4, 10, 3, 13, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_38(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [22, 25, 6, 7, 5, 1, 4, 1, 4, 1, 7, 3, 5, 11, 1, 13, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_39(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [23, 26, 7, 8, 1, 1, 4, 1, 4, 1, 7, 3, 5, 11, 1, 13, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_40(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [23, 26, 7, 9, 2, 2, 5, 2, 5, 2, 8, 4, 6, 1, 1, 13, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_41(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [24, 27, 1, 9, 2, 2, 5, 2, 5, 2, 8, 4, 6, 1, 2, 14, 2, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_42(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [24, 27, 1, 9, 2, 2, 5, 2, 5, 2, 8, 4, 7, 2, 3, 15, 3, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_43(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 28, 2, 10, 3, 3, 6, 3, 6, 3, 9, 5, 8, 0, 5, 17, 5, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_44(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 28, 2, 10, 3, 0, 7, 4, 7, 4, 10, 6, 1, 0, 5, 17, 5, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [30, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_45(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [3, 29, 3, 11, 4, 1, 1, 4, 7, 4, 10, 6, 1, 0, 5, 17, 5, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [30, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_46(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [3, 29, 3, 11, 4, 1, 2, 5, 8, 5, 11, 1, 1, 0, 5, 17, 5, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [30, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_47(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [3, 30, 4, 12, 5, 2, 3, 6, 1, 5, 11, 1, 1, 0, 5, 17, 5, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [30, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_48(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 30, 4, 12, 5, 2, 3, 6, 1, 5, 11, 2, 0, 0, 5, 17, 5, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [30, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_49(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 2, 5, 13, 6, 3, 4, 7, 3, 7, 13, 4, 2, 2, 7, 19, 7, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [30, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_50(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 2, 5, 13, 6, 3, 4, 7, 3, 7, 13, 5, 1, 2, 7, 19, 7, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [30, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_51(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [5, 2, 5, 13, 6, 3, 5, 8, 1, 7, 13, 5, 1, 2, 7, 19, 7, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [30, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_52(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 2, 5, 13, 6, 3, 5, 8, 1, 7, 13, 6, 0, 2, 7, 19, 7, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [30, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_53(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 2, 5, 13, 6, 3, 5, 8, 1, 7, 13, 6, 0, 2, 0, 20, 8, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_54(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 2, 5, 13, 6, 3, 5, 8, 1, 7, 13, 6, 1, 1, 0, 20, 8, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_55(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 5, 13, 6, 3, 5, 8, 1, 7, 13, 6, 1, 1, 0, 20, 8, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_56(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 2, 5, 13, 6, 3, 0, 9, 2, 8, 14, 1, 1, 1, 0, 20, 8, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_57(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 2, 5, 13, 6, 3, 0, 10, 1, 8, 14, 1, 1, 1, 0, 20, 8, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_58(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 5, 13, 6, 3, 0, 10, 1, 8, 14, 2, 0, 1, 0, 20, 8, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_59(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 3, 6, 1, 6, 3, 0, 10, 1, 9, 15, 3, 1, 2, 1, 21, 9, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_60(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [1, 0, 7, 2, 7, 4, 1, 11, 2, 1, 15, 3, 1, 2, 1, 21, 9, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_61(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [1, 0, 7, 2, 7, 5, 0, 11, 2, 1, 15, 3, 1, 2, 1, 21, 9, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_62(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 7, 2, 7, 5, 0, 11, 2, 1, 15, 3, 2, 1, 1, 21, 9, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_63(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 8, 1, 7, 5, 0, 11, 2, 1, 15, 3, 2, 1, 1, 21, 9, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_64(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 8, 1, 7, 5, 0, 11, 2, 1, 16, 4, 3, 2, 2, 22, 10, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_65(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 1, 1, 1, 7, 5, 0, 11, 2, 1, 16, 4, 3, 3, 3, 23, 11, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_66(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [3, 2, 2, 2, 8, 6, 1, 12, 3, 2, 1, 4, 3, 4, 4, 24, 12, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_67(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 3, 1, 2, 8, 6, 1, 12, 3, 2, 1, 4, 3, 4, 4, 24, 12, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_68(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 3, 1, 2, 8, 6, 1, 12, 3, 2, 1, 5, 4, 5, 1, 24, 12, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_69(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 4, 2, 3, 1, 6, 1, 12, 3, 2, 1, 5, 4, 5, 1, 25, 13, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_70(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 4, 2, 3, 1, 6, 1, 12, 3, 3, 2, 6, 5, 1, 1, 25, 13, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_71(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 5, 3, 1, 1, 6, 1, 12, 3, 3, 2, 6, 5, 1, 1, 25, 13, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_72(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [4, 5, 3, 1, 1, 6, 1, 13, 4, 1, 2, 6, 5, 1, 1, 25, 13, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_73(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 1, 3, 1, 1, 6, 1, 13, 4, 1, 2, 6, 5, 1, 1, 26, 14, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_74(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [5, 1, 3, 1, 1, 6, 1, 13, 4, 1, 2, 6, 6, 0, 1, 26, 14, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_75(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [6, 2, 4, 2, 2, 7, 2, 1, 4, 1, 2, 6, 6, 1, 2, 27, 15, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_76(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [6, 2, 4, 2, 2, 7, 2, 1, 4, 2, 1, 6, 6, 1, 2, 27, 15, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_77(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 1, 4, 2, 2, 7, 2, 1, 4, 2, 1, 6, 6, 1, 2, 27, 15, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_78(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [7, 1, 4, 2, 2, 7, 2, 1, 5, 1, 1, 6, 6, 1, 2, 27, 15, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_79(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [8, 2, 1, 2, 2, 7, 2, 1, 5, 1, 1, 6, 6, 1, 2, 27, 15, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_80(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [8, 2, 1, 2, 2, 7, 2, 2, 6, 2, 2, 7, 1, 1, 2, 27, 15, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_81(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 2, 2, 1, 2, 7, 2, 2, 6, 2, 2, 7, 1, 1, 2, 27, 15, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_82(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [8, 2, 2, 1, 2, 0, 3, 3, 7, 3, 3, 1, 1, 1, 2, 27, 15, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_83(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [8, 2, 2, 1, 2, 1, 4, 1, 7, 3, 3, 1, 1, 1, 2, 27, 15, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_84(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [8, 2, 2, 1, 2, 1, 4, 1, 7, 3, 3, 1, 2, 0, 2, 27, 15, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_85(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [8, 2, 2, 1, 2, 1, 5, 0, 7, 3, 3, 1, 2, 0, 2, 27, 15, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_86(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [8, 2, 2, 1, 2, 1, 5, 0, 7, 3, 3, 1, 2, 1, 1, 27, 15, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_87(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 2, 2, 1, 2, 1, 5, 0, 7, 3, 3, 2, 3, 2, 2, 28, 16, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_88(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [1, 2, 2, 1, 2, 1, 5, 1, 8, 1, 3, 2, 3, 2, 2, 28, 16, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_89(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 3, 1, 1, 2, 1, 5, 1, 8, 1, 3, 2, 3, 2, 2, 28, 16, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_90(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 3, 1, 1, 2, 1, 5, 1, 8, 1, 4, 3, 4, 3, 3, 29, 17, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_91(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 4, 0, 1, 2, 1, 5, 1, 8, 1, 4, 3, 4, 3, 3, 29, 17, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_92(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 4, 0, 1, 2, 1, 5, 1, 8, 2, 5, 4, 1, 3, 3, 29, 17, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_93(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [1, 4, 1, 2, 3, 2, 1, 1, 8, 2, 5, 4, 1, 3, 3, 29, 17, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_94(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 4, 1, 2, 3, 2, 1, 1, 8, 2, 5, 5, 0, 3, 3, 29, 17, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_95(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 4, 1, 2, 3, 2, 1, 1, 8, 2, 5, 5, 0, 3, 3, 29, 17, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_96(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 4, 1, 2, 3, 2, 1, 1, 9, 1, 5, 5, 0, 3, 3, 29, 17, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_97(self, gstate):
        """True never created a tuzdek.  False collected more seeds and won."""
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 1, 2, 3, 2, 1, 1, 9, 1, 5, 5, 0, 3, 3, 29, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 36]
        assert cond.name == "WIN"
        gstate.cond = cond
