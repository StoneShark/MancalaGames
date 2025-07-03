# -*- coding: utf-8 -*-
"""Integration test for toguz kumalak.

Test
    - captures of 2 and all evens
    - children
    - no opp right
    - no sym opp
    - end game because no moves

Created on Fri Mar  7 07:57:24 2025
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

    game, _ = man_config.make_game('./GameProps/Toguz_Kumalak.txt')
    gstate = GameTestData(game)
    return gstate


@pytest.mark.incremental
class TestToguzKumalak:

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = False
        game.starter = False
        assert game.board == [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [9, 9, 9, 9, 9, 9, 9, 9, 1, 10, 10, 10, 10, 10, 10, 10, 0, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [10, 10, 10, 10, 10, 10, 10, 0, 1, 10, 10, 10, 10, 10, 10, 10, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [10, 10, 10, 10, 10, 10, 10, 0, 0, 11, 10, 10, 10, 10, 10, 10, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [11, 10, 10, 10, 10, 10, 10, 0, 0, 11, 10, 10, 10, 10, 10, 10, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [11, 10, 10, 10, 10, 10, 1, 1, 1, 12, 11, 11, 11, 11, 11, 11, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [12, 11, 11, 10, 10, 10, 1, 1, 1, 1, 12, 12, 12, 12, 12, 12, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [12, 11, 11, 10, 10, 10, 1, 1, 0, 0, 12, 12, 12, 12, 12, 12, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [12, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [13, 12, 12, 11, 11, 11, 2, 2, 1, 0, 12, 12, 12, 12, 12, 1, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [12, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 13, 13, 12, 12, 12, 3, 3, 2, 1, 13, 13, 13, 12, 12, 1, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [12, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 14, 14, 13, 13, 13, 4, 0, 2, 1, 13, 13, 13, 12, 1, 2, 3, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 14, 14, 13, 13, 1, 5, 1, 3, 2, 14, 14, 14, 13, 2, 3, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [3, 15, 15, 14, 14, 2, 0, 1, 3, 2, 14, 1, 15, 14, 3, 4, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 1, 16, 15, 15, 3, 1, 2, 4, 3, 15, 2, 16, 15, 4, 5, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 1, 16, 15, 15, 3, 1, 2, 4, 3, 15, 2, 16, 15, 1, 6, 6, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 1, 1, 16, 16, 4, 2, 3, 5, 4, 16, 3, 17, 16, 2, 7, 7, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [4, 2, 2, 17, 17, 5, 3, 0, 5, 4, 1, 4, 18, 17, 3, 8, 8, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 3, 2, 1, 18, 6, 4, 1, 6, 5, 2, 5, 19, 18, 4, 9, 9, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [6, 4, 3, 2, 19, 7, 5, 2, 7, 6, 3, 6, 2, 19, 5, 10, 10, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 5, 4, 3, 20, 8, 5, 2, 7, 6, 3, 6, 2, 19, 5, 10, 10, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 5, 4, 3, 20, 8, 5, 2, 7, 6, 3, 1, 3, 20, 6, 11, 11, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [1, 5, 4, 3, 20, 8, 5, 2, 1, 7, 4, 2, 4, 21, 7, 11, 11, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 6, 5, 4, 21, 9, 6, 3, 2, 8, 5, 3, 5, 2, 9, 13, 12, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [2, 6, 5, 4, 21, 9, 6, 3, 1, 9, 5, 3, 5, 2, 9, 13, 12, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 7, 6, 5, 0, 9, 6, 3, 1, 9, 5, 3, 5, 2, 1, 14, 13, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [3, 7, 6, 5, 0, 9, 6, 1, 2, 0, 5, 3, 5, 2, 1, 14, 13, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [3, 7, 6, 5, 0, 9, 6, 1, 2, 0, 1, 4, 6, 3, 2, 14, 13, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [3, 7, 6, 5, 0, 9, 1, 2, 3, 1, 2, 5, 6, 3, 2, 14, 13, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [3, 7, 6, 5, 0, 9, 1, 2, 3, 1, 2, 1, 7, 4, 3, 15, 13, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [3, 7, 6, 5, 0, 9, 1, 2, 1, 2, 3, 1, 7, 4, 3, 15, 13, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [26, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 7, 6, 5, 0, 9, 1, 2, 1, 2, 3, 1, 7, 1, 4, 16, 14, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [26, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [3, 7, 6, 5, 0, 9, 0, 3, 1, 2, 3, 1, 7, 1, 4, 16, 14, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [26, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 7, 6, 5, 0, 9, 0, 3, 1, 2, 3, 1, 7, 1, 1, 17, 15, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [26, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [3, 7, 6, 5, 0, 9, 0, 1, 2, 3, 3, 1, 7, 1, 1, 17, 15, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [26, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [3, 7, 6, 5, 0, 9, 0, 1, 2, 1, 4, 2, 7, 1, 1, 17, 15, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [26, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [3, 7, 6, 5, 0, 9, 0, 1, 1, 0, 4, 2, 7, 1, 1, 17, 15, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [28, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 7, 6, 5, 0, 9, 0, 1, 1, 0, 4, 2, 1, 2, 2, 18, 16, 10]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [28, 50]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_37(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 7, 6, 5, 0, 9, 0, 1, 0, 1, 4, 2, 1, 2, 2, 18, 16, 10]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [28, 50]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_38(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 7, 6, 5, 0, 9, 0, 1, 0, 1, 4, 2, 1, 1, 3, 18, 16, 10]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [28, 50]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_39(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 7, 6, 5, 0, 1, 1, 2, 1, 2, 5, 3, 2, 0, 3, 18, 16, 10]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [30, 50]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_40(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 8, 7, 6, 1, 2, 2, 3, 0, 2, 5, 3, 2, 0, 3, 18, 16, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [30, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_41(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [1, 8, 7, 6, 1, 2, 2, 1, 1, 3, 5, 3, 2, 0, 3, 18, 16, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [30, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_42(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 9, 8, 7, 2, 3, 3, 2, 2, 4, 6, 4, 3, 1, 4, 1, 17, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [30, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_43(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 9, 8, 1, 3, 4, 4, 3, 3, 5, 6, 4, 3, 1, 4, 1, 17, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [30, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_44(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [2, 9, 8, 1, 3, 4, 4, 3, 3, 1, 7, 5, 4, 2, 4, 1, 17, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [30, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_45(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [2, 9, 8, 1, 3, 4, 1, 4, 4, 0, 7, 5, 4, 2, 4, 1, 17, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [32, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_46(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 9, 8, 1, 3, 4, 1, 4, 4, 0, 7, 5, 4, 2, 1, 2, 18, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [32, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_47(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 1, 9, 2, 4, 5, 2, 5, 5, 1, 7, 5, 4, 2, 1, 2, 18, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [32, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_48(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [2, 1, 9, 2, 4, 5, 2, 5, 5, 1, 7, 1, 5, 3, 2, 3, 18, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [32, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_49(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [2, 1, 9, 2, 4, 5, 2, 5, 1, 2, 8, 2, 0, 3, 2, 3, 18, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [38, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_50(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 0, 9, 2, 4, 5, 2, 5, 1, 2, 8, 2, 0, 3, 2, 3, 18, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [38, 54]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_51(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [3, 0, 9, 2, 4, 5, 2, 1, 2, 3, 9, 3, 0, 3, 2, 3, 18, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [38, 54]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_52(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 9, 2, 4, 5, 2, 1, 2, 3, 9, 3, 0, 3, 2, 3, 18, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [38, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_53(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 0, 9, 2, 4, 5, 2, 1, 1, 0, 9, 3, 0, 3, 2, 3, 18, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [42, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_54(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 9, 2, 4, 5, 2, 1, 1, 0, 9, 1, 1, 4, 2, 3, 18, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [42, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_55(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 0, 9, 2, 4, 5, 2, 1, 0, 1, 9, 1, 1, 4, 2, 3, 18, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [42, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_56(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 10, 3, 5, 6, 3, 2, 1, 2, 10, 2, 2, 5, 3, 4, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [42, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_57(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 1, 4, 6, 7, 4, 3, 2, 3, 11, 3, 2, 5, 3, 4, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [42, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_58(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [1, 1, 1, 4, 6, 7, 4, 3, 2, 1, 12, 4, 2, 5, 3, 4, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [42, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_59(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [1, 1, 1, 4, 6, 7, 1, 4, 3, 0, 12, 4, 2, 5, 3, 4, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [44, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_60(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 1, 4, 6, 7, 1, 4, 3, 0, 12, 4, 2, 5, 3, 1, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [44, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_61(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 1, 1, 4, 6, 7, 1, 4, 1, 1, 13, 4, 2, 5, 3, 1, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [44, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_62(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 1, 4, 6, 7, 1, 4, 1, 1, 13, 4, 1, 6, 3, 1, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [44, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_63(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 1, 4, 1, 8, 2, 5, 2, 0, 13, 4, 1, 6, 3, 1, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [46, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_64(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 1, 4, 1, 8, 2, 5, 2, 0, 13, 4, 0, 7, 3, 1, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [46, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_65(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 4, 1, 8, 2, 5, 2, 0, 13, 4, 0, 7, 3, 1, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [46, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_66(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 2, 4, 1, 8, 2, 5, 2, 0, 13, 4, 0, 7, 3, 1, 1, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [46, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_67(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [0, 0, 2, 4, 1, 8, 2, 1, 3, 1, 14, 5, 0, 7, 3, 1, 1, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [46, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_68(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 2, 4, 1, 8, 2, 1, 3, 1, 14, 5, 0, 1, 4, 2, 2, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [46, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_69(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [1, 1, 2, 4, 1, 8, 2, 0, 4, 1, 14, 5, 0, 1, 4, 2, 2, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [46, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_70(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 1, 2, 4, 1, 8, 2, 0, 4, 1, 14, 1, 1, 2, 5, 3, 2, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [46, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_71(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [1, 1, 2, 4, 1, 8, 2, 0, 1, 2, 15, 0, 1, 2, 5, 3, 2, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [48, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_72(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 2, 4, 1, 8, 2, 0, 1, 2, 15, 0, 0, 3, 5, 3, 2, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [48, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_73(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 2, 1, 2, 9, 3, 0, 1, 2, 15, 0, 0, 3, 5, 3, 2, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [48, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_74(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 2, 1, 2, 9, 3, 0, 1, 2, 15, 0, 0, 1, 6, 4, 2, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [48, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_75(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 2, 1, 2, 1, 4, 1, 2, 3, 16, 1, 1, 0, 6, 4, 2, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [50, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_76(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 0, 2, 1, 2, 1, 4, 1, 2, 3, 16, 1, 1, 0, 1, 5, 3, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [50, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_77(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [2, 0, 2, 1, 2, 1, 4, 0, 3, 3, 16, 1, 1, 0, 1, 5, 3, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [50, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_78(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 1, 3, 0, 2, 1, 4, 0, 3, 3, 16, 1, 1, 0, 1, 5, 3, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [50, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_79(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 2, 4, 0, 2, 1, 4, 0, 3, 3, 16, 1, 1, 0, 1, 5, 3, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [50, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_80(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 3, 4, 0, 2, 1, 4, 0, 3, 3, 16, 1, 1, 0, 1, 1, 4, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [50, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_81(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [2, 3, 4, 0, 2, 1, 1, 1, 4, 0, 16, 1, 1, 0, 1, 1, 4, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [54, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_82(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 3, 4, 0, 2, 1, 1, 1, 4, 0, 16, 1, 1, 0, 1, 1, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [54, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_83(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [3, 3, 4, 0, 2, 1, 1, 1, 1, 1, 17, 0, 1, 0, 1, 1, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [56, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_84(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 3, 4, 0, 2, 1, 1, 1, 1, 1, 17, 0, 1, 0, 0, 2, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [56, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_85(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 1, 5, 1, 2, 1, 1, 1, 1, 1, 17, 0, 1, 0, 0, 2, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [56, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_86(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [4, 0, 5, 1, 2, 1, 1, 1, 1, 1, 17, 0, 1, 0, 0, 2, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [56, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_87(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [4, 0, 5, 1, 2, 1, 1, 1, 0, 0, 17, 0, 1, 0, 0, 2, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_88(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 0, 5, 1, 2, 1, 1, 1, 0, 0, 17, 0, 1, 0, 0, 2, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_89(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 0, 5, 1, 1, 2, 1, 1, 0, 0, 17, 0, 1, 0, 0, 2, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_90(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 0, 5, 1, 1, 2, 1, 1, 0, 0, 17, 0, 1, 0, 0, 2, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_91(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 0, 1, 2, 2, 3, 2, 1, 0, 0, 17, 0, 1, 0, 0, 2, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_92(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 0, 1, 2, 2, 3, 2, 1, 0, 0, 17, 0, 1, 0, 0, 2, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_93(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [6, 0, 1, 2, 2, 1, 3, 2, 0, 0, 17, 0, 1, 0, 0, 2, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_94(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 0, 1, 2, 2, 1, 3, 2, 0, 0, 17, 0, 1, 0, 0, 2, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_95(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [7, 0, 1, 2, 2, 1, 3, 1, 1, 0, 17, 0, 1, 0, 0, 2, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_96(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [7, 0, 1, 2, 2, 1, 3, 1, 1, 0, 17, 0, 1, 0, 0, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_97(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 2, 2, 0, 17, 0, 1, 0, 0, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_98(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 2, 2, 0, 17, 0, 1, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_99(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 2, 1, 1, 17, 0, 1, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_100(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 2, 1, 0, 18, 0, 1, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_101(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 1, 2, 0, 18, 0, 1, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_102(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 1, 2, 0, 18, 0, 0, 1, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_103(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 1, 1, 1, 18, 0, 0, 1, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_104(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 1, 1, 0, 19, 0, 0, 1, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_105(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 0, 2, 0, 19, 0, 0, 1, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_106(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 0, 2, 0, 19, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_107(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 0, 1, 1, 19, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_108(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 0, 1, 0, 20, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_109(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 0, 0, 1, 20, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_110(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [7, 0, 1, 2, 2, 1, 1, 0, 0, 1, 20, 0, 0, 0, 0, 2, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_111(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [7, 0, 0, 3, 2, 1, 1, 0, 0, 1, 20, 0, 0, 0, 0, 2, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_112(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [7, 0, 0, 3, 2, 1, 1, 0, 0, 1, 20, 0, 0, 0, 0, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_113(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 0, 0, 1, 3, 2, 1, 0, 0, 1, 20, 0, 0, 0, 0, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_114(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [7, 0, 0, 1, 3, 2, 1, 0, 0, 1, 20, 0, 0, 0, 0, 0, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_115(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 0, 0, 0, 4, 2, 1, 0, 0, 1, 20, 0, 0, 0, 0, 0, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_116(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [7, 0, 0, 0, 4, 2, 1, 0, 0, 1, 20, 0, 0, 0, 0, 0, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_117(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [7, 0, 0, 0, 4, 2, 0, 1, 0, 1, 20, 0, 0, 0, 0, 0, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_118(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [8, 0, 0, 0, 4, 2, 0, 1, 0, 1, 20, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_119(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [8, 0, 0, 0, 4, 2, 0, 0, 1, 1, 20, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_120(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [8, 0, 0, 0, 4, 2, 0, 0, 1, 0, 21, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_121(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [8, 0, 0, 0, 4, 1, 1, 0, 1, 0, 21, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_122(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [8, 0, 0, 0, 4, 1, 1, 0, 1, 0, 21, 0, 0, 0, 0, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_123(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [8, 0, 0, 0, 1, 2, 2, 1, 1, 0, 21, 0, 0, 0, 0, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_124(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [9, 0, 0, 0, 1, 2, 2, 1, 1, 0, 21, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_125(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [9, 0, 0, 0, 1, 2, 2, 0, 2, 0, 21, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_126(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [10, 0, 0, 0, 1, 2, 2, 0, 2, 0, 21, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [58, 66]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_127(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.mdata.winner is False
        assert game.board == [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [T, N, N, N, N, N, N, N, N, N, F, N, N, N, N, N, N, N]
        assert game.store == [65, 66]
        assert cond.name == "WIN"
        gstate.cond = cond
