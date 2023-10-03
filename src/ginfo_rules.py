# -*- coding: utf-8 -*-
"""A class to enforce rules on the values in GameInfo.

Each game class should have a 'rules' variable that is
a RuleDict to enforce reasonable values for the
game_info data.

This allows the default set of rules for the Mancala
class to be defined below. Then classes derived from
Mancala can add, change or delete rules. The base
class (Mancala) no longer has to be a superset of
acceptable parameter combinations. For example,
the base Mancala class doesn't process BLOCKS without
ROUNDS, so setting both can be enforced. But Deka,
which uses BLOCKS without ROUNDS can remove that rule.

The RuleDict is class scope so that GameInfo can
get the rules in it's construction before the
actual game class is instantiated.

Created on Mon Aug 21 06:54:24 2023
@author: Ann"""

import collections as col
import dataclasses as dc
import warnings

import game_interface as gi
from game_interface import Direct
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
    rule: col.abc.Callable   # return True if error
    msg: str
    warn: bool = False       # do warning not exception
    excp: object = None      # exception to raise

    def test(self, gameinfo):
        """Test the rule, do the action if it returns true."""

        if self.rule(gameinfo):
            if self.warn:
                warnings.warn(self.msg)
            else:
                msg = self.name + ':  ' + self.msg
                raise self.excp(msg)


class RuleDict(dict):
    """A dictionary of game rules."""

    def add_rule(self, name, rule, msg, *, warn=False, excp=None):
        """Add a rule to the dictionary."""
        # pylint: disable=too-many-arguments

        if not warn and not excp:
            print(f'Rule {name} has no effect.')

        if name in self:
            print(f'Rule {name} being replaced.')

        self[name] = GameInfoRule(name, rule, msg, warn, excp)


# %% default mancala rules

def build_rules():
    """Build the default Mancala rules.
    These can be deleted or modified by derived classes."""

    man_rules = RuleDict()

    man_rules.add_rule(
        'invalid_holes',
        rule=lambda ginfo: (not ginfo.nbr_holes or
                            not isinstance(ginfo.nbr_holes, int)),
        msg='Holes must > 0.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'missing_name',
        rule=lambda ginfo: not ginfo.name,
        msg='Mising Name.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'invalid_flags',
        rule=lambda ginfo: (not ginfo.flags or
                            not isinstance(ginfo.flags, gi.GameFlags)),
        msg='Missing or bad game flags.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'invalid_scorer',
        rule=lambda ginfo: (not ginfo.scorer or
                            not isinstance(ginfo.scorer, gi.Scorer)),
        msg='Missing or bad scorer.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'invalid_ai_params',
        rule=lambda ginfo: not isinstance(ginfo.ai_params, dict),
        msg='Invalid AI parameter dictionary.',
        excp=gi.GameInfoError)

    ###  GameInfo.Flags checks

    man_rules.add_rule(
        'sow_dir_type',
        rule=lambda ginfo: not isinstance(ginfo.flags.sow_direct, Direct),
        msg='SOW_DIRECT not valid type, expected Direct.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'sow_own_needs_stores',
        rule=lambda ginfo: (ginfo.flags.sow_own_store
                            and not ginfo.flags.stores),
        msg='SOW_OWN_STORE set without STORES set.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'child_convert_cnt',
        rule=lambda ginfo: (ginfo.flags.child  and
                            not ginfo.flags.convert_cnt),
        msg="CHILD without CONVERT_CNT doesn't do anything.",
        warn=True)

    man_rules.add_rule(
        'child_gs_legal',
        rule=lambda ginfo: (ginfo.flags.child  and
                            ginfo.flags.grandslam != GrandSlam.LEGAL),
        msg='CHILD requires that GRANDSLAM be Legal.',
        excp=NotImplementedError)
        # the GS code doesn't handle children, I suppose it could

    man_rules.add_rule(
        'split_gs_not',
        rule=lambda ginfo: (ginfo.flags.sow_direct == Direct.SPLIT and
                            ginfo.flags.grandslam == GrandSlam.NOT_LEGAL),
        msg='SPLIT and GRANDSLAM of Not Legal is not implemented.',
        excp=NotImplementedError)

    man_rules.add_rule(
        'no_skip_start_mlap',
        rule=lambda ginfo: ginfo.flags.skip_start and ginfo.flags.mlaps,
        msg='SKIP_START not compatible with MULTI_LAP.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'no_sow_start_mlap',
        rule=lambda ginfo: ginfo.flags.sow_start and ginfo.flags.mlaps,
        msg='SOW_START not compatible with MULTI_LAP.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'visit_opp_req_mlap',
        rule=lambda ginfo: ginfo.flags.visit_opp and not ginfo.flags.mlaps,
        msg='VISIT_OPP requires MLAPS.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'split_mshare',
        rule=lambda ginfo: (ginfo.flags.sow_direct == Direct.SPLIT
                            and ginfo.flags.mustshare),
        msg='SPLIT and MUSTSHARE are currently incompatible.',
        excp=NotImplementedError)
        # supporting split_mshare would make allowables and get_moves
        # more complicated--the deco chain could be expanded,
        # BUT the UI would be really difficult, need partially
        # active buttons (left/right)

    man_rules.add_rule(
        'sow_start_skip_incomp',
        rule=lambda ginfo: ginfo.flags.sow_start and ginfo.flags.skip_start,
        msg='SOW_START and SKIP_START do not make sense together.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'rounds_wo_blocks',
        rule=lambda ginfo: ginfo.flags.rounds and not ginfo.flags.blocks,
        msg='ROUNDS without BLOCKS is not supported.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'blocks_wo_rounds',
        rule=lambda ginfo: ginfo.flags.blocks and not ginfo.flags.rounds,
        msg='BLOCKS without ROUNDS is not supported by Mancala (base class).',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'rstarter_wo_rounds',
        rule=lambda ginfo: not ginfo.flags.rounds
            and ginfo.flags.round_starter != RoundStarter.ALTERNATE,
        msg='ROUND_STARTER without ROUNDS is not supported.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'warn_capsamedir_multicapt',
        rule=lambda ginfo: ginfo.flags.capsamedir and not ginfo.flags.multicapt,
        msg="CAPSAMEDIR without MULTICAPT has no effect.",
        warn=True)

    man_rules.add_rule(
        'xcapt_multi_same',
        rule=lambda ginfo: (ginfo.flags.crosscapt and ginfo.flags.multicapt
                            and not ginfo.flags.capsamedir),
        msg="CROSSCAPT with MULTICAPT without CAPSAMEDIR"
            "is the same as just CROSSCAPT.",
        warn=True)
        # capturing the opp dir (as usual) wont capture because
        # the preceeding holes were just sown, that is, not empty

    man_rules.add_rule(
        'warn_crosscapt_evens',
        rule=lambda ginfo: ginfo.flags.crosscapt and ginfo.flags.evens,
        msg='CROSSCAPT with EVENS might be confusing '
            '(conditions are ANDed).',
        warn=True)

    man_rules.add_rule(
        'xpick_requires_cross',
        rule=lambda ginfo: ginfo.flags.xcpickown and not ginfo.flags.crosscapt,
        msg="XCPICKOWN without CROSSCAPT doesn't do anything.",
        excp=gi.GameInfoError)

    ## GameInfo checks

    man_rules.add_rule(
        'bad_no_side',
        rule=lambda ginfo: ginfo.flags.no_sides,
        msg='Mancala does not support NO_SIDES.',
        excp=gi.GameInfoError)
        # flag is in the base class because it changes how the UI works

    man_rules.add_rule(
        'warn_no_capt',
        rule=lambda ginfo: not any([ginfo.flags.evens,
                                    ginfo.flags.crosscapt,
                                    ginfo.flags.sow_own_store,
                                    ginfo.flags.cthresh,
                                    ginfo.capt_on]),
        msg='No capture mechanism provided.',
        warn=True)

    man_rules.add_rule(
        'capt_on_evens_incomp',
        rule=lambda ginfo: ginfo.flags.evens and ginfo.capt_on,
        msg='CAPT_ON and EVENS conditions are ANDed.',
        warn=True)

    man_rules.add_rule(
        'cross_capt_on_anded',
        rule=lambda ginfo: ginfo.flags.crosscapt and ginfo.capt_on,
        msg='CROSSCAPT with CAPT_ON conditions are ANDed.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'needs_moves',
        rule=lambda ginfo: ginfo.min_move == 1 and ginfo.flags.sow_start,
        msg='MIN_MOVE of 1 with SOW_START play is confusing.',
        excp=gi.GameInfoError)
        # pick-up a seed, sow it back into the same hole -> no change of state

    man_rules.add_rule(
        'mlap_capt_on_incomp',
        rule=lambda ginfo: ginfo.flags.mlaps and ginfo.capt_on,
        msg='CAPT_ON with MULTI_LAP never captures.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'too_many_udir',
        rule=lambda ginfo: len(ginfo.udir_holes) > ginfo.nbr_holes,
        msg='Too many udir_holes specified.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'udir_oo_range',
        rule=lambda ginfo: any(udir < 0 or udir >= ginfo.nbr_holes
                               for udir in ginfo.udir_holes),
        msg='Udir_holes value out of range 0..nbr_holes-1.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'udir_and_mshare',
        rule=lambda ginfo: ginfo.flags.udirect and ginfo.flags.mustshare,
        msg='UDIRECT and MUSTSHARE are currently incompatible.',
        excp=NotImplementedError)
        # see SPLIT / MUSHSHARE above

    man_rules.add_rule(
        'udir_gs_not',
        rule=lambda ginfo: (ginfo.flags.udirect and
                            ginfo.flags.grandslam == GrandSlam.NOT_LEGAL),
        msg='UDIRECT and GRANDLAM=Not Legal are currently incompatible.',
        excp=NotImplementedError)
        # see SPLIT / MUSHSHARE above

    man_rules.add_rule(
        'odd_split_udir',
        rule=lambda ginfo: (ginfo.flags.sow_direct == Direct.SPLIT
                            and ginfo.nbr_holes % 2
                            and ginfo.nbr_holes // 2 not in ginfo.udir_holes),
        msg='SPLIT with odd number of holes, '
            'but center hole not listed in udir_holes.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'sdir_split',
        rule=lambda ginfo: (ginfo.flags.udirect
                            and len(ginfo.udir_holes) != ginfo.nbr_holes
                            and ginfo.flags.sow_direct != Direct.SPLIT),
        msg= 'Odd choice of sow direction when udir_holes != nbr_holes.',
        warn=True)

    man_rules.add_rule(
        'def_diff',
        rule=lambda ginfo: ginfo.difficulty not in range(DIFF_LEVELS),
        msg='Difficulty not 0, 1, 2 or 3.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'high_min_moves',
        rule=lambda ginfo: ginfo.min_move not in range(1, MAX_MIN_MOVES + 1),
        msg=f'Min_move seems wrong  (1<= convention <={MAX_MIN_MOVES}).',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'params_four_diff',
        rule=lambda ginfo: (ginfo.ai_params and
                            all(len(values) != DIFF_LEVELS
                                for values in ginfo.ai_params.values())),
        msg=f'Exactly {DIFF_LEVELS} param values are expected '
            'for each ai parameter.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'mlaps_access_prohibit',
        rule=lambda ginfo: ginfo.scorer.access_m and ginfo.flags.mlaps,
        msg='Access scorer not supported for multilap games.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'child_scorer',
        rule=lambda ginfo: ginfo.scorer.child_cnt_m and not ginfo.flags.child,
        msg='Child count scorer not supported without child flag.',
        excp=gi.GameInfoError)

    man_rules.add_rule(
        'scorer_vals',
        rule=lambda ginfo: all(not val
                               for val in vars(ginfo.scorer).values()),
        msg='At least one scorer value should be non-zero'
            'to prevent random play.',
        warn=True)

    return man_rules
