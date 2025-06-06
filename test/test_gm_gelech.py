"""
Created on Fri Mar  7 13:25:08 2025
@author: Ann"""


import pytest
pytestmark = pytest.mark.integtest

from context import game_info as gi
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

    game, _ = man_config.make_game('./GameProps/Gelech.txt')
    gstate = GameTestData(game)
    return gstate


CW = gi.Direct.CW
CCW = gi.Direct.CCW


@pytest.mark.incremental
class TestGelech:

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = True
        game.starter = True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 0, 4, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 0, 4, 5, 1, 6, 6, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 0, 0, 6, 2, 7, 7, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [6, 6, 6, 6, 1, 1, 0, 2, 7, 7, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [6, 6, 6, 6, 2, 0, 0, 0, 7, 7, 6, 0]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [7, 7, 7, 7, 3, 0, 0, 0, 7, 0, 7, 1]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [8, 8, 0, 7, 3, 0, 0, 1, 8, 1, 8, 2]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [8, 8, 0, 7, 0, 0, 1, 0, 8, 1, 8, 2]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [9, 0, 0, 7, 0, 1, 2, 1, 9, 2, 9, 3]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [9, 0, 0, 7, 0, 1, 2, 1, 9, 0, 10, 4]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [10, 1, 1, 0, 0, 1, 0, 1, 10, 1, 11, 5]
        assert game.store == [4, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [11, 2, 1, 1, 1, 2, 1, 1, 0, 2, 12, 6]
        assert game.store == [4, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [11, 2, 2, 0, 1, 2, 1, 0, 0, 0, 12, 6]
        assert game.store == [7, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [11, 2, 2, 0, 1, 1, 2, 1, 1, 1, 13, 0]
        assert game.store == [7, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [11, 2, 2, 0, 1, 0, 1, 0, 1, 1, 13, 0]
        assert game.store == [10, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [12, 3, 1, 1, 2, 1, 2, 1, 2, 3, 1, 1]
        assert game.store == [10, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [12, 3, 1, 1, 2, 0, 1, 1, 0, 0, 1, 1]
        assert game.store == [17, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [17, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [17, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [1, 0, 2, 0, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [17, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [17, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [17, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [17, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0]
        assert game.store == [17, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 1]
        assert game.store == [17, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 1]
        assert game.store == [17, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 1]
        assert game.store == [17, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [17, 31]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 0, 5, 5, 5, 5, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 0, 6, 6, 6, 6, 0, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 1, 0, 6, 6, 6, 0, 4, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [6, 5, 5, 5, 1, 0, 0, 7, 7, 1, 5, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [7, 0, 5, 5, 1, 0, 0, 0, 8, 2, 6, 7]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [7, 0, 5, 5, 2, 1, 1, 1, 9, 3, 7, 0]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [7, 0, 0, 6, 3, 2, 1, 2, 9, 3, 7, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [8, 0, 0, 6, 3, 0, 1, 2, 9, 0, 8, 1]
        assert game.store == [8, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [9, 1, 1, 0, 3, 0, 1, 2, 9, 1, 9, 2]
        assert game.store == [8, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [10, 2, 0, 0, 3, 0, 1, 2, 9, 1, 9, 0]
        assert game.store == [8, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [10, 3, 1, 1, 0, 0, 1, 2, 9, 1, 9, 0]
        assert game.store == [8, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [10, 3, 0, 1, 0, 1, 0, 2, 9, 1, 9, 0]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [10, 3, 0, 1, 1, 0, 0, 2, 0, 1, 9, 0]
        assert game.store == [17, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_14(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [10, 4, 1, 2, 2, 1, 1, 3, 1, 2, 0, 0]
        assert game.store == [17, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_15(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [10, 5, 0, 2, 2, 1, 0, 3, 1, 0, 0, 0]
        assert game.store == [20, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_16(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [10, 5, 0, 0, 2, 1, 0, 0, 2, 1, 1, 0]
        assert game.store == [20, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_17(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 6, 1, 1, 3, 2, 1, 1, 3, 2, 2, 0]
        assert game.store == [20, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_18(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 6, 1, 1, 0, 0, 2, 0, 3, 2, 2, 0]
        assert game.store == [20, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_19(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 2, 2, 1, 1, 3, 1, 0, 0, 2, 0]
        assert game.store == [25, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_20(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 0, 2, 2, 0, 1, 3, 1, 1, 1, 0, 0]
        assert game.store == [25, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_21(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 0, 2, 2, 1, 0, 0, 1, 1, 1, 0, 0]
        assert game.store == [28, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_22(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 20]
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
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_2(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 0, 5, 5, 5, 5, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_3(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [5, 5, 6, 6, 1, 6, 6, 0, 5, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_4(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [5, 5, 6, 6, 0, 7, 6, 0, 5, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_5(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [6, 6, 7, 7, 1, 8, 0, 0, 5, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_6(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [6, 6, 7, 7, 0, 9, 0, 0, 5, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_7(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [7, 7, 8, 7, 0, 9, 0, 0, 5, 4, 0, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_8(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [8, 8, 9, 7, 0, 0, 1, 1, 6, 5, 1, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_9(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [8, 0, 9, 7, 0, 0, 1, 1, 6, 5, 0, 3]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_10(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [8, 0, 9, 0, 1, 1, 2, 2, 7, 6, 1, 3]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_11(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [8, 1, 10, 1, 2, 2, 3, 3, 0, 6, 1, 3]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_12(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [8, 1, 10, 1, 0, 3, 4, 3, 0, 6, 0, 3]
        assert game.store == [1, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_13(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [9, 2, 11, 2, 0, 3, 4, 3, 0, 0, 1, 4]
        assert game.store == [1, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_14(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [10, 3, 0, 3, 1, 4, 5, 4, 1, 1, 2, 5]
        assert game.store == [1, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_15(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [10, 3, 0, 0, 1, 4, 5, 5, 0, 1, 2, 5]
        assert game.store == [1, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_16(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [11, 0, 0, 0, 1, 4, 5, 0, 0, 1, 3, 6]
        assert game.store == [6, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_17(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [11, 0, 0, 0, 1, 4, 5, 0, 0, 0, 4, 6]
        assert game.store == [6, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_18(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [11, 1, 1, 1, 2, 0, 5, 0, 0, 0, 4, 6]
        assert game.store == [6, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_19(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [11, 2, 2, 2, 3, 1, 0, 0, 0, 0, 4, 6]
        assert game.store == [6, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_20(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [11, 3, 3, 0, 3, 1, 0, 0, 0, 0, 4, 6]
        assert game.store == [6, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_21(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [11, 3, 3, 0, 3, 1, 1, 1, 1, 1, 0, 6]
        assert game.store == [6, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_22(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 4, 4, 1, 4, 2, 1, 2, 2, 2, 1, 7]
        assert game.store == [7, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_23(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 4, 1, 4, 0, 1, 2, 2, 2, 0, 8]
        assert game.store == [7, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_24(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 1, 5, 2, 0, 0, 1, 2, 0, 2, 0, 8]
        assert game.store == [9, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_25(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [1, 1, 5, 2, 0, 0, 1, 3, 1, 0, 0, 8]
        assert game.store == [9, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_26(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 3, 1, 1, 2, 4, 1, 0, 0, 0]
        assert game.store == [17, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_27(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 1, 2, 4, 0, 1, 0, 0]
        assert game.store == [17, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_28(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 20]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_4_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_4_move_1(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [5, 5, 0, 4, 4, 4, 4, 4, 4, 4, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_2(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [6, 5, 0, 4, 4, 4, 4, 4, 0, 5, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_3(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [7, 6, 1, 5, 0, 4, 4, 4, 0, 5, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_4(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [8, 7, 2, 6, 1, 4, 4, 4, 0, 5, 0, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_5(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [8, 7, 0, 7, 2, 4, 4, 0, 0, 5, 0, 7]
        assert game.store == [4, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_6(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [8, 7, 0, 7, 2, 4, 0, 1, 1, 6, 1, 7]
        assert game.store == [4, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 7, 0, 7, 3, 5, 1, 2, 2, 7, 2, 8]
        assert game.store == [4, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 7, 0, 7, 3, 0, 1, 2, 3, 8, 0, 8]
        assert game.store == [4, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_9(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [0, 8, 1, 8, 0, 0, 1, 2, 3, 8, 0, 8]
        assert game.store == [4, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_10(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 8, 1, 8, 0, 1, 2, 0, 3, 8, 0, 8]
        assert game.store == [4, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_11(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 8, 1, 8, 1, 0, 0, 0, 3, 0, 0, 8]
        assert game.store == [14, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_12(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 8, 1, 8, 1, 1, 1, 1, 0, 0, 0, 8]
        assert game.store == [14, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 8, 1, 2, 1, 1, 1, 1, 1, 9]
        assert game.store == [16, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_14(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 9]
        assert game.store == [16, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_15(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_16(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_17(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_18(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 0, 1]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_19(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 1]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_20(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_21(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 1]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_22(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 0, 1]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_23(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 1]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_24(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 0, 1]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_25(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 1]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_26(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_27(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 1]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_28(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_29(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_30(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 2, 2, 0, 0]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_31(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 2, 2, 0, 0]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_32(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 2, 2, 0, 0]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_33(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 2, 0, 0, 0]
        assert game.store == [27, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_34(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 2, 0, 0, 0]
        assert game.store == [27, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_35(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [29, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_36(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [29, 19]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_5_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_5_move_1(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 4, 0, 5, 5, 5, 5, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 6, 6, 6, 5, 4, 0, 5, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 7, 6, 6, 5, 4, 0, 5, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 7, 6, 6, 5, 5, 1, 6, 6, 6, 0, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_6(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 7, 0, 7, 6, 6, 2, 7, 7, 6, 0, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_7(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 7, 0, 7, 7, 7, 0, 7, 7, 6, 0, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 8, 8, 8, 1, 8, 8, 6, 0, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_9(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [1, 1, 2, 9, 9, 1, 2, 9, 0, 6, 0, 0]
        assert game.store == [0, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_10(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [2, 2, 0, 9, 9, 1, 0, 9, 0, 6, 0, 0]
        assert game.store == [2, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_11(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [2, 2, 0, 10, 10, 2, 1, 10, 1, 0, 0, 0]
        assert game.store == [2, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_12(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [3, 3, 1, 10, 0, 3, 2, 11, 2, 1, 1, 1]
        assert game.store == [2, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_13(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 10, 0, 3, 0, 12, 3, 1, 1, 1]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_14(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 11, 1, 0, 0, 12, 3, 1, 1, 1]
        assert game.store == [2, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_15(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 11, 1, 0, 0, 12, 3, 1, 1, 0]
        assert game.store == [2, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_16(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 11, 1, 0, 0, 0, 3, 1, 1, 1]
        assert game.store == [14, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_17(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 11, 1, 1, 1, 1, 0, 1, 1, 1]
        assert game.store == [14, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_18(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 2, 2, 1, 1, 1, 2, 2, 2]
        assert game.store == [16, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_19(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 0, 1, 0, 1, 1, 2, 2, 2]
        assert game.store == [16, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_20(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [2, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0]
        assert game.store == [22, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_21(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [2, 0, 1, 0, 0, 1, 0, 0, 2, 0, 0, 0]
        assert game.store == [22, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_22(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 20]
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
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [5, 5, 5, 0, 4, 4, 4, 4, 4, 4, 4, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [5, 5, 5, 0, 4, 4, 5, 5, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_3(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [5, 5, 0, 1, 5, 5, 6, 6, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_4(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [6, 6, 1, 2, 6, 6, 0, 6, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_5(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [6, 6, 0, 3, 6, 6, 0, 6, 5, 0, 5, 0]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_6(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [7, 7, 0, 3, 6, 6, 0, 0, 6, 1, 6, 1]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_7(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [8, 8, 1, 4, 0, 6, 0, 0, 6, 1, 7, 2]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [8, 8, 0, 4, 0, 6, 0, 0, 6, 2, 8, 0]
        assert game.store == [5, 1]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_9(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [8, 0, 1, 5, 1, 7, 1, 1, 7, 3, 8, 0]
        assert game.store == [5, 1]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [9, 1, 2, 6, 1, 1, 2, 1, 7, 3, 0, 1]
        assert game.store == [5, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_11(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [10, 2, 3, 0, 1, 1, 0, 0, 7, 4, 1, 2]
        assert game.store == [8, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_12(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [10, 1, 4, 1, 2, 2, 1, 1, 0, 4, 1, 2]
        assert game.store == [8, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_13(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 1, 5, 2, 3, 3, 2, 2, 1, 5, 1, 3]
        assert game.store == [9, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_14(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 5, 0, 3, 3, 2, 0, 2, 6, 1, 3]
        assert game.store == [9, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_15(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 0, 6, 1, 4, 0, 2, 0, 2, 6, 1, 3]
        assert game.store == [9, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_16(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 6, 1, 4, 0, 0, 1, 3, 6, 1, 3]
        assert game.store == [9, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_17(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 5, 1, 1, 2, 1, 6, 1, 3]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_18(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 5, 0, 1, 2, 2, 7, 2, 0]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_19(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 0, 0, 1, 2, 2, 7, 2, 1]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_20(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 0, 0, 0, 3, 2, 7, 2, 1]
        assert game.store == [12, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_21(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [0, 1, 2, 0, 0, 0, 0, 3, 0, 0, 0, 1]
        assert game.store == [23, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_22(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
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
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 4, 0, 5, 5, 5, 5, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_3(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 5, 5, 6, 6, 5, 1, 6, 0, 5, 5, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_4(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 5, 0, 7, 7, 6, 2, 7, 0, 5, 5, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_5(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 5, 0, 7, 8, 7, 3, 8, 1, 0, 5, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_6(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 6, 1, 8, 0, 7, 3, 8, 2, 1, 6, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_7(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [2, 7, 1, 9, 1, 8, 4, 0, 2, 1, 6, 6]
        assert game.store == [0, 1]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 7, 1, 9, 1, 8, 4, 0, 2, 0, 7, 7]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 8, 2, 10, 2, 9, 5, 0, 2, 0, 7, 0]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_10(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [2, 9, 0, 10, 2, 9, 5, 0, 2, 0, 7, 0]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_11(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [3, 10, 1, 11, 3, 10, 5, 0, 2, 0, 0, 1]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_12(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [3, 10, 1, 11, 0, 11, 6, 1, 2, 0, 0, 1]
        assert game.store == [1, 1]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_13(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [0, 10, 1, 11, 0, 11, 6, 1, 2, 0, 1, 0]
        assert game.store == [1, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_14(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [1, 11, 2, 12, 1, 0, 7, 2, 3, 1, 2, 1]
        assert game.store == [1, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_15(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 11, 0, 12, 1, 0, 7, 2, 4, 2, 0, 1]
        assert game.store == [1, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_16(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [1, 12, 1, 1, 2, 1, 8, 1, 5, 3, 1, 2]
        assert game.store == [3, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_17(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 1, 9, 0, 5, 3, 1, 2]
        assert game.store == [3, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_18(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [22, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_19(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [22, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_20(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [27, 21]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_8_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_8_move_1(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 0, 5, 5, 5, 5, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_2(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [5, 5, 4, 4, 4, 0, 5, 5, 0, 6, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_3(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [5, 5, 0, 5, 5, 1, 6, 5, 0, 6, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_4(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [6, 5, 0, 5, 5, 1, 6, 0, 1, 7, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_5(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [6, 5, 0, 5, 0, 2, 1, 1, 2, 8, 6, 6]
        assert game.store == [6, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_6(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [6, 5, 0, 5, 0, 1, 0, 1, 2, 8, 6, 6]
        assert game.store == [6, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_7(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [7, 6, 1, 0, 0, 1, 0, 1, 2, 8, 7, 7]
        assert game.store == [6, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [8, 7, 2, 1, 1, 2, 1, 1, 2, 8, 7, 0]
        assert game.store == [6, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_9(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [8, 7, 2, 0, 2, 2, 1, 0, 0, 8, 7, 0]
        assert game.store == [9, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_10(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [8, 7, 2, 0, 2, 0, 0, 1, 0, 8, 7, 0]
        assert game.store == [9, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 7, 2, 0, 3, 1, 1, 2, 1, 9, 8, 1]
        assert game.store == [9, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_12(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [0, 7, 2, 0, 3, 0, 1, 2, 1, 9, 9, 0]
        assert game.store == [9, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_13(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [0, 7, 2, 0, 0, 1, 2, 3, 1, 9, 9, 0]
        assert game.store == [9, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_14(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 7, 2, 0, 1, 2, 3, 0, 1, 9, 9, 0]
        assert game.store == [9, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_15(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 8, 0, 0, 1, 2, 3, 0, 1, 9, 9, 0]
        assert game.store == [9, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_16(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [2, 9, 1, 1, 2, 3, 4, 0, 1, 0, 10, 1]
        assert game.store == [9, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_17(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [2, 9, 0, 2, 2, 3, 4, 0, 0, 0, 10, 1]
        assert game.store == [10, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_18(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [0, 9, 0, 2, 2, 3, 4, 0, 0, 0, 11, 0]
        assert game.store == [10, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_19(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [0, 10, 1, 0, 2, 3, 4, 0, 0, 0, 11, 0]
        assert game.store == [10, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_20(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 10, 2, 1, 3, 4, 0, 0, 0, 0, 11, 0]
        assert game.store == [10, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_21(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 10, 0, 2, 4, 4, 0, 0, 0, 0, 11, 0]
        assert game.store == [10, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_22(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [1, 11, 1, 3, 5, 5, 1, 1, 1, 1, 0, 1]
        assert game.store == [10, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_23(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [2, 0, 2, 4, 6, 6, 2, 2, 2, 1, 1, 1]
        assert game.store == [12, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_24(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 4, 6, 6, 2, 0, 3, 2, 1, 1]
        assert game.store == [12, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_25(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 1, 1, 5, 0, 6, 2, 0, 3, 2, 2, 2]
        assert game.store == [12, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_26(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 5, 0, 6, 0, 1, 4, 2, 2, 2]
        assert game.store == [12, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_27(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 5, 0, 6, 0, 1, 4, 0, 0, 1]
        assert game.store == [18, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_28(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 5, 0, 6, 1, 0, 4, 0, 0, 1]
        assert game.store == [18, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_29(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 1, 7, 2, 1, 5, 0, 0, 1]
        assert game.store == [18, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_30(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 7, 0, 2, 6, 0, 0, 1]
        assert game.store == [18, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_31(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [1, 2, 2, 1, 1, 0, 0, 2, 6, 0, 1, 2]
        assert game.store == [18, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_32(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [1, 0, 2, 1, 1, 0, 0, 2, 6, 1, 0, 2]
        assert game.store == [18, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_33(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 2, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [28, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_34(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_35(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_36(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 1]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_37(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_38(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_39(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_40(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_41(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_42(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_43(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_44(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_45(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_46(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_47(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_48(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_49(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_50(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_51(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_52(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_53(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_54(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [28, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_55(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [31, 17]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_9_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_9_move_1(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 5, 5, 5, 5, 0, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 6, 5, 5, 5, 0, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_3(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 5, 5, 5, 6, 6, 6, 6, 1, 0, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_4(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 0, 5, 5, 6, 6, 6, 6, 2, 1, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_5(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [2, 0, 0, 5, 6, 6, 0, 7, 3, 2, 6, 6]
        assert game.store == [0, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_6(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 5, 6, 6, 0, 7, 3, 2, 6, 6]
        assert game.store == [0, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 2, 6, 7, 7, 0, 7, 3, 2, 6, 0]
        assert game.store == [0, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 2, 2, 6, 7, 7, 0, 7, 3, 2, 6, 1]
        assert game.store == [0, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_9(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [1, 3, 3, 7, 8, 8, 1, 0, 3, 2, 6, 1]
        assert game.store == [0, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_10(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [2, 3, 3, 7, 0, 9, 2, 1, 4, 3, 7, 1]
        assert game.store == [1, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_11(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [0, 3, 3, 7, 0, 9, 0, 2, 5, 3, 7, 1]
        assert game.store == [1, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_12(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [1, 4, 4, 8, 1, 0, 0, 2, 6, 4, 8, 2]
        assert game.store == [1, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [2, 5, 5, 9, 2, 1, 1, 2, 6, 4, 0, 3]
        assert game.store == [1, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_14(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 6, 6, 9, 2, 1, 0, 2, 6, 4, 0, 3]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_15(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [0, 6, 6, 9, 2, 1, 0, 2, 7, 5, 1, 0]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_16(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [1, 6, 6, 0, 3, 2, 1, 3, 8, 6, 2, 1]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_17(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 6, 6, 0, 3, 1, 0, 3, 8, 6, 2, 1]
        assert game.store == [2, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_18(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [0, 7, 7, 1, 0, 1, 0, 3, 8, 6, 2, 1]
        assert game.store == [2, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_19(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 7, 7, 2, 1, 2, 1, 4, 9, 0, 2, 1]
        assert game.store == [2, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_20(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 8, 3, 2, 3, 2, 1, 10, 0, 2, 1]
        assert game.store == [6, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_21(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 0, 8, 3, 0, 3, 2, 1, 11, 1, 0, 1]
        assert game.store == [6, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_22(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 8, 3, 0, 0, 3, 2, 12, 1, 0, 1]
        assert game.store == [6, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_23(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 0, 0, 0, 3, 13, 2, 0, 1]
        assert game.store == [6, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_24(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 3, 13, 2, 0, 1]
        assert game.store == [6, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_25(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 1, 3, 13, 2, 0, 0]
        assert game.store == [6, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_26(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 13, 2, 0, 0]
        assert game.store == [9, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_27(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 1, 13, 2, 0, 0]
        assert game.store == [9, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_28(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [22, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_29(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0]
        assert game.store == [22, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_30(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [24, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_31(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_32(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [27, 21]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_10_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_10_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_2(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 4, 4, 4, 4, 4, 4, 0, 6, 6, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_3(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [0, 4, 4, 4, 0, 5, 5, 1, 7, 6, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_4(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 4, 4, 4, 0, 5, 5, 0, 8, 6, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_5(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 5, 0, 4, 0, 5, 5, 0, 8, 6, 7, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_6(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [2, 6, 1, 5, 0, 5, 5, 0, 8, 0, 8, 8]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_7(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [2, 6, 0, 6, 0, 5, 5, 0, 8, 0, 8, 8]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_8(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [2, 6, 0, 6, 0, 5, 0, 1, 9, 1, 9, 9]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_9(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [3, 7, 1, 7, 1, 0, 0, 1, 9, 1, 9, 9]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_10(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [4, 8, 1, 8, 1, 1, 0, 1, 0, 2, 10, 10]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_11(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [4, 8, 1, 8, 2, 0, 0, 0, 0, 0, 10, 10]
        assert game.store == [3, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_12(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [5, 9, 2, 9, 3, 1, 1, 1, 1, 0, 0, 11]
        assert game.store == [3, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [6, 0, 2, 9, 4, 2, 1, 2, 2, 1, 1, 12]
        assert game.store == [4, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_14(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [6, 0, 0, 9, 4, 1, 2, 0, 2, 1, 1, 12]
        assert game.store == [4, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_15(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [6, 0, 0, 9, 4, 0, 1, 0, 2, 1, 1, 12]
        assert game.store == [6, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_16(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [6, 0, 0, 9, 4, 0, 2, 1, 0, 1, 1, 12]
        assert game.store == [6, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_17(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [7, 1, 1, 0, 4, 0, 3, 2, 1, 2, 2, 13]
        assert game.store == [6, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_18(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [7, 1, 1, 0, 4, 0, 0, 3, 2, 3, 2, 13]
        assert game.store == [6, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_19(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [8, 2, 2, 1, 0, 0, 0, 3, 2, 0, 0, 13]
        assert game.store == [11, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_20(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [10, 3, 3, 2, 1, 1, 1, 4, 3, 1, 1, 1]
        assert game.store == [11, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_21(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [10, 3, 3, 2, 0, 2, 0, 0, 3, 1, 1, 1]
        assert game.store == [16, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_22(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 3, 1, 1, 0, 1, 1, 1]
        assert game.store == [16, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_23(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 3, 1, 1, 0, 1, 1, 1]
        assert game.store == [16, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_24(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1]
        assert game.store == [16, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_25(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1]
        assert game.store == [16, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_26(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0]
        assert game.store == [16, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_27(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1]
        assert game.store == [16, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_28(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [16, 32]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_11_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_11_move_1(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_2(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [5, 0, 6, 5, 5, 5, 5, 4, 4, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [5, 0, 6, 5, 5, 5, 6, 5, 5, 5, 1, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_4(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [5, 0, 6, 0, 6, 6, 7, 6, 6, 5, 1, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_5(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [6, 1, 6, 0, 6, 6, 7, 0, 7, 6, 2, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_6(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [7, 2, 7, 1, 7, 0, 7, 0, 7, 6, 0, 2]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_7(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [8, 3, 8, 2, 7, 0, 7, 0, 7, 0, 1, 3]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_8(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [8, 3, 8, 0, 8, 1, 7, 0, 7, 0, 1, 3]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_9(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [9, 1, 9, 1, 8, 1, 7, 0, 0, 1, 2, 4]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_10(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [10, 2, 10, 2, 0, 1, 0, 0, 1, 2, 1, 5]
        assert game.store == [11, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [10, 0, 10, 0, 0, 1, 1, 1, 2, 3, 2, 0]
        assert game.store == [11, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_12(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 11, 1, 1, 2, 1, 2, 3, 4, 3, 0]
        assert game.store == [12, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_13(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 11, 1, 1, 0, 1, 2, 3, 0, 4, 1]
        assert game.store == [12, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_14(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 12, 2, 1, 0, 1, 0, 0, 0, 4, 0]
        assert game.store == [18, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_15(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [1, 0, 12, 2, 1, 0, 2, 1, 1, 1, 0, 0]
        assert game.store == [18, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_16(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 12, 2, 1, 0, 2, 0, 1, 1, 0, 0]
        assert game.store == [19, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_17(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 2, 0, 0, 2, 0, 0]
        assert game.store == [19, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_18(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 2, 0, 0, 2, 0, 0]
        assert game.store == [19, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_19(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 2, 1, 0, 0, 0, 2, 0, 0]
        assert game.store == [19, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_20(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [25, 23]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_12_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_12_move_1(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 0, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 0, 4, 4, 5, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_3(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [5, 5, 0, 6, 1, 5, 5, 6, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_4(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [5, 5, 0, 6, 2, 6, 6, 7, 6, 0, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 6, 1, 7, 3, 7, 6, 7, 6, 0, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_6(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [1, 7, 2, 7, 3, 7, 6, 0, 7, 1, 6, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_7(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 8, 3, 8, 0, 7, 6, 0, 7, 1, 6, 0]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [2, 9, 1, 9, 1, 7, 6, 0, 7, 1, 0, 1]
        assert game.store == [1, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_9(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [2, 9, 1, 10, 0, 7, 6, 0, 7, 0, 0, 1]
        assert game.store == [2, 3]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_10(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [0, 9, 1, 10, 0, 7, 6, 0, 7, 0, 1, 0]
        assert game.store == [2, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_11(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [1, 10, 2, 11, 1, 0, 6, 0, 7, 0, 2, 1]
        assert game.store == [2, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_12(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 10, 2, 11, 1, 0, 6, 0, 8, 1, 0, 1]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 3, 12, 2, 1, 7, 1, 9, 2, 1, 2]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_14(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 4, 13, 1, 2, 7, 1, 0, 3, 2, 3]
        assert game.store == [2, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_15(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 14, 2, 3, 8, 0, 0, 3, 0, 0]
        assert game.store == [8, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_16(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 0, 14, 2, 3, 8, 0, 0, 0, 1, 1]
        assert game.store == [8, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_17(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [2, 1, 1, 15, 3, 0, 8, 0, 0, 0, 0, 1]
        assert game.store == [9, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_18(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 2, 15, 3, 0, 0, 1, 1, 1, 1, 2]
        assert game.store == [9, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_19(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 3, 2, 15, 3, 0, 0, 1, 1, 1, 1, 0]
        assert game.store == [11, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_20(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [11, 37]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is True
        gstate.cond = cond

    def test_round_13_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_13_move_1(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 5, 5, 5, 5, 0, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [0, 5, 5, 5, 5, 5, 5, 6, 6, 1, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_4(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 0, 6, 7, 7, 2, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_5(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [0, 5, 5, 5, 5, 0, 6, 7, 7, 0, 7, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_6(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [0, 5, 5, 0, 6, 1, 7, 8, 8, 0, 7, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_7(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [1, 6, 6, 1, 7, 2, 8, 9, 0, 0, 7, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 7, 2, 8, 3, 9, 10, 0, 0, 7, 0]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_9(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [2, 1, 8, 3, 9, 4, 0, 10, 0, 1, 8, 1]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_10(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 8, 3, 9, 0, 1, 11, 1, 2, 0, 1]
        assert game.store == [9, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_11(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 1, 8, 0, 9, 0, 1, 12, 0, 2, 0, 1]
        assert game.store == [9, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_12(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 2, 9, 1, 0, 0, 1, 13, 1, 3, 1, 2]
        assert game.store == [9, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_13(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [2, 0, 9, 0, 0, 0, 1, 13, 1, 0, 2, 3]
        assert game.store == [9, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_14(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 1, 1, 2, 14, 2, 1, 3, 4]
        assert game.store == [9, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_15(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [2, 0, 0, 1, 1, 1, 2, 14, 2, 0, 4, 4]
        assert game.store == [9, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_16(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 5, 5]
        assert game.store == [27, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_17(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [27, 21]
        assert cond.name == "ROUND_WIN"
        assert game.mdata.winner is False
        gstate.cond = cond

    def test_round_14_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_14_move_1(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [5, 0, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [5, 0, 4, 4, 4, 4, 5, 5, 5, 6, 6, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 4, 4, 4, 4, 5, 6, 6, 7, 7, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_4(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 0, 5, 5, 5, 5, 6, 7, 7, 0, 7, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_5(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 5, 5, 5, 6, 7, 7, 1, 8, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_6(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [2, 2, 1, 6, 6, 6, 0, 7, 7, 1, 8, 2]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_7(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [2, 0, 2, 7, 6, 6, 0, 7, 7, 0, 8, 2]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [3, 1, 3, 8, 7, 7, 1, 7, 7, 0, 0, 3]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_9(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [3, 1, 3, 0, 8, 8, 2, 8, 8, 1, 1, 4]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_10(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [3, 0, 0, 0, 8, 8, 2, 9, 9, 2, 2, 0]
        assert game.store == [1, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 1, 8, 8, 2, 9, 9, 2, 2, 0]
        assert game.store == [1, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_12(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [1, 2, 2, 2, 9, 8, 2, 0, 10, 3, 3, 1]
        assert game.store == [1, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_13(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [1, 2, 0, 3, 10, 8, 2, 0, 10, 3, 3, 0]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_14(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [1, 2, 0, 3, 10, 8, 2, 1, 11, 4, 0, 0]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_15(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [2, 3, 0, 3, 10, 0, 3, 2, 12, 5, 1, 1]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_16(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 10, 0, 3, 0, 13, 6, 1, 1]
        assert game.store == [2, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_17(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 1, 1, 4, 0, 0, 4, 1, 14, 7, 2, 2]
        assert game.store == [2, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_18(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [2, 2, 2, 5, 1, 1, 5, 2, 1, 9, 4, 3]
        assert game.store == [2, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_19(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [2, 2, 2, 5, 0, 2, 0, 0, 1, 9, 4, 3]
        assert game.store == [9, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_20(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [3, 3, 3, 1, 1, 3, 1, 0, 1, 0, 5, 4]
        assert game.store == [9, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_21(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [4, 4, 0, 1, 1, 3, 1, 0, 0, 0, 5, 5]
        assert game.store == [10, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_22(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [5, 5, 1, 2, 1, 0, 1, 0, 0, 0, 0, 6]
        assert game.store == [10, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_23(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [5, 5, 1, 2, 0, 1, 1, 0, 0, 0, 0, 6]
        assert game.store == [10, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_24(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [5, 5, 1, 2, 0, 1, 2, 1, 1, 1, 1, 0]
        assert game.store == [10, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_25(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 5, 1, 2, 0, 1, 0, 2, 2, 1, 2, 1]
        assert game.store == [13, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_26(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 5, 0, 2, 0, 2, 1, 0, 2, 1, 2, 1]
        assert game.store == [13, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_27(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 3, 1, 3, 2, 0, 2, 1, 2, 1]
        assert game.store == [13, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_28(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 3, 2, 4, 0, 0, 2, 1, 2, 1]
        assert game.store == [13, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_29(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 1, 1, 4, 3, 0, 0, 0, 2, 1, 2, 1]
        assert game.store == [13, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_30(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 4, 3, 0, 0, 0, 2, 1, 3, 0]
        assert game.store == [13, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_31(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 4, 0, 1, 1, 1, 2, 1, 0, 0]
        assert game.store == [16, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_32(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 4, 0, 0, 2, 0, 2, 1, 0, 0]
        assert game.store == [16, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_33(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 1, 3, 1, 2, 1, 0, 0]
        assert game.store == [16, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_34(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 4, 2, 0, 1, 0, 0]
        assert game.store == [16, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_35(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 2, 0, 1, 0, 0]
        assert game.store == [20, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_36(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 2, 1, 0, 0, 0]
        assert game.store == [20, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_37(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [22, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_38(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [22, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_39(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [22, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_40(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [22, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_41(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [22, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_42(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [22, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_43(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [25, 23]
        assert cond.name == "WIN"
        assert game.mdata.winner is False
        gstate.cond = cond
