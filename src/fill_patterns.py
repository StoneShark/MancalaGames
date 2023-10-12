# -*- coding: utf-8 -*-
"""Class describing alternate starting fill patterns.

Created on Wed Oct 11 17:54:37 2023
@author: Ann"""

import abc

from game_interface import StartPattern


class StartPatternIf:
    """A group of pattern methods."""

    @staticmethod
    @abc.abstractmethod
    def size_ok(holes):
        """Return True if the pattern can be used
        with holes per side."""

    @staticmethod
    @abc.abstractmethod
    def nbr_seeds(holes, nbr_start):
        """Return the total number of seeds."""

    @staticmethod
    @abc.abstractmethod
    def fill_seeds(game):
        """Put the seeds into the board and adjust for start player."""


    @staticmethod
    def rev_board(game):
        """Rotate the board (as though you picked up the
        board and rotated it 180 degrees)."""

        holes = game.cts.holes
        dholes = game.cts.dbl_holes
        return game.board[holes:dholes] + game.board[0:holes]


class GamachaPattern(StartPatternIf):
    """Gamacha pattern:  two empty, then alternating 4 and 0.
    First prescribed move is automatically done."""

    @staticmethod
    def size_ok(holes):
        return holes >= 3
    err_msg = 'Pattern One requires at least 3 holes'

    @staticmethod
    def nbr_seeds(holes, nbr_start):
        """return the total number of seeds."""
        return (holes - 1) * nbr_start

    @staticmethod
    def compute_dest(holes):
        """Compute the lower hole (destination).
        Starting at 3:
            1, 1, 3, 3, 3, 3, 5, 5, 5, 5, 7, 7 ..."""
        return 1 + 2 * ((holes-1) // 4)

    @staticmethod
    def fill_seeds(game):

        game.board = [0] * game.cts.dbl_holes
        for loc in range(2, game.cts.dbl_holes, 2):
            game.board[loc] = game.cts.nbr_start

        dest = GamachaPattern.compute_dest(game.cts.holes)
        source = game.cts.dbl_holes - dest - 1

        game.board[dest] = game.board[source]
        game.board[source] = 0

        if game.turn:
            game.board = StartPatternIf.rev_board(game)


class SadeqaPatternOne(StartPatternIf):
    """Sadeqa pattern: alternating 0 and nbr_start.
    If the sides are not even, starter get fewer seeds."""

    @staticmethod
    def size_ok(holes):
        return True
    err_msg = 'Sadeqa Pattern One is always good'


    @staticmethod
    def nbr_seeds(holes, nbr_start):
        return holes * nbr_start


    @staticmethod
    def fill_seeds(game):

        game.board = [0] * game.cts.dbl_holes
        for loc in range(1, game.cts.dbl_holes, 2):
            game.board[loc] = game.cts.nbr_start

        if game.cts.holes % 2 and game.turn:
            game.board = StartPatternIf.rev_board(game)


class SadeqaPatternTwo(StartPatternIf):
    """Sadeqa pattern: alternating 0 and nbr_start, with second
    nbr_start on starter side as 1."""

    @staticmethod
    def size_ok(holes):
        return holes >= 3
    err_msg = 'Sadeqa Pattern Two requires at least 3 holes'


    @staticmethod
    def nbr_seeds(holes, nbr_start):
        return holes * nbr_start - 3


    @staticmethod
    def fill_seeds(game):

        game.board = [0] * game.cts.dbl_holes
        for loc in range(1, game.cts.dbl_holes, 2):
            game.board[loc] = game.cts.nbr_start

        second = game.cts.holes + 3 - game.cts.holes % 2
        game.board[second] = 1

        if not game.turn:
            game.board = StartPatternIf.rev_board(game)


class TapataPattern(StartPatternIf):
    """Tapata pattern: repeating 0 nbr_start nbr_start"""

    @staticmethod
    def size_ok(holes):
        return holes >= 3
    err_msg = 'Tapata Pattern requires at least 3 holes'


    @staticmethod
    def nbr_seeds(holes, nbr_start):
        return holes // 3 * nbr_start * 4


    @staticmethod
    def fill_seeds(game):

        holes = game.cts.holes
        dbl_holes = game.cts.dbl_holes
        seeds = game.cts.nbr_start

        game.board = [0] * dbl_holes
        for loc in range(3, holes + 1, 3):
            game.board[loc - 1] = seeds
            game.board[loc - 2] = seeds
        game.board[holes:dbl_holes] = game.board[:holes]


# %%

PCLASSES = [None] * len(StartPattern)

PCLASSES[StartPattern.GAMACHA] = GamachaPattern
PCLASSES[StartPattern.SADEQA_ONE] = SadeqaPatternOne
PCLASSES[StartPattern.SADEQA_TWO] = SadeqaPatternTwo
PCLASSES[StartPattern.TAPATA] = TapataPattern
