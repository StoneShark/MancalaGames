# -*- coding: utf-8 -*-
"""Test giuthi

Created on Thu Jul 11 17:56:04 2024
@author: Ann"""

import pytest
pytestmark = pytest.mark.integtest

from context import game_interface as gi
from context import man_config


CW = gi.Direct.CW
CCW = gi.Direct.CCW

N = None
T = True
F = False


class GameTestData:
    """allow passing move end cond between tests."""

    def __init__(self, game):
        self.game = game
        self.cond = None


@pytest.fixture(scope="class")
def gstate():
    """This fixture will maintain state between tests in the
    same class but will be reconstructed for each class."""

    game, _ = man_config.make_game('./GameProps/Giuthi.txt')
    gstate = GameTestData(game)
    return gstate



@pytest.mark.incremental
class TestGiuthiTWin:

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = True
        game.starter = True
        assert game.board == [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move((6, CCW))
        assert game.turn is True
        assert game.board == [6, 6, 6, 6, 6, 6, 6, 6, 0, 2, 9, 9, 9, 9, 9, 1]
        assert game.store == [0, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [9, 9, 9, 9, 1, 7, 7, 0, 0, 2, 9, 0, 10, 0, 12, 4]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [11, 11, 11, 11, 3, 1, 8, 1, 1, 3, 10, 1, 10, 0, 0, 6]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [11, 11, 11, 11, 3, 1, 8, 1, 1, 0, 12, 0, 14, 1, 2, 1]
        assert game.store == [0, 8]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [1, 12, 12, 12, 1, 0, 0, 0, 6, 0, 0, 4, 18, 1, 2, 4]
        assert game.store == [0, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [2, 0, 12, 12, 1, 0, 1, 1, 7, 1, 0, 5, 19, 2, 3, 5]
        assert game.store == [2, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [2, 0, 12, 12, 1, 0, 1, 1, 7, 1, 1, 6, 20, 3, 4, 0]
        assert game.store == [2, 23]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 12, 1, 0, 1, 1, 7, 1, 1, 6, 20, 0, 6, 2]
        assert game.store == [2, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [3, 3, 3, 0, 0, 3, 1, 4, 1, 1, 1, 0, 25, 1, 11, 1]
        assert game.store == [2, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 1, 7, 1, 1, 1, 1, 6, 3, 7, 2, 7, 0, 6]
        assert game.store == [2, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [5, 2, 3, 0, 3, 0, 4, 0, 0, 6, 3, 7, 2, 0, 2, 8]
        assert game.store == [4, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [5, 2, 3, 0, 3, 0, 4, 0, 0, 6, 0, 8, 3, 1, 2, 8]
        assert game.store == [4, 47]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 6, 3, 0, 1, 1, 3, 3, 9, 3, 0, 1, 3, 4, 0]
        assert game.store == [4, 54]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [1, 2, 7, 0, 0, 1, 1, 3, 3, 9, 3, 0, 1, 3, 4, 0]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [2, 3, 0, 0, 0, 1, 1, 3, 3, 9, 3, 1, 2, 4, 5, 1]
        assert game.store == [4, 54]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move((7, CW))
        assert game.turn is False
        assert game.board == [2, 3, 1, 1, 1, 1, 4, 0, 0, 9, 3, 1, 2, 4, 5, 1]
        assert game.store == [4, 54]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 9, 3, 1, 2, 4, 0, 3]
        assert game.store == [4, 54]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 9, 0, 3, 1, 5, 1, 3]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 12, 0, 0, 1, 5, 1, 3]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 15, 0, 1, 2, 0, 1, 3]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 15, 0, 1, 0, 2, 3, 1]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 15, 0, 0, 2, 1, 3, 1]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 15, 0, 1, 3, 2, 0, 1]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [1, 4, 0, 0, 3, 1, 5, 1, 1, 15, 0, 1, 3, 1, 2, 0]
        assert game.store == [4, 54]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [2, 5, 1, 1, 4, 0, 0, 2, 2, 0, 0, 2, 4, 2, 3, 1]
        assert game.store == [4, 63]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [1, 8, 4, 0, 0, 0, 0, 2, 2, 0, 0, 2, 4, 2, 3, 1]
        assert game.store == [4, 63]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move((7, CCW))
        assert game.turn is True
        assert game.board == [1, 8, 4, 0, 0, 0, 0, 0, 3, 1, 0, 2, 4, 2, 3, 1]
        assert game.store == [4, 63]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 8, 4, 0, 0, 0, 0, 0, 3, 1, 1, 1, 7, 2, 0, 1]
        assert game.store == [4, 63]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [1, 8, 4, 0, 0, 0, 0, 0, 3, 1, 1, 1, 7, 1, 2, 0]
        assert game.store == [4, 63]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 4, 0, 0, 0, 0, 0, 3, 1, 1, 1, 7, 1, 0, 2]
        assert game.store == [4, 72]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 7, 1, 1, 3]
        assert game.store == [4, 72]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 1, 4, 2, 2, 2, 0, 1, 1, 3]
        assert game.store == [4, 72]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 1, 4, 2, 2, 2, 0, 1, 1, 3]
        assert game.store == [4, 72]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 0, 1, 1, 3]
        assert game.store == [4, 74]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 0, 1, 1, 3]
        assert game.store == [4, 74]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 1, 2, 2, 0]
        assert game.store == [4, 74]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_37(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 1, 2, 0, 2]
        assert game.store == [4, 76]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_38(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 1, 2, 0, 2]
        assert game.store == [4, 76]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_39(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 1, 2, 0, 0]
        assert game.store == [4, 76]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_40(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 2, 2, 1, 2, 0, 0]
        assert game.store == [4, 76]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_41(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 2, 4, 1, 0, 0]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_42(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 2, 0, 2, 0, 3]
        assert game.store == [4, 76]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_43(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 2, 0, 2, 0, 3]
        assert game.store == [4, 76]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_44(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 1, 1, 2, 0, 0, 3]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_45(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 3, 1, 0, 0, 3]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_46(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 2, 1, 1, 3]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_47(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 1, 3, 0, 3]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_48(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 1, 0, 0, 6]
        assert game.store == [4, 76]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_49(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 6, 0, 0, 0, 1, 0, 0, 6]
        assert game.store == [4, 76]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_50(self, gstate):
        game = gstate.game
        cond = game.move((7, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 2, 1, 1, 6]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_51(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 4, 0, 3, 2, 2, 0]
        assert game.store == [4, 76]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_52(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 1, 2, 2, 0, 0, 3, 2, 2, 0]
        assert game.store == [4, 76]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_53(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 1, 1, 2, 2, 0, 0, 3, 2, 2, 0]
        assert game.store == [4, 76]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_54(self, gstate):
        game = gstate.game
        cond = game.move((7, CW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 3, 2, 2, 0]
        assert game.store == [4, 80]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_55(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 3, 2, 2, 0]
        assert game.store == [4, 80]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_56(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 3, 2, 0, 2]
        assert game.store == [4, 82]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_57(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 3, 2, 0, 2]
        assert game.store == [4, 82]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_58(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 1, 4, 2, 0]
        assert game.store == [4, 82]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_59(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 6, 1, 0]
        assert game.store == [4, 82]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_60(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 2, 1]
        assert game.store == [4, 82]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_61(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 2, 1]
        assert game.store == [4, 82]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_62(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 0, 1, 0, 0, 0, 2, 0, 0, 1, 1, 0, 1]
        assert game.store == [4, 82]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_63(self, gstate):
        game = gstate.game
        cond = game.move((6, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [9, 87]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1]
        assert game.store == [0, 78]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move((7, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 1, 1, 1, 1, 1]
        assert game.store == [0, 78]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move((6, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 1, 1, 1, 1]
        assert game.store == [0, 78]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 5, 2]
        assert game.store == [0, 80]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 5, 2]
        assert game.store == [0, 80]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 5, 0]
        assert game.store == [0, 83]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 5, 0]
        assert game.store == [0, 83]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 0, 1]
        assert game.store == [0, 83]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [4, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 0, 1]
        assert game.store == [0, 83]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [4, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1]
        assert game.store == [0, 83]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [4, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1]
        assert game.store == [0, 83]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 2, 2, 2]
        assert game.store == [0, 83]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0]
        assert game.store == [0, 83]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [6, 90]
        assert cond.name == "WIN"
        gstate.cond = cond



@pytest.mark.incremental
class TestGiuthiFWin:

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = False
        game.starter = False
        assert game.board == [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [1, 9, 9, 9, 9, 9, 2, 0, 6, 6, 6, 6, 6, 6, 6, 6]
        assert game.store == [0, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [4, 12, 0, 10, 0, 9, 2, 0, 0, 7, 7, 1, 9, 9, 9, 9]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [5, 13, 1, 11, 1, 10, 3, 1, 0, 7, 7, 1, 9, 9, 0, 10]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [6, 0, 2, 12, 1, 13, 0, 2, 1, 8, 8, 2, 10, 10, 0, 11]
        assert game.store == [10, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [5, 1, 7, 19, 8, 2, 9, 3, 0, 15, 3, 8, 3, 1, 0, 2]
        assert game.store == [10, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [10, 6, 12, 5, 14, 0, 0, 4, 1, 0, 0, 0, 6, 4, 3, 0]
        assert game.store == [31, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [10, 6, 12, 5, 14, 0, 1, 5, 2, 1, 1, 1, 0, 4, 3, 0]
        assert game.store == [31, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [10, 1, 14, 7, 16, 2, 3, 0, 2, 1, 1, 1, 0, 4, 3, 0]
        assert game.store == [31, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [10, 1, 14, 7, 16, 0, 4, 1, 2, 1, 1, 1, 0, 4, 3, 0]
        assert game.store == [31, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move((6, CW))
        assert game.turn is True
        assert game.board == [13, 0, 0, 9, 18, 2, 1, 2, 3, 2, 2, 2, 1, 0, 0, 0]
        assert game.store == [41, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [13, 0, 0, 9, 18, 2, 1, 2, 0, 4, 0, 5, 1, 0, 0, 0]
        assert game.store == [41, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 10, 19, 3, 2, 3, 1, 5, 1, 1, 3, 2, 2, 2]
        assert game.store == [41, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [2, 1, 5, 0, 1, 4, 0, 7, 5, 0, 0, 3, 5, 4, 4, 4]
        assert game.store == [51, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [2, 1, 5, 0, 1, 4, 0, 7, 5, 0, 0, 0, 7, 6, 6, 1]
        assert game.store == [51, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 1, 5, 0, 1, 4, 0, 0, 7, 2, 2, 2, 9, 0, 9, 0]
        assert game.store == [51, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 1, 8, 0, 2, 0, 0, 0, 7, 2, 2, 2, 9, 0, 9, 0]
        assert game.store == [51, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [3, 0, 0, 2, 1, 1, 1, 1, 0, 5, 5, 1, 10, 0, 0, 0]
        assert game.store == [63, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 3, 2, 2, 2, 2, 1, 6, 6, 2, 0, 0, 0, 0]
        assert game.store == [63, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 3, 1, 5, 2, 0, 1, 6, 6, 2, 0, 0, 0, 0]
        assert game.store == [63, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 5, 7, 1, 0, 2, 0, 1, 6, 6, 2, 0, 0, 0, 0]
        assert game.store == [63, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [0, 0, 5, 7, 0, 2, 1, 0, 1, 6, 6, 2, 0, 0, 0, 0]
        assert game.store == [63, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 5, 7, 0, 0, 2, 1, 1, 6, 6, 2, 0, 0, 0, 0]
        assert game.store == [63, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move((6, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 5, 7, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [78, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 5, 7, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [78, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 3, 3, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        assert game.store == [78, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 3, 3, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        assert game.store == [78, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 4, 0, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 7, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 1, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.store == [78, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [1, 1, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.store == [78, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 3, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 3, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 3, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        assert game.store == [78, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_37(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [85, 11]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1]
        assert game.store == [74, 0]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 4, 2, 3, 3, 0, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [77, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 4, 2, 3, 3, 0, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [77, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [2, 0, 0, 0, 4, 2, 3, 3, 0, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [79, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [2, 0, 0, 0, 4, 2, 3, 3, 0, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [79, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 4, 2, 3, 3, 0, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [79, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 4, 2, 3, 3, 0, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [79, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 3, 4, 4, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [79, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 3, 4, 4, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [79, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 4, 4, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [79, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move((7, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 4, 0, 5, 0, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [79, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move((6, CW))
        assert game.turn is False
        assert game.board == [0, 1, 2, 2, 5, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [79, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [1, 2, 0, 2, 5, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1]
        assert game.store == [79, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [3, 0, 0, 2, 5, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [81, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_14(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [3, 0, 0, 2, 5, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [81, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_15(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 5, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.store == [81, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_16(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 5, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.store == [81, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_17(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [3, 0, 1, 3, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.store == [81, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_18(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [3, 0, 1, 3, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.store == [81, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_19(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 0, 1, 2, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.store == [81, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_20(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 0, 1, 0, 2, 1, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.store == [81, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_21(self, gstate):
        game = gstate.game
        cond = game.move((6, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 1, 0, 1, 0, 0, 3, 0, 0, 0, 1, 0, 1, 1, 1]
        assert game.store == [84, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_22(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [3, 0, 1, 0, 1, 0, 0, 3, 0, 0, 0, 1, 0, 1, 1, 1]
        assert game.store == [84, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_23(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 2, 1, 1, 0, 0, 3, 0, 0, 0, 1, 0, 1, 1, 1]
        assert game.store == [84, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_24(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 3, 0, 0, 0, 3, 0, 0, 0, 1, 0, 1, 1, 1]
        assert game.store == [84, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_25(self, gstate):
        game = gstate.game
        cond = game.move((7, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 3, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.store == [84, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_26(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 1, 3, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.store == [84, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_27(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.mdata.winner is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.owner == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [89, 7]
        assert cond.name == "WIN"
        gstate.cond = cond
