# -*- coding: utf-8 -*-
"""Deka - but adjusted for two rows.  All holes can be blocked.

Created on Thu Jul 27 15:20:35 2023
@author: Ann"""

# %% imports

import functools as ft

from game_log import game_log
import game_interface as gi
import ginfo_rules
import no_seed_goal
import sower

from game_interface import WinCond
from game_interface import GrandSlam

# %% constant

# Lots more than base game,
# as we reduce the number of holes, the more laps we do
MAX_LOOPS = 100


# %% deka rules

def build_deka_rules():
    """Update the rules for deka.  Add deka rules to RuleDict first,
    so that invalid flags are eliminated; then the consistency checking
    rules in the base set wont trigger.
    Delete a few that will still trigger that we don't want to."""

    def rev_getattr(name, obj):
        return getattr(obj.flags, name)

    deka_rules = ginfo_rules.RuleDict()

    deka_rules.add_rule(
        'min_move_one',
        rule=lambda ginfo: ginfo.min_move != 1,
        msg='Deka requires a minimum move of 1.',
        excp=gi.GameInfoError)

    deka_rules.add_rule(
        'need_convert_cnt',
        rule=lambda ginfo: not ginfo.flags.convert_cnt,
        msg='Deka requires CONVERT_CNT to control closing holes.',
        excp=gi.GameInfoError)

    deka_rules.add_rule(
        'need_blocks',
        rule=lambda ginfo: not ginfo.flags.blocks,
        msg='Deka requires BLOCKS for closing holes.',
        excp=gi.GameInfoError)

    deka_rules.add_rule(
        'gs_legal',
        rule=lambda ginfo: ginfo.flags.grandslam != GrandSlam.LEGAL,
        msg='Deka requires that GRANDSLAM be Legal.',
        excp=gi.GameInfoError)

    capt_flags = ['capsamedir', 'crosscapt', 'evens', 'cthresh',
                  'multicapt', 'oppsidecapt', 'xcpickown']
    for flag in capt_flags:
        deka_rules.add_rule(
            f'no_capt_{flag}',
            rule=ft.partial(rev_getattr, flag),
            msg='Deka closes holes to remove seeds from play, '
                f'no other capture mechanisms are allowed [{flag.upper()}].',
        excp=gi.GameInfoError)

    deka_rules.add_rule(
        'no_capt_on',
        rule=lambda ginfo: any(ginfo.capt_on),
        msg='Deka closes holes to remove seeds from play, ' + \
            'no other capture mechanisms are allowed [CAPT_ON].',
        excp=gi.GameInfoError)

    bad_flags = ['child', 'moveunlock', 'mustshare', 'mustpass',
                 'rounds', 'round_starter', 'rnd_left_fill', 'rnd_umove',
                 'no_sides', 'sow_own_store', 'stores',
                 'skip_start', 'sow_start', 'visit_opp']
    for flag in bad_flags:
        deka_rules.add_rule(
            f'bad_{flag}',
            rule=ft.partial(rev_getattr, flag),
            msg=f'Deka cannot be used with {flag.upper()}.',
            excp=gi.GameInfoError)

    deka_rules |= ginfo_rules.build_rules()

    # delete rules
    del deka_rules['blocks_wo_rounds']
    del deka_rules['warn_no_capt']

    return deka_rules


# %%  deka sowers

class DekaSower(sower.SowMethodIf):
    """Deka sower, diverts blocked holes on opp side
    to store (out of play)."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        loc = mdata.cont_sow_loc
        seeds = mdata.seeds
        while seeds:

            loc = (loc + mdata.direct) % self.game.cts.dbl_holes

            while self.game.blocked[loc]:
                if self.game.cts.opp_side(self.game.turn, loc):
                    self.game.store[0] += 1

                    seeds -= 1
                    if not seeds:
                        mdata.capt_loc = loc
                        return mdata

                loc = (loc + mdata.direct) % self.game.cts.dbl_holes

            self.game.board[loc] += 1
            seeds -= 1

        mdata.capt_loc = loc
        return mdata


class DekaSowClosed(sower.SowMethodIf):
    """For non-multilap sowing, check for closing, remove the
    final seeds from play and block the hole."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        mdata = self.decorator.sow_seeds(mdata)
        loc = mdata.capt_loc

        if (self.game.board[loc] == self.game.info.flags.convert_cnt
                and self.game.cts.opp_side(self.game.turn, loc)):

            self.game.store[0] += self.game.board[loc]
            self.game.board[loc] = 0
            self.game.blocked[loc] = True
        return mdata


class DekaLapper(sower.LapContinuerIf):
    """Continue sowing if end in hole with > 1 seeds, but
    stop if we ended on a blocked hole (will be opp side,
    i.e. last seed was taken out of play)."""

    def do_another_lap(self, mdata):
        """Determine if we are done sowing."""

        loc = mdata.capt_loc
        return not self.game.blocked[loc] and self.game.board[loc] > 1


class DekaLapSower(sower.SowMethodIf):
    """Do sow operations until until lap continuer test tells
    us to stop, closing holes along the way."""

    def __init__(self, game, decorator, lap_cont):

        super().__init__(game, decorator)
        self.lap_cont = lap_cont

    def sow_seeds(self, mdata):
        """Sow seeds."""

        loc = mdata.cont_sow_loc
        for _ in range(MAX_LOOPS):

            mdata = self.decorator.sow_seeds(mdata)

            if self.lap_cont.do_another_lap(mdata):
                loc = mdata.capt_loc
                mdata.cont_sow_loc = loc
                mdata.seeds = self.game.board[loc]

                if (self.game.board[loc] == self.game.info.flags.convert_cnt
                        and self.game.cts.opp_side(self.game.turn, loc)):
                    self.game.blocked[loc] = True
                self.game.board[loc] = 0

            else:
                return mdata

        game_log.add('MLAP game ENDLESS', game_log.IMPORT)
        mdata.capt_loc = WinCond.ENDLESS
        return mdata


# %%

class Deka(no_seed_goal.NoSeedGoal):
    """Not really deka but maybe like deka."""

    rules = build_deka_rules()

    def __init__(self, game_consts, game_info):
        """Call parent init.
        Replace the sower deco chain with our own."""

        super().__init__(game_consts, game_info)

        if self.info.flags.mlaps:
            self.deco.sower = DekaLapSower(self, DekaSower(self),
                                           DekaLapper(self))
        else:
            self.deco.sower = DekaSowClosed(self, DekaSower(self))
