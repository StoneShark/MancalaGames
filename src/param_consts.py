# -*- coding: utf-8 -*-
"""Constants for the UI and in the param config table.

Created on Fri Oct 27 16:54:51 2023
@author: Ann"""


# %% import

import collections

import game_info as gi

from ai_player import ALGORITHM_DICT
from game_classes import GAME_CLASSES


# %% types from the params file

INT_TYPE = 'int'
STR_TYPE = 'str'
BOOL_TYPE = 'bool'
MSTR_TYPE = 'multi_str'
BLIST_TYPE = 'list[bool]'
ILIST_TYPE = 'list[int]'

LABEL_TYPE = 'label'   # just a label, no value or param


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
         'End in Occupied hole (1st lap)': gi.AllowRule.OCCUPIED,
         'End Empty or Opp Side (1st lap)': gi.AllowRule.OPP_OR_EMPTY,
         'Singles to Empties': gi.AllowRule.SINGLE_TO_ZERO,
         'Singles only when all single': gi.AllowRule.SINGLE_ONLY_ALL,
         'Singles when all & to Empty': gi.AllowRule.SINGLE_ALL_TO_ZERO,
         'Doubles only when all doubles': gi.AllowRule.TWO_ONLY_ALL,
         'Doubles, all doubles, rightmost': gi.AllowRule.TWO_ONLY_ALL_RIGHT,
         'Rightmost two on first turn':
             gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
         'Right 2 1st, then twos only if all 2s':
             gi.AllowRule.RIGHT_2_1ST_THEN_ALL_TWO,
         'Move from all holes once first':
             gi.AllowRule.MOVE_ALL_HOLES_FIRST,
         'Not across from 1s': gi.AllowRule.NOT_XFROM_1S,
         'Right Half 1st Moves': gi.AllowRule.RIGHT_HALF_FIRSTS,
         'Right Half 1sts; Opp or Empty': gi.AllowRule.RIGHT_HALF_1ST_OPE,
         }),

    'CaptExtraPick': lookup_dicts(
        gi.CaptExtraPick,
        {'No additional': gi.CaptExtraPick.NONE,
         'Pick Cross Seeds': gi.CaptExtraPick.PICKCROSS,
         'Pick Cross Seeds Multi': gi.CaptExtraPick.PICKCROSSMULT,
         "Pick all Opponent's' 2s": gi.CaptExtraPick.PICKTWOS,
         "Pick last seeds <= nbr_start": gi.CaptExtraPick.PICKLASTSEEDS,
         "Pick last seeds <= 2x nbr_start": gi.CaptExtraPick.PICK2XLASTSEEDS,
         "Pick Final Hole": gi.CaptExtraPick.PICKFINAL}),

    'CaptRTurn': lookup_dicts(
        gi.CaptRTurn,
        {"No Repeat": gi.CaptRTurn.NO_REPEAT,
         "One Repeat": gi.CaptRTurn.ONCE,
         "Unlimited": gi.CaptRTurn.ALWAYS}),

    'CaptSide': lookup_dicts(
        gi.CaptSide,
        {'BOTH': gi.CaptSide.BOTH,
         'Opposite': gi.CaptSide.OPP_SIDE,
         'Own': gi.CaptSide.OWN_SIDE,
         'First Opp, then either': gi.CaptSide.OPP_CONT,
         'First Own, then either': gi.CaptSide.OWN_CONT,
         "Opponent's Territory": gi.CaptSide.OPP_TERR,
         'Own Territory': gi.CaptSide.OWN_TERR}),

    'CaptType': lookup_dicts(
        gi.CaptType,
        {'None': gi.CaptType.NONE,
         'Next Hole': gi.CaptType.NEXT,
         'Two Out (across gap)': gi.CaptType.TWO_OUT,
         'Match Opposite Side': gi.CaptType.MATCH_OPP,
         'All Singletons': gi.CaptType.SINGLETONS}),

    'ChildLocs': lookup_dicts(
        gi.ChildLocs,
        {'Anywhere': gi.ChildLocs.ANYWHERE,
         'Ends Only': gi.ChildLocs.ENDS_ONLY,
         'Not Ends': gi.ChildLocs.NO_ENDS,
         'Opposite Ends plus all own inner': gi.ChildLocs.INV_ENDS_PLUS_MID,
         'Any end holes plus next two inner': gi.ChildLocs.ENDS_PLUS_ONE_OPP,
         'No own rightmost': gi.ChildLocs.NO_OWN_RIGHT,
         'No opposite rightmost': gi.ChildLocs.NO_OPP_RIGHT,
         'No opposite leftmost': gi.ChildLocs.NO_OPP_LEFT,
         'Not Symetrically Opposite': gi.ChildLocs.NOT_SYM_OPP,
         'Not Facing': gi.ChildLocs.NOT_FACING,
         'Ends plus all opposite': gi.ChildLocs.ENDS_PLUS_ALL_OPP,
         "Fixed: 1 child in right hole": gi.ChildLocs.FIXED_ONE_RIGHT,
         }),

    'ChildType': lookup_dicts(
        gi.ChildType,
        {'No Children': gi.ChildType.NOCHILD,
         'Normal': gi.ChildType.NORMAL,
         'One Child': gi.ChildType.ONE_CHILD,
         'Weg / Daughter': gi.ChildType.WEG,
         'Bull': gi.ChildType.BULL,
         'Qur': gi.ChildType.QUR}),

    'ChildRule': lookup_dicts(
        gi.ChildRule,
        {'No additional restrictions': gi.ChildRule.NONE,
         'Opposite Side Only': gi.ChildRule.OPP_SIDE_ONLY,
         'Own Side Only': gi.ChildRule.OWN_SIDE_ONLY,
         'Opp Only and not 1st w/One': gi.ChildRule.OPPS_ONLY_NOT_1ST,
         'Opposite Territory Only': gi.ChildRule.OPP_OWNER_ONLY,
         'Own Territory Only': gi.ChildRule.OWN_OWNER_ONLY,
         'Not 1st Opposite with 1': gi.ChildRule.NOT_1ST_OPP,
         }),

    'CrossCaptOwn': lookup_dicts(
        gi.CrossCaptOwn,
        {'Leave': gi.CrossCaptOwn.LEAVE,
         'Pick on Capture': gi.CrossCaptOwn.PICK_ON_CAPT,
         'Alway Pick': gi.CrossCaptOwn.ALWAYS_PICK}),

    'Direct': lookup_dicts(
        gi.Direct,
        {'Clockwise': gi.Direct.CW,
         'Counter-clockwise': gi.Direct.CCW,
         'Split': gi.Direct.SPLIT,
         'To Center Line': gi.Direct.TOCENTER,
         'Players Alternate': gi.Direct.PLAYALTDIR,
         'Odd Seeds-CCW Even-CW': gi.Direct.EVEN_ODD_DIR}),

    'EndGameSeeds': lookup_dicts(
        gi.EndGameSeeds,
        {'Hole Owner': gi.EndGameSeeds.HOLE_OWNER,
         'Not Scored': gi.EndGameSeeds.DONT_SCORE,
         'Last Mover': gi.EndGameSeeds.LAST_MOVER,
         'Unfed Player': gi.EndGameSeeds.UNFED_PLAYER,
         'Divvied Equally': gi.EndGameSeeds.DIVVIED,
            }),

    'GameClasses': lookup_strs(GAME_CLASSES.keys()),

    'Goal': lookup_dicts(
        gi.Goal,
        {'Max Seeds': gi.Goal.MAX_SEEDS,
         'Clear Own': gi.Goal.CLEAR,
         'Deprive Opponent': gi.Goal.DEPRIVE,
         'Territory': gi.Goal.TERRITORY,
         'Immobilize Opponent': gi.Goal.IMMOBILIZE,
         'Collect total seeds': gi.Goal.RND_SEED_COUNT,
         'Collect extra seeds': gi.Goal.RND_EXTRA_SEEDS,
         'Score Points': gi.Goal.RND_POINTS,
         'Win Rounds (max seeds)': gi.Goal.RND_WIN_COUNT_MAX,
         'Win Rounds (clear)': gi.Goal.RND_WIN_COUNT_CLR,
         'Win Rounds (deprive)': gi.Goal.RND_WIN_COUNT_DEP,
         'Win Rounds (immobilize)': gi.Goal.RND_WIN_COUNT_IMB,
         }),

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

    'PreSowCapt': lookup_dicts(
        gi.PreSowCapt,
        {'No PreSow Capture': gi.PreSowCapt.NONE,
         'Capture 1 seed (per lap)': gi.PreSowCapt.CAPT_ONE,
         'Capture across from all 1s': gi.PreSowCapt.ALL_SINGLE_XCAPT,
         'Cross capture when drawing 1': gi.PreSowCapt.DRAW_1_XCAPT,
        }),

    'Rounds': lookup_dicts(
        gi.Rounds,
        {'Not Played in Rounds': gi.Rounds.NO_ROUNDS,
         'Half seeds ends Rounds': gi.Rounds.HALF_SEEDS,
         'No Moves': gi.Rounds.NO_MOVES,
         'End when start seeds left': gi.Rounds.END_S_SEEDS,
         'End when 2x start seeds left': gi.Rounds.END_2S_SEEDS,
         }),

    'RoundFill': lookup_dicts(
        gi.RoundFill,
        {'Not Applicable': gi.RoundFill.NOT_APPLICABLE,
         'Left Fill': gi.RoundFill.LEFT_FILL,
         'Right Fill': gi.RoundFill.RIGHT_FILL,
         'Outside In Fill': gi.RoundFill.OUTSIDE_FILL,
         'Even Fill': gi.RoundFill.EVEN_FILL,
         'Shorten Board': gi.RoundFill.SHORTEN,
         'Choose Blocks': gi.RoundFill.UCHOOSE,
         'Rearrange Seeds': gi.RoundFill.UMOVE,
         'Winner Chooses Owners': gi.RoundFill.UCHOWN}),

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
         "Sower Captures while Sow from captside(s)": gi.SowRule.SOW_CAPT_ALL,
         "Don't sow Opp holes w/sow_param seeds": gi.SowRule.NO_SOW_OPP_NS,
         "Change Direction each Lap": gi.SowRule.CHANGE_DIR_LAP,
         "Never sow holes above sow_param": gi.SowRule.MAX_SOW,
         "Do captures on each lap (lap_capt)": gi.SowRule.LAP_CAPT,
         "Lap Capt, sow with capt'ed seeds": gi.SowRule.LAP_CAPT_SEEDS,
         "Lap Capt Then Opp takes Own (< sow_param)":
             gi.SowRule.LAP_CAPT_OPP_GETS,
         "Do not sow opponents children": gi.SowRule.NO_OPP_CHILD,
         "Don't sow opp children unless final seed": gi.SowRule.OPP_CHILD_ONLY1,
         "Continue lap sow only on sow_param seeds": gi.SowRule.CONT_LAP_ON,
         "Continue lap sow when >= sow_param seeds": gi.SowRule.CONT_LAP_GREQ,
         }),

    'StartPattern': lookup_dicts(
        gi.StartPattern,
        {'All Equal': gi.StartPattern.ALL_EQUAL,
         'Gamacha': gi.StartPattern.GAMACHA,
         'Alternates': gi.StartPattern.ALTERNATES,
         'Alts with 1': gi.StartPattern.ALTS_WITH_1,
         'Clipped Triples': gi.StartPattern.CLIPPEDTRIPLES,
         'Two Empty': gi.StartPattern.TWOEMPTY,
         'Alts Split Right': gi.StartPattern.ALTS_SPLIT,
         'Equal plus one in Right': gi.StartPattern.RIGHTMOST_PLUS_ONE,
         'No Repeat Sow Own': gi.StartPattern.NO_REPEAT_SOW_OWN,
         'Random': gi.StartPattern.RANDOM,
         'Random Move': gi.StartPattern.MOVE_RANDOM,
         'Move Rightmost Hole': gi.StartPattern.MOVE_RIGHTMOST,
         }),

}
