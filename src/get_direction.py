# -*- coding: utf-8 -*-
"""Choose a direction for the move.
Make as many decisions at construction as possible.

Created on Thu Aug 10 04:26:30 2023
@author: Ann"""

import abc

import deco_chain_if
import game_info as gi


# %% interface

class GetDirIf(deco_chain_if.DecoChainIf):
    """Determine the direction to sow the seeds."""

    @abc.abstractmethod
    def get_direction(self, mdata):
        """Return: Direct - but always CCW or CW"""


# %% direction getters

class ConstDir(GetDirIf):
    """Direction is Diect.CW or Direct.CCW, don't need to
    make any game time decisions."""

    def __init__(self, game, decorator=None):
        super().__init__(game, decorator)
        self.const = game.info.sow_direct

    def get_direction(self, _):
        return self.const


class SplitDir(GetDirIf):
    """Sow towards the outer edge of the board.
    Precompute the diretions for all locations,
    then lookup and return at game time.

    This shouldn't be called for the center hole
    when the board size is odd, None will be returned."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)
        holes = game.cts.holes
        half_holes, rem = divmod(holes, 2)
        self.direction = [gi.Direct.CW] * half_holes
        self.direction += [None] if rem else []
        self.direction += [gi.Direct.CCW] * half_holes
        self.direction += [gi.Direct.CW] * half_holes
        self.direction += [None] if rem else []
        self.direction += [gi.Direct.CCW] * half_holes

    def get_direction(self, mdata):
        return self.direction[mdata.sow_loc]


class CenterLineDir(GetDirIf):
    """Sow towards the center line of the board.
    Precompute the diretions for all locations,
    then lookup and return at game time.

    This shouldn't be called for the center hole
    when the board size is odd, None will be returned."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)
        holes = game.cts.holes
        half_holes, rem = divmod(holes, 2)
        self.direction = [gi.Direct.CCW] * half_holes
        self.direction += [None] if rem else []
        self.direction += [gi.Direct.CW] * half_holes
        self.direction += [gi.Direct.CCW] * half_holes
        self.direction += [None] if rem else []
        self.direction += [gi.Direct.CW] * half_holes

    def get_direction(self, mdata):
        return self.direction[mdata.sow_loc]


class UdirDir(GetDirIf):
    """The hole is a udir. Move is a tuple (pos, direct).
    The UI/user picked the direction, just return it."""

    def get_direction(self, mdata):
        return mdata.move[1]


class UdirTripleDir(GetDirIf):
    """The hole is user choice. Move is a tuple (row, pos, direct).
    The UI/user picked the direction, just return it."""

    def get_direction(self, mdata):
        return mdata.move[2]


class UdirOtherDir(GetDirIf):
    """If the hole is udirect, then use the udir_getter,
    otherwise use the decorator."""

    def __init__(self, game, decorator, udir_getter):

        super().__init__(game, decorator)
        self.udir_getter = udir_getter

    def get_direction(self, mdata):

        left_cnt = self.game.cts.loc_to_left_cnt(mdata.sow_loc)
        if left_cnt in self.game.info.udir_holes:
            return self.udir_getter.get_direction(mdata)

        return self.decorator.get_direction(mdata)


class PlayAltDir(GetDirIf):
    """After the first player chooses the direction,
    players alternate directions."""

    def __init__(self, game, decorator):

        super().__init__(game, decorator)
        self.player_dirs = [None, None]

    def get_direction(self, mdata):

        turn = self.game.turn
        if self.game.mcount == 1:
            direct = self.decorator.get_direction(mdata)
            self.player_dirs[turn] = direct
            self.player_dirs[not turn] = direct.opp_dir()

        return self.player_dirs[turn]


class EvenOddDir(GetDirIf):
    """Holes with an odd number of seeds sow CCW, and CW otherwise."""

    def get_direction(self, mdata):

        seeds = mdata.board[mdata.sow_loc]
        return gi.Direct.CCW if seeds % 2 else gi.Direct.CW


class StoreDir(GetDirIf):
    """A wrapper that get's the direction for games that
    play from stores--it is the base game sower."""

    def get_direction(self, mdata):

        if isinstance(mdata.move, tuple) and mdata.move[0] < 0:
            return self.game.info.sow_direct

        return self.decorator.get_direction(mdata)


# %%  build deco

def _pick_udir_getter(game):
    """Pick the udir_getter (if needed). The main code will figure
    out where it goes in the deco chain."""

    udir_getter = None
    if game.info.udirect:
        if game.info.mlength == 3:
            udir_getter = UdirTripleDir(game)
        else:
            udir_getter = UdirDir(game)

    return udir_getter


def deco_dir_getter(game):
    """Create the dir_getter chain."""

    udir_getter = _pick_udir_getter(game)

    if len(game.info.udir_holes) == game.cts.holes:
        if game.info.sow_direct == gi.Direct.PLAYALTDIR:
            dir_getter = PlayAltDir(game, udir_getter)

        else:
            dir_getter = udir_getter

    else:
        if game.info.sow_direct is gi.Direct.SPLIT:
            dir_getter = SplitDir(game)

        elif game.info.sow_direct is gi.Direct.TOCENTER:
            dir_getter = CenterLineDir(game)

        elif game.info.sow_direct is gi.Direct.EVEN_ODD_DIR:
            dir_getter = EvenOddDir(game)

        else:
            dir_getter = ConstDir(game)

        if game.info.udirect:
            dir_getter = UdirOtherDir(game, dir_getter, udir_getter)

    if game.info.play_locs:
        dir_getter = StoreDir(game, dir_getter)

    return dir_getter
