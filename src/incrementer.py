# -*- coding: utf-8 -*-
"""Incrementer to support sowing and capturing. Given
start location and concrete direction (CW or CCW)
determine the next hole to sow or attempt capture from.

The chained decorator is called first in each decorator
(pre-call), allowing each decorator to increment futher
if the next hole is not to be played (e.g. blocked,
start).


Refactor consideration: If more decorators are added:
    1. have the first increment use child deco
    2. have the extra increments restart at the top of the chain,
       new init parameters:  child - decorator below; top - first decorator

Created on Fri Apr  7 11:21:07 2023
@author: Ann"""


# %% imports

import abc

import deco_chain_if
import game_info as gi


# %% constants

# disable the skip start when incrementing, loc can never be -1
NOSKIPSTART = -1


# %%  incrementer interface

class IncrementerIf(deco_chain_if.DecoChainIf):
    """Interface for incrementer."""

    @abc.abstractmethod
    def incr(self, loc, direct, start=NOSKIPSTART):
        """Do one increment.
        RETURN new loc"""


# %% base class

class Increment(IncrementerIf):
    """Do increment with mod for board size."""

    def incr(self, loc, direct, _=NOSKIPSTART):
        """Do an increment."""

        return (loc + direct) % self.game.cts.dbl_holes


class MapIncrement(IncrementerIf):
    """An incrementer based on mapping.

    The attributes ccw_map and cw_map should be changed
    to make this useful."""


    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        dholes = game.cts.dbl_holes
        self.ccw_map = [(loc + 2) % dholes for loc in range(dholes)]
        self.cw_map = [(loc - 2) % dholes for loc in range(dholes)]


    def __str__(self):
        return self.str_deco_detail('cw:  ' + str(self.cw_map)
                                    + '\n   ccw:  ' + str(self.ccw_map))


    def incr(self, loc, direct, _=NOSKIPSTART):
        """Do an increment."""

        if direct == gi.Direct.CCW:
            return self.ccw_map[loc]

        return self.cw_map[loc]


# %% decorators

class IncPastStart(IncrementerIf):
    """Do an increment past the start hole."""

    def incr(self, loc, direct, start=NOSKIPSTART):
        """Increment with skip_start."""

        loc = self.decorator.incr(loc, direct, start)

        if loc == start:
            return self.decorator.incr(loc, direct, start)

        return loc


class IncPastBlocks(IncrementerIf):
    """Increment past blocked cells."""

    def incr(self, loc, direct, start=NOSKIPSTART):
        """Incerement past blocked holes"""

        loc = self.decorator.incr(loc, direct, start)

        while self.game.blocked[loc]:
            loc = self.decorator.incr(loc, direct, start)

        return loc


# %%

def deco_incrementer(game):
    """Create decorator chain for incementer."""

    incer = Increment(game)

    if game.info.skip_start:
        incer = IncPastStart(game, incer)

    if game.info.blocks:
        incer = IncPastBlocks(game, incer)

    return incer
