# -*- coding: utf-8 -*-
"""Decos to preform the seed sowing step, that is, increment
around the game board, dropping one seed into each hole.
This file contains the basic sowing decos--anything that is
not associated with mlap sowing.

The incrementer deco is used to select the increment options.

Created on Fri Apr  7 15:57:47 2023
@author: Ann"""


# %% imports

import abc

import deco_chain_if
import game_interface as gi

from game_logger import game_log



# %%  sow interface

class SowMethodIf(deco_chain_if.DecoChainIf):
    """Interface for sowing."""

    @abc.abstractmethod
    def sow_seeds(self, mdata):
        """Sow seeds from mdata.cont_sow_loc.
        Update mdata.capt_loc with the last sow location."""

    def get_single_sower(self):
        """Return the first non-lap sower in the deco chain.
        Used to deicede if allowable test OPP_OR_EMPTY is met."""
        return self


# %%  base sower

class SowSeeds(SowMethodIf):
    """Basic sower.  Handles direction, skip_start and blocks
    (via the incr)."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        loc = mdata.cont_sow_loc
        for _ in range(mdata.seeds):

            loc = self.game.deco.incr.incr(loc,
                                           mdata.direct,
                                           mdata.cont_sow_loc)
            self.game.board[loc] += 1

        mdata.capt_loc = loc


# %%  more single sowers

class SowSeedsNStore(SowMethodIf):
    """Sow a seed into the player's own store when passing it.

    If the sow ends in the store, set capt_loc to WinCond.REPEAT_TURN.

    This assumes that at least one hole is not blocked on
    each side of the board."""

    def __init__(self, game, decorator=None):

        def f_to_t_store(ploc, loc):
            """Return True if ploc is false side of the board
            (not store) and loc is on the true side of the board."""

            return (ploc != gi.WinCond.REPEAT_TURN
                    and 0 <= ploc < self.game.cts.holes
                    and self.game.cts.holes <= loc < self.game.cts.dbl_holes)

        def t_to_f_store(ploc, loc):
            """Return True if ploc is true side of the board
            (not store) and loc is on the false side of the board."""

            return (ploc != gi.WinCond.REPEAT_TURN
                    and self.game.cts.holes <= ploc < self.game.cts.dbl_holes
                    and 0 <= loc < self.game.cts.holes)

        super().__init__(game, decorator)

        self.sow_store = {gi.Direct.CCW: [f_to_t_store, t_to_f_store],
                          gi.Direct.CW: [t_to_f_store, f_to_t_store]}


    def sow_seeds(self, mdata):
        """Sow seeds.
        ploc is start hole and then follows along as the
        previously hole sown."""

        turn = self.game.turn
        incr = self.game.deco.incr.incr
        sow_store = self.sow_store[mdata.direct][turn]

        ploc = mdata.cont_sow_loc
        loc = incr(ploc, mdata.direct, mdata.cont_sow_loc)

        for _ in range(mdata.seeds):

            if sow_store(ploc, loc):
                self.game.store[turn] += 1
                ploc = gi.WinCond.REPEAT_TURN

            else:
                self.game.board[loc] += 1
                ploc = loc
                loc = incr(loc, mdata.direct, mdata.cont_sow_loc)

        if ploc == gi.WinCond.REPEAT_TURN:
            game_log.add('Sow ended in store REPEAT TURN', game_log.INFO)

        mdata.capt_loc = ploc


class DivertSkipBlckdSower(SowMethodIf):
    """Divert blocked holes on opp side out of play (to store 0).
    Skip sowing blocked holes on own side of board.

    Don't use the incrementer because it will skip blocks.
    The option to select this is:  sow_rule: SOW_BLKD_DIV

    XXXX  visit_opp is not currently supported because we need to
    close the hole if we end on goal_param seeds (ie. block it).
    This needs to occur if lapping or not.
    This doesn't quite fit the model of the code right now but might
    in the future."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        loc = mdata.cont_sow_loc
        seeds = mdata.seeds
        while seeds > 0:

            loc = (loc + mdata.direct) % self.game.cts.dbl_holes

            while self.game.blocked[loc]:
                if self.game.cts.opp_side(self.game.turn, loc):

                    self.game.store[0] += 1
                    seeds -= 1
                    if not seeds:
                        mdata.capt_loc = loc
                        return

                loc = (loc + mdata.direct) % self.game.cts.dbl_holes

            self.game.board[loc] += 1
            seeds -= 1

        mdata.capt_loc = loc


class SowClosed(SowMethodIf):
    """For SOW_BLKD_DIV without multilap sowing,
    check for closing, remove the final seeds
    from play (to store 0) and block the hole."""

    def __init__(self, game, not_right=False, decorator=None):
        super().__init__(game, decorator)
        if not_right:
            self.no_close = (game.cts.holes - 1, game.cts.dbl_holes - 1)
        else:
            self.no_close = set()

    def sow_seeds(self, mdata):
        """Sow seeds."""

        self.decorator.sow_seeds(mdata)
        loc = mdata.capt_loc

        if (loc not in self.no_close
                and self.game.board[loc] == self.game.info.goal_param
                and self.game.cts.opp_side(self.game.turn, loc)
                and not self.game.inhibitor.stop_me_capt(self.game.turn)):

            self.game.store[0] += self.game.board[loc]
            self.game.board[loc] = 0
            self.game.blocked[loc] = True


class SowCaptOwned(SowMethodIf):
    """Any holes sown to allow capture are captured by the hole's
    owner.

    OWN_SOW_CAPT_ALL:

    LAPPER: Owner's capture seeds with capt_ok, until the last seed.
    The hole that the last seed is sown into may be captured from
    the  opponent's hole (let the capturer deal with it).

    LAPPER_NEXT: Any seed with capt_ok is captured by the hole
    owner.

    SOW_CAPT_ALL:
        similar to above, but only the sower captures from
        the holes as specified by CAPT_SIDE."""

    def __init__(self, game, decorator=None):
        """Create a list of conditions (as lambda functions)
        to be tested for each hole sown.
        Prototype is cfunc(seed#, loc, turn)

        Define an captor function with prototype owner(loc, turn)"""

        super().__init__(game, decorator)
        self.conds = []

        if game.info.sow_rule == gi.SowRule.OWN_SOW_CAPT_ALL:

            # no added conditions, only need to determine capturer

            if game.info.goal == gi.Goal.TERRITORY:
                self.captor = lambda loc, turn: game.owner[loc]

            else:
                self.captor = lambda loc, turn: game.cts.board_side(loc)

        else:  #  self.game.info.sow_rule == gi.SowRule.SOW_CAPT_ALL

            # capturer is always current player
            self.captor = lambda loc, turn: turn

            if self.game.info.capt_side in (gi.CaptSide.OWN_SIDE,
                                            gi.CaptSide.OWN_CONT,
                                            gi.CaptSide.OWN_TERR):

                if game.info.goal == gi.Goal.TERRITORY:
                    self.conds += [lambda scnt, loc, turn:
                                       turn == game.owner[loc]]
                else:
                    self.conds += [lambda scnt, loc, turn:
                                       turn == game.cts.board_side(loc)]

            elif self.game.info.capt_side in (gi.CaptSide.OPP_SIDE,
                                              gi.CaptSide.OPP_CONT,
                                              gi.CaptSide.OPP_TERR):

                if game.info.goal == gi.Goal.TERRITORY:
                    self.conds += [lambda scnt, loc, turn:
                                       turn != game.owner[loc]]
                else:
                    self.conds += [lambda scnt, loc, turn:
                                       turn != game.cts.board_side(loc)]

        # LAPPER do not pick on the last seed, it's captured instead
        if game.info.mlaps == gi.LapSower.LAPPER:
            self.conds += [lambda scnt, loc, turn: scnt > 1]


    def sow_seeds(self, mdata):
        """Sow seeds."""

        incr = self.game.deco.incr.incr
        loc = mdata.cont_sow_loc
        for scnt in range(mdata.seeds, 0, -1):

            loc = incr(loc, mdata.direct, mdata.cont_sow_loc)
            self.game.board[loc] += 1

            if (all(cfunc(scnt, loc, self.game.turn) for cfunc in self.conds)
                    and not self.game.inhibitor.stop_me_capt(self.game.turn)
                    and self.game.deco.capt_ok.capture_ok(mdata, loc)):

                captor = self.captor(loc, self.game.turn)
                game_log.step(f'Capture from {loc} by {captor}')
                self.game.store[captor] += self.game.board[loc]
                self.game.board[loc] = 0

        mdata.capt_loc = loc


class SowSkipOppN(SowMethodIf):
    """Skip sowing holes with a specified number of seeds in them
    on the opponents side of the board."""

    def __init__(self, game, skip_set, decorator=None):
        super().__init__(game, decorator)
        self.skip_set = skip_set

    def sow_seeds(self, mdata):
        """Sow seeds."""

        incr = self.game.deco.incr.incr
        loc = mdata.cont_sow_loc
        for _ in range(mdata.seeds):

            loc = incr(loc, mdata.direct, mdata.cont_sow_loc)

            while (self.game.cts.opp_side(self.game.turn, loc)
                   and self.game.board[loc] in self.skip_set):

                loc = incr(loc, mdata.direct, mdata.cont_sow_loc)

            self.game.board[loc] += 1

        mdata.capt_loc = loc


class SowMaxN(SowMethodIf):
    """Never sow a hole to more than the specified number
    of seeds."""

    def __init__(self, game, max_seeds, decorator=None):
        super().__init__(game, decorator)
        self.max_seeds = max_seeds

    def sow_seeds(self, mdata):
        """Sow seeds."""

        incr = self.game.deco.incr.incr
        loc = mdata.cont_sow_loc
        for _ in range(mdata.seeds):

            loc = incr(loc, mdata.direct, mdata.cont_sow_loc)
            while self.game.board[loc] >= self.max_seeds:
                loc = incr(loc, mdata.direct, mdata.cont_sow_loc)

            self.game.board[loc] += 1

        mdata.capt_loc = loc


class SowSkipOppChild(SowMethodIf):
    """Skip sowing opponents children."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        incr = self.game.deco.incr.incr
        loc = mdata.cont_sow_loc
        for _ in range(mdata.seeds):

            loc = incr(loc, mdata.direct, mdata.cont_sow_loc)
            while self.game.child[loc] == (not self.game.turn):
                loc = incr(loc, mdata.direct, mdata.cont_sow_loc)

            self.game.board[loc] += 1

        mdata.capt_loc = loc


class SowOppCaptsLast(SowMethodIf):
    """A sower that wraps another sower until we are down to
    the last few seeds.

    When down to the last seeds (sow_param): seeds sown on the
    opponent's side are captured by the opponent. If the last
    seed would do a normal capture, the sower takes those seeds,
    including the last seed sown."""

    def sow_seeds(self, mdata):

        # use a base sower until down to the spec number of seeds
        if sum(self.game.board) > self.game.info.sow_param:
            self.decorator.sow_seeds(mdata)
            return

        incr = self.game.deco.incr.incr
        opp_side = self.game.cts.opp_side
        capt_ok = self.game.deco.capt_ok.capture_ok

        loc = mdata.cont_sow_loc
        opp_took = 0
        for rem_seeds in range(mdata.seeds, 0, -1):

            loc = incr(loc, mdata.direct, mdata.cont_sow_loc)
            self.game.board[loc] += 1    # for capt_ok test

            if (opp_side(self.game.turn, loc)
                    and (rem_seeds > 1 or not capt_ok(mdata, loc))):
                self.game.board[loc] -= 1
                self.game.store[not self.game.turn] += 1
                opp_took += 1
                mdata.captured = True

        if opp_took:
            game_log.add(f'{not self.game.turn} takes own {opp_took}.',
                         game_log.DETAIL)

        mdata.capt_loc = loc


# %% precature decorators

# captures occur after prescribed openings, (i.e. don't occur if
# there was a prescribed opening) and before the rest of the sower

# choosing not to set captured --
#   no repeat turn; Mancala doesn't need to print as changes logged below

class SCaptOne(SowMethodIf):
    """Take one seeds on the opening move."""

    def sow_seeds(self, mdata):

        self.game.store[self.game.turn] += 1
        mdata.seeds -= 1
        game_log.step('Presow Capt from lap', self.game, game_log.DETAIL)

        self.decorator.sow_seeds(mdata)


class SCaptCrossOnOne(SowMethodIf):
    """If one seed then capture any cross.
    SOW_START and XDRAW_1_XCAPT will capture the 1 drawn seed
    when there are two seeds in the start hole. Warning is produced."""

    def sow_seeds(self, mdata):

        cross = self.game.cts.cross_from_loc(mdata.cont_sow_loc)

        if (mdata.seeds == 1
            and self.game.board[cross]
            and self.game.child[cross] is None):

            self.game.store[self.game.turn] += self.game.board[cross]
            self.game.board[cross] = 0

            game_log.step(f'Presow Capt Cross at {mdata.cont_sow_loc}',
                          self.game, game_log.DETAIL)

        self.decorator.sow_seeds(mdata)


class SCaptCrossSingles(SowMethodIf):
    """Capture across from any holes that have a singleton"""

    def sow_seeds(self, mdata):

        log = []

        for loc in self.game.cts.get_my_range(self.game.turn):
            cross = self.game.cts.cross_from_loc(loc)

            if (self.game.board[loc] == 1
                and self.game.board[cross]
                and self.game.child[cross] is None):

                self.game.store[self.game.turn] += self.game.board[cross]
                self.game.board[cross] = 0
                log += [cross]

        if log:
            game_log.step(f'Presow Capt Cross all 1s from {log}',
                          self.game, game_log.DETAIL)

        self.decorator.sow_seeds(mdata)


# %% prescribed opening moves

# use prescribed openings if the first player has a choice
# if it's a standard pattern use start_pattern

class SowPrescribedIf(SowMethodIf):
    """A deco that does prescribed moves for one or more turns.
    Concrete subclasses should not provide sow_seeds."""

    def __init__(self, game, count, decorator=None):

        if not decorator:
            raise gi.GameInfoError(
                "Prescribed sower's must have follow on decorators")

        super().__init__(game, decorator)
        self.dispose = count


    @abc.abstractmethod
    def do_prescribed(self, mdata):
        """Do the prescribed opening moves."""


    def sow_seeds(self, mdata):
        """If the decorator has expired, call the child sower."""

        if self.game.mcount > self.dispose:
            self.decorator.sow_seeds(mdata)
        else:
            self.do_prescribed(mdata)


    def get_single_sower(self):
        """Get the non-prescribed single sower. Skip past
        the self and get the single sower of the next
        deco--there must be one because that's how prescribed
        sowers work.

        This is not what the allowables test wants  (for
        do_sow simulation), it should  not use it. Rules
        should prevent it.

        BearOff uses this to wrap the single sower."""

        return self.decorator.get_single_sower()


class SowBasicFirst(SowPrescribedIf):
    """Use the default basic sower for the first sows."""

    def __init__(self, game, count, decorator=None):
        super().__init__(game, count, decorator)
        self.sower = SowSeeds(game)


    def do_prescribed(self, mdata):
        self.sower.sow_seeds(mdata)


class SowOneOpp(SowPrescribedIf):
    """The last seed must be on the opponents side of the board
    skip our own holes, if required, to make that happen."""

    def do_prescribed(self, mdata):

        loc = mdata.cont_sow_loc
        incrementer = self.game.deco.incr.incr

        for _ in range(mdata.seeds - 1):

            loc = incrementer(loc, mdata.direct, mdata.cont_sow_loc)
            self.game.board[loc] += 1

        loc = incrementer(loc, mdata.direct, mdata.cont_sow_loc)
        while not self.game.cts.opp_side(self.game.turn, loc):
            loc = incrementer(loc, mdata.direct, mdata.cont_sow_loc)
        self.game.board[loc] += 1

        mdata.capt_loc = loc


class SowPlus1Minus1Capt(SowPrescribedIf):
    """Starting after the selected move one seed forward
    in every other hole."""

    def do_prescribed(self, mdata):

        loc = mdata.cont_sow_loc
        self.game.board[loc] = mdata.seeds
        incrementer = self.game.deco.incr.incr

        add_one = False
        while True:
            loc = incrementer(loc, mdata.direct, mdata.cont_sow_loc)
            if loc == mdata.cont_sow_loc:
                break
            self.game.board[loc] += 1 if add_one else -1
            add_one = not add_one

        cross = self.game.cts.cross_from_loc(mdata.cont_sow_loc)
        self.game.board[cross] += 1

        mdata.capt_loc = cross
