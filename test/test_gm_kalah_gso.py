# -*- coding: utf-8 -*-
"""Test the Kalah_GSO game.
Tests sow stores and cross capture with pick own.

Created on Thu Aug 17 06:42:25 2023
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

    game, _ = man_config.make_game('./GameProps/Kalah_GSO.txt')
    gstate = GameTestData(game)
    return gstate


@pytest.mark.incremental
class TestTie:

    def test_setup(self, gstate):

        game = gstate.game
        game.turn = False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 4, 0, 5, 5, 5, 4, 4, 4, 4, 4, 4]
        assert game.store == [1, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 4, 0, 5, 5, 0, 5, 5, 5, 5, 4, 4]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 1, 5, 5, 0, 5, 5, 5, 5, 4, 0]
        assert game.store == [2, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 6, 2, 6, 6, 0, 0, 5, 5, 5, 4, 0]
        assert game.store == [8, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 6, 2, 6, 6, 0, 0, 0, 6, 6, 5, 1]
        assert game.store == [8, 2]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 6, 2, 6, 6, 0, 0, 0, 6, 6, 5, 0]
        assert game.store == [8, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 7, 2, 6, 6, 0, 0, 0, 0, 7, 6, 1]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [1, 7, 2, 6, 0, 1, 1, 1, 1, 8, 6, 1]
        assert game.store == [9, 4]
        assert cond is None
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [1, 7, 2, 6, 0, 1, 1, 1, 1, 8, 6, 0]
        assert game.store == [9, 5]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 8, 3, 7, 0, 1, 1, 1, 1, 8, 0, 1]
        assert game.store == [9, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 8, 3, 7, 0, 0, 1, 1, 1, 8, 0, 1]
        assert game.store == [10, 6]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 8, 0, 8, 1, 0, 0, 1, 1, 8, 0, 1]
        assert game.store == [12, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [2, 8, 0, 8, 1, 0, 0, 0, 2, 8, 0, 1]
        assert game.store == [12, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [2, 8, 0, 0, 2, 1, 1, 1, 3, 9, 1, 1]
        assert game.store == [13, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [2, 8, 0, 0, 2, 1, 1, 1, 3, 9, 1, 0]
        assert game.store == [13, 7]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_16(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 8, 0, 0, 2, 1, 1, 1, 0, 10, 2, 0]
        assert game.store == [13, 10]
        assert cond is None
        gstate.cond = cond

    def test_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 8, 0, 0, 2, 0, 1, 1, 0, 10, 2, 0]
        assert game.store == [14, 10]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_18(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 8, 0, 0, 0, 1, 1, 1, 0, 10, 2, 0]
        assert game.store == [15, 10]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 8, 0, 0, 0, 0, 1, 1, 0, 10, 2, 0]
        assert game.store == [16, 10]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_20(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 1, 2, 2, 1, 10, 2, 0]
        assert game.store == [17, 10]
        assert cond is None
        gstate.cond = cond

    def test_move_21(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 1, 0, 3, 2, 10, 2, 0]
        assert game.store == [17, 10]
        assert cond is None
        gstate.cond = cond

    def test_move_22(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 3, 2, 10, 2, 0]
        assert game.store == [18, 10]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_23(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 3, 2, 10, 2, 0]
        assert game.store == [18, 10]
        assert cond is None
        gstate.cond = cond

    def test_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 3, 2, 10, 0, 1]
        assert game.store == [18, 11]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_25(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 2, 0, 0, 0, 3, 11, 1, 1]
        assert game.store == [18, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_26(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 3, 11, 1, 1]
        assert game.store == [19, 11]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_27(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 3, 11, 1, 1]
        assert game.store == [20, 11]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_28(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 1, 1]
        assert game.store == [24, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_29(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [24, 24]
        assert cond.name == "TIE"
        gstate.cond = cond


@pytest.mark.incremental
class TestWin:

    def test_win(self, gstate):

        game = gstate.game
        game.turn = False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 4, 0, 5, 5, 5, 4, 4, 4, 4, 4, 4]
        assert game.store == [1, 0]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [4, 4, 0, 5, 5, 0, 5, 5, 5, 5, 4, 4]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 5, 1, 5, 5, 0, 5, 5, 5, 5, 4, 0]
        assert game.store == [2, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 0, 2, 6, 6, 1, 5, 5, 5, 5, 4, 0]
        assert game.store == [3, 1]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 0, 2, 6, 6, 0, 5, 5, 5, 5, 4, 0]
        assert game.store == [4, 1]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 3, 7, 7, 0, 0, 5, 5, 5, 4, 0]
        assert game.store == [10, 1]
        assert cond is None
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 1, 3, 7, 7, 0, 0, 0, 6, 6, 5, 1]
        assert game.store == [10, 2]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 3, 7, 7, 0, 0, 0, 6, 6, 5, 0]
        assert game.store == [10, 3]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 4, 7, 7, 0, 0, 0, 6, 0, 6, 1]
        assert game.store == [10, 4]
        assert cond is None
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [1, 2, 0, 8, 8, 1, 0, 0, 6, 0, 6, 1]
        assert game.store == [11, 4]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 2, 0, 8, 8, 0, 0, 0, 6, 0, 6, 1]
        assert game.store == [12, 4]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 0, 8, 8, 0, 0, 0, 6, 0, 6, 1]
        assert game.store == [12, 4]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 4, 0, 8, 8, 0, 0, 0, 0, 1, 7, 2]
        assert game.store == [12, 5]
        assert cond is None
        gstate.cond = cond

    def test_move_14(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 9, 9, 1, 0, 0, 0, 1, 7, 2]
        assert game.store == [12, 5]
        assert cond is None
        gstate.cond = cond

    def test_move_15(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 1, 2, 10, 10, 1, 0, 0, 0, 1, 0, 3]
        assert game.store == [12, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [2, 1, 2, 10, 10, 0, 0, 0, 0, 1, 0, 3]
        assert game.store == [13, 6]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_17(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [3, 2, 2, 10, 0, 1, 1, 1, 1, 2, 1, 4]
        assert game.store == [14, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_18(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [3, 2, 2, 10, 0, 1, 1, 1, 0, 3, 1, 4]
        assert game.store == [14, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_19(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 2, 2, 10, 0, 0, 1, 1, 0, 3, 1, 4]
        assert game.store == [15, 6]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_20(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 2, 0, 11, 0, 0, 1, 0, 0, 3, 1, 4]
        assert game.store == [17, 6]
        assert cond is None
        gstate.cond = cond

    def test_move_21(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 3, 1, 11, 0, 0, 1, 0, 0, 3, 1, 0]
        assert game.store == [17, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_22(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [5, 4, 1, 0, 1, 1, 2, 1, 1, 4, 2, 1]
        assert game.store == [18, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_23(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [5, 4, 1, 0, 1, 1, 2, 1, 0, 5, 2, 1]
        assert game.store == [18, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_24(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 4, 1, 0, 1, 0, 2, 1, 0, 5, 2, 1]
        assert game.store == [19, 7]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_25(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [5, 4, 1, 0, 0, 0, 0, 1, 0, 5, 2, 1]
        assert game.store == [22, 7]
        assert cond is None
        gstate.cond = cond

    def test_move_26(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [5, 4, 1, 0, 0, 0, 0, 1, 0, 5, 2, 0]
        assert game.store == [22, 8]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_27(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [5, 4, 1, 0, 0, 0, 0, 1, 0, 5, 0, 1]
        assert game.store == [22, 9]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_28(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [5, 4, 1, 0, 0, 0, 0, 1, 0, 5, 0, 0]
        assert game.store == [22, 10]
        assert cond.name == "REPEAT_TURN"
        gstate.cond = cond

    def test_move_29(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [5, 4, 1, 0, 0, 0, 0, 0, 1, 5, 0, 0]
        assert game.store == [22, 10]
        assert cond is None
        gstate.cond = cond

    def test_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 4, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [24, 11]
        assert cond is None
        gstate.cond = cond

    def test_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 6, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1]
        assert game.store == [25, 11]
        assert cond.name == "WIN"
        gstate.cond = cond
