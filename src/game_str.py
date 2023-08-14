# -*- coding: utf-8 -*-
"""Generate games string for the game log based
on game flags.

Created on Fri Apr  7 17:33:56 2023
@author: Ann"""

# %% imports

import abc


# %% constants

LOCK = ['_', ' ']

UP = '\u02c4'
DN = '\u02c5'

CHILD = {True: UP,
         False: DN,
         None: ' '}


# %%  interfaces

class HoleStrIF(abc.ABC):
    """Generate a hole string."""

    def __init__(self, game, decorator):
        self.decorator = decorator
        self.game = game

    @abc.abstractmethod
    def get_hole_str(self, loc):
        """Generate a hole string.
        Default implementation so first class in chaing can call it."""
        return ''


class StringIf(abc.ABC):
    """Interface for strings."""

    def __init__(self, game):
        self.game = game

    @abc.abstractmethod
    def get_string(self):
        """Generate the game string."""


# %% String classes

class StringBasic(StringIf):
    """Create a game string."""

    def get_string(self):
        """Return the basic string."""

        sgame = self.game

        string = ' '.join(
            [f'{p:3}' for p in
             sgame.board[sgame.cts.holes:sgame.cts.dbl_holes][::-1]])
        string += '  *' if sgame.turn else '   '
        string += f'  {sgame.store[1]:3}' if sgame.store[1] else ''
        string += '\n'
        string += ' '.join([f'{p:3}'
                            for p in sgame.board[0:sgame.cts.holes]])
        string += '  *' if not sgame.turn else '   '
        string += f'  {sgame.store[0]:3}' if sgame.store[0] else ''

        return string


class StringAnnotates(StringIf):
    """Create a game string, given a hole string object."""

    def __init__(self, game, hole_str):

        super().__init__(game)
        self.hole_str = hole_str

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


# %% Hole classes

class HoleStrUnlock(HoleStrIF):
    """Create a hole string for games with locks,
    relief is used in the UI for locked holes."""

    def get_hole_str(self, loc):
        """Return mark for hole"""

        return LOCK[self.game.unlocked[loc]] + super().get_hole_str(loc)


class HoleStrChild(HoleStrIF):
    """Create a hole string for games with hole owners:
    children/daughters/waldas"""


    def get_hole_str(self, loc):
        """Return mark for hole"""

        return CHILD[self.game.child[loc]] + super().get_hole_str(loc)


# %%

def deco_get_string(game):
    """Not a decorator chain, just an individual class.

    Blocked is handled by both string base classes."""

    if not any([game.info.flags.child, game.info.flags.moveunlock]):
        return StringBasic(game)

    hole_deco = None

    if game.info.flags.moveunlock:
        hole_deco = HoleStrUnlock(game, hole_deco)

    if game.info.flags.child:
        hole_deco = HoleStrChild(game, hole_deco)

    return StringAnnotates(game, hole_deco)
