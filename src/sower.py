# -*- coding: utf-8 -*-
"""Preform the seed sowing step, that is, increment around
the game board, dropping one seed into each hole.

Any 'soft' direction (e.g. split, user choice) has already been
translated to clockwise or counter-clockwise (i.e. CW or CCW).
The sow_starter deco chain has already adjusted the strat hole
contents and determined the number of seeds to sow.

The incrementer deco is used to select the increment options.

For the multi lap sowers, sowing is terminated after 50 sows
returning an error condition.

Created on Fri Apr  7 15:57:47 2023
@author: Ann"""


# %% imports

import abc

from game_log import game_log
from game_interface import Direct
from game_interface import Goal
from game_interface import LapSower
from game_interface import SowPrescribed
from game_interface import WinCond
from incrementer import NOSKIPSTART


# %% constants

MAX_LAPS = 50


# %%  sow interface

class SowMethodIf(abc.ABC):
    """Interface for sowing."""

    def __init__(self, game, decorator=None):
        self.game = game
        self.decorator = decorator

    @abc.abstractmethod
    def sow_seeds(self, mdata):
        """Sow seeds from mdata.cont_sow_loc.
        Update mdata.capt_loc with the last sow location.
        RETURN mdata."""

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
        return mdata


# %%

class SowSeedsNStore(SowMethodIf):
    """Sow a seed into the player's own store when passing it.

    If the sow ends in the store, return WinCond.REPEAT_TURN.
    Usually it means that sowing player gets another turn.

    Fill Store: If we have just incremented past current
    player's store, eval True to state that we should stop
    and put a seed into the store.
    Poses: don't bother looking up fill_store if loc isn't
    in this tuple."""

    def __init__(self, game, decorator=None):
        super().__init__(game, decorator)

        self.fill_store = ((self.game.cts.holes - 1,       # for CW not turn
                            self.game.cts.dbl_holes - 1),  # for CW turn
                           (0, 0),                         # not used
                           (self.game.cts.holes, 0))       # for CCW

        if game.info.sow_direct == Direct.CW:
            self.poses = (self.game.cts.holes - 1,
                          self.game.cts.dbl_holes - 1)
        elif game.info.sow_direct == Direct.CCW:
            self.poses = (0, self.game.cts.holes)
        else:
            self.poses = (0, self.game.cts.holes - 1,
                          self.game.cts.holes, self.game.cts.dbl_holes - 1)


    def sow_seeds(self, mdata):
        """Sow seeds.
        Copy some deep values into locals a bit of speed."""

        turn = self.game.turn
        incr = self.game.deco.incr.incr

        loc = mdata.cont_sow_loc
        seeds = mdata.seeds

        while seeds > 0:

            loc = incr(loc, mdata.direct, mdata.cont_sow_loc)

            if (loc in self.poses
                    and loc == self.fill_store[mdata.direct + 1][turn]):

                self.game.store[turn] += 1
                seeds -= 1
                if not seeds:
                    mdata.capt_loc = WinCond.REPEAT_TURN
                    return mdata

            self.game.board[loc] += 1
            seeds -= 1

        mdata.capt_loc = loc
        return mdata



class DivertSkipBlckdSower(SowMethodIf):
    """Divert blocked holes on opp side to store 0 (out of play).
    Skipped blocked holes on own side.

    Don't use the incrementer because it will skip blocks.

    The option to select this is:  sow_blkd_div"""

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
                        return mdata

                loc = (loc + mdata.direct) % self.game.cts.dbl_holes

            self.game.board[loc] += 1
            seeds -= 1

        mdata.capt_loc = loc
        return mdata


class SowClosed(SowMethodIf):
    """For non-multilap sowing, check for closing, remove the
    final seeds from play and block the hole.

    This included with sow_blkd_div without mlaps"""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        mdata = self.decorator.sow_seeds(mdata)
        loc = mdata.capt_loc

        if (self.game.board[loc] == self.game.info.gparam_one
                and self.game.cts.opp_side(self.game.turn, loc)):

            self.game.store[0] += self.game.board[loc]
            self.game.board[loc] = 0
            self.game.blocked[loc] = True
        return mdata


class SowCaptOwned(SowMethodIf):
    """Any holes sown to allow capture are captured by the hole's
    owner, except for the last seed. The last hole may be captured
    from the opponent's hole (let the capturer do that--keeps the
    log nice)."""

    def __init__(self, game, owner_func, decorator=None):
        super().__init__(game, decorator)
        self.owner = owner_func

    def sow_seeds(self, mdata):
        """Sow seeds."""

        loc = mdata.cont_sow_loc
        for scnt in range(mdata.seeds, 0, -1):

            loc = self.game.deco.incr.incr(loc,
                                           mdata.direct,
                                           mdata.cont_sow_loc)
            self.game.board[loc] += 1

            if scnt > 1 and self.game.deco.capt_ok.capture_ok(loc):
                owner = self.owner(loc)
                game_log.step(f'Catpure from {loc} by {owner}')
                self.game.store[owner] += self.game.board[loc]
                self.game.board[loc] = 0

        mdata.capt_loc = loc
        return mdata



# %%  lap continue testers

class LapContinuerIf(abc.ABC):
    """Interface for algorithm that determines if
    sowing should continue."""

    def __init__(self, game):
        self.game = game

    def do_another_lap(self, mdata):
        """Return True if we should continue sowing, False otherwise."""


class SimpleLapCont(LapContinuerIf):
    """Stop if we end a sow in a store, otherwise if have
    more than one seed return to CONTINUE sowing."""

    def do_another_lap(self, mdata):
        """Determine if we are done sowing."""

        if mdata.capt_loc is WinCond.REPEAT_TURN:
            return False

        return self.game.board[mdata.capt_loc] > 1


class NextLapCont(LapContinuerIf):
    """Continue sowing based on seeds being in the next
    hole. If there are any, continue from there.

    Laurence Russ calls this Indian Style lapping."""

    def do_another_lap(self, mdata):
        """Determine if we are done sowing."""

        if mdata.capt_loc is WinCond.REPEAT_TURN:
            return False

        loc = self.game.deco.incr.incr(mdata.capt_loc,
                                       mdata.direct,
                                       NOSKIPSTART)
        if self.game.board[loc]:
            mdata.capt_loc = loc
            return True
        return False

# XXXX could a deco chain be used to implement LAPPER_NEXT with CHILD & GS


class DivertBlckdLapper(LapContinuerIf):
    """Continue sowing if end in hole with > 1 seeds, but
    stop if we ended on a blocked hole (will be opp side,
    i.e. last seed was taken out of play)."""

    def do_another_lap(self, mdata):
        """Determine if we are done sowing."""

        loc = mdata.capt_loc
        return not self.game.blocked[loc] and self.game.board[loc] > 1


class ChildLapCont(LapContinuerIf):
    """Multilap sow in the presence/creation of children:
        1. Stop sowing if we end in a store or a child.
        2. Stop sowing if we should make a child.
        3. BUT don't make child in opponents first hole with
           a single seed from our right-most hole.

        4. Continue sowing if end in hole with > 1 seeds that
           is not a designated child.

    Mohr's book states that a turn ends when 'any' seed is sown
    into a child, but it doesn't describe what to do with the
    remaining seeds; therefore this condition is not
    implemented here. (rules for Bao). Russ's book confirms this
    p 44, first paragraph, but he also doesn't describe what to do
    with the remaining seeds."""

    def do_another_lap(self, mdata):
        """Determine if we are done sowing."""

        loc = mdata.capt_loc
        if loc is WinCond.REPEAT_TURN or self.game.child[loc] is not None:
            return False

        if (mdata.seeds > 1
                and self.game.board[loc] == self.game.info.child_cvt):
            if ((self.game.info.oppsidecapt
                    and self.game.cts.opp_side(self.game.turn, loc))
                    or not self.game.info.oppsidecapt):

                return False

        return self.game.board[loc] > 1 and self.game.child[loc] is None


# %%  mlap sowers


class MlapSowerIf(SowMethodIf):
    """An interface and init for mlap sowers."""

    def __init__(self, game, decorator, lap_cont):

        super().__init__(game, decorator)
        self.lap_cont = lap_cont


    def get_single_sower(self):
        """Return the first non-lap sower in the deco chain."""
        return self.decorator.get_single_sower()


class SowMlapSeeds(MlapSowerIf):
    """Do sow operations until until lap continuer test tells
    us to stop.

    The extended deco chain sows from each starting hole.
    Here we only decide if we should continue with sowing from
    the ending hole."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        loc = mdata.cont_sow_loc
        for _ in range(MAX_LAPS):

            game_log.add(f'    Sowing from {loc}.', game_log.DETAIL)
            mdata = self.decorator.sow_seeds(mdata)

            if self.lap_cont.do_another_lap(mdata):
                loc = mdata.capt_loc
                mdata.cont_sow_loc = loc
                mdata.seeds = self.game.board[loc]
                self.game.board[loc] = 0

            else:
                return mdata

        mdata.capt_loc = WinCond.ENDLESS
        return mdata


class DivertBlckdLapSower(MlapSowerIf):
    """Do sow operations until until lap continuer test tells
    us to stop, closing holes along the way.

    XXXX This is incredibly similar to SowMlapSeeds with an
    extra operation before sowing another lap. Consider combining
    in future, if there are other mlap sowers that behave the
    same way."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        loc = mdata.cont_sow_loc
        for _ in range(2 * MAX_LAPS):

            game_log.add(f'    Sowing from {loc}.', game_log.DETAIL)
            mdata = self.decorator.sow_seeds(mdata)

            if self.lap_cont.do_another_lap(mdata):
                loc = mdata.capt_loc
                mdata.cont_sow_loc = loc
                mdata.seeds = self.game.board[loc]

                if (self.game.board[loc] == self.game.info.gparam_one
                        and self.game.cts.opp_side(self.game.turn, loc)):
                    self.game.blocked[loc] = True
                self.game.board[loc] = 0

            else:
                return mdata

        # searches have not found a way to exercise this code
        game_log.add('MLAP game ENDLESS', game_log.IMPORT)  # pragma: no cover
        mdata.capt_loc = WinCond.ENDLESS                    # pragma: no cover
        return mdata                                        # pragma: no cover


class SowVisitedMlap(SowMethodIf):
    """Enforce an mlap option in which the first sow, must reach or
    pass through the opponents side of the board before a second
    lap may begin. A sow that does not reach the opponents side of
    the board, ends the turn. In otherwords, a second lap may not
    be started on a players side of the board, unless they have
    passed through the opponents side of the board.

    Can check the child array even if the child flag not set, because
    it is initialized to None (not a designated child)."""

    def __init__(self, game, single_sower, lap_sower, lap_cont):

        super().__init__(game, lap_sower)
        self.lap_cont = lap_cont
        self.single_sower = single_sower


    def get_single_sower(self):
        """Return the first non-lap sower in the deco chain.
        This is not a single sower, override the default to call
        down the deco chain"""
        return self.decorator.get_single_sower()


    def sow_seeds(self, mdata):
        """Do the first sow."""

        game_log.add(f'    Sowing from {mdata.cont_sow_loc}.', game_log.DETAIL)

        mdata = self.single_sower.sow_seeds(mdata)
        if mdata.capt_loc is WinCond.REPEAT_TURN:
            return mdata

        visited_opp = (mdata.seeds >= self.game.cts.holes or
                       self.game.cts.opp_side(self.game.turn, mdata.capt_loc))
        if not visited_opp:
            return mdata

        if self.lap_cont.do_another_lap(mdata):
            loc = mdata.capt_loc
            mdata.cont_sow_loc = loc
            mdata.seeds = self.game.board[loc]
            self.game.board[loc] = 0
            return self.decorator.sow_seeds(mdata)

        return mdata


# %% prescribed opening moves

# only use prescribe openings if the first player has a choice
# if it's a standard pattern use start_pattern

# Usage will be like this:

# parent = SowMethodHolder(game, None)
# parent.decorator = SowDoAlternates(game, 1, parent, sower)
# sower = parent


class SowMethodHolder(SowMethodIf):
    """A deco delegates sow_seeds, but gives us a place and
    means to delete a decorator out of the deco chain."""

    def sow_seeds(self, mdata):
        return self.decorator.sow_seeds(mdata)

    def delete_deco(self):
        """Delete the child decorator; it will have a child decorator."""
        self.decorator = self.decorator.decorator


class SowPrescribedIf(SowMethodIf):
    """A deco that becomes obsolete after a one or more turns.
    It has it's parent remove itself the deco chain,
    the parent must be a SowMethodHolder.

    Concrete subclasses should not provide sow_seeds."""

    def __init__(self, game, count, parent, decorator=None):

        super().__init__(game, decorator)
        self.dispose = count
        self.parent = parent

    @abc.abstractmethod
    def do_prescribed(self, mdata):
        """Do the prescribed opening moves."""

    def sow_seeds(self, mdata):
        """If the decorator has expired, tell the parent to
        remove this deco from the chain and this will be the
        last call to decorator."""

        mdata = self.do_prescribed(mdata)

        if self.game.mcount >= self.dispose:
            self.parent.delete_deco()

        return mdata


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
        return mdata


class SowTriples(SowPrescribedIf):
    """from the selected hole sow:
        1, 3, (0, 3, 3)+
        """
    # TODO how to adjust for other than 2 start seeds

    def do_prescribed(self, mdata):

        loc = mdata.cont_sow_loc
        incrementer = self.game.deco.incr.incr

        self.game.board[loc] = 1
        loc = incrementer(loc, mdata.direct, mdata.cont_sow_loc)
        self.game.board[loc] = 3

        for cnt in range(self.game.cts.dbl_holes - 2):

            loc = incrementer(loc, mdata.direct, mdata.cont_sow_loc)
            self.game.board[loc] = 3 if cnt % 3 else 0

        mdata.capt_loc = loc
        return mdata


class SowPlus1Minus1Capt(SowPrescribedIf):
    """Starting after the selected move one seed forward
    in every other hole.
    Capture the seeds across from the start hole.

    Requires stores, prohibit move unlock (or just ignore it?)"""

    def do_prescribed(self, mdata):

        loc = mdata.cont_sow_loc
        incrementer = self.game.deco.incr.incr

        for cnt in range(self.game.cts.dbl_holes - 1):
            loc = incrementer(loc, mdata.direct, mdata.cont_sow_loc)
            self.game.board[loc] += 1 if cnt % 2 else -1

        # TODO need to assure same number of seeds

        cross = self.game.cts.cross_from_loc(mdata.capt_loc)
        self.game.store[self.game.turn] += self.game.board[cross]
        self.game.board[cross] = 0

        mdata.capt_loc = loc
        return mdata


# %% build deco chain


def deco_blkd_divert_sower(game):
    """Implement the sow_blkd_div sower.
    When sowing seeds, blocked holes on own side of the board are
    skipped and seeds for blocked opponent holes are diverted out
    of play (actually store 0).

    XXXX  visit_opp is not currently supported because we need to
    close the hole if we end on gparam_one seeds (ie. block it).
    This needs to occur if lapping or not.
    This doesn't quite fit the model of the code right now but might
    in the future."""

    sower = DivertSkipBlckdSower(game)

    if game.info.mlaps == LapSower.LAPPER:
        sower = DivertBlckdLapSower(game, sower, DivertBlckdLapper(game))

    else:
        sower = SowClosed(game, sower)

    return sower


def deco_base_sower(game):
    """Choose the base sower."""

    if game.info.sow_blkd_div:
        return deco_blkd_divert_sower(game)

    if game.info.sow_capt_all:
        if game.info.goal == Goal.TERRITORY:
            sower = SowCaptOwned(game, lambda loc: game.owner[loc])
        else:
            sower = SowCaptOwned(game, game.cts.board_side)

    elif game.info.sow_own_store:
        sower = SowSeedsNStore(game)

    else:
        sower = SowSeeds(game)

    return sower


def deco_mlap_sower(game, sower):
    """Build the deco chain elements for multiple lap sowing."""

    pre_lap_sower = sower

    if game.info.child_cvt:
        lap_cont = ChildLapCont(game)
    elif game.info.mlaps == LapSower.LAPPER:
        lap_cont = SimpleLapCont(game)
    else:   # game.info.mlaps == LapSower.LAPPER_NEXT:
        lap_cont = NextLapCont(game)

    sower = SowMlapSeeds(game, sower, lap_cont)

    if game.info.visit_opp:
        sower = SowVisitedMlap(game, pre_lap_sower, sower, lap_cont)

    return sower


def deco_prescribed_sower(game, sower):
    """Add two deco's to the chain, a stub class that will allow
    the class derived from SowPrescribedIf to be deleted when we
    are done with it."""

    parent = SowMethodHolder(game, None)

    if game.info.prescribed == SowPrescribed.SOW1OPP:
        parent.decorator = SowOneOpp(game, 1, parent, sower)

    elif game.info.prescribed == SowPrescribed.TRIPLES:
        parent.decorator = SowTriples(game, 1, parent, sower)

    elif game.info.prescribed == SowPrescribed.PLUS1MINUS1:
        parent.decorator = SowPlus1Minus1Capt(game, 1, parent, sower)

    return parent


def deco_sower(game):
    """Build the sower chain."""

    sower = deco_base_sower(game)

    if game.info.mlaps != LapSower.OFF:
        sower = deco_mlap_sower(game, sower)

    if game.info.prescribed != SowPrescribed.NONE:
        sower = deco_prescribed_sower(game, sower)

    return sower
