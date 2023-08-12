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


# %%  base sower

class SowStart(SowStartIf):
    """start the sower"""

    def start_sow(self, loc):
        """start sow in next hole"""

        seeds = self.game.board[loc]
        self.game.board[loc] = 0

        return loc, seeds


# %% decorators


class SowStartHole(SowStartIf):
    """Leave one seed in the start hole."""

    def start_sow(self, loc):
        """Start sow in start hole, don't call further."""

        seeds = self.game.board[loc] - 1
        self.game.board[loc] = 1

        return loc, seeds


class SowMarkUnlock(SowStartIf):
    """Start the sower. If locks are used then unlock the hole."""

    def start_sow(self, loc):
        """Unlock the start hole, pass on the request"""

        self.game.unlocked[loc] = True
        return self.decorator.start_sow(loc)


class SowStartTop(SowStartIf):
    """Start the sower. Translate pos to loc, always use this decorator."""

    def start_sow(self, pos):
        """Translate pos to loc. Call the chain.

        Arguement intentionally renamed because this method
        gets pos, but calls chained decorators with loc."""
        # pylint: disable=arguments-renamed

        loc = self.game.cts.pos_to_loc(not self.game.turn, pos)
        return self.decorator.start_sow(loc)


# %% build decorator chain

def deco_sow_starter(game):
    """Build the sow_starter decorator chain"""

    starter = SowStart(game)

    if game.info.flags.sow_start:
        starter = SowStartHole(game, starter)

    if game.info.flags.moveunlock:
        starter = SowMarkUnlock(game, starter)

    starter = SowStartTop(game, starter)

    return starter
