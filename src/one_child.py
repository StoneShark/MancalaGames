# -*- coding: utf-8 -*-
"""Game class the mancala game one_class.

Created on Thu Jan  5 03:15:41 2023
@author: Ann"""


# %% imports

import functools as ft

import capturer
import game_interface as gi
import ginfo_rules
import mancala
import sow_starter


# %%

def build_rules():
    """Refine the GameInfo rules for one_child."""

    def rev_getattr(name, obj):
        return getattr(obj.flags, name)

    rules = ginfo_rules.RuleDict()

    rules.add_rule(
        'need_sow_start',
        rule=lambda ginfo: not ginfo.flags.sow_start,
        msg='OneChild requires SOW_START.',
        excp=gi.GameInfoError)

    rules.add_rule(
        'need_child',
        rule=lambda ginfo: not ginfo.flags.child,
        msg='OneChild requires CHILD to support tuzdek creation.',
        excp=gi.GameInfoError)

    rules.add_rule(
        'need_convert_cnt',
        rule=lambda ginfo: not ginfo.flags.convert_cnt,
        msg='OneChild requires CONVERT_CNT to define tuzdek creation.',
        excp=gi.GameInfoError)

    bad_flags = ['blocks',
                 'rounds', 'round_starter', 'rnd_left_fill', 'rnd_umove',
                 'no_sides', 'grandslam']
    for flag in bad_flags:
        rules.add_rule(
            f'bad_{flag}',
            rule=ft.partial(rev_getattr, flag),
            msg=f'OneChild cannot be used with {flag.upper()}.',
            excp=gi.GameInfoError)

    rules |= ginfo_rules.build_rules()
    del rules['needs_moves']

    return rules

# %%


class SowStart(sow_starter.SowStartIf):
    """Sow the start hole unless there is only one seed."""

    def start_sow(self, loc):
        """start sow"""

        seeds = self.game.board[loc]
        if seeds >= 1:
            self.game.board[loc] = 0
        else:
            seeds -= 1
            self.game.board[loc] = 1

        return loc, seeds


class MakeTuzdek(capturer.CaptMethodIf):
    """A tuzdek (child) may not be made in leftmost hole on
    either side.  Each player can only have one tuzdek and player's
    tuzdek must not be opposite eachother on the board."""

    def tuzdek_test(self, loc):
        """put the test in a function to keep the linter from
        complaining that it's too complex"""

        cross = self.game.cts.cross_from_loc(loc)
        opp_range = self.game.cts.get_opp_range(self.game.turn)

        return (self.game.cts.opp_side(self.game.turn, loc)
                and self.game.child[loc] is None
                and self.game.child[cross] is None
                and self.game.board[loc] == self.game.info.flags.convert_cnt
                and self.game.cts.loc_to_left_cnt(loc)
                and not any(self.game.child[tloc] is not None
                            for tloc in opp_range))


    def do_captures(self, mdata):

        loc = mdata.capt_loc

        if self.tuzdek_test(loc):
            self.game.child[loc] = self.game.turn
            return True

        return self.decorator.do_captures(mdata)



# %%  game class


class OneChild(mancala.Mancala):
    """A single-lap Mancala with two-directional movement
    and created storehouses."""

    rules = build_rules()

    def __init__(self, game_consts, game_info):
        """Call parent init.
        starter: replace SowStartHole
        capturer: replace MakeChild
        """

        super().__init__(game_consts, game_info)

        if isinstance(self.deco.starter, sow_starter.SowStartHole):
            self.deco.starter = SowStart(self,
                                         self.deco.starter.decorator)

        else:
            starter = self.deco.starter
            prev_starter = None
            while starter and not isinstance(starter,
                                             sow_starter.SowStartHole):
                prev_starter = starter
                starter = starter.decorator

            if prev_starter and starter:
                prev_starter.decorator = SowStart(self, starter.decorator)
            else:
                raise gi.GameInfoError(
                    'SowStartHole not found in starter chain.')

        if isinstance(self.deco.capturer, capturer.MakeChild):
            self.deco.capturer = MakeTuzdek(self,
                                            self.deco.capturer.decorator)
        else:
            capt = self.deco.capturer
            prev_capt = None
            while capt and not isinstance(capturer, capturer.MakeChild):
                prev_capt = capt
                capt = capt.decorator

            if prev_capt and capt:
                prev_capt.decorator = MakeTuzdek(self, capt.decorator)
            else:
                raise gi.GameInfoError(
                    'MakeChild not found in capturer chain.')
