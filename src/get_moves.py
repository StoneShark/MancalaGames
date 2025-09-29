# -*- coding: utf-8 -*-
"""Get moves for the current player.
This is used for the ai player.

Created on Mon Apr 10 10:08:40 2023
@author: Ann"""


# %% imports

import abc

import deco_chain_if
import game_info as gi


# %%  mover  interface

class MovesIf(deco_chain_if.DecoChainIf):
    """get_moves interface."""

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
                    moves += [gi.MoveTpl(pos, gi.Direct.CCW),
                              gi.MoveTpl(pos, gi.Direct.CW)]
                else:
                    moves += [gi.MoveTpl(pos, None)]

        return moves


class MovesTriples(MovesIf):
    """Base moves for triples, moves must be (row, pos, direct).
    Allowables is dbl_holes long."""

    def get_moves(self):
        """If move is allowable, collect positions."""

        moves = []
        for loc, allow in enumerate(self.game.get_allowable_holes()):

            if allow:
                row = int(loc < self.game.cts.holes)
                pos = self.game.cts.xlate_pos_loc(row, loc)
                moves += [gi.MoveTpl(row, pos, None)]

        return moves


class MovesUdirTriples(MovesIf):
    """Udir moves for triples, moves must be (row, pos, direct)
    no matter if hole is udir or not.
    There are no passes in no_sides games,
    because if there isn't a move then the game is over."""

    def get_moves(self):
        """If move is allowable, collect positions."""

        moves = []
        for loc, allow in enumerate(self.game.get_allowable_holes()):

            if allow:
                row = int(loc < self.game.cts.holes)
                pos = self.game.cts.xlate_pos_loc(row, loc)
                cnt = self.game.cts.loc_to_left_cnt(loc)
                if cnt in self.game.info.udir_holes:
                    moves += [gi.MoveTpl(row, pos, gi.Direct.CCW),
                              gi.MoveTpl(row, pos, gi.Direct.CW)]
                else:
                    moves += [gi.MoveTpl(row, pos, None)]

        return moves


# %% decorators

class PassMoves(MovesIf):
    """Get moves when only mustpass is set."""

    def get_moves(self):
        """If no moves, return PASS_TOKEN."""

        moves = self.decorator.get_moves()
        return moves if moves else [gi.PASS_TOKEN]


class AltDirMoves(MovesIf):
    """For PLAYALTDIR: first player selects the direction then,
    directions alternate by player. Allow direction to be specified
    for first move, then filter it to None and remove duplicates.
    get_direction decides the actual direction for sowing.

    moves are always MoveTpl's or PASS.
    mcount is not updated until the move is selected e.g. by Mancala.move"""

    def get_moves(self):

        moves = self.decorator.get_moves()

        if self.game.mcount == 1 or gi.PASS_TOKEN in moves:
            return moves

        new_moves = set()
        for move in moves:
            new_moves.add(move.set_dir(None))

        return list(new_moves)


class StoreMoveAll(MovesIf):
    """Moves are allowed from the player's own store."""

    def get_moves(self):

        moves = self.decorator.get_moves()
        if self.game.store[self.game.turn]:
            moves += [(-(self.game.turn + 1),
                       self.game.store[self.game.turn])]

        return moves


class StoreMoveChoose(MovesIf):
    """Any number of seeds may be moved from the player's own store."""

    def get_moves(self):

        moves = self.decorator.get_moves()

        for seeds in range(1, self.game.store[self.game.turn] + 1):
            moves += [(-(self.game.turn + 1), seeds)]

        return moves


# %% build deco chain

def deco_moves(game):
    """Build the get_moves deco."""

    if game.info.mlength == 2:
        moves = UdirMoves(game)

    elif game.info.mlength == 3:
        if game.info.udirect:
            moves = MovesUdirTriples(game)
        else:
            moves = MovesTriples(game)

    else:
        moves = Moves(game)

    if game.info.mustpass:
        moves = PassMoves(game, moves)

    if game.info.sow_direct == gi.Direct.PLAYALTDIR:
        moves = AltDirMoves(game, moves)

    if game.info.play_locs == gi.PlayLocs.BRD_OWN_STR_ALL:
        moves = StoreMoveAll(game, moves)
    elif game.info.play_locs == gi.PlayLocs.BRD_OWN_STR_CHS:
        moves = StoreMoveChoose(game, moves)

    return moves
