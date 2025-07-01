# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 06:44:29 2023

@author: Ann
"""


# %% imports


import pytest

# unit test
# report warnings as errrors
pytestmark = [pytest.mark.unittest, pytest.mark.filterwarnings("error")]


from context import cfg_keys as ckey
from context import game_info as gi
from context import ginfo_rules

from game_info import Direct
from game_info import Goal
from game_info import WinCond


# %%

TEST_COVERS = ['src\\cfg_keys.py',
               'src\\game_info.py',
               'src\\ginfo_rules.py']


# %%

class TestEnumsClasses:

    def test_allow(self):

        assert gi.AllowRule.OCCUPIED.no_moves()
        assert not gi.AllowRule.TWO_ONLY_ALL.no_moves()


    def test_direct_op(self):

        # these integer values are required
        assert Direct.CCW == 1
        assert Direct.CW == -1
        assert Direct.SPLIT == 0

        assert Direct.CCW.opp_dir() == Direct.CW
        assert Direct.CW.opp_dir() == Direct.CCW

        with pytest.raises(gi.GameInfoError):
            Direct.SPLIT.opp_dir()

        with pytest.raises(gi.GameInfoError):
            Direct.PLAYALTDIR.opp_dir()


    def test_goal(self):

        assert Goal.DEPRIVE.eliminate()
        assert not Goal.TERRITORY.eliminate()

        assert not Goal.DEPRIVE.rnd_win_count()
        assert Goal.RND_WIN_COUNT_DEP


    def test_win(self):

        assert WinCond.WIN in WinCond

        assert WinCond.WIN.is_ended()
        assert WinCond.TIE.is_ended()
        assert WinCond.ENDLESS.is_ended()
        assert not WinCond.REPEAT_TURN.is_ended()

        assert WinCond.WIN.is_win()
        assert WinCond.ROUND_WIN.is_win()
        assert not WinCond.TIE.is_win()
        assert not WinCond.ENDLESS.is_win()

        assert WinCond.TIE.is_tie()
        assert WinCond.ROUND_TIE.is_tie()
        assert not WinCond.WIN.is_tie()
        assert not WinCond.ENDLESS.is_tie()

        assert WinCond.TIE.is_game_over()
        assert WinCond.WIN.is_game_over()
        assert not WinCond.ROUND_WIN.is_game_over()
        assert not WinCond.ROUND_TIE.is_game_over()

        assert not WinCond.TIE.is_round_over()
        assert not WinCond.WIN.is_round_over()
        assert WinCond.ROUND_WIN.is_round_over()
        assert WinCond.ROUND_TIE.is_round_over()


    def test_move_tuple(self):

        tup = gi.MoveTpl(3, Direct.CCW)
        assert isinstance(tup, tuple)
        assert str(tup) == '(3, CCW)'

        new_tup = tup.set_dir(Direct.CCW)
        assert tup == new_tup
        assert isinstance(new_tup, tuple)
        assert str(new_tup) == '(3, CCW)'

        tup = gi.MoveTpl(2, None)
        assert isinstance(tup, tuple)
        assert str(tup) == '(2, None)'

        new_tup = tup.set_dir(Direct.CW)
        assert tup != new_tup
        assert isinstance(new_tup, tuple)
        assert str(new_tup) == '(2, CW)'

        tup = gi.MoveTpl(True, 3, Direct.CW)
        assert isinstance(tup, tuple)
        assert str(tup) == '(True, 3, CW)'

        new_tup = tup.set_dir(Direct.CCW)
        assert tup != new_tup
        assert isinstance(new_tup, tuple)
        assert str(new_tup) == '(True, 3, CCW)'

        tup = gi.MoveTpl(False, 2, None)
        assert isinstance(tup, tuple)
        assert str(tup) == '(False, 2, None)'


class TestConstruction:

    def test_gf_existence(self):

        rules = ginfo_rules.test_rules

        with pytest.raises(TypeError):
            gi.GameInfo()

        with pytest.raises(gi.GameInfoError):   # name
            gi.GameInfo(name='',
                        nbr_holes=2,
                        rules=rules)

        with pytest.raises(gi.GameInfoError):  # nbr_holes
            gi.GameInfo(nbr_holes=0,
                        rules=rules)

        with pytest.raises(gi.GameInfoError):  # no sew direction, not playable
            gi.GameInfo(nbr_holes=2,
                        sow_direct=None,
                        rules=rules)

        # confirm this is min game config, that doesn't generate errors
        ginfo = gi.GameInfo(nbr_holes=6,
                            stores=True,
                            capt_on=[2],
                            rules=rules)
        assert ginfo.basic_capt
        assert ginfo.any_captures

        # test derived params
        ginfo = gi.GameInfo(capt_on=[2],
                            stores=True,
                            nbr_holes=6,
                            rules=rules)
        assert ginfo.mlength == 1
        assert not ginfo.udirect

        ginfo = gi.GameInfo(capt_on=[2],
                            udir_holes=[2],
                            sow_direct=Direct.SPLIT,
                            stores=True,
                            nbr_holes=6,
                            rules=rules)
        assert ginfo.mlength == 2
        assert ginfo.udirect

        ginfo = gi.GameInfo(capt_on=[2],
                            goal=Goal.TERRITORY,
                            goal_param=10,
                            stores=True,
                            nbr_holes=6,
                            rules=rules)
        assert ginfo.mlength == 3
        assert not ginfo.udirect

        ginfo = gi.GameInfo(capt_on=[2],
                            goal=Goal.TERRITORY,
                            goal_param=10,
                            stores=True,
                            udir_holes=[2],
                            sow_direct=Direct.SPLIT,
                            nbr_holes=6,
                            rules=rules)
        assert ginfo.mlength == 3
        assert ginfo.udirect


        ginfo = gi.GameInfo(capt_on=[2],
                            sow_direct=Direct.PLAYALTDIR,
                            nbr_holes=6,
                            stores=True,
                            rules=rules)
        assert ginfo.mlength == 2
        assert ginfo.udirect

        ginfo = gi.GameInfo(crosscapt=True,
                            goal=Goal.TERRITORY,
                            goal_param=10,
                            stores=True,
                            udir_holes=[2],
                            sow_direct=Direct.PLAYALTDIR,
                            nbr_holes=6,
                            rules=rules)
        assert ginfo.mlength == 3
        assert ginfo.udirect
        assert len(ginfo.udir_holes) == 6
        assert not ginfo.repeat_turn
        assert not ginfo.basic_capt
        assert ginfo.any_captures

        ginfo = gi.GameInfo(capt_on=[2],
                            capt_rturn=True,
                            nbr_holes=6,
                            stores=True,
                            rules=rules)
        assert ginfo.repeat_turn

        ginfo = gi.GameInfo(capt_on=[2],
                            sow_own_store=True,
                            nbr_holes=6,
                            stores=True,
                            rules=rules)
        assert ginfo.repeat_turn

        ginfo = gi.GameInfo(sow_own_store=True,
                            nbr_holes=6,
                            stores=True,
                            rules=rules)
        assert ginfo.repeat_turn
        assert not ginfo.any_captures



class TestCfgKeys:

    def test_cfg_keys(self):
        """Confirm all of the CameInfo fields are in cfg_keys."""

        fields = gi.GameInfo.get_fields()
        ckey_dir = [key for key in dir(ckey) if key[0] != '_']

        for field in fields:
            assert field.upper() in ckey_dir


class TestGetDefaults:

    def test_gi_defaults(self):

        assert not gi.GameInfo.get_default('stores')
        assert gi.GameInfo.get_default('allow_rule') == gi.AllowRule.NONE
        assert gi.GameInfo.get_default('capt_on') == []
        assert gi.GameInfo.get_default('missing') is None
