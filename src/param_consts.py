# -*- coding: utf-8 -*-
"""Constants for the UI and in the param config table.

Created on Fri Oct 27 16:54:51 2023
@author: Ann"""


# %% import

import collections

from ai_player import ALGORITHM_DICT
from game_classes import GAME_CLASSES
from game_interface import AllowRule
from game_interface import ChildType
from game_interface import CrossCaptOwn
from game_interface import Direct
from game_interface import Goal
from game_interface import GrandSlam
from game_interface import RoundStarter
from game_interface import StartPattern


# %% types from the params file

INT_TYPE = 'int'
STR_TYPE = 'str'
BOOL_TYPE = 'bool'
MSTR_TYPE = 'multi_str'
BLIST_TYPE = 'list[bool]'
ILIST_TYPE = 'list[int]'


# %% enum dictionaries

LDicts = collections.namedtuple('LDicts', 'str_dict, int_dict, enum_dict')

def lookup_dicts(etype, adict):
    """Return the dict, it's inverse, and enum name: enum dict
    for the enum (etype)."""

    vals = adict.values()
    assert len(vals) == len(set(vals)), 'values not unique for adict'
    return LDicts(adict,
                  {value: key for key, value in adict.items()},
                  {e.name: e for e in etype})


def lookup_strs(strings):
    """The string and values are both the strings.
    Build and return dictionaries."""

    sdict = {s: s for s in strings}
    return LDicts(sdict, sdict, sdict)


STRING_DICTS = {
    'GameClasses': lookup_strs(GAME_CLASSES.keys()),

    'Direct': lookup_dicts(Direct,
        {'Clockwise': Direct.CW,
         'Counter-clockwise': Direct.CCW,
         'Split': Direct.SPLIT}),

    'GrandSlam': lookup_dicts(GrandSlam,
        {"Legal": GrandSlam.LEGAL,
         "Not Legal": GrandSlam.NOT_LEGAL,
         "Legal but no capture": GrandSlam.NO_CAPT,
         "Legal but opp takes remaining": GrandSlam.OPP_GETS_REMAIN,
         "Legal but leave leftmost": GrandSlam.LEAVE_LEFT,
         "Legal but leave rightmost": GrandSlam.LEAVE_RIGHT}),

    'RoundStarter': lookup_dicts(RoundStarter,
        {'Alternate': RoundStarter.ALTERNATE,
         'Round Winner': RoundStarter.WINNER,
         'Round Loser': RoundStarter.LOSER}),

    'CrossCaptOwn': lookup_dicts(CrossCaptOwn,
        {'Leave': CrossCaptOwn.LEAVE,
         'Pick on Capture': CrossCaptOwn.PICK_ON_CAPT,
         'Alway Pick': CrossCaptOwn.ALWAYS_PICK}),

    'StartPattern': lookup_dicts(StartPattern,
        {'All Equal': StartPattern.ALL_EQUAL,
         'Gamacha': StartPattern.GAMACHA,
         'Alternates': StartPattern.ALTERNATES,
         'Alts with 1': StartPattern.ALTS_WITH_1,
         'Clipped Triples': StartPattern.CLIPPEDTRIPLES,
         'Two Empty': StartPattern.TWOEMPTY}),

    'Goal': lookup_dicts(Goal,
        {'Max Seeds': Goal.MAX_SEEDS,
         'Deprive Opponent': Goal.DEPRIVE,
         'Territory': Goal.TERRITORY}),

    'Algorithm': lookup_strs(ALGORITHM_DICT.keys()),

    'ChildType': lookup_dicts(ChildType,
        {'No Children': ChildType.NOCHILD,
         'Normal': ChildType.NORMAL,
         'Waldas': ChildType.WALDA,
         'One Child (tuzdek)': ChildType.ONE_CHILD}),

    'AllowRule': lookup_dicts(AllowRule,
        {'No special rule': AllowRule.NONE,
         'End Empty or Opp Side': AllowRule.OPP_OR_EMPTY,
         'Singles to Empties': AllowRule.SINGLE_TO_ZERO,
         'Singles only when all single': AllowRule.SINGLE_ONLY_ALL,
         'Singles when all & to Empty': AllowRule.SINGLE_ALL_TO_ZERO,
         'Doubles only when all doubles': AllowRule.TWO_ONLY_ALL,
         'Doubles, all doubles, rightmost': AllowRule.TWO_ONLY_ALL_RIGHT,
         'Rightmost two on first turn': AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
         })
}
