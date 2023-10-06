# -*- coding: utf-8 -*-
"""Get moves for the current player.
This is used for the ai player.

Created on Mon Apr 10 10:08:40 2023
@author: Ann"""


# %% imports

import abc

from game_interface import Direct
from game_interface import PASS_TOKEN
from game_interface import MoveTpl


# %%  mover  interface

class MovesIf(abc.ABC):
    """get_moves interface."""

    def __init__(self, game, decorator=None):
        self.game = game
        self.decorator = decorator

    @abc.abstractmethod
    def get_moves(self):
        """RETURN  list of possible moves."""


# %% base classes

class Moves(MovesIf):
    """Base mover."""

    def get_moves(self):
        """If move is allowable, collect positions."""
        return [pos for pos, ok_move in
                enumerate(self.game.get_allowable_holes()) if ok_move]


class UdirMoves(MovesIf):
    """Base udirect holes mover.
    When udirect is true, moves must be (pos, direct)."""

    def get_moves(self):
        """If move is allowable, collect positions."""

        allowable = self.game.get_allowable_holes()
        moves = []
        for pos in range(self.game.cts.holes):

            if allowable[pos]:
                loc = self.game.cts.xlate_pos_loc(not self.game.turn, pos)
                cnt = self.game.cts.loc_to_left_cnt(loc)
                if cnt in self.game.info.udir_holes:
                    moves += [MoveTpl(pos, Direct.CCW),
                              MoveTpl(pos, Direct.CW)]
                else:
                    moves += [MoveTpl(pos, None)]

        return moves


# %% decorators


class UdirPassMoves(MovesIf):
    """Get moves when udirect and mustpass are set."""

    def get_moves(self):
        """Used when game is both UDIRECT and PASS:
        If no one can move, return an empty list.
        Collect possible moves,
        expand bi-directional holes so that there is one move per direction,
        if there are any moves, return them.
        otherwise pass."""

        moves = self.decorator.get_moves()
        return moves if moves else [MoveTpl(PASS_TOKEN, None)]


class PassMoves(MovesIf):
    """Get moves when only mustpass is set."""

    def get_moves(self):
        """Used if PASS required in game:
        If no one can move, return an empty list.
        Collect possible moves, if there are any moves, return them.
        otherwise pass."""

        moves = self.decorator.get_moves()
        return moves if moves else [PASS_TOKEN]


# %% build deco chain

def deco_moves(game):
    """Build the get_moves deco."""

    if game.info.udirect:

        moves = UdirMoves(game)
        if game.info.mustpass:
            moves = UdirPassMoves(game, moves)

    else:

        moves = Moves(game)
        if game.info.mustpass:
            moves = PassMoves(game, moves)

    return moves
