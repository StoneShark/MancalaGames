# -*- coding: utf-8 -*-
"""A class to enforce rules on the values in GameInfo.

Each game class should have a 'rules' variable that is
a RuleDict to enforce reasonable values for the
game_info data.  The RuleDict is class scope so that
GameInfo can get the rules in it's construction before
the actual game class is instantiated.

This allows the default set of rules for the Mancala
class to be defined below. Then classes derived from
Mancala can add, change or delete rules.

Created on Mon Aug 21 06:54:24 2023
@author: Ann"""

# pylint: disable=too-many-lines

import collections
import dataclasses as dc
import warnings

import game_interface as gi
import round_tally

from fill_patterns import PCLASSES


# %% constants

DIFF_LEVELS = 4
MAX_MIN_MOVES = 5
MAX_MINIMAX_DEPTH = 15

PRINT_MSG = 'print msg'


# %% rule classes

@dc.dataclass(frozen=True)
class ParamRule:
    """An individual rule to apply to GameInfo.

    name: dictionary key for rule
          an message is printed if the name is reused
    rule: a function or lambda that takes 1 or 2 params
          should return True if there is an error
    warn: if PRINT_MSG, will print a message to console (too early to
          be put into a game log)
          if True, genearte a warning, else an exception
    excp: if generating an exception, generate this exception
    both_objs: if True, call with obj1 and obj2, otherwise only obj1"""

    name: str
    rule: collections.abc.Callable
    msg: str
    warn: bool = False
    excp: object = None
    both_objs: bool = False

    def test(self, obj1, obj2):
        """Test the rule, do the action if it returns true."""

        error = self.rule(obj1, obj2) if self.both_objs else self.rule(obj1)
        if error:
            msg = self.msg + f' ({self.name}).'
            if self.warn == PRINT_MSG:
                print('\n*** Gentle Warning:  ', msg)
            elif self.warn:
                warnings.warn(msg)
            else:
                raise self.excp(msg)


class RuleDict(dict):
    """A dictionary of game rules."""

    def add_rule(self, name, *, rule, msg,
                 both_objs=False, warn=False, excp=None):
        """Add a rule to the dictionary."""
        # pylint: disable=too-many-arguments

        if not warn and not excp:
            print(f'Rule {name} has no effect.')

        if name in self:
            print(f'Rule {name} being replaced.')

        self[name] = ParamRule(name, both_objs=both_objs, rule=rule, msg=msg,
                                  warn=warn, excp=excp)


    def test(self, obj1, obj2):
        """Test each of the rules."""

        for rule in self.values():
            rule.test(obj1, obj2)


# %%

def sow_blkd_div(ginfo):
    """Test if either of the sow_blkd_div rules."""
    return (ginfo.sow_rule in
            (gi.SowRule.SOW_BLKD_DIV, gi.SowRule.SOW_BLKD_DIV_NR))


# %% grouped rules

def add_creation_rules(rules):
    """Basic rules to make sure that everything that should exist does."""

    rules.add_rule(
        'invalid_holes',
        both_objs=True,
        rule=lambda ginfo, holes: (not holes or not isinstance(holes, int)),
        msg='Holes must > 0',
        excp=gi.GameInfoError)

    rules.add_rule(
        'missing_name',
        rule=lambda ginfo: not ginfo.name,
        msg='Mising Name',
        excp=gi.GameInfoError)

    rules.add_rule(
        'sow_dir_type',
        rule=lambda ginfo: not isinstance(ginfo.sow_direct, gi.Direct),
        msg='SOW_DIRECT not valid type, expected gi.Direct',
        excp=gi.GameInfoError)

    rules.add_rule(
        'high_min_moves',
        both_objs=True,
        rule=lambda ginfo, holes: not 1 <= ginfo.min_move <= min(holes, MAX_MIN_MOVES),
        msg=f'Min_move seems wrong (1<= convention <= min(holes, {MAX_MIN_MOVES}))',
        excp=gi.GameInfoError)
        # First, convenstion. Second, the even fill round ender
        # assumes that min move is <= holes


def add_pattern_rules(rules):
    """Add a rule for each pattern to check the number of holes."""

    def test_pattern(index, pattern):
        """Return a function that tests that the pattern is index
        and tests the size_ok function."""

        def _pattern(ginfo, holes):
            return ginfo.start_pattern == index and not pattern.size_ok(holes)

        return _pattern

    for idx, pat in enumerate(PCLASSES):
        if not pat:
            continue

        rules.add_rule(
            f'pattern_{idx}_req_size',
            both_objs=True,
            rule=test_pattern(idx, pat),
            msg=pat.err_msg,
            excp=gi.GameInfoError)

    rules.add_rule(
        'pattern_bad_fills',
        rule=lambda ginfo: (ginfo.start_pattern
                            and ginfo.round_fill
                                    not in (gi.RoundFill.NOT_APPLICABLE,
                                            gi.RoundFill.UCHOWN)),
        msg='START_PATTERN is incompatible for the selected ROUND_FILL',
        excp=gi.GameInfoError)

    rules.add_rule(
        'pattern_bad_rgoals',
        rule=lambda ginfo: (ginfo.start_pattern
                            and ginfo.rounds
                            and ginfo.goal not in
                                    round_tally.RoundTally.GOALS
                                    | {gi.Goal.TERRITORY}),
        msg='START_PATTERN is incompatible for ROUNDS with selected GOAL',
        excp=gi.GameInfoError)

    rules.add_rule(
        'move_rmost_mlength',
        rule=lambda ginfo: (ginfo.start_pattern ==
                                gi.StartPattern.MOVE_RIGHTMOST
                            and ginfo.mlength > 1),
        msg='START_PATTERN of MOVE_RIGHTMOST is incompatible with ' \
            'territory GOAL, SPLIT sow, user directed sow direction, ' \
            'and NO_SIDES (mlength > 1)',
        excp=gi.GameInfoError)
        # would need to define what the sow direction should be if split sow
        # no_sides without split sow could be supported but not supporting
        # makes code the simpler (uncondition move type)


def add_elim_seeds_goal_rules(rules):
    """Add rules for the game eliminating our own or opponents seeds."""

    def _dep_clr_and(flag_name):
        """Return a function that tests that goal is divert
        and the specified flag, based only on a ginfo parameter."""

        def _dep_clr_and(ginfo):
            return (ginfo.goal in (gi.Goal.DEPRIVE,
                                   gi.Goal.CLEAR,
                                   gi.Goal.RND_WIN_COUNT_CLR,
                                   gi.Goal.RND_WIN_COUNT_DEP)
                    and getattr(ginfo, flag_name))

        return _dep_clr_and

    rules.add_rule(
        'elseed_gs_legal',
        rule=lambda ginfo: (ginfo.goal in (gi.Goal.DEPRIVE,
                                           gi.Goal.CLEAR,
                                           gi.Goal.RND_WIN_COUNT_CLR,
                                           gi.Goal.RND_WIN_COUNT_DEP)
                            and ginfo.grandslam != gi.GrandSlam.LEGAL),
        msg='CLEAR & DEPRIVE games require that GRANDSLAM be Legal',
        excp=gi.GameInfoError)

    bad_flags = ['child_type', 'child_cvt', 'child_rule',
                 'moveunlock', 'mustshare', 'mustpass']
    for flag in bad_flags:
        rules.add_rule(
            f'elseed_bad_{flag}',
            rule=_dep_clr_and(flag),
            msg=f'CLEAR & DEPRIVE games cannot be used with {flag.upper()}',
            excp=gi.GameInfoError)

    rules.add_rule(
        'elseed_no_rounds',
        rule=lambda ginfo: (ginfo.goal in (gi.Goal.CLEAR, gi.Goal.DEPRIVE)
                            and ginfo.rounds),
        msg="""Goals CLEAR and DEPRIVE cannot be played in rounds.
            Consider the Round Tally goals""",
            excp=gi.GameInfoError)

    rules.add_rule(
        'elseed_no_moves',
        rule=lambda ginfo: (ginfo.goal in (gi.Goal.RND_WIN_COUNT_CLR,
                                           gi.Goal.RND_WIN_COUNT_DEP)
                            and ginfo.rounds != gi.Rounds.NO_MOVES),
        msg="""Goals RND_WIN_COUNT_CLR and RND_WIN_COUNT_DEP
            require ROUNDS to be NO_MOVES""",
            excp=gi.GameInfoError)

    rules.add_rule(
        'deprive_mmgr1_rturn',
        rule=lambda ginfo: (ginfo.goal in (gi.Goal.DEPRIVE,
                                           gi.Goal.RND_WIN_COUNT_DEP)
                            and ginfo.min_move > 1
                            and (ginfo.capt_rturn or ginfo.sow_own_store)),
        msg='DEPRIVE games with min_move > 1 cannot use repeat turn',
        excp=gi.GameInfoError)
        # min_move > 1 for DEPRIVE => last mover wins
        # but what if there is a repeat turn?
        #    F moves, giving away all seeds,
        #    they were the last mover (F win?), but can't move again (T win?)
        # who should win?  just don't allow it

    rules.add_rule(
        'clear_no_min_move',
        rule=lambda ginfo: (ginfo.goal in (gi.Goal.CLEAR,
                                           gi.Goal.RND_WIN_COUNT_CLR)
                            and ginfo.min_move != 1),
        msg='CLEAR games require that MIN_MOVE be 1',
        excp=gi.GameInfoError)
        # clear game, if there are seeds they must be playable

    rules.add_rule(
        'clear_no_prevent',
        rule=lambda ginfo: (
            ginfo.goal in (gi.Goal.CLEAR, gi.Goal.RND_WIN_COUNT_CLR)
            and ginfo.allow_rule in (gi.AllowRule.SINGLE_TO_ZERO,
                                     gi.AllowRule.SINGLE_ALL_TO_ZERO,
                                     gi.AllowRule.NOT_XFROM_1S,
                                     gi.AllowRule.OCCUPIED)),
        msg="""CLEAR games prohibit the selected allow rule.
            If a player has seeds, they must be able to play""",
        excp=gi.GameInfoError)
        # clear game, if there are seeds they must be playable

    return rules


def add_territory_rules(rules):
    """Add the rules for games with a goal of territory."""

    rules.add_rule(
        'terr_goal_param',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.goal == gi.Goal.TERRITORY
                                   and (ginfo.goal_param <= holes
                                        or ginfo.goal_param > 2 * holes)),
        msg='Territory Goal requires GOAL_PARAM between holes and 2 * holes',
        excp=gi.GameInfoError)

    rules.add_rule(
        'terr_need_stores',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and not ginfo.stores),
        msg='Territory goal requires stores',
        excp=gi.GameInfoError)

    rules.add_rule(
        'terr_no_sides_incomp',
        rule=lambda ginfo: ginfo.goal == gi.Goal.TERRITORY and ginfo.no_sides,
        msg='Territory goal is incompatible with NO_SIDES',
        excp=gi.GameInfoError)
        # XXXX could initial ownship be changed so that no_sides makes sense

    rules.add_rule(
        'terr_capt_side',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and ginfo.capt_side in (gi.CaptSide.OPP_SIDE,
                                                    gi.CaptSide.OWN_SIDE,
                                                    gi.CaptSide.OPP_CONT,
                                                    gi.CaptSide.OWN_CONT)),
        msg='CAPT_SIDE based on board location is odd for Territory games',
        warn=True)

    rules.add_rule(
        'capt_terr',
        rule=lambda ginfo: (ginfo.goal != gi.Goal.TERRITORY
                            and ginfo.capt_side in (gi.CaptSide.OPP_TERR,
                                                    gi.CaptSide.OWN_TERR)),
        msg='CAPT_SIDE based on hole ownership is only valid for Territory games',
        excp=gi.GameInfoError)

    rules.add_rule(
        'terr_no_rfill',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and ginfo.round_fill not in (gi.RoundFill.NOT_APPLICABLE,
                                                         gi.RoundFill.UCHOWN)),
        msg='Round Fill is ignored for Territory goal',
        warn=True)

    rules.add_rule(
        'uchown_terr_only',
        rule=lambda ginfo: (ginfo.goal != gi.Goal.TERRITORY
                            and ginfo.round_fill == gi.RoundFill.UCHOWN),
        msg='Round Fill UCHOWN is only supported for Territory goal',
        excp=gi.GameInfoError)

    rules.add_rule(
        'terr_gs_not',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and ginfo.grandslam == gi.GrandSlam.NOT_LEGAL),
        msg='Territory goal and GRANDLAM=Not Legal are currently incompatible',
        excp=NotImplementedError)
        # territory requires move triples, GS allowables doesn't support

    rules.add_rule(
        'terr_no_fchild',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and ginfo.child_locs == gi.ChildLocs.FIXED_ONE_RIGHT),
        msg='Territory goal and fixed children in incompatible',
        excp=NotImplementedError)
        # player might not own the child hole

    rules.add_rule(
        'terr_half_rounds',
        rule=lambda ginfo: (ginfo.goal == gi.Goal.TERRITORY
                            and ginfo.rounds == gi.Rounds.HALF_SEEDS),
        msg='Territory goal is incompatible with ROUNDS.HALF_SEEDS',
        excp=gi.GameInfoError)
        # half seeds would lead to endless territory games
        # most seeds must be moved out of play for territory games

    rules.add_rule(
        'terr_gparam_high',
        both_objs=True,
        rule=lambda ginfo, nbr_holes: (
            ginfo.goal == gi.Goal.TERRITORY
            and ginfo.unclaimed == gi.EndGameSeeds.DONT_SCORE
            and ((ginfo.rounds == gi.Rounds.END_S_SEEDS
                  and ginfo.goal_param > (nbr_holes * 2) - 1)
                 or (ginfo.rounds == gi.Rounds.END_2S_SEEDS
                     and ginfo.goal_param > (nbr_holes * 2) - 2))),
        msg='Territory goal param is too high for ROUNDS of DONT_SCORE, '
            'a game winner is unlikely',
        excp=gi.GameInfoError)


def add_block_and_divert_rules(rules):
    """sow_blkd_div is implemented primarily by the sower and the
    capturer is not used (capt mechanisms not supported). Add rules
    to ensure the right corresponding flags are used (or not used).

    This concept was originally part of Deka which was a DEPRIVE
    goal, not requiring that here."""

    def divert_and(flag_name):
        """Return a function that the divert option and the specified
        flag, based only on a ginfo parameter."""

        def _divert_and(ginfo):
            return (sow_blkd_div(ginfo)
                    and getattr(ginfo, flag_name))

        return _divert_and

    rules.add_rule(
        'next_ml_no_bdiv',
        rule=lambda ginfo: (ginfo.mlaps == gi.LapSower.LAPPER_NEXT
                            and sow_blkd_div(ginfo)),
        msg='MLAPS of LAPPER_NEXT is not supported with SOW_BLKD_DIV(_NR)',
        excp=NotImplementedError)

    rules.add_rule(
        'bdiv_need_gparam',
        rule=lambda ginfo: (sow_blkd_div(ginfo)
                            and not ginfo.sow_param),
        msg='SOW_BLKD_DIV(_NR) requires SOW_PARAM for closing holes',
        excp=gi.GameInfoError)

    rules.add_rule(
        'bdiv_need_blocks',
        rule=lambda ginfo: (sow_blkd_div(ginfo)
                            and not ginfo.blocks),
        msg='SOW_BLKD_DIV(_NR) requires BLOCKS for closing holes',
        excp=gi.GameInfoError)

    rules.add_rule(
        'bdiv_req_dep_goal',
        rule=lambda ginfo: (sow_blkd_div(ginfo)
                            and ginfo.goal not in (gi.Goal.DEPRIVE,
                                                   gi.Goal.RND_WIN_COUNT_DEP)),
        msg='SOW_BLKD_DIV(_NR) requires a DEPRIVE goal',
        excp=gi.GameInfoError)

    capt_flags = ['capsamedir', 'capt_max', 'capt_min', 'capt_type',
                  'capt_on', 'capt_rturn', 'crosscapt',
                  'evens', 'multicapt',
                  'nosinglecapt', 'capt_side', 'pickextra', 'xcpickown']
    for flag in capt_flags:
        rules.add_rule(
            f'bdiv_nocapt_{flag}',
            rule=divert_and(flag),
            msg='SOW_BLKD_DIV(_NR) closes holes to remove seeds from play, '
                f'no other capture mechanisms are allowed [{flag.upper()}]',
        excp=gi.GameInfoError)

    rules.add_rule(
        'bdiv_no_capt_on',
        rule=lambda ginfo: (sow_blkd_div(ginfo)
                            and any(ginfo.capt_on)),
        msg='SOW_BLKD_DIV(_NR) closes holes to remove seeds from play, ' + \
            'no other capture mechanisms are allowed [CAPT_ON]',
        excp=gi.GameInfoError)

    bad_flags = ['allow_rule', 'sow_start']
    for flag in bad_flags:
        rules.add_rule(
            f'bdiv_bad_{flag}',
            rule=divert_and(flag),
            msg=f'sow_blkd_div is incompatible with {flag.upper()}',
            excp=gi.GameInfoError)

    bad_flags = ['skip_start', 'visit_opp']
    for flag in bad_flags:
        rules.add_rule(
            f'bdiv_not_{flag}',
            rule=divert_and(flag),
            msg=f'sow_blkd_div is not supported with {flag.upper()}',
            excp=NotImplementedError)
    # sower doesn't use incrementer which implements skip_start
    # visit_opp cuz the DivertSkipBlckdSower sower comment says so


def add_child_rules(rules):
    """Add rules specific to having children."""

    rules.add_rule(
        'next_ml_nochild',
        rule=lambda ginfo: (ginfo.mlaps == gi.LapSower.LAPPER_NEXT
                            and ginfo.child_type),
        msg='MLAPS of LAPPER_NEXT is not supported with CHILD',
        excp=NotImplementedError)
        # StopOnChild would need to change and ChildLapCont would
        # need to be integrated into the lap continuer chain

    rules.add_rule(
        'child_need_cvt',
        rule=lambda ginfo: (ginfo.child_type
                            and ginfo.child_locs
                                    != gi.ChildLocs.FIXED_ONE_RIGHT
                            and not ginfo.child_cvt),
        msg='Selected child type requires CHILD_CVT',
        excp=gi.GameInfoError)

    rules.add_rule(
        'dont_need_cvt',
        rule=lambda ginfo: (ginfo.child_type
                            and ginfo.child_locs
                                    == gi.ChildLocs.FIXED_ONE_RIGHT
                            and ginfo.child_cvt),
        msg='CHILD_CVT is ignored with Child Locs of FIXED_ONE_RIGHT',
        warn=True)

    rules.add_rule(
        'child_cvt_need_type',
        rule=lambda ginfo: not ginfo.child_type and ginfo.child_cvt,
        msg='CHILD_CVT requires a CHILD_TYPE != NOCHILD',
        excp=gi.GameInfoError)

    rules.add_rule(
        'child_no_gs',
        rule=lambda ginfo: (ginfo.child_type
                            and ginfo.grandslam != gi.GrandSlam.LEGAL),
        msg='Children requires that GRANDSLAM be Legal',
        excp=NotImplementedError)
    # NOT_LEGAL is now supported, others are not

    rules.add_rule(
        'ch_rule_own_incom',
        rule=lambda ginfo: (ginfo.goal != gi.Goal.TERRITORY
                            and ginfo.child_rule in (gi.ChildRule.OPP_OWNER_ONLY,
                                                     gi.ChildRule.OWN_OWNER_ONLY)),
        msg='CHILD_RULE: *_OWNER_ONLY requires territory GOAL',
        excp=gi.GameInfoError)

    rules.add_rule(
        'no_opp_child_req',
        rule=lambda ginfo: (not ginfo.child_type
                            and ginfo.sow_rule == gi.SowRule.NO_OPP_CHILD),
        msg='Sow rule NO_OPP_CHILD requires children',
        excp=gi.GameInfoError)

    rules.add_rule(
        'not1st_static',
        rule=lambda ginfo: (ginfo.child_rule == gi.ChildRule.NOT_1ST_OPP
                            and (ginfo.blocks
                                 or ginfo.goal == gi.Goal.TERRITORY)),
        msg='ChildRule NOT_1ST_OPP not supported with blocks or territory games',
        excp=NotImplementedError)
        # code assumes 1st's are specific holes
        # complexity of 'current' 1st opposite hole is not implemented
        # for reference: sow own store does have this complexity


def add_no_sides_rules(rules):
    """Add the no_sides rules."""

    def no_sides_and(flag_name):
        """Return a function that tests no_sides and the specified
        flag, based only on a ginfo parameter."""

        def _no_sides_and(ginfo):
            return ginfo.no_sides and getattr(ginfo, flag_name)

        return _no_sides_and

    rules.add_rule(
        'no_sides_need_stores',
        rule=lambda ginfo: ginfo.no_sides and not ginfo.stores,
        msg='NO_SIDES requires STORES',
        excp=gi.GameInfoError)

    bad_flags = ['grandslam', 'mustpass', 'mustshare', 'capt_side',
                 'rounds', 'round_starter', 'round_fill',
                 'visit_opp']
    for flag in bad_flags:
        rules.add_rule(
            f'no_sides_bad_{flag}',
            rule=no_sides_and(flag),
            msg=f'NO_SIDES cannot be used with {flag.upper()}',
            excp=gi.GameInfoError)


def add_capture_rules(rules):
    """Most of the capture rules are added here."""

    rules.add_rule(
        'warn_no_capt',
        rule=lambda ginfo: not any([sow_blkd_div(ginfo),
                                    ginfo.child_type,
                                    ginfo.capt_type,
                                    ginfo.evens,
                                    ginfo.crosscapt,
                                    ginfo.sow_own_store,
                                    ginfo.capt_max,
                                    ginfo.capt_min,
                                    ginfo.capt_on,
                                    ginfo.presowcapt]),
        msg='No capture mechanism provided',
        warn=True)

    rules.add_rule(
        'capt_no_place',
        rule=lambda ginfo: (ginfo.goal in (gi.Goal.MAX_SEEDS, gi.Goal.TERRITORY)
                            and not (ginfo.stores or ginfo.child_type)
                            and any([ginfo.capt_type,
                                     ginfo.evens,
                                     ginfo.crosscapt,
                                     ginfo.capt_max,
                                     ginfo.capt_min,
                                     ginfo.capt_on,
                                     ginfo.presowcapt])),
        msg="""The game has captures configured but there is no place
            to put captured seeds. Suggest stores or children be used""",
        warn=True)

    rules.add_rule(
        'capt_conflict',
        rule=lambda ginfo: any(
            [(ginfo.capt_min and ginfo.capt_max
                  and ginfo.capt_min > ginfo.capt_max),
             (ginfo.capt_on and ginfo.evens
                  and all(cval % 2 == 1 for cval in ginfo.capt_on)),
             (ginfo.capt_min and ginfo.capt_on
                  and max(ginfo.capt_on) < ginfo.capt_min),
             (ginfo.capt_max and ginfo.capt_on
                  and min(ginfo.capt_on) > ginfo.capt_max),
              ]),
        msg='Selected capture mechanisms conflict (no captures)',
        warn=True)
        # this doesn't catch all conflicts :(

    rules.add_rule(
        'xcapt_multi_same',
        rule=lambda ginfo: (ginfo.crosscapt and ginfo.multicapt
                            and not ginfo.capsamedir),
        msg="""CROSSCAPT with MULTICAPT without CAPSAMEDIR
            is the same as just CROSSCAPT""",
        warn=True)
        # capturing the opp dir (as usual) wont capture because
        # the preceeding holes were just sown, that is, not empty

    rules.add_rule(
        'warn_capsamedir_multicapt',
        rule=lambda ginfo: (ginfo.capt_type != gi.CaptType.TWO_OUT
                            and ginfo.capt_type != gi.CaptType.NEXT
                            and ginfo.capsamedir
                            and not ginfo.multicapt),
        msg="CAPSAMEDIR without MULTICAPT has no effect",
        warn=True)

    rules.add_rule(
        'capt2out_needs_samedir',
        rule=lambda ginfo: (ginfo.capt_type == gi.CaptType.TWO_OUT
                            and not ginfo.capsamedir),
        msg="""Capture type TWO_OUT requires CAPSAMEDIR because
            the preceeding holes were just sown (not empty)""",
        excp=gi.GameInfoError)

    rules.add_rule(
        'capttype_xcross_incomp',
        rule=lambda ginfo: ginfo.capt_type and ginfo.crosscapt,
        msg="CAPT_TYPE and CROSSCAPT are incompatible",
        warn=True)

    rules.add_rule(
        'lcapt_no_ctype',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.LAP_CAPT
                            and ginfo.capt_type not in (gi.CaptType.NONE,
                                                        gi.CaptType.TWO_OUT,
                                                        gi.CaptType.NEXT)),
        msg="""LAP_CAPT is only supported for basic captures,
            cross capture, capt two out, and capt next""",
        excp=NotImplementedError)
        # currently only MATCH_OPP is not supported

    rules.add_rule(
        'ogol_no_ctype',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.LAP_CAPT_OPP_GETS
                            and ginfo.capt_type not in (gi.CaptType.NONE,
                                                        gi.CaptType.TWO_OUT,
                                                        gi.CaptType.NEXT)),
        msg="""LAP_CAPT_OPP_GETS is only supported for basic captures,
            cross capture, capt two out, and capt next""",
        excp=NotImplementedError)
        # see lcapt_no_ctype

    rules.add_rule(
        'lcs_useful',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.LAP_CAPT_SEEDS
                            and not (ginfo.capt_type or ginfo.crosscapt)),
        msg="""LAP_CAPT_SEEDS is only supported when seeds are
            captured from holes in addition to final hole sown""",
        excp=gi.GameInfoError)
        # don't lap_capt_seeds if we are not capturing seeds from some
        # place other than the end hole, it does nothing useful

    rules.add_rule(
        'lcs_ctype_warn',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.LAP_CAPT_SEEDS
                            and ginfo.capt_type
                            and ginfo.capt_type != gi.CaptType.MATCH_OPP),
        msg="""LAP_CAPT_SEEDS with selected capture type will generally
            end result in an ENDLESS sow""",
        warn=True)
        # start pattern, prescribed sow, or other option could prevent this
        # making an actual warning because the gentle warning might be lost
        # above the endless sow log

    rules.add_rule(
        'sca_gs_not',
        rule=lambda ginfo: (ginfo.sow_rule in (gi.SowRule.OWN_SOW_CAPT_ALL,
                                               gi.SowRule.SOW_CAPT_ALL)
                            and ginfo.grandslam != gi.GrandSlam.LEGAL),
        msg='(OWN_)SOW_CAPT_ALL requires that GRANDLAM be LEGAL',
        excp=gi.GameInfoError)

    rules.add_rule(
        'xpick_requires_cross',
        rule=lambda ginfo: ginfo.xcpickown and not ginfo.crosscapt,
        msg="XCPICKOWN without CROSSCAPT doesn't do anything",
        excp=gi.GameInfoError)

    rules.add_rule(
        'xc_const_pickextra',
        rule=lambda ginfo: (ginfo.crosscapt
                            and any([ginfo.capt_max,
                                     ginfo.capt_min,
                                     ginfo.capt_on,
                                     ginfo.evens])
                            and ginfo.pickextra == gi.CaptExtraPick.PICKCROSS),
        msg="""A constrainted CROSSCAPT with PICKEXTRA=PICKCROSS will
            ingnore constraint""",
        excp=gi.GameInfoError)

    rules.add_rule(
        'xpick_pickcross',
        rule=lambda ginfo: (ginfo.crosscapt
                            and ginfo.pickextra == gi.CaptExtraPick.PICKCROSS),
        msg="PICKEXTRA=PICKCROSS with CROSSCAPT is redundant",
        warn=True)

    rules.add_rule(
        'moveall_no_locks',
        rule=lambda ginfo: (ginfo.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST
                            and ginfo.moveunlock),
        msg="""Do not set MOVEUNLOCK with MOVE_ALL_HOLES_FIRST.
            Locks are automatically used to limit first moves but not captures""",
        excp=gi.GameInfoError)
        # we do not want CaptUnlocked added to the capt_ok deco
        # which causes captures to be limited by locks

    rules.add_rule(
        'moveall_no_capttype',
        rule=lambda ginfo: (ginfo.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST
                            and ginfo.capt_type == gi.CaptType.TWO_OUT),
        msg='MOVE_ALL_HOLES_FIRST is incompatible with CAPT_TYPE TWO_OUT',
        excp=gi.GameInfoError)
        # decos do not use capt_ok, but checks the locks directly

    rules.add_rule(
        'moveall_no_picker',
        rule=lambda ginfo: (ginfo.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST
                            and (ginfo.xcpickown or ginfo.pickextra)),
        msg='MOVE_ALL_HOLES_FIRST is incompatible with all pickers',
        excp=gi.GameInfoError)
        # the pickers check the locks directly
        # an alternate approach could be to not check any locks on pickers
        # locks are rarely used

    rules.add_rule(
        'pcm_multi',
        rule=lambda ginfo: (ginfo.pickextra == gi.CaptExtraPick.PICKCROSSMULT
                            and not ginfo.multicapt),
        msg='PICKCROSSMULT does nothing without MULICAPT',
        excp=gi.GameInfoError)

    rules.add_rule(
        'scont_mcapt',
        rule=lambda ginfo: (ginfo.capt_side in (gi.CaptSide.OWN_CONT,
                                                gi.CaptSide.OPP_CONT)
                            and not ginfo.multicapt),
        msg='CAPT_SIDE *_CONT requires multicapt',
        excp=gi.GameInfoError)

    rules.add_rule(
        'capt2out_cside',
        rule=lambda ginfo: (ginfo.capt_side
                            and ginfo.capt_type == gi.CaptType.TWO_OUT),
        msg='Capture TWO_OUT cannot be used with CAPT_SIDE other than BOTH',
        excp=gi.GameInfoError)

    rules.add_rule(
        'singles_no_mult',
        rule=lambda ginfo: (ginfo.capt_type == gi.CaptType.SINGLETONS
                            and ginfo.multicapt),
        msg='Multiple captures with capture SINGLETONS is not supported',
        excp=gi.GameInfoError)



# %% the base ruleset

def build_rules():
    """Build the default Mancala rules.
    These can be deleted or modified by derived classes."""

    man_rules = RuleDict()

    add_creation_rules(man_rules)
    add_pattern_rules(man_rules)
    add_elim_seeds_goal_rules(man_rules)
    add_territory_rules(man_rules)
    add_block_and_divert_rules(man_rules)
    add_child_rules(man_rules)
    add_no_sides_rules(man_rules)
    add_capture_rules(man_rules)

    man_rules.add_rule(
        'allowrule_mlen3',
        rule=lambda ginfo: (ginfo.mlength == 3
                            and ginfo.allow_rule in
                                {gi.AllowRule.TWO_ONLY_ALL_RIGHT,
                                 gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
                                 gi.AllowRule.RIGHT_2_1ST_THEN_ALL_TWO,
                                 gi.AllowRule.NOT_XFROM_1S}),
        msg='Selected allow rule not supported for MLENGTH 3 games',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'opp_empty_no_tuples',
        rule=lambda ginfo: (ginfo.allow_rule == gi.AllowRule.OPP_OR_EMPTY
                            and ginfo.mlength > 1),
        msg='MLENGTH > 1 not supported with OPP_OR_EMPTY',
        excp=gi.GameInfoError)
        # UDIRECT: partials hole activation not supported
        # TERRITORY: what does it mean if the hole is already opp?

    man_rules.add_rule(
        'no_pres_opp_empty',
        rule=lambda ginfo: (ginfo.prescribed != gi.SowPrescribed.NONE
                            and ginfo.allow_rule == gi.AllowRule.OPP_OR_EMPTY),
        msg='Prescribed moves not supported with OPP_OR_EMPTY',
        excp=gi.GameInfoError)
        # don't know how to get the single_sower from a prescribed sow,
        # the don't have to follow a prescribed (pun intended) sow structure

    man_rules.add_rule(
        'sow_own_needs_stores',
        rule=lambda ginfo: ginfo.sow_own_store and not ginfo.stores,
        msg='SOW_OWN_STORE requires STORES',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'sow_own_nocapt',
        rule=lambda ginfo: ginfo.sow_own_store and ginfo.nocaptmoves,
        msg='SOW_OWN_STORE cannot be used with NOCAPTMOVES',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'sow_own_not_rules',
        rule=lambda ginfo: (ginfo.sow_own_store
                            and ginfo.sow_rule in
                                (gi.SowRule.OWN_SOW_CAPT_ALL,
                                 gi.SowRule.SOW_CAPT_ALL,
                                 gi.SowRule.NO_SOW_OPP_NS)),
        msg='SOW_OWN_STORE is not supported with the selected sow rule',
        excp=NotImplementedError)

    man_rules.add_rule(
        'no_opp_n_sparam',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.NO_SOW_OPP_NS
                            and not ginfo.sow_param),
        msg='NO_SOW_OPP_NS requires sow_param',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'max_sow_param',
        rule=lambda ginfo: (not ginfo.sow_param
                            and ginfo.sow_rule == gi.SowRule.MAX_SOW),
        msg='Sow rule MAX_SOW requires that sow_param be greater than 0',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'lcapt_no_lnext',
        rule=lambda ginfo: (ginfo.sow_rule in (gi.SowRule.LAP_CAPT,
                                               gi.SowRule.LAP_CAPT_OPP_GETS,
                                               gi.SowRule.LAP_CAPT_SEEDS)
                            and ginfo.mlaps == gi.LapSower.LAPPER_NEXT),
        msg="""SOW_RULE LAP_CAPT and variants are not supported
            with LAPPER_NEXT""",
        excp=NotImplementedError)
        # would need to carefully decide how it would work

    man_rules.add_rule(
        'ogol_no_lnext',
        rule=lambda ginfo: (ginfo.sow_rule == gi.SowRule.LAP_CAPT_OPP_GETS
                            and ginfo.mlaps == gi.LapSower.LAPPER_NEXT),
        msg='LAP_CAPT_OPP_GETS is not supported with LAPPER_NEXT',
        excp=NotImplementedError)

    man_rules.add_rule(
        'sow_own_prescribed',
        rule=lambda ginfo: (ginfo.sow_own_store
                            and ginfo.prescribed in
                                (gi.SowPrescribed.BASIC_SOWER,
                                 gi.SowPrescribed.MLAPS_SOWER,
                                 gi.SowPrescribed.SOW1OPP,
                                 gi.SowPrescribed.PLUS1MINUS1)
                            ),
        msg='SOW_OWN_STORE is ignored for the selected first prescribed sow',
        warn=True)

    man_rules.add_rule(
        'visit_opp_req_mlap',
        rule=lambda ginfo: ginfo.visit_opp and ginfo.mlaps == gi.LapSower.OFF,
        msg='VISIT_OPP requires MLAPS',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'sow_start_skip_incomp',
        rule=lambda ginfo: ginfo.sow_start and ginfo.skip_start,
        msg='SOW_START and SKIP_START do not make sense together',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'blocks_wo_rounds',
        rule=lambda ginfo: (ginfo.blocks
                            and not sow_blkd_div(ginfo)
                            and not ginfo.rounds),
        msg='BLOCKS without ROUNDS or SOW_BLKD_DIV(_NR) does nothing',
        warn=True)

    man_rules.add_rule(
        'rstarter_wo_rounds',
        rule=lambda ginfo: not ginfo.rounds
            and ginfo.round_starter != gi.RoundStarter.ALTERNATE,
        msg='ROUND_STARTER requires ROUNDS',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'mx_round_limit',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.rounds
                                   and ginfo.goal == gi.Goal.MAX_SEEDS
                                   and ginfo.goal_param > holes),
        msg="""Minimum holes needed to play another round must be
            less the holes per side""",
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'rnd_goals_rounds',
        rule=lambda ginfo: (ginfo.goal in round_tally.RoundTally.GOALS
                            and not ginfo.rounds),
        msg='RND_* goal requires game be played in rounds',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'rnd_goals_gp1',
        rule=lambda ginfo: (ginfo.goal in round_tally.RoundTally.GOALS
                            and ginfo.goal_param <= 0),
        msg="""RND_* goal requires GOAL_PARAM be greater than 0 to
            define win condition""",
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'rnd_goals_no_fill',
        rule=lambda ginfo: (ginfo.goal in round_tally.RoundTally.GOALS
                            and ginfo.round_fill),
        msg='RND_* goal does not use round_fill',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'move_one_start',
        rule=lambda ginfo: ginfo.move_one and not ginfo.sow_start,
        msg='MOVE_ONE requires SOW_START',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'xc_draw1_sowstart',
        rule=lambda ginfo: (ginfo.presowcapt == gi.PreSowCapt.DRAW_1_XCAPT
                            and ginfo.sow_start),
        msg="""DRAW_1_XCAPT with SOW_START will capture when start hole
            has 2 seeds (1 is drawn)""",
        warn=True)

    man_rules.add_rule(
        'presowcapt_locks',
        rule=lambda ginfo: ginfo.presowcapt and ginfo.moveunlock,
        msg='PRESOWRULEs are not supported with MOVEUNLOCK',
        excp=gi.GameInfoError)
        # locks have two purposes: don't capt from locks and moveall first
        # see no need to make these compatible with presowcapt

    man_rules.add_rule(
        'needs_moves',
        rule=lambda ginfo: (ginfo.min_move == 1
                            and ginfo.sow_start
                            and not ginfo.move_one),
        msg='MIN_MOVE of 1 with SOW_START play is confusing (unless MOVE_ONE)',
        excp=gi.GameInfoError)
        # pick-up a seed, sow it back into the same hole -> no change of state

    man_rules.add_rule(
        'mmg1_mustshare',
        rule=lambda ginfo: ginfo.min_move > 1 and ginfo.mustshare,
        msg='Shared seeds from MUSTSHARE might not be playable with min_move > 1',
        warn=PRINT_MSG)

    man_rules.add_rule(
        'unfed_mustshare',
        rule=lambda ginfo: (ginfo.unclaimed == gi.EndGameSeeds.UNFED_PLAYER
                            and not ginfo.mustshare),
        msg='EndGameSeeds UNFED_PLAYER cannot be used without MUSTSHARE',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'unfed_quitter',
        rule=lambda ginfo: ginfo.quitter == gi.EndGameSeeds.UNFED_PLAYER,
        msg="""EndGameSeeds UNFED_PLAYER should not be used as a QUITTER
            (DONT_SCORE will be used)""",
        warn=True)

    man_rules.add_rule(
        'p1m1_conflict',
        rule=lambda ginfo: (ginfo.prescribed == gi.SowPrescribed.PLUS1MINUS1
                            and (ginfo.sow_start or ginfo.move_one)),
        msg='PLUS1MINUS1 is incompatible with SOW_START and/or MOVE_ONE',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'too_many_udir',
        both_objs=True,
        rule=lambda ginfo, holes: len(ginfo.udir_holes) > holes,
        msg='Too many udir_holes specified',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'udir_oo_range',
        both_objs=True,
        rule=lambda ginfo, holes: any(udir < 0 or udir >= holes
                                      for udir in ginfo.udir_holes),
        msg='Udir_holes value out of range 0..nbr_holes-1',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'udir_gs_not',
        rule=lambda ginfo: (ginfo.udirect and
                            ginfo.grandslam == gi.GrandSlam.NOT_LEGAL),
        msg='UDIR_HOLES and GRANDLAM=Not Legal are incompatible',
        excp=NotImplementedError)
        # no games use these two features together,
        # implement when there's a use

    man_rules.add_rule(
        'udir_bad_allowrule',
        rule=lambda ginfo: (ginfo.allow_rule not in  (
                                  gi.AllowRule.NONE,
                                  gi.AllowRule.SINGLE_ONLY_ALL,
                                  gi.AllowRule.TWO_ONLY_ALL,
                                  gi.AllowRule.TWO_ONLY_ALL_RIGHT,
                                  gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
                                  gi.AllowRule.RIGHT_2_1ST_THEN_ALL_TWO,
                                  gi.AllowRule.MOVE_ALL_HOLES_FIRST,
                                  gi.AllowRule.NOT_XFROM_1S)
                             and ginfo.udirect),
        msg='UDIR_HOLES and ALLOW_RULE are incompatible',
        excp=NotImplementedError)
        # allow rules which do not depend on sow direction are fine
        # listing those so new allow rules are excluded with code changes

    man_rules.add_rule(
        'odd_split_udir',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.sow_direct == gi.Direct.SPLIT
                                   and holes % 2
                                   and holes // 2 not in ginfo.udir_holes),
        msg="""SPLIT with odd number of holes,
            but center hole not listed in udir_holes""",
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'sdir_split',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.udirect
                                   and len(ginfo.udir_holes) != holes
                                   and ginfo.sow_direct != gi.Direct.SPLIT),
        msg= 'Odd choice of sow direction when udir_holes != nbr_holes',
        warn=True)

    man_rules.add_rule(
        'gs_not_legal_no_tuple',
        rule=lambda ginfo: (ginfo.mlength > 1 and
                            ginfo.grandslam == gi.GrandSlam.NOT_LEGAL),
        msg='MLENGTH > 1 and GRANDLAM = Not Legal is not supported',
        excp=gi.GameInfoError)
        # GS allowables doesn't support tuples
        # UDIRECT: partials hole activation not supported
        # TERRITORY: partial side ownership is not implemented

    man_rules.add_rule(
        'short_no_blocks',
        rule=lambda ginfo: (ginfo.round_fill == gi.RoundFill.SHORTEN
                            and not ginfo.blocks),
        msg='RoundFill SHORTEN without BLOCKS, yields an odd game dynamic',
        warn=True)

    man_rules.add_rule(
        'pick_rend_agree',
        rule=lambda ginfo: (
            ginfo.rounds in (gi.Rounds.END_S_SEEDS,
                             gi.Rounds.END_2S_SEEDS)
            and ginfo.pickextra in (gi.CaptExtraPick.PICKLASTSEEDS,
                                    gi.CaptExtraPick.PICK2XLASTSEEDS)
            and ginfo.rounds != ginfo.pickextra),
        msg="""Pick extra and round end condition must agree
            on number of seeds (seeds or 2x seeds)""",
        excp=gi.GameInfoError)
        # if the picker is included, the round ender is not; so they must agree

    return man_rules
