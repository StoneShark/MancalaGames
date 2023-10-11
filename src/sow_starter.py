# -*- coding: utf-8 -*-
"""Start the sowing by handling the start hole and
determining the number of seeds.

Created on Fri Apr  7 22:19:24 2023
@author: Ann"""


# %% imports

import abc


# %%  sow interface


class SowStartIf(abc.ABC):
    """Interface for sowing."""

    def __init__(self, game, decorator=None):
        self.game = game
        self.decorator = decorator

    @abc.abstractmethod
    def start_sow(self, loc):
        """Start the sowing:
        Convert the pos (index on player side, 0..HOLES) to
        location (board array index, 0..DBL_HOLES),
        determine the number of seeds for sowing, and
        update the start hole seeds.
        RETURN loc, seeds."""


# %%  base sowers

class SowStart(SowStartIf):
    """start the sower"""

    def start_sow(self, loc):
        """start sow in next hole"""

        seeds = self.game.board[loc]
        self.game.board[loc] = 0

        return loc, seeds


class SowStartHole(SowStartIf):
    """Leave one seed in the start hole."""

    def start_sow(self, loc):
        """Start sow in start hole, don't call further."""

        seeds = self.game.board[loc] - 1
        self.game.board[loc] = 1

        return loc, seeds


class SowStartMoveOne(SowStartIf):
    """Sow the start hole unless there is only one seed."""

    def start_sow(self, loc):
        """start sow"""

        seeds = self.game.board[loc]
        if seeds == 1:
            self.game.board[loc] = 0
        else:
            seeds -= 1
            self.game.board[loc] = 1

        return loc, seeds



# %% decorators


class SowMarkUnlock(SowStartIf):
    """Start the sower. If locks are used then unlock the hole."""

    def start_sow(self, loc):
        """Unlock the start hole, pass on the request"""

        self.game.unlocked[loc] = True
        return self.decorator.start_sow(loc)


# %%  top level starters
#     convert move to pos for the rest of the chain

class SowStartPos(SowStartIf):
    """Start the sower. Translate move to loc."""

    def start_sow(self, pos):
        """Translate move (is pos) to loc. Call the chain.

        Arguement intentionally renamed because this method
        gets pos, but calls chained decorators with loc."""
        # pylint: disable=arguments-renamed

        loc = self.game.cts.xlate_pos_loc(not self.game.turn, pos)
        return self.decorator.start_sow(loc)


class SowStartUdir(SowStartIf):
    """Start the sower. Translate move to loc."""

    def start_sow(self, move):
        """Translate move to loc. Udir moves are (pos, direct).
        Call the chain.

        Arguement intentionally renamed because this method
        gets move, but calls chained decorators with loc."""
        # pylint: disable=arguments-renamed

        loc = self.game.cts.xlate_pos_loc(not self.game.turn, move[0])
        return self.decorator.start_sow(loc)


class SowStartNoSides(SowStartIf):
    """Start the sower. Translate move to loc."""

    def start_sow(self, move):
        """Translate move to loc. NoSides moves are (row, pos, direct).
        Call the chain.

        Arguement intentionally renamed because this method
        gets move, but calls chained decorators with loc."""
        # pylint: disable=arguments-renamed

        row, pos, _ = move
        loc = self.game.cts.xlate_pos_loc(row, pos)
        return self.decorator.start_sow(loc)


# %% build decorator chain

def deco_sow_starter(game):
    """Build the sow_starter decorator chain"""

    if game.info.sow_start:
        if game.info.move_one:
            starter = SowStartMoveOne(game)
        else:
            starter = SowStartHole(game)
    else:
        starter = SowStart(game)

    if game.info.moveunlock:
        starter = SowMarkUnlock(game, starter)

    if game.info.udirect and not game.info.no_sides:
        starter = SowStartUdir(game, starter)
    elif game.info.no_sides:
        starter = SowStartNoSides(game, starter)
    else:
        starter = SowStartPos(game, starter)

    return starter
