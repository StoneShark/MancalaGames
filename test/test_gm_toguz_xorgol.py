# -*- coding: utf-8 -*-
"""Integration testing of Toguz Xorgol.
Tuzdek!

One test.
Tuzdek making:
    no 2nd child
    not in 0 & 9 by T & F respectively
    not in symmetric opposite

Confirm stores always grow by an even number >= 4


Created on Wed Oct  9 09:24:54 2024
@author: Ann"""


import pytest
pytestmark = pytest.mark.integtest

from context import man_config


T = True
F = False
N = None

class GameTestData:
    """move data (cond) to be carried between tests."""

    def __init__(self, game):
        self.game = game
        self.cond = None
        self.store = (0, 0)


@pytest.fixture(scope="class")
def gstate():
    """This fixture will maintain state between tests in the
    same class but will be reconstructed for each class."""

    game, _ = man_config.make_game('./GameProps/Toguz_Xorgol.txt')
    gstate = GameTestData(game)
    return gstate


def check_save_store(pdata):
    """assure that the store always increases by evens of at least 4.

    pdata is GameTestData for the test"""

    for s in [0, 1]:
        diff = pdata.game.store[s] - pdata.store[s]
        if diff == 0:
            continue
        assert (not diff % 2) and (diff >= 4)

    pdata.store = tuple(pdata.game.store)


@pytest.mark.incremental
class TestTuzdekGame:

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = True
        game.starter = True
        assert game.board == [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [9, 9, 9, 9, 9, 9, 9, 0, 10, 10, 10, 10, 10, 10, 10, 1, 9, 9]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [10, 10, 10, 1, 9, 9, 9, 0, 10, 10, 10, 10, 10, 11, 11, 2, 10, 10]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [10, 10, 10, 1, 9, 9, 9, 1, 11, 11, 11, 11, 11, 12, 12, 3, 1, 10]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [11, 11, 1, 1, 9, 9, 9, 1, 11, 11, 11, 0, 12, 13, 13, 4, 2, 11]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [12, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_5(self, gstate):
        """No capture of 2 at 7"""
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [11, 11, 1, 1, 9, 9, 9, 2, 12, 12, 12, 1, 13, 14, 14, 5, 3, 1]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [12, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 11, 1, 1, 9, 9, 9, 2, 13, 13, 13, 2, 14, 15, 15, 6, 4, 2]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [12, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [2, 12, 2, 2, 10, 10, 10, 3, 14, 14, 1, 2, 14, 15, 15, 6, 5, 3]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [12, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 13, 1, 2, 10, 10, 10, 3, 14, 14, 1, 2, 14, 15, 15, 6, 5, 3]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [12, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 14, 2, 3, 11, 11, 11, 4, 15, 15, 2, 3, 15, 1, 15, 6, 5, 4]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [12, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 14, 2, 3, 11, 11, 11, 4, 15, 15, 2, 3, 15, 1, 15, 6, 0, 5]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [1, 14, 2, 3, 11, 11, 11, 4, 15, 16, 1, 3, 15, 1, 15, 6, 0, 5]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 15, 1, 3, 11, 11, 11, 4, 15, 16, 1, 3, 15, 1, 15, 6, 0, 5]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 15, 1, 3, 11, 11, 11, 4, 15, 16, 1, 3, 15, 2, 16, 7, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 15, 1, 3, 11, 11, 11, 4, 15, 16, 1, 3, 15, 2, 16, 7, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [1, 16, 2, 4, 12, 12, 12, 5, 16, 1, 1, 3, 16, 3, 17, 8, 2, 3]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [18, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 16, 2, 4, 12, 12, 12, 5, 16, 1, 1, 3, 16, 3, 17, 8, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 16, 2, 4, 12, 12, 12, 5, 16, 2, 2, 1, 16, 3, 17, 8, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 17, 3, 5, 13, 1, 12, 5, 16, 2, 2, 1, 17, 4, 18, 9, 3, 1]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 17, 3, 5, 13, 1, 12, 5, 16, 2, 3, 0, 17, 4, 18, 9, 3, 1]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is True
        assert game.board == [1, 17, 3, 6, 14, 2, 13, 1, 16, 2, 3, 0, 17, 4, 18, 9, 3, 1]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 17, 3, 6, 14, 2, 13, 1, 16, 2, 4, 1, 18, 1, 18, 9, 3, 1]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [2, 18, 4, 7, 15, 3, 14, 2, 1, 2, 4, 2, 19, 2, 19, 10, 4, 2]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_23(self, gstate):
        """Tuzdek by True at 7"""
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [2, 18, 4, 7, 15, 3, 14, 3, 2, 3, 1, 2, 19, 2, 19, 10, 4, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [2, 18, 4, 7, 15, 3, 14, 4, 1, 3, 1, 2, 19, 2, 19, 10, 4, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [2, 18, 4, 7, 15, 3, 14, 4, 1, 3, 2, 1, 19, 2, 19, 10, 4, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 18, 4, 8, 16, 1, 14, 4, 1, 3, 2, 1, 19, 2, 19, 10, 4, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [2, 18, 4, 8, 16, 1, 14, 4, 1, 4, 1, 1, 19, 2, 19, 10, 4, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 1, 5, 9, 17, 2, 15, 5, 2, 5, 2, 2, 20, 3, 20, 11, 5, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [3, 1, 5, 9, 17, 2, 15, 5, 2, 6, 1, 2, 20, 3, 20, 11, 5, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 2, 1, 9, 17, 2, 15, 5, 2, 6, 1, 2, 20, 3, 20, 11, 0, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [28, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 2, 1, 9, 17, 2, 15, 5, 2, 6, 1, 3, 21, 1, 20, 11, 0, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [28, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 3, 2, 10, 1, 2, 16, 6, 3, 7, 2, 4, 22, 2, 21, 12, 1, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [28, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [6, 4, 3, 11, 2, 3, 17, 7, 4, 8, 3, 5, 24, 4, 2, 13, 2, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [28, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 5, 4, 1, 2, 3, 17, 7, 4, 8, 3, 0, 25, 5, 3, 14, 3, 7]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [34, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 5, 4, 1, 2, 3, 17, 7, 4, 8, 3, 1, 26, 6, 4, 15, 4, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [34, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [8, 6, 5, 2, 3, 4, 1, 7, 5, 9, 4, 2, 27, 7, 5, 16, 5, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [34, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [9, 7, 6, 3, 5, 6, 3, 9, 7, 11, 6, 4, 2, 8, 6, 17, 6, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [34, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_38(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [10, 8, 7, 4, 6, 1, 3, 9, 7, 11, 6, 4, 2, 8, 6, 17, 6, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [34, 10]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_39(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [10, 8, 7, 4, 6, 1, 0, 10, 8, 12, 7, 5, 3, 1, 6, 17, 6, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [34, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_40(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 8, 7, 4, 6, 1, 0, 10, 8, 13, 8, 6, 4, 2, 7, 18, 7, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [34, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_41(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 9, 8, 5, 7, 2, 1, 11, 9, 14, 9, 7, 5, 3, 8, 1, 8, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [34, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_42(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 10, 9, 1, 7, 2, 1, 11, 9, 14, 9, 7, 5, 3, 8, 1, 8, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [40, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_43(self, gstate):
        """Second child prevented at 5."""
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [3, 10, 9, 1, 7, 3, 2, 12, 10, 15, 10, 1, 5, 3, 8, 1, 8, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [40, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_44(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 1, 9, 1, 7, 3, 2, 12, 10, 15, 11, 2, 6, 4, 9, 2, 9, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [40, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_45(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 1, 9, 1, 7, 3, 2, 12, 10, 15, 11, 2, 6, 4, 10, 1, 9, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [40, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_46(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 1, 9, 2, 8, 1, 2, 12, 10, 15, 11, 2, 6, 4, 10, 1, 9, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [40, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_47(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [4, 1, 9, 2, 8, 2, 3, 13, 11, 16, 12, 3, 7, 5, 1, 1, 9, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [40, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_48(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [5, 2, 10, 3, 9, 3, 4, 14, 1, 16, 12, 3, 7, 5, 1, 1, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [50, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_49(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [5, 2, 10, 3, 9, 3, 4, 14, 1, 17, 13, 1, 7, 5, 1, 1, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [50, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_50(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 2, 10, 4, 10, 1, 4, 14, 1, 17, 13, 1, 7, 5, 1, 1, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [50, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_51(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [6, 3, 11, 5, 11, 2, 5, 15, 2, 1, 13, 2, 8, 6, 2, 2, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [50, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_52(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 3, 11, 5, 11, 2, 5, 15, 2, 1, 13, 2, 8, 7, 3, 3, 2, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [50, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_53(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 3, 11, 5, 11, 2, 5, 15, 2, 1, 13, 2, 8, 7, 3, 4, 1, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [50, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_54(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [1, 3, 12, 6, 12, 3, 1, 15, 2, 1, 13, 2, 8, 7, 3, 4, 1, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [50, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_55(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [2, 4, 13, 7, 13, 4, 2, 16, 3, 2, 1, 2, 8, 7, 3, 4, 2, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [50, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_56(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [3, 5, 14, 8, 1, 4, 2, 16, 3, 2, 2, 3, 9, 8, 4, 5, 3, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [50, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_57(self, gstate):
        """False child prevented at 9"""
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [3, 5, 14, 8, 1, 4, 2, 16, 3, 3, 3, 1, 9, 8, 4, 5, 3, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [50, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_58(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 1, 14, 8, 1, 4, 2, 16, 3, 3, 3, 1, 9, 8, 4, 0, 4, 7]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 14]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_59(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [4, 1, 14, 8, 1, 4, 2, 16, 0, 4, 1, 1, 9, 8, 4, 0, 4, 7]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 18]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_60(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 1, 14, 9, 0, 4, 2, 16, 0, 4, 1, 1, 9, 8, 4, 0, 4, 7]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 18]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_61(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 1, 14, 9, 0, 4, 2, 16, 0, 4, 1, 2, 10, 9, 5, 1, 5, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 18]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_62(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [4, 1, 14, 9, 0, 5, 1, 16, 0, 4, 1, 2, 10, 9, 5, 1, 5, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 18]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_63(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 1, 14, 9, 0, 0, 2, 17, 1, 5, 2, 3, 11, 1, 5, 1, 5, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_64(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [4, 1, 14, 9, 0, 1, 1, 17, 1, 5, 2, 3, 11, 1, 5, 1, 5, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_65(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 1, 14, 9, 0, 1, 1, 17, 1, 5, 2, 3, 11, 1, 5, 1, 6, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_66(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 2, 1, 9, 0, 1, 1, 18, 2, 6, 3, 4, 12, 2, 6, 2, 7, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_67(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 2, 1, 9, 0, 1, 1, 18, 2, 7, 4, 5, 13, 3, 1, 2, 7, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_68(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [5, 2, 1, 9, 0, 1, 1, 19, 1, 7, 4, 5, 13, 3, 1, 2, 7, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_69(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [5, 2, 1, 9, 0, 1, 1, 20, 2, 8, 1, 5, 13, 3, 1, 2, 7, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_70(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 2, 1, 9, 0, 1, 1, 20, 2, 8, 1, 5, 13, 3, 2, 3, 8, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_71(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 1, 9, 0, 1, 1, 20, 2, 8, 1, 5, 13, 3, 2, 3, 9, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_72(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [1, 2, 1, 9, 0, 1, 1, 21, 1, 8, 1, 5, 13, 3, 2, 3, 9, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_73(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [1, 2, 2, 10, 1, 2, 2, 22, 2, 1, 1, 5, 13, 3, 2, 3, 9, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_74(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 1, 2, 10, 1, 2, 2, 22, 2, 1, 1, 5, 13, 3, 2, 3, 9, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_75(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [2, 1, 2, 10, 1, 2, 2, 23, 3, 2, 2, 1, 13, 3, 2, 3, 9, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_76(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 0, 2, 10, 1, 2, 2, 23, 3, 2, 2, 1, 13, 3, 2, 3, 9, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_77(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 0, 2, 10, 1, 2, 2, 23, 3, 2, 2, 2, 14, 1, 2, 3, 9, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_78(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 1, 3, 1, 1, 2, 2, 23, 3, 2, 2, 2, 15, 2, 3, 4, 10, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_79(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [4, 1, 3, 1, 1, 2, 2, 24, 4, 3, 3, 3, 16, 3, 4, 5, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_80(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [4, 1, 3, 1, 1, 3, 3, 25, 1, 3, 3, 3, 16, 3, 4, 5, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_81(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 1, 3, 1, 1, 3, 3, 25, 1, 3, 3, 4, 17, 1, 4, 5, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_82(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 0, 3, 1, 1, 3, 3, 25, 1, 3, 3, 4, 17, 1, 4, 5, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_83(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [5, 0, 3, 1, 1, 3, 3, 25, 1, 3, 3, 5, 18, 2, 5, 1, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_84(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 0, 3, 1, 1, 3, 3, 25, 1, 3, 3, 5, 18, 2, 0, 2, 2, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [62, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_85(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 3, 1, 1, 3, 3, 25, 1, 3, 3, 5, 19, 1, 0, 2, 2, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [62, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_86(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 4, 0, 1, 3, 3, 25, 1, 3, 3, 5, 19, 1, 0, 2, 2, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [62, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_87(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 4, 0, 1, 3, 3, 25, 1, 3, 3, 5, 20, 0, 0, 2, 2, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [62, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_88(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 4, 0, 1, 3, 3, 25, 1, 3, 3, 5, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_89(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 0, 4, 0, 1, 3, 3, 26, 2, 1, 3, 5, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_90(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 4, 1, 0, 3, 3, 26, 2, 1, 3, 5, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_91(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 0, 4, 1, 0, 3, 3, 26, 3, 0, 3, 5, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_92(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 4, 2, 1, 1, 3, 26, 3, 0, 3, 5, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 24]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_93(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 0, 4, 2, 1, 1, 3, 26, 0, 1, 1, 5, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_94(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 5, 1, 1, 1, 3, 26, 0, 1, 1, 5, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_95(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 5, 1, 1, 1, 3, 27, 1, 2, 2, 1, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_96(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 0, 5, 1, 1, 1, 3, 28, 0, 2, 2, 1, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_97(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 5, 1, 1, 1, 3, 28, 0, 2, 3, 0, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_98(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 5, 2, 0, 1, 3, 28, 0, 2, 3, 0, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_99(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 0, 5, 2, 0, 1, 3, 28, 1, 3, 1, 0, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_100(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 0, 5, 2, 0, 1, 3, 29, 0, 3, 1, 0, 20, 0, 0, 2, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_101(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 5, 2, 0, 1, 3, 29, 0, 3, 1, 0, 20, 0, 0, 3, 1, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_102(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 5, 2, 1, 0, 3, 29, 0, 3, 1, 0, 20, 0, 0, 3, 1, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_103(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 6, 3, 2, 1, 4, 30, 1, 4, 2, 2, 2, 1, 1, 4, 2, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_104(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 6, 4, 1, 1, 4, 30, 1, 4, 2, 2, 2, 1, 1, 4, 2, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_105(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 6, 4, 1, 1, 4, 30, 1, 4, 2, 2, 2, 2, 0, 4, 2, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_106(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [1, 1, 6, 4, 1, 1, 4, 31, 0, 4, 2, 2, 2, 2, 0, 4, 2, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_107(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 6, 4, 1, 1, 4, 31, 0, 4, 2, 2, 2, 2, 0, 5, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_108(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 6, 4, 1, 1, 4, 31, 0, 4, 2, 2, 2, 2, 0, 5, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_109(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [2, 0, 6, 4, 1, 1, 4, 31, 0, 5, 1, 2, 2, 2, 0, 5, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_110(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 0, 6, 4, 2, 0, 4, 31, 0, 5, 1, 2, 2, 2, 0, 5, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_111(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [2, 0, 6, 4, 2, 1, 5, 32, 1, 1, 1, 2, 2, 2, 0, 5, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_112(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 0, 6, 4, 2, 1, 5, 32, 1, 1, 1, 2, 2, 2, 0, 5, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_113(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 6, 4, 2, 1, 5, 32, 1, 1, 1, 2, 2, 2, 0, 6, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_114(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 7, 1, 2, 1, 5, 32, 1, 1, 1, 2, 2, 2, 0, 6, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_115(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [2, 1, 7, 1, 2, 1, 5, 32, 1, 2, 0, 2, 2, 2, 0, 6, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_116(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 1, 7, 2, 1, 1, 5, 32, 1, 2, 0, 2, 2, 2, 0, 6, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_117(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 1, 7, 2, 1, 1, 5, 32, 1, 2, 1, 3, 3, 3, 1, 1, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_118(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 1, 7, 2, 2, 0, 5, 32, 1, 2, 1, 3, 3, 3, 1, 1, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_119(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [2, 1, 7, 2, 2, 0, 5, 32, 2, 1, 1, 3, 3, 3, 1, 1, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_120(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 8, 1, 2, 0, 5, 32, 2, 1, 1, 3, 3, 3, 1, 1, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_121(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 1, 8, 1, 2, 0, 5, 32, 2, 1, 1, 3, 3, 4, 0, 1, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_122(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [2, 1, 9, 2, 3, 1, 1, 32, 2, 1, 1, 3, 3, 4, 0, 1, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_123(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 1, 9, 2, 3, 1, 1, 32, 2, 1, 1, 3, 3, 4, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_124(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [2, 1, 9, 2, 3, 2, 0, 32, 2, 1, 1, 3, 3, 4, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_125(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [2, 1, 9, 2, 3, 2, 0, 32, 2, 2, 0, 3, 3, 4, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_126(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 0, 9, 2, 3, 2, 0, 32, 2, 2, 0, 3, 3, 4, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_127(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [3, 0, 9, 2, 3, 2, 0, 32, 2, 3, 1, 1, 3, 4, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_128(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [3, 0, 9, 2, 4, 1, 0, 32, 2, 3, 1, 1, 3, 4, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_129(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 0, 9, 2, 4, 1, 0, 32, 2, 3, 2, 2, 1, 4, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_130(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [3, 1, 10, 3, 1, 1, 0, 32, 2, 3, 2, 2, 1, 4, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_131(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 1, 10, 3, 1, 1, 0, 32, 2, 3, 3, 3, 2, 1, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_132(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 2, 11, 1, 1, 1, 0, 32, 2, 3, 3, 3, 2, 1, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_133(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [3, 2, 11, 1, 1, 1, 0, 33, 3, 1, 3, 3, 2, 1, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_134(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 2, 12, 0, 1, 1, 0, 33, 3, 1, 3, 3, 2, 1, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_135(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 2, 12, 0, 1, 1, 0, 33, 3, 1, 3, 4, 1, 1, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_136(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 1, 12, 0, 1, 1, 0, 33, 3, 1, 3, 4, 1, 1, 1, 0, 0, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_137(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 1, 12, 0, 1, 1, 0, 33, 3, 1, 3, 4, 1, 1, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_138(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 1, 12, 1, 0, 1, 0, 33, 3, 1, 3, 4, 1, 1, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_139(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [4, 1, 12, 1, 0, 1, 0, 33, 3, 1, 3, 4, 1, 2, 0, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_140(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 1, 12, 1, 0, 1, 0, 33, 3, 1, 3, 4, 1, 2, 0, 1, 2, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_141(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 12, 1, 0, 1, 0, 33, 3, 1, 3, 4, 1, 2, 0, 2, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_142(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 2, 1, 1, 0, 1, 0, 33, 3, 2, 4, 5, 2, 3, 1, 3, 2, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 28]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_143(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [2, 2, 1, 1, 0, 1, 0, 33, 0, 1, 4, 5, 2, 3, 1, 3, 2, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_144(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 1, 1, 1, 0, 1, 0, 33, 0, 1, 4, 5, 2, 3, 1, 3, 2, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_145(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 1, 1, 1, 0, 1, 0, 33, 0, 1, 4, 5, 2, 4, 2, 1, 2, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_146(self, gstate):
        """OneChild prevented child in symmetric hole @ 16."""
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 0, 1, 0, 33, 0, 1, 4, 5, 2, 4, 2, 1, 3, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_147(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 1, 0, 34, 1, 2, 5, 1, 2, 4, 2, 1, 3, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_148(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 1, 0, 0, 34, 1, 2, 5, 1, 2, 4, 2, 1, 3, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_149(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 1, 0, 0, 34, 1, 2, 5, 1, 2, 5, 1, 1, 3, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_150(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 1, 0, 0, 34, 1, 2, 5, 1, 2, 5, 1, 1, 3, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_151(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 1, 0, 0, 34, 1, 2, 5, 1, 2, 6, 0, 1, 3, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_152(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 1, 2, 0, 0, 0, 34, 1, 2, 5, 1, 2, 6, 0, 1, 3, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_153(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 2, 0, 0, 0, 34, 2, 3, 6, 2, 3, 1, 0, 1, 3, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_154(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 1, 1, 2, 0, 0, 0, 35, 1, 3, 6, 2, 3, 1, 0, 1, 3, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_155(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 2, 0, 0, 0, 35, 1, 3, 6, 2, 3, 1, 1, 2, 1, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_156(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 0, 0, 0, 35, 1, 3, 6, 2, 3, 1, 1, 2, 1, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_157(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 2, 0, 2, 0, 0, 0, 35, 1, 3, 7, 1, 3, 1, 1, 2, 1, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_158(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 0, 0, 0, 36, 0, 3, 7, 1, 3, 1, 1, 2, 1, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_159(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 0, 2, 0, 0, 0, 36, 0, 3, 8, 2, 1, 1, 1, 2, 1, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_160(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 0, 2, 0, 0, 0, 36, 0, 3, 8, 2, 1, 1, 1, 2, 1, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_161(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 0, 2, 0, 0, 0, 36, 0, 3, 8, 2, 1, 1, 2, 1, 1, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [66, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_162(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 0, 0, 0, 36, 0, 3, 8, 2, 1, 1, 2, 1, 1, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_163(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 2, 0, 0, 0, 36, 0, 3, 8, 2, 1, 2, 1, 1, 1, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_164(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 36, 0, 3, 8, 2, 1, 2, 1, 1, 1, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_165(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 36, 0, 3, 8, 2, 1, 3, 0, 1, 1, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_166(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 36, 0, 3, 8, 2, 1, 3, 0, 1, 1, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_167(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 36, 0, 3, 8, 2, 1, 3, 1, 0, 1, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_168(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 36, 0, 3, 8, 2, 1, 3, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_169(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 36, 0, 3, 8, 2, 1, 3, 1, 0, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_170(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 36, 0, 3, 8, 2, 1, 3, 1, 0, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_171(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 36, 0, 3, 8, 2, 1, 4, 0, 0, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_172(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 36, 0, 3, 8, 2, 1, 4, 0, 0, 2, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_173(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 36, 0, 3, 8, 2, 1, 4, 0, 1, 1, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_174(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 36, 0, 3, 8, 2, 1, 4, 0, 1, 1, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_175(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 1, 1, 1, 37, 1, 4, 1, 2, 1, 4, 0, 1, 1, 0]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_176(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 1, 1, 37, 1, 4, 1, 2, 1, 4, 0, 1, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_177(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 1, 1, 37, 1, 4, 1, 3, 0, 4, 0, 1, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_178(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 1, 1, 38, 0, 4, 1, 3, 0, 4, 0, 1, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_179(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 1, 1, 38, 0, 5, 0, 3, 0, 4, 0, 1, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_180(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 2, 0, 1, 38, 0, 5, 0, 3, 0, 4, 0, 1, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_181(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 2, 0, 1, 38, 0, 5, 0, 3, 0, 4, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_182(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 2, 0, 1, 38, 0, 5, 0, 3, 0, 4, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_183(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 2, 0, 1, 38, 0, 6, 1, 1, 0, 4, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_184(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 2, 0, 1, 38, 0, 6, 1, 1, 0, 4, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_185(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 3, 1, 2, 39, 1, 1, 1, 1, 0, 4, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_186(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 3, 2, 1, 39, 1, 1, 1, 1, 0, 4, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_187(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 3, 2, 1, 39, 1, 1, 2, 0, 0, 4, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_188(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 3, 2, 1, 39, 1, 1, 2, 0, 0, 4, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_189(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 3, 2, 1, 39, 1, 1, 3, 1, 1, 1, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_190(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 1, 1, 1, 2, 1, 39, 1, 1, 3, 1, 1, 1, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_191(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 2, 1, 1, 1, 2, 1, 39, 2, 0, 3, 1, 1, 1, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_192(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 2, 1, 1, 1, 2, 1, 40, 1, 0, 3, 1, 1, 1, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_193(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 2, 1, 1, 1, 2, 1, 40, 1, 0, 4, 0, 1, 1, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_194(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 3, 0, 1, 1, 2, 1, 40, 1, 0, 4, 0, 1, 1, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_195(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 3, 0, 1, 1, 2, 1, 40, 1, 0, 4, 0, 2, 0, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_196(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 3, 0, 1, 1, 3, 0, 40, 1, 0, 4, 0, 2, 0, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_197(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 3, 0, 1, 1, 3, 0, 41, 2, 1, 1, 0, 2, 0, 1, 0, 1, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_198(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 0, 1, 1, 3, 0, 41, 2, 1, 1, 0, 2, 0, 1, 0, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_199(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 1, 3, 0, 41, 2, 1, 1, 0, 2, 1, 0, 0, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_200(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 1, 3, 0, 41, 2, 1, 1, 0, 2, 1, 0, 0, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_201(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 0, 0, 1, 1, 3, 0, 41, 2, 1, 1, 0, 3, 0, 0, 0, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_202(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 1, 3, 0, 42, 1, 1, 1, 0, 3, 0, 0, 0, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_203(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [2, 0, 0, 1, 1, 3, 0, 42, 1, 2, 0, 0, 3, 0, 0, 0, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_204(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 0, 1, 0, 1, 3, 0, 42, 1, 2, 0, 0, 3, 0, 0, 0, 1, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_205(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 0, 1, 0, 1, 3, 0, 42, 1, 2, 0, 0, 3, 0, 0, 0, 2, 1]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_206(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 3, 0, 42, 1, 2, 0, 0, 3, 0, 0, 0, 2, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_207(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 3, 0, 42, 1, 2, 1, 1, 1, 0, 0, 0, 2, 2]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_208(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 3, 0, 42, 1, 2, 1, 1, 1, 0, 0, 0, 2, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_209(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 3, 0, 42, 1, 2, 1, 1, 1, 0, 0, 1, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_210(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 3, 0, 43, 0, 2, 1, 1, 1, 0, 0, 1, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_211(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 3, 0, 43, 0, 3, 0, 1, 1, 0, 0, 1, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_212(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 3, 0, 43, 0, 3, 0, 1, 1, 0, 0, 1, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_213(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 3, 0, 43, 0, 3, 0, 1, 1, 0, 1, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_214(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 3, 0, 43, 0, 3, 0, 1, 1, 0, 1, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_215(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 3, 0, 43, 0, 3, 0, 1, 1, 1, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_216(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 3, 0, 43, 0, 3, 0, 1, 1, 1, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_217(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 3, 0, 43, 0, 3, 0, 1, 2, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_218(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 1, 1, 0, 43, 0, 3, 0, 1, 2, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_219(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 1, 1, 0, 44, 1, 1, 0, 1, 2, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_220(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 2, 0, 0, 44, 1, 1, 0, 1, 2, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_221(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 2, 0, 0, 44, 1, 1, 1, 0, 2, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_222(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 2, 0, 0, 44, 1, 1, 1, 0, 2, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_223(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 2, 0, 0, 44, 1, 2, 0, 0, 2, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_224(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 0, 1, 2, 0, 0, 44, 1, 2, 0, 0, 2, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_225(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 2, 0, 0, 44, 1, 2, 0, 1, 1, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_226(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 2, 0, 0, 44, 1, 2, 0, 1, 1, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_227(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 0, 0, 1, 2, 0, 0, 44, 1, 2, 0, 2, 0, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_228(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 0, 0, 2, 1, 0, 0, 44, 1, 2, 0, 2, 0, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_229(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [2, 0, 0, 2, 1, 0, 0, 44, 1, 2, 1, 1, 0, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_230(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 0, 0, 3, 0, 0, 0, 44, 1, 2, 1, 1, 0, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_231(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [2, 0, 0, 3, 0, 0, 0, 44, 1, 3, 0, 1, 0, 0, 0, 0, 1, 3]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_232(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 0, 0, 3, 0, 0, 0, 44, 1, 3, 0, 1, 0, 0, 0, 0, 1, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_233(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 3, 0, 0, 0, 44, 1, 3, 0, 1, 0, 0, 0, 1, 0, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_234(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 0, 0, 0, 44, 1, 3, 0, 1, 0, 0, 0, 1, 0, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_235(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 0, 0, 45, 2, 1, 0, 1, 0, 0, 0, 1, 0, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_236(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 0, 0, 0, 46, 1, 1, 0, 1, 0, 0, 0, 1, 0, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_237(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 0, 0, 46, 1, 1, 0, 1, 0, 0, 1, 0, 0, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_238(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 1, 1, 0, 0, 0, 46, 1, 1, 0, 1, 0, 0, 1, 0, 0, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_239(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [2, 0, 1, 1, 0, 0, 0, 46, 1, 1, 1, 0, 0, 0, 1, 0, 0, 4]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_240(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 46, 1, 1, 1, 0, 0, 0, 1, 0, 0, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_241(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 46, 2, 0, 1, 0, 0, 0, 1, 0, 0, 5]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_242(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 46, 2, 0, 1, 0, 0, 0, 1, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_243(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 46, 2, 1, 0, 0, 0, 0, 1, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_244(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 47, 1, 1, 0, 0, 0, 0, 1, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_245(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 47, 1, 1, 0, 0, 0, 1, 0, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_246(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 47, 1, 1, 0, 0, 0, 1, 0, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_247(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 47, 2, 0, 0, 0, 0, 1, 0, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_248(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 47, 2, 0, 0, 0, 0, 1, 0, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_249(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 47, 2, 0, 0, 0, 1, 0, 0, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_250(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 47, 2, 0, 0, 0, 1, 0, 0, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_251(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 47, 2, 0, 0, 1, 0, 0, 0, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_252(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 47, 2, 0, 0, 1, 0, 0, 0, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_253(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 47, 2, 0, 1, 0, 0, 0, 0, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_254(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 0, 0, 0, 0, 0, 47, 2, 0, 1, 0, 0, 0, 0, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_255(self, gstate):
        game = gstate.game
        cond = game.move(7)
        assert game.turn is False
        assert game.board == [2, 0, 0, 0, 0, 0, 0, 47, 2, 1, 0, 0, 0, 0, 0, 0, 0, 6]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_256(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 47, 2, 1, 0, 0, 0, 0, 0, 0, 0, 7]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_257(self, gstate):
        game = gstate.game
        cond = game.move(8)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 47, 3, 0, 0, 0, 0, 0, 0, 0, 0, 7]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [72, 32]
        assert cond is None
        gstate.cond = cond
        check_save_store(gstate)

    def test_round_1_move_258(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8]
        assert game.child == [N, N, N, N, N, N, N, T, N, N, N, N, N, N, N, N, N, F]
        assert game.store == [75, 32]
        assert cond.name == "WIN"
        gstate.cond = cond
        # don't check stores, seeds were collected
