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
    def incr(self, loc, direct, turn, start=NOSKIPSTART):
        """Do one increment.
        RETURN new loc"""


# %% base class

class Increment(IncrementerIf):
    """Do increment with mod for board size."""

    def incr(self, loc, direct, turn, _=NOSKIPSTART):
        """Do an increment."""

        return (loc + direct) % self.game.cts.dbl_holes


class MapIncrement(IncrementerIf):
    """An incrementer based on mapping.

    The attributes ccw_map and cw_map should be changed
    to make this useful.

    Stores are not included and there must only be one
    cycle that reaches all holes."""


    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        dholes = game.cts.dbl_holes
        self.ccw_map = [(loc + 2) % dholes for loc in range(dholes)]
        self.cw_map = [(loc - 2) % dholes for loc in range(dholes)]


    def __str__(self):
        return self.str_deco_detail('cw:  ' + str(self.cw_map)
                                    + '\n   ccw:  ' + str(self.ccw_map))


    def build_maps_from_cycle(self, cycle):
        """Build the maps from a cycle.

        Provide a CCW cycle which starts anywhere but has the
        indecies in the order they should be sown."""

        dbl_holes = self.game.cts.dbl_holes
        assert set(cycle) == set(range(dbl_holes)), "Bad cycle provided."

        self.ccw_map = [cycle[(cycle.index(idx) + 1) % dbl_holes]
                         for idx in range(dbl_holes)]

        self.cw_map =  [cycle[(cycle.index(idx) - 1) % dbl_holes]
                         for idx in range(dbl_holes)]


    def incr(self, loc, direct, turn, _=NOSKIPSTART):
        """Do an increment."""

        if direct == gi.Direct.CCW:
            return self.ccw_map[loc]

        return self.cw_map[loc]



class MapStoresIncr(IncrementerIf):
    """An incrementer based on mapping that includes one
    or both stores. There may be seperate cycles for each
    player and each cycle might not include all locations.

    The map is in the order:
        t_store  f_store board-indecies

    corresponding to the indecies:
        -2       -1      0 1 2 ..."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)
        self.map = None

    def __str__(self):

        return self.str_deco_detail(
            'cw true:   ' + str(self.map[True][gi.Direct.CW])
            + '\n   cw false:  ' + str(self.map[False][gi.Direct.CW])
            + '\n   ccw true:  ' + str(self.map[True][gi.Direct.CCW])
            + '\n   ccw false: ' + str(self.map[False][gi.Direct.CCW]))


    @staticmethod
    def next_hole(cur_hole, cycle, cycle_len, step):
        """Return the hole that cur_hole would sow to
        given the cycle, step direction, and cycle size."""

        try:
            h_idx = cycle.index(cur_hole)
        except ValueError:
            return None

        return cycle[(h_idx + step) % cycle_len]


    def build_one_map(self, cycle, step):
        """Build a map such that map[current] is the next
        location to sow.

        Do this by looking up where each index is in the cycle,
        then using the next value in step order as the destination."""

        dbl_holes = self.game.cts.dbl_holes
        cycle_len = len(cycle)

        return [self.next_hole(idx, cycle, cycle_len, step)
                for idx in range(-2, dbl_holes)]


    def build_maps_from_cycles(self, f_cycle, t_cycle=None):
        """Build the maps from a cycle."""


        self.map = {}

        self.map[False] = {gi.Direct.CCW: self.build_one_map(f_cycle, 1),
                           gi.Direct.CW: self.build_one_map(f_cycle, -1)}

        if t_cycle:
            self.map[True] = {gi.Direct.CCW: self.build_one_map(t_cycle, 1),
                               gi.Direct.CW: self.build_one_map(t_cycle, -1)}
        else:
            self.map[True] = self.map[False]



    def incr(self, loc, direct, turn, _=NOSKIPSTART):
        """Do an increment."""

        return self.map[turn][direct][loc + 2]


class IncOwnStores(MapStoresIncr):
    """Increment that cycles through the board and store of
    the current player. The store is put where it would be
    when passing it."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        holes = game.cts.holes
        dholes = game.cts.dbl_holes

        f_cycle = list(range(holes)) + [gi.F_STORE] + list(range(holes, dholes))
        t_cycle = list(range(dholes)) + [gi.T_STORE]

        self.build_maps_from_cycles(f_cycle, t_cycle)


class IncBothStores(MapStoresIncr):
    """Increment that cycles through the board and both stores.
    The store is put where they would be when passing them."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)

        holes = game.cts.holes
        dholes = game.cts.dbl_holes

        self.build_maps_from_cycles(list(range(holes))
                                   + [gi.F_STORE]
                                   + list(range(holes, dholes))
                                   + [gi.T_STORE])


# %% decorators

class IncPastStart(IncrementerIf):
    """Do an increment past the start hole."""

    def incr(self, loc, direct, turn, start=NOSKIPSTART):
        """Increment with skip_start."""

        loc = self.decorator.incr(loc, direct, turn, start)

        if loc == start:
            return self.decorator.incr(loc, direct, turn, start)

        return loc


class IncPastBlocks(IncrementerIf):
    """Increment past blocked cells."""

    def incr(self, loc, direct, turn, start=NOSKIPSTART):
        """Incerement past blocked holes"""

        loc = self.decorator.incr(loc, direct, turn, start)
        while self.game.blocked[loc]:
            loc = self.decorator.incr(loc, direct, turn, start)

        return loc


# %%

def deco_incrementer(game):
    """Create decorator chain for incementer."""

    if game.info.sow_stores.sow_both():
        incer = IncBothStores(game)

    elif game.info.sow_stores:
        incer = IncOwnStores(game)

    else:
        incer = Increment(game)

    if game.info.skip_start:
        incer = IncPastStart(game, incer)

    if game.info.blocks:
        incer = IncPastBlocks(game, incer)

    return incer
