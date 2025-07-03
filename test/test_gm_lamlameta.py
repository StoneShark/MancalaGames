# -*- coding: utf-8 -*-
"""Test lamlameta

TODO verify:

        no sow with 2 unless all 2
            assert game.mdata...  help find them and removed where checked
            commented out because they as a second to test time
        skip opp 2 on sow
        sow own 2s
        xcapt but only if 2  - yep
        capt all opp 2s on capt - yep

Created on Thu Oct 10 10:09:57 2024
@author: Ann"""


import pytest
pytestmark = pytest.mark.integtest

from context import man_config

T = True
F = False
N = None

class GameTestData:
    """allow passing move end cond between tests."""

    def __init__(self, game):
        self.game = game
        self.cond = None


@pytest.fixture(scope="class")
def gstate():
    """This fixture will maintain state between tests in the
    same class but will be reconstructed for each class."""

    game, _ = man_config.make_game('./GameProps/Lamlameta.txt')
    gstate = GameTestData(game)
    return gstate


@pytest.mark.incremental
class TestLamlameta:
    """ """

    def test_game_setup(self, gstate):
        game = gstate.game
        game.turn = False
        game.starter = False
        assert game.board == [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert game.store == [0, 0]

    def test_round_1_move_1(self, gstate):
        """First move from 10 or 11. No captures, but then there can be no twos."""
        game = gstate.game
        cond = game.move(10)
        assert game.turn is True
        assert game.board == [0, 3, 3, 0, 3, 3, 0, 3, 3, 0, 1, 4, 1, 3, 3, 0, 3, 3, 0, 3, 3, 0, 3, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_2(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 3, 3, 0, 3, 3, 0, 3, 3, 0, 1, 4, 1, 3, 0, 1, 4, 0, 1, 4, 4, 1, 3, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_3(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 3, 0, 1, 4, 0, 1, 4, 4, 1, 1, 4, 1, 3, 0, 1, 4, 0, 1, 4, 4, 1, 3, 3]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 3, 0, 1, 4, 0, 1, 4, 4, 1, 1, 4, 1, 3, 0, 1, 4, 0, 0, 0, 5, 2, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_5(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 3, 0, 1, 4, 0, 1, 4, 0, 2, 2, 5, 0, 4, 1, 1, 4, 0, 0, 0, 5, 2, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_6(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 3, 0, 1, 4, 0, 1, 4, 0, 2, 2, 5, 0, 4, 0, 0, 5, 1, 0, 0, 5, 2, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_7(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 5, 1, 1, 4, 0, 2, 2, 5, 0, 4, 0, 0, 5, 1, 0, 0, 5, 2, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_8(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 2, 5, 1, 1, 4, 0, 2, 2, 5, 0, 4, 0, 0, 5, 0, 1, 0, 5, 2, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_9(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 5, 1, 0, 0, 1, 3, 3, 6, 1, 4, 0, 0, 5, 0, 1, 0, 5, 2, 4, 4]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_10(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 1, 2, 5, 1, 0, 0, 1, 3, 3, 6, 1, 4, 0, 0, 5, 0, 1, 0, 0, 3, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_11(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 1, 1, 2, 5, 1, 0, 0, 1, 0, 4, 7, 0, 5, 1, 0, 5, 0, 1, 0, 0, 3, 5, 5]
        assert game.store == [0, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_12(self, gstate):
        """capture from 15. collect alt he other 2s."""
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 8, 1, 6, 2, 1, 0, 1, 2, 1, 1, 0, 6, 6]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_13(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 8, 1, 6, 2, 1, 0, 1, 2, 1, 1, 0, 6, 6]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_14(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 8, 1, 0, 3, 2, 1, 2, 3, 0, 2, 1, 6, 6]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_15(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 8, 1, 0, 3, 2, 1, 2, 3, 0, 2, 1, 6, 6]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_16(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 8, 1, 0, 3, 2, 1, 2, 3, 0, 2, 1, 0, 7]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 2, 1, 0, 1, 1, 1, 0, 8, 1, 0, 3, 2, 1, 2, 3, 0, 2, 1, 0, 7]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_18(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 1, 2, 2, 1, 2, 0, 2, 1, 8, 1, 0, 0, 3, 2, 0, 4, 1, 0, 2, 1, 0]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_19(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 1, 0, 0, 3, 2, 0, 1, 3, 0, 9, 0, 1, 1, 3, 2, 0, 4, 1, 0, 2, 1, 0]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_20(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 0, 0, 3, 2, 0, 1, 3, 0, 9, 0, 1, 1, 3, 2, 0, 4, 0, 1, 2, 1, 0]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_21(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 3, 2, 1, 0, 3, 2, 0, 1, 3, 0, 0, 1, 0, 0, 4, 0, 1, 5, 1, 0, 0, 0, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_22(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 3, 2, 1, 0, 3, 2, 0, 1, 3, 0, 0, 0, 1, 0, 4, 0, 1, 5, 1, 0, 0, 0, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_23(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 3, 2, 1, 0, 3, 2, 0, 1, 0, 1, 1, 1, 1, 0, 4, 0, 1, 5, 1, 0, 0, 0, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_24(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 3, 2, 1, 0, 3, 2, 0, 1, 0, 1, 1, 1, 0, 1, 4, 0, 1, 5, 1, 0, 0, 0, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_25(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 3, 2, 1, 0, 3, 2, 0, 1, 0, 1, 0, 0, 1, 0, 5, 1, 1, 5, 1, 0, 0, 0, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_26(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 3, 2, 1, 0, 3, 2, 0, 1, 0, 1, 0, 0, 1, 0, 5, 1, 1, 5, 0, 1, 0, 0, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_27(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 3, 2, 0, 1, 3, 2, 0, 1, 0, 1, 0, 0, 1, 0, 5, 1, 1, 5, 0, 1, 0, 0, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_28(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 3, 2, 0, 1, 3, 2, 0, 1, 0, 1, 0, 0, 1, 0, 5, 0, 0, 6, 1, 1, 0, 0, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_29(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 3, 2, 0, 1, 3, 2, 0, 1, 0, 0, 1, 0, 1, 0, 5, 0, 0, 6, 1, 1, 0, 0, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_30(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 3, 2, 0, 1, 3, 2, 0, 1, 0, 0, 1, 0, 1, 0, 5, 0, 0, 6, 0, 0, 1, 1, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_31(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 3, 2, 0, 1, 0, 3, 1, 0, 1, 1, 1, 0, 1, 0, 5, 0, 0, 6, 0, 0, 1, 1, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_32(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 3, 2, 0, 1, 0, 3, 1, 0, 1, 1, 1, 0, 0, 1, 5, 0, 0, 6, 0, 0, 1, 1, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_33(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 3, 2, 0, 1, 0, 3, 0, 1, 1, 1, 1, 0, 0, 1, 5, 0, 0, 6, 0, 0, 1, 1, 1]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_34(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 3, 2, 0, 1, 0, 3, 0, 1, 1, 1, 1, 0, 0, 1, 5, 0, 0, 0, 1, 1, 2, 2, 2]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_35(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 3, 1, 2, 1, 3, 0, 1, 1, 1, 1, 0, 0, 1, 5, 0, 0, 0, 1, 1, 2, 2, 2]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_36(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 3, 1, 2, 1, 3, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 3, 3]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_37(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 3, 0, 4, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 3, 3]
        assert game.store == [10, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_38(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 1, 5, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 3, 0, 1, 4, 0]
        assert game.store == [10, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_39(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 3, 0, 1, 4, 0]
        assert game.store == [10, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_40(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 2, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 1]
        assert game.store == [10, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_41(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 2, 2, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 1]
        assert game.store == [10, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_42(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 2, 2, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0]
        assert game.store == [10, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_43(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 2, 2, 2, 1, 0, 1, 1, 1, 0, 0, 2, 0, 1, 1, 0, 1, 0, 0, 3, 0, 0, 0, 0]
        assert game.store == [10, 20]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_44(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_45(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_46(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_47(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_48(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_49(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_50(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_51(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_52(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 2, 1, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_53(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 2, 1, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_54(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 2, 1, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_55(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 2, 1, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_56(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 2, 1, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_57(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 2, 1, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_58(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 2, 1, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_59(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 2, 1, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_60(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_61(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_62(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 2, 0, 0, 1, 1, 0, 0, 0, 1, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_63(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 2, 0, 0, 1, 1, 0, 0, 0, 1, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_64(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 2, 0, 0, 1, 1, 0, 0, 0, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_65(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 2, 0, 0, 1, 1, 0, 0, 0, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_66(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 2, 0, 0, 1, 0, 1, 0, 0, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_67(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 2, 0, 0, 1, 0, 1, 0, 0, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_68(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 2, 0, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_69(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 2, 1, 0, 1, 0, 0, 1, 0, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_70(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 1, 0, 1, 1, 1, 0, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_71(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 1, 0, 1, 1, 1, 0, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_72(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 2, 1, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_73(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 0, 0, 0, 2, 1, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_74(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0, 2, 1, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_75(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0, 2, 1, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_76(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 1, 0, 2, 1, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_77(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 2, 0, 0, 1, 0, 2, 1, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_78(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 2, 0, 0, 0, 1, 2, 1, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_79(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 2, 1, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_80(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 1, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_81(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 1, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_82(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_83(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 2, 0, 0, 0, 0, 0, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_84(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_85(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_86(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_87(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_88(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_89(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_90(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_91(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_92(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_93(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_94(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_95(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 2, 0, 1]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_96(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 2]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_97(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 2]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_98(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_99(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 2, 2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_100(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 2, 2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_101(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 2, 2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [10, 28]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_102(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_103(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_104(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_105(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_106(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_107(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_108(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_109(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_110(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_111(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_112(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_113(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_114(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_115(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [10, 32]
        assert cond is None
        gstate.cond = cond

    def test_round_1_move_116(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [10, 38]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_2_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        assert game.blocked == [F, F, F, F, F, T, T, T, T, T, T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [0, 14]

    def test_round_2_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 3, 3, 0, 3, 3, 0, 3, 3]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_2(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 4, 0, 2, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 1, 4, 0, 1, 4, 4, 1, 3, 0]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 6, 2, 2, 1, 5, 2, 4, 1]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_4(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 6, 2, 2, 0, 0, 3, 5, 2]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_5(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 7, 2, 2, 1, 0, 3, 5, 2]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_6(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 3, 0, 3, 3, 2, 1, 4, 1, 4]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 4, 1, 3, 3, 2, 1, 4, 1, 4]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 4, 4, 1, 3, 3, 2, 0, 0, 2, 5]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 5, 2, 4, 4, 2, 1, 0, 2, 5]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_10(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 5, 2, 4, 0, 3, 2, 1, 0, 6]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_11(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 5, 2, 4, 0, 3, 2, 1, 0, 6]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_12(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 7, 1, 0, 2, 1, 4, 3, 2, 1]
        assert game.store == [0, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 5, 4, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_14(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 4, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_15(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 4, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_16(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 4, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_17(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 5, 4, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_18(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 5, 1, 1]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_19(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 5, 1, 1]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_20(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 5, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_21(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 5, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_22(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 5, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_23(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 5, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_24(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 5, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_25(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 5, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_26(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 5, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_27(self, gstate):
        """False is allowed to sow with 2 seeds because all holes have 2 seeds (or 0)"""
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 5, 0, 0]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_28(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0, 1, 1]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_29(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0, 1, 1]
        assert game.store == [14, 22]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_30(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 1, 1, 1]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_31(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0, 1, 1, 1]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_32(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2, 0, 0, 1, 1, 1]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_33(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2, 0, 0, 1, 1, 1]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_34(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 0, 1, 1, 1]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_35(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 0, 1, 1, 1]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_36(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 0, 1, 1, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_37(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 0, 1, 1, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_38(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 0, 1, 0, 1]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_39(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 0, 1, 0, 1]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_40(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 0, 0, 1, 1]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_41(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 2, 0, 0, 0, 1, 1]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_42(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 2, 0, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_43(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 2, 0, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_44(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_45(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_46(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_47(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_48(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 2, 0, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_49(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 2, 0, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_50(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 2, 0, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_51(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 2, 0, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_52(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3, 1, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_53(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3, 1, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_54(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 3, 1, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_55(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 3, 1, 0, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_56(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 3, 0, 1, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_57(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 3, 0, 1, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_58(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 0, 1, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_59(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 3, 0, 1, 0, 0, 0]
        assert game.store == [14, 26]
        assert cond is None
        gstate.cond = cond

    def test_round_2_move_60(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, T, T, T, T, T, T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [14, 34]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_3_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [0, 10]

    def test_round_3_move_1(self, gstate):
        game = gstate.game
        cond = game.move(6)
        assert game.turn is True
        assert game.board == [3, 0, 3, 3, 0, 3, 1, 0, 0, 0, 0, 0, 0, 1, 4, 4, 1, 3, 3, 0, 3, 3, 0, 3]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_2(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [4, 1, 3, 3, 0, 3, 1, 0, 0, 0, 0, 0, 0, 1, 4, 4, 1, 3, 0, 1, 4, 0, 1, 4]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [5, 0, 4, 1, 1, 4, 0, 0, 0, 0, 0, 0, 1, 0, 5, 0, 2, 4, 1, 2, 0, 1, 2, 5]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [6, 1, 4, 1, 1, 4, 0, 0, 0, 0, 0, 0, 1, 0, 5, 0, 2, 4, 0, 0, 1, 2, 0, 6]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_5(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [6, 1, 0, 2, 2, 5, 1, 0, 0, 0, 0, 0, 1, 0, 5, 0, 2, 4, 0, 0, 1, 2, 0, 6]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_6(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [6, 1, 0, 2, 2, 5, 1, 0, 0, 0, 0, 0, 0, 1, 5, 0, 2, 4, 0, 0, 1, 2, 0, 6]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_7(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [6, 1, 0, 2, 2, 5, 0, 0, 0, 0, 0, 0, 1, 1, 5, 0, 2, 4, 0, 0, 1, 2, 0, 6]
        assert game.store == [0, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_8(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [6, 1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 3, 5, 1, 1, 1, 2, 0, 6]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_9(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 2, 1, 1, 1, 6, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 3, 5, 1, 1, 1, 2, 0, 6]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 2, 2, 2, 7, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 4, 0, 2, 2, 2, 3, 1, 1]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_11(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 1, 4, 0, 1, 2, 3, 0, 0, 0, 0, 0, 2, 1, 2, 2, 0, 2, 2, 2, 2, 1, 2, 2]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_12(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [4, 2, 0, 1, 2, 2, 4, 0, 0, 0, 0, 0, 3, 1, 0, 3, 1, 0, 3, 3, 0, 2, 3, 0]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_13(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 3, 1, 2, 0, 3, 5, 0, 0, 0, 0, 0, 0, 2, 1, 4, 0, 1, 0, 4, 1, 2, 4, 1]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_14(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 4, 2, 2, 1, 3, 5, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 2, 1, 5, 0, 3, 0, 2]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 4, 2, 2, 1, 0, 6, 0, 0, 0, 0, 0, 1, 2, 1, 0, 1, 2, 1, 5, 0, 3, 0, 2]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_16(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 5, 2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 2, 3, 2, 1, 2, 3, 0, 1, 0, 5, 0, 4]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_17(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 5, 2, 2, 0, 0, 1, 0, 0, 0, 0, 0, 2, 3, 2, 1, 2, 3, 0, 1, 0, 5, 0, 4]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_18(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 6, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 2, 0, 3, 2, 0, 4, 1, 0, 1, 0, 1, 5]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_19(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 6, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 1, 3, 2, 0, 4, 1, 0, 1, 0, 1, 5]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_20(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 7, 2, 2, 1, 1, 2, 0, 0, 0, 0, 0, 3, 2, 0, 3, 1, 5, 0, 1, 0, 1, 1, 0]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_21(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 7, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 4, 2, 1, 0, 2, 6, 1, 0, 1, 0, 2, 1]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_22(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 7, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 4, 2, 1, 0, 2, 6, 0, 1, 1, 0, 2, 1]
        assert game.store == [0, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_23(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 1, 3, 3, 2, 1, 1, 0, 0, 0, 0, 0, 5, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_24(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [3, 1, 3, 3, 2, 1, 1, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_25(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 0, 0, 4, 3, 2, 0, 0, 0, 0, 0, 0, 6, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_26(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [3, 0, 0, 4, 3, 2, 0, 0, 0, 0, 0, 0, 6, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_27(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 4, 3, 1, 0, 0, 0, 0, 0, 7, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_28(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 4, 3, 1, 0, 0, 0, 0, 0, 7, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_29(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 4, 0, 2, 0, 0, 0, 0, 0, 8, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_30(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 4, 0, 2, 0, 0, 0, 0, 0, 8, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_31(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 4, 0, 2, 0, 0, 0, 0, 0, 8, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_32(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 4, 0, 2, 0, 0, 0, 0, 0, 8, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_33(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 4, 0, 2, 0, 0, 0, 0, 0, 8, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_34(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 4, 0, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1, 1, 2, 2, 1, 0, 1, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_35(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 3, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 0, 2, 2, 2, 1, 1, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_36(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 3, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 0, 2, 2, 2, 1, 0, 1]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_37(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 1]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_38(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 0]
        assert game.store == [12, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_39(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_40(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_41(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_42(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_43(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_44(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_45(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_46(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_48(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_49(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_50(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_51(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_52(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_53(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_54(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_55(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_56(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_57(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_58(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_59(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_60(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_61(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_62(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_63(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_64(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_65(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_66(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_67(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_68(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_69(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_70(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_71(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [30, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_3_move_72(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, T, T, T, T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [30, 18]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_4_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [6, 0]

    def test_round_4_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is False
        assert game.board == [4, 1, 3, 3, 0, 3, 3, 0, 3, 3, 0, 3, 3, 0, 3, 3, 0, 3, 3, 0, 1, 0, 0, 0]
        assert game.store == [6, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_2(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [5, 0, 4, 0, 1, 4, 4, 1, 3, 3, 0, 0, 4, 1, 0, 4, 1, 4, 0, 1, 2, 0, 0, 0]
        assert game.store == [6, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_3(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [6, 1, 0, 1, 2, 5, 5, 0, 4, 0, 1, 1, 5, 0, 1, 0, 2, 5, 1, 1, 1, 0, 0, 0]
        assert game.store == [6, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_4(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 2, 1, 2, 3, 1, 7, 0, 6, 0, 1, 0, 1, 2, 2, 0, 2, 7, 2, 1, 2, 0, 0, 0]
        assert game.store == [6, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_5(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 2, 2, 4, 0, 8, 1, 6, 0, 1, 0, 1, 2, 2, 0, 2, 0, 3, 2, 3, 0, 0, 0]
        assert game.store == [6, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_6(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 2, 2, 2, 4, 0, 0, 2, 7, 1, 2, 1, 2, 2, 2, 1, 2, 1, 3, 2, 3, 0, 0, 0]
        assert game.store == [6, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_7(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 1, 2, 0, 2, 9, 2, 2, 1, 3, 0, 3, 2, 0, 1, 1, 0, 5, 0, 0, 0]
        assert game.store == [6, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_8(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 3, 3, 3, 2, 0, 1, 3, 1, 3, 3, 2, 4, 1, 4, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [10, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_9(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [3, 3, 3, 3, 2, 0, 1, 3, 1, 3, 3, 2, 4, 1, 4, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [10, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_10(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 3, 3, 3, 2, 0, 1, 3, 0, 0, 4, 3, 5, 0, 5, 1, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [10, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_11(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [3, 3, 3, 3, 2, 0, 1, 3, 0, 0, 4, 3, 5, 0, 5, 0, 0, 1, 1, 0, 1, 0, 0, 0]
        assert game.store == [10, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_12(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 3, 3, 3, 2, 0, 1, 0, 1, 1, 0, 4, 6, 1, 6, 1, 0, 1, 1, 0, 1, 0, 0, 0]
        assert game.store == [10, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_13(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [3, 3, 3, 3, 0, 0, 1, 0, 1, 1, 0, 4, 6, 1, 6, 1, 0, 1, 0, 1, 1, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_14(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 3, 3, 3, 0, 0, 1, 0, 1, 0, 1, 4, 6, 1, 6, 1, 0, 1, 0, 1, 1, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_15(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 4, 4, 4, 1, 0, 1, 0, 1, 0, 1, 4, 6, 1, 6, 1, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_16(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 4, 0, 5, 2, 1, 0, 1, 0, 1, 0, 5, 0, 2, 7, 2, 1, 2, 1, 0, 1, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_17(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 5, 1, 5, 2, 1, 0, 1, 0, 1, 0, 5, 0, 2, 0, 3, 2, 3, 2, 1, 2, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_18(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 5, 1, 0, 3, 2, 1, 2, 1, 1, 0, 5, 0, 2, 0, 3, 2, 3, 2, 1, 2, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_19(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 5, 1, 0, 3, 2, 1, 2, 1, 1, 0, 5, 0, 2, 0, 0, 3, 4, 0, 2, 3, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_20(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 5, 1, 0, 3, 2, 1, 2, 0, 0, 1, 0, 1, 2, 1, 1, 4, 5, 1, 2, 3, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_21(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 2, 1, 4, 2, 2, 2, 1, 1, 1, 0, 1, 2, 1, 1, 4, 5, 0, 0, 4, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_22(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 2, 0, 0, 3, 3, 3, 2, 0, 2, 1, 1, 2, 1, 1, 4, 5, 0, 0, 4, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_23(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 2, 0, 0, 3, 3, 3, 2, 0, 2, 1, 1, 2, 1, 0, 0, 6, 1, 1, 5, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_24(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 1, 2, 0, 0, 3, 3, 0, 3, 1, 0, 2, 2, 2, 0, 1, 1, 6, 1, 1, 5, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_25(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 1, 1, 4, 4, 1, 3, 1, 0, 2, 2, 2, 0, 0, 0, 7, 0, 2, 0, 0, 0, 0]
        assert game.store == [10, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_26(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 2, 1, 0, 0, 5, 2, 4, 2, 1, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0]
        assert game.store == [16, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_27(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 1, 1, 0, 2, 5, 2, 2, 2, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [16, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_28(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 1, 0, 1, 2, 5, 2, 2, 2, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [16, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_29(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 1, 0, 1, 2, 5, 2, 2, 2, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
        assert game.store == [16, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_30(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 1, 0, 1, 2, 0, 3, 3, 3, 2, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
        assert game.store == [16, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_31(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 0, 1, 0, 2, 1, 0, 4, 4, 3, 1, 1, 1, 1, 1, 0, 0, 2, 0, 0, 0]
        assert game.store == [16, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_32(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 0, 0, 1, 2, 1, 0, 4, 4, 3, 1, 1, 1, 1, 1, 0, 0, 2, 0, 0, 0]
        assert game.store == [16, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_33(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 0, 0, 1, 2, 1, 0, 4, 4, 3, 0, 0, 2, 0, 2, 1, 0, 2, 0, 0, 0]
        assert game.store == [16, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_34(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 0, 0, 1, 2, 1, 0, 4, 0, 4, 1, 1, 2, 1, 2, 1, 0, 2, 0, 0, 0]
        assert game.store == [16, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_35(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 1, 1, 0, 2, 2, 1, 4, 0, 4, 1, 0, 0, 2, 3, 0, 1, 0, 0, 0, 0]
        assert game.store == [16, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_36(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 1, 1, 0, 2, 2, 0, 0, 1, 5, 2, 1, 1, 2, 3, 0, 1, 0, 0, 0, 0]
        assert game.store == [16, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_37(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 0, 2, 1, 2, 2, 0, 0, 1, 5, 2, 1, 0, 0, 4, 1, 0, 1, 0, 0, 0]
        assert game.store == [16, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_38(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 0, 2, 0, 0, 3, 1, 1, 1, 5, 0, 1, 0, 0, 4, 1, 0, 1, 0, 0, 0]
        assert game.store == [18, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_39(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 1, 2, 0, 0, 3, 1, 1, 1, 5, 0, 1, 0, 0, 0, 2, 1, 2, 0, 0, 0]
        assert game.store == [18, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_40(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 0, 3, 3, 0, 3, 1, 0, 3, 0, 0, 2, 0, 1, 2, 1, 1, 1, 2, 0, 2, 0, 0, 0]
        assert game.store == [18, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_41(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 4, 4, 1, 3, 1, 0, 3, 0, 0, 2, 0, 1, 2, 0, 0, 2, 0, 1, 3, 0, 0, 0]
        assert game.store == [18, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_42(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 4, 4, 1, 3, 0, 1, 3, 0, 0, 2, 0, 1, 2, 0, 0, 2, 0, 1, 3, 0, 0, 0]
        assert game.store == [18, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_43(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 5, 0, 2, 4, 1, 2, 0, 1, 1, 2, 1, 1, 0, 1, 1, 0, 1, 2, 0, 0, 0, 0]
        assert game.store == [18, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_44(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 2, 5, 0, 2, 0, 2, 3, 1, 0, 2, 0, 2, 2, 1, 1, 1, 0, 1, 2, 0, 0, 0, 0]
        assert game.store == [18, 2]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_45(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 5, 0, 0, 0, 0, 3, 1, 0, 0, 0, 2, 2, 1, 1, 0, 1, 1, 2, 0, 0, 0, 0]
        assert game.store == [18, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_46(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 1, 1, 1, 0, 2, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_47(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 1, 1, 0, 2, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_48(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 1, 1, 0, 2, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_49(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 1, 1, 0, 2, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_50(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 1, 1, 0, 2, 0, 0, 2, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_51(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 1, 1, 0, 2, 0, 0, 2, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_52(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 1, 0, 1, 2, 0, 0, 2, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_53(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 1, 1, 0, 1, 2, 0, 0, 2, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_54(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 1, 1, 0, 1, 2, 0, 0, 2, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_55(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 1, 1, 0, 1, 2, 0, 0, 2, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_56(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 2, 1, 1, 2, 0, 0, 2, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_57(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 2, 1, 1, 2, 0, 0, 2, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_58(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 2, 2, 0, 1, 1, 0, 1, 2, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_59(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 2, 2, 0, 1, 1, 0, 1, 2, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_60(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 1, 0, 2, 2, 0, 1, 1, 0, 1, 2, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 10]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_61(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 2, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_62(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 2, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_63(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 2, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_64(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 2, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_65(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 2, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_66(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 2, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_67(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_68(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_69(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_70(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_71(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_72(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_73(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_74(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_75(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_76(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_77(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_78(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_79(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_80(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_81(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_82(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_83(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_84(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_85(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_86(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_87(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_88(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_89(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_90(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_91(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_92(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 2, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_93(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_94(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_95(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 2, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_96(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 2, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_97(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 2, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_98(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 2, 0, 1, 1, 1, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_99(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 2, 0, 0, 0, 2, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_100(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 2, 0, 0, 0, 2, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_101(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 2, 0, 0, 0]
        assert game.store == [24, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_102(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_103(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_104(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_105(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_106(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_107(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_108(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_109(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_110(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_111(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_112(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_113(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_114(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_115(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_116(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_117(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_118(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_119(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_120(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_121(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_122(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_123(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_124(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_125(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_126(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_127(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_128(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_129(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_130(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_131(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_132(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_133(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_134(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_135(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_136(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_137(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_138(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_139(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_140(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 14]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_141(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [26, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_142(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_143(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_144(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_145(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_146(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_147(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_148(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_149(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_150(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_151(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_152(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_153(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_154(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_155(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_156(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_157(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_158(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_159(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_160(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_161(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_162(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_163(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_164(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_165(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [28, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_4_move_166(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.mdata.winner is False     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T, T, T]
        assert game.store == [32, 16]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_5_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [8, 0]

    def test_round_5_move_1(self, gstate):
        game = gstate.game
        cond = game.move(4)
        assert game.turn is False
        assert game.board == [3, 0, 3, 3, 0, 3, 3, 0, 3, 3, 0, 3, 3, 0, 3, 3, 0, 3, 3, 1, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_2(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [4, 1, 0, 4, 1, 4, 0, 1, 4, 4, 1, 0, 4, 1, 0, 4, 1, 4, 0, 2, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_3(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [4, 1, 0, 4, 1, 4, 0, 1, 4, 4, 1, 0, 4, 0, 1, 4, 1, 4, 0, 2, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_4(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [4, 1, 0, 4, 1, 4, 0, 0, 0, 5, 2, 1, 5, 1, 1, 4, 1, 4, 0, 2, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_5(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [4, 1, 0, 4, 1, 4, 0, 0, 0, 5, 2, 1, 5, 0, 0, 5, 0, 5, 1, 2, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [4, 1, 0, 0, 2, 5, 1, 1, 0, 5, 2, 1, 5, 0, 0, 5, 0, 5, 1, 2, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_7(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 2, 1, 1, 2, 6, 0, 2, 1, 5, 2, 1, 5, 0, 0, 0, 1, 6, 2, 3, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_8(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 2, 1, 0, 0, 7, 1, 0, 2, 6, 0, 2, 6, 1, 0, 0, 1, 6, 2, 3, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_9(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 2, 1, 0, 0, 7, 1, 0, 2, 6, 0, 2, 6, 0, 1, 0, 1, 6, 2, 3, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_10(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 2, 1, 0, 0, 0, 2, 1, 3, 7, 1, 3, 0, 1, 2, 1, 2, 7, 2, 4, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_11(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 1, 1, 0, 2, 1, 3, 7, 1, 3, 0, 1, 2, 1, 2, 7, 2, 0, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_12(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 2, 1, 1, 0, 2, 1, 3, 0, 2, 4, 1, 2, 2, 2, 2, 8, 2, 1, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_13(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 0, 1, 2, 0, 4, 1, 2, 4, 0, 0, 3, 3, 0, 9, 3, 0, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_14(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 0, 1, 2, 0, 0, 2, 3, 5, 1, 0, 3, 3, 0, 9, 3, 0, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_15(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 1, 0, 2, 1, 1, 2, 3, 5, 1, 0, 3, 3, 0, 9, 0, 1, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_16(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 2, 2, 1, 0, 2, 1, 1, 2, 0, 6, 2, 1, 3, 3, 0, 9, 0, 1, 0, 0, 0, 0]
        assert game.store == [8, 0]
        assert cond is None
        gstate.cond = cond

    def test_round_5_move_17(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T, T, T, T]
        assert game.store == [8, 40]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_6_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        assert game.blocked == [F, F, F, F, T, T, T, T, T, T, T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [0, 16]

    def test_round_6_move_1(self, gstate):
        game = gstate.game
        cond = game.move(3)
        assert game.turn is True
        assert game.board == [3, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 4, 1, 3, 3, 0, 3, 3, 0, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_2(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [4, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 4, 0, 0, 4, 1, 4, 0, 1, 4]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_3(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [4, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 5, 1, 1, 5, 0, 5, 1, 1, 4]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_4(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 2, 0, 1, 3, 1, 2, 7, 3, 0, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 2, 0, 2, 2, 8, 4, 1, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_6(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 2, 0, 2, 2, 0, 5, 2, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_7(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 2, 2, 1, 5, 2, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_8(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 0, 3, 2, 0, 3, 4]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 2, 1, 4, 2, 1, 3, 4]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_10(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 4, 4, 0, 2, 1, 4, 2, 1, 3, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_11(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 1, 2, 2, 5, 2, 0, 4, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_12(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 6, 2, 3, 0, 6, 3, 1, 4, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_13(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 7, 2, 0, 1, 7, 4, 0, 5, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_14(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [4, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 7, 2, 0, 0, 0, 5, 1, 6, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_15(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 4, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 0, 7, 2, 0, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_16(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 5, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 3, 2, 0, 1, 8, 0, 1, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_17(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 0, 2, 0, 2, 1, 2, 9, 1, 1, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_18(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 0, 1, 0, 4, 1, 3, 0, 2, 1, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_19(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 2, 1, 2, 1, 2, 4, 1, 2, 2, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_20(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 2, 3, 2, 3, 5, 2, 0, 3, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_21(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 1, 2, 5, 7, 2, 2, 1, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_22(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 3, 1, 0, 6, 8, 0, 3, 2, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_23(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 3, 1, 0, 6, 8, 0, 3, 2, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_24(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 1, 0, 2, 1, 7, 0, 1, 4, 3, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_25(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 2, 0, 1, 2, 0, 8, 1, 1, 4, 3, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_26(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 2, 3, 1, 1, 2, 2, 5, 4, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [5, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 2, 1, 2, 0, 2, 2, 8, 0, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_28(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [5, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 2, 0, 2, 2, 8, 0, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_29(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [5, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 2, 2, 2, 1, 2, 2, 8, 0, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [6, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 2, 2, 1, 2, 2, 0, 1, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_31(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [6, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [7, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_33(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 2, 2, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_34(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 2, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_35(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 3, 7, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_36(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 3, 3, 0, 3, 3, 0, 3, 3, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_37(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 3, 3, 0, 3, 3, 0, 3, 3, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_38(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 3, 3, 0, 3, 3, 0, 0, 4, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_39(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 1, 4, 4, 1, 4, 4, 1, 0, 4, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_40(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 1, 4, 4, 1, 4, 4, 1, 0, 0, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_41(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 1, 4, 4, 1, 4, 4, 1, 0, 0, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_42(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 0, 0, 5, 2, 5, 5, 0, 1, 1, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_43(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 6, 2, 6, 0, 1, 2, 2, 4]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_44(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 6, 2, 0, 1, 2, 3, 3, 5]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_45(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 0, 2, 1, 2, 2, 4, 4, 6]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_46(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 0, 1, 3, 1, 0, 3, 5, 0, 7]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_47(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 0, 1, 3, 1, 0, 3, 5, 0, 7]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_48(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 0, 1, 3, 0, 1, 3, 5, 0, 7]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_49(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 1, 0, 4, 1, 1, 3, 5, 0, 7]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_50(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 3, 2, 1, 4, 1, 1, 3, 5, 0, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_51(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 2, 2, 5, 2, 2, 0, 6, 1, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_52(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 5, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 4, 7, 1, 0, 2, 1, 3, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_53(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 1, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 2, 1, 8, 2, 1, 2, 2, 0, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_54(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 2, 9, 0, 2, 3, 0, 1, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_55(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 2, 1, 2, 10, 1, 2, 3, 0, 1, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_56(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 2, 0, 0, 11, 2, 0, 4, 1, 0, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_57(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 2, 1, 0, 11, 2, 0, 4, 1, 0, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_58(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 2, 1, 0, 11, 2, 0, 0, 2, 1, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_59(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 2, 1, 0, 11, 2, 0, 0, 2, 1, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_60(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 7, 1, 2, 1, 0, 3, 1, 1, 3, 2, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_61(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 8, 0, 2, 2, 1, 3, 1, 1, 3, 2, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_62(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1, 3, 3, 2, 4, 2, 2, 0, 3, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_63(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 4, 4, 2, 0, 2, 2, 1, 4, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_64(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [4, 4, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 4, 0, 3, 1, 3, 0, 2, 5, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_65(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 5, 1, 3, 1, 3, 0, 2, 5, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_66(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 5, 1, 0, 2, 4, 1, 2, 5, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_67(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 5, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 5, 1, 0, 2, 4, 1, 2, 5, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_68(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 5, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 6, 2, 1, 2, 4, 1, 2, 5, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_69(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 2, 2, 2, 5, 2, 2, 6, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_70(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1, 2, 1, 3, 3, 0, 3, 3, 1, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_71(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 1, 2, 1, 3, 3, 0, 3, 3, 1, 3]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_72(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 1, 2, 1, 0, 4, 1, 0, 4, 2, 4]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_73(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [5, 0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_74(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 3, 3, 0, 3, 3, 0, 3, 3, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_75(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1, 4, 4, 1, 3, 3, 0, 3, 3, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_76(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1, 4, 4, 1, 3, 3, 0, 3, 3, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_77(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 2, 5, 0, 2, 4, 4, 1, 0, 4, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_78(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 6, 1, 0, 5, 5, 0, 1, 0, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_79(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 7, 2, 1, 0, 6, 1, 2, 1, 2]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_80(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 1, 4, 0, 2, 8, 0, 2, 0, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_81(self, gstate):
        """False sows with two seeds but not from 0 or 1 :)"""
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [2, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 0, 5, 1, 2, 8, 0, 2, 0, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_82(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 0, 5, 1, 2, 8, 0, 2, 0, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_83(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 5, 1, 5, 1, 2, 8, 0, 2, 0, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_84(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 6, 0, 6, 1, 0, 9, 1, 0, 1, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_85(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 6, 0, 6, 1, 0, 9, 1, 0, 1, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_86(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1, 0, 2, 1, 10, 2, 1, 2, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_87(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 7, 1, 0, 2, 1, 10, 2, 1, 2, 0]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_88(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 7, 1, 0, 2, 1, 10, 2, 0, 0, 1]
        assert game.store == [0, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_89(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 11, 0, 1, 1, 0]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_90(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 4, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 2, 2, 1]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_91(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 0, 1, 1, 0, 1, 2, 2, 1]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_92(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 0, 1, 1, 0, 0, 0, 3, 2]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_93(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 2, 1, 0, 2, 1, 0, 0, 3, 2]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_94(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 1, 0, 2, 1, 1, 3, 2]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_95(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 1, 0, 2, 1, 1, 3, 2]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_96(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 0, 2, 1, 0, 2, 1, 0, 0, 3]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_97(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 1, 2, 0, 1, 2, 0, 1, 1, 3]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_98(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 1, 2, 0, 1, 2, 0, 0, 0, 4]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_99(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 2, 0, 2, 1, 0, 2, 1, 1, 0, 4]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_100(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 4, 1, 2, 1, 0, 2, 1, 1]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_101(self, gstate):
        game = gstate.game
        cond = game.move(0)
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 2, 4, 1, 2, 1, 0, 2, 1, 1]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_102(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 2, 4, 1, 2, 1, 0, 2, 1, 0]
        assert game.store == [12, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_103(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 4, 1, 0, 1, 0, 0, 1, 0]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_104(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 4, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_105(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 4, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_106(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 4, 0, 1, 0, 1, 0, 1, 0]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_107(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 4, 0, 1, 0, 1, 0, 1, 0]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_108(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 4, 0, 1, 0, 1, 0, 0, 1]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_109(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 4, 0, 1, 0, 1, 0, 0, 1]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_110(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 4, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_111(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 4, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_112(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 4, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_113(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 4, 0, 1, 0, 0, 1, 0, 1]
        assert game.store == [20, 16]
        assert cond is None
        gstate.cond = cond

    def test_round_6_move_114(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.blocked == [F, F, F, F, T, T, T, T, T, T, T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [20, 28]
        assert cond.name == "ROUND_WIN"
        gstate.cond = cond

    def test_round_7_setup(self, gstate):
        game = gstate.game
        game.new_game(new_round=True)
        assert game.turn is False
        assert game.board == [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.store == [0, 4]

    def test_round_7_move_1(self, gstate):
        game = gstate.game
        cond = game.move(9)
        assert game.turn is True
        assert game.board == [3, 0, 3, 3, 0, 3, 3, 0, 3, 1, 0, 0, 0, 1, 4, 4, 1, 3, 3, 0, 3, 3, 0, 3]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_2(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [3, 0, 3, 3, 0, 3, 3, 0, 3, 1, 0, 0, 0, 1, 0, 5, 2, 4, 0, 1, 4, 4, 1, 3]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_3(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 0, 3, 0, 1, 4, 0, 1, 4, 2, 0, 0, 1, 1, 0, 5, 2, 4, 0, 1, 4, 4, 1, 3]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_4(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [4, 1, 3, 0, 1, 4, 0, 1, 4, 2, 0, 0, 1, 1, 0, 5, 2, 4, 0, 1, 4, 0, 2, 4]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_5(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 2, 4, 1, 0, 5, 1, 1, 4, 2, 0, 0, 1, 1, 0, 5, 2, 4, 0, 1, 4, 0, 2, 4]
        assert game.store == [0, 4]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_6(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 1, 6, 0, 0, 5, 0, 0, 0, 0, 2, 1, 0, 3, 5, 1, 2, 0, 1, 3, 5]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_7(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 1, 1, 6, 1, 0, 0, 1, 2, 2, 1, 3, 5, 1, 2, 0, 1, 3, 5]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_8(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 0, 0, 1, 1, 6, 1, 0, 0, 1, 2, 2, 1, 0, 6, 2, 0, 1, 2, 0, 6]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_9(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 1, 0, 1, 1, 6, 1, 0, 0, 1, 2, 2, 1, 0, 6, 2, 0, 1, 2, 0, 6]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_10(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 0, 1, 1, 0, 1, 1, 6, 1, 0, 0, 0, 0, 3, 2, 1, 6, 2, 0, 1, 2, 0, 6]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_11(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 0, 1, 1, 0, 1, 0, 0, 2, 0, 0, 1, 1, 4, 2, 2, 7, 2, 1, 1, 2, 0, 6]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_12(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 0, 1, 1, 0, 1, 0, 0, 2, 0, 0, 1, 1, 4, 2, 2, 0, 3, 2, 2, 3, 1, 7]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_13(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 1, 0, 1, 0, 1, 1, 0, 0, 2, 0, 0, 1, 1, 4, 2, 2, 0, 3, 2, 2, 3, 1, 7]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_14(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 1, 0, 1, 0, 2, 1, 0, 2, 0, 0, 1, 0, 0, 3, 3, 1, 4, 0, 3, 4, 0, 8]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_15(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 1, 0, 0, 1, 2, 1, 0, 2, 0, 0, 1, 0, 0, 3, 3, 1, 4, 0, 3, 4, 0, 8]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_16(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 2, 1, 1, 2, 2, 2, 1, 2, 0, 0, 2, 1, 0, 3, 3, 0, 0, 1, 4, 5, 1, 0]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_17(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 2, 3, 1, 0, 3, 0, 3, 2, 0, 0, 0, 2, 2, 1, 0, 4, 1, 1, 0, 5, 0, 2, 1]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_18(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [3, 2, 3, 1, 0, 3, 0, 3, 2, 0, 0, 0, 2, 2, 1, 0, 4, 1, 0, 1, 5, 0, 2, 1]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_19(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [3, 2, 3, 1, 0, 3, 0, 0, 3, 1, 0, 0, 2, 2, 0, 1, 0, 2, 1, 2, 6, 1, 2, 1]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_20(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [4, 2, 0, 2, 1, 4, 1, 0, 3, 1, 0, 0, 2, 2, 0, 1, 0, 2, 1, 2, 6, 0, 0, 2]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_21(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [4, 2, 0, 2, 1, 4, 1, 0, 0, 2, 0, 0, 2, 2, 1, 0, 1, 2, 0, 2, 7, 1, 0, 2]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_22(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [5, 2, 1, 2, 2, 5, 0, 1, 1, 2, 0, 0, 2, 2, 1, 0, 0, 0, 1, 3, 0, 2, 1, 3]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_23(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [5, 2, 1, 2, 2, 5, 0, 0, 0, 3, 0, 0, 2, 2, 0, 1, 1, 0, 1, 3, 0, 2, 1, 3]
        assert game.store == [0, 12]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_24(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [5, 0, 1, 0, 0, 5, 0, 0, 0, 3, 0, 0, 2, 2, 0, 0, 0, 1, 0, 4, 1, 2, 1, 3]
        assert game.store == [0, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_25(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [5, 0, 1, 0, 0, 5, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 1, 0, 4, 1, 2, 1, 3]
        assert game.store == [0, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_26(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [5, 0, 1, 0, 0, 5, 0, 0, 0, 0, 0, 0, 2, 2, 1, 0, 0, 2, 1, 4, 1, 2, 1, 3]
        assert game.store == [0, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_27(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [5, 0, 0, 1, 0, 5, 0, 0, 0, 0, 0, 0, 2, 2, 1, 0, 0, 2, 1, 4, 1, 2, 1, 3]
        assert game.store == [0, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_28(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [6, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 3, 0, 2, 1, 1, 2, 1, 0, 2, 3, 2, 0]
        assert game.store == [0, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_29(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [6, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 4, 1, 2, 1, 1, 2, 1, 0, 2, 3, 2, 0]
        assert game.store == [0, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_30(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 2, 2, 1, 2, 1, 2, 0, 1, 1, 0, 0, 4, 1, 2, 1, 1, 2, 1, 0, 2, 0, 3, 1]
        assert game.store == [0, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_31(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 2, 2, 0, 0, 2, 3, 1, 1, 1, 0, 0, 4, 1, 2, 1, 1, 2, 1, 0, 2, 0, 3, 1]
        assert game.store == [0, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_32(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 2, 0, 0, 2, 3, 1, 1, 1, 0, 0, 4, 1, 2, 1, 1, 2, 1, 0, 2, 0, 3, 0]
        assert game.store == [0, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_33(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 2, 2, 0, 0, 2, 0, 2, 2, 0, 0, 0, 5, 0, 2, 2, 0, 2, 2, 1, 2, 0, 3, 0]
        assert game.store == [0, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_34(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 2, 2, 0, 0, 2, 0, 2, 2, 0, 0, 0, 0, 1, 3, 3, 1, 0, 3, 2, 0, 1, 4, 1]
        assert game.store == [0, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_35(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 3, 1, 1, 2, 0, 2, 2, 0, 0, 0, 0, 1, 3, 3, 1, 0, 3, 0, 0, 1, 4, 1]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_36(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 3, 1, 1, 2, 0, 2, 2, 0, 0, 0, 0, 1, 3, 3, 1, 0, 3, 0, 0, 1, 4, 0]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_37(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 3, 1, 0, 0, 1, 3, 0, 1, 0, 0, 1, 0, 4, 0, 2, 1, 4, 1, 0, 1, 4, 0]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_38(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 3, 1, 0, 0, 1, 3, 0, 1, 0, 0, 1, 0, 4, 0, 2, 1, 4, 0, 1, 1, 4, 0]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_39(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 1, 4, 0, 1, 1, 1, 3, 0, 0, 0, 0, 0, 1, 0, 1, 2, 2, 5, 1, 0, 2, 0, 1]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_40(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 4, 0, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 5, 1, 0, 2, 0, 1]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_41(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 1, 4, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 5, 1, 0, 2, 0, 1]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_42(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 4, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 3, 0, 6, 2, 1, 2, 0, 1]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_43(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 1, 4, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 2, 0, 3, 0, 6, 2, 1, 2, 0, 1]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_44(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 5, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 2, 0, 3, 0, 0, 3, 2, 3, 1, 2]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_45(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 0, 2, 2, 1, 2, 1, 1, 1, 0, 0, 0, 0, 2, 0, 3, 0, 0, 3, 2, 3, 1, 2]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_46(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 0, 2, 2, 1, 2, 1, 1, 1, 0, 0, 0, 0, 2, 0, 3, 0, 0, 3, 2, 0, 2, 3]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_47(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 1, 2, 2, 1, 2, 1, 1, 1, 0, 0, 0, 0, 2, 0, 3, 0, 0, 3, 2, 0, 2, 3]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_48(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 0, 2, 2, 2, 2, 0, 2, 0, 0, 0, 1, 1, 2, 0, 3, 0, 0, 0, 3, 1, 0, 4]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_49(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 1, 2, 2, 2, 2, 0, 2, 0, 0, 0, 1, 1, 2, 0, 3, 0, 0, 0, 3, 1, 0, 4]
        assert game.store == [2, 18]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_50(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 4, 1, 0, 0, 3, 1, 0, 4]
        assert game.store == [2, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_51(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 4, 1, 0, 0, 3, 1, 0, 4]
        assert game.store == [2, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_52(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 1, 4, 0, 1, 0]
        assert game.store == [2, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_53(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 4, 0, 1, 0]
        assert game.store == [4, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_54(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 4, 0, 0, 1]
        assert game.store == [4, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_55(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 1, 0, 0, 2, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 4, 0, 0, 1]
        assert game.store == [4, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_56(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 0, 0, 2, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 4, 0, 0, 1]
        assert game.store == [4, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_57(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 1, 0, 2, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 4, 0, 0, 1]
        assert game.store == [4, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_58(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 1, 1, 0, 2, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 2]
        assert game.store == [4, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_59(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 1, 0, 1, 2, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 2]
        assert game.store == [4, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_60(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [2, 0, 1, 0, 2, 2, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3]
        assert game.store == [4, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_61(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [2, 0, 1, 0, 2, 2, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3]
        assert game.store == [4, 30]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_62(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_63(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_64(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 3]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_65(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 3]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_66(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_67(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_68(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_69(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 2, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_70(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 2, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_71(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_72(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_73(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_74(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_75(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_76(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_77(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_78(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_79(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_80(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_81(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_82(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_83(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_84(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_85(self, gstate):
        game = gstate.game
        cond = game.move(2)
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_86(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_87(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_88(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_89(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_90(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 2, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_91(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 2, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_92(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_93(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_94(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_95(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_96(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_97(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_98(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_99(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_100(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_101(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_102(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_103(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_104(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_105(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_106(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_107(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 1, 0, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_108(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 0, 1, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_109(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 0, 1, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_110(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 1, 1, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_111(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 1, 1, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_112(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 1, 1, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_113(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 1, 1, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_114(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_115(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_116(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_117(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_118(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_119(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_120(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_121(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_122(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_123(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_124(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [4, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_125(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 2, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [6, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_126(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [6, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_127(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert game.store == [6, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_128(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [6, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_129(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [6, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_130(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [6, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_131(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        assert game.store == [6, 36]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_132(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_133(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_134(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_135(self, gstate):
        game = gstate.game
        cond = game.move(0)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_136(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_137(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_138(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_139(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_140(self, gstate):
        game = gstate.game
        cond = game.move(2)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_141(self, gstate):
        game = gstate.game
        cond = game.move(3)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_142(self, gstate):
        game = gstate.game
        cond = game.move(10)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_143(self, gstate):
        game = gstate.game
        cond = game.move(4)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_144(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_145(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_146(self, gstate):
        game = gstate.game
        cond = game.move(1)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_147(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_148(self, gstate):
        game = gstate.game
        cond = game.move(6)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_149(self, gstate):
        game = gstate.game
        cond = game.move(7)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_150(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_151(self, gstate):
        game = gstate.game
        cond = game.move(8)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_152(self, gstate):
        game = gstate.game
        cond = game.move(5)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is False
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_153(self, gstate):
        game = gstate.game
        cond = game.move(9)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.turn is True
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert game.store == [6, 38]
        assert cond is None
        gstate.cond = cond

    def test_round_7_move_154(self, gstate):
        game = gstate.game
        cond = game.move(11)
        # assert game.mdata.board[game.mdata.sow_loc] != 2
        assert game.mdata.winner is True     # manual change
        assert game.board == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert game.store == [6, 42]
        assert game.blocked == [F, F, F, F, F, F, F, F, F, F, T, T, F, F, F, F, F, F, F, F, F, F, F, F]
        assert game.unlocked == [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T]
        assert game.child == [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
        assert cond.name == "WIN"
        gstate.cond = cond
