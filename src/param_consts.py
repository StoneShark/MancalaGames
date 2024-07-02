# -*- coding: utf-8 -*-
"""Constants for the UI and in the param config table.

Created on Fri Oct 27 16:54:51 2023
@author: Ann"""


# %% import

import collections

import game_interface as gi

from ai_player import ALGORITHM_DICT
from game_classes import GAME_CLASSES


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

    'AllowRule': lookup_dicts(
        gi.AllowRule,
        {'No special rule': gi.AllowRule.NONE,
         'End Empty or Opp Side': gi.AllowRule.OPP_OR_EMPTY,
         'Singles to Empties': gi.AllowRule.SINGLE_TO_ZERO,
         'Singles only when all single': gi.AllowRule.SINGLE_ONLY_ALL,
         'Singles when all & to Empty': gi.AllowRule.SINGLE_ALL_TO_ZERO,
         'Doubles only when all doubles': gi.AllowRule.TWO_ONLY_ALL,
         'Doubles, all doubles, rightmost': gi.AllowRule.TWO_ONLY_ALL_RIGHT,
         'Rightmost two on first turn':
             gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
         'Right 2 1st, then twos only if all 2s':
             gi.AllowRule.RIGHT_2_1ST_THEN_ALL_TWO
         }),

    'CaptExtraPick': lookup_dicts(
        gi.CaptExtraPick,
        {'No additional': gi.CaptExtraPick.NONE,
         'Pick Cross Seeds': gi.CaptExtraPick.PICKCROSS,
         "Pick all Opponent's' 2s": gi.CaptExtraPick.PICKTWOS}),

    'ChildType': lookup_dicts(
        gi.ChildType,
        {'No Children': gi.ChildType.NOCHILD,
         'Normal': gi.ChildType.NORMAL,
         'Waldas': gi.ChildType.WALDA,
         'One Child (tuzdek)': gi.ChildType.ONE_CHILD,
         'Weg / Daughter': gi.ChildType.WEG,
         'Bull': gi.ChildType.BULL,
         'Qur': gi.ChildType.QUR}),

    'ChildRule': lookup_dicts(
        gi.ChildRule,
        {'No additional restrictions': gi.ChildRule.NONE,
         'Opposite Side/Territory Only': gi.ChildRule.OPP_ONLY,
         'Not 1st Opposite with 1': gi.ChildRule.NOT_1ST_OPP}),

    'CrossCaptOwn': lookup_dicts(
        gi.CrossCaptOwn,
        {'Leave': gi.CrossCaptOwn.LEAVE,
         'Pick on Capture': gi.CrossCaptOwn.PICK_ON_CAPT,
         'Alway Pick': gi.CrossCaptOwn.ALWAYS_PICK}),

    'Direct': lookup_dicts(
        gi.Direct,
        {'Clockwise': gi.Direct.CW,
         'Counter-clockwise': gi.Direct.CCW,
         'Split': gi.Direct.SPLIT}),

    'GameClasses': lookup_strs(GAME_CLASSES.keys()),

    'Goal': lookup_dicts(
        gi.Goal,
        {'Max Seeds': gi.Goal.MAX_SEEDS,
         'Deprive Opponent': gi.Goal.DEPRIVE,
         'Territory': gi.Goal.TERRITORY}),

    'GrandSlam': lookup_dicts(
        gi.GrandSlam,
        {"Legal": gi.GrandSlam.LEGAL,
         "Not Legal": gi.GrandSlam.NOT_LEGAL,
         "Legal but no capture": gi.GrandSlam.NO_CAPT,
         "Legal but opp takes remaining": gi.GrandSlam.OPP_GETS_REMAIN,
         "Legal but leave leftmost": gi.GrandSlam.LEAVE_LEFT,
         "Legal but leave rightmost": gi.GrandSlam.LEAVE_RIGHT}),

    'LapSower': lookup_dicts(
        gi.LapSower,
        {'Single sow': gi.LapSower.OFF,
         'Lap Sower (end)': gi.LapSower.LAPPER,
         'Lap Sower Next': gi.LapSower.LAPPER_NEXT}),

    'RoundFill': lookup_dicts(
        gi.RoundFill,
        {'Not Applicable': gi.RoundFill.NOT_APPLICABLE,
         'Left Fill': gi.RoundFill.LEFT_FILL,
         'Right Fill': gi.RoundFill.RIGHT_FILL,
         'Outside In Fill': gi.RoundFill.OUTSIDE_FILL,
         'Even Fill': gi.RoundFill.EVEN_FILL,
         'Shorten Board': gi.RoundFill.SHORTEN,
         'Choose Blocks': gi.RoundFill.UCHOOSE,
         'Rearrange Seeds': gi.RoundFill.UMOVE}),

    'RoundStarter': lookup_dicts(
        gi.RoundStarter,
        {'Alternate': gi.RoundStarter.ALTERNATE,
         'Round Winner': gi.RoundStarter.WINNER,
         'Round Loser': gi.RoundStarter.LOSER,
         'Last Mover': gi.RoundStarter.LAST_MOVER}),

    'SowPrescribed': lookup_dicts(
        gi.SowPrescribed,
        {'None': gi.SowPrescribed.NONE,
         'Sow Basic First': gi.SowPrescribed.BASIC_SOWER,
         'Sow Mlaps First': gi.SowPrescribed.MLAPS_SOWER,
         'Sow One Opposite': gi.SowPrescribed.SOW1OPP,
         'Plus 1, Minus 1': gi.SowPrescribed.PLUS1MINUS1,
         'Arrange or Limit ch & capts': gi.SowPrescribed.ARNGE_LIMIT}),

    'SowRule': lookup_dicts(
        gi.SowRule,
        {"No Special Rule": gi.SowRule.NONE,
         "Close, Skip Own, Capt Opp": gi.SowRule.SOW_BLKD_DIV,
         "Close, Skip, Capt; (not right)": gi.SowRule.SOW_BLKD_DIV_NR,
         "Owners Capture all while Sow": gi.SowRule.OWN_SOW_CAPT_ALL,
         "Sower Captures own while Sow": gi.SowRule.SOW_SOW_CAPT_ALL,
         "Don't sow Opp holes w/2s": gi.SowRule.NO_SOW_OPP_2S,
         "Change Direction each Lap": gi.SowRule.CHANGE_DIR_LAP,
         }),

    'StartPattern': lookup_dicts(
        gi.StartPattern,
        {'All Equal': gi.StartPattern.ALL_EQUAL,
         'Gamacha': gi.StartPattern.GAMACHA,
         'Alternates': gi.StartPattern.ALTERNATES,
         'Alts with 1': gi.StartPattern.ALTS_WITH_1,
         'Clipped Triples': gi.StartPattern.CLIPPEDTRIPLES,
         'Two Empty': gi.StartPattern.TWOEMPTY}),

}
