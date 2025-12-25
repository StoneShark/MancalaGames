# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 06:15:54 2025

@author: Ann
"""


# %% imports

import pytest
pytestmark = pytest.mark.unittest

from context import capt_ok
from context import game_constants as gconsts
from context import game_info as gi
from context import incrementer
from context import mancala


# %% constants

TEST_COVERS = ['src\\man_deco.py']


# %% tests

class TestManDeco:

    @pytest.fixture
    def game(self):
        """basic game"""

        game_consts = gconsts.GameConsts(nbr_start=4, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=lambda ginfo, holes: True)

        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_deco(self, game):

        assert game.deco.new_game
        assert game.deco.allow
        assert game.deco.moves
        assert game.deco.incr
        assert game.deco.drawer
        assert game.deco.get_dir
        assert game.deco.sower
        assert game.deco.ender
        assert game.deco.quitter
        assert game.deco.capt_basic
        assert game.deco.capt_check
        assert game.deco.capturer
        assert game.deco.gstr
        assert game.deco.make_child

        dstr = str(game.deco)
        for field, value in vars(game.deco).items():
            assert field in dstr


    def test_replace_deco_1(self):
        """Test replacing the head of the chain."""

        game_consts = gconsts.GameConsts(nbr_start=2, holes=5)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=gi.Goal.CLEAR,
                                skip_start=True,
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        # confirm expected structure of deco chain
        assert isinstance(game.deco.incr,
                          incrementer.IncPastStart), 'Test conditions changed'
        assert isinstance(game.deco.incr.decorator,
                          incrementer.Increment), 'Test conditions changed'

        game.deco.replace_deco('incr', incrementer.IncPastStart,
                               incrementer.IncPastBlocks(game))

        assert isinstance(game.deco.incr, incrementer.IncPastBlocks)
        assert isinstance(game.deco.incr.decorator, incrementer.Increment)


    @pytest.fixture
    def bad_game(self):
        """Bad config but no rules are checked."""

        game_consts = gconsts.GameConsts(nbr_start=2, holes=5)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=gi.Goal.CLEAR,
                                skip_start=True,
                                blocks=True,            # this is not valid
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=lambda ginfo, holes: True)  # no rules
        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_replace_deco_2(self, bad_game):
        """Test replacing the end of the deco chain."""

        # confirm expected structure of deco chain
        assert isinstance(bad_game.deco.incr,
                          incrementer.IncPastBlocks), 'Test conditions changed'
        assert isinstance(bad_game.deco.incr.decorator,
                          incrementer.IncPastStart), 'Test conditions changed'
        assert isinstance(bad_game.deco.incr.decorator.decorator,
                          incrementer.Increment), 'Test conditions changed'

        # true is not a valid decorator, but we want to assure that it
        # is replaced correctly
        new_incr = incrementer.IncPastBlocks(bad_game, True)
        assert new_incr.decorator

        bad_game.deco.replace_deco('incr', incrementer.Increment,
                                   new_incr)

        assert isinstance(bad_game.deco.incr, incrementer.IncPastBlocks)
        assert isinstance(bad_game.deco.incr.decorator,
                          incrementer.IncPastStart)
        assert isinstance(bad_game.deco.incr.decorator.decorator,
                          incrementer.IncPastBlocks)
        assert not new_incr.decorator


    def test_bad_deco_replace(self, mocker, bad_game):
        """Patch the deco chain to only a IncPastBlocks,
        but then try to replace Incrementer. It should fail."""

        bad_game.deco.incr = incrementer.IncPastBlocks(None)

        with pytest.raises(AssertionError):
            bad_game.deco.replace_deco('incr', incrementer.Increment,
                                   incrementer.IncPastBlocks(bad_game))

    def test_insert_deco_1(self):
        """Test inserting at the head of the chain."""

        game_consts = gconsts.GameConsts(nbr_start=2, holes=5)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=gi.Goal.CLEAR,
                                skip_start=True,
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        # confirm expected structure of deco chain
        assert isinstance(game.deco.incr,
                          incrementer.IncPastStart), 'Test conditions changed'
        assert isinstance(game.deco.incr.decorator,
                          incrementer.Increment), 'Test conditions changed'

        game.deco.insert_deco('incr', incrementer.IncPastStart,
                               incrementer.IncPastBlocks(game))

        assert isinstance(game.deco.incr, incrementer.IncPastBlocks)
        assert isinstance(game.deco.incr.decorator, incrementer.IncPastStart)


    def test_insert_deco_2(self):
        """Test inserting not at the head of the chain."""

        game_consts = gconsts.GameConsts(nbr_start=2, holes=5)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=gi.Goal.CLEAR,
                                skip_start=True,
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        capt_basic_deco = game.deco.capt_basic

        # confirm expected structure of deco chain
        assert isinstance(capt_basic_deco,
                          capt_ok.CaptNeedSeeds), 'Test conditions changed'
        assert isinstance(capt_basic_deco.decorator,
                          capt_ok.CaptSideOk), 'Test conditions changed'
        assert isinstance(capt_basic_deco.decorator.decorator,
                          capt_ok.CaptOn), 'Test conditions changed'
        assert isinstance(capt_basic_deco.decorator.decorator.decorator,
                          capt_ok.CaptTrue), 'Test conditions changed'

        game.deco.insert_deco('capt_basic', capt_ok.CaptOn,
                               capt_ok.CaptEvens(game))

        assert isinstance(capt_basic_deco,
                          capt_ok.CaptNeedSeeds)
        assert isinstance(capt_basic_deco.decorator,
                          capt_ok.CaptSideOk)
        assert isinstance(capt_basic_deco.decorator.decorator,
                          capt_ok.CaptEvens)
        assert isinstance(capt_basic_deco.decorator.decorator.decorator,
                          capt_ok.CaptOn)
        assert isinstance(capt_basic_deco.decorator.decorator.decorator.decorator,
                          capt_ok.CaptTrue)


    def test_bad_deco_insert(self, mocker, bad_game):
        """Patch the deco chain to only a IncPastBlocks,
        but then try to replace Incrementer. It should fail."""

        bad_game.deco.incr = incrementer.IncPastBlocks(None)

        with pytest.raises(AssertionError):
            bad_game.deco.insert_deco('incr', incrementer.Increment,
                                      incrementer.IncPastBlocks(bad_game))


    def test_append_deco_1(self, game):
        """test usual case."""

        deco = game.deco.capt_basic
        print(deco)
        assert isinstance(deco,
                          capt_ok.CaptNeedSeeds), 'Test conditions changed'
        assert isinstance(deco.decorator,
                          capt_ok.CaptOn), 'Test conditions changed'
        assert isinstance(deco.decorator.decorator,
                          capt_ok.CaptTrue), 'Test conditions changed'

        game.deco.append_deco('capt_basic',
                              (capt_ok.CaptOn, capt_ok.CaptNeedSeeds),
                               capt_ok.CaptEvens(game))

        deco = game.deco.capt_basic
        assert isinstance(deco, capt_ok.CaptNeedSeeds)
        assert isinstance(deco.decorator, capt_ok.CaptOn)
        assert isinstance(deco.decorator.decorator, capt_ok.CaptEvens)
        assert isinstance(deco.decorator.decorator.decorator,
                          capt_ok.CaptTrue)


    def test_append_deco_2(self, game):
        """CaptOn is in the deco chain, but it is not at the
        top of the chain.
        apppend_deco replaces after optional decos at the head of
        the deco chain.
        Test replacing the head of the deco chain."""

        deco = game.deco.capt_basic
        assert isinstance(deco,
                          capt_ok.CaptNeedSeeds), 'Test conditions changed'
        assert isinstance(deco.decorator,
                          capt_ok.CaptOn), 'Test conditions changed'
        assert isinstance(deco.decorator.decorator,
                          capt_ok.CaptTrue), 'Test conditions changed'

        game.deco.append_deco('capt_basic',
                              (capt_ok.CaptOn),
                              capt_ok.CaptEvens(game))

        deco = game.deco.capt_basic
        assert isinstance(deco, capt_ok.CaptEvens)
        assert isinstance(deco.decorator, capt_ok.CaptNeedSeeds)
        assert isinstance(deco.decorator.decorator, capt_ok.CaptOn)
        assert isinstance(deco.decorator.decorator.decorator,
                          capt_ok.CaptTrue)
