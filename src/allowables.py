# -*- coding: utf-8 -*-
"""Determine which game holes are available for play for
the current player. Used for both activating the UI buttons
and refining into actual moves available for the AI.

Created on Sat Apr  8 09:15:30 2023

@author: Ann
"""

# %% imports

import abc

from game_interface import GrandSlam
from game_interface import WinCond


# %%  allowable moves interface

class AllowableIf:
    """Allowable interface plus one common routine."""

    def __init__(self, game, decorator=None):
        self.game = game
        self.decorator = decorator

    def allow_move(self, loc):
        """Allowable:
            Hole must have min_move seeds.
            Hole must not be blocked.
            Hole must not be designated a child.

        If BLOCKED flag isn't set, the blocked array will be all False;
        so we can always use the boolean array.

        If CHILD flag isn't set, the child array will always be None;
        so we can always use the array."""

        return (self.game.board[loc] >= self.game.info.min_move
                and not self.game.blocked[loc]
                and self.game.child[loc] is None)

    @abc.abstractmethod
    def get_allowable_holes(self):
        """Return boolean array of plyable/allowable of length holes."""


# %% base class

class Allowable(AllowableIf):
    """Base allowable."""

    def get_allowable_holes(self):
        """Do allow_move for all locations"""

        return [self.allow_move(loc)
                for loc in self.game.cts.get_my_range(self.game.turn)]


# %%  decorators


class MustShare(AllowableIf):
    """If opponent has moves, return delegated get_allowable;
    Otherwise: Only allowable moves are those that provide
    seeds to the opponent.

    MUSTSHARE is not supported for UDIRECT or SPLIT sow games.
    Currently the MancalaUI makes a button active/inactive
    not left and/or right active."""

    def get_allowable_holes(self):
        """Return allowable moves."""

        my_rng, opp_rng = self.game.cts.get_ranges(self.game.turn)

        if any(self.game.board[loc] for loc in opp_rng):
            return self.decorator.get_allowable_holes()

        rval = [False] * self.game.cts.holes
        saved_state = self.game.state

        for pos, loc in enumerate(my_rng):
            if not self.allow_move(loc):
                continue

            self.game.do_sow(pos)

            if any(self.game.board[tloc] for tloc in opp_rng):
                rval[pos] = True

            self.game.state = saved_state

        return rval


class NoGrandSlam(AllowableIf):
    """Grand slam - taking all of opponents seeds is not legal.

    If the opponent doesn't have any seeds at the start,
    pass test down the chain.
    If the opponent has seeds, we must not capture them all.

    MUSTSHARE is don't care because we only process here if
    opp has seeds.

    GRANDSLAM == NOT_LEGAL is not supported for UDIRECT or SPLIT
    sow games, because it would make this more complicated
    and the UI doesn't support make holes partially active."""

    def get_allowable_holes(self):

        my_rng, opp_rng = self.game.cts.get_ranges(self.game.turn)

        if not any(self.game.board[tloc] for tloc in opp_rng):
            return self.decorator.get_allowable_holes()

        rval = [False] * self.game.cts.holes
        saved_state = self.game.state

        for pos, loc in enumerate(my_rng):
            if not self.allow_move(loc):
                continue

            tloc, direct = self.game.do_sow(pos)
            if tloc is WinCond.ENDLESS:
                continue
            self.game.capture_seeds(tloc, direct)

            if any(self.game.board[tloc] for tloc in opp_rng):
                rval[pos] = True

            self.game.state = saved_state

        return rval


# %% build deco chain

def deco_allowable(game):
    """Build the allowable deco."""

    allowable = Allowable(game)

    if game.info.flags.mustshare:
        allowable = MustShare(game, allowable)

    if game.info.flags.grandslam == GrandSlam.NOT_LEGAL:
        allowable = NoGrandSlam(game, allowable)

    return allowable
