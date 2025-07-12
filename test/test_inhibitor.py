# -*- coding: utf-8 -*-
"""Unit test for the inhibitors.

Created on Sun Jun 30 08:30:23 2024
@author: Ann"""


import pytest
pytestmark = pytest.mark.unittest

from context import animator
from context import inhibitor
from context import game_info as gi


# %%

TEST_COVERS = ['src\\inhibitor.py']


# %%  tiny stubs

class MdataStub:

    def __init__(self):
        self.captured = False
        self.capt_changed = False

class InfoStub:

    def __init__(self):
        self.nocaptmoves = 0
        self.round_fill = None
        self.prescribed = None

class GameStub:

    def __init__(self):

        self.info = InfoStub()
        self.movers = 0

# %%


def test_none():

    game = GameStub()
    mdata = MdataStub()

    inhibit = inhibitor.make_inhibitor(game)
    assert 'InhibitorNone' in str(inhibit)

    inhibit.new_game()
    assert not inhibit.stop_me_child(True)
    assert not inhibit.stop_me_child(False)
    assert not inhibit.stop_me_capt(True)
    assert not inhibit.stop_me_capt(False)

    inhibit.start_ani_msg()

    inhibit.set_on(True)
    assert not inhibit.stop_me_child(True)
    assert not inhibit.stop_me_child(False)
    assert not inhibit.stop_me_capt(True)
    assert not inhibit.stop_me_capt(False)

    inhibit.set_off()
    assert not inhibit.stop_me_child(True)
    assert not inhibit.stop_me_child(False)
    assert not inhibit.stop_me_capt(True)
    assert not inhibit.stop_me_capt(False)

    inhibit.set_child(True)
    assert not inhibit.stop_me_child(True)
    assert not inhibit.stop_me_child(False)
    assert not inhibit.stop_me_capt(True)
    assert not inhibit.stop_me_capt(False)

    inhibit.set_child(False)
    assert not inhibit.stop_me_child(True)
    assert not inhibit.stop_me_child(False)
    assert not inhibit.stop_me_capt(True)
    assert not inhibit.stop_me_capt(False)

    inhibit.clear_if(game, mdata)
    assert not inhibit.stop_me_child(True)
    assert not inhibit.stop_me_child(False)
    assert not inhibit.stop_me_capt(True)
    assert not inhibit.stop_me_capt(False)

    assert inhibit.get_state() is None
    inhibit.set_state(True)
    assert inhibit.get_state() is None


class TestCaptN:

    @pytest.fixture
    def game(self):
        game = GameStub()
        game.info.nocaptmoves = 1
        return game

    @pytest.fixture
    def mdata(self):
        return MdataStub()


    def test_capt_n(self, game, mdata):

        inhibit = inhibitor.make_inhibitor(game)
        assert 'InhibitorCaptN' in str(inhibit)

        inhibit.new_game()
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert inhibit.stop_me_capt(True)
        assert inhibit.stop_me_capt(False)

        inhibit.set_on(True)
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert inhibit.stop_me_capt(True)
        assert inhibit.stop_me_capt(False)

        inhibit.set_off()
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        inhibit.set_child(True)
        # no change from last setting
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        inhibit.set_child(False)
        # no change from last setting
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        # reset the inhibitor
        inhibit.new_game()
        assert inhibit.get_state()
        inhibit.clear_if(game, mdata)
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert inhibit.stop_me_capt(True)
        assert inhibit.stop_me_capt(False)

        inhibit.set_child(True)
        # no change from last setting
        assert inhibit.stop_me_capt(True)
        assert inhibit.stop_me_capt(False)

        inhibit.set_child(False)
        # no change from last setting
        assert inhibit.stop_me_capt(True)
        assert inhibit.stop_me_capt(False)

        # test clear_if for move 0
        game.movers = 0
        inhibit.clear_if(game, mdata)
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert inhibit.stop_me_capt(True)
        assert inhibit.stop_me_capt(False)
        assert inhibit.get_state()

        # test clear_if for move 1
        game.movers = 1
        inhibit.clear_if(game, mdata)
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)
        assert not inhibit.get_state()

        # test clear_if for move 2
        game.movers = 2
        inhibit.clear_if(game, mdata)
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        assert not inhibit.get_state()
        inhibit.set_state(True)
        assert inhibit.get_state()


    stmts = ['inhibit.start_ani_msg()',
             'inhibit.set_on(True)',
             'inhibit.set_off()',
             ]
    @pytest.mark.animator
    @pytest.mark.parametrize('stmt', stmts)
    def test_animator(self, mocker, game, mdata, stmt):
        """Test the interfaces that generate a message
        when the animator is active."""

        assert animator.ENABLED
        animator.make_animator(None)   # no game_ui, make sure it's not used
        animator.set_active(True)

        mobj = mocker.patch('animator.animator.message')

        inhibit = inhibitor.make_inhibitor(game)
        inhibit.new_game()

        exec(stmt)

        mobj.assert_called_once()


    @pytest.mark.animator
    def test_ani_clear_if(self, mocker, game, mdata):

        assert animator.ENABLED
        animator.make_animator(None)   # no game_ui, make sure it's not used
        animator.set_active(True)

        mobj = mocker.patch('animator.animator.message')

        inhibit = inhibitor.make_inhibitor(game)
        inhibit.new_game()

        game.movers = 0
        inhibit.clear_if(game, mdata)
        mobj.assert_not_called()

        game.movers = 1
        inhibit.clear_if(game, mdata)
        mobj.assert_called_once()

        game.movers = 2
        inhibit.clear_if(game, mdata)
        assert len(mobj.mock_calls) == 1



class TestChildOnly:
    """children only completely ignores turn, parametrize turn."""

    @pytest.fixture
    def game(self):
        game = GameStub()
        game.info.round_fill = gi.RoundFill.SHORTEN
        return game

    @pytest.fixture
    def mdata(self):
        return MdataStub()

    @pytest.mark.parametrize('turn', [False, True])
    def test_child(self, game, turn):

        inhibit = inhibitor.make_inhibitor(game)

        assert 'InhibitorChildrenOnly' in str(inhibit)
        assert not inhibit.stop_me_child(turn)
        assert not inhibit.stop_me_capt(turn)

        inhibit.set_on(True)
        assert inhibit.stop_me_child(turn)
        assert not inhibit.stop_me_capt(turn)

        inhibit.new_game()
        assert not inhibit.stop_me_child(turn)
        assert not inhibit.stop_me_capt(turn)

        inhibit.set_on(True)
        inhibit.set_off()
        assert not inhibit.stop_me_child(turn)
        assert not inhibit.stop_me_capt(turn)

        inhibit.set_on(False)
        assert inhibit.stop_me_child(turn)
        assert not inhibit.stop_me_capt(turn)

        inhibit.new_game()
        assert not inhibit.get_state()
        inhibit.set_state(True)
        assert inhibit.get_state()


    @pytest.mark.parametrize('turn', [False, True])
    def test_set_child(self, game, turn):

        inhibit = inhibitor.make_inhibitor(game)

        inhibit.set_child(True)
        assert inhibit.stop_me_child(turn)
        assert not inhibit.stop_me_capt(turn)

        inhibit.set_child(False)
        assert not inhibit.stop_me_child(turn)
        assert not inhibit.stop_me_capt(turn)


    @pytest.mark.parametrize('turn', [False, True])
    def test_clear_cond(self, game, mdata, turn):
        """clear_if does nothing for child only."""

        inhibit = inhibitor.make_inhibitor(game)
        inhibit.set_on(turn)

        assert inhibit.stop_me_child(turn)
        assert inhibit.stop_me_child(not turn)

        inhibit.clear_if(game, mdata)
        assert inhibit.stop_me_child(turn)
        assert inhibit.stop_me_child(not turn)


    stmts = ['inhibit.set_on(True)',
             'inhibit.set_off()',
             'inhibit.set_child(True)',
             'inhibit.set_child(False)',
             ]
    @pytest.mark.animator
    @pytest.mark.parametrize('stmt', stmts)
    def test_animator(self, mocker, game, mdata, stmt):
        """Test the interfaces that generate a message
        when the animator is active."""

        assert animator.ENABLED
        animator.make_animator(None)   # no game_ui, make sure it's not used
        animator.set_active(True)

        mobj = mocker.patch('animator.animator.message')

        inhibit = inhibitor.make_inhibitor(game)
        inhibit.new_game()

        exec(stmt)

        mobj.assert_called_once()


    @pytest.mark.animator
    def test_start_ani_msg(self, mocker, game, mdata):

        assert animator.ENABLED
        animator.make_animator(None)   # no game_ui, make sure it's not used
        animator.set_active(True)

        mobj = mocker.patch('animator.animator.message')

        inhibit = inhibitor.make_inhibitor(game)
        inhibit.new_game()

        inhibit.start_ani_msg()
        mobj.assert_not_called()

        inhibit._children = True
        inhibit.start_ani_msg()
        mobj.assert_called_once()


class TestBoth:

    @pytest.fixture
    def game(self):
        game = GameStub()
        game.info.prescribed = gi.SowPrescribed.ARNGE_LIMIT
        return game

    @pytest.fixture
    def mdata(self):
        return MdataStub()

    def test_both(self, game):

        inhibit = inhibitor.make_inhibitor(game)

        assert 'InhibitorBoth' in str(inhibit)
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        inhibit.set_on(True)
        # turn is set to True
        assert inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        inhibit.new_game()
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        inhibit.set_on(True)
        inhibit.set_off()
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        inhibit.set_on(False)
        assert not inhibit.stop_me_child(True)
        assert inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert inhibit.stop_me_capt(False)


    def test_set_child(self, game):

        inhibit = inhibitor.make_inhibitor(game)

        inhibit.set_child(True)
        assert inhibit.stop_me_child(True)
        assert inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        inhibit.set_child(False)
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)


    def test_independent(self, game):
        # test that changing child doesn't change capture

        inhibit = inhibitor.make_inhibitor(game)
        inhibit.set_on(True)  # turn both inhibits on for True

        inhibit.set_child(True)  # allow children, but don't change capture
        assert inhibit.stop_me_child(True)
        assert inhibit.stop_me_child(False)
        assert inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        inhibit.set_child(False)   # inhibit children, but don't change capture
        # TODO this behavior seems wrong, doesn't match log notes
        # assert not inhibit.stop_me_child(True)
        # assert not inhibit.stop_me_child(False)
        assert inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)


    def test_clear_cond(self, game, mdata):

        inhibit = inhibitor.make_inhibitor(game)
        inhibit.set_on(True)  # turn both inhibits on for True

        assert inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        inhibit.clear_if(game, mdata)
        assert inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        mdata.captured = True  # first condition
        inhibit.clear_if(game, mdata)
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)

        inhibit.set_on(False)    # turn both inhibits on for False
        assert not inhibit.stop_me_child(True)
        assert inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert inhibit.stop_me_capt(False)

        mdata.capt_changed = True   # second condition
        inhibit.clear_if(game, mdata)
        assert not inhibit.stop_me_child(True)
        assert not inhibit.stop_me_child(False)
        assert not inhibit.stop_me_capt(True)
        assert not inhibit.stop_me_capt(False)


    def test_state(self, game):

        inhibit = inhibitor.make_inhibitor(game)

        istate = inhibit.get_state()
        assert len(istate) == 4
        assert istate[0] == None
        assert istate[1] == False
        assert istate[2] == False
        assert istate[3] == False

        inhibit.set_state((123, 234, 345, 456))
        assert inhibit._turn == 123
        assert inhibit._captures == 234
        assert inhibit._children == 345
        assert inhibit._child_only == 456


    stmts = ['inhibit.set_on(True)',
             'inhibit.set_off()',
             'inhibit.set_child(True)',
             'inhibit.set_child(False)']
    @pytest.mark.animator
    @pytest.mark.parametrize('stmt', stmts)
    def test_animator(self, mocker, game, mdata, stmt):
        """Test the interfaces that generate a message
        when the animator is active."""

        assert animator.ENABLED
        animator.make_animator(None)   # no game_ui, make sure it's not used
        animator.set_active(True)

        mobj = mocker.patch('animator.animator.message')

        inhibit = inhibitor.make_inhibitor(game)
        inhibit.new_game()

        exec(stmt)

        mobj.assert_called_once()


    conds = [(False, False, False),   # no message
             (False, True, True),
             (True, False, False),    # capt only not supported by I-BOTH
             (True, True, True)]
    @pytest.mark.animator
    @pytest.mark.parametrize('capts, child, emsg', conds)
    def test_start_ani_msg(self, mocker, game, mdata, capts, child, emsg):

        assert animator.ENABLED
        animator.make_animator(None)   # no game_ui, make sure it's not used
        animator.set_active(True)

        mobj = mocker.patch('animator.animator.message')

        inhibit = inhibitor.make_inhibitor(game)
        inhibit.new_game()

        # don't use the interface to set, don't want messages
        inhibit._captures = capts
        inhibit._children = child
        inhibit._child_only = child and not capts
        inhibit._turn = False

        inhibit.start_ani_msg()

        if emsg:
            mobj.assert_called_once()
        else:
            mobj.assert_not_called()


    @pytest.mark.animator
    def test_ani_clear_if(self, mocker, game, mdata):

        assert animator.ENABLED
        animator.make_animator(None)   # no game_ui, make sure it's not used
        animator.set_active(True)

        mobj = mocker.patch('animator.animator.message')

        inhibit = inhibitor.make_inhibitor(game)
        inhibit.new_game()

        # don't use the interface to set, don't want messages
        inhibit._captures = True
        inhibit._children = True
        inhibit._turn = False

        inhibit.clear_if(game, mdata)
        mobj.assert_not_called()

        mdata.captured = True           # capture occured, test will turn off
        inhibit.clear_if(game, mdata)
        mobj.assert_called_once()

        inhibit.clear_if(game, mdata)   # don't generate a 2nd message
        assert len(mobj.mock_calls) == 1
