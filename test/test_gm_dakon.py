# -*- coding: utf-8 -*-
"""Test Dakon

Created on Fri Apr 25 13:06:49 2025
@author: Ann
"""


import pytest
pytestmark = pytest.mark.integtest

from context import game_interface as gi
from context import man_config


F = False
T = True

class GameTestData:
    """allow passing move end cond between tests."""

    def __init__(self, game):
        self.game = game
        self.cond = None


@pytest.fixture(scope="class")
def gstate():
    """This fixture will maintain state between tests in the
    same class but will be reconstructed for each class."""

    game, _ = man_config.make_game('./GameProps/Dakon.txt')
    gstate = GameTestData(game)
    return gstate



@pytest.mark.incremental
class TestDakon:

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = True
        game.starter = True
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 8, 8, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 1, 11, 11, 3, 4, 2, 11, 11, 11, 0, 2, 11, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [4, 10]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 4, 3, 15, 7, 8, 6, 0, 14, 1, 3, 5, 2, 6]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [8, 10]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [7, 5, 1, 17, 9, 1, 0, 2, 16, 3, 5, 7, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [8, 6, 2, 18, 10, 2, 1, 3, 1, 0, 7, 9, 6, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [10, 12]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 12, 8, 5, 16, 2, 3, 4, 8, 4, 1, 2, 1, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [10, 19]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 13, 0, 6, 17, 3, 4, 5, 9, 5, 2, 1, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [10, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [1, 0, 3, 1, 19, 5, 2, 8, 12, 2, 0, 4, 5, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [13, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 0, 0, 2, 20, 6, 0, 9, 13, 0, 1, 5, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [13, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 1, 1, 0, 21, 0, 1, 10, 14, 1, 0, 0, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [17, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 3, 3, 0, 23, 0, 0, 0, 1, 3, 2, 2, 3, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [17, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 3, 0, 1, 24, 0, 0, 0, 0, 3, 2, 2, 3, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [19, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 4, 1, 2, 25, 1, 1, 0, 0, 3, 2, 2, 0, 8]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [19, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 8, 0, 5, 3, 5, 0, 4, 1, 7, 0, 0, 4, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [25, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [4, 8, 0, 5, 3, 5, 0, 0, 2, 8, 1, 1, 4, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [25, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [4, 8, 0, 5, 0, 6, 1, 0, 2, 8, 1, 1, 4, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [26, 30]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 1, 0, 7, 0, 8, 0, 2, 1, 9, 2, 0, 5, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [28, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 3, 0, 1, 2, 10, 2, 0, 3, 2, 5, 0, 7, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [28, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 0, 0, 0, 11, 3, 0, 3, 2, 5, 0, 7, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [29, 35]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 11, 3, 0, 3, 0, 5, 0, 7, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 2, 2, 1, 11, 3, 0, 3, 0, 5, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 1, 0, 3, 2, 0, 4, 1, 4, 1, 6, 0, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [35, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 2, 1, 3, 2, 0, 4, 1, 4, 0, 0, 1, 2, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [35, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [3, 2, 1, 3, 2, 0, 0, 2, 5, 1, 0, 1, 2, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [36, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [3, 2, 1, 3, 2, 0, 0, 2, 5, 1, 0, 1, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [36, 38]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 0, 1, 3, 2, 0, 0, 2, 5, 1, 0, 0, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [36, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 0, 0, 0, 3, 1, 1, 2, 5, 1, 0, 0, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [37, 41]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [3, 0, 0, 0, 3, 0, 0, 0, 6, 2, 1, 0, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [38, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 1, 1, 0, 3, 0, 0, 0, 6, 2, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [38, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 2, 1, 0, 1, 1, 1, 6, 2, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [39, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 0, 1, 1, 1, 6, 0, 2, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [39, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 0, 0, 0, 0, 7, 1, 2, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [40, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 0, 0, 0, 0, 7, 0, 0, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [40, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 47]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_37(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 48]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_38(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_39(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_40(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_41(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_42(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_43(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 48]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_1_move_44(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_45(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_46(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [50, 48]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [1, 6]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [8, 8, 8, 8, 8, 8, 1, 0, 8, 8, 8, 8, 8, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [3, 6]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [8, 8, 8, 8, 8, 0, 2, 0, 9, 9, 9, 9, 9, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [4, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [12, 0, 12, 12, 1, 2, 3, 0, 2, 13, 3, 13, 4, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [4, 11]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [15, 0, 15, 15, 0, 5, 6, 0, 2, 0, 7, 2, 0, 9]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [4, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [16, 1, 16, 16, 0, 0, 7, 0, 3, 0, 0, 3, 1, 10]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [7, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [17, 2, 17, 0, 1, 1, 8, 0, 4, 1, 0, 3, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [7, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [17, 0, 18, 1, 1, 1, 8, 0, 4, 1, 0, 3, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [7, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [17, 0, 18, 0, 1, 1, 8, 0, 4, 0, 0, 3, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [7, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [20, 0, 1, 4, 0, 4, 1, 0, 0, 0, 3, 6, 3, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [14, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [21, 1, 1, 4, 0, 4, 1, 0, 0, 0, 3, 6, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [14, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [21, 1, 0, 0, 1, 5, 2, 0, 1, 0, 3, 6, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [15, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 4, 3, 3, 0, 8, 5, 0, 4, 1, 5, 0, 2, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [15, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 5, 0, 2, 1, 7, 0, 0, 3, 7, 2, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [23, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 1, 1, 3, 2, 8, 0, 1, 0, 1, 4, 6, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [23, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 4, 1, 1, 5, 1, 9, 0, 0, 1, 0, 5, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [24, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 4, 1, 0, 5, 1, 9, 0, 0, 0, 0, 5, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [24, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_17(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 6, 0, 10, 0, 0, 0, 0, 5, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [25, 47]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_18(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 3, 0, 0, 1, 11, 0, 1, 1, 0, 0, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [28, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 0, 1, 11, 0, 0, 0, 1, 0, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [28, 51]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_20(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 1, 11, 0, 0, 0, 1, 0, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [28, 51]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_21(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 1, 1, 11, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [28, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_22(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 1, 3, 2, 0, 1, 1, 0, 1, 1, 2, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [29, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 4, 0, 0, 2, 0, 0, 1, 0, 3, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [29, 55]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 5, 0, 0, 2, 0, 0, 1, 0, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 55]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_25(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 5, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 55]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 3, 1, 0, 0, 1, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [34, 55]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_27(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 2, 0, 1, 1, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [35, 55]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_28(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 2, 0, 1, 1, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [35, 56]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_29(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 2, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [35, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_30(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_31(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_33(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_34(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_35(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 59]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_36(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_38(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 60]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_39(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_40(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 60]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_2_move_41(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_42(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_43(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_44(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_45(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_46(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 61]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_3_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [2, 12]

    def test_round_3_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 10, 0, 10, 1, 10, 3, 11, 2, 11, 11, 11]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [2, 16]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_3_move_2(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 2, 12, 2, 12, 3, 12, 5, 13, 1, 13, 2, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_3(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 1, 14, 4, 0, 1, 14, 0, 15, 3, 15, 4, 3]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [6, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_4(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 5, 6, 3, 20, 1, 0, 3, 22, 4, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [6, 25]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_3_move_5(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 6, 3, 20, 0, 0, 3, 22, 4, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [6, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 4, 21, 1, 1, 0, 0, 5, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [31, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 3, 1, 0, 4, 21, 1, 1, 0, 0, 0, 3]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [31, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_8(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 1, 3, 1, 0, 0, 22, 2, 0, 1, 1, 0, 3]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_9(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 4, 1, 4, 3, 0, 3, 1, 0, 5, 5, 4, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 5, 2, 1, 0, 2, 1, 3, 0, 7, 1, 5, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [34, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_11(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 1, 7, 0, 1, 2, 1, 4, 1, 0, 2, 4, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [34, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 3, 0, 3, 6, 1, 1, 0, 5, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [36, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_13(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 3, 0, 3, 6, 1, 1, 0, 5, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [36, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 3, 0, 3, 6, 0, 1, 0, 5, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [38, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_15(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 2, 1, 1, 1, 8, 0, 1, 0, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [38, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_16(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 3, 0, 2, 1, 8, 0, 1, 0, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [39, 43]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_3_move_17(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 3, 1, 8, 0, 1, 0, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [40, 43]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_3_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 2, 9, 1, 1, 0, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [41, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 2, 0, 2, 2, 1, 2, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [41, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_20(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 1, 0, 2, 0, 2, 2, 1, 2, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [41, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_21(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 1, 1, 0, 2, 0, 2, 2, 0, 0, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [41, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_22(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 1, 2, 0, 2, 2, 0, 0, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [42, 45]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_3_move_23(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 2, 0, 0, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [43, 45]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_3_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 2, 0, 2, 2, 0, 0, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [43, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_25(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 1, 0, 2, 0, 2, 2, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [43, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 2, 0, 2, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [46, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_27(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 2, 0, 0, 1, 1, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [46, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_28(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 1, 1, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [47, 46]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_3_move_29(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_3_move_30(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_32(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_33(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_34(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_35(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_36(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_37(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_38(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_39(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_40(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_41(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 47]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_3_move_42(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_43(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_44(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_45(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_46(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_47(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_48(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 49]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_3_move_49(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 49]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_50(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 49]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_51(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 49]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_52(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 49]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_53(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 49]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_54(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 49]
        assert cond.name == "ROUND_TIE"
        assert game.mdata.winner is None
        gstate.cond = cond

    def test_round_4_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [0, 0]

    def test_round_4_move_1(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [1, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_4_move_2(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [6, 2, 0, 1, 3, 0, 4, 13, 5, 13, 13, 4, 13, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [8, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_4_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [6, 0, 1, 0, 4, 0, 4, 13, 0, 13, 13, 4, 13, 13]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [14, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [9, 3, 4, 3, 0, 3, 7, 16, 3, 0, 1, 6, 2, 16]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [14, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 6, 3, 6, 1, 19, 0, 3, 0, 9, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [37, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_6(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 0, 6, 3, 6, 1, 19, 0, 0, 1, 10, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [37, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 0, 6, 3, 6, 1, 19, 0, 0, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_8(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [3, 0, 0, 0, 5, 8, 3, 2, 3, 3, 4, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [4, 1, 0, 0, 0, 9, 4, 3, 0, 4, 5, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [4, 1, 0, 0, 0, 9, 4, 3, 0, 4, 5, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 18]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_4_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 1, 1, 1, 0, 5, 4, 1, 5, 1, 3, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 2, 0, 5, 4, 0, 5, 1, 3, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 2, 0, 5, 4, 0, 5, 1, 0, 3, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 21]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_4_move_14(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 2, 0, 5, 0, 1, 6, 2, 1, 3, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_15(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 3, 1, 0, 0, 1, 0, 1, 2, 7, 0, 0, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [56, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 0, 2, 1, 0, 0, 1, 0, 3, 0, 1, 1, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_17(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [3, 0, 2, 1, 0, 0, 0, 0, 3, 0, 1, 1, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [57, 24]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_4_move_18(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 3, 0, 1, 0, 0, 0, 0, 0, 1, 1, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_19(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 3, 0, 1, 0, 0, 0, 0, 0, 1, 1, 5, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 25]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_4_move_20(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 2, 0, 1, 2, 1, 1, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_21(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 2, 0, 1, 2, 1, 0, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [62, 26]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_4_move_22(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 0, 2, 1, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [63, 26]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_4_move_23(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 2, 1, 0, 0, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [65, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_24(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 2, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [65, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_25(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [66, 26]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_4_move_26(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_27(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 27]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_4_move_28(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_29(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [69, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_30(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [69, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [69, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_32(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [69, 29]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_5_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [20, 1]

    def test_round_5_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [8, 8, 8, 0, 8, 8, 8, 0, 0, 0, 8, 1, 9, 9]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [20, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_5_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [9, 9, 9, 1, 8, 8, 8, 0, 0, 0, 0, 2, 10, 10]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [20, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [11, 11, 2, 4, 11, 11, 11, 0, 0, 0, 3, 5, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [23, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [13, 1, 3, 5, 12, 12, 12, 0, 0, 0, 4, 1, 3, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [23, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_5(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [14, 2, 4, 6, 13, 1, 13, 0, 0, 0, 5, 2, 4, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [24, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 4, 9, 11, 4, 6, 0, 0, 0, 0, 10, 7, 0, 10]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [24, 12]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_5_move_7(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 7, 12, 1, 0, 2, 3, 0, 0, 0, 3, 11, 4, 14]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [24, 16]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_5_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 9, 14, 0, 2, 4, 0, 0, 0, 0, 5, 13, 6, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [24, 19]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_5_move_9(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 11, 16, 2, 4, 0, 2, 0, 0, 0, 7, 2, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [24, 22]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_5_move_10(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 13, 18, 4, 1, 1, 3, 0, 0, 0, 8, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [24, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_11(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 19, 6, 0, 1, 0, 3, 0, 0, 0, 0, 7, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [35, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 20, 7, 1, 1, 0, 3, 0, 0, 0, 0, 0, 2, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [35, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 10, 3, 0, 4, 3, 0, 0, 0, 3, 3, 0, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [39, 25]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_5_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 10, 0, 1, 5, 0, 0, 0, 0, 4, 4, 1, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [40, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 10, 0, 1, 5, 0, 0, 0, 0, 4, 0, 2, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [40, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 2, 0, 2, 1, 2, 1, 0, 0, 0, 1, 0, 2, 10]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [47, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_17(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 2, 0, 2, 1, 2, 1, 0, 0, 0, 1, 0, 0, 11]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [47, 27]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_5_move_18(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [4, 2, 0, 2, 1, 2, 1, 0, 0, 0, 0, 1, 0, 11]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [47, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 2, 0, 0, 2, 0, 2, 0, 0, 0, 1, 1, 0, 11]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [48, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_20(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 0, 0, 0, 2, 0, 2, 0, 0, 0, 1, 0, 0, 11]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [48, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_21(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [4, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 11]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [49, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 3, 1, 1, 0, 0, 0, 1, 2, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [49, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_23(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 2, 2, 0, 0, 0, 0, 3, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [52, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_24(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [52, 38]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_5_move_25(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [52, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_26(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [53, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [53, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_28(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [53, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_29(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [53, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_30(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [54, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_31(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [54, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_32(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [54, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_33(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [54, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_34(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_35(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_36(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_37(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 42]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_5_move_38(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_39(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_40(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_41(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_42(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_43(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_44(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 43]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_6_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [6, 1]

    def test_round_6_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 13, 13, 4, 13, 13, 13, 0, 2, 0, 1, 3, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [6, 8]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_6_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 13, 13, 4, 13, 13, 13, 0, 2, 0, 1, 0, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [6, 9]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_6_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [6, 14, 14, 0, 0, 14, 14, 0, 3, 0, 1, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [6, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [7, 0, 15, 1, 1, 15, 15, 0, 4, 1, 2, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [10, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [7, 0, 15, 1, 1, 15, 15, 0, 4, 1, 2, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [10, 26]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_6_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [7, 0, 15, 1, 1, 15, 15, 0, 4, 1, 2, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [10, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_7(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 0, 6, 4, 1, 3, 5, 0, 4, 7, 0, 10, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [22, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 1, 7, 0, 2, 4, 6, 0, 5, 8, 0, 10, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [22, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_9(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 2, 8, 1, 0, 1, 8, 0, 6, 0, 1, 11, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [24, 33]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_6_move_10(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 0, 9, 2, 0, 0, 0, 0, 7, 0, 2, 12, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [27, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 10, 0, 1, 1, 1, 0, 0, 1, 3, 13, 3, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [27, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 10, 0, 1, 0, 0, 0, 1, 1, 3, 13, 3, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [28, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_13(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 10, 0, 1, 0, 0, 0, 1, 1, 3, 13, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [28, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 11, 0, 1, 0, 0, 0, 1, 1, 0, 13, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [32, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 12, 0, 2, 1, 1, 0, 2, 2, 0, 0, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [32, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 12, 0, 2, 0, 0, 0, 0, 3, 1, 1, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 12, 0, 2, 0, 0, 0, 0, 3, 1, 0, 0, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 39]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_6_move_18(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_19(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 2, 0, 0, 0, 0, 3, 0, 0, 0, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_20(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 1, 1, 1, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_21(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 3, 1, 0, 0, 0, 0, 1, 1, 1, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_22(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 4, 0, 1, 0, 1, 0, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 53]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_23(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 0, 1, 2, 0, 0, 1, 1, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [34, 53]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 1, 2, 0, 0, 1, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [34, 55]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_25(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [35, 55]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [35, 55]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 55]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_28(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 57]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_29(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 57]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_30(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 58]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 59]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_6_move_33(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_34(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_35(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_36(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_37(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_38(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_39(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_40(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_41(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [37, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_42(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [38, 59]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_6_move_43(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [38, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_44(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [38, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_45(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [38, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_46(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [38, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_47(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [38, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_48(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [38, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_49(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [38, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_50(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [38, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_51(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [38, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_52(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [38, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_53(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [39, 59]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_7_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [4, 10]

    def test_round_7_move_1(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 3, 13, 4, 13, 6, 5, 1, 1, 13, 2, 3, 13]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_2(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 9, 5, 1, 18, 11, 0, 7, 7, 3, 8, 0, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [11, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_3(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 12, 8, 4, 3, 1, 3, 10, 1, 6, 11, 3, 5]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [15, 16]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_7_move_4(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 18, 0, 5, 9, 3, 5, 2, 1, 0, 1, 9, 3]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [26, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_5(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 6, 10, 4, 6, 3, 0, 1, 0, 0, 4]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [26, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 11, 5, 7, 4, 1, 0, 1, 1, 4]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [27, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 11, 5, 7, 4, 1, 0, 0, 0, 5]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [27, 38]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_7_move_8(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 11, 5, 7, 0, 2, 1, 1, 1, 5]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [27, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_9(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 6, 8, 1, 3, 0, 2, 2, 6]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [31, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_10(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 6, 0, 2, 4, 1, 3, 3, 7]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [31, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 1, 0, 1, 3, 0, 2, 4, 0, 8]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [38, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_12(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 2, 2, 1, 2, 1, 2, 0, 1, 3, 5, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [38, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 1, 0, 2, 0, 0, 2, 0, 6, 2, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [41, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 1, 2, 1, 2, 0, 1, 0, 2, 1, 3]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [41, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_15(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 2, 0, 1, 2, 1, 2, 1, 3]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [42, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 3, 1, 1, 0, 2, 0, 1, 2, 1, 0, 2, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [42, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 2, 0, 2, 0, 0, 2, 1, 0, 2, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [44, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_18(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 2, 0, 2, 0, 0, 0, 2, 1, 2, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [44, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 3, 1, 2, 0, 0, 0, 2, 1, 2, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [44, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_20(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 3, 1, 2, 0, 0, 0, 2, 1, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [44, 44]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_7_move_21(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 3, 1, 2, 0, 0, 0, 2, 0, 1, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [44, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_22(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 3, 1, 0, 1, 0, 0, 2, 0, 1, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [45, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_23(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 3, 1, 0, 1, 0, 0, 2, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [45, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_24(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 2, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [47, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_25(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [47, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_26(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 45]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_7_move_27(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 45]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_7_move_28(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_29(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 46]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_7_move_30(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 47]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_7_move_31(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_33(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_34(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_35(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_36(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_7_move_37(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_38(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_39(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_40(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_41(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 47]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_8_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [2, 5]

    def test_round_8_move_1(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 10, 10, 10, 3, 0, 11, 0, 10, 0, 10, 2, 10, 10]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [6, 5]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_2(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 12, 12, 0, 4, 1, 1, 0, 12, 2, 0, 4, 12, 12]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [21, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 2, 1, 2, 6, 3, 3, 0, 14, 2, 3, 2, 15, 15]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [21, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_4(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 4, 3, 0, 9, 0, 6, 0, 16, 1, 5, 4, 1, 17]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [24, 8]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_5(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 4, 3, 0, 9, 0, 0, 0, 17, 2, 6, 5, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [44, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 4, 1, 10, 1, 1, 0, 17, 2, 0, 6, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [44, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 0, 2, 1, 3, 3, 0, 18, 3, 1, 7, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [46, 9]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_8(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 3, 2, 0, 3, 2, 6, 0, 1, 5, 3, 9, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [49, 9]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 4, 0, 1, 4, 0, 7, 0, 0, 6, 0, 10, 5, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [52, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 5, 1, 1, 4, 0, 7, 0, 0, 6, 0, 10, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [52, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 3, 6, 0, 1, 0, 1, 7, 1, 11, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [54, 10]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_12(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 0, 3, 6, 0, 0, 0, 1, 7, 1, 11, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [55, 10]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 7, 1, 1, 0, 1, 7, 1, 11, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [55, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_14(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 7, 1, 1, 0, 1, 7, 1, 11, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [55, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 8, 0, 2, 0, 1, 7, 1, 11, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [56, 11]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 3, 0, 2, 8, 2, 12, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [57, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 3, 0, 0, 9, 0, 13, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [57, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 1, 10, 1, 13, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [58, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 1, 10, 1, 13, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [58, 14]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_20(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 14, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [58, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 0, 2, 1, 0, 0, 0, 2, 14, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [58, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 0, 2, 1, 0, 2, 1, 0, 0, 0, 2, 14, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [58, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 0, 2, 1, 0, 0, 2, 0, 0, 0, 2, 14, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [59, 16]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_24(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 1, 1, 2, 0, 0, 0, 2, 14, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [59, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_25(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 1, 1, 2, 0, 0, 0, 0, 15, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [59, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_26(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 1, 1, 0, 0, 1, 0, 0, 15, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [60, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 1, 3, 2, 2, 1, 0, 2, 1, 1, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [60, 20]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_28(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 2, 0, 4, 0, 3, 2, 0, 0, 2, 2, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [60, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_29(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 4, 3, 0, 1, 2, 2, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [61, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_30(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 4, 3, 0, 1, 0, 3, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [61, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_31(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 4, 0, 0, 2, 1, 3, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [62, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_32(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 4, 0, 0, 2, 1, 3, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [62, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_33(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 3, 2, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [65, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_34(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 0, 3, 2, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [65, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_35(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 3, 2, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [65, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_36(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 3, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [65, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_37(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 3, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [65, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_38(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 2, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [65, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_39(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 2, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [65, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_40(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 2, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [65, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_41(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [66, 27]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_42(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [66, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_43(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 2, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [66, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_44(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [67, 27]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_45(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [67, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_46(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [67, 28]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_47(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [67, 29]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_48(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_8_move_49(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [67, 31]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_9_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [18, 3]

    def test_round_9_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [8, 8, 8, 0, 8, 8, 8, 0, 0, 0, 8, 1, 9, 9]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [18, 5]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [9, 9, 9, 1, 8, 8, 8, 0, 0, 0, 0, 2, 10, 10]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [18, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 11, 11, 3, 2, 11, 11, 0, 0, 0, 3, 5, 1, 12]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [21, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 12, 12, 4, 3, 12, 12, 0, 0, 0, 4, 6, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [21, 8]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 12, 12, 4, 3, 12, 12, 0, 0, 0, 0, 7, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [21, 9]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 13, 0, 0, 4, 13, 13, 0, 0, 0, 1, 0, 3, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [21, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_7(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 14, 1, 0, 4, 13, 13, 0, 0, 0, 0, 0, 3, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [23, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 1, 2, 4, 5, 20, 1, 0, 0, 0, 6, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [23, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_9(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 1, 5, 7, 1, 2, 4, 0, 0, 0, 9, 4, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [26, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 2, 6, 8, 2, 3, 0, 0, 0, 0, 10, 5, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [26, 33]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 2, 1, 6, 0, 0, 0, 6, 12, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [26, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 0, 2, 1, 2, 0, 0, 0, 0, 0, 7, 13, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [30, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 1, 3, 2, 3, 1, 1, 0, 0, 0, 8, 1, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [30, 41]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 0, 3, 2, 3, 1, 1, 0, 0, 0, 8, 0, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [30, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 1, 4, 3, 4, 1, 0, 0, 0, 0, 0, 1, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [31, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 1, 4, 3, 4, 1, 0, 0, 0, 0, 0, 0, 0, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [31, 44]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_17(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 0, 5, 4, 0, 2, 1, 0, 0, 0, 1, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [31, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_18(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [5, 0, 0, 5, 1, 3, 2, 0, 0, 0, 1, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [32, 48]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 0, 0, 0, 2, 4, 3, 0, 0, 0, 0, 2, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [33, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_20(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 4, 3, 0, 0, 0, 0, 2, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [33, 54]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_21(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 4, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [36, 54]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 4, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [36, 54]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_23(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [36, 54]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_24(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [36, 55]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_25(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [36, 55]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_26(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [37, 55]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_27(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 2, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 55]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_28(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 56]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_29(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 57]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_30(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 58]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_31(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 59]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_9_move_32(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 59]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_33(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [39, 59]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_10_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [4, 10]

    def test_round_10_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 6, 14, 5, 0, 1, 2, 0, 13, 3, 13, 4, 13]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [14, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 7, 15, 6, 1, 2, 3, 1, 14, 4, 14, 5, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [14, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 9, 4, 5, 5, 1, 16, 1, 16, 7, 3]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [17, 11]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_10_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 1, 3, 1, 0, 7, 7, 3, 18, 0, 18, 9, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [19, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_5(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 4, 1, 0, 0, 10, 10, 0, 20, 2, 2, 12, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [19, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 4, 0, 0, 0, 10, 10, 0, 0, 2, 2, 12, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [40, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 4, 0, 0, 0, 10, 10, 0, 0, 2, 0, 13, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [40, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_8(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 0, 2, 0, 0, 1, 1, 3, 1, 14, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [53, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_9(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 2, 3, 1, 3, 1, 1, 2, 2, 4, 1, 1, 4]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [53, 20]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_10_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 3, 4, 0, 4, 0, 2, 0, 3, 5, 0, 2, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [53, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_11(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 1, 5, 1, 2, 0, 3, 5, 0, 2, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [54, 21]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_10_move_12(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 1, 5, 0, 2, 0, 3, 5, 0, 2, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [55, 21]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_10_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 0, 1, 2, 3, 1, 4, 0, 1, 3, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [57, 21]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_10_move_14(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 2, 3, 0, 1, 0, 0, 2, 0, 1, 0, 4, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [64, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_15(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 1, 2, 0, 0, 2, 0, 1, 0, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [64, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 3, 0, 0, 0, 1, 1, 2, 0, 1, 0, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [65, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [65, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_18(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [66, 24]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_10_move_19(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [66, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_20(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [66, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [66, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_22(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [66, 27]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_10_move_23(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [66, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_24(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [66, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_25(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [66, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [66, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_27(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [66, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_28(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_10_move_29(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_30(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_31(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_32(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_33(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_34(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_35(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [68, 30]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_11_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [19, 2]

    def test_round_11_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [10, 10, 0, 10, 0, 1, 10, 0, 0, 0, 10, 0, 10, 10]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [25, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [11, 11, 0, 11, 1, 2, 11, 0, 0, 0, 11, 0, 10, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [25, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 2, 13, 3, 4, 13, 0, 0, 0, 13, 2, 12, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [30, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 2, 13, 3, 4, 13, 0, 0, 0, 13, 0, 13, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [30, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 9, 6, 1, 7, 1, 5, 0, 0, 0, 2, 6, 4, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [9, 0, 7, 2, 8, 2, 6, 0, 0, 0, 3, 7, 1, 8]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 7]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_11_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [11, 0, 9, 1, 9, 3, 0, 0, 0, 0, 4, 1, 3, 10]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 3, 12, 0, 12, 6, 3, 0, 0, 0, 6, 3, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [41, 9]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_11_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 0, 2, 1, 15, 1, 6, 0, 0, 0, 8, 5, 2, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [44, 9]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_11_move_10(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 3, 0, 16, 0, 1, 0, 0, 0, 9, 6, 3, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [46, 9]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_11_move_11(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 3, 0, 16, 0, 0, 0, 0, 0, 9, 6, 3, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [47, 9]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_11_move_12(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 17, 1, 1, 0, 0, 0, 9, 6, 3, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [47, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_13(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 17, 1, 1, 0, 0, 0, 9, 6, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [47, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 18, 1, 1, 0, 0, 0, 0, 7, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [48, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 18, 1, 1, 0, 0, 0, 0, 7, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [48, 11]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_11_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 3, 0, 0, 19, 2, 0, 0, 0, 0, 1, 0, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [48, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_17(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 4, 1, 0, 19, 2, 0, 0, 0, 0, 0, 0, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [50, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 7, 2, 0, 2, 5, 0, 0, 0, 0, 3, 3, 0, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [50, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 4, 7, 0, 0, 0, 0, 1, 4, 1, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [52, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_20(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 0, 2, 4, 7, 0, 0, 0, 0, 1, 0, 2, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [52, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 0, 1, 0, 1, 9, 0, 0, 0, 0, 1, 1, 0, 8]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [54, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_22(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 1, 2, 0, 2, 10, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [54, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_23(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 1, 0, 1, 0, 11, 2, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 24]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_11_move_24(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 2, 1, 2, 1, 0, 3, 0, 0, 0, 1, 1, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [56, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_25(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 2, 1, 2, 1, 0, 3, 0, 0, 0, 1, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [56, 25]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_11_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 0, 1, 2, 1, 0, 3, 0, 0, 0, 1, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [56, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 0, 0, 0, 2, 1, 0, 0, 0, 0, 2, 1, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [57, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_28(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 3, 0, 1, 0, 0, 0, 0, 2, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [57, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_29(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 0, 1, 2, 0, 0, 0, 0, 2, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [58, 29]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_11_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 3, 0, 0, 0, 0, 2, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [59, 29]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_11_move_31(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [63, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_32(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [63, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_33(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [65, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_34(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [65, 31]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_11_move_35(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [65, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_36(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [65, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_37(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [65, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_38(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [65, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_39(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [65, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_40(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [65, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_41(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [65, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_42(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [65, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_43(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [65, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_44(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [66, 31]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_11_move_45(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [66, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_46(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [66, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [66, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_48(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [66, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_49(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [67, 31]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_12_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [18, 3]

    def test_round_12_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 9, 9, 9, 9, 0, 10, 0, 0, 0, 0, 9, 9, 9]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [21, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_12_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [3, 6, 19, 19, 1, 4, 2, 0, 0, 0, 6, 0, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [30, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 1, 20, 20, 2, 5, 3, 0, 0, 0, 1, 0, 6, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [30, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_4(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [5, 1, 20, 20, 2, 5, 0, 0, 0, 0, 2, 1, 6, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [31, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [6, 2, 21, 0, 0, 6, 1, 0, 0, 0, 0, 2, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [31, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [8, 4, 0, 3, 0, 9, 4, 0, 0, 0, 2, 4, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [34, 28]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_12_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 3, 4, 0, 4, 0, 8, 0, 0, 0, 0, 8, 1, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_8(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 6, 0, 1, 0, 10, 0, 0, 0, 0, 2, 0, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 6, 0, 0, 1, 10, 0, 0, 0, 0, 2, 0, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_10(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 7, 1, 1, 1, 10, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [38, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_11(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 7, 1, 0, 0, 11, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [39, 37]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_12_move_12(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 8, 0, 1, 1, 11, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [39, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_13(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 8, 0, 1, 1, 11, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [39, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 1, 9, 1, 2, 1, 1, 0, 0, 0, 1, 1, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [40, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 1, 9, 1, 2, 1, 1, 0, 0, 0, 1, 0, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [40, 38]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_12_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 0, 10, 0, 3, 0, 2, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [40, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_17(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [2, 0, 10, 0, 3, 0, 0, 0, 0, 0, 1, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [41, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_18(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 10, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [41, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_19(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 4, 1, 1, 0, 0, 0, 1, 1, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [44, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_20(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 4, 1, 1, 0, 0, 0, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [44, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_21(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 4, 1, 1, 0, 0, 0, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [44, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_22(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 4, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [44, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 4, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [45, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 4, 0, 0, 0, 0, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [45, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_25(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 4, 0, 0, 0, 0, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [45, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_26(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [45, 46]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_12_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [45, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_28(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [46, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_29(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [46, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_30(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [47, 48]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_12_move_31(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [47, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [47, 49]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_12_move_33(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [47, 49]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_34(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [48, 49]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_12_move_35(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [48, 49]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_36(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [48, 50]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_13_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [6, 1]

    def test_round_13_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 11, 3, 11, 11, 2, 11, 11, 11, 0, 1, 12, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [6, 6]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_13_move_2(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 12, 0, 12, 12, 3, 12, 12, 12, 0, 1, 0, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [6, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 4, 2, 1, 15, 0, 5, 14, 0, 14, 2, 3, 2, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [23, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 4, 2, 1, 15, 0, 5, 14, 0, 14, 2, 3, 2, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [23, 13]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_13_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 3, 2, 16, 1, 0, 15, 1, 15, 1, 5, 1, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [23, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 17, 0, 1, 15, 1, 15, 1, 5, 1, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [24, 14]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_13_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 4, 1, 1, 2, 3, 16, 2, 16, 2, 6, 2, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [26, 14]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_13_move_8(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 2, 3, 4, 16, 2, 16, 2, 6, 2, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [27, 14]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_13_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 5, 0, 0, 3, 17, 0, 7, 3, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [46, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 3, 0, 2, 2, 5, 2, 3, 10, 0, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [46, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_11(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 4, 0, 2, 2, 0, 2, 3, 10, 0, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [52, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 4, 0, 2, 2, 0, 2, 0, 11, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [52, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 5, 1, 2, 2, 0, 2, 0, 11, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [52, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 2, 1, 1, 6, 0, 3, 3, 0, 2, 0, 0, 2, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [52, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_15(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 3, 0, 2, 1, 1, 4, 4, 1, 0, 1, 1, 0, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [53, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 1, 3, 2, 0, 5, 0, 2, 1, 2, 2, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [53, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_17(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 3, 1, 0, 1, 3, 2, 3, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [57, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 3, 1, 0, 1, 0, 3, 4, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [57, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_19(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 2, 1, 1, 0, 3, 4, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [58, 28]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_13_move_20(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 2, 0, 1, 0, 3, 4, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [59, 28]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_13_move_21(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 0, 3, 4, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [60, 28]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_13_move_22(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 4, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 28]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_13_move_23(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 4, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_24(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 5, 1, 1, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_25(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 5, 1, 1, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 5, 0, 0, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 29]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_13_move_27(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 5, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_28(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 5, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_29(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 5, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_31(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_32(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_33(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_34(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_35(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_36(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_37(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_38(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_39(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_40(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_41(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [67, 31]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_14_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [18, 3]

    def test_round_14_move_1(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 9, 9, 9, 1, 9, 9, 0, 0, 0, 9, 9, 0, 10]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [18, 6]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_14_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [2, 11, 11, 11, 1, 10, 0, 0, 0, 0, 1, 11, 2, 12]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [18, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 0, 1, 13, 3, 12, 2, 0, 0, 0, 3, 13, 0, 14]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [25, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_4(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [7, 1, 4, 1, 6, 15, 0, 0, 0, 0, 3, 17, 4, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [25, 12]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_14_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [8, 2, 0, 0, 7, 16, 1, 0, 0, 0, 0, 18, 5, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [25, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_6(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [8, 2, 0, 0, 7, 16, 0, 0, 0, 0, 0, 18, 5, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [26, 16]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_14_move_7(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 6, 4, 4, 11, 1, 5, 0, 0, 0, 1, 3, 10, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [37, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_8(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 5, 5, 12, 2, 6, 0, 0, 0, 0, 4, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [37, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 5, 5, 12, 2, 6, 0, 0, 0, 0, 4, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [37, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_10(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 1, 5, 5, 12, 2, 6, 0, 0, 0, 0, 0, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [37, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_11(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 4, 1, 0, 7, 2, 0, 0, 0, 3, 1, 3, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [43, 26]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_14_move_12(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 1, 4, 1, 0, 7, 0, 0, 0, 0, 0, 2, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [53, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 4, 1, 0, 7, 0, 0, 0, 0, 0, 0, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [53, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 4, 1, 0, 0, 1, 0, 0, 0, 1, 1, 6, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [57, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_15(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 2, 5, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [57, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 0, 1, 2, 2, 2, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [58, 27]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_14_move_17(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 0, 3, 3, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [59, 27]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_14_move_18(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [2, 0, 1, 1, 1, 3, 0, 0, 0, 0, 2, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [60, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 0, 1, 1, 1, 3, 0, 0, 0, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [60, 28]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_14_move_20(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 0, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [60, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 0, 1, 0, 0, 4, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [60, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 2, 1, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [60, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_23(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 1, 4, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [60, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_24(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 0, 2, 1, 4, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [60, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_25(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 2, 0, 0, 2, 0, 0, 0, 1, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_26(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 2, 0, 0, 2, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_27(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 1, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [63, 29]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_28(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [63, 30]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_14_move_29(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [63, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_30(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [64, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_31(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [64, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [64, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_33(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [64, 31]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_14_move_34(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [64, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_35(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [65, 31]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_14_move_36(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [66, 31]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_14_move_37(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [66, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_38(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [66, 32]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_15_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [17, 4]

    def test_round_15_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [8, 8, 8, 0, 8, 8, 8, 0, 0, 0, 8, 1, 9, 9]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [17, 6]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_15_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [9, 9, 9, 1, 8, 8, 8, 0, 0, 0, 0, 2, 10, 10]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [17, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 10, 10, 2, 9, 9, 9, 0, 0, 0, 1, 0, 11, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [30, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 11, 0, 3, 10, 10, 10, 0, 0, 0, 2, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [30, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 0, 1, 4, 11, 11, 11, 0, 0, 0, 3, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [33, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 1, 4, 11, 11, 11, 0, 0, 0, 3, 0, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [33, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 12, 12, 12, 0, 0, 0, 0, 0, 2, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [36, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_8(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 12, 12, 12, 0, 0, 0, 0, 0, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [36, 21]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_15_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 1, 0, 12, 12, 12, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [36, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_10(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 1, 12, 12, 12, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [36, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_11(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [1, 2, 0, 1, 12, 12, 12, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [36, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_12(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 3, 0, 3, 16, 3, 0, 0, 0, 0, 1, 3, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [40, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 3, 0, 3, 16, 3, 0, 0, 0, 0, 1, 0, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [40, 23]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_15_move_14(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 0, 1, 4, 17, 0, 1, 0, 0, 0, 2, 1, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [40, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_15(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [5, 0, 1, 4, 17, 0, 0, 0, 0, 0, 2, 1, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [41, 24]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_15_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [6, 1, 0, 0, 18, 1, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [45, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_17(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [6, 1, 0, 0, 18, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [45, 25]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_15_move_18(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [6, 1, 0, 0, 18, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [45, 26]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_15_move_19(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [6, 1, 0, 0, 18, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [45, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_20(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 1, 1, 19, 2, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [46, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 19, 2, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [46, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_22(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 2, 0, 1, 19, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [47, 28]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_15_move_23(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 1, 3, 1, 4, 1, 0, 0, 0, 3, 3, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [50, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 0, 0, 0, 1, 6, 1, 0, 0, 0, 2, 0, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [50, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_25(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 0, 0, 0, 1, 0, 2, 0, 0, 0, 3, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 0, 0, 0, 1, 0, 2, 0, 0, 0, 3, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [55, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_27(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [56, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_28(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [56, 33]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_15_move_29(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [56, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_30(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [57, 35]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_15_move_31(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [58, 35]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_15_move_32(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [59, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_33(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [59, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_34(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_35(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_36(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_37(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_38(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_39(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_40(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_41(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_42(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_43(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_44(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_45(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_46(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_47(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [61, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_48(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, F, F, F, F]
        assert game.store == [62, 36]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_16_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 0, 7, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [13, 1]

    def test_round_16_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [11, 2, 11, 4, 12, 3, 12, 0, 0, 11, 0, 1, 11, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [18, 1]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_2(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [12, 3, 12, 5, 13, 1, 14, 0, 0, 0, 1, 2, 12, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [20, 1]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_3(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [13, 4, 13, 6, 14, 2, 1, 0, 0, 1, 2, 3, 13, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [22, 1]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_4(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [14, 5, 14, 1, 15, 3, 2, 0, 0, 2, 0, 4, 14, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [23, 1]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_5(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [7, 13, 4, 0, 1, 5, 10, 0, 0, 1, 8, 8, 3, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [23, 10]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [8, 14, 5, 1, 1, 5, 10, 0, 0, 1, 8, 8, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [23, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [8, 14, 0, 2, 2, 6, 11, 0, 0, 1, 8, 8, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [24, 11]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [8, 14, 0, 0, 3, 0, 12, 0, 0, 2, 9, 9, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [25, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_9(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [9, 15, 1, 1, 4, 1, 12, 0, 0, 2, 9, 0, 5, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [25, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 18, 4, 4, 7, 4, 1, 0, 0, 4, 1, 2, 7, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [28, 12]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_11(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 20, 2, 1, 10, 0, 2, 0, 0, 2, 1, 5, 10, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [31, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_12(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 20, 2, 1, 10, 0, 2, 0, 0, 2, 1, 5, 10, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [31, 13]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 21, 0, 2, 11, 1, 2, 0, 0, 0, 2, 0, 11, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [31, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 3, 0, 6, 15, 1, 0, 0, 0, 1, 4, 0, 16, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [36, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 3, 0, 6, 15, 1, 0, 0, 0, 1, 4, 0, 16, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [36, 15]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_16(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 3, 0, 6, 15, 1, 0, 0, 0, 1, 0, 1, 17, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [36, 16]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_17(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 3, 0, 0, 15, 1, 0, 0, 0, 0, 0, 1, 17, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [36, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_18(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 16, 0, 1, 0, 0, 0, 0, 1, 17, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [37, 23]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 2, 0, 4, 0, 0, 1, 2, 0, 19, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [40, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_20(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 4, 2, 0, 4, 2, 6, 0, 0, 0, 4, 2, 0, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [40, 26]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_21(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [3, 5, 3, 1, 0, 3, 7, 0, 0, 1, 5, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [40, 28]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_22(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [3, 5, 3, 1, 0, 3, 7, 0, 0, 1, 5, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [40, 29]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_23(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 5, 3, 1, 0, 3, 7, 0, 0, 1, 5, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [40, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_24(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 5, 3, 1, 0, 0, 8, 0, 0, 0, 6, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [41, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_25(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 3, 1, 0, 0, 8, 0, 0, 0, 6, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [41, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 1, 1, 8, 0, 0, 0, 6, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [41, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 0, 2, 1, 1, 8, 0, 0, 0, 0, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [41, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [2, 2, 0, 2, 1, 0, 0, 0, 0, 1, 1, 0, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [45, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_29(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 3, 1, 0, 2, 1, 1, 0, 0, 0, 0, 1, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [45, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_30(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 3, 1, 0, 2, 1, 0, 0, 0, 0, 0, 1, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [46, 41]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_31(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 0, 2, 1, 0, 0, 0, 0, 1, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [47, 41]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_32(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 0, 0, 2, 0, 0, 0, 0, 1, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [48, 41]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_33(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [48, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_34(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 2, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [48, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_35(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 1, 2, 0, 0, 1, 2, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [48, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_36(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [48, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_37(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [49, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_38(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [49, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_39(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [49, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_40(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [49, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_41(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [49, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_42(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [49, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_43(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [49, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_44(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [49, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_45(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_16_move_46(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_47(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_48(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_49(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_50(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_51(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_52(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_53(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [50, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_54(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [51, 47]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_17_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [2, 5]

    def test_round_17_move_1(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 10, 10, 10, 3, 0, 11, 0, 10, 0, 10, 2, 10, 10]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [6, 5]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [9, 4, 2, 0, 3, 9, 20, 0, 1, 6, 18, 0, 4, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [15, 5]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [10, 0, 3, 1, 4, 0, 21, 0, 2, 7, 19, 1, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [22, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [14, 0, 7, 0, 8, 0, 2, 0, 4, 12, 0, 6, 5, 8]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [22, 10]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 15, 4, 1, 7, 2, 0, 3, 1, 0, 2, 6, 16]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [22, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_6(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [6, 2, 0, 7, 3, 1, 10, 0, 3, 1, 0, 12, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 18]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_7(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [8, 4, 2, 1, 5, 2, 2, 0, 6, 4, 3, 1, 4, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_8(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [9, 0, 3, 2, 6, 3, 0, 0, 7, 5, 0, 2, 1, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 20]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [10, 1, 0, 3, 7, 4, 1, 0, 7, 5, 0, 2, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [11, 2, 0, 0, 8, 5, 0, 0, 0, 6, 1, 0, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [41, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [11, 2, 0, 0, 8, 5, 0, 0, 0, 6, 1, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [41, 22]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_12(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 5, 1, 2, 0, 7, 2, 0, 2, 2, 4, 3, 3, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [41, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 2, 1, 4, 0, 3, 3, 5, 4, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [43, 25]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 2, 5, 0, 3, 3, 5, 4, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [44, 25]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 2, 5, 0, 3, 3, 5, 4, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [49, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 1, 0, 2, 0, 2, 5, 0, 0, 4, 6, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [49, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_17(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [1, 1, 0, 2, 0, 2, 0, 0, 1, 5, 7, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [50, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 1, 2, 0, 2, 0, 0, 1, 5, 7, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [50, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 1, 3, 1, 0, 1, 5, 7, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [50, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_20(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 2, 0, 2, 0, 2, 6, 0, 2, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [50, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_21(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 2, 0, 0, 0, 0, 7, 1, 0, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [51, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 2, 0, 0, 0, 0, 7, 1, 0, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [51, 31]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_23(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 2, 0, 0, 0, 0, 7, 0, 0, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [51, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 2, 0, 0, 0, 0, 7, 0, 0, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [51, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_25(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 2, 0, 0, 0, 0, 7, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [51, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_26(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 1, 1, 0, 0, 7, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [52, 34]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_27(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 0, 1, 7, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [53, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 1, 1, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [53, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_29(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 0, 3, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [53, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_30(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 2, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [53, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_31(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [53, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_32(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [53, 37]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_33(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [53, 38]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_34(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [53, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_35(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [54, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_36(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [54, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_37(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [54, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_38(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [54, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_39(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [54, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_40(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [54, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_41(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [54, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_42(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [54, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_43(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [55, 41]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_44(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [55, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_45(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [55, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_46(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [56, 41]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_17_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [56, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_48(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [56, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_49(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [57, 41]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_18_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 0, 7, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [8, 6]

    def test_round_18_move_1(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [3, 13, 3, 13, 4, 13, 6, 0, 0, 5, 1, 1, 13, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [15, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 13, 3, 4, 0, 1, 3, 0, 0, 0, 1, 2, 17, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [15, 30]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_18_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 13, 3, 4, 0, 1, 3, 0, 0, 0, 0, 0, 18, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [15, 31]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_18_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 16, 1, 7, 3, 4, 6, 0, 0, 1, 0, 1, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [15, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 16, 1, 0, 4, 5, 7, 0, 0, 2, 1, 0, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [16, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 16, 1, 0, 4, 5, 7, 0, 0, 2, 1, 0, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [16, 42]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_18_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 16, 0, 0, 4, 5, 7, 0, 0, 0, 2, 0, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [16, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_8(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 16, 0, 0, 0, 6, 8, 0, 0, 1, 2, 0, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [17, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 17, 1, 0, 0, 6, 8, 0, 0, 1, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [17, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 2, 4, 0, 3, 9, 1, 0, 0, 3, 2, 3, 2, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [19, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_11(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 3, 5, 1, 3, 9, 1, 0, 0, 0, 3, 4, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [19, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 0, 6, 2, 4, 1, 2, 0, 0, 1, 4, 5, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [20, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 2, 0, 0, 6, 3, 4, 0, 0, 0, 2, 0, 3, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [20, 50]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 6, 0, 5, 0, 0, 1, 2, 0, 3, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [21, 50]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_15(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 3, 1, 1, 7, 1, 0, 0, 0, 1, 1, 2, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [21, 52]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_18_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 4, 0, 0, 8, 0, 1, 0, 0, 0, 2, 0, 6, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [21, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_17(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 4, 0, 0, 0, 1, 2, 0, 0, 1, 3, 1, 7, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [22, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 5, 1, 1, 1, 1, 2, 0, 0, 1, 3, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [22, 57]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_19(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 5, 1, 1, 0, 0, 3, 0, 0, 1, 3, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [23, 57]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_18_move_20(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 2, 2, 1, 1, 4, 0, 0, 1, 3, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [24, 57]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_18_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 2, 0, 5, 0, 0, 1, 3, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [25, 57]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_18_move_22(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 6, 0, 0, 1, 3, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [26, 57]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_18_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 4, 2, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [31, 57]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_24(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 3, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [31, 58]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_18_move_25(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 3, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [31, 59]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_18_move_26(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [31, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [34, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_28(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [34, 61]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_29(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [34, 61]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_30(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [34, 62]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_18_move_31(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [34, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [34, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_33(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [34, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_34(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [34, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_35(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [34, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_36(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [34, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_37(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [34, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_38(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 62]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_18_move_39(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_40(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_41(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_42(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_43(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_44(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_45(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_46(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_48(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_49(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [36, 62]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_19_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [1, 13]

    def test_round_19_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 11, 4, 12, 3, 12, 11, 0, 1, 11, 1, 11, 2]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [6, 13]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_19_move_2(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 13, 6, 14, 1, 2, 14, 1, 4, 1, 3, 13, 4]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [9, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 18, 11, 0, 4, 0, 4, 1, 3, 7, 3, 19, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [9, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 20, 13, 0, 2, 1, 0, 1, 5, 1, 5, 21, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [11, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_5(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 1, 15, 2, 4, 3, 2, 2, 2, 0, 8, 24, 3]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [11, 21]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_19_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 2, 4, 3, 2, 0, 3, 0, 8, 24, 3]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [11, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 4, 4, 3, 4, 6, 4, 3, 2, 12, 0, 3]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [16, 37]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_19_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 5, 4, 5, 6, 4, 3, 2, 12, 0, 3]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [17, 37]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_19_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 2, 0, 0, 2, 6, 1, 15, 3, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [30, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_10(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 1, 2, 0, 0, 0, 7, 0, 16, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [30, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 1, 0, 1, 0, 0, 7, 0, 16, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [31, 38]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_19_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 1, 0, 1, 0, 7, 0, 16, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_13(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 0, 7, 0, 16, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 16, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [40, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [40, 42]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_19_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 0, 2, 0, 2, 0, 2, 0, 1, 1, 4]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [40, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_17(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 3, 0, 0, 0, 2, 0, 1, 1, 4]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [43, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 2, 0, 1, 1, 1, 0, 1, 2, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [43, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_19(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 3, 0, 1, 1, 0, 0, 1, 2, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [45, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_20(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 3, 0, 1, 0, 1, 0, 1, 2, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [45, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 2, 0, 1, 0, 1, 2, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [46, 44]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_19_move_22(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_23(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_19_move_24(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_25(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_26(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_27(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_28(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_29(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_30(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_31(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_32(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_33(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_34(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_35(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_36(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_37(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_38(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 46]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_19_move_39(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 47]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_20_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [2, 5]

    def test_round_20_move_1(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 2, 12, 4, 12, 12, 0, 3, 12, 12, 12, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [2, 11]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 3, 0, 15, 1, 2, 15, 0, 6, 15, 15, 0, 3, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [2, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 4, 1, 1, 0, 4, 17, 0, 7, 16, 16, 1, 4, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [4, 17]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_4(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [10, 0, 8, 1, 7, 4, 3, 0, 15, 6, 1, 9, 1, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 9, 2, 8, 5, 4, 0, 16, 1, 3, 11, 0, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [12, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_6(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 0, 5, 3, 14, 11, 10, 0, 2, 0, 8, 4, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [18, 19]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 0, 0, 4, 15, 12, 11, 0, 2, 0, 8, 4, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [19, 19]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 0, 0, 0, 16, 13, 12, 0, 2, 0, 8, 4, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [20, 19]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 2, 2, 2, 2, 16, 1, 0, 4, 2, 10, 6, 2, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [22, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 5, 5, 5, 0, 2, 4, 0, 7, 1, 0, 10, 6, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [22, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 5, 5, 5, 0, 0, 5, 0, 7, 1, 0, 10, 6, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [23, 31]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 6, 0, 1, 2, 2, 7, 0, 1, 2, 1, 11, 7, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [25, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 0, 3, 4, 5, 5, 1, 0, 2, 5, 2, 0, 2, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [25, 35]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 2, 5, 1, 7, 7, 0, 0, 4, 1, 0, 2, 4, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [25, 38]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 5, 1, 7, 7, 0, 0, 4, 1, 0, 2, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [25, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 0, 2, 8, 8, 1, 0, 4, 1, 0, 2, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [26, 39]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 0, 2, 8, 0, 2, 0, 5, 2, 1, 3, 5, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [27, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_18(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 3, 1, 2, 8, 0, 2, 0, 5, 0, 2, 0, 6, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [27, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_19(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 3, 1, 2, 8, 0, 0, 0, 0, 1, 3, 1, 7, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [32, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_20(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 1, 2, 8, 0, 0, 0, 0, 1, 0, 2, 8, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [32, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 3, 1, 0, 9, 1, 0, 0, 0, 1, 0, 2, 8, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [32, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 4, 2, 1, 10, 0, 1, 0, 1, 1, 0, 2, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [32, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_23(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [1, 4, 2, 1, 10, 0, 0, 0, 1, 1, 0, 2, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 41]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 3, 2, 11, 0, 0, 0, 0, 1, 0, 2, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [35, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_25(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 1, 3, 2, 11, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [35, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_26(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 1, 3, 0, 12, 1, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [35, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_27(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 1, 3, 0, 12, 1, 0, 0, 0, 0, 1, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [35, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_28(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 13, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 42]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_29(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 1, 1, 13, 0, 1, 0, 0, 0, 1, 0, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_30(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 13, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_31(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 1, 2, 0, 1, 0, 3, 0, 1, 1, 2, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [38, 45]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 3, 0, 1, 0, 3, 0, 1, 1, 0, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [41, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_33(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 3, 0, 1, 0, 3, 0, 0, 0, 1, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [41, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_34(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [1, 0, 3, 0, 1, 0, 0, 0, 1, 1, 1, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [42, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_35(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 2, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [42, 50]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_36(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 50]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_37(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 50]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_38(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 50]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_39(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 51]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_40(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_20_move_41(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_42(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_43(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_20_move_44(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [46, 52]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_21_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [4, 3]

    def test_round_21_move_1(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 8, 0, 8]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [6, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_21_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 4, 6, 15, 15, 5, 2, 3, 15, 6, 1, 2, 7, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [13, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 5, 7, 16, 16, 0, 3, 4, 16, 7, 2, 0, 1, 3]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [13, 5]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_21_move_4(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 5, 0, 16, 16, 0, 3, 0, 17, 8, 3, 0, 1, 3]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [13, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 7, 0, 18, 0, 3, 0, 0, 19, 10, 0, 2, 3, 5]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [18, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 9, 2, 20, 2, 5, 0, 2, 0, 13, 0, 5, 6, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [18, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 9, 2, 20, 0, 6, 0, 0, 0, 13, 0, 5, 6, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [21, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 9, 2, 20, 0, 6, 0, 0, 0, 13, 0, 5, 6, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [21, 16]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_21_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 10, 3, 21, 1, 6, 0, 0, 0, 13, 0, 5, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [21, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_10(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 10, 3, 21, 1, 0, 1, 1, 1, 14, 1, 5, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [22, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_11(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 3, 21, 1, 0, 1, 0, 0, 15, 0, 6, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [22, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 22, 2, 1, 1, 0, 0, 15, 0, 6, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [22, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 1, 23, 3, 2, 2, 1, 1, 1, 0, 8, 0, 3]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [22, 30]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_21_move_14(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 3, 2, 2, 1, 1, 0, 0, 8, 0, 3]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [22, 54]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 3, 0, 3, 1, 1, 0, 0, 8, 0, 3]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [23, 54]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_21_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 1, 4, 1, 1, 0, 0, 8, 0, 3]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [24, 54]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_21_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 2, 2, 1, 1, 8, 0, 3]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [25, 54]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_18(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 2, 2, 1, 1, 1, 1, 2, 2, 1, 0, 0, 1, 4]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [25, 55]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_19(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 2, 0, 2, 0, 0, 3, 2, 1, 0, 1, 4]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [26, 55]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_20(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 3, 1, 3, 1, 2, 0, 0, 3, 2, 1, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [26, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_21(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 3, 0, 0, 2, 3, 1, 0, 3, 2, 1, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [27, 56]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_21_move_22(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 3, 0, 0, 2, 0, 2, 1, 3, 2, 1, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [28, 56]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_23(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 2, 0, 0, 3, 2, 1, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [28, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_24(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 1, 0, 3, 2, 1, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [29, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_25(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 1, 0, 3, 0, 2, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [29, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_26(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 2, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [31, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_27(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 2, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [31, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 3, 0, 2, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [31, 60]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_29(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [31, 61]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_30(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 61]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_21_move_31(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 61]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_32(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 61]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_33(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 61]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_34(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 62]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_21_move_35(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_36(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_37(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_38(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 62]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_39(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 63]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_21_move_40(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 63]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_41(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 63]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_42(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_43(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_44(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [32, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_45(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [33, 64]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_21_move_46(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [33, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_47(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [33, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_48(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [33, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_49(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [33, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_50(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [33, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_51(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [33, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_52(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [33, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_53(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [33, 64]
        assert cond is None
        gstate.cond = cond

    def test_round_21_move_54(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [34, 64]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_22_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [6, 15]

    def test_round_22_move_1(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 8, 1, 9, 9, 8, 8, 8, 0, 8, 8, 8]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [8, 15]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_2(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 5, 13, 4, 13, 1, 1, 4, 2, 12, 12]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [13, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 4, 6, 14, 5, 14, 2, 2, 5, 1, 14, 1]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [13, 17]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_4(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 12, 6, 0, 0, 8, 0, 6, 13, 2, 5, 6]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [13, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_5(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 7, 1, 1, 9, 1, 7, 0, 3, 6, 7]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [29, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_6(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 2, 0, 4, 12, 1, 0, 4, 1, 0, 11]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [29, 31]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_7(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 3, 2, 0, 4, 12, 1, 0, 0, 2, 1, 12]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [29, 32]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_8(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 4, 3, 1, 5, 13, 2, 1, 1, 3, 1, 1]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [29, 34]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_9(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 4, 3, 1, 5, 13, 2, 1, 1, 0, 2, 2]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [29, 35]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 4, 2, 6, 14, 0, 2, 2, 1, 2, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [29, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_11(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 4, 2, 0, 15, 1, 3, 3, 0, 3, 1]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [30, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_12(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 4, 2, 0, 15, 0, 0, 4, 1, 4, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [30, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 3, 1, 16, 1, 0, 4, 1, 4, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [31, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 3, 1, 16, 0, 1, 4, 1, 4, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [31, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 2, 2, 4, 1, 2, 3, 6, 3, 0, 2]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [34, 37]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_16(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 4, 0, 5, 0, 0, 0, 7, 4, 1, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [39, 37]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_17(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 5, 1, 5, 0, 0, 0, 0, 5, 2, 1]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [39, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_18(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 6, 0, 6, 0, 0, 0, 0, 5, 2, 1]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [40, 38]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_19(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 7, 1, 0, 0, 1, 1, 1, 0, 3, 2]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [43, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_20(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 8, 0, 0, 0, 1, 1, 1, 0, 3, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [43, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 1, 3, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [44, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_22(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 1, 0, 3, 0, 2, 4, 1]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [44, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_23(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 3, 5, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [45, 41]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 2, 1, 0, 0, 1, 0, 1, 3, 0, 1]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [45, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_25(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 2, 0, 1, 0, 1, 0, 1, 3, 0, 1]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [45, 42]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 2, 0, 1, 0, 1, 0, 1, 0, 1, 2]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [45, 43]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 2, 0, 1, 0, 1, 0, 0, 1, 1, 2]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [45, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_28(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 2, 0, 0, 0, 1, 0, 0, 1, 1, 2]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [46, 43]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_29(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 1, 1, 0, 1, 0, 0, 1, 1, 2]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [46, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_30(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 1, 1, 0, 0, 1, 0, 1, 1, 2]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [46, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_31(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 1, 0, 0, 0, 1, 0, 1, 1, 2]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [47, 43]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_32(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 2]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [48, 43]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_33(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 2]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 43]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_34(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 2]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_35(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 3]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 44]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_22_move_36(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 3]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 3]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 44]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_38(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_39(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [50, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_40(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [50, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_41(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [52, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_42(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [52, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_43(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [52, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_44(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [52, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_45(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [52, 45]
        assert cond is None
        gstate.cond = cond

    def test_round_22_move_46(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, T, T, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [52, 46]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_23_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [3, 4]

    def test_round_23_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 13, 13, 4, 13, 13, 13, 0, 2, 0, 1, 3, 0, 4]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [3, 11]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_23_move_2(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 15, 15, 6, 15, 15, 1, 0, 3, 1, 1, 1, 2, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [3, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 16, 16, 1, 17, 17, 0, 0, 5, 1, 2, 0, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [5, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 16, 16, 1, 17, 17, 0, 0, 0, 2, 3, 1, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [5, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_5(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [6, 4, 22, 0, 22, 2, 1, 0, 2, 0, 0, 1, 2, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [14, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_6(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [6, 4, 22, 0, 22, 2, 1, 0, 0, 1, 1, 1, 2, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [14, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [6, 0, 23, 1, 23, 0, 2, 0, 1, 1, 1, 1, 2, 6]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [15, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 26, 4, 2, 3, 5, 0, 4, 4, 0, 4, 5, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [15, 20]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_23_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 2, 4, 9, 1, 0, 10, 0, 2, 5, 6, 1, 11, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [15, 26]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_23_move_10(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [7, 0, 0, 15, 7, 2, 0, 0, 8, 1, 0, 6, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [15, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_11(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [8, 1, 1, 16, 0, 3, 1, 0, 9, 0, 1, 0, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [19, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [8, 1, 0, 16, 0, 3, 1, 0, 9, 0, 0, 0, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [19, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_13(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 0, 5, 2, 3, 8, 3, 0, 0, 2, 4, 0, 5, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [24, 38]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_23_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 0, 5, 2, 3, 0, 4, 0, 1, 3, 5, 1, 6, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [25, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_15(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 6, 3, 4, 1, 4, 0, 1, 3, 0, 2, 7, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [25, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 6, 3, 4, 0, 0, 0, 2, 4, 1, 0, 8, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [30, 39]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 2, 7, 4, 5, 1, 1, 0, 0, 5, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [30, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [1, 2, 7, 4, 5, 0, 0, 0, 1, 5, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [31, 40]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 3, 0, 5, 6, 1, 1, 0, 1, 1, 2, 0, 2, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [31, 42]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_23_move_20(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 4, 1, 5, 6, 1, 1, 0, 1, 0, 0, 1, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [31, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [1, 4, 1, 0, 7, 2, 2, 0, 0, 1, 1, 1, 3, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [32, 43]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_22(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 0, 2, 0, 8, 3, 0, 0, 1, 1, 0, 2, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [32, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_23(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 0, 2, 0, 0, 4, 1, 0, 2, 2, 1, 3, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 46]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 3, 1, 0, 4, 1, 0, 2, 2, 1, 3, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [33, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_25(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 1, 5, 0, 0, 0, 3, 2, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_26(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 1, 5, 0, 0, 0, 0, 3, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [36, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 0, 0, 0, 2, 0, 1, 0, 1, 1, 4, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [40, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 0, 0, 0, 2, 0, 1, 0, 0, 0, 5, 1, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [40, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_29(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 2, 0, 1, 0, 0, 0, 5, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [42, 47]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_30(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 2, 0, 1, 0, 0, 0, 0, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [42, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_31(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 2, 0, 1, 0, 0, 0, 0, 1, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [42, 48]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 2, 0, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [42, 49]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_23_move_33(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 2, 0, 1, 0, 0, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [42, 49]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_34(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 2, 0, 0, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [43, 49]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_23_move_35(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [44, 49]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_36(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [44, 49]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_37(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [44, 49]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_38(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [44, 51]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_39(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [44, 51]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_40(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [44, 51]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_41(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 51]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_23_move_42(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 51]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_43(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_44(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_45(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_46(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_47(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_48(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_49(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_50(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_51(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_52(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_53(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_54(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_55(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [45, 52]
        assert cond is None
        gstate.cond = cond

    def test_round_23_move_56(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F, F, F]
        assert game.store == [46, 52]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_24_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [4, 3]

    def test_round_24_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 11, 11, 0, 1, 12, 1, 1, 11, 3, 11, 11, 2, 11]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [9, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_24_move_2(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 12, 12, 1, 0, 0, 2, 2, 12, 0, 12, 12, 3, 12]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [15, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 13, 2, 1, 1, 3, 3, 13, 1, 13, 13, 1, 14]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [15, 5]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_24_move_4(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 1, 14, 0, 2, 2, 4, 1, 15, 3, 0, 14, 2, 15]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [15, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_5(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 8, 1, 11, 0, 2, 4, 1, 11, 8, 5, 10, 3]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 3, 11, 4, 14, 1, 4, 0, 1, 13, 1, 7, 2, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [24, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 4, 12, 5, 0, 2, 5, 1, 2, 0, 2, 8, 3, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [40, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_8(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 0, 15, 1, 3, 5, 2, 3, 0, 4, 1, 0, 2, 5]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [40, 17]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_24_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 1, 16, 2, 0, 0, 3, 4, 0, 4, 1, 0, 2, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [40, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_10(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [0, 1, 16, 2, 0, 0, 0, 5, 1, 4, 1, 0, 2, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [41, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_11(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 16, 2, 0, 0, 0, 5, 1, 0, 2, 1, 3, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [41, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_12(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 1, 4, 2, 0, 2, 6, 2, 1, 3, 2, 4, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [43, 25]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_24_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 3, 1, 3, 6, 2, 1, 3, 2, 4, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [44, 25]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_24_move_14(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 2, 4, 6, 2, 1, 3, 2, 4, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [45, 25]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_24_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 2, 4, 6, 2, 1, 0, 2, 4, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_16(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 0, 2, 4, 6, 2, 1, 0, 2, 0, 3]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 2, 0, 1, 0, 2, 4, 6, 2, 1, 0, 2, 0, 3]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_18(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 3, 1, 1, 0, 2, 4, 6, 2, 1, 0, 2, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [49, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 2, 2, 0, 2, 4, 6, 2, 0, 0, 2, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_20(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 2, 4, 6, 0, 1, 0, 2, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [51, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_21(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 2, 4, 6, 0, 0, 0, 2, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [53, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_22(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 2, 4, 6, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [53, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_23(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 2, 4, 6, 0, 0, 0, 0, 1, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [53, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_24(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 2, 4, 6, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [53, 31]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_24_move_25(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 2, 4, 6, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [53, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 5, 6, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [54, 31]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_24_move_27(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 5, 6, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [54, 31]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_28(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 5, 6, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [54, 32]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_24_move_29(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 5, 0, 1, 1, 1, 1, 1, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [54, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_30(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 1, 2, 2, 2, 0, 2, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [55, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_31(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 1, 0, 3, 0, 1, 3, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [55, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_32(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [59, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_33(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [59, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_34(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 2]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [59, 33]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_35(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [59, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_36(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_37(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_38(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_39(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_40(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 34]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_41(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 35]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_24_move_42(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [61, 35]
        assert cond is None
        gstate.cond = cond

    def test_round_24_move_43(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [62, 35]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_24_move_44(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [T, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [63, 35]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_25_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 7, 7, 7, 0, 0, 7, 7, 7, 7, 7]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [14, 0]

    def test_round_25_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [8, 8, 8, 8, 8, 1, 9, 0, 0, 8, 8, 8, 8, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [16, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_25_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [5, 1, 2, 0, 3, 6, 14, 0, 0, 4, 0, 13, 13, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 2, 0, 1, 4, 7, 15, 0, 0, 5, 1, 0, 14, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [35, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 7, 0, 6, 2, 12, 4, 0, 0, 9, 2, 4, 1, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [40, 5]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_25_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 10, 3, 9, 3, 2, 1, 0, 0, 0, 5, 7, 2, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [44, 5]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_25_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [4, 12, 5, 0, 6, 1, 3, 0, 0, 2, 0, 9, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [46, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [6, 1, 6, 1, 7, 2, 4, 0, 0, 3, 1, 10, 1, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [46, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_8(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [7, 2, 1, 0, 9, 4, 0, 0, 0, 1, 3, 12, 3, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [48, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_9(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 2, 0, 10, 5, 1, 0, 0, 2, 0, 13, 4, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [48, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 2, 1, 3, 0, 8, 1, 0, 0, 4, 0, 15, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [50, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_11(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 0, 2, 4, 1, 8, 1, 0, 0, 0, 1, 16, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [50, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_12(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 0, 2, 0, 2, 9, 2, 0, 0, 0, 1, 16, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [51, 11]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_25_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 3, 1, 0, 10, 0, 0, 0, 0, 0, 17, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [54, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 3, 1, 0, 10, 0, 0, 0, 0, 0, 17, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [54, 12]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_25_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 1, 2, 5, 4, 1, 3, 0, 0, 1, 3, 1, 4, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [54, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_16(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 0, 3, 0, 5, 2, 4, 0, 0, 0, 0, 0, 5, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [60, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_17(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 2, 1, 2, 7, 0, 1, 0, 0, 2, 2, 0, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [60, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_18(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 2, 1, 2, 7, 0, 0, 0, 0, 2, 2, 0, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [61, 18]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_25_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 8, 1, 0, 0, 0, 2, 2, 0, 2, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [61, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_20(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 8, 1, 0, 0, 0, 2, 2, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [61, 19]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_25_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 2, 0, 0, 8, 1, 0, 0, 0, 0, 3, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [61, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_22(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 8, 1, 0, 0, 0, 0, 0, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [65, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_23(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [65, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_24(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [65, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_25(self, gstate):
        game = gstate.game
        cond = game.move(gi.PASS_TOKEN)
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [65, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_26(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 2, 1, 0, 0, 1, 1, 1, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [68, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_27(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 2, 1, 0, 0, 1, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [68, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_25_move_28(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 2, 0, 0, 0, 1, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [69, 22]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_25_move_29(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [70, 22]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_round_25_move_30(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, F, F, F, F]
        assert game.store == [71, 22]
        assert cond.name == "WIN"
        assert game.mdata.winner is False
        gstate.cond = cond
