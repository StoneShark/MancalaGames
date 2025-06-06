# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 10:46:45 2025
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

    game, _ = man_config.make_game('./GameProps/Enlightenment.txt')
    gstate = GameTestData(game)
    return gstate


CW = gi.Direct.CW
CCW = gi.Direct.CCW


@pytest.mark.incremental
class TestEnlightenment:

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = True
        game.starter = True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CW))
        assert game.turn is False
        assert game.board == [4, 4, 4, 5, 5, 5, 5, 0, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move((1, 2, CW))
        assert game.turn is True
        assert game.board == [5, 5, 0, 5, 5, 5, 5, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move((0, 3, CW))
        assert game.turn is False
        assert game.board == [5, 6, 1, 6, 6, 6, 0, 0, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move((1, 3, CCW))
        assert game.turn is True
        assert game.board == [5, 6, 1, 0, 7, 7, 1, 1, 6, 6]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CW))
        assert game.turn is False
        assert game.board == [6, 7, 0, 1, 8, 0, 1, 1, 7, 7]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move((1, 1, CW))
        assert game.turn is True
        assert game.board == [7, 0, 0, 1, 9, 1, 0, 0, 8, 8]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move((0, 4, CW))
        assert game.turn is False
        assert game.board == [7, 0, 0, 1, 10, 0, 0, 0, 8, 8]
        assert game.store == [2, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move((1, 0, CW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 11, 1, 1, 1, 9, 9]
        assert game.store == [4, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move((0, 0, CCW))
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 12, 0, 0, 0, 10, 0]
        assert game.store == [4, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 1, 11, 1]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move((0, 2, CW))
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 11, 1]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        game = gstate.game
        cond = game.move((1, 4, CCW))
        assert game.mdata.winner is False
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 11, 1]
        assert game.store == [12, 14]
        assert cond.name == "WIN"
        gstate.cond = cond
