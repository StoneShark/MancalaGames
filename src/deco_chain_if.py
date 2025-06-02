# -*- coding: utf-8 -*-
"""The base class for decorator chains.

Decorator chains can save data unique to the game
on startup/creation, but they should not store
state data that would be changed during the game.

Decos are not told about a new game or round
being started. Data is not saved with game state!

Created on Tue Dec 19 12:11:06 2023
@author: Ann"""


import abc


class DecoChainIf(abc.ABC):
    """Common deco chain implementations."""

    def __init__(self, game, decorator=None):
        self.game = game
        self.decorator = decorator


    def __str__(self):
        """A recursive func to print the whole decorator chain."""

        my_str = repr(self)
        if self.decorator:
            return my_str + '\n' + str(self.decorator)
        return my_str


    def str_deco_detail(self, details):
        """Use this in derived __str__ methods that add details
        to the deco repr."""

        my_str = '\n'.join([repr(self), '   ' + details])

        if self.decorator:
            my_str += '\n' + str(self.decorator)
        return my_str
