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
from game_interface import WinCond
from game_interface import Direct


# %% constants

MAX_LAPS = 50


# %%  sow interface

class SowMethodIf(abc.ABC):
    """Interface for sowing."""

    def __init__(self, game, decorator=None):
        self.game = game
        self.decorator = decorator

    @abc.abstractmethod
    def sow_seeds(self, start, direct, seeds):
        """Sow seeds
        RETURN last loc seeded."""


# %%  base sower

class SowSeeds(SowMethodIf):
    """Basic sower.  Handles direction, skip_start and blocks
    (via the incr)."""

    def sow_seeds(self, start, direct, seeds):
        """Sow seeds."""

        loc = start
        for _ in range(seeds):

            loc = self.game.deco.incr.incr(loc, direct, start)
            self.game.board[loc] += 1

        return loc


# %%

class SowSeedsNStore(SowMethodIf):
    """Sow a seed into the player's own store when passing it.

    If the sow ends in the store, return WinCond.END_STORE.
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

        if game.info.flags.sow_direct == Direct.CW:
            self.poses = (self.game.cts.holes - 1,
                          self.game.cts.dbl_holes - 1)
        elif game.info.flags.sow_direct == Direct.CCW:
            self.poses = (0, self.game.cts.holes)
        else:
            self.poses = (0, self.game.cts.holes - 1,
                          self.game.cts.holes, self.game.cts.dbl_holes - 1)


    def sow_seeds(self, start, direct, seeds):
        """Sow seeds.
        Copy some deep values into locals a bit of speed."""

        turn = self.game.turn
        incr = self.game.deco.incr.incr
        store = self.game.store
        board = self.game.board
        loc = start

        while seeds > 0:

            loc = incr(loc, direct, start)

            if (loc in self.poses
                    and loc == self.fill_store[direct + 1][turn]):

                store[turn] += 1
                seeds -= 1
                if not seeds:
                    return WinCond.END_STORE

            board[loc] += 1
            seeds -= 1

        return loc


# %%  lap continue testers

class LapContinuerIf(abc.ABC):
    """Interface for algorithm that determines if
    sowing should continue."""

    def __init__(self, game):
        self.game = game

    def do_another_lap(self, loc, seeds):
        """Return True if we should continue sowing, False otherwise."""


class SimpleLapCont(LapContinuerIf):
    """Stop if we end a sow in a store, otherwise if have
    more than one seed return to CONTINUE sowing."""

    def do_another_lap(self, loc, _):
        """Determine if we are done sowing."""

        if loc is WinCond.END_STORE:
            return False

        return self.game.board[loc] > 1



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

    def do_another_lap(self, loc, seeds):
        """Determine if we are done sowing."""

        if loc is WinCond.END_STORE or self.game.child[loc] is not None:
            return False

        if (seeds > 1
                and self.game.board[loc] == self.game.info.flags.convert_cnt):
            if ((self.game.info.flags.oppsidecapt
                    and self.game.cts.opp_side(self.game.turn, loc))
                    or not self.game.info.flags.oppsidecapt):

                return False

        if self.game.board[loc] > 1 and self.game.child[loc] is None:
            return True

        return False


# %%  mlap sowers


class SowMlapSeeds(SowMethodIf):
    """Do sow operations until until lap continuer test tells
    us to stop.

    The extended deco chain sows from each starting hole.
    Here we only decide if we should continue with sowing from
    the ending hole."""

    def __init__(self, game, decorator, lap_cont):

        super().__init__(game, decorator)
        self.lap_cont = lap_cont

    def sow_seeds(self, start, direct, seeds):
        """Sow seeds."""

        loc = start
        for _ in range(MAX_LAPS):

            game_log.add(f'    Sowing from {loc}.', game_log.DETAIL)
            loc = self.decorator.sow_seeds(loc, direct, seeds)

            if self.lap_cont.do_another_lap(loc, seeds):
                seeds = self.game.board[loc]
                self.game.board[loc] = 0

            else:
                return loc

        return WinCond.ENDLESS


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

    def sow_seeds(self, start, direct, seeds):
        """Do the first sow."""

        game_log.add(f'    Sowing from {start}.', game_log.DETAIL)
        loc = self.single_sower.sow_seeds(start, direct, seeds)
        if loc is WinCond.END_STORE:
            return loc

        visited_opp = (seeds >= self.game.cts.holes or
                       self.game.cts.opp_side(self.game.turn, loc))
        if not visited_opp:
            return loc

        if self.lap_cont.do_another_lap(loc, seeds):
            seeds = self.game.board[loc]
            self.game.board[loc] = 0
            return self.decorator.sow_seeds(loc, direct, seeds)

        return loc


# %%

def deco_sower(game):
    """Build the sower chain."""

    if game.info.flags.sow_own_store:
        sower = SowSeedsNStore(game)
    else:
        sower = SowSeeds(game)

    pre_lap_sower = sower

    if game.info.flags.mlaps:

        if game.info.flags.child:
            lap_cont = ChildLapCont(game)
        else:
            lap_cont = SimpleLapCont(game)

        sower = SowMlapSeeds(game, sower, lap_cont)

        if game.info.flags.visit_opp:
            sower = SowVisitedMlap(game, pre_lap_sower, sower, lap_cont)

    return sower


def deco_replace_base_sower(game, base_sower):
    """Replace the base sower with a new one."""

    if game.info.flags.mlaps:

        if game.info.flags.visit_opp:
            game.deco.sower.single_sower = base_sower
            game.deco.sower.decorator.decorator = base_sower

        else:
            game.deco.sower.decorator = base_sower

    else:
        game.deco.sower = base_sower
