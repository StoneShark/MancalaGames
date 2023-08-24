# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 19:21:23 2023

@author: Ann
"""

# TODO test win_conditions with children

# %% imports

import sys

import pytest

sys.path.extend(['src'])

import game_interface as gi
from game_interface import WinCond
from game_interface import GameFlags
from game_interface import Direct

import game_constants as gc
import mancala
import utils


# %%

class TestBasicWConds:

    @pytest.fixture
    def ccw_game(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.CCW,
                                                evens=True),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_no_win(self, ccw_game):
        ccw_game.board = utils.build_board([0, 2, 1],
                                           [0, 2, 0])
        ccw_game.store = [3, 4]
        ccw_game.turn = True

        assert not ccw_game.win_conditions()
        assert ccw_game.get_turn()
        assert ccw_game.board == utils.build_board([0, 2, 1],
                                                   [0, 2, 0])
        assert ccw_game.store == [3, 4]

    def test_tt_win(self, ccw_game):
        # true win on true turn, playable, no pass
        ccw_game.board = utils.build_board([1, 0, 0],
                                           [0, 0, 1])
        ccw_game.store = [2, 8]
        ccw_game.turn = True

        assert ccw_game.win_conditions() == WinCond.WIN
        assert ccw_game.get_turn()
        assert ccw_game.board == utils.build_board([1, 0, 0],
                                                   [0, 0, 1])
        assert ccw_game.store == [2, 8]

    def test_ft_win(self, ccw_game):
        # true win on false turn, playable, no pass
        ccw_game.board = utils.build_board([1, 0, 0],
                                           [0, 0, 1])
        ccw_game.store = [2, 8]
        ccw_game.turn = False

        assert ccw_game.win_conditions() == WinCond.WIN
        assert ccw_game.get_turn()
        assert ccw_game.board == utils.build_board([1, 0, 0],
                                                   [0, 0, 1])
        assert ccw_game.store == [2, 8]

    def test_ff_win(self, ccw_game):
        # false win on false turn, playable, no pass
        ccw_game.board = utils.build_board([1, 0, 0],
                                           [0, 0, 1])
        ccw_game.store = [8, 2]
        ccw_game.turn = False

        assert ccw_game.win_conditions() == WinCond.WIN
        assert not ccw_game.get_turn()
        assert ccw_game.board == utils.build_board([1, 0, 0],
                                                   [0, 0, 1])
        assert ccw_game.store == [8, 2]

    def test_tf_win(self, ccw_game):
        # false win on true turn, playable, no pass
        ccw_game.board = utils.build_board([1, 0, 0],
                                           [0, 0, 1])
        ccw_game.store = [8, 2]
        ccw_game.turn = True

        assert ccw_game.win_conditions() == WinCond.WIN
        assert not ccw_game.get_turn()
        assert ccw_game.board == utils.build_board([1, 0, 0],
                                                   [0, 0, 1])
        assert ccw_game.store == [8, 2]

    def test_f_tie_win(self, ccw_game):
        # tie  on false turn, playable, no pass
        ccw_game.board = utils.build_board([0, 0, 0],
                                           [0, 0, 0])
        ccw_game.store = [6, 6]
        ccw_game.turn = False

        assert ccw_game.win_conditions() == WinCond.TIE
        assert ccw_game.board == utils.build_board([0, 0, 0],
                                                   [0, 0, 0])
        assert ccw_game.store == [6, 6]

    def test_t_tie_win(self, ccw_game):
        # tie on false turn, playable, no pass
        ccw_game.board = utils.build_board([0, 0, 0],
                                           [0, 0, 0])
        ccw_game.store = [6, 6]
        ccw_game.turn = True

        assert ccw_game.win_conditions() == WinCond.TIE
        assert ccw_game.board == utils.build_board([0, 0, 0],
                                                   [0, 0, 0])
        assert ccw_game.store == [6, 6]

    def test_t_nopass_win(self, ccw_game):
        # true's turn ended, false has no moves, no pass
        ccw_game.board = utils.build_board([5, 0, 0],
                                           [0, 0, 0])
        ccw_game.store = [3, 4]
        ccw_game.turn = True

        assert ccw_game.win_conditions() == WinCond.WIN
        assert ccw_game.get_turn()
        assert ccw_game.board == utils.build_board([0, 0, 0],
                                                   [0, 0, 0])
        assert ccw_game.store == [3, 9]
        assert not ccw_game.test_pass()

    def test_f_nopass_win(self, ccw_game):
        # false's turn ended, true has no moves, no pass
        ccw_game.board = utils.build_board([0, 0, 0],
                                           [0, 0, 5])
        ccw_game.store = [3, 4]
        ccw_game.turn = False

        assert ccw_game.win_conditions() == WinCond.WIN
        assert not ccw_game.get_turn()
        assert ccw_game.board == utils.build_board([0, 0, 0],
                                                   [0, 0, 0])
        assert ccw_game.store == [8, 4]
        assert not ccw_game.test_pass()

    def test_t_repeat_win(self, ccw_game):
        ccw_game.board = utils.build_board([5, 0, 0],
                                           [0, 0, 0])
        ccw_game.store = [3, 4]
        ccw_game.turn = True

        assert ccw_game.win_conditions(repeat_turn=True) is None
        assert ccw_game.get_turn()
        assert ccw_game.board == utils.build_board([5, 0, 0],
                                                   [0, 0, 0])
        assert ccw_game.store == [3, 4]

    def test_f_repeat_win(self, ccw_game):
        ccw_game.board = utils.build_board([0, 0, 0],
                                           [0, 0, 5])
        ccw_game.store = [3, 4]
        ccw_game.turn = False

        assert ccw_game.win_conditions(repeat_turn=True) is None
        assert not ccw_game.get_turn()
        assert ccw_game.board == utils.build_board([0, 0, 0],
                                                   [0, 0, 5])
        assert ccw_game.store == [3, 4]


class TestRoundsWConds:

    @pytest.fixture
    def rgame(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,

                                flags=GameFlags(sow_direct=Direct.CCW,
                                                rounds=True,
                                                blocks=True,
                                                evens=True),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_tt_win(self, rgame):
        rgame.board = utils.build_board([1, 0, 0],
                                        [0, 0, 1])
        rgame.store = [2, 8]
        rgame.turn = True

        assert rgame.win_conditions() == WinCond.ROUND_WIN
        assert rgame.get_turn()
        assert rgame.board == utils.build_board([1, 0, 0],
                                                [0, 0, 1])
        assert rgame.store == [2, 8]

    def test_ft_win(self, rgame):
        rgame.board = utils.build_board([1, 0, 0],
                                        [0, 0, 1])
        rgame.store = [2, 8]
        rgame.turn = False

        assert rgame.win_conditions() == WinCond.ROUND_WIN
        assert rgame.get_turn()
        assert rgame.board == utils.build_board([1, 0, 0],
                                                [0, 0, 1])
        assert rgame.store == [2, 8]

    def test_ff_win(self, rgame):
        rgame.board = utils.build_board([1, 0, 0],
                                        [0, 0, 1])
        rgame.store = [8, 2]
        rgame.turn = False

        assert rgame.win_conditions() == WinCond.ROUND_WIN
        assert not rgame.get_turn()
        assert rgame.board == utils.build_board([1, 0, 0],
                                                [0, 0, 1])
        assert rgame.store == [8, 2]

    def test_tf_win(self, rgame):
        rgame.board = utils.build_board([1, 0, 0],
                                        [0, 0, 1])
        rgame.store = [8, 2]
        rgame.turn = True

        assert rgame.win_conditions() == WinCond.ROUND_WIN
        assert not rgame.get_turn()
        assert rgame.board == utils.build_board([1, 0, 0],
                                                [0, 0, 1])
        assert rgame.store == [8, 2]

    def test_f_tie_win(self, rgame):
        # tie  on false turn, playable, no pass
        rgame.board = utils.build_board([0, 0, 0],
                                        [0, 0, 0])
        rgame.store = [6, 6]
        rgame.turn = False

        assert rgame.win_conditions() == WinCond.ROUND_TIE
        assert rgame.board == utils.build_board([0, 0, 0],
                                                [0, 0, 0])
        assert rgame.store == [6, 6]

    def test_t_tie_win(self, rgame):
        rgame.board = utils.build_board([0, 0, 0],
                                        [0, 0, 0])
        rgame.store = [6, 6]
        rgame.turn = True

        assert rgame.win_conditions() == WinCond.ROUND_TIE
        assert rgame.board == utils.build_board([0, 0, 0],
                                                [0, 0, 0])
        assert rgame.store == [6, 6]


class TestPassWConds:

    @pytest.fixture
    def pass_game(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.CCW,
                                                mustpass=True,
                                                evens=True),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_nopass_win(self, pass_game):
        # true's turn ended, false has moves
        pass_game.board = utils.build_board([0, 2, 1],
                                            [0, 2, 0])
        pass_game.store = [3, 4]
        pass_game.turn = True

        assert not pass_game.win_conditions()
        assert pass_game.get_turn()
        assert pass_game.board == utils.build_board([0, 2, 1],
                                                    [0, 2, 0])
        assert pass_game.store == [3, 4]

        pass_game.turn = False    # move does this, after win_cond

        assert not pass_game.test_pass()
        assert not pass_game.get_turn()

    def test_t_pass_win(self, pass_game):
        # true's turn ended, false has no moves
        pass_game.board = utils.build_board([2, 2, 1],
                                            [0, 0, 0])
        pass_game.store = [3, 4]
        pass_game.turn = True

        assert not pass_game.win_conditions()
        assert pass_game.get_turn()
        assert pass_game.board == utils.build_board([2, 2, 1],
                                                    [0, 0, 0])
        assert pass_game.store == [3, 4]

        pass_game.turn = False    # move does this, after win_cond

        assert pass_game.test_pass()
        assert pass_game.get_turn()

    def test_f_pass_win2(self, pass_game):
        # false's turn ended, true has no moves
        pass_game.board = utils.build_board([0, 0, 0],
                                            [2, 2, 1])
        pass_game.store = [3, 4]
        pass_game.turn = False

        assert not pass_game.win_conditions()
        assert not pass_game.get_turn()
        assert pass_game.board == utils.build_board([0, 0, 0],
                                                    [2, 2, 1])
        assert pass_game.store == [3, 4]

        assert pass_game.move(mancala.PASS_TOKEN) is None
        assert pass_game.get_turn()

    def test_t_gover_win(self, pass_game):
        pass_game.board = utils.build_board([0, 0, 0],
                                            [0, 0, 0])
        pass_game.store = [4, 8]
        pass_game.turn = True

        assert pass_game.win_conditions() == WinCond.WIN
        assert pass_game.get_turn()
        assert pass_game.board == utils.build_board([0, 0, 0],
                                                    [0, 0, 0])
        assert pass_game.store == [4, 8]

    def test_f_gover_win(self, pass_game):
        pass_game.board = utils.build_board([0, 0, 0],
                                            [0, 0, 0])
        pass_game.store = [4, 8]
        pass_game.turn = False

        assert pass_game.win_conditions() == WinCond.WIN
        assert pass_game.get_turn()
        assert pass_game.board == utils.build_board([0, 0, 0],
                                                    [0, 0, 0])
        assert pass_game.store == [4, 8]


class TestMustShareWConds:

    @pytest.fixture
    def msgame(self):
        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.CCW,
                                                mustshare=True,
                                                evens=True),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_no_win(self, msgame):
        msgame.board = utils.build_board([2, 3, 0],
                                         [0, 4, 1])
        msgame.store = [2, 2]
        msgame.turn = False

        assert not msgame.win_conditions()
        assert not msgame.get_turn()
        assert msgame.board == utils.build_board([2, 3, 0],
                                                 [0, 4, 1])
        assert msgame.store == [2, 2]
        assert msgame.get_allowable_holes() == [False, True, True]

    def test_tie(self, msgame):
        msgame.board = utils.build_board([0, 0, 0],
                                         [0, 0, 0])
        msgame.store = [6, 6]
        msgame.turn = False

        assert msgame.win_conditions() == WinCond.TIE
        assert msgame.board == utils.build_board([0, 0, 0],
                                                 [0, 0, 0])
        assert msgame.store == [6, 6]

    def test_t_can_win(self, msgame):
        # false ended with no moves, but true can share
        # win_cond is called before the turn is flipped
        msgame.board = utils.build_board([5, 0, 0],
                                         [0, 0, 0])
        msgame.store = [3, 4]
        msgame.turn = False

        assert not msgame.win_conditions()
        assert not msgame.get_turn()
        assert msgame.board == utils.build_board([5, 0, 0],
                                                 [0, 0, 0])
        assert msgame.store == [3, 4]

    def test_f_can_win(self, msgame):
        # true ended with no moves, but false can share
        msgame.board = utils.build_board([0, 0, 0],
                                         [0, 0, 5])
        msgame.store = [3, 4]
        msgame.turn = True

        assert not msgame.win_conditions()
        assert msgame.get_turn()
        assert msgame.board == utils.build_board([0, 0, 0],
                                                 [0, 0, 5])
        assert msgame.store == [3, 4]

    def test_t_cant_win(self, msgame):
        # false ended with no moves and true can't share
        msgame.board = utils.build_board([0, 0, 2],
                                         [0, 0, 0])
        msgame.store = [5, 5]
        msgame.turn = False

        assert msgame.win_conditions() == WinCond.WIN
        assert msgame.get_turn()
        assert msgame.board == utils.build_board([0, 0, 0],
                                                 [0, 0, 0])
        assert msgame.store == [5, 7]

    def test_f_cant_win(self, msgame):
        # true ended with no moves and false can't share
        msgame.board = utils.build_board([0, 0, 0],
                                         [2, 0, 0])
        msgame.store = [5, 5]
        msgame.turn = True

        assert msgame.win_conditions() == WinCond.WIN
        assert not msgame.get_turn()
        assert msgame.board == utils.build_board([0, 0, 0],
                                                 [0, 0, 0])
        assert msgame.store == [7, 5]

    def test_t_can_winr(self, msgame):
        # false ended with no moves, but repeat turn
        msgame.board = utils.build_board([5, 0, 0],
                                         [0, 0, 0])
        msgame.store = [3, 4]
        msgame.turn = False

        assert msgame.win_conditions(repeat_turn=True) == WinCond.WIN
        assert msgame.get_turn()
        assert msgame.board == utils.build_board([0, 0, 0],
                                                 [0, 0, 0])
        assert msgame.store == [3, 9]

    def test_f_can_winr(self, msgame):
        # true ended with no moves, but repeat turn
        msgame.board = utils.build_board([0, 0, 0],
                                         [0, 0, 5])
        msgame.store = [3, 4]
        msgame.turn = True

        assert msgame.win_conditions(repeat_turn=True) == WinCond.WIN
        assert not msgame.get_turn()
        assert msgame.board == utils.build_board([0, 0, 0],
                                                 [0, 0, 0])
        assert msgame.store == [8, 4]

    def test_t_cant_winr(self, msgame):
        # false ended with no moves and true can't share
        msgame.board = utils.build_board([0, 0, 2],
                                         [0, 0, 0])
        msgame.store = [5, 5]
        msgame.turn = False

        assert msgame.win_conditions(repeat_turn=True) == WinCond.WIN
        assert msgame.get_turn()
        assert msgame.board == utils.build_board([0, 0, 0],
                                                 [0, 0, 0])
        assert msgame.store == [5, 7]

    def test_f_cant_winr(self, msgame):
        # true ended with no moves and false can't share
        msgame.board = utils.build_board([0, 0, 0],
                                         [2, 0, 0])
        msgame.store = [5, 5]
        msgame.turn = True

        assert msgame.win_conditions(repeat_turn=True) == WinCond.WIN
        assert not msgame.get_turn()
        assert msgame.board == utils.build_board([0, 0, 0],
                                                 [0, 0, 0])
        assert msgame.store == [7, 5]
