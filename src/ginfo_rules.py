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

import collections
import dataclasses as dc
import warnings

import game_interface as gi

from game_interface import AllowRule
from game_interface import ChildType
from game_interface import Direct
from game_interface import Goal
from game_interface import GrandSlam
from game_interface import LapSower
from game_interface import RoundFill
from game_interface import RoundStarter
from game_interface import SowPrescribed
from game_interface import SowRule
from fill_patterns import PCLASSES


# %% constants

DIFF_LEVELS = 4
MAX_MIN_MOVES = 5
MAX_MINIMAX_DEPTH = 15


# %% rule classes

@dc.dataclass(frozen=True)
class ParamRule:
    """An individual rule to apply to GameInfo.

    name: dictionary key for rule
          an message is printed if the name is reused
    rule: a function or lambda that takes 1 or 2 params
          should return True if there is an error
    warn: if True, genearte a warning, else an exception
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
            if self.warn:
                warnings.warn(self.msg)
            else:
                msg = self.msg + f' ({self.name}).'
                raise self.excp(msg)


class RuleDict(dict):
    """A dictionary of game rules."""

    def add_rule(self, name, *, rule, msg, both_objs=False, warn=False, excp=None):
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
        rule=lambda ginfo: not isinstance(ginfo.sow_direct, Direct),
        msg='SOW_DIRECT not valid type, expected Direct',
        excp=gi.GameInfoError)

    rules.add_rule(
        'high_min_moves',
        rule=lambda ginfo: ginfo.min_move not in range(1, MAX_MIN_MOVES + 1),
        msg=f'Min_move seems wrong  (1<= convention <= {MAX_MIN_MOVES})',
        excp=gi.GameInfoError)


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
        'pattern_no_rounds',
        rule=lambda ginfo: ginfo.start_pattern and ginfo.rounds,
        msg='START_PATTERN and ROUNDS are incompatible',
        excp=gi.GameInfoError)


def add_deprive_rules(rules):
    """Add rules for the game goal of depriving the opponent of
    seeds."""

    def deprive_and(flag_name):
        """Return a function that tests that goal is divert
        and the specified flag, based only on a ginfo parameter."""

        def _deprive_and(ginfo):
            return ginfo.goal == Goal.DEPRIVE and getattr(ginfo, flag_name)

        return _deprive_and

    rules.add_rule(
        'deprive_gs_legal',
        rule=lambda ginfo: (ginfo.goal == Goal.DEPRIVE
                            and ginfo.grandslam != GrandSlam.LEGAL),
        msg='Goal of DEPRIVE requires that GRANDSLAM be Legal',
        excp=gi.GameInfoError)

    bad_flags = ['moveunlock', 'mustshare', 'mustpass',
                 'rounds', 'round_starter', 'round_fill',
                 'no_sides', 'sow_own_store', 'stores',
                 'skip_start', 'sow_start', 'visit_opp']
    for flag in bad_flags:
        rules.add_rule(
            f'deprive_bad_{flag}',
            rule=deprive_and(flag),
            msg=f'Goal of DEPRIVE cannot be used with {flag.upper()}',
            excp=gi.GameInfoError)

    return rules


def add_territory_rules(rules):
    """Add the rules for games with a goal of territory."""

    rules.add_rule(
        'terr_gparam_one',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.goal == Goal.TERRITORY
                                   and (ginfo.gparam_one <= holes
                                        or ginfo.gparam_one > 2 * holes)),
        msg='Territory Goal requires GPARAM_ONE between holes and 2 * holes',
        excp=gi.GameInfoError)

    rules.add_rule(
        'terr_need_stores',
        rule=lambda ginfo: ginfo.goal == Goal.TERRITORY and not ginfo.stores,
        msg='Territory goal requires stores',
        excp=gi.GameInfoError)

    rules.add_rule(
        'terr_no_sides_incomp',
        rule=lambda ginfo: ginfo.goal == Goal.TERRITORY and ginfo.no_sides,
        msg='Territory goal is incompatible with NO_SIDES',
        excp=gi.GameInfoError)
        # XXXX could initial ownship be changed so that no_sides makes sense

    rules.add_rule(
        'terr_pattern_incomp',
        rule=lambda ginfo: (ginfo.goal == Goal.TERRITORY
                            and ginfo.start_pattern),
        msg='Territory goal is incompatible with START_PATTERN',
        excp=gi.GameInfoError)
        # depending on pattern one player might not end up with seeds

    rules.add_rule(
        'terr_gs_not',
        rule=lambda ginfo: (ginfo.goal == Goal.TERRITORY and
                            ginfo.grandslam == GrandSlam.NOT_LEGAL),
        msg='Territory goal and GRANDLAM=Not Legal are currently incompatible',
        excp=NotImplementedError)
        # territory requires move triples, GS allowables doesn't support

    rules.add_rule(
        'terr_no_opp_empty',
        rule=lambda ginfo: (ginfo.goal == Goal.TERRITORY and
                            ginfo.allow_rule == AllowRule.OPP_OR_EMPTY),
        msg='OPP_OR_EMPTY cannot be used with TERRITORY',
        excp=gi.GameInfoError)
        # TERRITORY: what does it mean if the hole is already opp?

    rules.add_rule(
        'confuse_allow',
        rule=lambda ginfo: (ginfo.goal == Goal.TERRITORY and
                            ginfo.allow_rule != AllowRule.NONE),
        msg='Some ALLOW_RULEs are confusing with TERRITORY',
        warn=True)
        # AllowRules are not written for move triples


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
            return (ginfo.sow_rule == SowRule.SOW_BLKD_DIV
                    and getattr(ginfo, flag_name))

        return _divert_and

    rules.add_rule(
        'next_ml_no_bdiv',
        rule=lambda ginfo: (ginfo.mlaps == LapSower.LAPPER_NEXT
                            and ginfo.sow_rule == SowRule.SOW_BLKD_DIV),
        msg='MLAPS of LAPPER_NEXT is not supported with SOW_BLKD_DIV',
        excp=NotImplementedError)

    rules.add_rule(
        'bdiv_need_gparam1',
        rule=lambda ginfo: (ginfo.sow_rule == SowRule.SOW_BLKD_DIV
                            and not ginfo.gparam_one),
        msg='SOW_BLKD_DIV requires GPARAM_ONE for closing holes',
        excp=gi.GameInfoError)

    rules.add_rule(
        'bdiv_need_blocks',
        rule=lambda ginfo: (ginfo.sow_rule == SowRule.SOW_BLKD_DIV
                            and not ginfo.blocks),
        msg='SOW_BLKD_DIV requires BLOCKS for closing holes',
        excp=gi.GameInfoError)

    rules.add_rule(
        'bdiv_min_move_one',
        rule=lambda ginfo: (ginfo.sow_rule == SowRule.SOW_BLKD_DIV
                            and ginfo.min_move != 1),
        msg='SOW_BLKD_DIV requires a minimum move of 1',
        excp=gi.GameInfoError)

    rules.add_rule(
        'bdiv_min_req_dep_goal',
        rule=lambda ginfo: (ginfo.sow_rule == SowRule.SOW_BLKD_DIV
                            and ginfo.goal != Goal.DEPRIVE),
        msg='SOW_BLKD_DIV requires a goal of DEPRIVE',
        excp=gi.GameInfoError)

    capt_flags = ['capsamedir', 'crosscapt', 'evens', 'capt_min', 'capt_max',
                  'multicapt', 'oppsidecapt', 'xcpickown', 'capt_on',
                  'capt_next', 'capttwoout', 'sow_own_store']
    for flag in capt_flags:
        rules.add_rule(
            f'bdiv_no_capt_{flag}',
            rule=divert_and(flag),
            msg='sow_blkd_div closes holes to remove seeds from play, '
                f'no other capture mechanisms are allowed [{flag.upper()}]',
        excp=gi.GameInfoError)

    rules.add_rule(
        'bdiv_no_capt_on',
        rule=lambda ginfo: (ginfo.sow_rule == SowRule.SOW_BLKD_DIV
                            and any(ginfo.capt_on)),
        msg='sow_blkd_div closes holes to remove seeds from play, ' + \
            'no other capture mechanisms are allowed [CAPT_ON]',
        excp=gi.GameInfoError)

    rules.add_rule(
        'sbd_not_umove',
        rule=lambda ginfo: (ginfo.sow_rule == SowRule.SOW_BLKD_DIV
                            and ginfo.round_fill == RoundFill.UMOVE),
        msg='sow_blkd_div incompatible with UMOVE',
        excp=gi.GameInfoError)

    bad_flags = ['child_cvt', 'moveunlock', 'mustshare', 'mustpass',
                 'rounds', 'round_starter',
                 'no_sides', 'sow_own_store', 'stores',
                 'skip_start', 'sow_start', 'visit_opp']
    for flag in bad_flags:
        rules.add_rule(
            f'bdiv_bad_{flag}',
            rule=divert_and(flag),
            msg=f'sow_blkd_div cannot be used with {flag.upper()}',
            excp=gi.GameInfoError)


def add_child_rules(rules):
    """Add rules specific to having children."""

    rules.add_rule(
        'next_ml_nochild',
        rule=lambda ginfo: (ginfo.mlaps == LapSower.LAPPER_NEXT
                            and (ginfo.child_type != ChildType.NOCHILD
                                 or ginfo.child_cvt)),
        msg='MLAPS of LAPPER_NEXT is not supported with CHILD',
        excp=NotImplementedError)

    rules.add_rule(
        'child_need_cvt',
        rule=lambda ginfo: ginfo.child_type and not ginfo.child_cvt,
        msg='Selected child type requires CHILD_CVT',
        excp=gi.GameInfoError)

    rules.add_rule(
        'child_cvt_need_type',
        rule=lambda ginfo: not ginfo.child_type and ginfo.child_cvt,
        msg='CHILD_CVT requires a CHILD_TYPE != NOCHILD',
        excp=gi.GameInfoError)

    rules.add_rule(
        'child_not_deprive',
        rule=lambda ginfo: ginfo.child_cvt and ginfo.goal == Goal.DEPRIVE,
        msg='Children cannot be used with a game goal of DEPRIVE',
        excp=gi.GameInfoError)

    rules.add_rule(
        'child_no_gs',
        rule=lambda ginfo: (ginfo.child_cvt
                            and ginfo.grandslam != GrandSlam.LEGAL),
        msg='Children requires that GRANDSLAM be Legal',
        excp=NotImplementedError)

    rules.add_rule(
        'walda_store',
        rule=lambda ginfo: (ginfo.child_type == ChildType.WALDA
                            and ginfo.stores),
        msg='WALDA does not use STORES',
        warn=True)

    rules.add_rule(
        'one_child_store',
        rule=lambda ginfo: (ginfo.child_type == ChildType.ONE_CHILD
                            and not ginfo.stores),
        msg='ONE_CHILD requires STORES',
        excp=gi.GameInfoError)


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
        msg='NO_SIDES requires STORES.',
        excp=gi.GameInfoError)

    rules.add_rule(
        'no_sides_req_max_seeds',
        rule=lambda ginfo: ginfo.no_sides and ginfo.goal != Goal.MAX_SEEDS,
        msg='NO_SIDES requires a goal of MAX_SEEDS',
        excp=gi.GameInfoError)


    bad_flags = ['grandslam', 'mustpass', 'mustshare', 'oppsidecapt',
                 'rounds', 'round_starter', 'round_fill',
                 'visit_opp']
    for flag in bad_flags:
        rules.add_rule(
            f'no_sides_bad_{flag}',
            rule=no_sides_and(flag),
            msg=f'NO_SIDES cannot be used with {flag.upper()}',
            excp=gi.GameInfoError)



# %% the base ruleset

def build_rules():
    """Build the default Mancala rules.
    These can be deleted or modified by derived classes."""

    man_rules = RuleDict()

    add_creation_rules(man_rules)
    add_pattern_rules(man_rules)
    add_deprive_rules(man_rules)
    add_territory_rules(man_rules)
    add_block_and_divert_rules(man_rules)
    add_child_rules(man_rules)
    add_no_sides_rules(man_rules)


    man_rules.add_rule(
        'no_udir_1to0',
        rule=lambda ginfo: (ginfo.udirect
                            and ginfo.allow_rule == AllowRule.SINGLE_TO_ZERO),
        msg='Allow rule SINGLE_TO_ZERO cannot be used with UDIR_HOLES',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'no_right_two_ml3',
        rule=lambda ginfo: (ginfo.mlength == 3
                            and ginfo.allow_rule in
                                {AllowRule.FIRST_TURN_ONLY_RIGHT_TWO,
                                 AllowRule.RIGHT_2_1ST_THEN_ALL_TWO}),
        msg='Right Two allow rules not supported for MLENGTH 3 games',
        excp=gi.GameInfoError)
        # what does 'right' mean if can move more than one side of the board

    man_rules.add_rule(
        'no_pres_opp_empty',
        rule=lambda ginfo: (ginfo.prescribed != SowPrescribed.NONE
                            and ginfo.allow_rule == AllowRule.OPP_OR_EMPTY),
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
        'sow_own_not_capt_all',
        rule=lambda ginfo: (ginfo.sow_own_store
                            and ginfo.sow_rule == SowRule.OWN_SOW_CAPT_ALL),
        msg='SOW_OWN_STORE is not supported with OWN_SOW_CAPT_ALL',
        excp=NotImplementedError)

    man_rules.add_rule(
        'visit_opp_req_mlap',
        rule=lambda ginfo: ginfo.visit_opp and ginfo.mlaps == LapSower.OFF,
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
                            and not ginfo.sow_rule == SowRule.SOW_BLKD_DIV
                            and not ginfo.rounds),
        msg='BLOCKS without ROUNDS or SOW_BLKD_DIV does nothing',
        warn=True)

    man_rules.add_rule(
        'rstarter_wo_rounds',
        rule=lambda ginfo: not ginfo.rounds
            and ginfo.round_starter != RoundStarter.ALTERNATE,
        msg='ROUND_STARTER requires ROUNDS',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'warn_no_capt',
        rule=lambda ginfo: not any([ginfo.sow_rule == SowRule.SOW_BLKD_DIV,
                                    ginfo.capttwoout,
                                    ginfo.capt_next,
                                    ginfo.evens,
                                    ginfo.crosscapt,
                                    ginfo.sow_own_store,
                                    ginfo.capt_max,
                                    ginfo.capt_min,
                                    ginfo.capt_on]),
        msg='No capture mechanism provided',
        warn=True)

    man_rules.add_rule(
        'xcapt_multi_same',
        rule=lambda ginfo: (ginfo.crosscapt and ginfo.multicapt
                            and not ginfo.capsamedir),
        msg="CROSSCAPT with MULTICAPT without CAPSAMEDIR"
            "is the same as just CROSSCAPT.",
        warn=True)
        # capturing the opp dir (as usual) wont capture because
        # the preceeding holes were just sown, that is, not empty

    man_rules.add_rule(
        'warn_capsamedir_multicapt',
        rule=lambda ginfo: (not ginfo.capttwoout
                            and not ginfo.capt_next
                            and ginfo.capsamedir
                            and not ginfo.multicapt),
        msg="CAPSAMEDIR without MULTICAPT has no effect",
        warn=True)

    man_rules.add_rule(
        'capt2out_needs_samedir',
        rule=lambda ginfo: ginfo.capttwoout and not ginfo.capsamedir,
        msg='CAPTTWOOUT requires CAPSAMEDIR because the preceeding '
            'holes were just sown (not empty)',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'capt2_cross_incomp',
        rule=lambda ginfo: ginfo.capttwoout and ginfo.crosscapt,
        msg="CAPTTWOOUT and CROSSCAPT are incompatible",
        warn=True)

    man_rules.add_rule(
        'capt2_child_incomp',
        rule=lambda ginfo: ginfo.capttwoout and ginfo.child_cvt,
        msg="CAPTTWOOUT and CHILDREN are incompatible",
        warn=True)

    man_rules.add_rule(
        'capt2_gs_legal',
        rule=lambda ginfo: (ginfo.capttwoout
                            and ginfo.grandslam != GrandSlam.LEGAL),
        msg="CAPTTWOOUT requires that GRANDSLAM be LEGAL",
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'captnext_needs_samedir',
        rule=lambda ginfo: ginfo.capttwoout and not ginfo.capsamedir,
        msg='CAPT_NEXT requires CAPSAMEDIR',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'captnext_cross_incomp',
        rule=lambda ginfo: ginfo.capt_next and ginfo.crosscapt,
        msg="CAPT_NEXT and CROSSCAPT are incompatible",
        warn=True)

    man_rules.add_rule(
        'captnext_child_incomp',
        rule=lambda ginfo: ginfo.capt_next and ginfo.child_cvt,
        msg="CAPT_NEXT and CHILDREN are incompatible",
        warn=True)

    man_rules.add_rule(
        'captnext_multi_not',
        rule=lambda ginfo: ginfo.capt_next and ginfo.multicapt,
        msg="CAPT_NEXT with MULTICAPT is not implemented",
        excp=NotImplementedError)

    man_rules.add_rule(
        'sca_gs_not',
        rule=lambda ginfo: (ginfo.sow_rule == SowRule.OWN_SOW_CAPT_ALL
                            and ginfo.grandslam != GrandSlam.LEGAL),
        msg='OWN_SOW_CAPT_ALL requires that GRANDLAM be LEGAL',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'xpick_requires_cross',
        rule=lambda ginfo: ginfo.xcpickown and not ginfo.crosscapt,
        msg="XCPICKOWN without CROSSCAPT doesn't do anything",
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'move_one_start',
        rule=lambda ginfo: ginfo.move_one and not ginfo.sow_start,
        msg='MOVE_ONE requires SOW_START',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'needs_moves',
        rule=lambda ginfo: (ginfo.min_move == 1
                            and ginfo.sow_start
                            and not ginfo.move_one),
        msg='MIN_MOVE of 1 with SOW_START play is confusing (unless MOVE_ONE)',
        excp=gi.GameInfoError)
        # pick-up a seed, sow it back into the same hole -> no change of state

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
        'udir_and_mshare',
        rule=lambda ginfo: ginfo.udirect and ginfo.mustshare,
        msg='UDIRECT and MUSTSHARE are currently incompatible',
        excp=NotImplementedError)
        # supporting udirect and mustshare would require a UI design change
        # to support partially active buttons (left/right)
        # and would make allowables and get_moves more complicated

    man_rules.add_rule(
        'udir_gs_not',
        rule=lambda ginfo: (ginfo.udirect and
                            ginfo.grandslam == GrandSlam.NOT_LEGAL),
        msg='UDIRECT and GRANDLAM=Not Legal are currently incompatible',
        excp=NotImplementedError)
        # see comment for udir_and_mshare rule above

    man_rules.add_rule(
        'udir_allowrule',
        rule=lambda ginfo: (ginfo.udirect and
                            ginfo.allow_rule != AllowRule.NONE),
        msg='UDIRECT and ALLOW_RULE are currently incompatible',
        excp=NotImplementedError)
        # see comment for udir_and_mshare rule above

    man_rules.add_rule(
        'odd_split_udir',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.sow_direct == Direct.SPLIT
                                   and holes % 2
                                   and holes // 2 not in ginfo.udir_holes),
        msg='SPLIT with odd number of holes, '
            'but center hole not listed in udir_holes',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'sdir_split',
        both_objs=True,
        rule=lambda ginfo, holes: (ginfo.udirect
                                   and len(ginfo.udir_holes) != holes
                                   and ginfo.sow_direct != Direct.SPLIT),
        msg= 'Odd choice of sow direction when udir_holes != nbr_holes',
        warn=True)

    man_rules.add_rule(
        'gs_not_legal_no_tuple',
        rule=lambda ginfo: (ginfo.mlength > 1 and
                            ginfo.grandslam == GrandSlam.NOT_LEGAL),
        msg='MLENGTH > 1 and GRANDLAM = Not Legal is not supported',
        excp=gi.GameInfoError)
        # GS allowables doesn't support tuples
        # UDIRECT: partials hole activation not supported
        # TERRITORY: partial side ownership is not implemented

    man_rules.add_rule(
        'opp_empty_no_tuples',
        rule=lambda ginfo: (ginfo.allow_rule == AllowRule.OPP_OR_EMPTY
                            and ginfo.mlength > 1),
        msg='MLENGTH > 1 not supported with OPP_OR_EMPTY',
        excp=gi.GameInfoError)
        # UDIRECT: partials hole activation not supported
        # TERRITORY: what does it mean if the hole is already opp?

    return man_rules
