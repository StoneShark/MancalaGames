# -*- coding: utf-8 -*-
"""Choose a direction for the move.
Make as many decisions at construction as possible.

Created on Thu Aug 10 04:26:30 2023
@author: Ann"""

import abc

from game_interface import Direct


# %% interface

class GetDirIf(abc.ABC):
    """Determine the direction to sow the seeds.
    Get both the move, either a pos or (pos, move) tuple,
    and the translated loc."""

    @abc.abstractmethod
    def get_direction(self, move, loc):
        """Return: Direct - but always CCW or CW"""


# %% direction getters

class ConstDir(GetDirIf):
    """Direction is Diect.CW or Direct.CCW, don't need to
    make any game time decisions."""

    def __init__(self, const):
        self.const = const

    def get_direction(self, _1, _2):
        return self.const


class SplitDir(GetDirIf):
    """Pure split dir, precompute the diretions for all
    locations, then lookup and return at game time.
    Board size must be even or an error would have been
    generated at game creation; include odd center
    hole so this can be used by UdirOther."""

    def __init__(self, holes):

        half_holes, rem = divmod(holes, 2)
        self.direction = [Direct.CW] * half_holes
        self.direction += [None] if rem else []
        self.direction += [Direct.CCW] * half_holes
        self.direction += [Direct.CW] * half_holes
        self.direction += [None] if rem else []
        self.direction += [Direct.CCW] * half_holes

    def get_direction(self, _, loc):

        return self.direction[loc]


class UdirAllDir(GetDirIf):
    """All of the holes are user choice.
    The UI/user picked the direction, just return it."""

    def get_direction(self, move, _):
        """Move is a tuple (pos, direct)."""

        return move[1]


class UdirOtherDir(GetDirIf):
    """Use split sow for any holes that are not in
    udir_holes."""

    def __init__(self, decorator, udir_holes):

        self.decorator = decorator
        self.udir_holes = udir_holes

    def get_direction(self, move, loc):
        """Move is a (pos, dir) tuple.
        If the user picked the direction, return it.
        Other use the next direction getter."""

        pos, direct = move
        if pos in self.udir_holes:
            return direct
        return self.decorator.get_direction(pos, loc)


# %%  build deco

def deco_dir_getter(game):
    """Select the direction chooser.
    If all holes are specified as user dir, don't care
    what sow_direction is."""

    gflags = game.info.flags

    if len(game.info.udir_holes) == game.cts.holes:
        return UdirAllDir()

    if gflags.sow_direct is Direct.SPLIT:
        dir_getter = SplitDir(game.cts.holes)
    else:
        dir_getter = ConstDir(gflags.sow_direct)

    if gflags.udirect:
        return UdirOtherDir(dir_getter, game.info.udir_holes)

    return dir_getter
