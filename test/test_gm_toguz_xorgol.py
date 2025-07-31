# -*- coding: utf-8 -*-
"""Integration test for toguz kumalak.

Test
    - captures all evens  (rejection of 2 is not tested)
    - children
    - not facing
    - not opp left
    - win because > 81 seeds

Created on Fri Mar  7 08:28:57 2025
@author: Ann"""


import pytest
pytestmark = pytest.mark.integtest

from context import man_config
from context import man_path

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

    game, _ = man_config.make_game(man_path.GAMEPATH + 'Toguz_Xorgol.txt')
    gstate = GameTestData(game)
    return gstate


@pytest.mark.incremental
class TestToguzXorgol:

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = True
        game.starter = True
        assert game.board == [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [9, 9, 9, 9, 9, 9, 9, 9, 0, 10, 10, 10, 10, 10, 10, 10, 1, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [10, 10, 10, 10, 10, 10, 10, 1, 0, 10, 10, 10, 10, 10, 10, 10, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [11, 11, 11, 11, 11, 11, 11, 2, 1, 1, 10, 10, 10, 10, 10, 10, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [12, 12, 1, 11, 11, 11, 11, 2, 1, 1, 11, 11, 11, 11, 11, 11, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [12, 12, 1, 11, 11, 0, 12, 3, 2, 2, 12, 12, 12, 12, 12, 1, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 12, 1, 11, 11, 0, 12, 4, 3, 3, 13, 13, 13, 13, 13, 2, 3, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 12, 2, 12, 12, 1, 13, 5, 4, 4, 14, 14, 14, 14, 1, 2, 3, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 12, 2, 12, 12, 1, 13, 5, 4, 4, 14, 14, 14, 14, 1, 2, 3, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [10, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 12, 2, 12, 12, 1, 0, 6, 5, 1, 14, 14, 14, 14, 1, 2, 3, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [10, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 2, 12, 12, 1, 0, 6, 6, 2, 15, 15, 15, 15, 2, 3, 4, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [10, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 2, 3, 13, 13, 2, 1, 7, 7, 3, 16, 16, 16, 1, 2, 3, 4, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [10, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 3, 4, 1, 13, 2, 1, 7, 7, 0, 17, 17, 17, 2, 3, 4, 5, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [14, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 3, 4, 1, 13, 2, 1, 7, 7, 0, 17, 17, 18, 3, 4, 5, 1, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [14, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 4, 5, 2, 1, 2, 1, 7, 7, 0, 0, 18, 19, 4, 5, 6, 2, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [32, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [4, 4, 5, 2, 1, 2, 1, 7, 7, 0, 1, 19, 20, 5, 1, 6, 2, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [32, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 4, 5, 2, 1, 2, 1, 7, 7, 0, 1, 19, 20, 5, 1, 7, 3, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [32, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 4, 5, 2, 1, 2, 1, 7, 7, 1, 2, 20, 21, 6, 2, 1, 3, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [32, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 1, 5, 2, 1, 2, 1, 7, 7, 1, 2, 20, 21, 6, 2, 1, 0, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [36, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [2, 1, 5, 2, 1, 2, 1, 7, 0, 0, 2, 20, 21, 6, 2, 1, 0, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [36, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [2, 2, 6, 3, 2, 3, 2, 1, 0, 0, 2, 20, 21, 6, 2, 1, 0, 9]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [36, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 3, 7, 4, 3, 4, 3, 2, 1, 1, 4, 22, 2, 7, 3, 2, 1, 10]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [36, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 4, 1, 4, 3, 4, 3, 2, 1, 1, 4, 22, 2, 7, 0, 3, 2, 11]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [40, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [5, 5, 2, 5, 4, 5, 4, 3, 3, 3, 6, 2, 3, 8, 1, 4, 3, 12]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [40, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [6, 1, 2, 5, 4, 5, 4, 3, 3, 3, 6, 2, 3, 8, 1, 5, 4, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [40, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [6, 1, 2, 5, 4, 0, 5, 4, 4, 4, 1, 2, 3, 8, 1, 5, 4, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [40, 50]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 2, 3, 1, 4, 0, 5, 4, 4, 4, 1, 2, 3, 8, 1, 5, 4, 14]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [40, 50]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [7, 2, 3, 1, 4, 0, 0, 5, 5, 1, 1, 2, 3, 8, 1, 5, 4, 14]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [40, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 2, 3, 1, 4, 0, 0, 5, 5, 1, 1, 2, 0, 9, 2, 6, 5, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 2, 3, 1, 4, 1, 1, 6, 6, 2, 2, 3, 1, 1, 2, 6, 5, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [1, 2, 4, 2, 5, 2, 2, 1, 6, 2, 2, 3, 1, 1, 2, 6, 5, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 2, 4, 2, 5, 2, 2, 1, 6, 2, 2, 4, 0, 1, 2, 6, 5, 15]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 4, 2, 5, 2, 2, 1, 6, 2, 2, 4, 0, 1, 2, 6, 5, 16]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 2, 4, 2, 5, 2, 2, 1, 7, 1, 2, 4, 0, 1, 2, 6, 5, 16]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 3, 1, 2, 5, 2, 2, 1, 7, 1, 2, 4, 0, 1, 2, 6, 5, 17]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [1, 3, 1, 2, 5, 2, 2, 1, 8, 0, 2, 4, 0, 1, 2, 6, 5, 17]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 1, 1, 2, 5, 2, 2, 1, 8, 0, 2, 4, 0, 1, 2, 6, 5, 18]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_37(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 1, 1, 2, 5, 2, 2, 1, 8, 0, 2, 4, 0, 2, 1, 6, 5, 18]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_38(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 2, 0, 2, 5, 2, 2, 1, 8, 0, 2, 4, 0, 2, 1, 6, 5, 18]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_39(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [2, 2, 0, 2, 5, 2, 2, 1, 9, 1, 3, 1, 0, 2, 1, 6, 5, 18]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_40(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 2, 0, 2, 5, 2, 2, 1, 9, 1, 3, 1, 0, 2, 1, 6, 5, 19]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_41(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [1, 2, 0, 2, 5, 2, 2, 1, 10, 2, 1, 1, 0, 2, 1, 6, 5, 19]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_42(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 5, 2, 2, 1, 10, 2, 1, 1, 0, 2, 1, 6, 5, 20]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_43(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 2, 0, 2, 5, 2, 2, 1, 10, 2, 2, 0, 0, 2, 1, 6, 5, 20]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_44(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 6, 1, 2, 1, 10, 2, 2, 0, 0, 2, 1, 6, 5, 20]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_45(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 2, 0, 2, 6, 1, 2, 1, 11, 1, 2, 0, 0, 2, 1, 6, 5, 20]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_46(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 6, 2, 1, 1, 11, 1, 2, 0, 0, 2, 1, 6, 5, 20]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_47(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 2, 0, 2, 6, 2, 1, 1, 12, 0, 2, 0, 0, 2, 1, 6, 5, 20]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_48(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 6, 2, 2, 0, 12, 0, 2, 0, 0, 2, 1, 6, 5, 20]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_49(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 0, 2, 6, 2, 2, 0, 12, 0, 2, 0, 1, 3, 2, 7, 1, 20]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_50(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 1, 1, 6, 2, 2, 0, 12, 0, 2, 0, 1, 3, 2, 7, 1, 20]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_51(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 1, 1, 6, 2, 2, 0, 12, 0, 2, 0, 1, 3, 2, 8, 0, 20]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_52(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 3, 2, 2, 1, 2, 2, 0, 12, 0, 2, 0, 1, 3, 2, 8, 0, 21]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_53(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 3, 2, 2, 1, 2, 2, 0, 12, 0, 2, 1, 2, 1, 2, 8, 0, 21]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_54(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 1, 2, 2, 1, 2, 2, 0, 12, 0, 2, 1, 2, 1, 2, 8, 0, 22]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_55(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 1, 2, 2, 1, 2, 2, 0, 13, 1, 3, 2, 3, 2, 3, 1, 0, 22]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_56(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 1, 2, 2, 1, 2, 2, 0, 13, 1, 3, 2, 3, 2, 3, 1, 0, 23]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_57(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [1, 1, 2, 2, 1, 2, 2, 0, 14, 2, 1, 2, 3, 2, 3, 1, 0, 23]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_58(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 2, 2, 1, 2, 2, 0, 14, 2, 1, 2, 3, 2, 3, 1, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_59(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 1, 2, 2, 1, 2, 2, 0, 15, 1, 1, 2, 3, 2, 3, 1, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_60(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 2, 2, 2, 1, 2, 0, 15, 1, 1, 2, 3, 2, 3, 1, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_61(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 1, 2, 2, 2, 1, 2, 0, 16, 0, 1, 2, 3, 2, 3, 1, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_62(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 1, 2, 2, 2, 2, 1, 0, 16, 0, 1, 2, 3, 2, 3, 1, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_63(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 2, 2, 2, 2, 1, 0, 16, 0, 1, 2, 3, 2, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_64(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 1, 2, 2, 2, 1, 0, 16, 0, 1, 2, 3, 2, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_65(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 2, 1, 2, 2, 2, 1, 0, 16, 1, 0, 2, 3, 2, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_66(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 2, 1, 2, 2, 1, 0, 16, 1, 0, 2, 3, 2, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_67(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 2, 2, 1, 2, 2, 1, 0, 17, 0, 0, 2, 3, 2, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_68(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 2, 2, 1, 2, 1, 0, 17, 0, 0, 2, 3, 2, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_69(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 2, 2, 1, 2, 1, 0, 17, 0, 0, 2, 4, 1, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_70(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 2, 2, 2, 1, 1, 0, 17, 0, 0, 2, 4, 1, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_71(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 2, 2, 2, 1, 1, 0, 17, 0, 0, 2, 5, 0, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_72(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 2, 2, 2, 2, 2, 0, 0, 17, 0, 0, 2, 5, 0, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_73(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 2, 2, 2, 2, 0, 0, 18, 1, 1, 3, 1, 0, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_74(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 2, 2, 2, 2, 0, 0, 18, 1, 1, 3, 1, 0, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_75(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [1, 1, 2, 2, 2, 2, 0, 0, 19, 0, 1, 3, 1, 0, 4, 0, 0, 24]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_76(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 2, 2, 2, 2, 0, 0, 19, 0, 1, 3, 1, 0, 4, 0, 0, 25]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_77(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 2, 2, 2, 2, 0, 0, 19, 0, 1, 4, 2, 1, 1, 0, 0, 25]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_78(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 2, 2, 2, 0, 0, 19, 0, 1, 4, 2, 1, 1, 0, 0, 25]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_79(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 0, 2, 2, 2, 2, 0, 0, 20, 1, 2, 1, 2, 1, 1, 0, 0, 25]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_80(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 2, 2, 2, 2, 0, 0, 20, 1, 2, 1, 2, 1, 1, 0, 0, 26]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_81(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 0, 2, 2, 2, 2, 0, 0, 21, 0, 2, 1, 2, 1, 1, 0, 0, 26]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_82(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 1, 2, 2, 2, 0, 0, 21, 0, 2, 1, 2, 1, 1, 0, 0, 26]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_83(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 2, 2, 2, 0, 0, 21, 0, 2, 1, 2, 2, 0, 0, 0, 26]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_84(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 2, 2, 0, 0, 21, 0, 2, 1, 2, 2, 0, 0, 0, 26]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_85(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 0, 2, 2, 2, 0, 0, 21, 0, 2, 2, 1, 2, 0, 0, 0, 26]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_86(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 1, 1, 2, 2, 0, 0, 21, 0, 2, 2, 1, 2, 0, 0, 0, 26]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_87(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 1, 1, 2, 2, 0, 0, 21, 0, 2, 2, 2, 1, 0, 0, 0, 26]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_88(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 2, 0, 2, 2, 0, 0, 21, 0, 2, 2, 2, 1, 0, 0, 0, 26]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_89(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 2, 2, 0, 2, 2, 0, 0, 21, 1, 1, 2, 2, 1, 0, 0, 0, 26]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_90(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 2, 0, 2, 2, 0, 0, 21, 1, 1, 2, 2, 1, 0, 0, 0, 26]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_91(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [1, 1, 2, 0, 2, 2, 0, 0, 22, 0, 1, 2, 2, 1, 0, 0, 0, 26]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_92(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 2, 2, 0, 0, 22, 0, 1, 2, 2, 1, 0, 0, 0, 27]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_93(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 2, 0, 2, 2, 0, 0, 22, 0, 2, 1, 2, 1, 0, 0, 0, 27]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_94(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 2, 2, 0, 0, 22, 0, 2, 1, 2, 1, 0, 0, 0, 27]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_95(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 2, 2, 0, 0, 22, 0, 2, 2, 1, 1, 0, 0, 0, 27]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_96(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 2, 2, 0, 0, 22, 0, 2, 2, 1, 1, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_97(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 2, 2, 0, 0, 22, 0, 2, 2, 2, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_98(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 2, 1, 1, 2, 0, 0, 22, 0, 2, 2, 2, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_99(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 1, 2, 0, 0, 22, 1, 1, 2, 2, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_100(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 2, 2, 0, 2, 0, 0, 22, 1, 1, 2, 2, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_101(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 0, 2, 2, 0, 2, 0, 0, 23, 0, 1, 2, 2, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_102(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 2, 2, 1, 1, 0, 0, 23, 0, 1, 2, 2, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_103(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 2, 2, 1, 1, 0, 0, 23, 0, 2, 1, 2, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_104(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 2, 2, 2, 0, 0, 0, 23, 0, 2, 1, 2, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_105(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 2, 2, 2, 0, 0, 0, 23, 0, 2, 2, 1, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_106(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 1, 2, 2, 0, 0, 0, 23, 0, 2, 2, 1, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_107(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 1, 1, 2, 2, 0, 0, 0, 23, 1, 1, 2, 1, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_108(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 2, 0, 0, 0, 23, 1, 1, 2, 1, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_109(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 2, 0, 2, 2, 0, 0, 0, 24, 0, 1, 2, 1, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_110(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 1, 1, 2, 0, 0, 0, 24, 0, 1, 2, 1, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_111(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 2, 1, 1, 2, 0, 0, 0, 24, 0, 2, 1, 1, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_112(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 2, 0, 2, 0, 0, 0, 24, 0, 2, 1, 1, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_113(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 2, 0, 2, 0, 0, 0, 24, 0, 2, 2, 0, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_114(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 2, 0, 2, 0, 0, 0, 24, 0, 2, 2, 0, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_115(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [1, 1, 2, 0, 2, 0, 0, 0, 24, 1, 1, 2, 0, 0, 0, 0, 0, 28]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_116(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 2, 0, 0, 0, 24, 1, 1, 2, 0, 0, 0, 0, 0, 29]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_117(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 1, 2, 0, 2, 0, 0, 0, 25, 0, 1, 2, 0, 0, 0, 0, 0, 29]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_118(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 2, 0, 0, 0, 25, 0, 1, 2, 0, 0, 0, 0, 0, 29]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_119(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 2, 0, 0, 0, 25, 1, 0, 2, 0, 0, 0, 0, 0, 29]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_120(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 1, 1, 1, 0, 0, 0, 25, 1, 0, 2, 0, 0, 0, 0, 0, 29]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_121(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.mdata.winner is True
        assert game.board == [0, 2, 1, 1, 1, 0, 0, 0, 26, 0, 0, 2, 0, 0, 0, 0, 0, 29]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, F]
        assert game.store == [44, 56]
        assert cond.name == "WIN"
        gstate.cond = cond
