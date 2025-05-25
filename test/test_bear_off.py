# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 13:38:20 2025

@author: annda
"""


import dataclasses as dc

import pytest
pytestmark = pytest.mark.unittest

from context import game_constants as gconsts
from context import game_interface as gi
from context import mancala
from context import bear_off

import utils


# %%

TEST_COVERS = ['src\\bear_off.py']

# %% constants

T = True
F = False
N = None

WIN = gi.WinCond.WIN
TIE = gi.WinCond.TIE


# %%

class TestGameState:

    def test_state(self):

        with pytest.raises(TypeError):
            bear_off.BearOffState()

        state1 = bear_off.BearOffState(board='a board tuple',
                                       store=(3, 4),
                                       mcount=5,
                                       _turn=True)
        assert state1.board == 'a board tuple'
        assert state1.store == (3, 4)
        assert state1.mcount == 5
        assert state1._turn is True
        assert state1.normal_sow

        state2 = bear_off.BearOffState(board='a board tuple',
                                       store=(3, 4),
                                       mcount=5,
                                       _turn=False,
                                       normal_sow=False)
        assert state2.turn is False            # test via the property
        assert not state2.normal_sow

        assert state1 != state2

        state1 = bear_off.BearOffState(board='a board tuple',
                                       store=(3, 4),
                                       mcount=5,
                                       _turn=False,
                                       normal_sow=False)
        assert state1 == state2
        assert state1 is not state2
        assert hash(state1) == hash(state2)

        with pytest.raises(dc.FrozenInstanceError):
            state1.store = (5, 6)


    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                goal=gi.Goal.CLEAR,
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=bear_off.BearOff.rules)

        game = bear_off.BearOff(game_consts, game_info)
        game.turn = False
        return game


    def test_get_state(self, game):

        state = game.state
        assert state.board == (2, 2, 2, 2, 2, 2)
        assert state.store == (0, 0)
        assert state.normal_sow is True

        game.board = [1, 2, 3, 4, 5 ,6]
        game.store = [12, 12]
        game.normal_sow = False

        state = game.state
        assert state.board == (1, 2, 3, 4, 5, 6)
        assert state.store == (12, 12)
        assert state.normal_sow is False


    def test_set_state(self, game):

        assert game.board == [2, 2, 2, 2, 2, 2]
        assert game.store == [0, 0]
        assert game.turn is False
        assert game.normal_sow is True

        state = bear_off.BearOffState(board=(3, 1, 4, 1, 5, 9),
                                      store=(3, 4),
                                      mcount=5,
                                      _turn=False,
                                      normal_sow=False)
        game.state = state
        assert game.board == [3, 1, 4, 1, 5, 9]
        assert game.store == [3, 4]
        assert game.turn is False
        assert game.normal_sow is False


    def test_get_bstate(self, game):

        state = game.board_state
        assert state.board == (2, 2, 2, 2, 2, 2)
        assert state.store == (0, 0)
        assert state.normal_sow is True


class TestGameExtensions:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(capt_on=[3],
                                stores=True,
                                goal=gi.Goal.CLEAR,
                                nbr_holes=game_consts.holes,
                                rules=bear_off.BearOff.rules)

        game = bear_off.BearOff(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def dgame(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(capt_on=[3],
                                stores=True,
                                goal=gi.Goal.DEPRIVE,
                                nbr_holes=game_consts.holes,
                                rules=bear_off.BearOff.rules)

        game = bear_off.BearOff(game_consts, game_info)
        game.turn = False
        return game


    @pytest.fixture
    def mgame(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(capt_on=[3],
                                stores=True,
                                goal=gi.Goal.MAX_SEEDS,
                                nbr_holes=game_consts.holes,
                                rules=bear_off.BearOff.rules)

        game = bear_off.BearOff(game_consts, game_info)
        game.turn = False
        return game


    def test_new_game(self, game, mocker):
        """Confirm mancala implementation is called
        and that normal_sow is cleared to True"""

        assert game.normal_sow is True
        game.normal_sow = False

        mobj = mocker.patch('mancala.Mancala.new_game')
        game.new_game()
        mobj.assert_called_once()
        assert game.normal_sow is True

    # all tests are on False's turn
    # either player may win on either turn in clear games
    END_CASES =  [   # start with a bunch of general combinations
                     # all with seeds on both sides
                  ['game', board, nsow, rturn, ended,
                   gi.WinCond.TIE if ended else None, None]
                  for board in [[2] * 6, [1] * 6, [1, 0] * 3]
                  for nsow in [False, True]
                  for rturn in [False, True]   # rturn not used, no effect
                  for ended in [False, True]
                  ]

    END_CASES += [
        # False cleared their seeds (both normal_sow and not)
        ['game', [0, 0, 0, 1, 2, 0], True, False, False, WIN, False],
        ['game', [0, 0, 0, 1, 2, 0], False, False, False, WIN, False],

        # True's seeds cleared  (both normal_sow and not)
        ['game', [1, 2, 0, 0, 0, 0], True, False, False, WIN, True],
        ['game', [1, 2, 0, 0, 0, 0], False, False, False, WIN, True],
        ]

    END_CASES += [
        # False cleared their seeds (both normal_sow and not)
        ['dgame', [0, 0, 0, 1, 2, 0], True, False, False, WIN, True],
        ['dgame', [0, 0, 0, 1, 2, 0], False, False, False, WIN, True],

        # True has no seeds to play  (both normal_sow and not)
        ['dgame', [1, 2, 0, 0, 0, 0], True, False, False, WIN, False],
        ['dgame', [1, 2, 0, 0, 0, 0], False, False, False, WIN, False],
        ]

    END_CASES += [
        # does not use the BearOff ender
        ['mgame', [0, 0, 2, 0, 2, 0], True, False, False, WIN, False],

        ]

    @pytest.mark.parametrize('game_fixt, '
                             'board, normal_sow, repeat_turn, ended, '
                             'econd, ewinner',
                             END_CASES)
    def test_ender(self, request, game_fixt,
                   board, normal_sow, repeat_turn, ended,
                   econd, ewinner):

        game = request.getfixturevalue(game_fixt)
        game.board = board
        game.store[0] = game.cts.total_seeds - sum(board)
        game.normal_sow = normal_sow
        # print(game)

        mdata = utils.make_ender_mdata(game, repeat_turn, ended)
        game.deco.ender.game_ended(mdata)
        # print(mdata.win_cond, mdata.winner)
        assert mdata.win_cond == econd
        assert mdata.winner == ewinner


    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('board, esow',
                             [[[2, 2, 2, 2, 2, 2], True],
                              [[1, 0, 2, 0, 0, 1], True],
                              [[1, 0, 1, 0, 0, 1], False],
                              [[1, 1, 1, 1, 1, 1], False],
                              ])
    def test_sow_change(self, game, board, esow):
        """Confirm mode change based on board at start of sow."""

        game.board = board
        game.store[0] = game.cts.total_seeds - sum(board)
        # print(game)

        game.move(0)
        assert game.normal_sow == esow


    # @pytest.mark.usefixtures("logger")
    def test_sow_no_reset(self, game):
        """Confirm once the normal_sow state changes, it is
        not reset if the baoard goes back to other conditions"""

        assert game.normal_sow is True

        game.board = [1, 1, 1, 1, 1, 1]
        game.store = [6, 0]
        # print("pre move 1:\n", game)

        game.move(0)
        assert game.normal_sow is False
        assert game.board == [0, 2, 1, 1, 1, 1]
        assert game.store == [6, 0]

        game.turn = True
        # print("pre move 2:\n", game)
        game.move(0)
        assert game.normal_sow is False
        assert game.board == [0, 2, 1, 1, 1, 0]
        assert game.store == [6, 1]


    MCASES = [
        # normal sow
        [[1, 0, 2, 0, 0, 1], [8, 0], 0, False,
         [0, 1, 2, 0, 0, 1], [8, 0], None, None],

        [[1, 0, 1, 0, 0, 1], [9, 0], 2, False,
         [1, 0, 0, 0, 0, 1], [10, 0], None, None],

        [[1, 0, 0, 0, 0, 1], [10, 0], 0, True,
         [1, 0, 0, 0, 0, 0], [10, 1], WIN, True],

        [[0, 0, 1, 0, 1, 0], [10, 0], 2, False,
         [0, 0, 0, 0, 1, 0], [11, 0], WIN, False],
        ]

    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize('board, store, move, turn, '
                             'eboard, estore, econd, ewin',
                             MCASES)
    def test_move(self, game, board, store, move, turn,
                  eboard, estore, econd, ewin):
        """Game is not a multilap sow game."""

        game.normal_sow = False
        game.board = board
        game.store = store
        game.turn = turn
        # print(game)

        cond = game.move(move)

        assert cond == econd
        if ewin is not None:
            assert game.turn == ewin

        assert game.board == eboard
        assert game.store == estore
