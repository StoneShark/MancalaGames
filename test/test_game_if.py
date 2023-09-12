# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 06:44:29 2023

@author: Ann
"""


# %% imports

import sys

import pytest

sys.path.extend(['src'])

import game_interface as gi
import ginfo_rules
import mancala

from game_interface import Direct
from game_interface import GameFlags
from game_interface import WinCond



# %%

def test_direct_op():

    # these integer values are required
    assert Direct.CCW == 1
    assert Direct.CW == -1
    assert Direct.SPLIT == 0

    assert Direct.CCW.opp_dir() == Direct.CW
    assert Direct.CW.opp_dir() == Direct.CCW

    with pytest.raises(gi.GameInfoError):
        Direct.SPLIT.opp_dir()


def test_win():

    assert WinCond.WIN in WinCond

    assert WinCond.WIN.is_ended()
    assert WinCond.TIE.is_ended()
    assert WinCond.ENDLESS.is_ended()
    assert not WinCond.END_STORE.is_ended()


def test_default_scorer():

    scorer = gi.Scorer()

    score_vals = vars(scorer).values()
    assert sum(score_vals) > 0


def test_gf_existence():

    with pytest.raises(TypeError):
        gi.GameInfo()

    with pytest.raises(gi.GameInfoError):   # name
        gi.GameInfo(name='',
                    nbr_holes=2,
                    rules=mancala.Mancala.rules)

    with pytest.raises(gi.GameInfoError):  # nbr_holes
        gi.GameInfo(nbr_holes=0,
                    flags=gi.GameFlags(),
                    rules=mancala.Mancala.rules)

    with pytest.raises(AttributeError):  # flags
        gi.GameInfo(nbr_holes=2,
                    flags=0,
                    rules=mancala.Mancala.rules)

    with pytest.raises(gi.GameInfoError):  # scorer
        gi.GameInfo(nbr_holes=2,
                    scorer=1,
                    rules=mancala.Mancala.rules)

    with pytest.raises(gi.GameInfoError):  # no sew direction, not playable
        gi.GameInfo(nbr_holes=2,
                    flags=GameFlags(sow_direct=None),
                    rules=mancala.Mancala.rules)

    gi.GameInfo(name='Mancala',
                nbr_holes=6,
                capt_on=[2],
                flags=GameFlags(sow_direct=Direct.CCW),
                rules=mancala.Mancala.rules)

    # evaluate if new tests should be added
    assert len(GameFlags.get_fields()) == 23


def test_gf_stores():

    with pytest.raises(gi.GameInfoError):
        gi.GameInfo(nbr_holes=6,
                    flags=GameFlags(sow_direct=Direct.CCW,
                                    sow_own_store=True),
                    rules=mancala.Mancala.rules)


def test_rule_dict(capsys):

    rules = ginfo_rules.RuleDict()

    rules.add_rule(name='rule_name',
                   msg='something bad',
                   rule= lambda ginfo : ginfo)

    data = capsys.readouterr().out
    assert 'rule_name' in data
    assert 'has no effect' in data


def test_dupl_rule(capsys):

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


def test_move_tuple():

    tup = gi.MoveTpl(3, Direct.CCW)
    assert isinstance(tup, tuple)
    assert str(tup) == '(3, CCW)'

    tup = gi.MoveTpl(2, None)
    assert isinstance(tup, tuple)
    assert str(tup) == '(2, None)'
