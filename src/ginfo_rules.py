# -*- coding: utf-8 -*-
"""A class to enforce rules on the values in GameInfo.

Each game class should have a 'rules' variable that is
a RuleDict to enforce reasonable values for the
game_info data.  The RuleDict is class scope so that
GameInfo can get the rules in it's construction before
the actual game class is instantiated.

This allows the default set of rules for the Mancala
class to be defined below. Then classes derived from
Mancala can add, change or delete rules. The base
class (Mancala) no longer has to be a superset of
acceptable parameter combinations. For example,
the base Mancala class doesn't process BLOCKS without
ROUNDS, so setting both can be enforced. But Deka,
which uses BLOCKS without ROUNDS can remove that rule.

Created on Mon Aug 21 06:54:24 2023
@author: Ann"""

import collections as col
import dataclasses as dc
import warnings

import game_interface as gi

from game_interface import Direct
from game_interface import Goal
from game_interface import GrandSlam
from game_interface import RoundStarter


# %% constants

DIFF_LEVELS = 4
MAX_MIN_MOVES = 5
MAX_MINIMAX_DEPTH = 15


# %% rule classes

@dc.dataclass(frozen=True)
class GameInfoRule:
    """An individual rule to apply to GameInfo."""

    name: str
    rule: col.abc.Callable   # return True if errorl
    msg: str
    warn: bool = False       # do warning not exception
    excp: object = None      # exception to raise
    holes: bool = False      # when True call the rule with holes & ginfo

    def test(self, holes, ginfo):
        """Test the rule, do the action if it returns true."""

        error = self.rule(holes, ginfo) if self.holes else self.rule(ginfo)
        if error:
            if self.warn:
                warnings.warn(self.msg)
            else:
                msg = self.msg + f' ({self.name}).'
                raise self.excp(msg)


class RuleDict(dict):
    """A dictionary of game rules."""

    def add_rule(self, name, *, rule, msg, holes=False, warn=False, excp=None):
        """Add a rule to the dictionary."""
        # pylint: disable=too-many-arguments

        if not warn and not excp:
            print(f'Rule {name} has no effect.')

        if name in self:
            print(f'Rule {name} being replaced.')

        self[name] = GameInfoRule(name, holes=holes, rule=rule, msg=msg,
                                  warn=warn, excp=excp)


    def test(self, holes, ginfo):
        """Test each of the rules."""

        for rule in self.values():
            rule.test(holes, ginfo)


# %% grouped rules


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
                 'rounds', 'round_starter', 'rnd_left_fill', 'rnd_umove',
                 'no_sides', 'sow_own_store', 'stores',
                 'skip_start', 'sow_start', 'visit_opp']
    for flag in bad_flags:
        rules.add_rule(
            f'deprive_bad_{flag}',
            rule=deprive_and(flag),
            msg=f'Goal of DEPRIVE cannot be used with {flag.upper()}',
            excp=gi.GameInfoError)

    return rules


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
            return ginfo.sow_blkd_div and getattr(ginfo, flag_name)

        return _divert_and

    rules.add_rule(
        'bdiv_need_convert_cnt',
        rule=lambda ginfo: ginfo.sow_blkd_div and not ginfo.convert_cnt,
        msg='SOW_BLKD_DIV requires CONVERT_CNT for closing holes',
        excp=gi.GameInfoError)

    rules.add_rule(
        'bdiv_need_blocks',
        rule=lambda ginfo: ginfo.sow_blkd_div and not ginfo.blocks,
        msg='SOW_BLKD_DIV requires BLOCKS for closing holes',
        excp=gi.GameInfoError)

    rules.add_rule(
        'bdiv_min_move_one',
        rule=lambda ginfo: ginfo.sow_blkd_div and ginfo.min_move != 1,
        msg='SOW_BLKD_DIV requires a minimum move of 1',
        excp=gi.GameInfoError)

    rules.add_rule(
        'bdiv_min_req_dep_goal',
        rule=lambda ginfo: ginfo.sow_blkd_div and ginfo.goal != Goal.DEPRIVE,
        msg='SOW_BLKD_DIV requires a goal of DEPRIVE',
        excp=gi.GameInfoError)

    capt_flags = ['capsamedir', 'crosscapt', 'evens', 'cthresh',
                  'multicapt', 'oppsidecapt', 'xcpickown', 'capt_on',
                  'capttwoout']
    for flag in capt_flags:
        rules.add_rule(
            f'bdiv_no_capt_{flag}',
            rule=divert_and(flag),
            msg='sow_blkd_div closes holes to remove seeds from play, '
                f'no other capture mechanisms are allowed [{flag.upper()}]',
        excp=gi.GameInfoError)

    rules.add_rule(
        'bdiv_no_capt_on',
        rule=lambda ginfo: ginfo.sow_blkd_div and any(ginfo.capt_on),
        msg='sow_blkd_div closes holes to remove seeds from play, ' + \
            'no other capture mechanisms are allowed [CAPT_ON]',
        excp=gi.GameInfoError)

    bad_flags = ['child', 'moveunlock', 'mustshare', 'mustpass',
                 'rounds', 'round_starter', 'rnd_left_fill', 'rnd_umove',
                 'no_sides', 'sow_own_store', 'stores',
                 'skip_start', 'sow_start', 'visit_opp']
    for flag in bad_flags:
        rules.add_rule(
            f'bdiv_bad_{flag}',
            rule=divert_and(flag),
            msg=f'sow_blkd_div cannot be used with {flag.upper()}',
            excp=gi.GameInfoError)


def add_walda_rules(rules):
    """Add rules specific to having waldas.  Originally from Qelat."""

    def waldas_and(flag_name):
        """Return a function that tests waldas and the specified
        flag, based only on a ginfo parameter."""

        def _waldas_and(ginfo):
            return ginfo.waldas and getattr(ginfo, flag_name)

        return _waldas_and

    rules.add_rule(
        'waldas_need_child',
        rule=lambda ginfo: ginfo.waldas and not ginfo.child,
        msg='Waldas requires CHILD',
        excp=gi.GameInfoError)

    rules.add_rule(
        'waldas_need_convert_cnt',
        rule=lambda ginfo: ginfo.waldas and not ginfo.convert_cnt,
        msg='Waldas requires CONVERT_CNT',
        excp=gi.GameInfoError)

    rules.add_rule(
        'walda_req_max_seeds',
        rule=lambda ginfo: ginfo.waldas and ginfo.goal != Goal.MAX_SEEDS,
        msg='WALDAS requires a goal of MAX_SEEDS',
        excp=gi.GameInfoError)

    rules.add_rule(
        'waldas_gs_legal',
        rule=lambda ginfo: (ginfo.waldas
                            and ginfo.grandslam != GrandSlam.LEGAL),
        msg='Waldas requires that GRANDSLAM be Legal',
        excp=gi.GameInfoError)

    bad_flags = ['blocks',
                 'rounds', 'round_starter', 'rnd_left_fill', 'rnd_umove',
                 'no_sides', 'sow_own_store', 'stores']
    for flag in bad_flags:
        rules.add_rule(
            f'waldas_bad_{flag}',
            rule=waldas_and(flag),
            msg=f'Waldas cannot be used with {flag.upper()}',
            excp=gi.GameInfoError)


def add_no_sides_rules(rules):
    """Add the no_sides rules."""

    def no_sides_and(flag_name):
        """Return a function that tests waldas and the specified
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

    rules.add_rule(
        'no_side_scorers',
        rule=lambda ginfo: ginfo.no_sides and
                                any([ginfo.scorer.empties_m,
                                     ginfo.scorer.evens_m,
                                     ginfo.scorer.access_m,
                                     ginfo.scorer.seeds_m,
                                     ginfo.scorer.child_cnt_m]),
        msg='Scorer multipliers empties, evens, access, seeds '
            'and child_cnt are incompatible with NoSides',
        excp=gi.GameInfoError)
        # XXXX could override scorer for evens, empties, access
        # and child_cnt to max/min the total count of them.
        # would need to restructure base game scorer to allow
        # individual overrides

    bad_flags = ['grandslam', 'mustpass', 'mustshare', 'oppsidecapt',
                 'rounds', 'round_starter', 'rnd_left_fill', 'rnd_umove',
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

    man_rules.add_rule(
        'invalid_holes',
        holes=True,
        rule=lambda holes, ginfo: (not holes or not isinstance(holes, int)),
        msg='Holes must > 0',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'missing_name',
        rule=lambda ginfo: not ginfo.name,
        msg='Mising Name',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'invalid_scorer',
        rule=lambda ginfo: (not ginfo.scorer or
                            not isinstance(ginfo.scorer, gi.Scorer)),
        msg='Missing or bad scorer',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'invalid_ai_params',
        rule=lambda ginfo: not isinstance(ginfo.ai_params, dict),
        msg='Invalid AI parameter dictionary',
        excp=gi.GameInfoError)

    add_deprive_rules(man_rules)
    add_block_and_divert_rules(man_rules)
    add_walda_rules(man_rules)
    add_no_sides_rules(man_rules)

    man_rules.add_rule(
        'sow_dir_type',
        rule=lambda ginfo: not isinstance(ginfo.sow_direct, Direct),
        msg='SOW_DIRECT not valid type, expected Direct',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'sow_own_needs_stores',
        rule=lambda ginfo: (ginfo.sow_own_store
                            and not ginfo.stores),
        msg='SOW_OWN_STORE set without STORES set',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'child_convert_cnt',
        rule=lambda ginfo: (ginfo.child  and
                            not ginfo.convert_cnt),
        msg="CHILD without CONVERT_CNT doesn't do anything.",
        warn=True)

    man_rules.add_rule(
        'child_gs_legal',
        rule=lambda ginfo: (ginfo.child  and
                            ginfo.grandslam != GrandSlam.LEGAL),
        msg='CHILD requires that GRANDSLAM be Legal',
        excp=NotImplementedError)
        # the GS code doesn't handle children, I suppose it could

    man_rules.add_rule(
        'split_gs_not',
        rule=lambda ginfo: (ginfo.sow_direct == Direct.SPLIT and
                            ginfo.grandslam == GrandSlam.NOT_LEGAL),
        msg='SPLIT and GRANDSLAM of Not Legal is not implemented',
        excp=NotImplementedError)

    man_rules.add_rule(
        'no_sow_start_mlap',
        rule=lambda ginfo: ginfo.sow_start and ginfo.mlaps,
        msg='SOW_START not compatible with MULTI_LAP',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'visit_opp_req_mlap',
        rule=lambda ginfo: ginfo.visit_opp and not ginfo.mlaps,
        msg='VISIT_OPP requires MLAPS',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'split_mshare',
        rule=lambda ginfo: (ginfo.sow_direct == Direct.SPLIT
                            and ginfo.mustshare),
        msg='SPLIT and MUSTSHARE are currently incompatible',
        excp=NotImplementedError)
        # supporting split_mshare would make allowables and get_moves
        # more complicated--the deco chain could be expanded,
        # BUT the UI would be really difficult, need partially
        # active buttons (left/right)

    man_rules.add_rule(
        'sow_start_skip_incomp',
        rule=lambda ginfo: ginfo.sow_start and ginfo.skip_start,
        msg='SOW_START and SKIP_START do not make sense together',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'blocks_wo_rounds',
        rule=lambda ginfo: (not ginfo.sow_blkd_div
                            and ginfo.blocks and not ginfo.rounds),
        msg='BLOCKS without ROUNDS is not supported '
            'without sow_blkd_div.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'rstarter_wo_rounds',
        rule=lambda ginfo: not ginfo.rounds
            and ginfo.round_starter != RoundStarter.ALTERNATE,
        msg='ROUND_STARTER without ROUNDS is not supported',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'warn_capsamedir_multicapt',
        rule=lambda ginfo: (not ginfo.capttwoout
                            and ginfo.capsamedir
                            and not ginfo.multicapt),
        msg="CAPSAMEDIR without MULTICAPT has no effect (unless CAPTTWOOUT).",
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
        'warn_crosscapt_evens',
        rule=lambda ginfo: ginfo.crosscapt and ginfo.evens,
        msg='CROSSCAPT with EVENS might be confusing '
            '(conditions are ANDed)',
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
        'capt2_waldas_incomp',
        rule=lambda ginfo: ginfo.capttwoout and (ginfo.child or ginfo.waldas),
        msg="CAPTTWOOUT and WALDAS/CHILD are incompatible",
        warn=True)

    man_rules.add_rule(
        'capt2_gs_legal',
        rule=lambda ginfo: (ginfo.capttwoout
                            and ginfo.grandslam != GrandSlam.LEGAL),
        msg="CAPTTWOOUT requires that GRANDSLAM be LEGAL",
        warn=True)

    man_rules.add_rule(
        'capt2_multi_incomp',
        rule=lambda ginfo: ginfo.capttwoout and ginfo.multicapt,
        msg="CAPTTWOOUT and MULTICAPT are incompatible",
        warn=True)

    man_rules.add_rule(
        'xpick_requires_cross',
        rule=lambda ginfo: ginfo.xcpickown and not ginfo.crosscapt,
        msg="XCPICKOWN without CROSSCAPT doesn't do anything",
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'warn_no_capt',
        rule=lambda ginfo: not any([ginfo.sow_blkd_div,
                                    ginfo.capttwoout,
                                    ginfo.evens,
                                    ginfo.crosscapt,
                                    ginfo.sow_own_store,
                                    ginfo.cthresh,
                                    ginfo.capt_on]),
        msg='No capture mechanism provided',
        warn=True)

    man_rules.add_rule(
        'capt_on_evens_incomp',
        rule=lambda ginfo: ginfo.evens and ginfo.capt_on,
        msg='CAPT_ON and EVENS conditions are ANDed',
        warn=True)

    man_rules.add_rule(
        'cross_capt_on_anded',
        rule=lambda ginfo: ginfo.crosscapt and ginfo.capt_on,
        msg='CROSSCAPT with CAPT_ON conditions are ANDed',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'needs_moves',
        rule=lambda ginfo: ginfo.min_move == 1 and ginfo.sow_start,
        msg='MIN_MOVE of 1 with SOW_START play is confusing',
        excp=gi.GameInfoError)
        # pick-up a seed, sow it back into the same hole -> no change of state

    man_rules.add_rule(
        'mlap_capt_on_incomp',
        rule=lambda ginfo: ginfo.mlaps and ginfo.capt_on,
        msg='CAPT_ON with MULTI_LAP never captures',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'too_many_udir',
        holes=True,
        rule=lambda holes, ginfo: len(ginfo.udir_holes) > holes,
        msg='Too many udir_holes specified',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'udir_oo_range',
        holes=True,
        rule=lambda holes, ginfo: any(udir < 0 or udir >= holes
                                      for udir in ginfo.udir_holes),
        msg='Udir_holes value out of range 0..nbr_holes-1',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'udir_and_mshare',
        rule=lambda ginfo: ginfo.udirect and ginfo.mustshare,
        msg='UDIRECT and MUSTSHARE are currently incompatible',
        excp=NotImplementedError)
        # see SPLIT / MUSHSHARE above

    man_rules.add_rule(
        'udir_gs_not',
        rule=lambda ginfo: (ginfo.udirect and
                            ginfo.grandslam == GrandSlam.NOT_LEGAL),
        msg='UDIRECT and GRANDLAM=Not Legal are currently incompatible',
        excp=NotImplementedError)
        # see SPLIT / MUSHSHARE above

    man_rules.add_rule(
        'odd_split_udir',
        holes=True,
        rule=lambda holes, ginfo: (ginfo.sow_direct == Direct.SPLIT
                                   and holes % 2
                                   and holes // 2 not in ginfo.udir_holes),
        msg='SPLIT with odd number of holes, '
            'but center hole not listed in udir_holes',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'sdir_split',
        holes=True,
        rule=lambda holes, ginfo: (ginfo.udirect
                                   and len(ginfo.udir_holes) != holes
                                   and ginfo.sow_direct != Direct.SPLIT),
        msg= 'Odd choice of sow direction when udir_holes != nbr_holes',
        warn=True)

    man_rules.add_rule(
        'def_diff',
        rule=lambda ginfo: ginfo.difficulty not in range(DIFF_LEVELS),
        msg='Difficulty not 0, 1, 2 or 3',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'high_min_moves',
        rule=lambda ginfo: ginfo.min_move not in range(1, MAX_MIN_MOVES + 1),
        msg=f'Min_move seems wrong  (1<= convention <={MAX_MIN_MOVES})',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'params_four_diff',
        rule=lambda ginfo: (ginfo.ai_params and
                            all(len(values) != DIFF_LEVELS
                                for values in ginfo.ai_params.values())),
        msg=f'Exactly {DIFF_LEVELS} param values are expected '
            'for each ai parameter',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'mlaps_access_prohibit',
        rule=lambda ginfo: ginfo.scorer.access_m and ginfo.mlaps,
        msg='Access scorer not supported for multilap games',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'child_scorer',
        rule=lambda ginfo: ginfo.scorer.child_cnt_m and not ginfo.child,
        msg='Child count scorer not supported without child flag',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'scorer_vals',
        rule=lambda ginfo: all(not val
                               for val in vars(ginfo.scorer).values()),
        msg='At least one scorer value should be non-zero'
            'to prevent random play',
        warn=True)

    return man_rules
