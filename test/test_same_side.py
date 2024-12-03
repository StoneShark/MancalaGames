# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 06:34:51 2024

@author: Ann"""

import dataclasses as dc

import pytest
pytestmark = pytest.mark.unittest

from context import game_constants as gc
from context import game_interface as gi
from context import ginfo_rules
from context import incrementer
from context import mancala
from context import same_side


# %%

TEST_COVERS = ['src\\same_side.py']

# %% constants

T = True
F = False
N = None

# %%

class TestGameState:

    def test_state(self):

        with pytest.raises(TypeError):
            same_side.SSGameState()

        state1 = same_side.SSGameState(board='a board tuple',
                                      store=(3, 4),
                                      mcount=5,
                                      _turn=True)
        assert state1.board == 'a board tuple'
        assert state1.store == (3, 4)
        assert state1.mcount == 5
        assert state1._turn == True
        assert state1.empty_store == False

        state2 = same_side.SSGameState(board='a board tuple',
                                      store=(3, 4),
                                      mcount=5,
                                      _turn=False,
                                      empty_store=True)
        assert state2.turn == False            # test via the property
        assert state2.empty_store == True

        assert state1 != state2

        state1 = same_side.SSGameState(board='a board tuple',
                                      store=(3, 4),
                                      mcount=5,
                                      _turn=False,
                                      empty_store=True)
        assert state1 == state2
        assert state1 is not state2
        assert hash(state1) == hash(state2)

        with pytest.raises(dc.FrozenInstanceError):
            state1.store = (5, 6)


    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                goal=3,
                                no_sides=True,
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=same_side.SameSide.rules)

        game = same_side.SameSide(game_consts, game_info)
        game.turn = False
        return game


    def test_get_state(self, game):

        state = game.state
        assert state.board == (2, 2, 2, 2, 2, 2)
        assert state.store == (0, 0)
        assert state.empty_store is False

        game.board = [1, 2, 3, 4, 5 ,6]
        game.store = [12, 12]
        game.empty_store = True

        state = game.state
        assert state.board == (1, 2, 3, 4, 5, 6)
        assert state.store == (12, 12)
        assert state.empty_store is True


    def test_set_state(self, game):

        assert game.board == [2, 2, 2, 2, 2, 2]
        assert game.store == [0, 0]
        assert game.turn is False
        assert game.empty_store is False

        state = same_side.SSGameState(board=(3, 1, 4, 1, 5, 9),
                                      store=(3, 4),
                                      mcount=5,
                                      _turn=False,
                                      empty_store=True)
        game.state = state
        assert game.board == [3, 1, 4, 1, 5, 9]
        assert game.store == [3, 4]
        assert game.turn is False
        assert game.empty_store is True


class TestBoardSideIncr:
    """Test for TestBoardSideIncr and fix_incr_deco."""

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=5)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=3,
                                no_sides=True,
                                skip_start=True,
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=same_side.SameSide.rules)

        game = same_side.SameSide(game_consts, game_info)
        game.turn = False
        return game

    def test_bsincr(self, game):

        incr = same_side.BoardSideIncr(game)

        assert incr.incr(0, gi.Direct.CW) == 4
        assert incr.incr(1, gi.Direct.CW) == 0
        assert incr.incr(2, gi.Direct.CW) == 1
        assert incr.incr(3, gi.Direct.CW) == 2
        assert incr.incr(4, gi.Direct.CW) == 3
        assert incr.incr(5, gi.Direct.CW) == 4   # an invalid input, but ok

        assert incr.incr(0, gi.Direct.CCW) == 1
        assert incr.incr(1, gi.Direct.CCW) == 2
        assert incr.incr(2, gi.Direct.CCW) == 3
        assert incr.incr(3, gi.Direct.CCW) == 4
        assert incr.incr(4, gi.Direct.CCW) == 0
        assert incr.incr(5, gi.Direct.CCW) == 1 # an invalid input, but ok

        game.turn = True
        assert incr.incr(5, gi.Direct.CW) == 9
        assert incr.incr(6, gi.Direct.CW) == 5
        assert incr.incr(7, gi.Direct.CW) == 6
        assert incr.incr(8, gi.Direct.CW) == 7
        assert incr.incr(9, gi.Direct.CW) == 8
        assert incr.incr(1, gi.Direct.CW) == 5   # an invalid input, but ok

        assert incr.incr(5, gi.Direct.CCW) == 6
        assert incr.incr(6, gi.Direct.CCW) == 7
        assert incr.incr(7, gi.Direct.CCW) == 8
        assert incr.incr(8, gi.Direct.CCW) == 9
        assert incr.incr(9, gi.Direct.CCW) == 5
        assert incr.incr(3, gi.Direct.CCW) == 9 # an invalid input, but ok


    def test_deco_1(self, game):
        """A 'fragile' test--if mancala incr deco chain is changed
        this test will likely fail.
        But it exercises the while loop in fix_incr_deco.
        All other game fixtures, test the single incrementer."""

        assert isinstance(game.deco.incr, incrementer.IncPastStart)
        assert isinstance(game.deco.incr.decorator, same_side.BoardSideIncr)


    def test_deco_2(self):
        """Another fragile test, use an invalid game (don't check rules)
        to create a deco chain of length 2."""

        game_consts = gc.GameConsts(nbr_start=2, holes=5)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=3,
                                no_sides=True,
                                skip_start=True,
                                blocks=True,            # this is not valid
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())  # empty rule dict

        game = same_side.SameSide(game_consts, game_info)

        assert isinstance(game.deco.incr, incrementer.IncPastBlocks)
        assert isinstance(game.deco.incr.decorator, incrementer.IncPastStart)
        assert isinstance(game.deco.incr.decorator.decorator,
                          same_side.BoardSideIncr)


    def test_bad_deco(self, mocker):
        """Patch the deco chain creator to make only a BoardSideIncr.
        Which is fine deco, but when fix_incr_deco is called
        it will not find incrementer.Increment.
        The assert will fail!"""

        mobj = mocker.patch('incrementer.deco_incrementer')

        # bad param but we wont cause it to be used
        mobj.return_value = same_side.BoardSideIncr(None)

        game_consts = gc.GameConsts(nbr_start=2, holes=5)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=3,
                                no_sides=True,
                                skip_start=True,
                                blocks=True,            # this is not valid
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())  # empty rule dict

        with pytest.raises(AssertionError):
            same_side.SameSide(game_consts, game_info)


class TestSameSide:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=4)
        game_info = gi.GameInfo(capt_on=[3],
                                stores=True,
                                goal=3,
                                no_sides=True,
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=same_side.SameSide.rules)

        game = same_side.SameSide(game_consts, game_info)
        game.turn = False
        return game


    def test_new_game(self, game, mocker):
        """Confirm mancala implementation is called
        and that empty_store is cleared to False"""

        assert game.empty_store is False
        game.empty_store = True

        mobj = mocker.patch('mancala.Mancala.new_game')
        game.new_game()
        mobj.assert_called_once()
        assert game.empty_store is False


    def test_end_game(self, game, mocker):
        """Confirm mancala implementation is called
        and that empty_store is cleared to False"""

        assert game.empty_store is False
        game.empty_store = True

        mobj = mocker.patch('mancala.Mancala.end_game')
        game.end_game()
        mobj.assert_called_once()
        assert game.empty_store is False


    def test_allow(self, game, mocker):
        """When in empty_store move, don't call mancala.
        When not, do call mancala (parent class implementation)."""

        mobj = mocker.patch('mancala.Mancala.get_allowable_holes')
        mobj.return_value = [T] * 8

        game.empty_store = True
        game.turn = True
        result = game.get_allowable_holes()
        mobj.assert_not_called()
        assert result == [T, T, T, T, F, F, F, F]   # select opp hole: false side

        game.turn = False
        result = game.get_allowable_holes()
        mobj.assert_not_called()
        assert result == [F, F, F, F, T, T, T, T]

        game.empty_store = False
        game.turn = False
        result = game.get_allowable_holes()
        mobj.assert_called_once()
        assert result == [T, T, T, T, F, F, F, F]   # only allow own side holes

        game.turn = True
        mobj.return_value = [T] * 8           # reset, previous call changed it
        result = game.get_allowable_holes()
        assert result == [F, F, F, F, T, T, T, T]   # only allow own side holes


    def test_no_capture(self, game, mocker):
        """Check delegation to parent Mancala class and no captures."""

        mobj = mocker.patch('mancala.Mancala.capture_seeds')

        mdata = mancala.MoveData(game, 2)
        mdata.capt_loc = 3

        game.capture_seeds(mdata)
        assert not mdata.captured
        assert not mdata.capt_changed
        mobj.assert_called_once()


    def test_capture(self, game, mocker):
        """Do a single capture, confirm post proc was done."""

        game.board = [0, 1, 2, 3, 4, 5, 6, 7]
        mdata = mancala.MoveData(game, 0)
        mdata.capt_loc = 3

        game.capture_seeds(mdata)
        # normal stuff done by mancala.Mancala.capture_seeds
        assert not mdata.capt_changed
        assert game.board == [0, 1, 2, 0, 4, 5, 6, 7]
        assert game.store == [3, 0]
        # post proc stuff
        assert mdata.captured == gi.WinCond.REPEAT_TURN
        assert game.empty_store


    def test_del_move(self, game, mocker):
        """mancala.Mancala.move is called"""

        mobj = mocker.patch('mancala.Mancala.move')
        game.move((0, 3, None))
        mobj.assert_called_once()


    def test_not_del_move(self, game, mocker):
        """mancala.Mancala.move is NOT called"""

        mobj = mocker.patch('mancala.Mancala.move')
        game.empty_store = True
        game.move((0, 3, None))
        mobj.assert_not_called()


    # move is (row--not turn, pos, None)

    MCASES = [

        # Mancala.move -- nothing special move
        ([1, 3, 2, 2, 2, 2, 2, 2], [0, 0], (1, 2, None), False, False,
         [2, 3, 0, 3, 2, 2, 2, 2], [0, 0], None, True),

        # Mancala.move -- move with capture
        ([2, 2, 2, 2, 2, 2, 2, 2], [0, 0], (1, 2, None), False, False,
         [0, 2, 0, 3, 2, 2, 2, 2], [3, 0], gi.WinCond.REPEAT_TURN, False),

        # Mancala.move -- win by false
        ([0, 0, 1, 2, 5, 2, 4, 2], [0, 0], (1, 2, None), False, False,
         [0, 0, 0, 0, 5, 2, 4, 2], [3, 0], gi.WinCond.WIN, False),

        # Mancala.move -- win by true
        ([5, 2, 4, 2, 0, 0, 1, 2], [0, 0], (0, 1, None), True, False,
         [5, 2, 4, 2, 0, 0, 0, 0], [0, 3], gi.WinCond.WIN, True),

        # SameSide.move -- seeds moved from store & turn changed
        ([0, 2, 0, 3, 2, 2, 2, 2], [3, 0], (0, 3, None), False, True,
         [0, 2, 0, 3, 5, 2, 2, 2], [0, 0], None, True),

        ]

    # @pytest.mark.usefixtures("logger")
    @pytest.mark.parametrize(
        'board, store, move, turn, mtype, eboard, estore, ewcond, eturn',
        MCASES)
    def test_move(self, game, mocker,
                  board, store, move, turn, mtype,
                  eboard, estore, ewcond, eturn):

        game.board = board
        game.store = store
        game.turn = turn
        game.empty_store = mtype
        # print(game)

        wcond = game.move(move)
        assert wcond == ewcond
        assert game.board == eboard
        assert game.store == estore
        assert game.turn == eturn
