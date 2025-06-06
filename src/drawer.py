# -*- coding: utf-8 -*-
"""Start the sowing by handling the start hole and
determining the number of seeds to sow.
SOW_START is handled here.

Created on Fri Apr  7 22:19:24 2023
@author: Ann"""


# %% imports

import abc

import deco_chain_if

import game_info as gi

# %%  sow interface

class DrawerIf(deco_chain_if.DecoChainIf):
    """Interface for the draw."""

    @abc.abstractmethod
    def draw(self, loc):
        """Start the sowing:
        Convert the pos (index on player side, 0..HOLES) to
        location (board array index, 0..DBL_HOLES),
        determine the number of seeds for sowing, and
        update the start hole seeds.
        RETURN loc, seeds."""


# %%  base sowers

class DrawAll(DrawerIf):
    """Draw all the seeds"""

    def draw(self, loc):
        """Start sow in next hole"""

        seeds = self.game.board[loc]
        self.game.board[loc] = 0

        return loc, seeds


class DrawLeaveOne(DrawerIf):
    """Leave one seed in the start hole."""

    def draw(self, loc):
        """Start sow in start hole, don't call further."""

        seeds = self.game.board[loc] - 1
        self.game.board[loc] = 1

        return loc, seeds


class DrawMoveOne(DrawerIf):
    """Sow the start hole unless there is only one seed."""

    def draw(self, loc):
        """start sow"""

        seeds = self.game.board[loc]
        if seeds == 1:
            self.game.board[loc] = 0
        else:
            seeds -= 1
            self.game.board[loc] = 1

        return loc, seeds


# %% decorators

class MarkUnlock(DrawerIf):
    """If locks are used then unlock the hole."""

    def draw(self, loc):
        """Unlock the start hole, pass on the request"""

        self.game.unlocked[loc] = True
        return self.decorator.draw(loc)


# %%  top level starters
#     convert move to loc for the rest of the chain

class DrawMovePos(DrawerIf):
    """Start the sower. Translate move to loc."""

    def draw(self, pos):
        """Translate move (is pos) to loc. Call the chain.

        Arguement intentionally renamed because this method
        gets pos, but calls chained decorators with loc."""
        # pylint: disable=arguments-renamed

        loc = self.game.cts.xlate_pos_loc(not self.game.turn, pos)
        return self.decorator.draw(loc)


class DrawMovePair(DrawerIf):
    """Start the sower. Translate move to loc."""

    def draw(self, move):
        """Translate move to loc. Udir moves are (pos, direct).
        Call the chain.

        Arguement intentionally renamed because this method
        gets move, but calls chained decorators with loc."""
        # pylint: disable=arguments-renamed

        loc = self.game.cts.xlate_pos_loc(not self.game.turn, move[0])
        return self.decorator.draw(loc)


class DrawMoveTriple(DrawerIf):
    """Start the sower. Translate move to loc."""

    def draw(self, move):
        """Translate move to loc. Triple moves are (row, pos, direct).
        Call the chain.

        Arguement intentionally renamed because this method
        gets move, but calls chained decorators with loc."""
        # pylint: disable=arguments-renamed

        row, pos, _ = move
        loc = self.game.cts.xlate_pos_loc(row, pos)
        return self.decorator.draw(loc)


# %% build decorator chain

def deco_drawer(game):
    """Build the drawer decorator chain"""

    if game.info.sow_start:
        if game.info.move_one:
            drawer = DrawMoveOne(game)
        else:
            drawer = DrawLeaveOne(game)
    else:
        drawer = DrawAll(game)

    if (game.info.moveunlock
            or game.info.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST):
        drawer = MarkUnlock(game, drawer)

    if game.info.mlength == 2:
        drawer = DrawMovePair(game, drawer)
    elif game.info.mlength == 3:
        drawer = DrawMoveTriple(game, drawer)
    else:
        drawer = DrawMovePos(game, drawer)

    return drawer
