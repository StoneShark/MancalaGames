# -*- coding: utf-8 -*-
"""Common deco chain code:
If the deco chain doesn't do anything unique in
__init__ or __str__ use this class instead of abc.ABC.

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
