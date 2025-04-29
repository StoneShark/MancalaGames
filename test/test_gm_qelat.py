# -*- coding: utf-8 -*-
"""Test the qelat game.

Created on Thu Aug 17 06:42:25 2023
@author: Ann"""


import pytest
pytestmark = [pytest.mark.integtest]

from context import man_config
from context import game_interface as gi


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

    game, _ = man_config.make_game('./GameProps/Qelat.txt')
    gstate = GameTestData(game)
    return gstate


@pytest.mark.incremental
class TestQelat:

    def test_setup(self, gstate):
        game = gstate.game
        game.turn = True
        assert game.turn is True
        assert game.board == [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 0, 5]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [5, 5, 5, 4, 4, 0, 5, 5, 5, 5, 0, 5]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [5, 6, 6, 5, 5, 1, 0, 5, 5, 5, 0, 5]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [6, 7, 0, 5, 5, 1, 0, 5, 6, 6, 1, 6]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [6, 7, 1, 6, 6, 2, 1, 0, 6, 6, 1, 6]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [6, 7, 1, 0, 7, 3, 2, 1, 7, 7, 1, 6]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [7, 8, 2, 1, 8, 4, 2, 1, 7, 7, 1, 0]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [8, 0, 2, 1, 8, 5, 3, 2, 8, 8, 2, 1]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [8, 0, 2, 1, 8, 6, 4, 0, 8, 8, 2, 1]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [9, 0, 2, 1, 0, 7, 5, 1, 9, 9, 3, 2]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [10, 1, 3, 2, 1, 8, 6, 1, 9, 0, 4, 3]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [11, 2, 0, 2, 1, 8, 6, 1, 9, 0, 4, 4]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [11, 2, 0, 2, 1, 8, 7, 0, 9, 0, 4, 4]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_14(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 1, 3, 2, 9, 8, 1, 10, 1, 5, 5]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 4, 2, 4, 3, 10, 0, 1, 10, 1, 6, 6]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 5, 0, 4, 3, 10, 0, 1, 10, 1, 6, 6]
        assert game.child == [N, N, N, N, N, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_17(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 6, 1, 5, 4, 10, 0, 1, 10, 1, 0, 7]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [4, 0, 1, 5, 4, 10, 0, 2, 11, 2, 1, 8]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_19(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [4, 0, 1, 5, 4, 10, 0, 2, 11, 0, 2, 9]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_20(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 1, 5, 4, 10, 0, 2, 12, 1, 3, 10]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [1, 1, 2, 6, 9, 11, 1, 0, 0, 2, 4, 11]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_22(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 2, 0, 6, 9, 11, 1, 0, 0, 2, 4, 11]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_23(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [3, 3, 1, 6, 9, 11, 1, 0, 0, 2, 0, 12]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_24(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [3, 0, 0, 6, 9, 11, 1, 0, 0, 2, 0, 16]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_25(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [3, 0, 0, 6, 9, 11, 1, 0, 0, 0, 1, 17]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_26(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 0, 0, 6, 9, 11, 1, 0, 0, 1, 2, 18]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 6, 9, 11, 1, 0, 0, 0, 3, 18]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_28(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 10, 12, 2, 1, 1, 1, 3, 18]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_29(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.mdata.winner is True
        assert game.board == [0, 0, 0, 0, 14, 12, 2, 1, 1, 0, 0, 18]
        assert game.child == [N, N, N, N, T, T, N, N, N, N, N, F]
        assert game.store == [0, 0]
        assert cond.name == "WIN"
        gstate.cond = cond

        winmsg = game.win_message(cond)
        assert 'Game Over' in winmsg[0]
        assert gi.PLAYER_NAMES[True] in winmsg[1]
