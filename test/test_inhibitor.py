# -*- coding: utf-8 -*-
"""Unit test for the inhibitors.

Created on Sun Jun 30 08:30:23 2024
@author: Ann"""


import pytest
pytestmark = pytest.mark.unittest

from context import inhibitor
from context import game_interface as gi


# %%

TEST_COVERS = ['src\\inhibitor.py']


# %%  tiny stubs

class MdataStub:

    def __init__(self):
        self.captured = False
        self.capt_changed = False

class InfoStub:

    def __init__(self):
        self.nocaptfirst = False
        self.round_fill = None
        self.prescribed = None

class GameStub:

    def __init__(self):

        self.info = InfoStub()
        self.mcount = 0

# %%


def test_none():

    game = GameStub()
    mdata = MdataStub()

    deco = inhibitor.deco_inhibitor(game)
    assert 'InhibitorNone' in str(deco)

    deco.new_game()
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert not deco.stop_me_capt(True)
    assert not deco.stop_me_capt(False)

    deco.set_on(True)
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert not deco.stop_me_capt(True)
    assert not deco.stop_me_capt(False)

    deco.set_off()
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert not deco.stop_me_capt(True)
    assert not deco.stop_me_capt(False)

    deco.set_child(True)
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert not deco.stop_me_capt(True)
    assert not deco.stop_me_capt(False)

    deco.set_child(False)
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert not deco.stop_me_capt(True)
    assert not deco.stop_me_capt(False)

    deco.clear_if(game, mdata)
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert not deco.stop_me_capt(True)
    assert not deco.stop_me_capt(False)


def test_capt_n():

    game = GameStub()
    game.info.nocaptfirst = True
    mdata = MdataStub()

    deco = inhibitor.deco_inhibitor(game)
    assert 'InhibitorCaptN' in str(deco)

    deco.new_game()
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert deco.stop_me_capt(True)
    assert deco.stop_me_capt(False)

    deco.set_on(True)
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert deco.stop_me_capt(True)
    assert deco.stop_me_capt(False)

    deco.set_off()
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert not deco.stop_me_capt(True)
    assert not deco.stop_me_capt(False)

    deco.set_child(True)
    # no change from last setting
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert not deco.stop_me_capt(True)
    assert not deco.stop_me_capt(False)

    deco.set_child(False)
    # no change from last setting
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert not deco.stop_me_capt(True)
    assert not deco.stop_me_capt(False)

    # reset the inhibitor
    deco.new_game()
    deco.clear_if(game, mdata)
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert deco.stop_me_capt(True)
    assert deco.stop_me_capt(False)

    deco.set_child(True)
    # no change from last setting
    assert deco.stop_me_capt(True)
    assert deco.stop_me_capt(False)

    deco.set_child(False)
    # no change from last setting
    assert deco.stop_me_capt(True)
    assert deco.stop_me_capt(False)

    # test clear_if for move 1
    game.mcount = 1
    deco.clear_if(game, mdata)
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert deco.stop_me_capt(True)
    assert deco.stop_me_capt(False)

    # test clear_if for move 2
    game.mcount = 2
    deco.clear_if(game, mdata)
    assert not deco.stop_me_child(True)
    assert not deco.stop_me_child(False)
    assert not deco.stop_me_capt(True)
    assert not deco.stop_me_capt(False)


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

        deco = inhibitor.deco_inhibitor(game)

        assert 'InhibitorChildrenOnly' in str(deco)
        assert not deco.stop_me_child(turn)
        assert not deco.stop_me_capt(turn)

        deco.set_on(True)
        assert deco.stop_me_child(turn)
        assert not deco.stop_me_capt(turn)

        deco.new_game()
        assert not deco.stop_me_child(turn)
        assert not deco.stop_me_capt(turn)

        deco.set_on(True)
        deco.set_off()
        assert not deco.stop_me_child(turn)
        assert not deco.stop_me_capt(turn)

        deco.set_on(False)
        assert deco.stop_me_child(turn)
        assert not deco.stop_me_capt(turn)


    @pytest.mark.parametrize('turn', [False, True])
    def test_set_child(self, game, turn):

        deco = inhibitor.deco_inhibitor(game)

        deco.set_child(True)
        assert deco.stop_me_child(turn)
        assert not deco.stop_me_capt(turn)

        deco.set_child(False)
        assert not deco.stop_me_child(turn)
        assert not deco.stop_me_capt(turn)


    @pytest.mark.parametrize('turn', [False, True])
    def test_clear_cond(self, game, mdata, turn):
        """clear_if does nothing for child only."""

        deco = inhibitor.deco_inhibitor(game)
        deco.set_on(turn)

        assert deco.stop_me_child(turn)
        assert deco.stop_me_child(not turn)

        deco.clear_if(game, mdata)
        assert deco.stop_me_child(turn)
        assert deco.stop_me_child(not turn)



class TestBoth:

    @pytest.fixture
    def game(self):
        game = GameStub()
        game.info.prescribed = gi.SowPrescribed.ARNGE_LIMIT
        game.info.round_fill = gi.RoundFill.SHORTEN
        return game

    @pytest.fixture
    def mdata(self):
        return MdataStub()

    def test_both(self, game):

        deco = inhibitor.deco_inhibitor(game)

        assert 'InhibitorBoth' in str(deco)
        assert not deco.stop_me_child(True)
        assert not deco.stop_me_child(False)
        assert not deco.stop_me_capt(True)
        assert not deco.stop_me_capt(False)

        deco.set_on(True)
        # turn is set to True
        assert deco.stop_me_child(True)
        assert not deco.stop_me_child(False)
        assert deco.stop_me_capt(True)
        assert not deco.stop_me_capt(False)

        deco.new_game()
        assert not deco.stop_me_child(True)
        assert not deco.stop_me_child(False)
        assert not deco.stop_me_capt(True)
        assert not deco.stop_me_capt(False)

        deco.set_on(True)
        deco.set_off()
        assert not deco.stop_me_child(True)
        assert not deco.stop_me_child(False)
        assert not deco.stop_me_capt(True)
        assert not deco.stop_me_capt(False)

        deco.set_on(False)
        assert not deco.stop_me_child(True)
        assert deco.stop_me_child(False)
        assert not deco.stop_me_capt(True)
        assert deco.stop_me_capt(False)


    def test_set_child(self, game):

        deco = inhibitor.deco_inhibitor(game)

        deco.set_child(True)
        assert deco.stop_me_child(True)
        assert deco.stop_me_child(False)
        assert not deco.stop_me_capt(True)
        assert not deco.stop_me_capt(False)

        deco.set_child(False)
        assert not deco.stop_me_child(True)
        assert not deco.stop_me_child(False)
        assert not deco.stop_me_capt(True)
        assert not deco.stop_me_capt(False)


    def test_independent(self, game):
        # test that changing child doesn't change capture

        deco = inhibitor.deco_inhibitor(game)
        deco.set_on(True)  # turn both inhibits on for True

        deco.set_child(True)  # allow children, but don't change capture
        assert deco.stop_me_child(True)
        assert deco.stop_me_child(False)
        assert deco.stop_me_capt(True)
        assert not deco.stop_me_capt(False)

        deco.set_child(False)   # inhibit children, but don't change capture
        # TODO this behavior seems wrong, doesn't match log notes
        # assert not deco.stop_me_child(True)
        # assert not deco.stop_me_child(False)
        assert deco.stop_me_capt(True)
        assert not deco.stop_me_capt(False)


    def test_clear_cond(self, game, mdata):

        deco = inhibitor.deco_inhibitor(game)
        deco.set_on(True)  # turn both inhibits on for True

        assert deco.stop_me_child(True)
        assert not deco.stop_me_child(False)
        assert deco.stop_me_capt(True)
        assert not deco.stop_me_capt(False)

        deco.clear_if(game, mdata)
        assert deco.stop_me_child(True)
        assert not deco.stop_me_child(False)
        assert deco.stop_me_capt(True)
        assert not deco.stop_me_capt(False)

        mdata.captured = True  # first condition
        deco.clear_if(game, mdata)
        assert not deco.stop_me_child(True)
        assert not deco.stop_me_child(False)
        assert not deco.stop_me_capt(True)
        assert not deco.stop_me_capt(False)

        deco.set_on(False)    # turn both inhibits on for False
        assert not deco.stop_me_child(True)
        assert deco.stop_me_child(False)
        assert not deco.stop_me_capt(True)
        assert deco.stop_me_capt(False)

        mdata.capt_changed = True   # second condition
        deco.clear_if(game, mdata)
        assert not deco.stop_me_child(True)
        assert not deco.stop_me_child(False)
        assert not deco.stop_me_capt(True)
        assert not deco.stop_me_capt(False)
