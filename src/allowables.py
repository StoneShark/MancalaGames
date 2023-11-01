# -*- coding: utf-8 -*-
"""Determine which game holes are available for play for
the current player. Used for both activating the UI buttons
and refining into actual moves available for the AI.

Created on Sat Apr  8 09:15:30 2023

@author: Ann
"""

# %% imports

import abc

import game_interface as gi

from game_log import game_log
from game_interface import AllowRule
from game_interface import GrandSlam
from game_interface import WinCond
from incrementer import NOSKIPSTART


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


# %% base classes

class Allowable(AllowableIf):
    """Base allowable."""

    def get_allowable_holes(self):
        """Do allow_move for all locations"""

        return [self.allow_move(loc)
                for loc in self.game.cts.get_my_range(self.game.turn)]


class AllowableTriples(AllowableIf):
    """Base allowable for games in which the player can move from
    both sides of the board, e.g. territory and no_sides.
    Return is a list of booleans the same size as the board and
    in the same order."""

    def get_allowable_holes(self):
        """Do allow_move for all locations"""

        return [(self.game.owner[loc] is None
                 or self.game.turn == self.game.owner[loc])
                and self.allow_move(loc)
                for loc in range(self.game.cts.dbl_holes)]



# %%  decorators

class OppOrEmptyEnd(AllowableIf):
    """Can only play from holes that end in an empty hole or
    on the opponents side of the board."""

    def get_allowable_holes(self):

        allow = self.decorator.get_allowable_holes()
        saved_state = self.game.state
        my_rng = self.game.cts.get_my_range(self.game.turn)

        for pos in range(self.game.cts.holes):
            if not allow[pos] or self.game.board[pos] > self.game.cts.holes:
                continue

            game_log.set_simulate()
            mdata = self.game.do_single_sow(pos)
            game_log.clear_simulate()
            self.game.state = saved_state

            end_loc = mdata.capt_loc
            if end_loc in my_rng and self.game.board[end_loc]:
                allow[pos] = False

        return allow


class SingleToZero(AllowableIf):
    """Can only move holes with single seeds to the next hole
    if it empty."""

    def get_allowable_holes(self):
        """Return allowable moves."""

        allow = self.decorator.get_allowable_holes()

        for loc in self.game.cts.get_my_range(self.game.turn):

            pos = self.game.cts.xlate_pos_loc(not self.game.turn, loc)
            direct = self.game.deco.get_dir.get_direction(loc, loc)
            nloc = self.game.deco.incr.incr(loc, direct, NOSKIPSTART)

            if (allow[pos]
                    and self.game.board[loc] == 1
                    and self.game.board[nloc]):
                allow[pos] = False

        return allow


class OnlyIfAllN(AllowableIf):
    """Can't move from a hole with a N seed unless they
    are all N seeds (or zero).

    Pass 1: exclude all holes with N, use this if any allowable
    Pass 2: can move from any allowable hole"""

    def __init__(self, game, const, decorator=None):

        super().__init__(game, decorator)
        self.const = const

    def get_allowable_holes(self):
        """Return allowable moves."""

        allow = [self.allow_move(loc) and self.game.board[loc] != self.const
                for loc in self.game.cts.get_my_range(self.game.turn)]
        if any(allow):
            return allow

        return self.decorator.get_allowable_holes()


class AllTwoRightmost(AllowableIf):
    """Can't move from holes containing two, unless all holes
    have two (or zero), and THEN only the rightmost hole with two seeds."""

    def get_allowable_holes(self):
        """Return allowable moves."""

        allow = [self.allow_move(loc) and self.game.board[loc] != 2
                for loc in self.game.cts.get_my_range(self.game.turn)]
        if any(allow):
            return allow

        turn= self.game.turn
        holes = self.game.cts.holes
        dbl_holes = self.game.cts.dbl_holes
        rightedge = (dbl_holes if turn else holes) - 1
        leftedge = (holes if turn else 0) - 1
        allow = [False] * holes

        for loc in range(rightedge, leftedge, -1):
            if self.game.board[loc] == 2:
                pos = self.game.cts.xlate_pos_loc(not self.game.turn, loc)
                allow[pos] = True
                break

        return allow


class MustShare(AllowableIf):
    """If opponent has moves, return delegated get_allowable;
    Otherwise: Only allowable moves are those that provide
    seeds to the opponent.

    MUSTSHARE is not supported for UDIRECT sow games.
    Currently the MancalaUI makes a button active/inactive
    not left and/or right active."""


    def opp_has_seeds(self, opp_range):
        """Return true if the opponent has playable holes."""

        return any(self.game.board[loc] >= self.game.info.min_move
                   for loc in opp_range
                   if self.game.child[loc] is None)

    def get_allowable_holes(self):
        """Return allowable moves."""

        my_rng, opp_rng = self.game.cts.get_ranges(self.game.turn)

        if self.opp_has_seeds(opp_rng):
            return self.decorator.get_allowable_holes()

        rval = [False] * self.game.cts.holes
        saved_state = self.game.state

        for pos, loc in enumerate(my_rng):
            if not self.allow_move(loc):
                self.game.state = saved_state
                continue

            game_log.set_simulate()
            cond = self.game.move(pos)
            game_log.clear_simulate()

            if cond is WinCond.ENDLESS:
                game_log.add(f'Preventing ENDLESS move {loc}',
                             game_log.IMPORT)
                self.game.state = saved_state
                continue

            if self.opp_has_seeds(opp_rng):
                rval[pos] = True

            self.game.state = saved_state

        return rval


class MustShareOwners(AllowableIf):
    """If opponent has moves, return delegated get_allowable;
    Otherwise: Only allowable moves are those that provide
    seeds to the opponent.

    Moves are triples."""

    def opp_has_seeds(self, opponent):
        """Return true if any holes owned by the opponent
        have playbale seeds in them."""

        return any(self.game.board[loc] >= self.game.info.min_move
                   for loc in range(self.game.cts.dbl_holes)
                   if self.game.owner[loc] == opponent
                       and self.game.child[loc] is None)

    def get_allowable_holes(self):
        """Return allowable moves."""

        opponent = not self.game.turn
        if self.opp_has_seeds(opponent):
            return self.decorator.get_allowable_holes()

        holes = self.game.cts.holes
        dbl_holes = self.game.cts.dbl_holes
        rval = [False] * dbl_holes
        saved_state = self.game.state

        for loc in range(dbl_holes):
            if not self.allow_move(loc):
                self.game.state = saved_state
                continue

            game_log.set_simulate()
            cond = self.game.move(gi.MoveTpl(loc < holes, loc, None))
            game_log.clear_simulate()

            if cond is WinCond.ENDLESS:
                game_log.add(f'Preventing ENDLESS move {loc}',
                             game_log.IMPORT)
                self.game.state = saved_state
                continue

            if self.opp_has_seeds(opponent):
                rval[loc] = True

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


def deco_allow_rule(game, allowable):
    """Add the allow rule decos."""

    if game.info.allow_rule == AllowRule.OPP_OR_EMPTY:
        allowable = OppOrEmptyEnd(game, allowable)

    elif game.info.allow_rule == AllowRule.SINGLE_TO_ZERO:
        allowable = SingleToZero(game, allowable)

    elif game.info.allow_rule == AllowRule.SINGLE_ONLY_ALL:
        allowable = OnlyIfAllN(game, 1, allowable)

    elif game.info.allow_rule == AllowRule.SINGLE_ALL_TO_ZERO:
        allowable = OnlyIfAllN(game, 1, allowable)
        allowable = SingleToZero(game, allowable)

    elif game.info.allow_rule == AllowRule.TWO_ONLY_ALL:
        allowable = OnlyIfAllN(game, 2, allowable)

    elif game.info.allow_rule == AllowRule.TWO_ONLY_ALL_RIGHT:
        allowable = AllTwoRightmost(game, allowable)

    elif game.info.allow_rule == AllowRule.FIRST_TURN_ONLY_RIGHT_TWO:
        # TODO implement FIRST_TURN_ONLY_RIGHT_TWO (need to know turn #?)
        raise NotImplementedError("FIRST_TURN_ONLY_RIGHT_TWO")

    return allowable


def deco_allowable(game):
    """Build the allowable deco."""

    if game.info.mlength == 3:
        allowable =  AllowableTriples(game)
    else:
        allowable = Allowable(game)

    allowable = deco_allow_rule(game, allowable)

    if game.info.mustshare:
        if game.info.mlength == 3:
            allowable = MustShareOwners(game, allowable)
        else:
            allowable = MustShare(game, allowable)

    if game.info.grandslam == GrandSlam.NOT_LEGAL:
        allowable = NoGrandSlam(game, allowable)

    if (game.info.mustshare
            or game.info.allow_rule
            or game.info.grandslam == GrandSlam.NOT_LEGAL):
        allowable = MemoizeAllowable(game, allowable)

    return allowable
