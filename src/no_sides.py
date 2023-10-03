# -*- coding: utf-8 -*-
"""Game class for mancala games without sides;
either player can play from any hole.

Created on Thu Jan  5 03:15:41 2023
@author: Ann"""


# %% imports

import functools as ft

import allowables
import capturer
import end_move
import game_interface as gi
import get_moves
import ginfo_rules
import mancala
import sow_starter

from game_interface import Direct
from game_interface import MoveTpl
from game_log import game_log
from incrementer import NOSKIPSTART


# %%  build rules


def build_no_sides_rules():
    """Refine the GameInfo rules for NoSides."""

    def rev_getattr(name, obj):
        return getattr(obj.flags, name)

    rules = ginfo_rules.RuleDict()

    rules.add_rule(
        'need_stores',
        rule=lambda ginfo: not ginfo.flags.stores,
        msg='NoSides requires stores.',
        excp=gi.GameInfoError)

    rules.add_rule(
        'need_no_sides',
        rule=lambda ginfo: not ginfo.flags.no_sides,
        msg="NoSides requires no_sides; it will be set automatically "
            "(because it's not on the UI).",
        warn=True)

    rules.add_rule(
        'no_side_scorers',
        rule=lambda ginfo: any([ginfo.scorer.empties_m,
                                ginfo.scorer.evens_m,
                                ginfo.scorer.access_m,
                                ginfo.scorer.seeds_m]),
        msg='Scorer multipliers empties, evens, access and seeds '
            'are incompatible with NoSides.',
        excp=gi.GameInfoError)
        # child_cnt_m shouldn't be allowed either (it compares top/bot sides)

        # XXXX could override scorer for evens, empties and access
        # to max/min the total count of them. would need to
        # restructure base game scorer to allow individual
        # overrides

    rules.add_rule(
        'warn_eson_oppside',
        rule=lambda ginfo: (not ginfo.flags.capsamedir
                            and not any([ginfo.flags.evens,
                                         ginfo.flags.crosscapt,
                                         ginfo.flags.sow_own_store,
                                         ginfo.capt_on])),
        msg="Using ESON XORGOL capture mechanism without CAPSAMEDIR "
            "has very rare captures.",
        warn=True)

    bad_flags = ['grandslam', 'mustpass', 'mustshare', 'oppsidecapt',
                 'rounds', 'round_starter', 'rnd_left_fill', 'rnd_umove',
                 'visit_opp']
    for flag in bad_flags:
        rules.add_rule(
            f'bad_{flag}',
            rule=ft.partial(rev_getattr, flag),
            msg=f'NoSides cannot be used with {flag.upper()}.',
            excp=gi.GameInfoError)

    rules |= ginfo_rules.build_rules()
    del rules['bad_no_side']
    del rules['warn_no_capt']
    del rules['warn_capsamedir_multicapt']

    return rules


# %%  deco classes

class Allowable(allowables.AllowableIf):
    """Base allowable for no_sides games
    Return is a list of booleans the same size as the board and
    in the same order.
    This is 2x as long as a single side of the baord."""

    def get_allowable_holes(self):
        """Do allow_move for all locations"""

        return [self.allow_move(loc)
                for loc in range(self.game.cts.dbl_holes)]


class Moves(get_moves.MovesIf):
    """Base no turns holes mover.
    When no_turns is true, moves must be (row, pos, direct)
    no matter if udirect is true or not.
    There are no passes in no_sides games,
    because if there isn't a move then the game is over."""

    def get_moves(self):
        """If move is allowable, collect positions."""

        moves = []
        for loc, allow in enumerate(self.game.get_allowable_holes()):

            if allow:
                row = int(loc < self.game.cts.holes)
                pos = self.game.cts.xlate_pos_loc(row, loc)
                cnt = self.game.cts.loc_to_left_cnt(loc)
                if cnt in self.game.info.udir_holes:
                    moves += [MoveTpl(row, pos, Direct.CCW),
                              MoveTpl(row, pos, Direct.CW)]
                else:
                    moves += [MoveTpl(row, pos, None)]

        return moves


class SowStartMove(sow_starter.SowStartIf):
    """Start the sower. Translate move to loc."""

    def start_sow(self, move):
        """Translate move to loc. NoSides moves are (row, pos, direct).
        Call the chain.

        Arguement intentionally renamed because this method
        gets move, but calls chained decorators with loc."""
        # pylint: disable=arguments-renamed

        row, pos, _ = move
        loc = self.game.cts.xlate_pos_loc(row, pos)
        return self.decorator.start_sow(loc)


class CaptTwoOut(capturer.CaptMethodIf):
    """If the seed ended in a hole which previously had seeds,
    and the next hole is empty, capture the seeds in the
    following hole."""

    def do_captures(self, mdata):

        loc = mdata.capt_loc
        direct = mdata.direct
        loc_p1 = self.game.deco.incr.incr(loc, direct, NOSKIPSTART)
        loc_p2 = self.game.deco.incr.incr(loc_p1, direct, NOSKIPSTART)

        if (self.game.board[loc] > 1
                and not self.game.board[loc_p1]                # == 0
                and self.game.board[loc_p2]                    # > 0
                and self.game.child[loc_p2] is None
                and self.game.unlocked[loc_p2]):

            self.game.store[self.game.turn] += self.game.board[loc_p2]
            self.game.board[loc_p2] = 0
            return True
        return False


class CountOnlySeedsStores(end_move.ClaimSeedsIf):
    """Ignore unclaimed seeds; count stores and children"""
    #pylint: disable=duplicate-code

    def claim_seeds(self):

        seeds = self.game.store.copy()

        for loc in range(self.game.cts.dbl_holes):

            if self.game.child[loc] is True:
                seeds[True] += self.game.board[loc]

            elif self.game.child[loc] is False:
                seeds[False] += self.game.board[loc]

            else:
                # XXXX is removing unclaimed seeds right for game play?
                # the game is over so we don't need preserve seed count
                self.game.board[loc] = 0

        game_log.step('Divvied seeds', self.game)
        return seeds


# %%  game class

class NoSides(mancala.Mancala):
    """The NoSides game dynamics."""

    rules = build_no_sides_rules()

    def __init__(self, game_consts, game_info):
        """Set no_sides, no reason to put it in UI for this one class.
        Call parent init.
        Set the default owners.  Init false_holes (ender computes it
        and new_game uses it).
        Update the decorators:
            allow: replace the chain with our own class
            moves: replace the chain with our own class
            get_dir:  maybe nothing??
            sow_start: replace the move/loc translator
            capture: if no other capture mech provided use ours
            winner: replace bottom taker
            ender: replace bottom taker (deco chain is always the same)
            quitter: replace taker
        """

        object.__setattr__(game_info.flags, 'no_sides', True)
        super().__init__(game_consts, game_info)

        self.deco.allow = Allowable(self)
        self.deco.moves = Moves(self)
        self.deco.starter = SowStartMove(self, self.deco.starter.decorator)

        #         win   notPlay   win
        self.deco.ender.decorator.decorator.claimer = CountOnlySeedsStores(self)
        self.deco.quitter.claimer = CountOnlySeedsStores(self)

        ginfo = self.info
        if not any([ginfo.flags.evens,
                    ginfo.flags.crosscapt,
                    ginfo.flags.sow_own_store,
                    ginfo.flags.cthresh,
                    ginfo.capt_on]):

            captor = CaptTwoOut(self)
            if not ginfo.flags.capsamedir:
                captor = capturer.CaptOppDirMultiple(self, captor)

            self.deco.capturer = captor
