# -*- coding: utf-8 -*-
"""Gamacha as described in Mohr.

Created on Mon Sep 11 08:37:39 2023
@author: Ann"""

import functools as ft

import allowables
import ginfo_rules
import game_interface as gi
import new_game
import no_seed_goal

from game_interface import GrandSlam


def compute_dest(holes):
    """Compute the lower hole (destination).
    Starting at 3:
        1, 1, 3, 3, 3, 3, 5, 5, 5, 5, 7, 7 ..."""
    return 1 + 2 * ((holes-1) // 4)



def build_gamcha_rules():
    """Update the rules for gamacha.  Add gamacha rules to RuleDict first,
    so that invalid flags are eliminated; then the consistency checking
    rules in the base set wont trigger.
    Delete a few that will still trigger that we don't want to."""

    def rev_getattr(name, obj):
        return getattr(obj.flags, name)

    rules = ginfo_rules.RuleDict()

    rules.add_rule(
        'three_per_side',
        holes=True,
        rule=lambda holes, _: holes < 3,
        msg='Gamacha requires at least 3 holes per side',
        excp=gi.GameInfoError)

    rules.add_rule(
        'gs_legal',
        rule=lambda ginfo: ginfo.flags.grandslam != GrandSlam.LEGAL,
        msg='Gamacha requires that GRANDSLAM be Legal',
        excp=gi.GameInfoError)

    bad_flags = ['blocks', 'child', 'mlaps', 'moveunlock',
                 'mustpass', 'mustshare', 'round_starter',
                 'rounds', 'rnd_left_fill', 'rnd_umove',
                 'no_sides', 'skip_start', 'sow_own_store',
                 'sow_start', 'stores', 'visit_opp']
    for flag in bad_flags:
        rules.add_rule(
            f'bad_{flag}',
            rule=ft.partial(rev_getattr, flag),
            msg=f'Gamacha cannot be used with {flag.upper()}',
            excp=gi.GameInfoError)

    rules |= ginfo_rules.build_rules()
    del rules['blocks_wo_rounds']

    return rules


class SeedOrder(new_game.NewGameIf):
    """Seeds not distributed evenly.
    Rules conflict. If there was a previous game, the loser starts."""

    def new_game(self, win_cond=None, _=False):

        starter = None
        if win_cond is not None:
            starter = not self.game.turn

        self.decorator.new_game(win_cond, False)

        if starter is not None:
            self.game.starter = starter
            self.game.turn = starter

        self.game.board = [0] * self.game.cts.dbl_holes
        for loc in range(2, self.game.cts.dbl_holes, 2):
            self.game.board[loc] = self.game.cts.nbr_start

        dest = compute_dest(self.game.cts.holes)
        source = self.game.cts.dbl_holes - dest - 1

        self.game.board[dest] = self.game.board[source]
        self.game.board[source] = 0

        if self.game.turn:
            self.game.board = self.game.board[::-1]

        return True


class OppOrEmptyEnd(allowables.AllowableIf):
    """Can only play from holes that end in an empty hole or
    on the opponents side of the board."""

    def get_allowable_holes(self):

        allow = self.decorator.get_allowable_holes()
        saved_state = self.game.state
        my_rng = self.game.cts.get_my_range(self.game.turn)

        for pos in range(self.game.cts.holes):
            if not allow[pos]:
                continue

            mdata = self.game.do_sow(pos)
            self.game.state = saved_state

            end_loc = mdata.capt_loc
            if self.game.board[end_loc] and end_loc in my_rng:
                allow[pos] = False

        return allow


class Gamacha(no_seed_goal.NoSeedGoal):
    """The Gamacha game dynamics."""

    rules = build_gamcha_rules()

    def __init__(self, game_consts, game_info, player=None):

        object.__setattr__(
            game_consts, 'total_seeds',
            (game_consts.dbl_holes // 2 - 1) * game_consts.nbr_start)

        super().__init__(game_consts, game_info, player)

        self.deco.new_game = SeedOrder(self, self.deco.new_game)
        self.deco.allow = OppOrEmptyEnd(self, self.deco.allow)

        # new_game isn't called by default to allow setup of games
        self.deco.new_game.new_game()
