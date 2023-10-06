# -*- coding: utf-8 -*-
"""Determine which game holes are available for play for
the current player. Used for both activating the UI buttons
and refining into actual moves available for the AI.

Created on Sat Apr  8 09:15:30 2023

@author: Ann
"""

# %% imports

import abc

from game_log import game_log

from game_interface import GrandSlam
from game_interface import WinCond


# %%  allowable moves interface

class AllowableIf(abc.ABC):
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
                self.game.state = saved_state
                continue

            game_log.set_simulate()
            mdata = self.game.do_sow(pos)
            game_log.clear_simulate()

            if mdata.capt_loc is WinCond.ENDLESS:
                game_log.add(f'Preventing ENDLESS move {loc}',
                             game_log.IMPORT)
                self.game.state = saved_state
                continue

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
    opp has seeds. That is, only one of NoGrandSlam &
    MustShare will simulate games on any turn.

    GRANDSLAM == NOT_LEGAL is not supported for UDIRECT or SPLIT
    sow games, because it would make this more complicated
    and the UI doesn't support making holes partially active."""

    def get_allowable_holes(self):

        my_rng, opp_rng = self.game.cts.get_ranges(self.game.turn)

        if not any(self.game.board[tloc] for tloc in opp_rng):
            return self.decorator.get_allowable_holes()

        rval = [False] * self.game.cts.holes
        saved_state = self.game.state

        for pos, loc in enumerate(my_rng):
            if not self.allow_move(loc):
                self.game.state = saved_state
                continue

            game_log.set_simulate()
            mdata = self.game.do_sow(pos)
            if mdata.capt_loc is WinCond.ENDLESS:
                game_log.add(f'Preventing ENDLESS move {loc}',
                             game_log.IMPORT)
                self.game.state = saved_state
                game_log.clear_simulate()
                continue
            self.game.capture_seeds(mdata)
            game_log.clear_simulate()

            if any(self.game.board[tloc] for tloc in opp_rng):
                rval[pos] = True
            else:
                game_log.add(f'GRANDSLAM: prevented {loc}', game_log.IMPORT)

            self.game.state = saved_state

        return rval


class MemoizeAllowable(AllowableIf):
    """Allowables are checked in several places--move/end_move,
    test_pass and get_allowables--for each move.  If the game
    state hasn't changed return the same value (history of one).
    Getting game state is not trivial but less work than
    resimulating moves, only add this to the chain if there
    are deco's that do simulation."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)
        self.saved_state = None
        self.return_val = None

    def get_allowable_holes(self):

        if self.saved_state:
            cur_state = self.game.state

            if cur_state == self.saved_state:
                game_log.add('Re-using allowable result.', game_log.DETAIL)
                return self.return_val

        rval = self.decorator.get_allowable_holes()
        self.saved_state = self.game.state
        self.return_val = rval

        return rval


# %% build deco chain

def deco_allowable(game):
    """Build the allowable deco."""

    allowable = Allowable(game)

    if game.info.mustshare:
        allowable = MustShare(game, allowable)

    if game.info.grandslam == GrandSlam.NOT_LEGAL:
        allowable = NoGrandSlam(game, allowable)

    if (game.info.mustshare
            or game.info.grandslam == GrandSlam.NOT_LEGAL):
        allowable = MemoizeAllowable(game, allowable)

    return allowable
