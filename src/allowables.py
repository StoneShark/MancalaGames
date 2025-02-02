# -*- coding: utf-8 -*-
"""Determine which game holes are available for play for
the current player. Used for activating the UI buttons;
determining if the game is over, if there should be a
required pass, and the moves available for the AI player.

Memoize should be added at the top of any deco chain that
involves simulating moves. Getting and checking state is
not trivial, so don't add it indiscriminantely.

In general the individual decos defer to the child deco
until Allowable or AllowableTriples and then filter the
result by removing some allowable holes.

Created on Sat Apr  8 09:15:30 2023
@author: Ann"""


# %% imports

import abc

import deco_chain_if
import game_interface as gi

from game_logger import game_log


# %%  allowable moves interface

class AllowableIf(deco_chain_if.DecoChainIf):
    """Allowable interface plus some utility methods."""

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


    def get_holes_idx(self):
        """Return a pair of lists (one for each side) that correlates
        the index in the allowables array with the hole loc.
        If triples, use the same array for both.
        Otherwise, the index is pos."""

        holes = self.game.cts.holes
        dbl_holes = self.game.cts.dbl_holes

        if self.game.info.mlength == 3:
            fholes = [(p, p) for p in range(dbl_holes)]
            tholes = fholes
        else:
            fholes = [(p, p) for p in range(holes)]
            tholes = [(dbl_holes - p - 1, p) for p in range(holes, dbl_holes)]
        return fholes, tholes


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


class DontUndoMoveOne(AllowableIf):
    """For split sow games don't allow moving a singleton
    back across the board side in the immediate next move."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)
        self.end_sets = [set([0, game.cts.dbl_holes - 1]),
                         set([game.cts.holes - 1, game.cts.holes])]

        if game.info.mlength == 3:
            self.aidx = lambda cloc: cloc
        else:
            self.aidx = lambda cloc: cloc if cloc < game.cts.holes \
                                          else game.cts.dbl_holes - cloc - 1

    @staticmethod
    def include(game):
        """Return True if this deco should be included, otherwise False.
        Min move must be 1.
        SPLIT sow but without either end in the UDIR_HOLES"""

        return (game.info.min_move == 1
                and game.info.sow_direct == gi.Direct.SPLIT
                and 0 not in game.info.udir_holes
                and game.cts.holes - 1 not in game.info.udir_holes)

    def get_allowable_holes(self):

        allow = self.decorator.get_allowable_holes()
        lmdata = self.game.last_mdata
        if not lmdata:
            return allow

        capt_loc = lmdata.capt_loc
        if capt_loc == gi.WinCond.REPEAT_TURN:
            return allow

        aidx = self.aidx(capt_loc)
        if not allow[aidx]:
            return allow

        if (lmdata.seeds == 1
                and self.game.board[capt_loc] == 1
                and any(set([lmdata.sow_loc, capt_loc]) == test_set
                        for test_set in self.end_sets)):

            game_log.add(f"Preventing undo @ {aidx}.")
            allow[aidx] = False

        return allow


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

            mdata = self.game.sim_single_sow(pos)
            self.game.state = saved_state

            end_loc = mdata.capt_loc
            if end_loc in my_rng and self.game.board[end_loc]:
                game_log.add(f'OppOrEmpty: prevented {pos}', game_log.DETAIL)
                allow[pos] = False

        return allow


class SingleToZero(AllowableIf):
    """Can only move holes with single seeds to the next hole
    if it empty.
    Support allow length of holes and dbl_holes (move triples)."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)
        self.fholes, self.tholes = self.get_holes_idx()

    def get_allowable_holes(self):
        """Return allowable moves."""

        allow = self.decorator.get_allowable_holes()

        holes = self.tholes if self.game.turn else self.fholes
        for idx, loc in holes:

            direct = self.game.deco.get_dir.get_direction(loc, loc)
            nloc = self.game.deco.incr.incr(loc, direct)

            if (allow[idx]
                    and self.game.board[loc] == 1
                    and self.game.board[nloc]):
                allow[idx] = False

        return allow


class OnlyIfAllN(AllowableIf):
    """Can't move from a hole with N seeds unless they
    are all N seeds (or not allowable for another reason).
    Support allow length of holes and dbl_holes (move triples)."""

    def __init__(self, game, const, decorator=None):

        super().__init__(game, decorator)
        self.const = const
        self.fholes, self.tholes = self.get_holes_idx()

    def get_allowable_holes(self):
        """Return allowable moves."""

        allow = self.decorator.get_allowable_holes()
        holes = self.tholes if self.game.turn else self.fholes

        if any(allow[idx] and self.game.board[loc] != self.const
               for idx, loc in holes):

            for idx, loc in holes:
                if allow[idx] and self.game.board[loc] == self.const:
                    allow[idx] = False

        return allow


class AllTwoRightmost(AllowableIf):
    """Can't move from holes containing two, unless all holes
    have two (or zero), and THEN only the rightmost hole with two seeds.
    This class does not support move triples, but still uses get_holes_idx."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)
        self.fholes, self.tholes = self.get_holes_idx()

    def get_allowable_holes(self):
        """Return allowable moves."""

        allow = self.decorator.get_allowable_holes()
        holes = self.tholes if self.game.turn else self.fholes

        if any(allow[idx] and self.game.board[loc] != 2 for idx, loc in holes):

            # allowables do not all have 2 seeds, remove any holes with 2 seeds
            for idx, loc in holes:
                if self.game.board[loc] == 2:
                    allow[idx] = False

        else:
            # all allowables contain 2 seeds, remove all but rightmost hole
            if self.game.turn:
                from_right = range(0, self.game.cts.holes, 1)
            else:
                from_right = range(self.game.cts.holes - 1, -1, -1)

            found = False
            for pos in from_right:
                if allow[pos]:
                    if found:
                        allow[pos] = False
                    found = True

        return allow


class OnlyRightTwo(AllowableIf):
    """On the first turn (called before mcount's first increment),
    can only move from the rightmost two allowable holes."""

    def get_allowable_holes(self):
        """Return allowable moves."""

        allow = self.decorator.get_allowable_holes()
        if self.game.mcount:
            return allow

        if self.game.turn:
            from_right = range(0, self.game.cts.holes, 1)
        else:
            from_right = range(self.game.cts.holes - 1, -1, -1)

        found = 0
        for pos in from_right:

            if allow[pos]:
                found += 1

                if found > 2:
                    allow[pos] = False

        return allow



class MustShare(AllowableIf):
    """If opponent has moves, return delegated get_allowable;
    Otherwise, filter out allowables that do not provide seeds
    to the opponent.
    Support allow length of holes and dbl_holes (move triples)."""

    def __init__(self, game, owners, decorator=None):

        def get_owner_move(row, pos):
            return gi.MoveTpl(row, pos, None)

        def get_move(_, pos):
            return pos

        def get_owner_owner(loc):
            return game.owner[loc]

        super().__init__(game, decorator)
        self.fholes, self.tholes = self.get_holes_idx()

        if owners:
            self.make_move = get_owner_move
            self.owner = get_owner_owner
        else:
            self.make_move = get_move
            self.owner = game.cts.board_side


    def opp_has_seeds(self, opponent):
        """Return true if any holes owned by the opponent
        have seeds in them."""

        return any(self.game.board[loc]
                   for loc in range(self.game.cts.dbl_holes)
                   if (self.owner(loc) == opponent
                       and self.game.child[loc] is None))


    def get_allowable_holes(self):
        """Return allowable moves."""

        allow = self.decorator.get_allowable_holes()

        opponent = not self.game.turn
        if self.opp_has_seeds(opponent):
            return allow

        holes = self.tholes if self.game.turn else self.fholes
        saved_state = self.game.state

        for idx, loc in holes:
            if not allow[idx]:
                continue

            row = int(loc < self.game.cts.holes)
            pos = self.game.cts.xlate_pos_loc(row, loc)
            self.game.sim_sow_capt(self.make_move(row, pos))

            if not self.opp_has_seeds(opponent):
                game_log.add(f'MUSTSHARE: prevented {loc}', game_log.DETAIL)
                allow[idx] = False

            self.game.state = saved_state

        return allow


class MustShareUdir(MustShare):
    """Must Share for games with some udirect holes."""

    def __init__(self, game, decorator=None):

        def get_move_triple(row, pos, direct=None):
            return gi.MoveTpl(row, pos, direct)

        def get_move_pair(_, pos, direct=None):
            return gi.MoveTpl(pos, direct)

        def get_move(_1, pos, _2=None):
            return pos

        def get_owner_owner(loc):
            return game.owner[loc]

        super().__init__(game, False, decorator)
        self.fholes, self.tholes = self.get_holes_idx()
        # self.udirs = TODO precompute what holes to process

        self.make_move = [get_move,
                          get_move_pair,
                          get_move_triple][game.info.mlength - 1]

        if game.info.mlength == 3:          # TODO is the right condition TERRITORY?
            self.owner = get_owner_owner
        else:
            self.owner = game.cts.board_side


    def get_allowable_holes(self):
        """Return allowable moves."""

        allow = self.decorator.get_allowable_holes()

        opponent = not self.game.turn
        if self.opp_has_seeds(opponent):
            return allow

        holes = self.tholes if self.game.turn else self.fholes
        saved_state = self.game.state

        for idx, loc in holes:
            if not allow[idx]:
                continue

            row = int(loc < self.game.cts.holes)
            pos = self.game.cts.xlate_pos_loc(row, loc)

            cnt = self.game.cts.loc_to_left_cnt(loc)
            if cnt in self.game.info.udir_holes:
                pos_allow = [True, True]
                for pidx, direct in enumerate([gi.Direct.CW, gi.Direct.CCW]):

                    move = self.make_move(row, pos, direct)
                    self.game.sim_sow_capt(move)
                    if not self.opp_has_seeds(opponent):
                        game_log.add(f'MUSTSHARE: prevented {loc} {direct}',
                                     game_log.DETAIL)
                        pos_allow[pidx] = False

                    self.game.state = saved_state

                if not pos_allow[0] and not pos_allow[1]:
                    allow[idx] = False
                elif pos_allow[0] != pos_allow[1]:
                    allow[idx] = pos_allow

            else:
                self.game.sim_sow_capt(self.make_move(row, pos, None))

                if not self.opp_has_seeds(opponent):
                    game_log.add(f'MUSTSHARE: prevented {loc}', game_log.DETAIL)
                    allow[idx] = False

                self.game.state = saved_state

        return allow


class NoGrandSlam(AllowableIf):
    """Grand slam - taking all of opponents seeds is not legal.

    If the opponent doesn't have any playable seeds at the start,
    grandslam not possible, return the unfiltered allowables.
    If the opponent has seeds, filter any moves that remove them
    all.

    MUSTSHARE is don't care because we only process here if
    opp has seeds. That is, only one of NoGrandSlam &
    MustShare will simulate games on any turn.

    GRANDSLAM == NOT_LEGAL is not supported for UDIRECT or SPLIT
    sow games, because it would make this more complicated
    and the UI doesn't support making holes partially active."""

    def no_seeds(self, opp_rng):
        """Return true if there are not any seeds outside of children
        in opp_rng."""

        return not any(self.game.board[loc]
                       for loc in opp_rng
                       if self.game.child[loc] is None)

    def get_allowable_holes(self):

        my_rng, opp_rng = self.game.cts.get_ranges(self.game.turn)
        allow = self.decorator.get_allowable_holes()

        if self.no_seeds(opp_rng):
            return allow

        saved_state = self.game.state

        for pos, loc in enumerate(my_rng):
            if not allow[pos]:
                self.game.state = saved_state
                continue

            self.game.sim_sow_capt(pos)

            if self.no_seeds(opp_rng):
                allow[pos] = False
                game_log.add(f'GRANDSLAM: prevented {loc}', game_log.IMPORT)

            self.game.state = saved_state

        return allow


class MoveAllFirst(AllowableIf):
    """Must move from each of the holes in the first dbl_holes
    moves.

    Locks are used: initially all holes are locked.
    Until all the holes are unlocked, moves are only allowed from
    holes that are locked and allowable.

    After all holes have been unlocked the allowable result is
    always returned."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        if game.info.mlength == 3:
            # allowables will filter holes we don't own
            self.range = lambda _: range(game.cts.dbl_holes)
        else:
            self.range = game.cts.get_my_range

    def get_allowable_holes(self):

        unlocked = [self.game.unlocked[loc]
                    for loc in self.range(self.game.turn)]
        allowable = self.decorator.get_allowable_holes()

        if all(unlocked):
            return allowable

        return [not unlock and allow
                for (unlock, allow) in zip(unlocked, allowable)]


class NotXfromOnes(AllowableIf):
    """Holes across from 1s are not allowable.
    This not supported for move triples."""

    def get_allowable_holes(self):

        ones = [self.game.board[loc] == 1
                    for loc in self.game.cts.get_opp_range(self.game.turn)]
        allowable = self.decorator.get_allowable_holes()

        return [not ones and allow
                for (ones, allow) in zip(ones, allowable)]


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
    # pylint: disable=too-complex

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

    elif game.info.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST:
        allowable = MoveAllFirst(game, allowable)

    elif game.info.allow_rule == gi.AllowRule.NOT_XFROM_1S:
        allowable = NotXfromOnes(game, allowable)

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
        if game.info.udirect:
            allowable = MustShareUdir(game, allowable)
        else:
            allowable = MustShare(game, game.info.mlength == 3, allowable)

    if game.info.grandslam == gi.GrandSlam.NOT_LEGAL:
        allowable = NoGrandSlam(game, allowable)

    if DontUndoMoveOne.include(game):
        allowable = DontUndoMoveOne(game, allowable)

    if (game.info.mustshare
            or game.info.allow_rule == gi.AllowRule.OPP_OR_EMPTY
            or game.info.grandslam == gi.GrandSlam.NOT_LEGAL):
        allowable = MemoizeAllowable(game, allowable)

    return allowable
