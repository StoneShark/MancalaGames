# -*- coding: utf-8 -*-
"""Test urim.  The simulated games almost never end
with the test parameters, this does.

Added assert for round tally 1 (a skunk) and 11.

Created on Fri Mar  7 10:19:47 2025
@author: Ann"""

import pytest
pytestmark = pytest.mark.integtest

from context import man_config
from context import man_path


class GameTestData:
    """allow passing move end cond between tests."""

    def __init__(self, game):
        self.game = game
        self.cond = None


@pytest.fixture(scope="class")
def gstate():
    """This fixture will maintain state between tests in the
    same class but will be reconstructed for each class."""

    game, _ = man_config.make_game(man_path.GAMEPATH + 'Urim.txt')
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
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 4, 0, 5, 5, 5, 5, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [6, 6, 5, 5, 4, 0, 5, 5, 0, 6, 5, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 6, 5, 0, 5, 1, 6, 6, 1, 6, 5, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [7, 6, 5, 0, 5, 1, 0, 7, 2, 7, 6, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [7, 6, 5, 0, 0, 2, 1, 8, 3, 8, 6, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [8, 7, 6, 1, 1, 2, 1, 8, 3, 8, 0, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [8, 7, 6, 1, 0, 3, 1, 8, 3, 8, 0, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [9, 8, 7, 1, 0, 3, 1, 8, 3, 8, 0, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [9, 0, 8, 2, 1, 4, 2, 9, 4, 9, 0, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [9, 0, 8, 2, 1, 4, 0, 10, 5, 9, 0, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 9, 3, 2, 5, 1, 11, 6, 10, 0, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 10, 4, 3, 6, 2, 12, 6, 0, 1, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 2, 0, 5, 4, 7, 3, 13, 7, 1, 2, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 5, 4, 7, 3, 13, 7, 1, 2, 0]
        assert game.store == [0, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 5, 0, 8, 4, 14, 8, 1, 2, 0]
        assert game.store == [0, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 1, 6, 1, 9, 5, 0, 10, 3, 4, 1]
        assert game.store == [0, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 1, 6, 0, 10, 5, 0, 10, 3, 4, 1]
        assert game.store == [0, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 6, 0, 10, 5, 0, 10, 3, 0, 2]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 1, 7, 0, 0, 6, 1, 11, 4, 1, 3]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 1, 7, 0, 0, 6, 1, 11, 4, 0, 4]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 1, 1, 7, 2, 12, 5, 1, 4]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 1, 1, 7, 0, 13, 6, 1, 4]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 2, 7, 0, 13, 6, 1, 4]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 2, 2, 1, 0, 2, 7, 0, 13, 0, 2, 5]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 2, 2, 0, 1, 2, 7, 0, 13, 0, 2, 5]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 2, 0, 1, 2, 7, 0, 13, 0, 0, 6]
        assert game.store == [0, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 2, 2, 7, 0, 13, 0, 0, 6]
        assert game.store == [0, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 3, 1, 0, 0, 0, 7, 0, 13, 0, 0, 0]
        assert game.store == [0, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 3, 0, 1, 0, 0, 7, 0, 13, 0, 0, 0]
        assert game.store == [0, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 14, 1, 1, 1]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 14, 1, 1, 1]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 14, 1, 0, 2]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 14, 1, 0, 2]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 1, 14, 1, 0, 0]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 1, 14, 1, 0, 0]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_37(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 1, 14, 0, 1, 0]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_38(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 1, 14, 0, 1, 0]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_39(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 0, 15, 0, 1, 0]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_40(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 15, 0, 1, 0]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_41(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 15, 0, 0, 1]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_42(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 1, 0, 15, 0, 0, 1]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_43(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 0, 1, 0, 15, 0, 0, 0]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_44(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 15, 0, 0, 0]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_45(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 1, 0, 1, 15, 0, 0, 0]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_46(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 1, 0, 1, 15, 0, 0, 0]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_47(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 1, 0, 0, 16, 0, 0, 0]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_48(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 0, 16, 0, 0, 0]
        assert game.store == [0, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_49(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 1, 2, 1, 1, 0, 2, 2, 2]
        assert game.store == [0, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_50(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 1, 2, 1, 1, 0, 2, 2, 2]
        assert game.store == [0, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_51(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 3, 1, 2, 1, 1, 0, 2, 0, 3]
        assert game.store == [0, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_52(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 3, 0, 3, 1, 1, 0, 2, 0, 3]
        assert game.store == [0, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_53(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 3, 0, 3, 1, 1, 0, 0, 1, 4]
        assert game.store == [0, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_54(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 3, 0, 0, 2, 2, 1, 0, 1, 4]
        assert game.store == [0, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_55(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 3, 0, 0, 2, 2, 1, 0, 0, 5]
        assert game.store == [0, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_56(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 2, 1, 0, 0, 5]
        assert game.store == [3, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_57(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 2, 0, 1, 0, 5]
        assert game.store == [3, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_58(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 2, 0, 1, 0, 5]
        assert game.store == [3, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_59(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 2, 0, 0, 1, 5]
        assert game.store == [3, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_60(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 1, 2, 0, 0, 1, 5]
        assert game.store == [3, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_61(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 5]
        assert game.store == [3, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_62(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 5]
        assert game.store == [3, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_63(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 1, 0]
        assert game.store == [3, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_64(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 2, 0, 1, 0, 1, 0, 1, 1, 1, 0]
        assert game.store == [3, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_65(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 2, 0, 1, 0, 1, 0, 0, 2, 1, 0]
        assert game.store == [3, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_66(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 2, 0, 1, 0, 1, 0, 0, 2, 1, 0]
        assert game.store == [3, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_67(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 2, 0, 1, 0, 0, 1, 0, 2, 1, 0]
        assert game.store == [3, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_68(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 2, 0, 0, 1, 0, 1, 0, 2, 1, 0]
        assert game.store == [3, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_69(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 2, 0, 0, 1, 0, 1, 0, 2, 0, 1]
        assert game.store == [3, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_70(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 2, 0, 0, 0, 1, 1, 0, 2, 0, 1]
        assert game.store == [3, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_71(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 2, 2, 0, 0, 0, 1, 1, 0, 0, 1, 2]
        assert game.store == [3, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_72(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 1, 0, 1, 1, 0, 0, 1, 2]
        assert game.store == [3, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_73(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_74(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_75(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 2, 0, 0, 1, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_76(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 2, 0, 0, 2, 0, 0, 1, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_77(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 2, 0, 0, 2, 0, 0, 0, 1]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_78(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 2, 0, 0, 0, 1]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_79(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_80(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 2, 0, 0, 0, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_81(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_82(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_83(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_84(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_85(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 1, 0, 2, 0, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_86(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 1, 0, 1, 0, 2, 0, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_87(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_88(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_89(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_90(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 2, 0, 1, 0, 0, 1, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_91(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 2, 0, 0, 1, 0, 1, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_92(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 2, 0, 0, 1, 0, 1, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_93(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 2, 0, 0, 0, 1, 1, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_94(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_95(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 2, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_96(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 2, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_97(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 0, 1, 0, 2, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_98(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 2, 0]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_99(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_100(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 2, 0, 1, 0, 1, 0, 0, 1]
        assert game.store == [3, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_101(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [3, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_102(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [5, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_103(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [5, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_104(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [7, 41]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        assert game.rtally.score == [0, 2]   # a skunk
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 4, 0, 5, 5, 5, 5, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 4, 0, 5, 5, 5, 5, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 5, 1, 6, 6, 5, 5, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 6, 2, 7, 6, 5, 5, 0, 5, 5, 0, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 6, 2, 0, 7, 6, 6, 1, 6, 6, 1, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 7, 3, 1, 7, 6, 6, 1, 6, 0, 2, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 4, 2, 8, 7, 7, 2, 7, 0, 2, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 1, 5, 0, 8, 7, 7, 2, 0, 1, 3, 8]
        assert game.store == [0, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 1, 0, 1, 9, 8, 8, 0, 0, 1, 3, 8]
        assert game.store == [3, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 9, 8, 8, 0, 0, 1, 0, 9]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 10, 8, 8, 0, 0, 1, 0, 9]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 10, 8, 8, 0, 0, 0, 1, 9]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 9, 9, 1, 1, 1, 2, 10]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 9, 9, 1, 0, 2, 2, 10]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 2, 2, 0, 0, 0, 10, 2, 1, 3, 3, 11]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_16(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 2, 2, 0, 0, 0, 10, 2, 0, 4, 3, 11]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_17(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 3, 1, 0, 0, 10, 2, 0, 4, 3, 11]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 1, 4, 2, 1, 0, 0, 3, 1, 5, 4, 12]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_19(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 1, 0, 3, 2, 1, 1, 3, 1, 5, 4, 12]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_20(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 1, 0, 3, 2, 1, 1, 0, 2, 6, 5, 12]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_21(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 4, 2, 1, 1, 0, 2, 6, 5, 12]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_22(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 1, 4, 2, 1, 1, 0, 0, 7, 6, 12]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_23(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 5, 2, 1, 1, 0, 0, 7, 6, 12]
        assert game.store == [3, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 3, 6, 0, 1, 1, 0, 0, 7, 0, 13]
        assert game.store == [3, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_25(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 3, 6, 0, 0, 0, 0, 0, 7, 0, 13]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 2, 4, 7, 1, 0, 0, 0, 0, 0, 1, 14]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_27(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 5, 8, 1, 0, 0, 0, 0, 0, 1, 14]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_28(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 0, 5, 8, 1, 0, 0, 0, 0, 0, 0, 15]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_29(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 0, 5, 8, 0, 1, 0, 0, 0, 0, 0, 15]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_30(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 2, 7, 10, 1, 2, 1, 1, 1, 1, 1, 0]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 2, 0, 11, 2, 3, 0, 0, 0, 0, 1, 0]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_32(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [4, 2, 0, 11, 2, 3, 0, 0, 0, 0, 0, 1]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_33(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 3, 1, 0, 3, 4, 1, 1, 1, 1, 1, 2]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_34(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 3, 1, 0, 3, 4, 0, 2, 1, 1, 1, 2]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_35(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 0, 2, 1, 4, 4, 0, 2, 1, 1, 1, 2]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_36(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 0, 2, 1, 4, 4, 0, 2, 1, 1, 0, 3]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_37(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 0, 0, 2, 5, 4, 0, 2, 1, 1, 0, 3]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_38(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [5, 0, 0, 2, 5, 4, 0, 2, 1, 0, 1, 3]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_39(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 0, 0, 2, 5, 0, 1, 3, 2, 1, 1, 3]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_40(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 1, 1, 2, 5, 0, 1, 3, 2, 1, 1, 0]
        assert game.store == [13, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_41(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 2, 3, 6, 1, 0, 3, 2, 1, 1, 0]
        assert game.store == [15, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_42(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 2, 3, 6, 1, 0, 3, 0, 2, 2, 0]
        assert game.store == [15, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_43(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 2, 3, 0, 2, 1, 4, 1, 0, 0, 0]
        assert game.store == [21, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_44(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 2, 3, 0, 2, 1, 0, 2, 1, 1, 1]
        assert game.store == [21, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_45(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 3, 4, 0, 2, 1, 0, 2, 1, 1, 1]
        assert game.store == [21, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_46(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 3, 4, 0, 2, 0, 1, 2, 1, 1, 1]
        assert game.store == [21, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_47(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 3, 0, 1, 3, 1, 0, 2, 1, 1, 1]
        assert game.store == [23, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_48(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 1, 3, 1, 0, 0, 2, 2, 1]
        assert game.store == [23, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_49(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 3, 0, 0, 4, 1, 0, 0, 2, 2, 1]
        assert game.store == [23, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_50(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 0, 4, 0, 1, 0, 2, 2, 1]
        assert game.store == [23, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_51(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 5, 0, 1, 0, 2, 2, 1]
        assert game.store == [23, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_52(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 5, 0, 1, 0, 0, 3, 2]
        assert game.store == [23, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_53(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 2, 1, 1, 0, 2]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_54(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 3, 1, 1, 0, 2]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_55(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 3, 1, 1, 0, 2]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_56(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 3, 0, 2, 0, 2]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_57(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 3, 0, 2, 0, 2]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_58(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 4, 0, 2, 0, 2]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_59(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 4, 0, 2, 0, 2]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_60(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 4, 0, 2, 0, 0]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_61(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 4, 0, 2, 0, 0]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_62(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 0, 1, 3, 1, 1]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_63(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 1, 3, 1, 1]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_64(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 2, 2]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_65(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 2, 2]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_66(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 3]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_67(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 1, 0, 0, 1, 0, 1, 0, 0, 3]
        assert game.store == [27, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_68(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_69(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_70(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_71(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_72(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_73(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 2, 0, 0, 0, 0, 2, 0, 0, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_74(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 2, 0, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_75(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_76(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 2, 2, 0, 0, 0, 0, 0, 1, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_77(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 1, 0, 0, 0, 0, 1, 0, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_78(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_79(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 1, 1]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_80(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 2]
        assert game.store == [27, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_81(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_82(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_83(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_84(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_85(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_86(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_87(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_88(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_89(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_90(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_91(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_92(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_93(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2]
        assert game.store == [29, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_94(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [29, 19]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_3_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_3_move_1(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 4, 0, 5, 5, 5, 5, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 1, 6, 6, 5, 5, 0, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 5, 1, 6, 6, 0, 6, 1, 6, 6, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [5, 5, 1, 6, 6, 0, 6, 0, 7, 6, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 5, 1, 0, 7, 1, 7, 1, 8, 7, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_7(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [6, 6, 1, 0, 7, 1, 0, 2, 9, 8, 7, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_8(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [6, 6, 1, 0, 7, 0, 1, 2, 9, 8, 7, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_9(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [6, 6, 1, 0, 7, 0, 0, 3, 9, 8, 7, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [6, 6, 1, 0, 0, 1, 1, 4, 10, 9, 8, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [7, 7, 2, 1, 1, 2, 2, 4, 10, 9, 0, 1]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_12(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [7, 7, 2, 1, 0, 3, 2, 4, 10, 9, 0, 1]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_13(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [8, 7, 2, 1, 0, 3, 2, 4, 10, 9, 0, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_14(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [8, 0, 3, 2, 1, 4, 3, 5, 11, 9, 0, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_15(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [9, 1, 4, 3, 2, 5, 4, 6, 0, 10, 1, 1]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_16(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [9, 1, 4, 0, 3, 6, 5, 6, 0, 10, 1, 1]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_17(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [9, 1, 4, 0, 3, 6, 5, 6, 0, 10, 0, 2]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_18(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [9, 1, 0, 1, 4, 7, 6, 6, 0, 10, 0, 2]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [10, 1, 0, 1, 4, 7, 0, 7, 1, 11, 1, 3]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_20(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [10, 1, 0, 0, 5, 7, 0, 7, 1, 11, 1, 3]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [11, 2, 1, 0, 5, 7, 0, 0, 2, 12, 2, 4]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_22(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 2, 1, 6, 8, 1, 1, 3, 13, 3, 5]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 3, 2, 1, 6, 8, 0, 2, 3, 13, 3, 5]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 3, 2, 0, 7, 8, 0, 2, 3, 13, 3, 5]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_25(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 3, 2, 0, 7, 8, 0, 0, 4, 14, 3, 5]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 4, 2, 0, 7, 0, 1, 1, 5, 15, 4, 6]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_27(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 4, 2, 0, 7, 0, 1, 0, 6, 15, 4, 6]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_28(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 5, 2, 0, 7, 0, 1, 0, 6, 15, 4, 6]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_29(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 6, 0, 0, 7, 0, 1, 0, 6, 15, 0, 7]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_30(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 6, 0, 0, 0, 1, 2, 1, 7, 16, 1, 8]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_31(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 7, 1, 1, 1, 2, 3, 2, 7, 16, 1, 0]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 8, 2, 1, 1, 2, 3, 2, 7, 16, 1, 0]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_33(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 10, 0, 2, 2, 3, 4, 3, 8, 0, 3, 2]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_34(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 10, 0, 2, 2, 0, 5, 4, 9, 0, 3, 2]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_35(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 11, 0, 2, 2, 0, 5, 4, 9, 0, 0, 3]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_36(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 0, 1, 3, 3, 1, 6, 5, 10, 1, 1, 4]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 0, 1, 3, 3, 1, 0, 6, 11, 2, 2, 5]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_38(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 0, 1, 3, 3, 0, 1, 6, 11, 2, 2, 5]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_39(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [6, 0, 1, 3, 3, 0, 1, 6, 11, 2, 0, 6]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_40(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 0, 1, 0, 4, 1, 0, 6, 11, 2, 0, 6]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_41(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [7, 1, 1, 0, 4, 1, 0, 0, 12, 3, 1, 7]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_42(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 2, 1, 5, 2, 1, 1, 12, 3, 1, 7]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_43(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 2, 1, 5, 2, 1, 1, 12, 3, 0, 8]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_44(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 2, 0, 6, 2, 1, 1, 12, 3, 0, 8]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_45(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 2, 0, 6, 2, 1, 1, 12, 0, 1, 9]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_46(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 3, 1, 6, 2, 1, 1, 12, 0, 1, 9]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_47(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 3, 1, 6, 2, 1, 1, 12, 0, 0, 10]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_48(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 3, 1, 0, 3, 2, 2, 13, 1, 1, 10]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_49(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 1, 4, 2, 1, 4, 3, 3, 14, 2, 1, 0]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_50(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 5, 2, 1, 4, 3, 3, 14, 2, 1, 0]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_51(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 2, 5, 2, 1, 4, 3, 3, 14, 0, 2, 1]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_52(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 6, 3, 1, 4, 3, 3, 14, 0, 2, 1]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_53(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 6, 3, 1, 4, 3, 3, 14, 0, 2, 0]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_54(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 6, 3, 0, 5, 3, 3, 14, 0, 2, 0]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_55(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 6, 3, 0, 5, 3, 0, 15, 1, 3, 0]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_56(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 4, 1, 6, 4, 1, 16, 1, 3, 0]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_57(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 4, 1, 6, 4, 1, 16, 0, 4, 0]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_58(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 2, 7, 5, 0, 16, 0, 4, 0]
        assert game.store == [6, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_59(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 2, 7, 0, 1, 17, 1, 5, 1]
        assert game.store == [6, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_60(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 2, 0, 1, 2, 17, 2, 6, 2]
        assert game.store == [6, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_61(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 2, 0, 0, 3, 17, 2, 6, 2]
        assert game.store == [6, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_62(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 2, 0, 0, 3, 17, 2, 6, 2]
        assert game.store == [6, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_63(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 3, 2, 1, 0, 0, 0, 3, 17, 2, 0, 3]
        assert game.store == [6, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_64(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 3, 2, 1, 0, 0, 3, 17, 2, 0, 3]
        assert game.store == [6, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_65(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 3, 2, 1, 0, 0, 0, 17, 3, 1, 4]
        assert game.store == [6, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_66(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 3, 2, 1, 0, 0, 0, 17, 3, 1, 4]
        assert game.store == [6, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_67(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 3, 5, 3, 2, 1, 1, 1, 0, 5, 3, 6]
        assert game.store == [6, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_68(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 3, 5, 3, 2, 0, 0, 1, 0, 5, 3, 6]
        assert game.store == [8, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_69(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 4, 6, 4, 3, 1, 0, 1, 0, 5, 3, 0]
        assert game.store == [8, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_70(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 4, 0, 5, 4, 2, 1, 2, 1, 5, 3, 0]
        assert game.store == [8, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_71(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 4, 0, 5, 4, 2, 1, 0, 2, 6, 3, 0]
        assert game.store == [8, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_72(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 4, 0, 0, 5, 3, 2, 1, 0, 6, 3, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_73(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 4, 0, 0, 5, 3, 2, 0, 1, 6, 3, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_74(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 5, 1, 1, 5, 3, 2, 0, 1, 6, 3, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_75(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 5, 1, 1, 5, 3, 2, 0, 0, 7, 3, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_76(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 5, 1, 1, 5, 0, 3, 1, 1, 7, 3, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_77(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 5, 1, 1, 5, 0, 0, 2, 2, 8, 3, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_78(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 5, 1, 1, 0, 1, 1, 3, 3, 9, 3, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_79(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 5, 1, 1, 0, 1, 1, 0, 4, 10, 4, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_80(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 5, 1, 0, 1, 1, 1, 0, 4, 10, 4, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_81(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 5, 1, 0, 1, 1, 0, 1, 4, 10, 4, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_82(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 5, 1, 0, 1, 0, 1, 1, 4, 10, 4, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_83(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 6, 2, 1, 2, 1, 2, 2, 4, 0, 5, 1]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_84(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 3, 2, 3, 2, 0, 0, 4, 0, 5, 1]
        assert game.store == [17, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_85(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 3, 2, 0, 0, 4, 0, 0, 2]
        assert game.store == [17, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_86(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 0, 3, 1, 1, 4, 0, 0, 2]
        assert game.store == [17, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_87(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 3, 1, 1, 4, 0, 0, 0]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_88(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 2, 2, 5, 0, 0, 0]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_89(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 2, 2, 0, 1, 1, 1]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_90(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 2, 2, 0, 1, 1, 1]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_91(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 3, 1, 1, 1, 1]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_92(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 3, 1, 1, 1, 1]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_93(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 3, 1, 1, 1, 0]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_94(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 3, 1, 1, 1, 0]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_95(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 0, 2, 2, 2, 0]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_96(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 0, 0, 0, 0, 2, 2, 2, 0]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_97(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 2, 0, 0, 0, 0, 2, 0, 3, 1]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_98(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 1, 0, 0, 2, 0, 3, 1]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_99(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 4, 1]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_100(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 4, 1]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_101(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 4, 0]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_102(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 4, 0]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_103(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 2, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_104(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 2, 1, 0, 1, 1, 0, 0, 1, 0, 1]
        assert game.store == [17, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_105(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 0, 1, 1, 0, 0, 1, 0, 0]
        assert game.store == [17, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_106(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 1, 1, 1, 0, 0, 1, 0, 0]
        assert game.store == [17, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_107(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 1, 1, 1, 0, 0, 0, 1, 0]
        assert game.store == [17, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_108(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_109(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_110(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_111(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_112(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_113(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_114(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_115(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_116(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_117(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_118(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_119(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_120(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_121(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_122(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_123(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_124(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_125(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_126(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_127(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_128(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_129(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_130(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_131(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_132(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_133(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_134(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_135(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_136(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_137(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_138(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_139(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_140(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_141(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_142(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_143(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_144(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_145(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_146(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_147(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_148(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_149(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_150(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_151(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_152(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_153(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_154(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_155(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_156(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_157(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_158(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_159(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_160(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_161(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_162(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_163(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_164(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_165(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_166(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_167(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_168(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_169(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_170(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_171(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_172(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 0]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_173(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_174(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [19, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_175(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [19, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_176(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [19, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_177(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [19, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_178(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [21, 27]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_4_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_4_move_1(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_2(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 0, 5, 5, 5, 5, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 0, 5, 0, 6, 6, 5, 1, 6, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 1, 6, 1, 6, 6, 5, 1, 6, 5, 0, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 1, 6, 1, 0, 7, 6, 2, 7, 6, 1, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 1, 6, 1, 0, 7, 6, 2, 7, 6, 0, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_7(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [6, 1, 6, 1, 0, 0, 7, 3, 8, 7, 1, 8]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 2, 7, 2, 1, 1, 8, 4, 8, 7, 1, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 2, 7, 0, 2, 2, 8, 4, 8, 7, 1, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [7, 2, 7, 0, 2, 2, 8, 4, 8, 7, 0, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_11(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [7, 2, 7, 0, 0, 3, 9, 4, 8, 7, 0, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [8, 3, 8, 1, 1, 3, 9, 4, 8, 0, 1, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 3, 8, 0, 2, 3, 9, 4, 8, 0, 1, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [9, 4, 9, 1, 2, 3, 0, 5, 9, 1, 2, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_15(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [9, 0, 10, 2, 3, 4, 0, 5, 9, 1, 2, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_16(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [10, 1, 11, 3, 4, 5, 0, 5, 0, 2, 3, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [11, 2, 0, 4, 5, 6, 1, 6, 1, 3, 4, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_18(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [11, 2, 0, 4, 5, 6, 1, 6, 0, 4, 4, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [11, 2, 0, 0, 6, 7, 2, 7, 0, 4, 4, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_20(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [12, 3, 1, 1, 7, 7, 2, 7, 0, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_21(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 5, 2, 2, 8, 8, 3, 8, 1, 5, 5, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_22(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 5, 2, 2, 8, 8, 3, 8, 1, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_23(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 6, 2, 2, 8, 8, 3, 8, 1, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 7, 0, 0, 8, 8, 3, 8, 1, 5, 0, 1]
        assert game.store == [0, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_25(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 8, 0, 0, 8, 0, 4, 9, 2, 6, 1, 2]
        assert game.store == [0, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 9, 1, 1, 8, 0, 4, 9, 2, 0, 2, 3]
        assert game.store == [0, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 9, 1, 0, 9, 0, 4, 9, 2, 0, 2, 3]
        assert game.store == [0, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_28(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 10, 0, 0, 9, 0, 4, 9, 2, 0, 2, 0]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_29(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 11, 1, 1, 10, 0, 4, 9, 2, 0, 2, 0]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_30(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 11, 1, 1, 10, 0, 4, 9, 0, 1, 3, 0]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_31(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 11, 1, 0, 11, 0, 4, 9, 0, 1, 3, 0]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_32(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 11, 1, 0, 11, 0, 0, 10, 1, 2, 4, 0]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_33(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 1, 12, 1, 1, 11, 2, 3, 5, 1]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_34(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 12, 1, 0, 12, 2, 3, 5, 1]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_35(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 1, 3, 2, 0, 3, 1, 13, 3, 4, 6, 2]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_36(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 2, 4, 3, 1, 4, 2, 0, 5, 6, 7, 3]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_37(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [3, 2, 4, 3, 0, 5, 2, 0, 5, 6, 7, 3]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_38(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 3, 5, 3, 0, 5, 2, 0, 5, 6, 7, 0]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_39(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 0, 6, 4, 1, 5, 2, 0, 5, 6, 7, 0]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_40(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 1, 6, 4, 1, 5, 2, 0, 0, 7, 8, 1]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_41(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 7, 5, 2, 6, 2, 0, 0, 7, 8, 1]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_42(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 3, 8, 6, 0, 6, 2, 0, 0, 0, 9, 2]
        assert game.store == [0, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_43(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 4, 8, 6, 0, 6, 2, 0, 0, 0, 9, 2]
        assert game.store == [0, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_44(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 5, 9, 7, 1, 7, 3, 1, 0, 0, 0, 3]
        assert game.store == [0, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_45(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 5, 0, 8, 2, 8, 4, 2, 1, 1, 1, 0]
        assert game.store == [4, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_46(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 5, 0, 8, 2, 8, 4, 2, 0, 2, 1, 0]
        assert game.store == [4, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 6, 0, 8, 2, 0, 5, 3, 1, 3, 2, 1]
        assert game.store == [4, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_48(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 6, 0, 8, 2, 0, 5, 3, 1, 3, 2, 0]
        assert game.store == [4, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_49(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 6, 0, 8, 0, 1, 6, 3, 1, 3, 2, 0]
        assert game.store == [4, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_50(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 6, 0, 8, 0, 1, 6, 3, 0, 4, 2, 0]
        assert game.store == [4, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_51(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 6, 0, 0, 1, 2, 7, 4, 1, 5, 3, 1]
        assert game.store == [4, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_52(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 7, 0, 0, 1, 2, 0, 5, 2, 6, 4, 2]
        assert game.store == [4, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_53(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 7, 0, 0, 0, 3, 0, 5, 2, 6, 4, 2]
        assert game.store == [4, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_54(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 8, 1, 1, 0, 3, 0, 5, 2, 0, 5, 3]
        assert game.store == [4, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_55(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 8, 0, 2, 0, 3, 0, 5, 2, 0, 5, 3]
        assert game.store == [4, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_56(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 9, 1, 0, 0, 3, 0, 5, 2, 0, 0, 4]
        assert game.store == [4, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_57(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [3, 9, 1, 0, 0, 0, 1, 6, 0, 0, 0, 4]
        assert game.store == [7, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_58(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 9, 1, 0, 0, 0, 0, 7, 0, 0, 0, 4]
        assert game.store == [7, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_59(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 0, 2, 1, 1, 1, 1, 8, 1, 1, 1, 4]
        assert game.store == [7, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_60(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 1, 0, 0, 1, 1, 1, 8, 1, 1, 1, 0]
        assert game.store == [7, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_61(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 1, 0, 0, 0, 2, 1, 8, 1, 1, 1, 0]
        assert game.store == [7, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_62(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [4, 1, 0, 0, 0, 2, 0, 9, 1, 1, 1, 0]
        assert game.store == [7, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_63(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 1, 0, 0, 0, 0, 1, 10, 1, 1, 1, 0]
        assert game.store == [7, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_64(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [4, 1, 0, 0, 0, 0, 1, 10, 0, 2, 1, 0]
        assert game.store == [7, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_65(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 0, 1, 0, 0, 0, 1, 10, 0, 2, 1, 0]
        assert game.store == [7, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_66(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [5, 1, 2, 1, 1, 1, 1, 0, 1, 3, 2, 1]
        assert game.store == [7, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_67(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 3, 2, 2, 2, 1, 0, 1, 3, 2, 1]
        assert game.store == [7, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_68(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 2, 3, 2, 2, 2, 1, 0, 1, 3, 0, 2]
        assert game.store == [7, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_69(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 3, 2, 2, 0, 2, 1, 1, 3, 0, 2]
        assert game.store == [7, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_70(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 2, 3, 2, 2, 0, 2, 1, 1, 0, 1, 3]
        assert game.store == [7, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_71(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 3, 2, 0, 1, 0, 1, 1, 0, 1, 3]
        assert game.store == [10, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_72(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 3, 2, 0, 1, 0, 0, 2, 0, 1, 3]
        assert game.store == [10, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_73(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 3, 2, 0, 0, 1, 0, 2, 0, 1, 3]
        assert game.store == [10, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_74(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 3, 2, 0, 0, 0, 1, 2, 0, 1, 3]
        assert game.store == [10, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_75(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 3, 1, 1, 0, 1, 2, 0, 1, 3]
        assert game.store == [10, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_76(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 3, 1, 3, 1, 1, 0, 1, 2, 0, 1, 0]
        assert game.store == [10, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_77(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 3, 1, 0, 2, 2, 1, 1, 2, 0, 1, 0]
        assert game.store == [10, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_78(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 3, 1, 0, 2, 2, 1, 1, 0, 1, 2, 0]
        assert game.store == [10, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_79(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 3, 0, 1, 2, 2, 1, 1, 0, 1, 2, 0]
        assert game.store == [10, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_80(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 3, 0, 1, 2, 2, 1, 1, 0, 1, 0, 1]
        assert game.store == [10, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_81(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 3, 2, 1, 1, 0, 1, 0, 1]
        assert game.store == [10, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_82(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 3, 0, 0, 3, 2, 1, 0, 1, 1, 0, 1]
        assert game.store == [10, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_83(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 0, 3, 2, 1, 1, 1, 0, 1]
        assert game.store == [10, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_84(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 3, 0, 0, 0, 3, 2, 1, 1, 1, 0, 0]
        assert game.store == [10, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_85(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 1, 3, 2, 1, 1, 1, 0, 0]
        assert game.store == [10, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_86(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 1, 3, 2, 1, 1, 0, 1, 0]
        assert game.store == [10, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_87(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [17, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_88(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [17, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_89(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [17, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_90(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [17, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_91(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [17, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_92(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [17, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_93(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [17, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_94(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [17, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_95(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [17, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_96(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [17, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_97(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [17, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_98(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0]
        assert game.store == [17, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_99(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0]
        assert game.store == [17, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_100(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
        assert game.store == [17, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_101(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [20, 28]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_5_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_5_move_1(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 5, 0, 6, 5, 5, 5, 5, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_3(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 5, 0, 6, 5, 5, 0, 6, 5, 5, 5, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 5, 0, 6, 5, 0, 1, 7, 6, 6, 6, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_5(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 6, 1, 7, 5, 0, 1, 7, 6, 0, 7, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [6, 6, 0, 8, 5, 0, 1, 7, 6, 0, 7, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_7(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 7, 0, 8, 5, 0, 1, 7, 6, 0, 7, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 8, 1, 9, 6, 1, 2, 8, 6, 0, 7, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 9, 0, 9, 6, 1, 2, 8, 0, 1, 8, 1]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 9, 0, 9, 0, 2, 3, 9, 1, 2, 9, 1]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 10, 1, 10, 1, 3, 4, 10, 1, 2, 0, 2]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_12(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 11, 2, 10, 1, 3, 4, 10, 1, 2, 0, 2]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 11, 2, 10, 1, 3, 4, 10, 0, 3, 0, 2]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 11, 2, 10, 1, 0, 5, 11, 1, 3, 0, 2]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_15(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 12, 3, 11, 2, 1, 6, 0, 2, 4, 1, 3]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_16(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 13, 4, 0, 3, 2, 7, 1, 3, 5, 2, 4]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_17(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 14, 5, 1, 3, 2, 7, 1, 3, 5, 2, 0]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_18(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 14, 0, 2, 4, 3, 8, 0, 3, 5, 2, 0]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [4, 15, 1, 2, 4, 3, 0, 1, 4, 6, 3, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_20(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 16, 2, 3, 5, 3, 0, 1, 4, 6, 3, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 16, 2, 3, 5, 3, 0, 0, 5, 6, 3, 1]
        assert game.store == [2, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 4, 5, 7, 5, 0, 1, 6, 7, 4, 2]
        assert game.store == [4, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_23(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 1, 5, 5, 7, 5, 0, 1, 0, 8, 5, 3]
        assert game.store == [4, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 5, 0, 8, 6, 1, 2, 1, 8, 5, 3]
        assert game.store == [4, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_25(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 2, 6, 0, 8, 6, 1, 2, 1, 8, 5, 0]
        assert game.store == [4, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [3, 2, 6, 0, 8, 0, 2, 3, 2, 9, 6, 1]
        assert game.store == [4, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 3, 7, 1, 9, 1, 3, 3, 2, 0, 7, 2]
        assert game.store == [4, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_28(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 0, 8, 2, 10, 1, 3, 3, 2, 0, 7, 2]
        assert game.store == [4, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_29(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [4, 0, 8, 2, 10, 1, 0, 4, 3, 1, 7, 2]
        assert game.store == [4, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 0, 0, 3, 11, 2, 1, 5, 4, 2, 8, 2]
        assert game.store == [4, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 0, 0, 3, 11, 2, 1, 5, 4, 0, 9, 3]
        assert game.store == [4, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 0, 0, 0, 12, 3, 0, 5, 4, 0, 9, 3]
        assert game.store == [6, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_33(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 1, 1, 1, 13, 4, 1, 6, 4, 0, 0, 4]
        assert game.store == [6, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_34(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 1, 0, 2, 13, 4, 1, 6, 4, 0, 0, 4]
        assert game.store == [6, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_35(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [6, 0, 0, 2, 13, 4, 1, 0, 5, 1, 1, 5]
        assert game.store == [6, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_36(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [7, 1, 1, 3, 0, 6, 0, 1, 6, 2, 2, 6]
        assert game.store == [9, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_37(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [8, 2, 2, 4, 1, 7, 0, 1, 6, 2, 2, 0]
        assert game.store == [9, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_38(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [8, 2, 0, 5, 2, 7, 0, 1, 6, 2, 2, 0]
        assert game.store == [9, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_39(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [8, 2, 0, 5, 2, 7, 0, 0, 7, 2, 2, 0]
        assert game.store == [9, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_40(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [8, 0, 1, 6, 2, 7, 0, 0, 7, 2, 2, 0]
        assert game.store == [9, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_41(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [9, 0, 1, 6, 2, 7, 0, 0, 7, 2, 0, 1]
        assert game.store == [9, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_42(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [9, 0, 1, 0, 3, 8, 1, 1, 8, 0, 0, 1]
        assert game.store == [12, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_43(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [10, 1, 2, 1, 0, 8, 1, 1, 0, 1, 1, 2]
        assert game.store == [12, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_44(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [10, 0, 3, 1, 0, 8, 1, 1, 0, 1, 1, 2]
        assert game.store == [12, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_45(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [10, 0, 3, 1, 0, 8, 1, 1, 0, 0, 2, 2]
        assert game.store == [12, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_46(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [10, 0, 0, 2, 1, 9, 1, 1, 0, 0, 2, 2]
        assert game.store == [12, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [10, 0, 0, 2, 1, 9, 0, 2, 0, 0, 2, 2]
        assert game.store == [12, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_48(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 3, 2, 10, 1, 3, 1, 1, 0, 2]
        assert game.store == [15, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_49(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 1, 3, 2, 10, 1, 3, 1, 0, 1, 2]
        assert game.store == [15, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_50(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 3, 11, 0, 3, 1, 0, 1, 2]
        assert game.store == [17, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_51(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 3, 11, 0, 0, 2, 1, 2, 2]
        assert game.store == [17, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_52(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 2, 1, 4, 0, 1, 1, 3, 2, 3, 3]
        assert game.store == [17, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_53(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 2, 2, 1, 4, 0, 1, 0, 4, 2, 3, 3]
        assert game.store == [17, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_54(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 2, 2, 1, 0, 1, 2, 1, 5, 2, 3, 3]
        assert game.store == [17, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_55(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 2, 2, 1, 0, 1, 2, 0, 6, 2, 3, 3]
        assert game.store == [17, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_56(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 2, 1, 1, 2, 0, 6, 2, 3, 3]
        assert game.store == [17, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_57(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 3, 1, 2, 1, 1, 2, 0, 0, 3, 4, 4]
        assert game.store == [17, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_58(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 2, 3, 2, 1, 2, 0, 0, 3, 4, 4]
        assert game.store == [17, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_59(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 2, 3, 2, 1, 2, 0, 0, 0, 5, 5]
        assert game.store == [17, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_60(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 3, 2, 0, 0, 0, 0, 5, 5]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_61(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 3, 1, 3, 2, 0, 0, 0, 0, 0, 6]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_62(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 3, 1, 3, 0, 1, 1, 0, 0, 0, 6]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_63(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 3, 1, 3, 0, 0, 2, 0, 0, 0, 6]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_64(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 3, 1, 3, 0, 0, 2, 0, 0, 0, 6]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_65(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 3, 4, 2, 4, 1, 0, 2, 0, 0, 0, 0]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_66(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 4, 4, 2, 4, 1, 0, 2, 0, 0, 0, 0]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_67(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 4, 4, 2, 4, 1, 0, 0, 1, 1, 0, 0]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_68(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 4, 4, 2, 4, 0, 1, 0, 1, 1, 0, 0]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_69(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 4, 4, 2, 4, 0, 1, 0, 0, 2, 0, 0]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_70(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 4, 0, 3, 5, 1, 0, 0, 0, 2, 0, 0]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_71(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 4, 0, 3, 5, 1, 0, 0, 0, 0, 1, 1]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_72(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 4, 0, 3, 5, 0, 1, 0, 0, 0, 1, 1]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_73(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 4, 0, 3, 5, 0, 1, 0, 0, 0, 0, 2]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_74(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 4, 6, 1, 1, 0, 0, 0, 0, 2]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_75(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 4, 6, 1, 0, 1, 0, 0, 0, 2]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_76(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 4, 6, 0, 1, 1, 0, 0, 0, 2]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_77(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 4, 6, 0, 0, 2, 0, 0, 0, 2]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_78(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 4, 0, 1, 1, 3, 1, 1, 1, 2]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_79(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 4, 0, 1, 1, 0, 2, 2, 2, 2]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_80(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 5, 0, 1, 1, 0, 2, 2, 2, 2]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_81(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 5, 0, 1, 1, 0, 2, 2, 0, 3]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_82(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 5, 0, 1, 1, 0, 2, 2, 0, 3]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_83(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 1, 5, 0, 1, 1, 0, 2, 2, 0, 0]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_84(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 1, 5, 0, 1, 1, 0, 2, 2, 0, 0]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_85(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 1, 5, 0, 1, 1, 0, 0, 3, 1, 0]
        assert game.store == [22, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_86(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 3, 1, 5, 0, 0, 0, 0, 0, 3, 1, 0]
        assert game.store == [24, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_87(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 3, 1, 5, 0, 0, 0, 0, 0, 0, 2, 1]
        assert game.store == [24, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_88(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 6, 1, 0, 0, 0, 0, 0, 2, 1]
        assert game.store == [24, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_89(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 2, 6, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_90(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 7, 2, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_91(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 7, 2, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_92(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 7, 2, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_93(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 7, 2, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_94(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 0, 7, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_95(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 0, 7, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_96(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 0, 7, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_97(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 0, 7, 0, 0, 0, 2, 0, 0, 0, 0]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_98(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 7, 0, 0, 0, 2, 0, 0, 0, 0]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_99(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 7, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_100(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 8, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_101(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 8, 0, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_102(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 1, 1, 1, 1, 3, 1, 1]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_103(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 1, 1, 0, 2, 3, 1, 1]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_104(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 1, 0, 2, 3, 1, 1]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_105(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 1, 1, 0, 0, 4, 2, 1]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_106(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 4, 2, 1]
        assert game.store == [26, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_107(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 3, 2]
        assert game.store == [26, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_108(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 3, 2]
        assert game.store == [26, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_109(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_110(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 3]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_111(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 3]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_112(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 3]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_113(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_114(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_115(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_116(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 1, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_117(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_118(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 1, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_119(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 1, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_120(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 1, 0, 1, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_121(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 1, 0, 0, 1, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_122(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 2, 0, 0, 1, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_123(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 2, 0, 0, 0, 2, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_124(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 1, 0, 2, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_125(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_126(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_127(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_128(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_129(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 2, 0, 0, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_130(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 2, 0, 0, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_131(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 2, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_132(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 2, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_133(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_134(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_135(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_136(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_137(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_138(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_139(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_140(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 2, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_141(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 2, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_142(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 2, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_143(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_144(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 3, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_145(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 3, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_146(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 3, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_147(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 3, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_148(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_149(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 3, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_150(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 3, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_151(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 4, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_152(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_153(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_154(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_155(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [26, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_156(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [26, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_157(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_158(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_159(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [26, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_160(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0]
        assert game.store == [26, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_161(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0]
        assert game.store == [26, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_162(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [29, 19]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_6_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_6_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 4, 0, 5, 5, 5, 5, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 1, 6, 5, 5, 5, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 5, 0, 7, 5, 5, 5, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [6, 6, 1, 7, 5, 5, 5, 4, 4, 4, 0, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [6, 6, 1, 7, 0, 6, 6, 5, 5, 5, 0, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 6, 1, 7, 0, 6, 6, 5, 5, 5, 0, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_7(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [7, 6, 1, 7, 0, 0, 7, 6, 6, 6, 1, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_8(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [8, 7, 1, 7, 0, 0, 0, 7, 7, 7, 2, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 7, 1, 0, 1, 1, 1, 8, 8, 8, 0, 2]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [9, 8, 1, 0, 1, 1, 1, 8, 8, 8, 0, 0]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [9, 8, 1, 0, 1, 0, 0, 8, 8, 8, 0, 0]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_12(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [10, 9, 2, 1, 1, 0, 0, 0, 9, 9, 1, 1]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [10, 9, 2, 0, 2, 0, 0, 0, 9, 9, 1, 1]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [11, 10, 3, 1, 3, 1, 0, 0, 0, 10, 2, 2]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [11, 10, 3, 1, 3, 0, 1, 0, 0, 10, 2, 2]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [11, 10, 3, 1, 3, 0, 0, 1, 0, 10, 2, 2]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [11, 10, 0, 2, 4, 1, 0, 1, 0, 10, 2, 2]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_18(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [12, 11, 1, 3, 5, 2, 1, 2, 0, 0, 3, 3]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_19(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [12, 11, 1, 3, 0, 3, 2, 3, 1, 1, 3, 3]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_20(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [12, 11, 1, 3, 0, 3, 0, 4, 2, 1, 3, 3]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_21(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 13, 2, 4, 1, 4, 1, 5, 3, 2, 4, 4]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_22(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 13, 2, 4, 1, 4, 1, 5, 3, 0, 5, 5]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_23(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 13, 0, 5, 2, 4, 1, 5, 3, 0, 5, 5]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 13, 0, 5, 2, 4, 1, 5, 0, 1, 6, 6]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_25(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 13, 0, 5, 2, 0, 2, 6, 1, 0, 6, 6]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 13, 0, 5, 2, 0, 0, 7, 2, 0, 6, 6]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 13, 0, 0, 3, 1, 1, 8, 0, 0, 6, 6]
        assert game.store == [10, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_28(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 14, 1, 1, 0, 0, 1, 8, 0, 0, 6, 0]
        assert game.store == [10, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_29(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 3, 3, 2, 1, 2, 9, 1, 1, 7, 1]
        assert game.store == [10, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_30(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 0, 3, 3, 2, 1, 0, 10, 2, 1, 7, 1]
        assert game.store == [10, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_31(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 0, 3, 0, 3, 2, 1, 10, 2, 1, 7, 1]
        assert game.store == [10, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_32(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 1, 4, 1, 0, 0, 1, 0, 3, 2, 8, 2]
        assert game.store == [10, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_33(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 1, 4, 0, 1, 0, 1, 0, 3, 2, 8, 2]
        assert game.store == [10, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_34(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 1, 4, 0, 1, 0, 0, 1, 3, 2, 8, 2]
        assert game.store == [10, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_35(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 1, 0, 1, 2, 1, 1, 1, 3, 2, 8, 2]
        assert game.store == [10, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_36(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 1, 0, 1, 2, 1, 1, 1, 0, 3, 9, 3]
        assert game.store == [10, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [3, 1, 0, 1, 2, 0, 0, 1, 0, 3, 9, 3]
        assert game.store == [12, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_38(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 2, 0, 0, 1, 0, 0, 10, 4]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_39(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 3, 0, 0, 1, 0, 0, 10, 4]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_40(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 3, 0, 0, 0, 1, 0, 10, 4]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_41(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 3, 0, 0, 0, 1, 0, 10, 4]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_42(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 2, 1, 4, 1, 1, 1, 2, 0, 0, 5]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_43(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 2, 1, 4, 0, 0, 1, 2, 0, 0, 5]
        assert game.store == [14, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_44(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 2, 3, 2, 5, 0, 0, 1, 2, 0, 0, 0]
        assert game.store == [14, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_45(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 4, 3, 5, 0, 0, 1, 2, 0, 0, 0]
        assert game.store == [14, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_46(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 0, 4, 3, 5, 0, 0, 0, 3, 0, 0, 0]
        assert game.store == [14, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_47(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 0, 4, 0, 6, 1, 1, 0, 3, 0, 0, 0]
        assert game.store == [14, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_48(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 0, 4, 0, 6, 1, 1, 0, 0, 1, 1, 1]
        assert game.store == [14, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_49(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 0, 4, 0, 0, 2, 2, 1, 1, 0, 0, 1]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_50(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 0, 4, 0, 0, 2, 2, 1, 0, 1, 0, 1]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_51(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 5, 0, 0, 2, 2, 1, 0, 1, 0, 1]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_52(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 5, 0, 0, 2, 0, 2, 1, 1, 0, 1]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_53(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 3, 1, 0, 1, 1, 0, 1]
        assert game.store == [21, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_54(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 3, 1, 0, 0, 2, 0, 1]
        assert game.store == [21, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_55(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 2, 3, 1, 0, 0, 2, 0, 1]
        assert game.store == [21, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_56(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 2, 3, 1, 0, 0, 2, 0, 0]
        assert game.store == [21, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_57(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 2, 0, 2, 1, 1, 2, 0, 0]
        assert game.store == [21, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_58(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 2, 0, 0, 2, 2, 2, 0, 0]
        assert game.store == [21, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_59(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 2, 0, 0, 2, 2, 2, 0, 0]
        assert game.store == [21, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_60(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 2, 0, 0, 0, 3, 3, 0, 0]
        assert game.store == [21, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_61(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 1, 1, 0, 3, 3, 0, 0]
        assert game.store == [21, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_62(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 1, 1, 0, 0, 4, 1, 1]
        assert game.store == [21, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_63(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 0, 0, 4, 1, 1]
        assert game.store == [23, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_64(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 0, 0, 4, 0, 2]
        assert game.store == [23, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_65(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 4, 0, 2]
        assert game.store == [23, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_66(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 3]
        assert game.store == [23, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_67(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 3]
        assert game.store == [23, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_68(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 4]
        assert game.store == [23, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_69(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 4]
        assert game.store == [23, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_70(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [23, 25]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_7_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
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
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 5, 4, 4, 0, 5, 5, 5, 5, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [6, 6, 4, 4, 0, 5, 5, 5, 0, 1, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [6, 0, 5, 5, 1, 6, 6, 6, 0, 1, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 1, 6, 6, 2, 7, 6, 6, 0, 1, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [7, 1, 0, 7, 3, 8, 7, 7, 1, 1, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [8, 2, 1, 8, 0, 8, 7, 7, 1, 1, 0, 1]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 2, 1, 0, 1, 9, 8, 8, 2, 2, 1, 0]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [9, 3, 2, 1, 1, 9, 8, 0, 3, 3, 2, 1]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [9, 3, 2, 1, 0, 10, 8, 0, 3, 3, 2, 1]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [10, 3, 2, 1, 0, 10, 8, 0, 3, 3, 0, 2]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [10, 3, 2, 0, 1, 10, 8, 0, 3, 3, 0, 2]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_13(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [11, 0, 2, 0, 1, 10, 8, 0, 3, 3, 0, 0]
        assert game.store == [2, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 3, 1, 2, 11, 9, 1, 4, 4, 1, 1]
        assert game.store == [2, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_15(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 3, 1, 2, 11, 9, 1, 4, 4, 0, 2]
        assert game.store == [2, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 4, 2, 3, 0, 10, 2, 5, 5, 1, 3]
        assert game.store == [2, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 3, 5, 2, 3, 0, 10, 2, 5, 0, 2, 4]
        assert game.store == [2, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_18(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 3, 0, 3, 4, 1, 11, 0, 5, 0, 2, 4]
        assert game.store == [5, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 3, 0, 3, 4, 1, 11, 0, 5, 0, 0, 5]
        assert game.store == [5, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_20(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 3, 0, 3, 4, 0, 12, 0, 5, 0, 0, 5]
        assert game.store == [5, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_21(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 4, 1, 4, 5, 0, 12, 0, 5, 0, 0, 0]
        assert game.store == [5, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_22(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 4, 0, 5, 5, 0, 12, 0, 5, 0, 0, 0]
        assert game.store == [5, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 5, 1, 6, 6, 1, 0, 2, 6, 1, 1, 1]
        assert game.store == [5, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 2, 7, 7, 2, 1, 2, 6, 1, 1, 1]
        assert game.store == [5, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_25(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 2, 7, 7, 2, 1, 2, 6, 1, 1, 0]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_26(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 2, 7, 0, 3, 2, 3, 7, 2, 2, 1]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_27(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 2, 7, 0, 3, 2, 3, 7, 2, 0, 2]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 2, 7, 0, 0, 3, 4, 8, 2, 0, 2]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_29(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 2, 7, 0, 0, 0, 5, 9, 3, 0, 2]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_30(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 2, 7, 0, 0, 0, 5, 9, 3, 0, 2]
        assert game.store == [5, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_31(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 2, 7, 0, 0, 0, 5, 9, 3, 0, 0]
        assert game.store == [5, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 2, 7, 0, 0, 0, 5, 9, 3, 0, 0]
        assert game.store == [5, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_33(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 2, 7, 0, 0, 0, 5, 9, 0, 1, 1]
        assert game.store == [5, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_34(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 3, 7, 0, 0, 0, 5, 9, 0, 1, 1]
        assert game.store == [5, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_35(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 3, 7, 0, 0, 0, 0, 10, 1, 2, 2]
        assert game.store == [5, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_36(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 8, 1, 1, 0, 0, 10, 1, 2, 2]
        assert game.store == [5, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_37(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 8, 1, 1, 0, 0, 10, 0, 3, 2]
        assert game.store == [5, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_38(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 8, 1, 0, 1, 0, 10, 0, 3, 2]
        assert game.store == [5, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_39(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 8, 1, 0, 0, 1, 10, 0, 3, 2]
        assert game.store == [5, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_40(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 8, 0, 1, 0, 1, 10, 0, 3, 2]
        assert game.store == [5, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_41(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 8, 0, 1, 0, 1, 10, 0, 3, 0]
        assert game.store == [5, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_42(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 0, 8, 0, 0, 1, 1, 10, 0, 3, 0]
        assert game.store == [5, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_43(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 0, 8, 0, 0, 1, 0, 11, 0, 3, 0]
        assert game.store == [5, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_44(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 8, 0, 0, 1, 0, 11, 0, 3, 0]
        assert game.store == [5, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_45(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 8, 0, 0, 1, 0, 11, 0, 0, 1]
        assert game.store == [5, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_46(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 1, 2, 1, 12, 1, 1, 0]
        assert game.store == [7, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 2, 13, 1, 1, 0]
        assert game.store == [7, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_48(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 1, 0, 2, 13, 1, 1, 0]
        assert game.store == [7, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_49(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 1, 0, 2, 13, 0, 2, 0]
        assert game.store == [7, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_50(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 1, 2, 13, 0, 2, 0]
        assert game.store == [7, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_51(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 1, 0, 14, 1, 2, 0]
        assert game.store == [7, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_52(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 1, 0, 14, 1, 2, 0]
        assert game.store == [7, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_53(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 2, 1, 2, 1, 2, 1, 0, 3, 4, 2]
        assert game.store == [7, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_54(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 2, 1, 2, 0, 0, 1, 0, 3, 4, 2]
        assert game.store == [10, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_55(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 2, 0, 0, 1, 0, 3, 0, 3]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_56(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 3, 0, 0, 1, 0, 3, 0, 3]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_57(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 3, 0, 0, 0, 1, 3, 0, 3]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_58(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 1, 1, 3, 0, 3]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_59(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 4]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_60(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 4]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_61(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 5]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_62(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 5]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_63(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_64(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 2, 1, 0, 2, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_65(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 2, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_66(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 1, 2, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_67(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 0, 1, 2, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_68(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 3, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_69(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 3, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_70(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 3, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_71(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 3, 0, 0, 3, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_72(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_73(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_74(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_75(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1]
        assert game.store == [12, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_76(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_77(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_78(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_79(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 1, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_80(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 1, 1, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_81(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_82(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_83(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 2]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_84(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 2]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_85(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 2, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_86(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 2, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_87(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 2, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_88(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_89(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 2, 0, 0, 1, 0, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_90(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 3, 0, 0, 1, 0, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_91(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 3, 0, 0, 0, 1, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_92(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_93(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 0, 2, 1, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_94(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 1, 0, 2, 1, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_95(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 1, 2, 1, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_96(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 1, 2, 1, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_97(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 3, 1, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_98(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 3, 1, 0, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_99(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 3, 0, 1, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_100(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 1, 0]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_101(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 2, 1]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_102(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 2, 1]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_103(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 3, 1]
        assert game.store == [14, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_104(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1]
        assert game.store == [16, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_105(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
        assert game.store == [16, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_106(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
        assert game.store == [16, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_107(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [16, 32]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_8_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_8_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 4, 0, 5, 5, 5, 5, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [5, 5, 0, 5, 5, 5, 5, 4, 4, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 6, 1, 6, 6, 6, 5, 4, 4, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_4(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 6, 1, 6, 6, 6, 5, 4, 0, 1, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 6, 1, 6, 0, 7, 6, 5, 1, 2, 7, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 6, 1, 6, 0, 7, 6, 5, 1, 0, 8, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 7, 1, 8, 7, 6, 1, 0, 8, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_8(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 1, 2, 7, 1, 8, 7, 0, 2, 1, 9, 8]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 3, 7, 1, 8, 7, 0, 2, 1, 9, 8]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 1, 4, 8, 2, 9, 8, 1, 2, 1, 9, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 1, 4, 0, 3, 10, 9, 2, 3, 2, 10, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_12(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [4, 2, 5, 1, 4, 11, 10, 3, 4, 2, 0, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 2, 5, 1, 0, 12, 11, 4, 5, 2, 0, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_14(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 2, 5, 1, 0, 12, 11, 0, 6, 3, 1, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 3, 6, 2, 1, 0, 13, 1, 7, 4, 2, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 0, 6, 2, 1, 0, 13, 1, 7, 0, 3, 5]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_17(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [6, 0, 6, 2, 0, 1, 13, 1, 7, 0, 3, 5]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [7, 1, 7, 3, 1, 2, 0, 3, 9, 1, 4, 6]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 0, 8, 3, 1, 2, 0, 3, 9, 1, 4, 6]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_20(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [8, 1, 9, 0, 0, 0, 0, 3, 0, 2, 5, 7]
        assert game.store == [0, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_21(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 10, 1, 1, 1, 1, 4, 1, 2, 5, 7]
        assert game.store == [0, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_22(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 10, 1, 1, 1, 1, 0, 2, 3, 6, 8]
        assert game.store == [0, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 10, 1, 1, 0, 0, 0, 2, 3, 6, 8]
        assert game.store == [2, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_24(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 10, 1, 1, 0, 0, 0, 2, 0, 7, 9]
        assert game.store == [2, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_25(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 2, 10, 1, 0, 1, 0, 0, 2, 0, 7, 9]
        assert game.store == [2, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_26(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 3, 11, 2, 1, 0, 0, 0, 2, 0, 0, 10]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_27(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 4, 12, 2, 1, 0, 0, 0, 2, 0, 0, 10]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_28(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 4, 12, 2, 1, 0, 0, 0, 0, 1, 1, 10]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_29(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 13, 3, 2, 1, 0, 0, 0, 1, 1, 10]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_30(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 13, 3, 2, 1, 0, 0, 0, 1, 0, 11]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 0, 5, 4, 2, 1, 1, 1, 2, 1, 12]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_32(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 0, 5, 4, 2, 1, 0, 2, 2, 1, 12]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_33(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 5, 4, 2, 1, 0, 2, 2, 1, 12]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_34(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 5, 4, 2, 1, 0, 0, 3, 2, 12]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_35(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 0, 5, 4, 0, 2, 1, 0, 3, 2, 12]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_36(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 2, 0, 5, 4, 0, 2, 1, 0, 3, 0, 13]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_37(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 2, 0, 5, 0, 1, 3, 2, 1, 3, 0, 13]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_38(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 1, 6, 1, 2, 4, 3, 2, 4, 1, 0]
        assert game.store == [2, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_39(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 3, 5, 4, 3, 5, 1, 0]
        assert game.store == [2, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_40(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 2, 3, 5, 4, 0, 6, 2, 1]
        assert game.store == [2, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_41(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 2, 3, 5, 4, 0, 6, 2, 1]
        assert game.store == [2, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_42(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 2, 3, 5, 4, 0, 0, 3, 2]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_43(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 2, 3, 5, 4, 0, 0, 3, 2]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_44(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 1, 2, 0, 2, 3, 5, 4, 0, 0, 0, 3]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_45(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 3, 0, 2, 3, 5, 4, 0, 0, 0, 3]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_46(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 0, 3, 0, 2, 3, 0, 5, 1, 1, 1, 4]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_47(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 0, 3, 0, 0, 4, 1, 5, 1, 1, 1, 4]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_48(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 0, 3, 0, 0, 4, 1, 5, 1, 1, 0, 5]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_49(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 4, 0, 0, 4, 1, 5, 1, 1, 0, 5]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_50(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 5, 1, 1, 4, 1, 5, 1, 1, 0, 0]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_51(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 2, 5, 1, 0, 5, 1, 5, 1, 1, 0, 0]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_52(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 5, 1, 0, 5, 1, 5, 0, 2, 0, 0]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_53(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 2, 1, 6, 2, 6, 0, 2, 0, 0]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_54(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 0, 2, 1, 6, 2, 6, 0, 0, 1, 1]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_55(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 2, 7, 2, 6, 0, 0, 1, 1]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_56(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 2, 7, 2, 6, 0, 0, 0, 2]
        assert game.store == [2, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_57(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 0, 8, 0, 6, 0, 0, 0, 2]
        assert game.store == [5, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_58(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 8, 0, 6, 0, 0, 0, 0]
        assert game.store == [5, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_59(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 7, 1, 1, 1, 1]
        assert game.store == [5, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_60(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 2, 1, 0, 0, 0, 1, 0, 2, 2, 2, 2]
        assert game.store == [5, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_61(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 2, 0, 0, 0, 1, 0, 2, 2, 2, 2]
        assert game.store == [5, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_62(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 3, 2, 0, 0, 0, 0, 1, 2, 2, 2, 2]
        assert game.store == [5, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_63(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 3, 0, 1, 1, 0, 0, 1, 2, 2, 2, 2]
        assert game.store == [5, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_64(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 0, 1, 1, 0, 0, 1, 0, 3, 3, 2]
        assert game.store == [5, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_65(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 2, 0, 0, 1, 0, 3, 3, 2]
        assert game.store == [5, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_66(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 2, 0, 0, 1, 0, 3, 0, 3]
        assert game.store == [5, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_67(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 2, 0, 0, 1, 0, 3, 0, 3]
        assert game.store == [5, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_68(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 2, 0, 0, 0, 1, 3, 0, 3]
        assert game.store == [5, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_69(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 0, 1, 3, 0, 3]
        assert game.store == [5, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_70(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 0, 0, 4, 0, 3]
        assert game.store == [5, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_71(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 1, 0, 0, 4, 0, 3]
        assert game.store == [5, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_72(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 0, 0, 4, 0, 0]
        assert game.store == [5, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_73(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 0, 4, 0, 0]
        assert game.store == [5, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_74(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 1, 0, 1, 0, 4, 0, 0]
        assert game.store == [5, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_75(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 1, 0, 1, 0, 4, 0, 0]
        assert game.store == [5, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_76(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1]
        assert game.store == [5, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_77(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1]
        assert game.store == [5, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_78(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1]
        assert game.store == [5, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_79(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1]
        assert game.store == [5, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_80(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 2]
        assert game.store == [5, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_81(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 2]
        assert game.store == [5, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_82(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0]
        assert game.store == [5, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_83(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [8, 40]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_9_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_9_move_1(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 5, 5, 0, 5, 5, 5, 5, 4, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [6, 5, 5, 0, 5, 5, 5, 0, 5, 5, 1, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [6, 5, 0, 1, 6, 6, 6, 1, 5, 5, 1, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [7, 6, 0, 1, 6, 6, 6, 1, 0, 6, 2, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 6, 0, 0, 7, 6, 6, 1, 0, 6, 2, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [8, 7, 1, 1, 7, 6, 6, 1, 0, 0, 3, 8]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_8(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [8, 7, 1, 1, 7, 0, 7, 2, 1, 1, 4, 9]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [8, 7, 1, 1, 7, 0, 7, 0, 2, 2, 4, 9]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 8, 2, 2, 8, 1, 8, 1, 0, 2, 4, 9]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_11(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 8, 2, 2, 8, 1, 8, 1, 0, 0, 5, 10]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 8, 2, 2, 8, 0, 9, 1, 0, 0, 5, 10]
        assert game.store == [3, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_13(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 9, 0, 0, 8, 0, 9, 1, 0, 0, 0, 11]
        assert game.store == [3, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 10, 0, 0, 8, 0, 9, 1, 0, 0, 0, 11]
        assert game.store == [3, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 11, 1, 1, 8, 0, 0, 2, 1, 1, 1, 12]
        assert game.store == [3, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 12, 1, 1, 8, 0, 0, 2, 1, 1, 1, 12]
        assert game.store == [3, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_17(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 13, 2, 2, 9, 1, 1, 3, 2, 2, 2, 0]
        assert game.store == [3, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 13, 2, 2, 9, 0, 0, 3, 2, 2, 2, 0]
        assert game.store == [5, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_19(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 13, 2, 2, 9, 0, 0, 3, 2, 0, 3, 1]
        assert game.store == [5, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_20(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 14, 2, 2, 0, 1, 1, 4, 3, 1, 4, 2]
        assert game.store == [5, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_21(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 14, 2, 2, 0, 1, 1, 4, 3, 0, 5, 2]
        assert game.store == [5, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 4, 4, 2, 2, 2, 5, 4, 1, 6, 3]
        assert game.store == [5, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_23(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [3, 1, 5, 4, 2, 2, 2, 5, 4, 1, 6, 0]
        assert game.store == [5, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 1, 5, 0, 3, 3, 3, 6, 4, 1, 6, 0]
        assert game.store == [5, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_25(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 1, 5, 0, 3, 3, 0, 7, 5, 2, 6, 0]
        assert game.store == [5, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_26(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [3, 1, 5, 0, 0, 4, 1, 8, 5, 2, 6, 0]
        assert game.store == [5, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 1, 5, 0, 0, 4, 1, 8, 5, 0, 7, 1]
        assert game.store == [5, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_28(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 1, 0, 1, 1, 5, 2, 9, 5, 0, 7, 1]
        assert game.store == [5, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_29(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 2, 1, 0, 0, 5, 2, 0, 6, 1, 8, 2]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 2, 0, 1, 0, 5, 2, 0, 6, 1, 8, 2]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 2, 0, 1, 0, 5, 2, 0, 6, 0, 9, 2]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_32(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 2, 0, 1, 0, 0, 3, 1, 7, 1, 10, 2]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_33(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 2, 0, 1, 0, 0, 3, 0, 8, 1, 10, 2]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_34(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 0, 1, 2, 0, 0, 3, 0, 8, 1, 10, 2]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_35(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 1, 2, 3, 1, 0, 3, 0, 0, 2, 11, 3]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_36(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 3, 4, 2, 1, 3, 0, 0, 2, 11, 3]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 3, 4, 2, 1, 0, 1, 1, 3, 11, 3]
        assert game.store == [5, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_38(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 3, 0, 3, 2, 1, 0, 1, 3, 11, 3]
        assert game.store == [7, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_39(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 3, 0, 3, 2, 0, 1, 1, 3, 11, 3]
        assert game.store == [7, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_40(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 3, 0, 3, 0, 1, 0, 1, 3, 11, 3]
        assert game.store == [9, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_41(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 3, 0, 3, 0, 1, 0, 0, 4, 11, 3]
        assert game.store == [9, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_42(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 4, 1, 3, 0, 1, 0, 0, 4, 11, 3]
        assert game.store == [9, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_43(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 4, 1, 3, 0, 1, 0, 0, 0, 12, 4]
        assert game.store == [9, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_44(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 4, 1, 3, 0, 1, 0, 0, 0, 12, 4]
        assert game.store == [9, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_45(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 3, 5, 2, 4, 1, 2, 1, 1, 1, 0, 6]
        assert game.store == [9, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_46(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 3, 5, 0, 5, 2, 2, 1, 1, 1, 0, 6]
        assert game.store == [9, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_47(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 4, 6, 1, 6, 0, 2, 1, 1, 1, 0, 0]
        assert game.store == [9, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_48(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 4, 6, 0, 7, 0, 2, 1, 1, 1, 0, 0]
        assert game.store == [9, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_49(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 4, 6, 0, 7, 0, 2, 0, 2, 1, 0, 0]
        assert game.store == [9, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_50(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 4, 0, 1, 8, 1, 3, 1, 0, 1, 0, 0]
        assert game.store == [12, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_51(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 4, 0, 1, 8, 1, 3, 0, 1, 1, 0, 0]
        assert game.store == [12, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_52(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 4, 0, 1, 8, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [16, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_53(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 4, 0, 1, 8, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [16, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_54(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 1, 2, 9, 1, 0, 0, 0, 2, 0, 0]
        assert game.store == [16, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_55(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 0, 1, 2, 9, 1, 0, 0, 0, 0, 1, 1]
        assert game.store == [16, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_56(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 0, 0, 3, 9, 1, 0, 0, 0, 0, 1, 1]
        assert game.store == [16, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_57(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 9, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_58(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 10, 2, 1, 0, 0, 0, 1, 0]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_59(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 10, 2, 1, 0, 0, 0, 0, 1]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_60(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 3, 2, 1, 1, 1, 1, 2]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_61(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 3, 2, 1, 0, 2, 1, 2]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_62(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 3, 2, 1, 0, 2, 1, 2]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_63(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 0, 3, 2, 0, 1, 2, 1, 2]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_64(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 1, 0, 3, 2, 0, 1, 2, 1, 2]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_65(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 2, 1, 0, 3, 2, 0, 1, 2, 1, 0]
        assert game.store == [16, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_66(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 2, 1, 0, 0, 3, 1, 0, 2, 1, 0]
        assert game.store == [18, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_67(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 2, 1, 0, 0, 0, 2, 1, 3, 1, 0]
        assert game.store == [18, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_68(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 3, 1, 0, 0, 0, 2, 1, 3, 1, 0]
        assert game.store == [18, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_69(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 3, 1, 0, 0, 0, 2, 1, 0, 2, 1]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_70(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 3, 0, 1, 0, 0, 2, 1, 0, 2, 1]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_71(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 1, 0, 0, 0, 2, 1, 2, 1]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_72(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 3, 0, 0, 1, 0, 0, 2, 1, 2, 1]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_73(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 0, 1, 0, 0, 0, 2, 3, 1]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_74(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 2, 0, 0, 0, 2, 3, 1]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_75(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 1, 2, 0, 0, 0, 2, 0, 2]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_76(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 0, 1, 0, 3, 0, 0, 0, 2, 0, 2]
        assert game.store == [18, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_77(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 3, 0, 0, 0, 2, 0, 0]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_78(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 1, 1, 2, 0, 0]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_79(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 1, 0, 3, 0, 0]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_80(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 1, 0, 3, 0, 0]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_81(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_82(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_83(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_84(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_85(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_86(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_87(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_88(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_89(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_90(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 1, 0, 1, 1, 0, 0, 1]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_91(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 1, 0, 1, 0, 1, 0, 1]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_92(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 1, 0, 1, 0, 1]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_93(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 1, 1]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_94(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_95(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 2]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_96(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 2]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_97(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 2]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_98(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 2]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_99(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 2]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_100(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 0, 2]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_101(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 1, 0, 1, 0, 2]
        assert game.store == [18, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_102(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_103(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_104(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_105(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_106(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_107(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_108(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_109(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_110(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_111(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_112(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_113(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_114(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_115(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_116(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_117(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_118(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_119(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_120(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_121(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_122(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_123(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_124(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_125(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_126(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_127(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_128(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_129(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_130(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_131(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_132(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_133(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_134(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_135(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_136(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_137(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_138(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_139(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_140(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_141(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_142(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_143(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_144(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_145(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_146(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 2, 0]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_147(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_148(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [20, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_149(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [20, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_150(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [20, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_151(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [20, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_152(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [20, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_153(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [20, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_154(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [20, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_155(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [20, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_156(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [22, 26]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_10_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_10_move_1(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_2(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 6, 6, 5, 5, 4, 4, 4, 4, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 7, 6, 6, 5, 5, 5, 4, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 1, 8, 7, 7, 5, 5, 5, 4, 4, 0, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 1, 8, 7, 0, 6, 6, 6, 5, 5, 1, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 8, 7, 0, 6, 0, 7, 6, 6, 2, 2]
        assert game.store == [0, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_7(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 8, 7, 0, 0, 1, 8, 7, 7, 0, 0]
        assert game.store == [6, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_8(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 9, 8, 1, 0, 1, 8, 7, 0, 1, 1]
        assert game.store == [6, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 2, 9, 0, 2, 1, 2, 9, 8, 1, 0, 0]
        assert game.store == [10, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 3, 10, 1, 0, 1, 2, 0, 9, 2, 1, 1]
        assert game.store == [10, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_11(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 3, 0, 2, 1, 2, 3, 1, 10, 3, 2, 2]
        assert game.store == [10, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 3, 0, 2, 1, 2, 0, 2, 11, 4, 2, 2]
        assert game.store == [10, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 3, 0, 0, 2, 3, 0, 2, 11, 4, 2, 2]
        assert game.store == [10, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 3, 0, 2, 11, 0, 3, 3]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_15(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 4, 1, 2, 11, 0, 3, 3]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 4, 1, 2, 11, 0, 3, 0]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 0, 2, 3, 12, 1, 3, 0]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 0, 0, 4, 13, 1, 3, 0]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 0, 0, 4, 13, 1, 3, 0]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_20(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 1, 3, 1, 1, 1, 1, 5, 0, 3, 5, 1]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 3, 0, 2, 1, 1, 5, 0, 3, 5, 1]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 2, 4, 1, 2, 1, 1, 5, 0, 3, 0, 2]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_23(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 0, 5, 2, 2, 1, 1, 5, 0, 3, 0, 2]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_24(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 1, 5, 2, 2, 1, 1, 5, 0, 3, 0, 0]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_25(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 1, 5, 2, 2, 0, 0, 5, 0, 3, 0, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_26(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [5, 1, 5, 2, 2, 0, 0, 0, 1, 4, 1, 1]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_27(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 1, 5, 2, 0, 1, 1, 0, 1, 4, 1, 1]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_28(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 1, 5, 2, 0, 1, 1, 0, 0, 5, 1, 1]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_29(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 6, 3, 1, 2, 1, 0, 0, 5, 1, 1]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 3, 7, 3, 1, 2, 1, 0, 0, 0, 2, 2]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 3, 0, 4, 2, 3, 2, 1, 1, 1, 2, 2]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 3, 0, 4, 2, 3, 2, 1, 0, 2, 2, 2]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_33(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 5, 3, 3, 2, 1, 0, 2, 2, 2]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_34(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 5, 3, 3, 0, 2, 1, 2, 2, 2]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_35(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 4, 4, 1, 0, 0, 2, 2, 2]
        assert game.store == [17, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_36(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 4, 4, 0, 1, 0, 2, 2, 2]
        assert game.store == [17, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_37(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 4, 4, 0, 1, 0, 2, 2, 2]
        assert game.store == [17, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_38(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 4, 4, 0, 1, 0, 2, 2, 0]
        assert game.store == [17, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_39(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 1, 0, 1, 4, 0, 1, 2, 1, 0, 2, 0]
        assert game.store == [20, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_40(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 4, 0, 1, 2, 1, 0, 0, 1]
        assert game.store == [20, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_41(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 4, 0, 1, 2, 1, 0, 0, 1]
        assert game.store == [20, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_42(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 4, 0, 1, 0, 2, 1, 0, 1]
        assert game.store == [20, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_43(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 5, 0, 1, 0, 2, 1, 0, 1]
        assert game.store == [20, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_44(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 5, 0, 1, 0, 0, 2, 1, 1]
        assert game.store == [20, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_45(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 2, 1, 1, 0, 1, 1]
        assert game.store == [23, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_46(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 2, 1, 1, 0, 0, 2]
        assert game.store == [23, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_48(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_49(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_50(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_51(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_52(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_53(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_54(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 3]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_55(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 3]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_56(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_57(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_58(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_59(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_60(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_61(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_62(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_63(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_64(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_65(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_66(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 2, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_67(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_68(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_69(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_70(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_71(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_72(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_73(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_74(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_75(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 2, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_76(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_77(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_78(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_79(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_80(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_81(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_82(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_83(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_84(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_85(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_86(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_87(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_88(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_89(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_90(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_91(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_92(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 3]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_93(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 3]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_94(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_95(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 3]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_96(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_97(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_98(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_99(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_100(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_101(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_102(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 1, 0, 0, 0, 2, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_103(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 2, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_104(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_105(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_106(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_107(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_108(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_109(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_110(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_111(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_112(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_113(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_114(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_115(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_116(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_117(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_118(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_119(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_120(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_121(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_122(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_123(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_124(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_125(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_126(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_127(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_128(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_129(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_130(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_131(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_132(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 0, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_133(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 0, 2, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_134(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_135(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_136(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_137(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 2]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_138(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_139(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_140(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_141(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_142(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_143(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_144(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 3, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_145(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_146(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_147(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 2, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_148(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 2, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_149(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 2, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_150(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 2, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_151(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_152(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_153(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_154(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_155(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_156(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_157(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_158(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_159(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_160(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 20]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_11_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_11_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 4, 4, 4, 4, 4, 4, 4, 0, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 4, 0, 5, 5, 5, 5, 4, 0, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [5, 4, 0, 5, 5, 5, 5, 0, 1, 6, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 4, 0, 5, 5, 0, 6, 1, 2, 7, 7, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_5(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 5, 1, 6, 6, 0, 6, 1, 2, 0, 8, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [6, 5, 0, 7, 6, 0, 6, 1, 2, 0, 8, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [6, 5, 0, 7, 6, 0, 6, 0, 3, 0, 8, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 6, 1, 8, 7, 1, 7, 0, 3, 0, 8, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_9(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 7, 1, 8, 7, 1, 0, 1, 4, 1, 9, 8]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 8, 1, 8, 7, 1, 0, 1, 4, 1, 9, 8]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 9, 2, 9, 8, 2, 1, 2, 4, 1, 0, 9]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_12(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 10, 2, 9, 8, 2, 1, 2, 4, 1, 0, 9]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_13(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 10, 2, 9, 8, 2, 0, 3, 4, 1, 0, 9]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 10, 0, 10, 9, 2, 0, 3, 4, 1, 0, 9]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 11, 1, 11, 10, 3, 1, 4, 5, 1, 0, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 11, 0, 12, 10, 3, 1, 4, 5, 1, 0, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 11, 0, 12, 10, 3, 1, 4, 5, 0, 1, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 1, 13, 11, 4, 2, 5, 6, 1, 2, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 0, 1, 13, 11, 4, 0, 6, 7, 1, 2, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_20(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [3, 1, 2, 14, 0, 5, 1, 7, 8, 2, 3, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [4, 2, 3, 15, 1, 5, 1, 7, 0, 3, 4, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_22(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 4, 16, 2, 5, 1, 7, 0, 3, 4, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 3, 4, 16, 2, 5, 0, 8, 0, 3, 4, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 4, 5, 0, 4, 7, 2, 10, 0, 4, 5, 4]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_25(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 5, 6, 1, 4, 7, 2, 10, 0, 4, 0, 5]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 5, 0, 2, 5, 8, 3, 11, 1, 4, 0, 5]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 6, 0, 2, 5, 8, 3, 11, 1, 0, 1, 6]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 7, 0, 2, 5, 0, 4, 12, 2, 1, 2, 7]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_29(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 8, 1, 3, 6, 1, 5, 12, 2, 1, 2, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_30(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 0, 2, 4, 7, 2, 6, 13, 0, 0, 2, 0]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_31(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [6, 0, 2, 4, 7, 2, 6, 13, 0, 0, 0, 1]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 0, 2, 0, 8, 3, 7, 14, 0, 0, 0, 1]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_33(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [7, 1, 3, 1, 9, 4, 8, 0, 2, 2, 2, 2]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_34(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [8, 2, 3, 1, 0, 5, 9, 1, 3, 3, 3, 3]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_35(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [9, 0, 3, 1, 0, 5, 9, 1, 3, 3, 0, 4]
        assert game.store == [7, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_36(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [9, 0, 3, 0, 1, 5, 9, 1, 3, 3, 0, 4]
        assert game.store == [7, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_37(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [10, 0, 3, 0, 1, 5, 9, 1, 3, 0, 1, 5]
        assert game.store == [7, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_38(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 4, 1, 2, 6, 10, 2, 4, 1, 0, 5]
        assert game.store == [9, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_39(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 4, 1, 2, 6, 10, 0, 5, 2, 0, 5]
        assert game.store == [9, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_40(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 5, 1, 2, 6, 10, 0, 5, 2, 0, 5]
        assert game.store == [9, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_41(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 6, 0, 0, 6, 10, 0, 5, 2, 0, 0]
        assert game.store == [9, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_42(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 6, 0, 0, 0, 11, 1, 6, 3, 1, 1]
        assert game.store == [9, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_43(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 2, 7, 0, 0, 0, 11, 1, 0, 4, 2, 2]
        assert game.store == [9, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_44(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 2, 0, 1, 1, 1, 12, 2, 1, 5, 2, 2]
        assert game.store == [9, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_45(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 1, 1, 12, 2, 1, 5, 0, 3]
        assert game.store == [9, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_46(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 0, 2, 12, 2, 1, 5, 0, 3]
        assert game.store == [9, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_47(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 0, 2, 12, 2, 0, 6, 0, 3]
        assert game.store == [9, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_48(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 0, 2, 12, 2, 0, 6, 0, 3]
        assert game.store == [9, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_49(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 0, 2, 12, 0, 1, 7, 0, 3]
        assert game.store == [9, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_50(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 3, 12, 0, 1, 7, 0, 3]
        assert game.store == [9, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_51(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 2, 1, 2, 4, 0, 2, 2, 8, 1, 4]
        assert game.store == [9, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_52(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 0, 2, 3, 4, 0, 2, 2, 8, 1, 4]
        assert game.store == [9, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_53(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 2, 1, 0, 3, 4, 0, 2, 2, 8, 1, 0]
        assert game.store == [9, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_54(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 2, 1, 3, 4, 0, 2, 2, 8, 1, 0]
        assert game.store == [9, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_55(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 1, 3, 2, 4, 5, 0, 2, 2, 0, 2, 1]
        assert game.store == [9, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_56(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 1, 3, 0, 5, 6, 0, 2, 2, 0, 2, 1]
        assert game.store == [9, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_57(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 1, 3, 0, 5, 6, 0, 2, 2, 0, 2, 0]
        assert game.store == [9, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_58(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 3, 0, 5, 0, 1, 3, 3, 1, 3, 1]
        assert game.store == [9, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_59(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 3, 0, 5, 0, 1, 3, 3, 0, 4, 1]
        assert game.store == [9, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_60(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 6, 1, 1, 3, 3, 0, 4, 1]
        assert game.store == [9, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_61(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 6, 1, 1, 0, 4, 1, 5, 1]
        assert game.store == [9, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_62(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 6, 0, 0, 0, 4, 1, 5, 1]
        assert game.store == [11, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_63(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 6, 0, 0, 0, 0, 2, 6, 2]
        assert game.store == [11, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_64(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 7, 0, 0, 0, 0, 2, 6, 2]
        assert game.store == [11, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_65(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 7, 0, 0, 0, 0, 0, 7, 3]
        assert game.store == [11, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_66(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 7, 0, 0, 0, 0, 0, 7, 3]
        assert game.store == [11, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_67(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 1, 2, 1, 8, 1, 0, 0, 0, 0, 0, 4]
        assert game.store == [11, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_68(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 3, 1, 8, 1, 0, 0, 0, 0, 0, 4]
        assert game.store == [11, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_69(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 8, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [11, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_70(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1]
        assert game.store == [11, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_71(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 0, 0, 0, 0, 2, 1, 1, 0, 2, 1, 1]
        assert game.store == [11, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_72(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 2, 1, 1, 0, 2, 1, 1]
        assert game.store == [11, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_73(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 2, 1, 1, 0, 2, 1, 0]
        assert game.store == [11, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_74(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 1, 0]
        assert game.store == [15, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_75(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1]
        assert game.store == [15, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_76(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1]
        assert game.store == [15, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_77(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2]
        assert game.store == [15, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_78(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2]
        assert game.store == [15, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_79(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3]
        assert game.store == [15, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_80(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3]
        assert game.store == [15, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_81(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [15, 33]
        assert cond.name == "WIN"
        assert game.mdata.winner is True
        assert game.rtally.score == [3, 10]
        gstate.cond = cond
