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
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 7, 7, 7, 7, 0, 1, 7, 2, 8, 0, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 7, 0, 8, 8, 1, 2, 8, 3, 9, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [8, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 1, 2, 8, 0, 0, 8, 0, 0, 0, 0, 10, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [8, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [3, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 0, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [23, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 3, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [23, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 2, 0, 3, 1, 0, 2, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [23, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 2, 0, 3, 0, 1, 0, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [23, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [25, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [25, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [25, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [25, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [25, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [25, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [25, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [25, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [25, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [25, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [26, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [27, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [27, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [29, 41]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [4, 6]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [6, 0, 0, 6, 6, 0, 0, 6, 6, 0, 6, 0, 6, 6]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 2, 2, 0, 8, 0, 0, 2, 9, 0, 0, 0, 8, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 0, 0, 0, 3, 10, 1, 1, 0, 9, 1]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [20, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 2, 1, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 2, 0, 1, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [25, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [25, 45]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_3_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 10]

    def test_round_3_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 0, 6, 0, 6, 0, 0, 6, 6, 6, 6, 0, 0, 6]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 8, 0, 0, 8, 8, 1, 0, 2, 0, 8]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_3(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 8, 0, 0, 1, 3, 1, 9]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 3, 1, 9]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_7(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 2, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_8(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 2, 0, 0, 0, 2, 0, 2, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [23, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_9(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 2, 0, 0, 0, 0, 1, 3, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [23, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [27, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [27, 43]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_4_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 8]

    def test_round_4_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 6, 6, 0, 0, 0, 0, 6, 6, 0, 6, 0, 6, 6]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_2(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [8, 1, 0, 2, 0, 0, 0, 8, 0, 3, 0, 0, 8, 8]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 3, 1, 0, 0, 9, 1, 0, 1, 0, 0, 8]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_4(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [2, 0, 3, 1, 3, 0, 0, 2, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [24, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [32, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_6(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [32, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [32, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [32, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_9(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [32, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_10(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [32, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [32, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_12(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [32, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [32, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [32, 38]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_5_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 3]

    def test_round_5_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 7, 7, 7, 7, 0, 0, 0, 0, 7, 7, 7, 7, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 3, 1, 0, 0, 2, 0, 2, 11, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [31, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 3, 1, 0, 0, 2, 0, 0, 12, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [31, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 2, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [46, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_5(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [46, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [48, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_7(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [48, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_8(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [48, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [48, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [48, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [48, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_12(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [48, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [48, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [48, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_15(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [48, 22]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_6_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [13, 2]

    def test_round_6_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 9, 9, 0, 0, 0, 0, 1, 0, 3, 9, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [35, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 12, 0, 0, 2, 2, 2, 3, 2, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [39, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 0, 3, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [47, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_4(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [3, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [47, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [51, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [51, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [51, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_8(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [51, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [51, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [51, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [53, 17]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_7_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 2]

    def test_round_7_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 9, 9, 9, 0, 0, 0, 1, 0, 9, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 11, 11, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [29, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_3(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 14, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [29, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [48, 22]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_8_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [13, 2]

    def test_round_8_move_1(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [9, 3, 9, 2, 9, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [35, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [10, 0, 10, 3, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [35, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [68, 2]
        assert cond.name == "WIN"
        gstate.cond = cond
