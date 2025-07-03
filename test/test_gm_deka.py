# -*- coding: utf-8 -*-
"""Test deka games.

TestDeka1 was manually modified when Deka was changed
to an Immobilize goal.  See last two moves.

Created on Thu Aug 17 15:23:34 2023
@author: Ann"""

import pytest
pytestmark = [pytest.mark.integtest]

from context import man_config


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

    game, _ = man_config.make_game('./GameProps/Deka.txt')
    gstate = GameTestData(game)
    return gstate


@pytest.mark.incremental
class TestDeka1:

    def test_setup(self, gstate):

        game = gstate.game
        game.turn = False
        game.starter = False
        assert game.board == [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [3, 0, 3, 3, 0, 1, 4, 1, 3, 3, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [3, 0, 3, 3, 0, 1, 0, 2, 4, 4, 1, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 6, 1, 1, 0, 0, 0, 6, 1, 5]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [2, 3, 1, 7, 0, 2, 1, 0, 0, 6, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [2, 0, 2, 8, 1, 2, 1, 0, 0, 6, 1, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [2, 0, 2, 8, 1, 2, 1, 0, 0, 6, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [1, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 0, 0, 9, 0, 3, 0, 0, 1, 6, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [0, 3, 1, 2, 1, 0, 1, 0, 4, 1, 3, 3]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 3, 1, 2, 0, 1, 1, 0, 4, 1, 3, 3]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 3, 1, 2, 0, 1, 1, 0, 0, 2, 4, 4]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [6, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 3, 1, 2, 0, 0, 0, 0, 1, 2, 4, 4]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 4, 2, 3, 1, 0, 0, 0, 1, 0, 5, 0]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 4, 2, 3, 0, 1, 0, 0, 1, 0, 5, 0]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_14(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 4, 2, 3, 0, 1, 0, 0, 0, 1, 5, 0]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_15(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 4, 2, 0, 1, 2, 1, 0, 0, 1, 5, 0]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 4, 2, 0, 1, 2, 0, 0, 1, 1, 5, 0]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_17(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 4, 2, 3, 1, 1, 0, 0, 2, 0, 1]
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [9, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_18(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 5, 0, 4, 2, 0, 0, 1, 1, 1, 0]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [10, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_19(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 5, 3, 1, 0, 0, 2, 0, 1]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [11, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_20(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 5, 3, 1, 0, 0, 0, 1, 0]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [13, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 4, 2, 0, 1, 1, 1, 0]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_22(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 4, 2, 0, 0, 0, 2, 1]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_23(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 4, 2, 0, 0, 0, 2, 1]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [14, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_24(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 4, 2, 0, 0, 0, 0, 2]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [15, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_25(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 3, 0, 1, 1, 0, 2]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_26(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 3, 0, 1, 0, 1, 2]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_27(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 3, 0, 1, 0, 1, 2]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [16, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 2, 1, 0, 3]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [17, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_29a(self, gstate):
        """Change of Deka to immobilize game, continues the game
        at this point: False gave away their seeds, but True has
        moves--so they must move."""

        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 3]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [17, 0]
        assert cond is None

    def test_move_29b(self, gstate):
        """Force end game here, by moving for True, but don't give False
        seeds."""

        game = gstate.game
        cond = game.move(2)
        assert game.mdata.winner is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 3]
        assert game.blocked == [T, F, F, T, F, F, F, T, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [17, 0]
        assert cond.name == "WIN"


@pytest.mark.incremental
class TestDeka2:

    def test_setup(self, gstate):

        game = gstate.game
        game.turn = False
        game.starter = False
        assert game.board == [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]

    def test_move_1(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is True
        assert game.board == [3, 0, 3, 3, 0, 1, 4, 1, 3, 3, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_2(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [0, 1, 4, 4, 1, 1, 4, 1, 3, 0, 1, 4]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 0, 2, 7, 1, 3, 1, 0, 5, 2, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [4, 0, 4, 1, 2, 4, 1, 0, 1, 4, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_5(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [4, 0, 0, 2, 3, 5, 0, 0, 0, 5, 0, 3]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_6(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [5, 1, 1, 2, 3, 5, 0, 0, 0, 5, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_7(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [5, 1, 0, 0, 4, 6, 1, 0, 0, 5, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_8(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [6, 2, 1, 1, 4, 6, 1, 0, 0, 0, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [2, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [0, 1, 3, 1, 6, 1, 3, 0, 1, 1, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_10(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.turn is False
        assert game.board == [1, 2, 0, 2, 7, 2, 1, 0, 2, 2, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, F, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [5, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 8, 3, 0, 0, 0, 3, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_12(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [1, 2, 1, 2, 1, 4, 1, 0, 0, 4, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [7, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_13(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 2, 5, 0, 0, 0, 4, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [9, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_14(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is False
        assert game.board == [2, 3, 1, 0, 2, 5, 0, 0, 0, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [9, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_15(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is True
        assert game.board == [2, 3, 1, 0, 0, 6, 1, 0, 0, 0, 0, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [9, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_16(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is False
        assert game.board == [4, 1, 3, 0, 2, 1, 2, 0, 0, 1, 0, 1]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [9, 0]
        assert cond is None
        gstate.cond = cond

    def test_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        assert game.mdata.winner is False     # manual change
        assert game.board == [5, 0, 4, 1, 2, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, T, T, T, F, T, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [12, 0]
        assert cond.name == "WIN"
        gstate.cond = cond
