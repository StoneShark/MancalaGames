# -*- coding: utf-8 -*-
"""Constants for the UI and in the param config table.

Created on Fri Oct 27 16:54:51 2023
@author: Ann"""


# %% import

import collections

from ai_player import ALGORITHM_DICT
from game_classes import GAME_CLASSES
from game_interface import AllowRule
from game_interface import CaptExtraPick
from game_interface import ChildType
from game_interface import CrossCaptOwn
from game_interface import Direct
from game_interface import Goal
from game_interface import GrandSlam
from game_interface import LapSower
from game_interface import RoundStarter
from game_interface import SowPrescribed
from game_interface import SowRule
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

    'Algorithm': lookup_strs(ALGORITHM_DICT.keys()),

    'AllowRule': lookup_dicts(AllowRule,
        {'No special rule': AllowRule.NONE,
         'End Empty or Opp Side': AllowRule.OPP_OR_EMPTY,
         'Singles to Empties': AllowRule.SINGLE_TO_ZERO,
         'Singles only when all single': AllowRule.SINGLE_ONLY_ALL,
         'Singles when all & to Empty': AllowRule.SINGLE_ALL_TO_ZERO,
         'Doubles only when all doubles': AllowRule.TWO_ONLY_ALL,
         'Doubles, all doubles, rightmost': AllowRule.TWO_ONLY_ALL_RIGHT,
         'Rightmost two on first turn': AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
         'Right 2 1st, then twos only if all 2s':
             AllowRule.RIGHT_2_1ST_THEN_ALL_TWO
         }),

    'CaptExtraPick': lookup_dicts(CaptExtraPick,
        {'No additional': CaptExtraPick.NONE,
         'Pick Cross Seeds': CaptExtraPick.PICKCROSS,
         "Pick all Opponent's' 2s": CaptExtraPick.PICKTWOS}),

    'ChildType': lookup_dicts(ChildType,
        {'No Children': ChildType.NOCHILD,
         'Normal': ChildType.NORMAL,
         'Waldas': ChildType.WALDA,
         'One Child (tuzdek)': ChildType.ONE_CHILD}),

    'CrossCaptOwn': lookup_dicts(CrossCaptOwn,
        {'Leave': CrossCaptOwn.LEAVE,
         'Pick on Capture': CrossCaptOwn.PICK_ON_CAPT,
         'Alway Pick': CrossCaptOwn.ALWAYS_PICK}),

    'Direct': lookup_dicts(Direct,
        {'Clockwise': Direct.CW,
         'Counter-clockwise': Direct.CCW,
         'Split': Direct.SPLIT}),

    'GameClasses': lookup_strs(GAME_CLASSES.keys()),

    'Goal': lookup_dicts(Goal,
        {'Max Seeds': Goal.MAX_SEEDS,
         'Deprive Opponent': Goal.DEPRIVE,
         'Territory': Goal.TERRITORY}),

    'GrandSlam': lookup_dicts(GrandSlam,
        {"Legal": GrandSlam.LEGAL,
         "Not Legal": GrandSlam.NOT_LEGAL,
         "Legal but no capture": GrandSlam.NO_CAPT,
         "Legal but opp takes remaining": GrandSlam.OPP_GETS_REMAIN,
         "Legal but leave leftmost": GrandSlam.LEAVE_LEFT,
         "Legal but leave rightmost": GrandSlam.LEAVE_RIGHT}),

    'LapSower': lookup_dicts(LapSower,
        {'Single sow': LapSower.OFF,
         'Lap Sower (end)': LapSower.LAPPER,
         'Lap Sower Next': LapSower.LAPPER_NEXT}),

    'RoundStarter': lookup_dicts(RoundStarter,
        {'Alternate': RoundStarter.ALTERNATE,
         'Round Winner': RoundStarter.WINNER,
         'Round Loser': RoundStarter.LOSER}),

    'SowPrescribed': lookup_dicts(SowPrescribed,
        {'None': SowPrescribed.NONE,
         'Sow Basic First': SowPrescribed.BASIC_SOWER,
         'Sow Mlaps First': SowPrescribed.MLAPS_SOWER,
         'Sow One Opposite': SowPrescribed.SOW1OPP,
         'TRIPLES': SowPrescribed.TRIPLES,
         'Plus 1, Minus 1': SowPrescribed.PLUS1MINUS1}),

    'SowRule': lookup_dicts(SowRule,
        {"No Special Rule": SowRule.NONE,
         "Skip Own Blocked, Capt Opp": SowRule.SOW_BLKD_DIV,
         "Owners Capture all while Sow": SowRule.OWN_SOW_CAPT_ALL,
         "Sower Captures own while Sow": SowRule.SOW_SOW_CAPT_ALL,
         "Don't sow Opp holes w/2s": SowRule.NO_SOW_OPP_2S,
         }),

    'StartPattern': lookup_dicts(StartPattern,
        {'All Equal': StartPattern.ALL_EQUAL,
         'Gamacha': StartPattern.GAMACHA,
         'Alternates': StartPattern.ALTERNATES,
         'Alts with 1': StartPattern.ALTS_WITH_1,
         'Clipped Triples': StartPattern.CLIPPEDTRIPLES,
         'Two Empty': StartPattern.TWOEMPTY}),

}
