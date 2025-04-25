# -*- coding: utf-8 -*-
"""Test urim.  The simulated games almost never end,
this does.

This test is slow but marking it as slow still almost
as long.

Round tally assert statements added for first, second
and last rounds. First is skunk 2pts for false.
Second is not a skunk 1pt for True.

Created on Fri Mar  7 10:19:47 2025
@author: Ann"""

import pytest
pytestmark = pytest.mark.integtest

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

    game, _ = man_config.make_game('./GameProps/Urim.txt')
    gstate = GameTestData(game)
    return gstate


@pytest.mark.incremental
class TestUrim:

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = True
        game.starter = True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 4, 0, 5, 5, 5, 5, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [5, 5, 1, 5, 5, 5, 5, 0, 5, 0, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 5, 1, 0, 6, 6, 6, 1, 6, 0, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 6, 2, 1, 7, 7, 6, 1, 6, 0, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [6, 6, 0, 2, 8, 7, 6, 1, 6, 0, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [6, 6, 0, 2, 8, 7, 6, 0, 7, 0, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [7, 6, 0, 2, 0, 8, 7, 1, 8, 1, 7, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [8, 7, 1, 3, 1, 8, 7, 1, 0, 2, 8, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [8, 0, 2, 4, 2, 9, 8, 2, 1, 2, 8, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [8, 0, 2, 4, 2, 9, 8, 2, 0, 3, 8, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 0, 2, 0, 3, 10, 9, 0, 0, 3, 8, 2]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [9, 0, 2, 0, 3, 10, 9, 0, 0, 0, 9, 3]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [9, 0, 0, 1, 4, 10, 9, 0, 0, 0, 9, 3]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [10, 1, 1, 2, 5, 11, 10, 1, 0, 0, 0, 4]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [10, 1, 1, 0, 6, 12, 10, 1, 0, 0, 0, 4]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [11, 2, 2, 1, 6, 12, 10, 1, 0, 0, 0, 0]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 3, 2, 7, 13, 11, 2, 1, 1, 1, 1]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 4, 4, 3, 8, 14, 0, 3, 2, 2, 2, 2]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 5, 5, 4, 9, 0, 2, 5, 0, 3, 3, 3]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 6, 5, 4, 9, 0, 2, 5, 0, 3, 0, 4]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 7, 5, 4, 0, 1, 3, 6, 1, 4, 1, 5]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [4, 7, 5, 4, 0, 1, 0, 7, 2, 5, 1, 5]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 7, 5, 0, 1, 2, 1, 8, 2, 5, 1, 5]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 8, 6, 1, 0, 2, 1, 8, 2, 5, 1, 0]
        assert game.store == [7, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 9, 7, 2, 1, 3, 1, 8, 2, 5, 1, 0]
        assert game.store == [7, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 9, 7, 2, 1, 3, 0, 9, 2, 5, 1, 0]
        assert game.store == [7, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 9, 7, 2, 1, 0, 1, 10, 0, 5, 1, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 9, 7, 2, 1, 0, 0, 11, 0, 5, 1, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 9, 0, 3, 2, 1, 1, 12, 1, 6, 1, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 9, 0, 3, 2, 1, 0, 13, 1, 6, 1, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 9, 0, 3, 2, 0, 1, 13, 1, 6, 1, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 9, 0, 3, 2, 0, 0, 14, 1, 6, 1, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 9, 0, 0, 3, 1, 1, 14, 1, 6, 1, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 9, 0, 0, 3, 1, 1, 14, 0, 7, 1, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 9, 0, 0, 3, 0, 0, 14, 0, 7, 1, 0]
        assert game.store == [12, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_37(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 10, 1, 1, 4, 1, 1, 0, 2, 9, 3, 1]
        assert game.store == [12, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_38(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 2, 5, 2, 2, 1, 3, 10, 0, 0]
        assert game.store == [18, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_39(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 2, 2, 5, 2, 2, 0, 4, 10, 0, 0]
        assert game.store == [18, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_40(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 3, 6, 2, 2, 0, 4, 10, 0, 0]
        assert game.store == [18, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_41(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 6, 2, 2, 0, 0, 11, 1, 1]
        assert game.store == [18, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_42(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 0, 3, 3, 1, 1, 12, 0, 1]
        assert game.store == [20, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_43(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 1, 4, 1, 4, 4, 2, 2, 0, 2, 2]
        assert game.store == [20, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_44(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 2, 5, 5, 0, 2, 0, 2, 2]
        assert game.store == [23, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_45(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 2, 5, 5, 0, 2, 0, 0, 3]
        assert game.store == [23, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_46(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 2, 5, 5, 0, 2, 0, 0, 3]
        assert game.store == [23, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 2, 5, 0, 1, 3, 1, 1, 4]
        assert game.store == [23, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_48(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 0, 4]
        assert game.store == [33, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_49(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 2, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_50(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 1, 2, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_51(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 2, 0, 1, 2, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_52(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 0, 1, 2, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_53(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 3, 0, 1, 2, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_54(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_55(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_56(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_57(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 3, 0, 0, 0, 1, 0, 2, 0, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_58(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 1, 0, 2, 0, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_59(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 1, 0, 2, 0, 0, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_60(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 0, 1, 2, 0, 0, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_61(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 3, 0, 0, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_62(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 3, 0, 0, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_63(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 0, 1, 1, 2, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_64(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 2, 0, 0, 0, 1, 1, 2, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_65(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 2, 0, 0, 0, 1, 0, 3, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_66(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 3, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_67(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 3, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_68(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 3, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_69(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 3, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_70(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 3, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_71(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 2, 0, 1, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_72(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 2, 0, 1, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_73(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 2, 0, 0, 1, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_74(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 2, 0, 0, 1, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_75(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 2, 0, 0, 0, 2]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_76(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 1, 2, 0, 0, 0, 2]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_77(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 1, 0, 1, 1, 0, 2]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_78(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 2]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_79(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 2]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_80(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 1, 1, 1, 0, 2]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_81(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 0, 2, 1, 0, 2]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_82(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 2]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_83(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_84(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_85(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 0, 3, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_86(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 3, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_87(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 1, 3, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_88(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 1, 3, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_89(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 1, 3, 0, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_90(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 1, 3, 0, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_91(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 1, 3, 0, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_92(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 1, 3, 0, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_93(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 2]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_94(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 2]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_95(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_96(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_97(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_98(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 2, 0, 1, 0, 1, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_99(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 2, 0, 0, 1, 1, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_100(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 2, 0, 0, 1, 1, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_101(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 2, 0, 0, 1, 0, 1, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_102(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_103(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 2, 1, 0, 1, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_104(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 2, 1, 0, 1, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_105(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 0, 0, 2, 1, 0, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_106(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 0, 0, 0, 2, 1, 0, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_107(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 0, 0, 0, 2, 1, 0, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_108(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 1, 0, 0, 2, 1, 0, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_109(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 1, 0, 0, 2, 0, 1, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_110(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 1, 0, 2, 0, 1, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_111(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 1, 0, 0, 1, 2, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_112(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 1, 0, 0, 1, 2, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_113(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 1, 0, 0, 1, 2, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_114(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 0, 1, 0, 0, 1, 2, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_115(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_116(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_117(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_118(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 2, 0, 0, 1, 0, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_119(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 2, 0, 0, 1, 0, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_120(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 2, 0, 0, 1, 0, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_121(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 0, 2, 0, 0, 1, 0, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_122(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_123(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_124(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 1, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_125(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 0, 0, 0, 2, 0, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_126(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 1, 0, 0, 2, 0, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_127(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 1, 0, 0, 2, 0, 0, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_128(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 1, 0, 0, 2, 0, 0, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_129(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 2, 0, 1, 0, 0, 0, 1, 1, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_130(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 3, 0, 1, 0, 0, 0, 1, 1, 1, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_131(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 1, 0, 0, 0, 1, 1, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_132(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 2, 1, 0, 0, 1, 1, 0, 1]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_133(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 2, 1, 0, 0, 1, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_134(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 2, 1, 0, 1, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_135(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 2, 0, 1, 1, 1, 0, 0]
        assert game.store == [33, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_136(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_137(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_138(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_139(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_140(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_141(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_142(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 1, 1]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_143(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 2]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_144(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 2]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_145(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 2]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_146(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 2]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_147(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 2]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_148(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 2]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_149(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_150(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_151(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_152(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_153(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 0, 1, 2, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_154(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 1, 2, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_155(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 1, 1]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_156(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_157(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_158(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_159(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 2]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_160(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 2]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_161(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_162(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_163(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_164(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_165(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_166(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_167(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_168(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_169(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_170(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 1, 1, 0, 1, 0]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_171(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 1, 1, 0, 0, 1]
        assert game.store == [35, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_172(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_173(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_174(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_175(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_176(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_177(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_178(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_179(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_180(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_181(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_182(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_183(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_184(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_185(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_186(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_187(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_188(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_189(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_190(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_191(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_192(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_193(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_194(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_195(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_196(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_197(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_198(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_199(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_200(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_201(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_202(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_203(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_204(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_205(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_206(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_207(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_208(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_209(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_210(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_211(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_212(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_213(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_214(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_215(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_216(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_217(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_218(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_219(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_220(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_221(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_222(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_223(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_224(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_225(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_226(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_227(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_228(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_229(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_230(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_231(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_232(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_233(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_234(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_235(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_236(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_237(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_238(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_239(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_240(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_241(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_242(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_243(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_244(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_245(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_246(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_247(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_248(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_249(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_250(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_251(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_252(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_253(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_254(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_255(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_256(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_257(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_258(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_259(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_260(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_261(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_262(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [37, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_263(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [40, 8]
        assert cond.name == "ROUND_WIN"

        assert game.rtally.round_wins == [1, 0]
        assert game.rtally.seeds == [40, 8]
        assert game.rtally.diff_sums == [32, 0]
        assert game.rtally.score == [2, 0]   # a skunk

        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 0, 5, 5, 5, 5, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 5, 4, 0, 5, 5, 5, 5, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 5, 5, 4, 0, 0, 6, 6, 6, 5, 1, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 5, 4, 0, 0, 6, 6, 6, 5, 0, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 5, 5, 0, 1, 1, 7, 7, 6, 5, 0, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 6, 6, 1, 0, 0, 7, 7, 6, 5, 0, 0]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 7, 7, 2, 1, 1, 8, 7, 6, 5, 0, 0]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 8, 8, 2, 1, 1, 8, 0, 7, 6, 1, 1]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 8, 8, 0, 2, 2, 8, 0, 7, 6, 1, 1]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 9, 9, 0, 2, 2, 0, 1, 8, 7, 2, 2]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 9, 9, 0, 2, 0, 1, 0, 8, 7, 2, 2]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 10, 10, 1, 0, 0, 1, 0, 8, 0, 3, 3]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 0, 11, 2, 1, 1, 2, 1, 9, 1, 0, 0]
        assert game.store == [10, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [4, 1, 12, 0, 0, 0, 2, 1, 0, 2, 1, 1]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_15(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 0, 13, 0, 0, 0, 2, 1, 0, 2, 1, 1]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 0, 13, 0, 0, 0, 2, 1, 0, 0, 2, 2]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 1, 0, 2, 2, 1, 3, 2, 1, 1, 3, 3]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 1, 0, 2, 2, 1, 0, 3, 2, 2, 3, 3]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_19(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 1, 0, 2, 0, 2, 1, 3, 2, 2, 3, 3]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_20(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 1, 0, 2, 0, 2, 0, 4, 2, 2, 3, 3]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_21(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 1, 0, 2, 0, 0, 1, 5, 2, 2, 3, 3]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_22(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 1, 0, 2, 0, 0, 1, 5, 0, 3, 4, 3]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_23(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 0, 1, 2, 0, 0, 1, 5, 0, 3, 4, 3]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [6, 1, 0, 2, 0, 0, 1, 5, 0, 3, 0, 4]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_25(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 1, 0, 0, 1, 1, 1, 5, 0, 3, 0, 4]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [7, 1, 0, 0, 1, 1, 1, 5, 0, 0, 1, 5]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_27(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [7, 1, 0, 0, 0, 2, 1, 5, 0, 0, 1, 5]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_28(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [7, 1, 0, 0, 0, 2, 1, 5, 0, 0, 0, 6]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_29(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [7, 1, 0, 0, 0, 0, 2, 6, 0, 0, 0, 6]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_30(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [7, 1, 0, 0, 0, 0, 0, 7, 1, 0, 0, 6]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_31(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 0, 1, 0, 0, 0, 0, 7, 1, 0, 0, 6]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [8, 1, 2, 1, 1, 1, 0, 7, 1, 0, 0, 0]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_33(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 1, 2, 0, 2, 1, 0, 7, 1, 0, 0, 0]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_34(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [8, 1, 2, 0, 2, 1, 0, 7, 0, 1, 0, 0]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_35(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [8, 1, 0, 1, 3, 1, 0, 7, 0, 1, 0, 0]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_36(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [8, 1, 0, 1, 3, 1, 0, 7, 0, 0, 1, 0]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [8, 1, 0, 1, 3, 0, 1, 7, 0, 0, 1, 0]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_38(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [8, 1, 0, 1, 3, 0, 0, 8, 0, 0, 1, 0]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_39(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 2, 4, 1, 1, 9, 1, 0, 1, 0]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_40(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 1, 2, 4, 1, 1, 9, 0, 1, 1, 0]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_41(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 1, 2, 4, 0, 0, 9, 0, 1, 1, 0]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_42(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 1, 2, 4, 0, 0, 9, 0, 1, 0, 1]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_43(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 3, 4, 0, 0, 9, 0, 1, 0, 1]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_44(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 2, 3, 4, 0, 0, 9, 0, 0, 1, 1]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_45(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 5, 1, 1, 9, 0, 0, 1, 1]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_46(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 5, 1, 0, 10, 0, 0, 1, 1]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 5, 0, 1, 10, 0, 0, 1, 1]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_48(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 5, 0, 0, 11, 0, 0, 1, 1]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_49(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 6, 0, 0, 11, 0, 0, 1, 1]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_50(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 6, 0, 0, 11, 0, 0, 0, 2]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_51(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 7, 0, 0, 11, 0, 0, 0, 2]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_52(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 8, 1, 1, 0, 1, 1, 1, 3]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_53(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 0, 2, 8, 1, 1, 0, 1, 1, 1, 3]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_54(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 0, 2, 8, 1, 1, 0, 1, 0, 2, 3]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_55(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 9, 2, 1, 0, 1, 0, 2, 3]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_56(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 9, 2, 1, 0, 1, 0, 0, 4]
        assert game.store == [12, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_57(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 0, 3, 2, 1, 2, 1, 1, 5]
        assert game.store == [12, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_58(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 0, 3, 2, 0, 3, 1, 1, 5]
        assert game.store == [12, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_59(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 0, 0, 3, 1, 0, 1, 1, 5]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_60(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 0, 0, 3, 1, 0, 1, 0, 6]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_61(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 0, 3, 1, 0, 1, 0, 6]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_62(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 3, 1, 0, 0, 1, 6]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_63(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 0, 3, 1, 0, 0, 1, 6]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_64(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 0, 0, 2, 1, 1, 1, 6]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_65(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 1, 0, 0, 2, 1, 1, 1, 6]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_66(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 0, 0, 2, 1, 1, 0, 7]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_67(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 2, 1, 1, 0, 7]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_68(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 2, 0, 2, 0, 7]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_69(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 2, 0, 2, 0, 7]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_70(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 1, 8]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_71(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 2, 0, 0, 1, 8]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_72(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 2, 0, 0, 0, 9]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_73(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 1, 2, 0, 0, 0, 9]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_74(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 3, 0, 0, 0, 9]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_75(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 3, 0, 0, 0, 9]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_76(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 9]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_77(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 9]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_78(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 10]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_79(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 10]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_80(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0, 10]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_81(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 0, 10]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_82(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 10]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_83(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 0, 2, 0, 10]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_84(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 1, 1, 2, 2, 1, 3, 0, 0]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_85(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 1, 0, 0, 2, 1, 3, 0, 0]
        assert game.store == [19, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_86(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 1, 0, 0, 2, 1, 0, 1, 1]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_87(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 0, 1, 0, 2, 1, 0, 1, 1]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_88(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 0, 1, 0, 2, 0, 1, 1, 1]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_89(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 1, 0, 1, 0, 2, 0, 1, 1, 1]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_90(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 0, 1, 0, 2, 0, 1, 0, 2]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_91(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 1, 1, 0, 2, 0, 1, 0, 2]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_92(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 1, 1, 0, 2, 0, 0, 1, 2]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_93(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 2, 0, 2, 0, 0, 1, 2]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_94(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 2, 0, 0, 1, 1, 1, 2]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_95(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 3, 1, 0, 1, 1, 1, 2]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_96(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 3, 1, 0, 0, 2, 1, 2]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_97(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 2, 1, 1, 2, 1, 2]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_98(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 2, 1, 1, 2, 1, 0]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_99(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 2, 1, 1, 2, 1, 0]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_100(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 2, 2, 2, 1, 0]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_101(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 2, 2, 2, 1, 0]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_102(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 3, 3, 1, 0]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_103(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 0, 3, 3, 1, 0]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_104(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 0, 3, 3, 0, 1]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_105(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 3, 3, 0, 1]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_106(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 0, 3, 0, 1, 2]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_107(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 0, 3, 0, 1, 2]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_108(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 2, 3]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_109(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 2, 3]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_110(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 2, 3]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_111(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 2, 3]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_112(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 2, 3]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_113(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 2, 3]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_114(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 2, 3]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_115(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 2, 2, 3]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_116(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 3, 4]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_117(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 3, 4]
        assert game.store == [19, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_118(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 3, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_119(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 0, 1, 0, 0, 0, 3, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_120(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 1, 2, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_121(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 3, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_122(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 3, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_123(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 4, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_124(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 4, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_125(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 4, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_126(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 4, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_127(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 4, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_128(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 4, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_129(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 2, 1, 1, 0, 0, 1, 0, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_130(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_131(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 2, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_132(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 2, 0, 0, 2, 0, 1, 0, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_133(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 1, 1, 2, 0, 1, 0, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_134(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 3, 0, 1, 0, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_135(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 1, 0, 3, 0, 1, 0, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_136(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 1, 0, 0, 1, 2, 1, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_137(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 1, 0, 0, 1, 2, 1, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_138(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 1, 0, 0, 0, 3, 1, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_139(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 1, 0, 0, 3, 1, 0]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_140(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 1, 0, 0, 3, 0, 1]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_141(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 0, 0, 3, 0, 1]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_142(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 1, 0, 3, 0, 1]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_143(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 1, 0, 3, 0, 1]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_144(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 0, 1, 3, 0, 1]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_145(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 0, 1]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_146(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 2]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_147(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 2]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_148(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 3]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_149(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 3]
        assert game.store == [19, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_150(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_151(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_152(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_153(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_154(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_155(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_156(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 1, 0, 1, 0, 1, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_157(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_158(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_159(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_160(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 1, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_161(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 2, 0, 1, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_162(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 2, 0, 1, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_163(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [19, 29]
        assert cond.name == "ROUND_WIN"

        assert game.rtally.round_wins == [1, 1]
        assert game.rtally.seeds == [59, 37]
        assert game.rtally.diff_sums == [32, 10]
        assert game.rtally.score == [2, 1]  # not a skunk
        gstate.cond = cond

    def test_round_3_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_3_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_2(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 5, 4, 4, 4, 0, 5, 5, 5, 1, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [6, 6, 5, 5, 4, 0, 5, 5, 5, 1, 0, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [6, 0, 6, 6, 5, 1, 6, 6, 5, 1, 0, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 1, 7, 7, 6, 0, 6, 6, 5, 1, 0, 0]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [7, 1, 0, 8, 7, 1, 7, 7, 6, 0, 0, 0]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_7(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [8, 2, 1, 8, 7, 1, 7, 7, 0, 1, 1, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 2, 1, 0, 8, 2, 8, 8, 1, 0, 0, 0]
        assert game.store == [8, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_9(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [9, 0, 0, 0, 8, 2, 0, 9, 2, 1, 1, 1]
        assert game.store == [8, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [10, 0, 0, 0, 0, 3, 1, 10, 3, 2, 2, 2]
        assert game.store == [8, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_11(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [10, 0, 0, 0, 0, 3, 1, 10, 3, 0, 3, 3]
        assert game.store == [8, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [10, 0, 0, 0, 0, 0, 2, 11, 0, 0, 3, 3]
        assert game.store == [12, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [11, 1, 1, 1, 1, 1, 3, 0, 1, 1, 4, 4]
        assert game.store == [12, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [11, 1, 1, 0, 2, 1, 3, 0, 1, 1, 4, 4]
        assert game.store == [12, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [11, 1, 1, 0, 2, 1, 0, 1, 2, 2, 4, 4]
        assert game.store == [12, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [11, 1, 1, 0, 0, 2, 1, 1, 2, 2, 4, 4]
        assert game.store == [12, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_17(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [11, 1, 1, 0, 0, 2, 1, 0, 3, 2, 4, 4]
        assert game.store == [12, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_18(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [11, 1, 0, 1, 0, 2, 1, 0, 3, 2, 4, 4]
        assert game.store == [12, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_19(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [12, 2, 1, 0, 0, 2, 1, 0, 3, 2, 4, 0]
        assert game.store == [12, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_20(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [12, 2, 0, 1, 0, 2, 1, 0, 3, 2, 4, 0]
        assert game.store == [12, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_21(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [13, 3, 1, 1, 0, 2, 1, 0, 3, 2, 0, 1]
        assert game.store == [12, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_22(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 5, 3, 2, 1, 3, 2, 1, 4, 3, 1, 2]
        assert game.store == [12, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 5, 3, 2, 1, 3, 0, 2, 5, 3, 1, 2]
        assert game.store == [12, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 4, 3, 2, 4, 1, 2, 5, 3, 1, 2]
        assert game.store == [12, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_25(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 4, 3, 2, 4, 1, 2, 0, 4, 2, 3]
        assert game.store == [12, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_26(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 5, 3, 2, 4, 1, 2, 0, 4, 2, 3]
        assert game.store == [12, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_27(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 1, 6, 3, 2, 4, 1, 2, 0, 4, 2, 0]
        assert game.store == [12, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 1, 6, 3, 2, 0, 2, 3, 1, 5, 2, 0]
        assert game.store == [12, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_29(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 1, 6, 3, 2, 0, 2, 0, 2, 6, 3, 0]
        assert game.store == [12, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 1, 0, 4, 3, 1, 3, 1, 0, 6, 3, 0]
        assert game.store == [15, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 2, 1, 5, 3, 1, 3, 1, 0, 0, 4, 1]
        assert game.store == [15, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_32(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 0, 2, 6, 3, 1, 3, 1, 0, 0, 4, 1]
        assert game.store == [15, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_33(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 2, 6, 3, 1, 3, 1, 0, 0, 4, 0]
        assert game.store == [15, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_34(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 7, 4, 1, 3, 1, 0, 0, 4, 0]
        assert game.store == [15, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_35(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 1, 7, 4, 1, 3, 1, 0, 0, 0, 1]
        assert game.store == [15, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_36(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 7, 4, 1, 3, 1, 0, 0, 0, 1]
        assert game.store == [15, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_37(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 1, 7, 4, 1, 3, 1, 0, 0, 0, 0]
        assert game.store == [15, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_38(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 1, 7, 4, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [19, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_39(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 2, 1, 7, 4, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [19, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_40(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 2, 1, 0, 5, 1, 1, 1, 2, 1, 1, 0]
        assert game.store == [19, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_41(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 5, 1, 1, 1, 0, 2, 2, 0]
        assert game.store == [19, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_42(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 2, 1, 0, 0, 2, 2, 2, 1, 0, 2, 0]
        assert game.store == [22, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_43(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 0, 2, 0, 3, 2, 0, 2, 0]
        assert game.store == [22, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_44(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 1, 0, 0, 0, 1, 0, 2, 0, 2, 0]
        assert game.store == [26, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_45(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 0, 0, 1, 0, 2, 0, 0, 1]
        assert game.store == [26, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_46(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 0, 0, 1, 0, 2, 0, 0, 1]
        assert game.store == [26, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_47(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 0, 1, 0, 0, 1, 0, 2, 0, 0, 0]
        assert game.store == [26, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_48(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 1, 0, 1, 0, 2, 0, 0, 0]
        assert game.store == [26, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_49(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0]
        assert game.store == [26, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_50(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0]
        assert game.store == [26, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_51(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 0, 1, 1, 0, 0, 0, 2, 0]
        assert game.store == [26, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_52(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [28, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_53(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_54(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_55(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [31, 17]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_4_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_4_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 0, 5, 5, 5, 5, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 4, 0, 5, 5, 5, 5, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 0, 1, 6, 6, 6, 5, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_4(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [6, 6, 5, 5, 0, 1, 6, 0, 7, 6, 5, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 7, 6, 6, 1, 2, 7, 0, 7, 6, 5, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 8, 7, 7, 1, 2, 7, 0, 7, 6, 0, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_7(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 9, 7, 7, 1, 2, 7, 0, 7, 6, 0, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 10, 8, 8, 1, 2, 7, 0, 0, 7, 1, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 10, 8, 0, 2, 3, 8, 1, 1, 8, 0, 0]
        assert game.store == [6, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_10(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 11, 9, 1, 0, 0, 8, 1, 1, 0, 1, 1]
        assert game.store == [6, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_11(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 11, 0, 2, 1, 1, 9, 2, 2, 1, 0, 0]
        assert game.store == [10, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 12, 1, 0, 1, 1, 0, 3, 3, 2, 1, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [3, 12, 1, 0, 0, 2, 0, 3, 3, 2, 1, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 12, 1, 0, 0, 2, 0, 3, 3, 0, 2, 2]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 12, 0, 1, 0, 2, 0, 3, 3, 0, 2, 2]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 12, 0, 1, 0, 2, 0, 0, 4, 1, 3, 2]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_17(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 13, 1, 2, 0, 2, 0, 0, 4, 1, 3, 2]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_18(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 13, 1, 2, 0, 2, 0, 0, 0, 2, 4, 3]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 3, 4, 1, 3, 1, 1, 1, 3, 5, 4]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_20(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 0, 3, 4, 1, 3, 0, 2, 1, 3, 5, 4]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_21(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 4, 4, 1, 3, 0, 2, 1, 3, 5, 4]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_22(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 4, 4, 1, 3, 0, 0, 2, 4, 5, 4]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 4, 4, 1, 0, 1, 1, 0, 4, 5, 4]
        assert game.store == [13, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_24(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 4, 4, 1, 0, 1, 1, 0, 0, 6, 5]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_25(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 4, 4, 0, 1, 1, 1, 0, 0, 6, 5]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 4, 4, 0, 1, 0, 2, 0, 0, 6, 5]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 5, 1, 2, 1, 2, 0, 0, 6, 5]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_28(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 5, 1, 2, 1, 0, 1, 1, 6, 5]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_29(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 5, 1, 0, 2, 1, 1, 1, 6, 5]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_30(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 5, 1, 0, 2, 1, 0, 2, 6, 5]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_31(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 5, 0, 1, 2, 1, 0, 2, 6, 5]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 1, 1, 6, 1, 1, 2, 1, 0, 2, 6, 0]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_33(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 1, 0, 2, 2, 3, 2, 1, 0, 6, 0]
        assert game.store == [16, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_34(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 2, 2, 0, 3, 2, 1, 6, 0]
        assert game.store == [16, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_35(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 1, 1, 0, 2, 0, 1, 0, 2, 1, 6, 0]
        assert game.store == [20, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_36(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 2, 2, 1, 0, 0, 1, 0, 2, 1, 0, 1]
        assert game.store == [20, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_37(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 3, 2, 0, 0, 1, 0, 2, 1, 0, 1]
        assert game.store == [20, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_38(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 3, 3, 2, 0, 0, 1, 0, 2, 1, 0, 0]
        assert game.store == [20, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_39(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 4, 3, 1, 0, 1, 0, 2, 1, 0, 0]
        assert game.store == [20, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_40(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 4, 3, 1, 0, 0, 1, 2, 1, 0, 0]
        assert game.store == [20, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_41(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 4, 2, 1, 1, 1, 2, 1, 0, 0]
        assert game.store == [20, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_42(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 4, 2, 1, 1, 0, 3, 1, 0, 0]
        assert game.store == [20, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_43(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 4, 2, 1, 1, 0, 3, 1, 0, 0]
        assert game.store == [20, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_44(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 4, 2, 1, 0, 1, 3, 1, 0, 0]
        assert game.store == [20, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_45(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 3, 2, 1, 0, 3, 1, 0, 0]
        assert game.store == [22, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_46(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 3, 2, 1, 0, 0, 2, 1, 1]
        assert game.store == [22, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_47(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 3, 2, 1, 0, 2, 1, 1]
        assert game.store == [22, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_48(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 3, 2, 1, 0, 0, 2, 2]
        assert game.store == [22, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_49(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 3, 2, 1, 0, 0, 2, 2]
        assert game.store == [22, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_50(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 3, 0, 2, 1, 0, 2, 2]
        assert game.store == [22, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_51(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_52(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_53(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_54(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_55(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_56(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 3, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_57(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 3, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_58(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 3, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_59(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 4, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_60(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 4, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_61(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 1, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_62(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 1, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_63(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 0, 2, 0, 0, 0, 1, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_64(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 0, 2, 0, 0, 0, 0, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_65(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 0, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_66(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 0, 0, 0, 2, 0, 0, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_67(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_68(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_69(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_70(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 3, 0, 0, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_71(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 3, 0, 0, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_72(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_73(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_74(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_75(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_76(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_77(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_78(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_79(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_80(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_81(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_82(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_83(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_84(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_85(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_86(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 2, 0, 1, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_87(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 2, 0, 1, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_88(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 2, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_89(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 1, 2, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_90(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 1, 2, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_91(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 1, 2, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_92(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_93(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_94(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_95(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_96(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_97(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_98(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 3]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_99(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 3]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_100(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_101(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_102(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_103(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_104(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 0, 0, 1, 0, 0, 2, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_105(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 0, 0, 1, 0, 0, 2, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_106(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 0, 0, 1, 0, 0, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_107(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 0, 0, 1, 0, 0, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_108(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_109(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_110(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 2, 0, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_111(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 2, 0, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_112(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_113(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_114(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_115(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_116(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_117(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_118(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_119(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 4, 0, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_120(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_121(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_122(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_123(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_124(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_125(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_126(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_127(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_128(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_129(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_130(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_131(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 3, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_132(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 3, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_133(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_134(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_135(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 2, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_136(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 2, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_137(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 2, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_138(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 2, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_139(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_140(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 2, 0, 0, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_141(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 1, 2, 0, 0, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_142(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_143(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_144(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 0, 2, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_145(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 0, 2, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_146(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 0, 2, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_147(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 1, 0, 0, 2, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_148(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_149(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_150(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_151(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_152(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_153(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_154(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_155(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_156(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_157(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_158(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_159(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_160(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_161(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_162(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_163(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_164(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_165(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_166(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 0, 0, 1, 0, 0, 2, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_167(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_168(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 2, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_169(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_170(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 0, 0, 0, 0, 1, 2, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_171(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 1, 0, 0, 1, 2, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_172(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_173(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_174(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_175(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_176(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_177(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_178(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_179(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_180(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 2, 0, 1, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_181(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 2, 0, 1, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_182(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_183(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_184(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_185(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_186(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_187(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_188(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 0, 0, 2, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_189(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 0, 2, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_190(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 0, 2, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_191(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 1, 0, 0, 2, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_192(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 1, 0, 2, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_193(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 1, 0, 2, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_194(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 1, 2, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_195(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 1, 2, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_196(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 2, 0, 0, 0, 1, 2, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_197(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 2, 0, 0, 0, 1, 2, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_198(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_199(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 0, 0, 3, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_200(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 2, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_201(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_202(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_203(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_204(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [33, 15]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_5_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_5_move_1(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_2(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 0, 5, 5, 1, 6, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 5, 5, 4, 0, 5, 5, 1, 0, 6, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_4(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 5, 5, 0, 1, 6, 6, 0, 0, 6, 6, 6]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 6, 6, 1, 2, 7, 6, 0, 0, 6, 6, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [7, 6, 6, 1, 2, 0, 7, 1, 1, 7, 7, 1]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_7(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [8, 6, 6, 1, 2, 0, 7, 1, 1, 7, 7, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_8(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [8, 6, 6, 1, 0, 1, 8, 1, 1, 7, 7, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [9, 7, 7, 2, 1, 0, 8, 1, 1, 7, 0, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [9, 7, 7, 2, 0, 1, 8, 1, 1, 7, 0, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [9, 7, 7, 2, 0, 1, 8, 1, 0, 8, 0, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [9, 7, 7, 2, 0, 0, 9, 1, 0, 8, 0, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [9, 7, 7, 2, 0, 0, 9, 0, 1, 8, 0, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 8, 8, 3, 1, 1, 10, 1, 2, 9, 0, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 9, 9, 0, 0, 1, 0, 2, 3, 10, 1, 2]
        assert game.store == [2, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 9, 0, 1, 1, 2, 1, 3, 4, 11, 0, 0]
        assert game.store == [7, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_17(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 9, 0, 1, 1, 2, 1, 0, 5, 12, 1, 0]
        assert game.store == [7, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 2, 2, 3, 2, 1, 6, 13, 0, 0]
        assert game.store == [9, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 1, 0, 2, 2, 3, 2, 1, 0, 14, 1, 1]
        assert game.store == [9, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_20(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 2, 2, 3, 2, 1, 0, 14, 1, 1]
        assert game.store == [9, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_21(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 1, 2, 2, 3, 0, 2, 1, 14, 1, 1]
        assert game.store == [9, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_22(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 1, 2, 2, 0, 1, 0, 0, 14, 1, 1]
        assert game.store == [14, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_23(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 3, 2, 3, 3, 1, 2, 1, 1, 0, 3, 3]
        assert game.store == [14, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 3, 4, 4, 1, 2, 1, 1, 0, 3, 3]
        assert game.store == [14, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_25(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 4, 4, 1, 2, 1, 1, 0, 3, 0]
        assert game.store == [14, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_26(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 0, 4, 0, 2, 0, 0, 0, 0, 3, 0]
        assert game.store == [21, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_27(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 4, 0, 2, 0, 0, 0, 0, 0, 1]
        assert game.store == [21, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_28(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 3, 1, 1, 0, 0, 0, 1]
        assert game.store == [21, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_29(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 3, 0, 2, 0, 0, 0, 1]
        assert game.store == [21, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_30(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 4, 0, 2, 0, 0, 0, 1]
        assert game.store == [21, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_31(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 4, 0, 2, 0, 0, 0, 0]
        assert game.store == [21, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 4, 0, 2, 0, 0, 0, 0]
        assert game.store == [21, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_33(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 4, 0, 0, 1, 1, 0, 0]
        assert game.store == [21, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_34(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_35(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_36(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_37(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_38(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_39(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_40(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_41(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_42(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_43(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_44(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_45(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_46(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_48(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_49(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_50(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_51(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_52(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_53(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_54(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_55(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_56(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_57(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_58(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_59(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_60(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_61(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_62(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_63(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_64(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_65(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_66(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_67(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_68(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_69(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_70(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_71(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_72(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_73(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_74(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_75(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_76(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_77(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_78(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_79(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_80(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_81(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_82(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_83(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_84(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_85(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_86(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_87(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_88(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_89(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_90(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_91(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_92(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_93(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_94(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_95(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_96(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_97(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_98(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_99(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_100(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_101(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_102(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_103(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_104(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_105(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_106(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_107(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_108(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_109(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_110(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_111(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_112(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_113(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_114(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_115(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_116(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_117(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_118(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [25, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_119(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 20]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_6_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_6_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 4, 4, 0, 5, 5, 5, 5, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 5, 1, 5, 5, 5, 5, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 0, 6, 2, 6, 6, 6, 5, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [6, 1, 7, 2, 6, 6, 6, 5, 4, 4, 0, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_5(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [6, 1, 7, 2, 6, 0, 7, 6, 5, 5, 1, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [7, 0, 7, 2, 6, 0, 0, 7, 6, 6, 2, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_7(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 8, 3, 7, 1, 1, 8, 6, 6, 2, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_8(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 8, 3, 7, 1, 1, 8, 6, 6, 0, 2]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 8, 3, 0, 2, 2, 9, 7, 7, 1, 0]
        assert game.store == [5, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 2, 9, 0, 0, 2, 2, 9, 0, 8, 2, 1]
        assert game.store == [5, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_11(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 10, 0, 0, 2, 2, 9, 0, 8, 2, 1]
        assert game.store == [5, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_12(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 3, 10, 0, 0, 2, 2, 9, 0, 8, 0, 2]
        assert game.store == [5, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_13(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 4, 10, 0, 0, 2, 2, 9, 0, 8, 0, 2]
        assert game.store == [5, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 5, 11, 1, 1, 0, 2, 9, 0, 0, 1, 3]
        assert game.store == [5, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_15(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 5, 11, 1, 0, 1, 2, 9, 0, 0, 1, 3]
        assert game.store == [5, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 6, 12, 2, 1, 1, 2, 0, 1, 1, 2, 4]
        assert game.store == [5, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 7, 0, 4, 2, 2, 3, 1, 2, 2, 3, 5]
        assert game.store == [5, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_18(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 7, 0, 4, 2, 2, 3, 1, 0, 3, 4, 5]
        assert game.store == [5, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 0, 1, 5, 3, 3, 4, 2, 1, 3, 4, 5]
        assert game.store == [5, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_20(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 1, 2, 6, 0, 3, 4, 2, 1, 3, 4, 0]
        assert game.store == [5, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 1, 2, 0, 1, 4, 5, 0, 0, 0, 4, 0]
        assert game.store == [14, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 0, 0, 0, 1, 4, 5, 0, 0, 0, 0, 1]
        assert game.store == [14, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_23(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 1]
        assert game.store == [14, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_24(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0]
        assert game.store == [14, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_25(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 1, 6, 6, 0, 0, 0, 0, 0]
        assert game.store == [14, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 1, 6, 0, 1, 1, 1, 1, 1]
        assert game.store == [14, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_27(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_29(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 0, 2, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_30(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_31(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 0, 2, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 0, 2, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_33(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_34(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 2, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_35(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_36(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 0, 2, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_37(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 3, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_38(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 3, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_39(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_40(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 1, 0, 2, 0, 0, 0, 1]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_41(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 2, 0, 2, 0, 0, 0, 1]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_42(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 2, 0, 0, 1, 1, 0, 1]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_43(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 2, 0, 0, 1, 1, 0, 1]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_44(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 2, 0, 0, 0, 2, 0, 1]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_45(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 2, 0, 0, 0, 2, 0, 1]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_46(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 2, 0, 0, 0, 2, 0, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_47(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_48(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 1]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_49(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_50(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 2]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_51(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 2]
        assert game.store == [24, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_52(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_53(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_54(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_55(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_56(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 2, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_57(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 2, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_58(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_59(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_60(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_61(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_62(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_63(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_64(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_65(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_66(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_67(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_68(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_69(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_70(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_71(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_72(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_73(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_74(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_75(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_76(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_77(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_78(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_79(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_80(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_81(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_82(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_83(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_84(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_85(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_86(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_87(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_88(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_89(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_90(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_91(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_92(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_93(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_94(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_95(self, gstate):
        game = gstate.game
        #  GRANDSLAM: no capture

        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_96(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_97(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_98(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_99(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_100(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_101(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_102(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_103(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_104(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_105(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [24, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_106(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 20]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_7_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_7_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 5, 4, 0, 5, 5, 5, 5, 4, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 6, 5, 1, 6, 5, 5, 5, 4, 0, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_4(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [6, 6, 5, 1, 0, 6, 6, 6, 5, 1, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_5(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 6, 5, 1, 0, 6, 6, 6, 5, 0, 7, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [6, 6, 5, 1, 0, 0, 7, 7, 6, 1, 8, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_7(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [7, 7, 6, 1, 0, 0, 7, 7, 0, 2, 9, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 7, 6, 0, 1, 0, 7, 7, 0, 2, 9, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [8, 8, 7, 1, 2, 1, 8, 8, 0, 2, 0, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_10(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [8, 8, 0, 2, 3, 2, 9, 9, 1, 0, 0, 3]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_11(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [9, 9, 1, 0, 0, 2, 9, 0, 2, 1, 1, 4]
        assert game.store == [3, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [9, 9, 0, 1, 0, 2, 9, 0, 2, 1, 1, 4]
        assert game.store == [3, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_13(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [10, 10, 1, 0, 0, 2, 9, 0, 2, 1, 1, 0]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 11, 2, 1, 1, 3, 10, 1, 0, 0, 0, 0]
        assert game.store == [10, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 12, 0, 0, 0, 3, 0, 2, 1, 1, 1, 1]
        assert game.store == [10, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 12, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1]
        assert game.store == [15, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_17(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 12, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0]
        assert game.store == [15, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1]
        assert game.store == [15, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 1, 1, 0, 2, 2, 2, 2, 1]
        assert game.store == [15, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_20(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 2, 1, 1, 1, 0, 2, 2, 2, 2, 1]
        assert game.store == [15, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 2, 1, 1, 1, 0, 2, 0, 3, 3, 1]
        assert game.store == [15, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_22(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 2, 1, 0, 2, 0, 3, 3, 1]
        assert game.store == [15, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_23(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 2, 1, 0, 2, 0, 3, 0, 2]
        assert game.store == [15, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_24(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 2, 1, 2, 0, 3, 0, 2]
        assert game.store == [15, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_25(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 2, 1, 0, 1, 4, 0, 2]
        assert game.store == [15, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 0, 2, 1, 1, 4, 0, 2]
        assert game.store == [15, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 0, 2, 1, 0, 5, 0, 2]
        assert game.store == [15, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_28(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 1, 2, 1, 0, 5, 0, 2]
        assert game.store == [15, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_29(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 1, 2, 0, 1, 5, 0, 2]
        assert game.store == [15, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_30(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 1, 5, 0, 2]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_32(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_33(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_34(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 2, 0, 0, 0, 0, 1, 1, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_35(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 2, 0, 0, 0, 0, 0, 2, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_36(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 0, 1, 1, 0, 0, 0, 2, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 0, 1, 0, 1, 0, 0, 2, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_38(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 1, 0, 0, 1, 0, 1, 0, 0, 2, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_39(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 0, 1, 0, 0, 1, 0, 0, 1, 0, 2, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_40(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 0, 1, 0, 0, 0, 1, 0, 1, 0, 2, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_41(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 0, 1, 0, 0, 0, 0, 1, 1, 0, 2, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_42(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 0, 0, 0, 1, 1, 0, 2, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_43(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 0, 0, 1, 0, 0, 0, 1, 0, 1, 2, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_44(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 0, 0, 0, 1, 0, 0, 1, 0, 1, 2, 3]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_45(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 4]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_46(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 4]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_47(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_48(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_49(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 0, 0, 2, 0, 1, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_50(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 1, 0, 0, 0, 2, 0, 1, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_51(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 0, 0, 0, 2, 0, 0, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_52(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 2, 1, 0, 0, 0, 2, 0, 0, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_53(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 2, 1, 0, 0, 0, 0, 1, 1, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_54(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 1, 0, 0, 0, 1, 1, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_55(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 2, 0, 1, 0, 0, 0, 1, 1, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_56(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 0, 1, 0, 0, 1, 1, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_57(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 2, 0, 0, 1, 0, 0, 0, 2, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_58(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 0, 0, 1, 0, 0, 2, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_59(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 2, 0, 0, 0, 1, 0, 0, 0, 1, 2]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_60(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 1, 2]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_61(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 3, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_62(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 3, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_63(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 3, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_64(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_65(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_66(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 1, 1, 0, 1, 0, 0, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_67(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 1, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_68(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 1, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_69(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 1, 1, 0, 0, 0, 1, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_70(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 1, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_71(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 1, 0, 0, 1, 0, 1, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_72(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 0, 1, 0, 1, 0, 1, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_73(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 3, 0, 1, 0, 1, 0, 1, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_74(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 3, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_75(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 3, 0, 0, 0, 2, 0, 1, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_76(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 3, 0, 0, 0, 2, 0, 1, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_77(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 3, 0, 0, 0, 0, 1, 2, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_78(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 1, 1, 0, 1, 2, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_79(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 1, 0, 1, 1, 2, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_80(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 1, 0, 1, 1, 2, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_81(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 1, 0, 1, 0, 3, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_82(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 1, 1, 0, 3, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_83(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_84(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_85(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_86(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_87(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_88(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_89(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 2]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_90(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 1, 0, 1, 0, 0, 1, 0, 2]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_91(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 1, 0, 1, 0, 0, 0, 1, 2]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_92(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 1, 2]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_93(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 1, 0, 1, 0, 0, 1, 2]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_94(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 0, 1, 1, 0, 0, 1, 2]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_95(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 1, 2]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_96(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 1, 2]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_97(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 1, 2]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_98(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 1, 2]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_99(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 3, 0, 0, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_100(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 3, 0, 0, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_101(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 0, 1, 1, 2, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_102(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 2, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_103(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 0, 2, 2, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_104(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 1, 0, 0, 2, 2, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_105(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 0, 1, 0, 0, 2, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_106(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 0, 1, 0, 0, 2, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_107(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 1, 0, 2, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_108(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 1, 0, 2, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_109(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 1, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_110(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 2, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_111(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 2, 0, 0, 0, 1, 2, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_112(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 2, 0, 0, 0, 1, 2, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_113(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 2, 0, 0, 0, 0, 3, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_114(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 0, 3, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_115(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 1, 0, 1, 0, 3, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_116(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 1, 0, 3, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_117(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_118(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_119(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_120(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_121(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 3, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_122(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 3, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_123(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_124(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 3, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_125(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 3, 0, 1, 0, 0, 1, 0, 0, 0, 2, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_126(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 1, 0, 1, 0, 0, 0, 2, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_127(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 3, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_128(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 4, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_129(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 4, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_130(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 2, 1, 0, 1, 0, 0, 0, 1]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_131(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 2, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_132(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 2, 1, 1, 0, 0, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_133(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 2, 0, 2, 0, 0, 0, 0]
        assert game.store == [18, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_134(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_135(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_136(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_137(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_138(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_139(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_140(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_141(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_142(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_143(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_144(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [21, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_145(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [25, 23]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_8_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_8_move_1(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 6, 5, 5, 5, 4, 4, 4, 4, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 7, 5, 5, 5, 4, 4, 4, 4, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_4(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 7, 5, 5, 5, 4, 4, 0, 5, 1, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_5(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 7, 5, 5, 5, 0, 5, 1, 6, 0, 6, 6]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 7, 5, 5, 5, 0, 0, 2, 7, 1, 7, 7]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 7, 0, 6, 6, 1, 1, 0, 7, 1, 7, 7]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 8, 1, 7, 7, 2, 2, 0, 7, 1, 7, 0]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 8, 1, 0, 8, 3, 3, 1, 8, 2, 8, 0]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 9, 2, 1, 9, 3, 3, 1, 0, 3, 9, 1]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_11(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 10, 3, 1, 9, 3, 3, 1, 0, 3, 9, 1]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_12(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 10, 3, 1, 9, 3, 3, 1, 0, 3, 9, 0]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 10, 0, 2, 10, 4, 3, 1, 0, 3, 9, 0]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_14(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 11, 1, 3, 11, 5, 4, 2, 0, 3, 0, 1]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_15(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [3, 12, 2, 4, 0, 6, 5, 3, 1, 4, 1, 2]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 12, 2, 4, 0, 6, 0, 4, 2, 5, 2, 3]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [3, 12, 2, 4, 0, 0, 1, 5, 3, 6, 0, 0]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_18(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 12, 2, 4, 0, 0, 1, 0, 4, 7, 1, 1]
        assert game.store == [12, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 4, 5, 1, 1, 2, 1, 5, 8, 2, 2]
        assert game.store == [12, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_20(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 4, 5, 1, 1, 0, 2, 6, 8, 2, 2]
        assert game.store == [12, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 4, 0, 2, 2, 1, 3, 7, 8, 2, 2]
        assert game.store == [12, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_22(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 1, 5, 1, 0, 0, 1, 3, 7, 0, 3, 3]
        assert game.store == [12, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_23(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 1, 0, 2, 1, 1, 0, 0, 7, 0, 3, 3]
        assert game.store == [18, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_24(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 2, 1, 2, 1, 1, 0, 0, 7, 0, 3, 0]
        assert game.store == [18, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_25(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 0, 2, 3, 1, 1, 0, 0, 7, 0, 3, 0]
        assert game.store == [18, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_26(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [4, 1, 0, 0, 1, 1, 0, 0, 0, 1, 4, 1]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_27(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 1, 0, 0, 1, 0, 1, 0, 0, 1, 4, 1]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_28(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 1, 0, 0, 1, 0, 1, 0, 0, 0, 5, 1]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_29(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 1, 0, 0, 0, 1, 1, 0, 0, 0, 5, 1]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_30(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 2, 1, 1, 0, 1, 1, 0, 0, 0, 0, 2]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_31(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 0, 2, 2, 0, 1, 1, 0, 0, 0, 0, 2]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_32(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 0, 2, 2, 0, 1, 0, 1, 0, 0, 0, 2]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_33(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 3, 3, 1, 2, 0, 1, 0, 0, 0, 2]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_34(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 3, 3, 1, 2, 0, 1, 0, 0, 0, 0]
        assert game.store == [18, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_35(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 4, 2, 3, 0, 1, 0, 0, 0, 0]
        assert game.store == [18, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_36(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 4, 2, 3, 0, 0, 1, 0, 0, 0]
        assert game.store == [18, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 4, 2, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [20, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_38(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 4, 2, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [20, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_39(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 3, 1, 2, 1, 1, 0, 0, 0]
        assert game.store == [20, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_40(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 3, 1, 2, 0, 2, 0, 0, 0]
        assert game.store == [20, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_41(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0]
        assert game.store == [23, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_42(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 3, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [23, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_43(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [23, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_44(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 3, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [23, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_45(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 2, 0]
        assert game.store == [23, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_46(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 2, 0]
        assert game.store == [23, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_48(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_49(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_50(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_51(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_52(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_53(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_54(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_55(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_56(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_57(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_58(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [29, 19]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_9_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_9_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 4, 0, 5, 5, 5, 1, 5, 5, 5, 5, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [5, 4, 0, 5, 5, 5, 1, 0, 6, 6, 6, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 4, 0, 5, 5, 0, 2, 1, 7, 7, 7, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_5(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 4, 0, 5, 5, 0, 0, 2, 8, 7, 7, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_6(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 4, 0, 5, 0, 1, 1, 3, 9, 8, 7, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 5, 1, 6, 1, 0, 1, 3, 9, 0, 8, 6]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_8(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [6, 0, 2, 7, 2, 1, 0, 3, 9, 0, 8, 6]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 1, 3, 8, 0, 0, 0, 3, 9, 0, 8, 0]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 1, 3, 0, 1, 1, 1, 4, 10, 1, 9, 1]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_11(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [7, 1, 3, 0, 1, 1, 1, 0, 11, 2, 10, 2]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_12(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 0, 4, 0, 1, 1, 1, 0, 11, 2, 10, 2]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_13(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [7, 0, 4, 0, 1, 1, 0, 1, 11, 2, 10, 2]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [7, 0, 4, 0, 1, 0, 1, 1, 11, 2, 10, 2]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [7, 0, 4, 0, 1, 0, 0, 2, 11, 2, 10, 2]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 5, 1, 2, 1, 1, 0, 11, 2, 10, 2]
        assert game.store == [5, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_17(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 5, 1, 2, 1, 1, 0, 11, 2, 10, 0]
        assert game.store == [5, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_18(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 5, 1, 2, 1, 1, 0, 11, 2, 10, 0]
        assert game.store == [5, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 5, 1, 2, 1, 0, 1, 11, 2, 10, 0]
        assert game.store == [5, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_20(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 3, 2, 1, 0, 11, 2, 10, 0]
        assert game.store == [7, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_21(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 2, 3, 2, 0, 1, 11, 2, 10, 0]
        assert game.store == [7, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_22(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 0, 3, 1, 0, 11, 2, 10, 0]
        assert game.store == [9, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_23(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 1, 3, 1, 4, 2, 1, 0, 3, 11, 1]
        assert game.store == [9, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_24(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 1, 3, 1, 0, 3, 2, 1, 0, 11, 1]
        assert game.store == [13, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_25(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 2, 1, 3, 1, 0, 3, 0, 2, 1, 11, 1]
        assert game.store == [13, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_26(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 2, 1, 3, 0, 1, 3, 0, 2, 1, 11, 1]
        assert game.store == [13, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_27(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 2, 1, 3, 0, 1, 0, 1, 3, 2, 11, 1]
        assert game.store == [13, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_28(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 2, 1, 0, 1, 2, 1, 1, 3, 2, 11, 1]
        assert game.store == [13, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_29(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 1, 2, 1, 1, 0, 3, 12, 2]
        assert game.store == [13, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_30(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 1, 0, 1, 2, 1, 1, 0, 3, 12, 2]
        assert game.store == [13, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 3, 1, 0, 1, 2, 1, 1, 0, 0, 13, 3]
        assert game.store == [13, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_32(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 1, 2, 2, 1, 1, 0, 0, 13, 3]
        assert game.store == [13, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_33(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 2, 2, 0, 2, 0, 0, 13, 3]
        assert game.store == [13, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_34(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 2, 1, 2, 0, 1, 0, 0, 0, 13, 3]
        assert game.store == [16, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_35(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 2, 0, 0, 1, 0, 0, 13, 3]
        assert game.store == [16, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_36(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 3, 0, 0, 1, 0, 0, 13, 3]
        assert game.store == [16, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_37(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 1, 1, 2, 3, 0, 0, 1, 0, 0, 13, 0]
        assert game.store == [16, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_38(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 1, 0, 4, 1, 0, 1, 0, 0, 13, 0]
        assert game.store == [16, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_39(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 4, 1, 0, 0, 1, 0, 13, 0]
        assert game.store == [16, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_40(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 1, 1, 0, 0, 2, 1, 1, 0, 0, 13, 0]
        assert game.store == [18, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_41(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 0, 2, 0, 2, 0, 0, 13, 0]
        assert game.store == [18, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_42(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 1, 1, 0, 0, 0, 1, 0, 0, 0, 13, 0]
        assert game.store == [21, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_43(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 2, 1, 1, 1, 2, 1, 1, 1, 0, 2]
        assert game.store == [21, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_44(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 3, 2, 1, 1, 2, 1, 1, 1, 0, 2]
        assert game.store == [21, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_45(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 3, 2, 1, 1, 0, 2, 2, 1, 0, 2]
        assert game.store == [21, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_46(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 2, 2, 0, 2, 2, 1, 0, 2]
        assert game.store == [21, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_47(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 2, 2, 0, 0, 3, 2, 0, 2]
        assert game.store == [21, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_48(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 0, 3, 1, 0, 3, 2, 0, 2]
        assert game.store == [21, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_49(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 0, 3, 1, 0, 0, 3, 1, 3]
        assert game.store == [21, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_50(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 4, 0, 0, 0, 3, 1, 3]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_51(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 4, 0, 0, 0, 0, 2, 4]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_52(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 4, 0, 0, 0, 0, 2, 4]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_53(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 4, 0, 0, 0, 0, 0, 5]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_54(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_55(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 2, 1, 1, 1, 5, 0, 0, 0, 0, 0, 0]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_56(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_57(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 2, 1, 1, 1, 0, 1, 1, 1, 0, 2, 0]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_58(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 2, 1, 1, 0, 1, 1, 1, 0, 2, 0]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_59(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 3, 2, 1, 1, 0, 1, 1, 1, 0, 0, 1]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_60(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 3, 2, 2, 0, 1, 1, 1, 0, 0, 1]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_61(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 3, 2, 2, 0, 1, 1, 0, 1, 0, 1]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_62(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 3, 0, 3, 1, 1, 1, 0, 1, 0, 1]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_63(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 3, 0, 3, 1, 0, 2, 0, 1, 0, 1]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_64(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 4, 2, 0, 2, 0, 1, 0, 1]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_65(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 4, 2, 0, 0, 1, 2, 0, 1]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_66(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 4, 2, 0, 0, 1, 2, 0, 1]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_67(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 4, 2, 0, 0, 1, 0, 1, 2]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_68(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 3, 1, 1, 0, 0, 1, 2]
        assert game.store == [25, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_69(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 3, 1, 1, 0, 0, 1, 0]
        assert game.store == [25, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_70(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 2, 2, 1, 0, 1, 0]
        assert game.store == [25, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_71(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 3, 2, 0, 1, 0]
        assert game.store == [25, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_72(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 3, 2, 0, 1, 0]
        assert game.store == [25, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_73(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 3, 1, 2, 0]
        assert game.store == [25, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_74(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 3, 1, 2, 0]
        assert game.store == [25, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_75(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 2, 3, 1]
        assert game.store == [25, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_76(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 3, 1]
        assert game.store == [25, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_77(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 4, 2]
        assert game.store == [25, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_78(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 4, 2]
        assert game.store == [25, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_79(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 4, 2]
        assert game.store == [25, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_80(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 4, 2]
        assert game.store == [25, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_81(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_82(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_83(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 3]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_84(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 3]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_85(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_86(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_87(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_88(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_89(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_90(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_91(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_92(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [25, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_93(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [29, 19]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_10_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_10_move_1(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 0, 5, 5, 5, 5, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_2(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [5, 4, 4, 4, 0, 5, 5, 0, 6, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 4, 4, 0, 1, 6, 6, 1, 6, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 5, 5, 1, 0, 6, 6, 1, 6, 5, 5, 0]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_5(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [6, 5, 5, 1, 0, 0, 7, 2, 7, 6, 6, 1]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [7, 6, 6, 0, 0, 0, 7, 2, 7, 0, 7, 2]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 0, 7, 1, 1, 1, 8, 0, 7, 0, 7, 2]
        assert game.store == [3, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_8(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [8, 1, 8, 0, 0, 0, 8, 0, 7, 0, 0, 3]
        assert game.store == [3, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [8, 0, 9, 0, 0, 0, 8, 0, 7, 0, 0, 3]
        assert game.store == [3, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [9, 1, 10, 0, 0, 0, 8, 0, 7, 0, 0, 0]
        assert game.store == [3, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [9, 0, 11, 0, 0, 0, 8, 0, 7, 0, 0, 0]
        assert game.store == [3, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [10, 1, 12, 0, 0, 0, 0, 1, 8, 1, 1, 1]
        assert game.store == [3, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_13(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [10, 0, 13, 0, 0, 0, 0, 1, 8, 1, 1, 1]
        assert game.store == [3, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_14(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [10, 0, 13, 0, 0, 0, 0, 1, 8, 1, 0, 2]
        assert game.store == [3, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 14, 1, 1, 1, 1, 2, 9, 2, 1, 2]
        assert game.store == [3, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 14, 1, 1, 1, 0, 3, 9, 2, 1, 2]
        assert game.store == [3, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 3, 3, 3, 1, 4, 10, 3, 2, 3]
        assert game.store == [3, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_18(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 2, 0, 3, 3, 3, 1, 4, 10, 0, 3, 4]
        assert game.store == [3, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 4, 3, 3, 1, 4, 10, 0, 3, 4]
        assert game.store == [3, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_20(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 1, 4, 3, 3, 1, 4, 10, 0, 0, 5]
        assert game.store == [3, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 4, 4, 2, 5, 10, 0, 0, 5]
        assert game.store == [3, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_22(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 4, 4, 2, 0, 11, 1, 1, 6]
        assert game.store == [3, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 4, 0, 3, 1, 12, 0, 1, 6]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_24(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 4, 0, 0, 2, 13, 1, 1, 6]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_25(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 4, 0, 0, 2, 13, 1, 1, 6]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_26(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 4, 0, 0, 2, 13, 1, 0, 7]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 5, 0, 0, 2, 13, 1, 0, 7]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_28(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 5, 0, 0, 2, 13, 0, 1, 7]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_29(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 6, 0, 0, 2, 13, 0, 1, 7]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_30(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 7, 1, 1, 3, 0, 2, 3, 8]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_31(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 1, 7, 1, 1, 3, 0, 2, 3, 8]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_32(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 7, 1, 1, 0, 1, 3, 4, 8]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_33(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 8, 1, 1, 0, 1, 3, 4, 8]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_34(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 1, 1, 3, 9, 2, 2, 1, 1, 3, 4, 0]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_35(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 1, 0, 4, 9, 2, 2, 1, 1, 3, 4, 0]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_36(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 1, 0, 4, 9, 2, 2, 0, 2, 3, 4, 0]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 1, 0, 4, 9, 0, 3, 1, 2, 3, 4, 0]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_38(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 1, 0, 4, 9, 0, 3, 0, 3, 3, 4, 0]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_39(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 10, 1, 4, 1, 3, 3, 4, 0]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_40(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 10, 1, 0, 2, 4, 4, 5, 0]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_41(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 1, 0, 10, 1, 0, 2, 4, 4, 5, 0]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_42(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 1, 2, 1, 10, 1, 0, 2, 4, 4, 0, 1]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_43(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 2, 3, 1, 0, 2, 1, 3, 5, 5, 1, 2]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_44(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 0, 3, 1, 0, 2, 1, 3, 0, 6, 2, 3]
        assert game.store == [5, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_45(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 0, 3, 0, 1, 2, 1, 3, 0, 6, 2, 3]
        assert game.store == [5, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_46(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [5, 0, 3, 0, 1, 2, 1, 0, 1, 7, 3, 3]
        assert game.store == [5, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 0, 3, 0, 1, 0, 2, 1, 1, 7, 3, 3]
        assert game.store == [5, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_48(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 1, 0, 0, 1, 0, 2, 1, 1, 7, 3, 0]
        assert game.store == [5, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_49(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [6, 1, 0, 0, 0, 1, 2, 1, 1, 7, 3, 0]
        assert game.store == [5, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_50(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [6, 1, 0, 0, 0, 1, 2, 0, 2, 7, 3, 0]
        assert game.store == [5, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_51(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [6, 1, 0, 0, 0, 0, 0, 0, 2, 7, 3, 0]
        assert game.store == [8, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_52(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [7, 0, 0, 0, 0, 0, 0, 0, 2, 7, 0, 1]
        assert game.store == [8, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_53(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 1, 1, 1, 1, 2, 7, 0, 1]
        assert game.store == [8, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_54(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 1, 1, 2, 0, 1, 2]
        assert game.store == [8, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_55(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 2]
        assert game.store == [10, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_56(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 2]
        assert game.store == [10, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_57(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 2, 2]
        assert game.store == [10, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_58(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_59(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 2, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_60(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 3, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_61(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 3, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_62(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_63(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_64(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_65(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 1, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_66(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_67(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_68(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_69(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_70(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_71(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_72(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_73(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_74(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 2, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_75(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_76(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_77(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_78(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_79(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_80(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_81(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_82(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 2, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_83(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_84(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 2, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_85(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_86(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_87(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 2, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_88(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 2, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_89(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_90(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 1, 0, 2, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_91(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 2, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_92(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_93(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_94(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_95(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_96(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 2, 1, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_97(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_98(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_99(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_100(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 2, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_101(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 2, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_102(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_103(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_104(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 2, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_105(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 2, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_106(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_107(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_108(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_109(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 2]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_110(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_111(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_112(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_113(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_114(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_115(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_116(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 3, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_117(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_118(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_119(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_120(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_121(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 0, 1]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_122(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 2, 1, 0, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_123(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 2, 1, 0, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_124(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0]
        assert game.store == [10, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_125(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_126(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_127(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_128(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_129(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_130(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_131(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_132(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_133(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_134(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_135(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_136(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_137(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_138(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_139(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_140(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_141(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_142(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_143(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_144(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_145(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_146(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_147(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_148(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_149(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_150(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_151(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_152(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_153(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_154(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_155(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_156(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_157(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_158(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_159(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_160(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_161(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_162(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_163(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_164(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_165(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_166(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_167(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_168(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_169(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_170(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_171(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_172(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_173(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_174(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_175(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_176(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_177(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_178(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_179(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_180(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_181(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_182(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_183(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_184(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_185(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_186(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_187(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_188(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_189(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_190(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_191(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_192(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_193(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_194(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_195(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_196(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_197(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_198(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_199(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_200(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_201(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_202(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_203(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_204(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_205(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_206(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_207(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_208(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_209(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_210(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_211(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_212(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_213(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_214(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_215(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_216(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_217(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_218(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_219(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_220(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_221(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_222(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_223(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_224(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_225(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_226(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_227(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_228(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_229(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_230(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_231(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_232(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_233(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_234(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_235(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_236(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_237(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_238(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_239(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_240(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_241(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_242(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_243(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_244(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_245(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_246(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_247(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_248(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_249(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_250(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_251(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_252(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_253(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_254(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_255(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_256(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_257(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_258(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_259(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_260(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_261(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_262(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_263(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_264(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_265(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_266(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_267(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_268(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_269(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_270(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_271(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_272(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_273(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_274(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_275(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_276(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_277(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_278(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_279(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_280(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_281(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_282(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_283(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_284(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_285(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_286(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_287(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_288(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_289(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_290(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_291(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_292(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_293(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_294(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_295(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_296(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_297(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_298(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_299(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_300(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_301(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_302(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_303(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_304(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_305(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_306(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_307(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_308(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_309(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_310(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_311(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_312(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_313(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_314(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_315(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_316(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_317(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_318(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_319(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_320(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_321(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_322(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_323(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_324(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_325(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_326(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_327(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_328(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_329(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_330(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_331(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_332(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_333(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_334(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_335(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_336(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_337(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_338(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_339(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_340(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_341(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_342(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_343(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_344(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_345(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_346(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_347(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_348(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_349(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_350(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_351(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_352(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_353(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_354(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_355(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_356(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_357(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_358(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_359(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [12, 36]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_11_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_11_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 5, 4, 0, 5, 5, 5, 5, 4, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [6, 5, 4, 0, 5, 5, 5, 0, 5, 1, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_4(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [6, 5, 4, 0, 0, 6, 6, 1, 6, 0, 6, 6]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 6, 5, 1, 1, 7, 6, 1, 6, 0, 6, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_6(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [7, 6, 5, 1, 0, 8, 6, 1, 6, 0, 6, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [7, 6, 5, 1, 0, 8, 6, 0, 7, 0, 6, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_8(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [8, 7, 5, 1, 0, 0, 7, 1, 8, 1, 7, 1]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [9, 7, 5, 1, 0, 0, 7, 1, 8, 1, 7, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [9, 7, 5, 0, 1, 0, 7, 1, 8, 1, 7, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_11(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [9, 7, 5, 0, 1, 0, 7, 0, 9, 1, 7, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_12(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [9, 7, 5, 0, 0, 1, 7, 0, 9, 1, 7, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_13(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [10, 8, 5, 0, 0, 1, 0, 1, 10, 2, 8, 1]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [10, 8, 5, 0, 0, 0, 1, 1, 10, 2, 8, 1]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_15(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [10, 8, 5, 0, 0, 0, 1, 0, 11, 2, 8, 1]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_16(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [10, 0, 6, 1, 1, 1, 2, 1, 12, 0, 8, 1]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [10, 0, 6, 1, 1, 1, 0, 2, 13, 0, 8, 1]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_18(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [10, 0, 0, 2, 2, 2, 1, 3, 14, 0, 8, 1]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [10, 0, 0, 2, 2, 2, 0, 4, 14, 0, 8, 1]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_20(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [10, 0, 0, 2, 0, 3, 1, 4, 14, 0, 8, 1]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_21(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [11, 0, 0, 2, 0, 3, 1, 4, 14, 0, 8, 0]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_22(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [11, 0, 0, 0, 1, 4, 1, 4, 14, 0, 8, 0]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [11, 0, 0, 0, 1, 4, 0, 5, 14, 0, 8, 0]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_24(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 2, 5, 1, 6, 15, 1, 9, 1]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_25(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 2, 5, 1, 0, 16, 2, 10, 2]
        assert game.store == [5, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 2, 5, 1, 0, 16, 2, 10, 2]
        assert game.store == [5, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 3, 3, 6, 2, 1, 0, 4, 12, 4]
        assert game.store == [5, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_28(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 4, 7, 0, 1, 0, 4, 12, 4]
        assert game.store == [8, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_29(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 4, 7, 0, 1, 0, 0, 13, 5]
        assert game.store == [8, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_30(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 8, 1, 2, 1, 0, 13, 5]
        assert game.store == [8, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_31(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 2, 1, 1, 9, 2, 3, 2, 1, 0, 7]
        assert game.store == [8, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 2, 0, 2, 9, 2, 3, 2, 1, 0, 7]
        assert game.store == [8, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_33(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 2, 0, 2, 9, 0, 4, 3, 1, 0, 7]
        assert game.store == [8, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_34(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 2, 0, 0, 10, 1, 4, 3, 1, 0, 7]
        assert game.store == [8, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_35(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 3, 3, 1, 1, 11, 2, 4, 3, 1, 0, 0]
        assert game.store == [8, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_36(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 3, 3, 1, 0, 12, 2, 4, 3, 1, 0, 0]
        assert game.store == [8, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 3, 3, 1, 0, 12, 0, 5, 4, 1, 0, 0]
        assert game.store == [8, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_38(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 3, 3, 0, 1, 12, 0, 5, 4, 1, 0, 0]
        assert game.store == [8, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_39(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 3, 0, 1, 12, 0, 5, 0, 2, 1, 1]
        assert game.store == [8, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_40(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 4, 1, 2, 12, 0, 5, 0, 2, 1, 1]
        assert game.store == [8, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_41(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 4, 1, 2, 12, 0, 0, 1, 3, 2, 2]
        assert game.store == [8, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_42(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 4, 1, 0, 13, 1, 0, 1, 3, 2, 2]
        assert game.store == [8, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_43(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 4, 1, 0, 13, 1, 0, 0, 4, 2, 2]
        assert game.store == [8, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_44(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 1, 14, 0, 0, 0, 4, 2, 2]
        assert game.store == [10, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_45(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 1, 0, 2, 1, 14, 0, 0, 0, 4, 2, 0]
        assert game.store == [10, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_46(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 2, 1, 14, 0, 0, 0, 4, 2, 0]
        assert game.store == [10, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_47(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 1, 2, 1, 14, 0, 0, 0, 0, 3, 1]
        assert game.store == [10, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_48(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 1, 2, 0, 15, 0, 0, 0, 0, 3, 1]
        assert game.store == [10, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_49(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 0, 15, 0, 0, 0, 0, 3, 0]
        assert game.store == [10, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_50(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 16, 0, 0, 0, 0, 3, 0]
        assert game.store == [10, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_51(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 1, 16, 0, 0, 0, 0, 0, 1]
        assert game.store == [10, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_52(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 17, 0, 0, 0, 0, 0, 1]
        assert game.store == [10, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_53(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [29, 19]
        assert cond.name == "WIN"

        assert game.rtally.round_wins == [9, 2]
        assert game.rtally.seeds == [303, 225]
        assert game.rtally.diff_sums == [112, 34]
        assert game.rtally.score == [10, 3]

        gstate.cond = cond
