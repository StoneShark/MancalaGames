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
from context import game_interface as gi
from context import ginfo_rules

from game_interface import Direct
from game_interface import WinCond



# %%

TEST_COVERS = ['src\\cfg_keys.py',
               'src\\game_interface.py',
               'src\\ginfo_rules.py']


# %%

class TestEnumsClasses:

    def test_direct_op(self):

        # these integer values are required
        assert Direct.CCW == 1
        assert Direct.CW == -1
        assert Direct.SPLIT == 0

        assert Direct.CCW.opp_dir() == Direct.CW
        assert Direct.CW.opp_dir() == Direct.CCW

        with pytest.raises(gi.GameInfoError):
            Direct.SPLIT.opp_dir()


    def test_win(self):

        assert WinCond.WIN in WinCond

        assert WinCond.WIN.is_ended()
        assert WinCond.TIE.is_ended()
        assert WinCond.ENDLESS.is_ended()
        assert not WinCond.END_STORE.is_ended()


    def test_move_tuple(self):

        tup = gi.MoveTpl(3, Direct.CCW)
        assert isinstance(tup, tuple)
        assert str(tup) == '(3, CCW)'

        tup = gi.MoveTpl(2, None)
        assert isinstance(tup, tuple)
        assert str(tup) == '(2, None)'

        tup = gi.MoveTpl(True, 3, Direct.CW)
        assert isinstance(tup, tuple)
        assert str(tup) == '(True, 3, CW)'

        tup = gi.MoveTpl(False, 2, None)
        assert isinstance(tup, tuple)
        assert str(tup) == '(False, 2, None)'


class TestConstruction:

    def test_gf_existence(self):

        rules = ginfo_rules.build_rules()

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
                            capt_on=[2],
                            sow_direct=Direct.CCW,
                            rules=rules)

        ginfo = gi.GameInfo(capt_on=[2],
                            sow_direct=Direct.CCW,
                            nbr_holes=6,
                            rules=rules)


class TestRuleDict:

    def test_rule_dict(self, capsys):

        rules = ginfo_rules.RuleDict()

        rules.add_rule(name='rule_name',
                       msg='something bad',
                       rule= lambda ginfo : ginfo)

        data = capsys.readouterr().out
        assert 'rule_name' in data
        assert 'has no effect' in data

    def test_dupl_rule(self, capsys):

        rules = ginfo_rules.RuleDict()

        rules.add_rule(name='dupl_rule',
                       msg='something bad',
                       rule= lambda ginfo : ginfo,
                       warn=True)
        rules.add_rule(name='dupl_rule',
                       msg='more of bad stuff',
                       rule= lambda ginfo : ginfo,
                       warn=True)

        data = capsys.readouterr().out
        assert 'dupl_rule' in data
        assert 'replaced' in data


    def test_game_info_rule_test(self):

        # sow_own_needs_store
        with pytest.raises(gi.GameInfoError):
            gi.GameInfo(nbr_holes=6,
                        sow_direct=Direct.CCW,
                        sow_own_store=True,
                        rules=ginfo_rules.build_rules())

        # warn_no_capt
        with pytest.warns(UserWarning) as record:
            gi.GameInfo(nbr_holes=6,
                        rules=ginfo_rules.build_rules())

        assert len(record) == 1
        assert 'No capture mechanism provided' in record[0].message.args[0]


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
