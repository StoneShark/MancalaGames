# -*- coding: utf-8 -*-
"""Test NamNam

MUSTSHARE with TERRITORY goal

Created on Thu Aug 17 07:27:20 2023
@author: Ann"""


import pytest
pytestmark = pytest.mark.integtest

from context import game_info as gi
from context import man_config


T = True
F = False
CCW = gi.Direct.CCW


class GameTestData:
    """allow passing move end cond between tests."""

    def __init__(self, game):
        self.game = game
        self.cond = None


@pytest.fixture(scope="class")
def gstate():
    """This fixture will maintain state between tests in the
    same class but will be reconstructed for each class."""

    game, _ = man_config.make_game('./GameProps/namnam.txt')
    gstate = GameTestData(game)
    return gstate


@pytest.mark.incremental
class TestNamNam45:
    """6 rounds, """

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = True
        game.starter = True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [6, 6, 0, 1, 6, 6, 2, 7, 1, 6, 1, 6]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [7, 7, 1, 2, 7, 1, 0, 8, 2, 7, 2, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 10, 0, 0, 1, 3, 2, 10, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [1, 10, 0, 0, 0, 0, 2, 10, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [1, 10, 0, 0, 0, 0, 0, 11, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 1, 1, 1, 12, 2, 1, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 1, 2, 0, 2, 0, 13, 0, 2, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [2, 3, 2, 3, 1, 1, 2, 1, 2, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 2, 3, 1, 1, 0, 2, 0, 1, 3, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 2, 3, 0, 0, 1, 0, 1, 2, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 2, 3, 0, 0, 1, 0, 1, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 1, 1, 0, 1, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 1, 1, 0, 0, 1, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 1, 1, 0, 1, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 1, 0, 2, 0, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 0, 1, 0, 1, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [0, 2, 0, 2, 0, 1, 0, 1, 0, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 0, 0, 1, 1, 0, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 0, 2, 0, 0, 1, 1, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 1, 0, 0, 2, 1, 0, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_37(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 0, 2, 0, 1, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_38(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_39(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_40(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_41(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_42(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_43(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_44(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_45(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 1, 0, 0, 0, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_46(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 2, 1, 1, 0, 0, 0, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_47(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 1, 0, 0, 0, 0, 0, 1, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_48(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 1, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_49(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 3, 0, 2, 1, 0, 0, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_50(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 3, 0, 1, 1, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_51(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 3, 0, 1, 0, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_52(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 16]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False     # manual change
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [6, 2, 7, 1, 6, 1, 6, 6, 6, 0, 1, 6]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [9, 1, 0, 3, 8, 1, 8, 1, 8, 2, 3, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [4, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 1, 3, 10, 3, 10, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [8, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 3, 2, 1, 1, 0, 0, 11, 1, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [16, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 3, 0, 2, 0, 1, 1, 11, 1, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [16, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 2, 0, 1, 1, 11, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [20, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 0, 0, 0, 1, 2, 0, 12, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [20, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 3, 1, 1, 1, 2, 3, 1, 1, 1, 3, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [20, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 2, 2, 0, 3, 0, 1, 1, 1, 3, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [24, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 2, 2, 0, 3, 0, 1, 1, 0, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [24, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 3, 1, 3, 0, 1, 1, 0, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [24, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 3, 1, 3, 0, 1, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [24, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 3, 0, 0, 0, 1, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_14(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 0, 3, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_15(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 0, 3, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_16(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 0, 3, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_17(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_18(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_19(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_20(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 1, 0, 0, 1, 0, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_21(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 1, 0, 0, 0, 1, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_22(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 2, 1, 1, 1, 0, 0, 0, 1, 0, 2, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_23(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 1, 1, 0, 1, 0, 2, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_24(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_25(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 2, 1, 1, 1, 1, 0, 1, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_26(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 1, 1, 1, 0, 0, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_27(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 2, 1, 1, 1, 0, 1, 0, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_28(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 1, 1, 0, 1, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_29(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 2, 1, 1, 0, 1, 1, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_30(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 1, 0, 1, 1, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_31(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 2, 1, 1, 0, 1, 0, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_32(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 1, 0, 1, 0, 1, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_33(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 1, 0, 1, 0, 1, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_34(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_35(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_36(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_37(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_38(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_39(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_40(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_41(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_42(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_43(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 1, 0, 1, 1, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_44(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 2, 0, 2, 1, 0, 1, 1, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_45(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 1, 0, 0, 0, 1, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_46(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 0, 2, 1, 0, 0, 0, 1, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_47(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 2, 1, 0, 0, 1, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_48(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 2, 1, 0, 0, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_49(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_50(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [36, 12]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False     # manual change
        gstate.cond = cond

    def test_round_3_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [0, 0]

    def test_round_3_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 6, 1, 6, 6, 6, 0, 1, 6, 6, 2, 7]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_2(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 1, 9, 3, 2, 9, 2, 1, 10]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [4, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 1, 2, 10, 0, 3, 10, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [8, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 2, 2, 3, 11, 1, 3, 0, 2, 1, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [12, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [2, 3, 1, 0, 1, 1, 2, 0, 1, 3, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [24, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_6(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [2, 3, 1, 0, 1, 0, 0, 1, 2, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 0, 1, 0, 0, 1, 2, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_12(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_13(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [28, 20]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False     # manual change
        gstate.cond = cond

    def test_round_4_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [0, 0]

    def test_round_4_move_1(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [6, 6, 2, 7, 1, 6, 1, 6, 6, 6, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 8, 0, 8, 2, 7, 2, 0, 7, 7, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_3(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 11, 1, 11, 1, 2, 1, 3, 0, 2, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [4, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [0, 11, 1, 11, 1, 2, 1, 0, 1, 3, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [4, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 11, 1, 11, 1, 2, 0, 1, 1, 3, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [4, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_6(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [1, 11, 1, 11, 1, 2, 0, 0, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [4, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_7(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 13, 3, 0, 1, 1, 1, 1, 1, 2]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [8, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 1, 13, 3, 0, 1, 1, 0, 0, 2, 0]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [8, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_9(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 2, 14, 0, 0, 1, 1, 0, 0, 2, 0]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_10(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 2, 14, 0, 0, 1, 1, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_11(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 2, 14, 0, 0, 1, 1, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_12(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 2, 14, 0, 0, 1, 0, 1, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [2, 3, 0, 1, 2, 0, 3, 0, 3, 0, 2, 0]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [16, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_14(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 3, 1, 3, 0, 3, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_15(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 2, 0, 1, 3, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_16(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, T, T, T, T, T]
        assert game.store == [24, 24]
        assert cond.name == "ROUND_TIE"
        assert game.mdata.winner is None
        gstate.cond = cond

    def test_round_5_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]

    def test_round_5_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 6, 1, 6, 6, 6, 0, 1, 6, 6, 2, 7]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_2(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 3, 0, 1, 10, 0, 0, 1, 9, 2, 10]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 2, 11, 1, 0, 1, 0, 3, 11]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_4(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 1, 0, 12, 0, 1, 0, 1, 0, 11]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [2, 2, 1, 2, 1, 13, 1, 2, 1, 2, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_6(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [3, 3, 2, 3, 2, 1, 0, 0, 3, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 3, 2, 3, 2, 1, 0, 0, 3, 0, 2, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 3, 0, 0, 2, 1, 1, 3, 0, 2, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 0, 2, 1, 1, 0, 1, 3, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 3, 0, 0, 0, 2, 0, 1, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 3, 0, 0, 0, 2, 0, 0, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_12(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 16]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False     # manual change
        gstate.cond = cond

    def test_round_6_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]

    def test_round_6_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [6, 6, 0, 1, 6, 6, 2, 7, 1, 6, 1, 6]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 3, 0, 9, 2, 1, 10, 1, 9, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_3(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 10, 0, 2, 11, 0, 10, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 10, 0, 2, 11, 0, 10, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 10, 0, 0, 12, 1, 10, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_6(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [3, 2, 2, 3, 12, 2, 2, 1, 0, 2, 3, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [8, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_7(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 3, 0, 12, 2, 2, 1, 0, 2, 3, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [12, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 3, 0, 12, 2, 2, 1, 0, 2, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [16, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 3, 0, 12, 2, 2, 0, 1, 2, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [16, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_10(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 3, 0, 12, 2, 2, 0, 1, 2, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [16, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_11(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 12, 2, 2, 0, 1, 2, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [20, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_12(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 12, 2, 2, 0, 1, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [20, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 12, 0, 3, 1, 1, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [20, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_14(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 12, 0, 3, 1, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [20, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_15(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 2, 0, 2, 1, 1, 0, 3, 2, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [24, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_16(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 3, 0, 2, 1, 3, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_17(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 3, 0, 2, 0, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_18(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 3, 0, 2, 0, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_19(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 1, 3, 1, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_20(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 1, 3, 1, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_21(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 1, 0, 1, 3, 0, 1, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_22(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 1, 3, 0, 0, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_23(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [40, 8]
        assert cond.name == "WIN"
        assert game.mdata.winner is False     # manual change
        gstate.cond = cond


@pytest.mark.incremental
class TestNamNam49:
    """6 rounds, both True and False win rounds"""

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = True
        game.starter = True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [7, 1, 6, 1, 6, 6, 6, 0, 1, 6, 6, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        """False move, True pick two holes for 8, False captures from own hole."""
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [10, 1, 9, 0, 0, 1, 0, 3, 0, 9, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [11, 0, 10, 1, 0, 1, 0, 0, 1, 10, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [2, 3, 1, 3, 2, 3, 2, 2, 3, 12, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        """True's turn, captures from False hole at 3"""
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 2, 3, 2, 2, 3, 12, 2, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        """Pick seeds by both True @ 8 and False @ 5, no other capture"""
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 1, 0, 0, 3, 0, 0, 13, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 2, 1, 1, 0, 0, 3, 0, 0, 13, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 1, 0, 3, 0, 0, 13, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [2, 0, 2, 1, 2, 1, 1, 2, 2, 1, 2, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [2, 0, 2, 1, 2, 0, 0, 3, 0, 2, 3, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [3, 1, 2, 1, 2, 0, 0, 3, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 0, 2, 3, 1, 0, 3, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 0, 2, 3, 1, 0, 0, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 0, 2, 0, 2, 1, 1, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 0, 2, 0, 2, 1, 1, 0, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 0, 0, 1, 0, 2, 2, 1, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 3, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 3, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 1, 0, 0, 3, 0, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 2, 1, 1, 0, 0, 3, 0, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 1, 0, 0, 0, 1, 2, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 1, 1, 0, 1, 2, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 1, 0, 1, 1, 2, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 1, 1, 1, 2, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 0, 2, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 1, 0, 0, 2, 0, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 0, 1, 0, 2, 0, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 1, 2, 0, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 1, 1, 2, 0, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 3, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 3, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 0, 1, 0, 3, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 1, 0, 1, 0, 3, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 0, 0, 1, 3, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 1, 3, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_37(self, gstate):
        """True's turn, stop to capture at 8, only 4 seeds left,
        True get's them"""
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 32]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True     # manual change
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        """True controls 8 holes base on 32 seeds collected in
        last round. True started last round False starts this round."""
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 6, 6, 2, 7, 1, 6, 1, 6, 6, 6, 0]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 9, 1, 0, 3, 8, 1, 8, 1, 8, 2]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 2, 1, 0, 9, 2, 9, 2, 9, 0]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 2, 3, 2, 1, 10, 0, 10, 3, 1, 1]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 0, 1, 2, 1, 2, 3, 1, 1, 3, 3]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 2, 1, 2, 3, 1, 1, 3, 0]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 0, 2, 0, 0, 2, 0, 0, 1]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 1, 2, 0, 0, 2, 0, 0, 1]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 1, 0, 1, 1, 2, 0, 0, 1]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 1, 0, 0, 0, 3, 1, 0, 1]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 1, 0, 0, 3, 1, 0, 1]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 1, 0, 0, 3, 1, 0, 0]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 0, 1, 0, 3, 1, 0, 0]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_14(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 1, 3, 1, 0, 0]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_15(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 1, 3, 1, 0, 0]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_16(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 1, 0, 1, 3, 1, 0, 0]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_17(self, gstate):
        """False did last capture and collected last 4 seeds."""
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [T, T, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 28]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True     # manual change
        gstate.cond = cond

    def test_round_3_setup(self, gstate):
        """True has 28 seeds, controls 7 holes.
        False start last, True starts this round."""
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]

    def test_round_3_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [7, 1, 6, 1, 6, 6, 6, 0, 1, 6, 6, 2]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_2(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [10, 0, 2, 0, 9, 1, 10, 1, 0, 1, 0, 2]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [10, 0, 2, 0, 9, 1, 10, 0, 1, 1, 0, 2]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_4(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [11, 1, 2, 0, 0, 2, 11, 1, 2, 2, 1, 3]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [12, 2, 0, 1, 1, 0, 12, 2, 0, 3, 2, 1]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_6(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [12, 0, 1, 0, 2, 1, 12, 2, 0, 3, 2, 1]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 3, 0, 0, 0, 14, 0, 0, 1, 0, 1]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 1, 1, 14, 0, 0, 1, 0, 1]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_9(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 1, 14, 0, 0, 1, 0, 1]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 3, 0, 2, 2, 0, 3, 1, 0, 0]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 3, 0, 2, 0, 1, 0, 1, 0, 0]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_12(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 3, 1, 1, 0, 1, 0, 0]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_13(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 3, 0, 0, 1, 0, 1, 1]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_14(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 24]
        assert cond.name == "ROUND_TIE"
        assert game.mdata.winner is None
        gstate.cond = cond

    def test_round_4_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]

    def test_round_4_move_1(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 6, 6, 2, 7, 1, 6, 1, 6, 6, 6, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 2, 10, 0, 2, 0, 9, 1, 10, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_3(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 11, 1, 2, 0, 9, 1, 10, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 1, 1, 12, 0, 3, 1, 0, 2, 11, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 13, 1, 3, 1, 0, 2, 11, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_6(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 1, 2, 15, 1, 2, 1, 3, 2, 1, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_7(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 3, 0, 1, 3, 0, 3, 1, 3, 2, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 3, 0, 1, 3, 0, 3, 0, 0, 2, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_9(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 3, 0, 0, 0, 0, 3, 0, 0, 2, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_10(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [2, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 3]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_11(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 3]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_12(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 3]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 3]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_14(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_15(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_16(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_17(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_18(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_19(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_20(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_21(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_22(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_23(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_24(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 2, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_25(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 1, 1, 1, 0, 0, 0, 2, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_26(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_27(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 2, 2, 0, 1, 1, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_28(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 2, 2, 0, 1, 0, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_29(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 3, 1, 1, 0, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_30(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 3, 1, 1, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_31(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 2, 2, 1, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_32(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 2, 2, 1, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_33(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 0, 2, 2, 1, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_34(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 0, 2, 2, 0, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_35(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 1, 0, 2, 2, 0, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_36(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 0, 0, 3, 1, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_37(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 1, 3, 1, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_38(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 28]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True     # manual change
        gstate.cond = cond

    def test_round_5_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]

    def test_round_5_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [6, 6, 0, 1, 6, 6, 2, 7, 1, 6, 1, 6]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_2(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [7, 1, 2, 0, 8, 8, 0, 0, 2, 7, 2, 7]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [4, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 3, 0, 2, 10, 10, 2, 2, 1, 8, 1, 0]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_4(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 2, 0, 0, 11, 3, 3, 2, 9, 2, 1]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [3, 0, 3, 1, 0, 11, 3, 0, 3, 10, 0, 2]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_6(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 3, 2, 1, 0, 1, 0, 11, 1, 3]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 3, 2, 1, 0, 0, 1, 11, 1, 3]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 3, 2, 0, 1, 0, 1, 11, 1, 3]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [12, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [2, 0, 3, 1, 0, 1, 2, 1, 0, 1, 0, 1]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [3, 1, 0, 2, 1, 0, 3, 0, 1, 0, 1, 0]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [3, 1, 0, 2, 1, 0, 3, 0, 0, 1, 1, 0]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_12(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 1, 2, 1, 0, 3, 0, 0, 1, 1, 0]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_13(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 1, 0, 3, 0, 0, 0, 0, 1]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_14(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [T, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 24]
        assert cond.name == "ROUND_TIE"
        assert game.mdata.winner is None
        gstate.cond = cond

    def test_round_6_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]

    def test_round_6_move_1(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 6, 6, 2, 7, 1, 6, 1, 6, 6, 6, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 2, 10, 0, 2, 0, 9, 1, 10, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_3(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [1, 2, 1, 2, 0, 1, 3, 1, 10, 2, 11, 2]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [2, 3, 0, 3, 1, 1, 3, 1, 10, 0, 12, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [2, 0, 1, 0, 0, 2, 0, 1, 10, 0, 12, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_6(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [3, 1, 2, 1, 1, 3, 1, 1, 0, 1, 13, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [16, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_7(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [3, 1, 0, 2, 0, 0, 0, 2, 1, 1, 13, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [20, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 1, 3, 1, 1, 1, 3, 2, 1, 1, 3]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [24, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_9(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 2, 1, 3, 1, 0, 0, 0, 0, 2, 2, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_10(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 3, 0, 0, 0, 1, 1, 0, 0, 2, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_11(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 1, 1, 0, 0, 2, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_12(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 1, 1, 1, 0, 0, 2, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 1, 1, 1, 0, 0, 2, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_14(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_15(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 2, 0, 2, 1, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_16(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 2, 0, 2, 1, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_17(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 1, 3, 0, 1, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_18(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 1, 0, 1, 2, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_19(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 1, 2, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_20(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 3, 1, 1, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_21(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 3, 1, 1, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_22(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 0, 0, 0, 0, 3, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_23(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 1, 0, 0, 3, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_24(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 1, 0, 0, 3, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_25(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 3, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_26(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, T, T, T, T, T, T]
        assert game.store == [32, 16]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False     # manual change
        gstate.cond = cond

    def test_round_7_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]

    def test_round_7_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 6, 1, 6, 6, 6, 0, 1, 6, 6, 2, 7]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_2(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 0, 9, 1, 10, 1, 0, 1, 0, 2, 10]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 0, 9, 1, 10, 1, 0, 1, 0, 0, 11]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 2, 0, 9, 1, 10, 0, 1, 1, 0, 0, 11]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 0, 9, 1, 10, 0, 1, 0, 1, 0, 11]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_6(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is True
        assert game.board == [1, 2, 0, 9, 1, 10, 0, 0, 1, 1, 0, 11]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [2, 3, 1, 10, 2, 11, 1, 1, 2, 2, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 2, 11, 0, 1, 3, 0, 0, 0, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [20, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 1, 2, 0, 1, 1, 1, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [2, 0, 1, 1, 1, 2, 0, 1, 1, 1, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [3, 1, 1, 1, 1, 2, 0, 1, 1, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_12(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 2, 0, 2, 0, 1, 2, 0, 2, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_13(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 2, 2, 0, 2, 0, 1, 2, 0, 2, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_14(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 2, 0, 0, 1, 0, 3, 1, 2, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_15(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 2, 0, 0, 1, 0, 3, 0, 0, 1, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_16(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 2, 2, 0, 0, 0, 1, 3, 0, 0, 1, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_17(self, gstate):
        """True has no seeds, False must make some available,
        moves prevented from 0, 4 & 6.
        move 0, 1 is row 0, pos? 1  is index 7"""
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [2, 3, 0, 1, 1, 1, 1, 3, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_18(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is True
        assert game.board == [2, 3, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_19(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [2, 3, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [28, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_20(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_21(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_22(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 2, 1, 1, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_23(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 0, 2, 1, 1, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_24(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 0, 0, 0, 2, 0, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_25(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 0, 0, 2, 0, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_26(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 1, 1, 0, 2, 0, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_27(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 1, 0, 2, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_28(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 1, 0, 2, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_29(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 1, 1, 0, 2, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_30(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_31(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 0, 0, 1, 0, 0, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_32(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 0, 1, 0, 0, 1, 0, 0, 0, 2, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_33(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 1, 1, 1, 0, 0, 0, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_34(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 0, 2, 1, 0, 0, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_35(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 1, 0, 2, 1, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_36(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 2, 1, 1, 0, 2, 0, 1, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_37(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 1, 0, 2, 0, 0, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_38(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 1, 0, 1, 1, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_39(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 1, 0, 2, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_40(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 0, 2, 2, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_41(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 1, 0, 2, 2, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_42(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 1, 0, 2, 2, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_43(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 3, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_44(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 3, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_45(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 3, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_46(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 3, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_47(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_48(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 0, 1, 0, 2, 1, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_49(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 1, 0, 1, 0, 2, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_50(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 0, 0, 1, 2, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_51(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 1, 0, 0, 1, 0, 2, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_52(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 1, 1, 1, 0, 2, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_53(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_54(self, gstate):
        game = gstate.game
        cond = game.move((1, 5, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 0, 1, 0, 0, 0, 2, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_55(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 0, 0, 0, 2, 0, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_56(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [2, 0, 1, 1, 0, 0, 0, 2, 0, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_57(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 2, 0, 1, 1, 0, 2, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_58(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 2, 1, 2, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_59(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 2, 1, 2, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_60(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 2, 3, 1, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_61(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 2, 3, 0, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_62(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 2, 3, 0, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_63(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 2, 3, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_64(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 1, 0, 2, 0, 1, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_65(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 0, 2, 0, 1, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_66(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_67(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 2, 1, 0, 1, 0, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_68(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 2, 1, 0, 1, 0, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_69(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 2, 0, 2, 1, 0, 1, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_70(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 0, 2, 1, 1, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_71(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 2, 0, 0, 2, 1, 1, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_72(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 0, 2, 0, 0, 1, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_73(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 2, 0, 0, 2, 0, 0, 1, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_74(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_75(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_76(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 2]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_77(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_78(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_79(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_80(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_81(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_82(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 1, 0, 1, 1, 1, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_83(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 1, 0, 1, 1, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_84(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 2, 1, 1, 0, 0, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_85(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 2, 1, 1, 0, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_86(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 2, 1, 0, 1, 0, 0, 1, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_87(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 2, 1, 0, 1, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_88(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 2, 1, 0, 1, 0, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_89(self, gstate):
        game = gstate.game
        cond = game.move((0, 1, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 2, 1, 0, 1, 0, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_90(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 2, 1, 0, 1, 1, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_91(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 2, 1, 0, 1, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_92(self, gstate):
        game = gstate.game
        cond = game.move((0, 5, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 2, 0, 1, 1, 1, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_93(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 2, 0, 1, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_94(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 3, 1, 1, 1, 0, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_95(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 3, 1, 1, 0, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_96(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 3, 1, 0, 1, 1, 1, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_97(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 3, 1, 0, 1, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_98(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 3, 1, 0, 1, 0, 0, 1]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_99(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 3, 1, 0, 1, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [32, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_100(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.owner == [F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [40, 8]
        assert cond.name == "WIN"
        assert game.mdata.winner is False     # manual change
        gstate.cond = cond
