# -*- coding: utf-8 -*-
"""Incrementer to support sowing and capturing. Given
start location and concrete direction (CW or CCW)
determine the next hole to sow or attempt capture from.

Sowing always implements the skip_start flag by
incrementing past 'start', but capturing needs to not
skip the start (i.e. the capture should end when we find
an empty hole that was skipped in sowing).  The
NOSKIPSTART token can be provided for 'start' to support
this.

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


# %% constants

# the capturer needs to disable the skip start when incrementing
NOSKIPSTART = -1


# %%  incrementer interface

class IncrementerIf(abc.ABC):
    """Interface for incrementer."""

    def __init__(self, game, decorator=None):
        self.game = game
        self.decorator = decorator

    @abc.abstractmethod
    def incr(self, loc, direct, start):
        """Do one increment.
        RETURN new loc"""


# %% base class

class Increment(IncrementerIf):
    """Do increment with mod for board size."""

    def incr(self, loc, direct, _):
        """Do an increment."""

        return (loc + direct) % self.game.cts.dbl_holes


# %% decorators

class IncPastStart(IncrementerIf):
    """Do an increment past the start hole."""

    def incr(self, loc, direct, start):
        """Increment with skip_start."""

        loc = self.decorator.incr(loc, direct, start)

        if loc == start:
            return self.decorator.incr(loc, direct, start)

        return loc


class IncPastBlocks(IncrementerIf):
    """Increment past blocked cells."""

    def incr(self, loc, direct, start):
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
