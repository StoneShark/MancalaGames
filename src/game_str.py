# -*- coding: utf-8 -*-
"""Generate games string for the game log based
on game flags.

Created on Fri Apr  7 17:33:56 2023
@author: Ann"""

# %% imports

import abc

import deco_chain_if
import game_interface as gi

# %% constants

LOCK = ['_', ' ']

CHILD = {True: '\u02c4',
         False: '\u02c5',
         None: ' '}

OWNER = {True: '\u2191 ',
         False: '\u2193 ',
         None: ' '}


# %%  interfaces

class HoleMarkerIf(deco_chain_if.DecoChainIf):
    """Generate a hole string."""

    @abc.abstractmethod
    def get_hole_str(self, loc):
        """Generate a hole string."""


class StringIf(deco_chain_if.DecoChainIf):
    """Interface for strings."""

    @abc.abstractmethod
    def get_string(self):
        """Generate the game string."""


# %%  Hole class

class HoleMarker(HoleMarkerIf):
    """Generate a hole string."""

    def __init__(self, game, str_dict=None, field=None, decorator=None):

        super().__init__(game, decorator)
        self.str_dict = str_dict
        self.field = field


    def get_hole_str(self, loc):
        """Return mark for hole"""

        if not self.game:
            return ''

        vals = getattr(self.game, self.field)
        return self.str_dict[vals[loc]] + self.decorator.get_hole_str(loc)


# %% String class

class GameString(StringIf):
    """Create a game string, given a hole string object."""

    def __init__(self, game, hole_str):

        super().__init__(game)
        self.hole_str = hole_str

    def __str__(self):

        return repr(self) + '\n' + str(self.hole_str)

    def get_string(self):
        """Get string with blocks and/or marks."""

        string = ''

        for side, side_range in enumerate([self.game.cts.true_range,
                                           self.game.cts.false_range]):
            for loc in side_range:

                if self.game.blocked[loc]:
                    string += '  x'
                else:
                    string += f' {self.game.board[loc]:2}'
                string += self.hole_str.get_hole_str(loc)

            string += '  *' if int(not self.game.turn) == side else '   '
            loc = (side + 1) % 2
            string += f'  {self.game.store[loc]:3}' \
                      if self.game.store[loc] else ''

            if not side:
                string += '\n'

        return string


# %%

def deco_get_string(game):
    """Not a decorator chain, just an individual class
    with a decorator to add marks to the hole text."""

    hole_deco = HoleMarker(None)

    if game.info.goal == gi.Goal.TERRITORY:
        hole_deco = HoleMarker(game, OWNER, 'owner', hole_deco)

    if (game.info.moveunlock
            or game.info.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST):
        hole_deco = HoleMarker(game, LOCK, 'unlocked', hole_deco)

    if game.info.child_cvt:
        hole_deco = HoleMarker(game, CHILD, 'child', hole_deco)

    return GameString(game, hole_deco)
