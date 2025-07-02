# -*- coding: utf-8 -*-
"""Classes describing alternate starting fill patterns.

Each class is a collection of well defined operations
for a start pattern. The class is an easy way to group them.
The objects do need to be instantiated because there's
no data.

Start patterns differ from prescribed openings (see
sower.SowPrescribedIf and game_info.SowPrescirbed)
in that start patterns do not require any user input
and may simply be executed.

Not all patterns can be used for all board sizes (size_ok).
Start patterns may change the total number of seeds
used in the game (nbr_seeds).

The new_game decorator chain (NewGamePattern) calls the
fill_seeds method.

The patterns are available in a global variable in the
same order as gi.StartPattern.

Created on Wed Oct 11 17:54:37 2023
@author: Ann"""

import abc
import itertools as it
import random

import game_info as gi


FOUR = 4


class StartPatternIf(abc.ABC):
    """A group of pattern methods."""

    @staticmethod
    @abc.abstractmethod
    def size_ok(holes):
        """Return True if the pattern can be used
        with holes per side."""

    @classmethod
    @property
    @abc.abstractmethod
    def err_msg(cls):
        """The error message if size is not ok."""


    @staticmethod
    @abc.abstractmethod
    def nbr_seeds(holes, nbr_start):
        """Return the total number of seeds."""

    @staticmethod
    @abc.abstractmethod
    def fill_seeds(game):
        """Put the seeds into the board and adjust for start player."""


    @staticmethod
    def _rev_board(game):
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

    @classmethod
    @property
    def err_msg(cls):
        return 'Gamacha Pattern requires at least 3 holes'

    @staticmethod
    def nbr_seeds(holes, nbr_start):
        """return the total number of seeds."""
        return (holes - 1) * nbr_start

    @staticmethod
    def compute_dest(holes):
        """Compute the lower hole (destination).
        Starting at 3:
            1, 1, 3, 3, 3, 3, 5, 5, 5, 5, 7, 7 ..."""
        return 1 + 2 * ((holes - 1) // 4)

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
            game.board = StartPatternIf._rev_board(game)


class AlternatesPattern(StartPatternIf):
    """Alternates pattern: alternating 0 and nbr_start.
    If the sides are not even, starter get fewer seeds."""

    @staticmethod
    def size_ok(holes):
        return True

    @classmethod
    @property
    def err_msg(cls):
        return 'Alternates Pattern is always good'


    @staticmethod
    def nbr_seeds(holes, nbr_start):
        return holes * nbr_start


    @staticmethod
    def fill_seeds(game):

        game.board = [0] * game.cts.dbl_holes
        for loc in range(1, game.cts.dbl_holes, 2):
            game.board[loc] = game.cts.nbr_start

        if game.cts.holes % 2 and game.turn:
            game.board = StartPatternIf._rev_board(game)


class AltsWithOnePattern(StartPatternIf):
    """Alternates with One pattern: alternating 0 and nbr_start
    with two changes:

        1. the second from right nbr_start hole on non-starter
           side is reduced to 1
        2. if there are an even number of holes per side,
           remove seeds from the second from right hole
           with nbr_start seeds on the starter side.

    This yields board with 5 and 6 seeds having the same number
    of total seeds. The non-starter has 1 extra seed."""

    @staticmethod
    def size_ok(holes):
        return holes >= 3

    @classmethod
    @property
    def err_msg(cls):
        return 'Alternates w/ 1 requires at least 3 holes'


    @staticmethod
    def nbr_seeds(holes, nbr_start):
        not_filled = 2 - holes % 2
        return (holes - not_filled) * nbr_start + 1


    @staticmethod
    def fill_seeds(game):

        game.board = [0] * game.cts.dbl_holes
        for loc in range(1, game.cts.dbl_holes, 2):
            game.board[loc] = game.cts.nbr_start

        second = game.cts.holes + 3 - game.cts.holes % 2
        game.board[second] = 1
        if not game.cts.holes % 2:
            second = game.cts.holes - 3
            game.board[second] = 0

        if game.turn:
            game.board = StartPatternIf._rev_board(game)


class AltsThenSplitPattern(StartPatternIf):
    """Alternates then split pattern: alternating 0 and nbr_start,
    but then one-third of the non-starters rightmost hole's seeds
    are moved directly across the board to the starter (their
    leftmost hole)."""

    @staticmethod
    def size_ok(holes):
        return not holes % 2


    @classmethod
    @property
    def err_msg(cls):
        return 'Alternates Then Split requires an even number of holes per side'


    @staticmethod
    def nbr_seeds(holes, nbr_start):
        return holes * nbr_start


    @staticmethod
    def fill_seeds(game):

        holes = game.cts.holes
        dholes = game.cts.dbl_holes
        nstart = game.cts.nbr_start

        game.board = [0] * dholes
        for loc in range(1, dholes, 2):
            game.board[loc] = nstart

        move_seeds = nstart // 4
        game.board[holes] += move_seeds
        game.board[holes - 1] -= move_seeds

        if not game.turn:
            game.board = StartPatternIf._rev_board(game)


class ClippedTriplesPattern(StartPatternIf):
    """Clipped triples pattern (tapata): repeating 0 nbr_start nbr_start"""

    @staticmethod
    def size_ok(holes):
        return holes >= 3


    @classmethod
    @property
    def err_msg(cls):
        return 'Clipped Tripples Pattern requires at least 3 holes'


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


class TwoEmptyPattern(StartPatternIf):
    """TwoEmpty:  S S ... S 0 0"""

    @staticmethod
    def size_ok(holes):
        return holes >= FOUR


    @classmethod
    @property
    def err_msg(cls):
        return 'TwoEmpty Pattern requires at least 4 holes'


    @staticmethod
    def nbr_seeds(holes, nbr_start):
        return (holes - 2) * nbr_start * 2


    @staticmethod
    def fill_seeds(game):

        holes = game.cts.holes
        dbl_holes = game.cts.dbl_holes
        seeds = game.cts.nbr_start

        game.board = [0] * dbl_holes
        for loc in range(holes - 2):
            game.board[loc] = seeds
        game.board[holes:dbl_holes] = game.board[:holes]


class NoRepeatSowOwn(StartPatternIf):
    """If the game were to be a sow_own_store game, adjust
    the seeds so that there is no repeat turn on the opening move.
    An adjustment is not always done.

    Note that the opening player's move may give the opponent a
    repeat turn."""

    @staticmethod
    def size_ok(holes):
        """Return True if the pattern can be used
        with holes per side."""
        return holes > 2


    @classmethod
    @property
    def err_msg(cls):
        return 'NoRepeatSowOwn requires at least 3 holes per side'


    @staticmethod
    def nbr_seeds(holes, nbr_start):
        """Return the total number of seeds."""
        return nbr_start * holes * 2

    @staticmethod
    def fill_seeds(game):
        """Put the seeds into the board and adjust for start player."""

        holes = game.cts.holes
        dholes = game.cts.dbl_holes
        nbr_start = game.cts.nbr_start

        if nbr_start <= 2:
            p1_hole = holes - nbr_start
            m1_hole = max(0, p1_hole - 2)

        elif nbr_start <= holes:
            p1_hole = holes - nbr_start
            m1_hole = holes + 2 - nbr_start

        else:
            sstore = nbr_start % (dholes + 1)
            p1_hole = holes - sstore
            if not 0 <= p1_hole < holes:
                return

            m1_hole = holes + 2 - sstore
            if m1_hole >= holes:
                for tpos in range(holes):   # pragma: no coverage
                    if not (tpos == p1_hole
                            or tpos + (nbr_start - 1) % (dholes + 1) == holes):
                        break
                m1_hole = tpos

        game.board[m1_hole] -= 1
        game.board[p1_hole] += 1
        game.board[holes:dholes] = game.board[:holes]


class RandomPattern(StartPatternIf):
    """Fill with random seeds but at least two in each hole,
    if there are more than enough seeds to put 2 per hole.
    Otherwise, minimum is 0."""

    @staticmethod
    def size_ok(holes):
        return True


    @classmethod
    @property
    def err_msg(cls):
        return 'RandomPattern is always good'


    @staticmethod
    def nbr_seeds(_, nbr_start):
        return nbr_start


    @staticmethod
    def fill_seeds(game):

        dbl_holes = game.cts.dbl_holes
        total = game.cts.total_seeds

        min_seeds = 0 if total < 2 * dbl_holes else 2
        rnd_seeds = total - (min_seeds * dbl_holes)

        rnumbers = sorted([random.random() for _ in range(dbl_holes - 1)]
                           + [0, 1])
        values = [min_seeds + int(rnd_seeds * (b - a) + 0.4)
                  for a, b in it.pairwise(rnumbers)]

        error = total - sum(values)
        if error > 0:
            values[values.index(min(values))] += error

        elif error < 0:
            values[values.index(max(values))] += error

        game.board = values


class RandomEmptiesPattern(StartPatternIf):
    """Fill with random seeds, holes maybe empty, but
    every filled hole must have at least 4 seeds."""

    @staticmethod
    def size_ok(holes):
        return True


    @classmethod
    @property
    def err_msg(cls):
        return 'RandomEmptiesPattern is always good'


    @staticmethod
    def nbr_seeds(_, nbr_start):
        return nbr_start


    @staticmethod
    def fill_seeds(game):

        dbl_holes = game.cts.dbl_holes
        total = game.cts.total_seeds

        rnumbers = sorted([random.random() for _ in range(dbl_holes - 1)]
                           + [0, 1])
        values = [int(total * (b - a) + 0.4)
                  for a, b in it.pairwise(rnumbers)]

        error = total - sum(values)
        if error > 0:
            values[values.index(min(values))] += error
        elif error < 0:
            values[values.index(max(values))] += error

        # move seeds from any holes with fewer than 4
        # to the next hole that will be >= 4
        holding = 0
        for idx in range(dbl_holes):

            val = values[idx]
            if val + holding < FOUR:
                values[idx] = 0
                holding += val
            else:
                values[idx] = val + holding
                holding = 0

        # if we are still holding seeds find a place to put them
        if holding:
            for idx in range(dbl_holes):
                if values[idx] > 0:
                    values[idx] += holding
                    break

        game.board = values


class RightmostPlusOne(StartPatternIf):
    """Fill equally with start seeds but then put one more into
    into each player's rightmost hole."""

    @staticmethod
    def size_ok(holes):
        return True


    @classmethod
    @property
    def err_msg(cls):
        return 'RightmostPlusOne is always good'


    @staticmethod
    def nbr_seeds(holes, nbr_start):
        return nbr_start * holes * 2 + 2


    @staticmethod
    def fill_seeds(game):

        nstart = game.cts.nbr_start
        holes = game.cts.holes
        game.board = ([nstart] * (holes - 1) + [nstart + 1]) * 2


class MoveRightmost(StartPatternIf):
    """Require first move from rightmost hole, not exactly a start
    pattern, but certainly not a prescribed opening.

    Not supported for mlength 2 or 3 games."""

    @staticmethod
    def size_ok(holes):
        return True


    @classmethod
    @property
    def err_msg(cls):
        return 'MoveRightmost is always good'


    @staticmethod
    def nbr_seeds(holes, nbr_start):
        return nbr_start * holes * 2


    @staticmethod
    def fill_seeds(game):
        """Do the move.  The move result is ignored, it would
        be a very boring game if the required opening move
        resulted in a WIN."""

        move_pos = 0 if game.turn else game.cts.holes - 1
        game.move(move_pos)


class MoveRandom(StartPatternIf):
    """Make a random opening move."""

    @staticmethod
    def size_ok(holes):
        return True


    @classmethod
    @property
    def err_msg(cls):
        return 'MoveRandom is always good'


    @staticmethod
    def nbr_seeds(holes, nbr_start):
        return nbr_start * holes * 2


    @staticmethod
    def fill_seeds(game):
        """Do a random move.  The move result is ignored.
        If the turn is the same as the starter, swap it.
        No repeat turn on an opening move."""

        game.move(random.choice(game.get_moves()))

        if game.turn == game.starter:
            game.turn = not game.turn


# %% Pattern Classes variable

PCLASSES = [None] * len(gi.StartPattern)

PCLASSES[gi.StartPattern.GAMACHA] = GamachaPattern
PCLASSES[gi.StartPattern.ALTERNATES] = AlternatesPattern
PCLASSES[gi.StartPattern.ALTS_WITH_1] = AltsWithOnePattern
PCLASSES[gi.StartPattern.CLIPPEDTRIPLES] = ClippedTriplesPattern
PCLASSES[gi.StartPattern.TWOEMPTY] = TwoEmptyPattern
PCLASSES[gi.StartPattern.RANDOM] = RandomPattern
PCLASSES[gi.StartPattern.ALTS_SPLIT] = AltsThenSplitPattern
PCLASSES[gi.StartPattern.RIGHTMOST_PLUS_ONE] = RightmostPlusOne
PCLASSES[gi.StartPattern.MOVE_RIGHTMOST] = MoveRightmost
PCLASSES[gi.StartPattern.MOVE_RANDOM] = MoveRandom
PCLASSES[gi.StartPattern.NO_REPEAT_SOW_OWN] = NoRepeatSowOwn
PCLASSES[gi.StartPattern.RANDOM_ZEROS] = RandomEmptiesPattern
