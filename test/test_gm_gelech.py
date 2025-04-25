# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 13:25:08 2025
@author: Ann"""


import pytest
pytestmark = pytest.mark.integtest

from context import game_interface as gi
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
        game.turn = False
        game.starter = False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [4, 5, 5, 5, 5, 0, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [4, 5, 5, 5, 5, 0, 4, 5, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [5, 6, 0, 5, 5, 0, 4, 5, 5, 6, 6, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 6, 0, 6, 6, 1, 5, 6, 0, 6, 6, 1]
        assert game.store == [0, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [0, 6, 0, 0, 7, 2, 1, 7, 1, 7, 6, 1]
        assert game.store == [5, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 6, 0, 0, 8, 1, 2, 8, 2, 8, 0, 1]
        assert game.store == [5, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 9, 2, 1, 9, 2, 8, 0, 1]
        assert game.store == [7, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 2, 2, 10, 0, 1, 0, 3, 9, 1, 2]
        assert game.store == [7, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [2, 2, 3, 2, 0, 1, 2, 1, 4, 10, 1, 1]
        assert game.store == [10, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 4, 3, 1, 2, 3, 2, 4, 0, 2, 2]
        assert game.store == [10, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [2, 2, 0, 3, 1, 2, 3, 0, 4, 0, 1, 1]
        assert game.store == [16, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 3, 1, 2, 3, 0, 0, 1, 2, 2]
        assert game.store == [16, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 2, 3, 4, 0, 0, 1, 2, 0]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 2, 3, 4, 0, 1, 0, 2, 0]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 3, 4, 0, 1, 0, 2, 0]
        assert game.store == [18, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [2, 0, 1, 0, 0, 3, 4, 0, 1, 0, 0, 1]
        assert game.store == [18, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [2, 0, 2, 1, 1, 0, 4, 0, 1, 0, 0, 1]
        assert game.store == [18, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.mdata.winner is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [18, 30]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [6, 6, 6, 0, 4, 4, 4, 4, 4, 4, 0, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [6, 6, 7, 1, 5, 5, 0, 4, 4, 4, 0, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [6, 6, 7, 1, 5, 0, 1, 5, 1, 5, 1, 6]
        assert game.store == [4, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [7, 0, 7, 0, 5, 0, 1, 0, 2, 6, 2, 7]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [7, 0, 0, 1, 6, 1, 2, 1, 3, 7, 2, 7]
        assert game.store == [4, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [8, 1, 1, 2, 1, 2, 3, 1, 3, 7, 2, 0]
        assert game.store == [4, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [8, 1, 1, 0, 2, 3, 3, 0, 3, 0, 0, 0]
        assert game.store == [14, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [8, 1, 1, 0, 2, 3, 0, 1, 4, 1, 0, 0]
        assert game.store == [14, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [8, 1, 1, 0, 2, 0, 1, 2, 5, 0, 0, 0]
        assert game.store == [15, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [8, 1, 1, 1, 3, 1, 2, 3, 0, 0, 0, 0]
        assert game.store == [15, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [9, 0, 1, 1, 3, 1, 0, 3, 0, 0, 0, 0]
        assert game.store == [17, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [9, 0, 1, 1, 3, 1, 0, 0, 1, 1, 1, 0]
        assert game.store == [17, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_14(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.mdata.winner is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [35, 13]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_3_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_3_move_1(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [5, 5, 0, 4, 4, 4, 4, 4, 4, 4, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_2(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [5, 5, 0, 4, 5, 5, 5, 5, 0, 4, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_3(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [5, 5, 0, 4, 0, 6, 6, 6, 1, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_4(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [6, 5, 0, 0, 0, 6, 0, 7, 2, 6, 6, 6]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 6, 1, 1, 1, 7, 1, 7, 2, 6, 6, 6]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_6(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [1, 7, 2, 2, 2, 0, 1, 7, 2, 6, 0, 7]
        assert game.store == [0, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_7(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [1, 7, 2, 2, 0, 1, 2, 7, 2, 6, 0, 0]
        assert game.store == [7, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_8(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [2, 8, 3, 2, 0, 1, 2, 0, 3, 7, 1, 1]
        assert game.store == [7, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_9(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [3, 9, 0, 2, 0, 1, 0, 0, 3, 7, 1, 2]
        assert game.store == [9, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_10(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [4, 1, 1, 3, 1, 1, 0, 0, 3, 0, 2, 3]
        assert game.store == [9, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_11(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [4, 1, 0, 4, 1, 1, 0, 0, 3, 0, 0, 3]
        assert game.store == [11, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_12(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [4, 1, 0, 4, 1, 1, 0, 0, 0, 1, 1, 4]
        assert game.store == [11, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_13(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 1, 5, 2, 1, 0, 0, 0, 1, 0, 4]
        assert game.store == [12, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_14(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [0, 2, 0, 5, 2, 1, 0, 1, 1, 2, 1, 0]
        assert game.store == [12, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_15(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 0, 5, 2, 0, 1, 1, 1, 2, 1, 0]
        assert game.store == [12, 21]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_16(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.mdata.winner is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [12, 36]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_4_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_4_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_2(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [4, 5, 5, 5, 5, 0, 4, 5, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_3(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [4, 5, 6, 6, 6, 1, 0, 5, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_4(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [5, 6, 7, 0, 6, 1, 0, 5, 5, 6, 6, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_5(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 6, 8, 1, 7, 2, 1, 0, 5, 6, 6, 1]
        assert game.store == [0, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_6(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 0, 8, 1, 7, 2, 1, 1, 1, 7, 7, 2]
        assert game.store == [5, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_7(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 9, 1, 1, 0, 1, 1, 1, 0, 8, 3]
        assert game.store == [5, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 10, 1, 1, 0, 1, 0, 0, 0, 0, 3]
        assert game.store == [15, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 3, 11, 1, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [15, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_10(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.mdata.winner is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [33, 15]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_5_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_5_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 6, 6, 6, 5, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_3(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [2, 0, 6, 6, 5, 4, 4, 5, 5, 5, 5, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_4(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 7, 6, 5, 4, 4, 5, 5, 0, 6, 2]
        assert game.store == [0, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_5(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [2, 2, 8, 7, 0, 4, 4, 5, 5, 0, 0, 1]
        assert game.store == [8, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_6(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 2, 9, 8, 1, 5, 5, 0, 5, 0, 0, 1]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_7(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [1, 3, 10, 0, 1, 5, 5, 1, 6, 1, 1, 2]
        assert game.store == [8, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_8(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 1, 6, 0, 1, 6, 1, 1, 2]
        assert game.store == [8, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_9(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [19, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_10(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [3, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [19, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_11(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.mdata.winner is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 18]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_6_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_6_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_2(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [5, 5, 0, 4, 4, 4, 4, 5, 5, 5, 6, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_3(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 5, 1, 5, 5, 5, 0, 5, 5, 5, 6, 1]
        assert game.store == [0, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_4(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 6, 2, 6, 0, 5, 0, 5, 5, 0, 6, 2]
        assert game.store == [5, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [2, 7, 3, 7, 1, 5, 0, 5, 5, 0, 0, 3]
        assert game.store == [5, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_6(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [3, 8, 0, 7, 1, 5, 0, 0, 5, 0, 0, 4]
        assert game.store == [10, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [3, 8, 0, 7, 1, 5, 0, 1, 6, 1, 1, 0]
        assert game.store == [10, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 9, 1, 8, 1, 5, 0, 0, 6, 1, 1, 0]
        assert game.store == [11, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_9(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 9, 2, 6, 1, 1, 0, 1, 1, 0]
        assert game.store == [11, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_10(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 3, 7, 2, 2, 1, 1, 2, 1]
        assert game.store == [12, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_11(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 3, 7, 2, 2, 2, 2, 0, 1]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_12(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 8, 3, 3, 2, 2, 0, 1]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_13(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 8, 3, 3, 0, 3, 1, 1]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_14(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 1, 0, 3, 3, 0, 4, 2, 2]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_15(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 2, 2, 1, 0, 3, 0, 4, 2, 2]
        assert game.store == [12, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_16(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 1, 2, 3, 0, 1, 0, 3, 0, 0, 0, 0]
        assert game.store == [20, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_17(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [1, 1, 2, 3, 1, 2, 1, 0, 0, 0, 0, 0]
        assert game.store == [20, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_18(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 2, 0, 2, 3, 2, 0, 0, 0, 0, 0]
        assert game.store == [20, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_19(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 1, 2, 0, 3, 4, 0, 0, 0, 0, 0, 0]
        assert game.store == [20, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_20(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.mdata.winner is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [31, 17]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_7_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_7_move_1(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [4, 0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_2(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [4, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 5, 5, 5, 5, 5, 5, 6, 6, 1, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_4(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 0, 6, 6, 6, 6, 6, 6, 0, 6, 1, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_5(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 6, 0, 7, 7, 7, 7, 1, 7, 1, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_6(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [1, 1, 7, 1, 8, 8, 8, 0, 1, 7, 1, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_7(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [2, 2, 8, 2, 9, 0, 8, 0, 0, 8, 1, 1]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_8(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 1, 9, 3, 10, 1, 0, 0, 0, 8, 2, 2]
        assert game.store == [7, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_9(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 9, 3, 10, 0, 1, 0, 0, 8, 0, 0]
        assert game.store == [11, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_10(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [2, 2, 10, 4, 11, 1, 1, 0, 0, 0, 1, 1]
        assert game.store == [11, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_11(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [3, 3, 11, 5, 0, 2, 1, 1, 1, 1, 2, 2]
        assert game.store == [12, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_12(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [4, 3, 0, 0, 0, 0, 1, 1, 1, 1, 0, 3]
        assert game.store == [12, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [4, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 3]
        assert game.store == [12, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_14(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [5, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0]
        assert game.store == [12, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_15(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [5, 0, 2, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [13, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_16(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [5, 0, 2, 0, 0, 0, 1, 1, 0, 1, 0, 0]
        assert game.store == [13, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_17(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 3, 1, 1, 1, 1, 1, 0, 1, 0, 0]
        assert game.store == [13, 25]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_18(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 1, 3, 1, 0, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [13, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_19(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 0, 3, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [14, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_20(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [1, 0, 3, 1, 0, 0, 2, 0, 0, 0, 0, 0]
        assert game.store == [14, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_21(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [1, 0, 4, 0, 0, 0, 2, 0, 0, 0, 0, 0]
        assert game.store == [14, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_22(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 0, 4, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [14, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_23(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 4, 0, 1, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [14, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_24(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 0, 4, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [14, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_25(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0]
        assert game.store == [14, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_26(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 2, 2, 0, 1, 0, 0, 0, 0]
        assert game.store == [14, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_27(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 3, 2, 0, 1, 0, 0, 0, 0]
        assert game.store == [14, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_28(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 3, 2, 0, 0, 1, 0, 0, 0]
        assert game.store == [14, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_29(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 3, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [14, 27]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_30(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_31(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_32(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_33(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0]
        assert game.store == [14, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_34(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.mdata.winner is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [14, 34]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_8_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_8_move_1(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_2(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [5, 5, 0, 4, 4, 4, 0, 5, 5, 5, 6, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [5, 5, 0, 4, 4, 4, 1, 6, 6, 6, 7, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_4(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [5, 5, 0, 0, 5, 5, 2, 7, 6, 6, 7, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [6, 6, 1, 1, 6, 6, 2, 7, 6, 6, 0, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_6(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [7, 7, 2, 2, 7, 0, 2, 7, 0, 0, 0, 2]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_7(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [8, 8, 3, 2, 7, 0, 2, 0, 1, 1, 1, 3]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_8(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [8, 8, 3, 2, 0, 1, 3, 1, 2, 2, 2, 4]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_9(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [8, 8, 3, 2, 0, 1, 3, 2, 3, 0, 2, 4]
        assert game.store == [12, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_10(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 9, 4, 3, 1, 2, 1, 3, 4, 0, 2, 4]
        assert game.store == [15, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_11(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 9, 4, 3, 1, 0, 1, 3, 0, 1, 3, 5]
        assert game.store == [15, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_12(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [2, 10, 5, 0, 1, 0, 1, 0, 0, 1, 3, 0]
        assert game.store == [23, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_13(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [2, 10, 0, 0, 1, 1, 0, 0, 0, 1, 3, 0]
        assert game.store == [23, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_14(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [2, 10, 0, 0, 1, 0, 1, 0, 0, 1, 3, 0]
        assert game.store == [23, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_15(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [2, 10, 0, 0, 1, 0, 1, 0, 0, 0, 4, 0]
        assert game.store == [23, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_16(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [2, 0, 1, 1, 2, 1, 2, 1, 1, 1, 5, 1]
        assert game.store == [23, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_17(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 0, 2]
        assert game.store == [23, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_18(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [2, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [29, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_19(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [2, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [29, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_8_move_20(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.mdata.winner is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [35, 13]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_9_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_9_move_1(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [4, 4, 4, 0, 5, 5, 5, 5, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_2(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [4, 5, 5, 1, 6, 6, 0, 5, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_3(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [5, 6, 6, 2, 0, 6, 0, 5, 0, 4, 5, 5]
        assert game.store == [4, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [5, 6, 6, 2, 0, 6, 1, 6, 1, 5, 6, 0]
        assert game.store == [4, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [6, 0, 6, 2, 0, 6, 1, 7, 2, 6, 7, 1]
        assert game.store == [4, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_6(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 7, 3, 0, 0, 1, 7, 2, 0, 8, 2]
        assert game.store == [4, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_7(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [2, 2, 8, 0, 0, 0, 1, 7, 2, 0, 0, 0]
        assert game.store == [14, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_9_move_8(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.mdata.winner is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [14, 34]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_10_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_10_move_1(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 5, 5, 5, 5, 0, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_2(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [5, 0, 4, 4, 5, 5, 5, 5, 0, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_3(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [5, 0, 4, 4, 5, 5, 0, 6, 1, 6, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 5, 5, 6, 6, 0, 6, 1, 6, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_5(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 2, 6, 1, 7, 7, 1, 0, 1, 6, 6, 6]
        assert game.store == [0, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_6(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 3, 0, 1, 7, 7, 1, 0, 1, 7, 7, 7]
        assert game.store == [1, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_7(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [1, 3, 0, 1, 8, 1, 2, 1, 2, 8, 0, 7]
        assert game.store == [1, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 8, 1, 0, 1, 0, 8, 1, 1]
        assert game.store == [12, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_9(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 1, 0, 8, 0, 2]
        assert game.store == [12, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_10(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 1, 0, 8, 0, 2]
        assert game.store == [12, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 9, 1, 0]
        assert game.store == [12, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_12(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 9, 1, 0]
        assert game.store == [12, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 9, 0, 1]
        assert game.store == [12, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_14(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 9, 0, 1]
        assert game.store == [12, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_10_move_15(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.mdata.winner is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [12, 36]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_11_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_11_move_1(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [5, 5, 5, 5, 0, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_2(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [5, 5, 5, 5, 0, 4, 0, 5, 5, 5, 5, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_3(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [6, 6, 6, 0, 0, 4, 0, 5, 5, 5, 6, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_4(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [7, 7, 7, 0, 0, 4, 0, 5, 5, 0, 7, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [8, 0, 7, 0, 0, 4, 1, 6, 6, 1, 8, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_6(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [9, 1, 0, 0, 0, 0, 1, 0, 7, 2, 9, 8]
        assert game.store == [0, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 1, 2, 1, 8, 3, 1, 9]
        assert game.store == [9, 11]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_8(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 3, 2, 9, 0, 1, 9]
        assert game.store == [9, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_9(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 3, 2, 0, 0, 1, 9]
        assert game.store == [18, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 3, 2, 0, 1, 0, 9]
        assert game.store == [18, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_11(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 0, 3, 0, 0, 1, 0, 9]
        assert game.store == [20, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_11_move_12(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.mdata.winner is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [20, 28]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_12_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_12_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_2(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 0, 5, 5, 6, 6, 5, 5, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_3(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [5, 5, 4, 4, 0, 5, 5, 0, 7, 6, 6, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_4(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [6, 6, 5, 5, 1, 0, 5, 0, 7, 6, 6, 1]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_5(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 7, 6, 6, 1, 0, 5, 0, 7, 0, 7, 2]
        assert game.store == [0, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_6(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 7, 6, 7, 0, 0, 5, 0, 7, 0, 7, 0]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_7(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [2, 8, 7, 8, 0, 0, 5, 0, 0, 1, 8, 1]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_8(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [3, 9, 8, 0, 0, 0, 5, 1, 1, 2, 9, 2]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_9(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [3, 9, 8, 0, 0, 0, 6, 0, 1, 2, 9, 2]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [3, 0, 9, 1, 1, 1, 7, 1, 2, 3, 10, 2]
        assert game.store == [2, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [4, 1, 9, 1, 0, 1, 7, 1, 2, 3, 10, 0]
        assert game.store == [2, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_12(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [4, 1, 0, 2, 1, 2, 1, 2, 1, 4, 1, 1]
        assert game.store == [21, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_13(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 0, 1, 2, 1, 0, 2, 2]
        assert game.store == [21, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_14(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 1, 0, 0, 1, 2, 1, 0, 0, 0]
        assert game.store == [25, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_15(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 2, 0, 1, 0, 0, 0]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_16(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [27, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_17(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        assert game.store == [27, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_18(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        assert game.store == [27, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_19(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
        assert game.store == [27, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_20(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [27, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_21(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1]
        assert game.store == [27, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_22(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        assert game.store == [27, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_23(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1]
        assert game.store == [27, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_24(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1]
        assert game.store == [27, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_25(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [27, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_26(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0]
        assert game.store == [27, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_27(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [27, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_12_move_28(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.mdata.winner is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 18]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_13_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_13_move_1(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [5, 5, 0, 4, 4, 4, 4, 4, 4, 4, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_2(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [5, 5, 0, 5, 5, 5, 5, 0, 4, 4, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 6, 1, 6, 6, 6, 5, 0, 4, 4, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_4(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [1, 7, 2, 7, 6, 6, 5, 0, 4, 4, 0, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_5(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [2, 8, 3, 0, 6, 6, 5, 0, 5, 5, 1, 1]
        assert game.store == [6, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_6(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 0, 3, 0, 7, 7, 6, 1, 6, 0, 1, 1]
        assert game.store == [6, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_7(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 3, 0, 7, 0, 7, 2, 7, 1, 2, 2]
        assert game.store == [6, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_8(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 1, 1, 7, 0, 7, 2, 0, 2, 3, 3]
        assert game.store == [6, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 2, 2, 1, 7, 0, 7, 2, 0, 0, 0, 3]
        assert game.store == [11, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_10(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [1, 3, 2, 1, 7, 0, 0, 3, 1, 1, 1, 4]
        assert game.store == [11, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_11(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [1, 3, 2, 1, 0, 1, 1, 4, 1, 2, 2, 1]
        assert game.store == [16, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_12(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 3, 2, 0, 0, 0, 1, 5, 2, 0, 2, 1]
        assert game.store == [16, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 0, 2, 0, 0, 0, 1, 5, 2, 0, 3, 2]
        assert game.store == [16, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_14(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [2, 0, 2, 0, 0, 0, 1, 0, 3, 1, 4, 3]
        assert game.store == [16, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_15(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 0, 3, 1, 5, 4]
        assert game.store == [16, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_13_move_16(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.mdata.winner is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [16, 32]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_14_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_14_move_1(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_2(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 0, 5, 5, 1, 6, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_3(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [4, 5, 5, 5, 1, 6, 0, 1, 6, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_4(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [5, 6, 0, 5, 1, 6, 0, 0, 6, 6, 6, 6]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [6, 7, 1, 6, 2, 7, 0, 0, 6, 6, 6, 0]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_6(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 8, 2, 7, 3, 8, 1, 0, 6, 0, 6, 0]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_7(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 8, 3, 8, 4, 1, 2, 1, 0, 0, 6, 0]
        assert game.store == [7, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_8(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 8, 0, 9, 5, 2, 0, 1, 0, 0, 6, 0]
        assert game.store == [9, 8]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_9(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 8, 0, 9, 1, 3, 1, 2, 1, 1, 0, 0]
        assert game.store == [9, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 10, 2, 4, 2, 1, 2, 2, 0, 0]
        assert game.store == [11, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_11(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 10, 0, 4, 0, 2, 3, 2, 0, 0]
        assert game.store == [11, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_12(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 1, 0, 1, 5, 1, 3, 4, 1, 1, 1]
        assert game.store == [13, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_13(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 1, 2, 4, 0, 1, 1, 1]
        assert game.store == [13, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_14(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 1, 0, 4, 0, 1, 1, 1]
        assert game.store == [15, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_15(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 1, 0, 4, 0, 1, 1, 0]
        assert game.store == [15, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_16(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 4, 0, 1, 1, 0]
        assert game.store == [15, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_17(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 1, 0, 4, 1, 0, 1, 0]
        assert game.store == [15, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_18(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 1, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_19(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 0]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_20(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1, 1]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_21(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 1, 1]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_22(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1]
        assert game.store == [19, 24]
        assert cond is None
        gstate.cond = cond

    def test_round_14_move_23(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.mdata.winner is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [19, 29]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_15_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_15_move_1(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 0, 5, 5, 5, 5, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_2(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [5, 4, 4, 4, 4, 0, 5, 0, 6, 6, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_3(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [5, 4, 4, 0, 5, 1, 6, 1, 6, 6, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_4(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [6, 5, 5, 1, 1, 1, 6, 1, 6, 6, 5, 0]
        assert game.store == [0, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [7, 0, 5, 1, 1, 1, 0, 0, 1, 7, 6, 1]
        assert game.store == [13, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_6(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 0, 5, 0, 2, 2, 1, 1, 2, 8, 0, 1]
        assert game.store == [13, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_7(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 2, 2, 1, 1, 2, 9, 1, 2]
        assert game.store == [13, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_8(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 1, 1, 1, 1, 2, 1, 2, 0, 2, 3]
        assert game.store == [13, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_9(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 0, 2, 1, 1, 0, 0, 0, 0, 0, 3]
        assert game.store == [20, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_10(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [3, 2, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [20, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_15_move_11(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.mdata.winner is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 18]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_16_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_16_move_1(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 4, 4, 4, 4, 4, 4, 0, 6, 6, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_3(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 4, 4, 5, 5, 5, 5, 1, 7, 0, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_4(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 5, 6, 6, 6, 5, 1, 7, 0, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_5(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 5, 6, 0, 6, 0, 2, 8, 1, 7, 7]
        assert game.store == [0, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_6(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 5, 0, 1, 7, 1, 3, 9, 2, 7, 7]
        assert game.store == [0, 6]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_7(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 5, 0, 1, 0, 1, 3, 9, 0, 8, 8]
        assert game.store == [0, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_8(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 2, 1, 2, 1, 9, 0, 8, 8]
        assert game.store == [3, 13]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_9(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 2, 1, 2, 3, 1, 9, 0, 0, 9]
        assert game.store == [3, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_10(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 1, 2, 1, 0, 4, 1, 9, 0, 0, 0]
        assert game.store == [13, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_11(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 1, 2, 3, 1, 1, 0, 1, 9, 0, 0, 0]
        assert game.store == [13, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_12(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 4, 2, 1, 0, 0, 9, 0, 0, 0]
        assert game.store == [14, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_13(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [2, 2, 1, 5, 3, 2, 0, 0, 0, 1, 1, 1]
        assert game.store == [14, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_14(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is True
        assert game.board == [2, 2, 1, 5, 3, 0, 1, 1, 0, 0, 1, 1]
        assert game.store == [15, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_15(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 5, 0, 1, 0, 1, 0, 0, 1, 1]
        assert game.store == [15, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_16(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [1, 1, 2, 0, 0, 1, 0, 1, 0, 0, 2, 2]
        assert game.store == [15, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_17(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 2, 0, 0, 1, 0, 0, 1, 0, 2, 2]
        assert game.store == [15, 23]
        assert cond is None
        gstate.cond = cond

    def test_round_16_move_18(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.mdata.winner is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [25, 23]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_17_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_17_move_1(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 0, 5, 5, 5, 5, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_2(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [5, 5, 5, 4, 0, 5, 5, 5, 5, 4, 0, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_3(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [6, 0, 5, 4, 0, 5, 5, 5, 6, 5, 1, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_4(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [6, 0, 5, 4, 0, 5, 5, 5, 6, 6, 0, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_5(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [7, 1, 0, 4, 0, 5, 5, 5, 6, 7, 1, 7]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_6(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [7, 0, 1, 5, 1, 6, 6, 6, 7, 0, 1, 7]
        assert game.store == [0, 1]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_7(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [8, 1, 2, 6, 2, 0, 6, 0, 7, 0, 1, 8]
        assert game.store == [6, 1]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_8(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [8, 1, 3, 7, 3, 1, 7, 1, 0, 0, 1, 8]
        assert game.store == [6, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 1, 3, 7, 4, 2, 1, 2, 1, 1, 1, 9]
        assert game.store == [14, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_10(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 4, 0, 1, 0, 2, 2, 1, 9]
        assert game.store == [14, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_11(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [1, 1, 1, 1, 0, 0, 1, 0, 2, 2, 1, 9]
        assert game.store == [14, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_12(self, gstate):
        game = gstate.game
        cond = game.move((5, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 1, 2, 2, 1, 9]
        assert game.store == [14, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_13(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [1, 1, 0, 1, 0, 0, 0, 1, 0, 2, 1, 0]
        assert game.store == [25, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_14(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 2, 1, 0, 1, 0]
        assert game.store == [25, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_15(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 1, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_16(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 2, 0, 1, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_17(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 2, 0, 1, 0, 1]
        assert game.store == [26, 17]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_18(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_19(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_20(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_21(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_22(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_23(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_24(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_25(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_26(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_27(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_28(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_29(self, gstate):
        game = gstate.game
        cond = game.move((0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_30(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_31(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_32(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_33(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_34(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 0, 0]
        assert game.store == [26, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_17_move_35(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.mdata.winner is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 18]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_18_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_18_move_1(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 0, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_2(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [4, 4, 4, 0, 5, 5, 5, 1, 5, 5, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_3(self, gstate):
        game = gstate.game
        cond = game.move((3, CW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 1, 1, 6, 6, 2, 0, 5, 5, 5]
        assert game.store == [0, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_4(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is True
        assert game.board == [5, 5, 5, 2, 2, 0, 6, 0, 0, 5, 5, 6]
        assert game.store == [2, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [6, 6, 6, 3, 3, 1, 6, 0, 0, 5, 5, 0]
        assert game.store == [2, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_6(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [6, 6, 6, 0, 4, 2, 1, 0, 0, 5, 5, 0]
        assert game.store == [8, 5]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_7(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is False
        assert game.board == [7, 7, 7, 1, 4, 0, 1, 0, 0, 5, 0, 1]
        assert game.store == [8, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_8(self, gstate):
        game = gstate.game
        cond = game.move((4, CW))
        assert game.turn is True
        assert game.board == [8, 8, 8, 2, 0, 0, 1, 0, 0, 5, 0, 1]
        assert game.store == [8, 7]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_9(self, gstate):
        game = gstate.game
        cond = game.move((2, CW))
        assert game.turn is False
        assert game.board == [0, 8, 8, 2, 1, 1, 2, 1, 1, 0, 0, 1]
        assert game.store == [8, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, CW))
        assert game.turn is True
        assert game.board == [1, 0, 8, 2, 1, 2, 1, 1, 2, 1, 1, 2]
        assert game.store == [11, 15]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_11(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 0, 1, 1, 0, 2, 2, 2]
        assert game.store == [11, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_12(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 1, 1, 1, 0, 2, 2, 0]
        assert game.store == [13, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_18_move_13(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.mdata.winner is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [13, 35]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_19_setup(self, gstate):
        game = gstate.game
        game.new_game(gstate.cond, new_round_ok=True)
        assert game.turn is False
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_19_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is True
        assert game.board == [0, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_2(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [1, 6, 6, 6, 5, 4, 4, 4, 4, 4, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_3(self, gstate):
        game = gstate.game
        cond = game.move((4, CCW))
        assert game.turn is True
        assert game.board == [1, 6, 6, 6, 0, 5, 5, 5, 5, 5, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_4(self, gstate):
        game = gstate.game
        cond = game.move((5, CW))
        assert game.turn is False
        assert game.board == [1, 7, 7, 7, 1, 6, 0, 5, 5, 5, 4, 0]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_5(self, gstate):
        game = gstate.game
        cond = game.move((1, CCW))
        assert game.turn is True
        assert game.board == [1, 0, 8, 8, 2, 7, 1, 1, 6, 5, 4, 0]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_6(self, gstate):
        game = gstate.game
        cond = game.move((3, CCW))
        assert game.turn is False
        assert game.board == [2, 1, 9, 8, 0, 0, 1, 1, 0, 6, 5, 1]
        assert game.store == [5, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_7(self, gstate):
        game = gstate.game
        cond = game.move((2, CCW))
        assert game.turn is True
        assert game.board == [2, 1, 0, 9, 1, 1, 2, 2, 1, 7, 1, 2]
        assert game.store == [10, 9]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_8(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.turn is False
        assert game.board == [3, 1, 0, 0, 1, 1, 2, 2, 1, 7, 1, 0]
        assert game.store == [10, 19]
        assert cond is None
        gstate.cond = cond

    def test_round_19_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, CCW))
        assert game.mdata.winner is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [29, 19]
        assert cond.name == "WIN"
        gstate.cond = cond
