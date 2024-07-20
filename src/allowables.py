# -*- coding: utf-8 -*-
"""Determine which game holes are available for play for
the current player. Used for both activating the UI buttons
and refining into actual moves available for the AI.

Created on Sat Apr  8 09:15:30 2023
@author: Ann"""

# %% imports

import abc

import deco_chain_if
import game_interface as gi

from game_logger import game_log


# %%  allowable moves interface

class AllowableIf(deco_chain_if.DecoChainIf):
    """Allowable interface plus one common routine."""

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
            nloc = self.game.deco.incr.incr(loc, direct)

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

        turn = self.game.turn
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


class OnlyRightTwo(AllowableIf):
    """Can only move from the right two holes, but avoid any blocks.

    Start from rightmost side of current turn's board and increment
    clockwise to move left. If we stay on our side of the board, it
    is an allowable move."""

    def get_allowable_holes(self):
        """Return allowable moves."""

        if self.game.mcount < 1:

            my_row = not self.game.turn
            allow = [False] * self.game.cts.holes
            if self.game.turn:
                loc = self.game.cts.dbl_holes
            else:
                loc = self.game.cts.holes

            for _ in range(2):

                loc = self.game.deco.incr.incr(loc, gi.Direct.CW)
                if self.game.cts.my_side(self.game.turn, loc):
                    pos = self.game.cts.xlate_pos_loc(my_row, loc)
                    allow[pos] = True

            return allow

        return self.decorator.get_allowable_holes()


class MustShare(AllowableIf):
    """If opponent has moves, return delegated get_allowable;
    Otherwise: Only allowable moves are those that provide
    seeds to the opponent."""

    def __init__(self, game, owners, decorator=None):

        def get_owner_move(row, pos):
            return gi.MoveTpl(row, pos, None)

        def get_move(_, pos):
            return pos

        def get_owner_owner(loc):
            return game.owner[loc]

        def get_owner_range(_):
            return range(game.cts.dbl_holes)

        def get_range(turn):
            return game.cts.get_my_range(turn)


        super().__init__(game, decorator)

        if owners:
            self.size = game.cts.dbl_holes
            self.make_move = get_owner_move
            self.owner = get_owner_owner
            self.get_range = get_owner_range
        else:
            self.size = game.cts.holes
            self.make_move = get_move
            self.owner = game.cts.board_side
            self.get_range = get_range


    def opp_has_seeds(self, opponent):
        """Return true if any holes owned by the opponent
        have playbale seeds in them."""

        return any(self.game.board[loc] >= self.game.info.min_move
                   for loc in range(self.game.cts.dbl_holes)
                   if (self.owner(loc) == opponent
                       and self.game.child[loc] is None))


    def test_allowable(self, allow, opponent, row, pos, loc):
        """Test row/pos/loc to see if it provides the
        opponent with seeds."""
        # pylint: disable=too-many-arguments

        if not self.allow_move(loc):
            return

        game_log.set_simulate()
        self.game.move(self.make_move(row, pos))
        game_log.clear_simulate()

        if self.opp_has_seeds(opponent):
            idx = pos if self.size == self.game.cts.holes else loc
            allow[idx] = True


    def get_allowable_holes(self):
        """Return allowable moves."""

        opponent = not self.game.turn
        if self.opp_has_seeds(opponent):
            return self.decorator.get_allowable_holes()

        allow = [False] * self.size
        saved_state = self.game.state

        for loc in self.get_range(self.game.turn):
            row = int(loc < self.game.cts.holes)
            pos = self.game.cts.xlate_pos_loc(row, loc)
            self.test_allowable(allow, opponent, row, pos, loc)
            self.game.state = saved_state

        return allow


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

            if mdata.capt_loc is gi.WinCond.ENDLESS:
                rval[pos] = True
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

    if game.info.allow_rule == gi.AllowRule.NONE:
        pass

    elif game.info.allow_rule == gi.AllowRule.OPP_OR_EMPTY:
        allowable = OppOrEmptyEnd(game, allowable)

    elif game.info.allow_rule == gi.AllowRule.SINGLE_TO_ZERO:
        allowable = SingleToZero(game, allowable)

    elif game.info.allow_rule == gi.AllowRule.SINGLE_ONLY_ALL:
        allowable = OnlyIfAllN(game, 1, allowable)

    elif game.info.allow_rule == gi.AllowRule.SINGLE_ALL_TO_ZERO:
        allowable = OnlyIfAllN(game, 1, allowable)
        allowable = SingleToZero(game, allowable)

    elif game.info.allow_rule == gi.AllowRule.TWO_ONLY_ALL:
        allowable = OnlyIfAllN(game, 2, allowable)

    elif game.info.allow_rule == gi.AllowRule.TWO_ONLY_ALL_RIGHT:
        allowable = AllTwoRightmost(game, allowable)

    elif game.info.allow_rule == gi.AllowRule.FIRST_TURN_ONLY_RIGHT_TWO:
        allowable = OnlyRightTwo(game, allowable)

    elif game.info.allow_rule == gi.AllowRule.RIGHT_2_1ST_THEN_ALL_TWO:
        allowable = OnlyIfAllN(game, 2, allowable)
        allowable = OnlyRightTwo(game, allowable)

    else:
        raise NotImplementedError(
                f"AllowRule {game.info.allow_rule} not implemented.")

    return allowable


def deco_allowable(game):
    """Build the allowable deco."""

    if game.info.mlength == 3:
        allowable = AllowableTriples(game)
    else:
        allowable = Allowable(game)

    allowable = deco_allow_rule(game, allowable)

    if game.info.mustshare:
        allowable = MustShare(game, game.info.mlength == 3, allowable)

    if game.info.grandslam == gi.GrandSlam.NOT_LEGAL:
        allowable = NoGrandSlam(game, allowable)

    if (game.info.mustshare
            or game.info.allow_rule
            or game.info.grandslam == gi.GrandSlam.NOT_LEGAL):
        allowable = MemoizeAllowable(game, allowable)

    return allowable
