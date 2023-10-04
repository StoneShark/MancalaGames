# -*- coding: utf-8 -*-
"""Store and compute constants used throught the
games based on the size of the game board and
the number of seeds place in each hole at the
start.

Use a frozen class so that the two base numbers
can't be changed, assuring the other values are
consistent and accurate.

Created on Fri Mar 17 14:59:55 2023
@author: Ann"""

import dataclasses as dc

MAX_HOLES = 14
MIN_HOLES = 2

MAX_SEEDS = 12


class GameConstsError(Exception):
    """Error in GameConsts."""


@dc.dataclass(frozen=True)
class GameConsts:
    """Collect game constants into one class.
    Anything dependent on nbr_start or holes should be here."""

    nbr_start: int
    holes: int

    dbl_holes: int = dc.field(init=False, repr=False)
    half_holes: int = dc.field(init=False, repr=False)

    total_seeds: int = dc.field(init=False, repr=False)
    win_count: int = dc.field(init=False, repr=False)

    false_range: int = dc.field(init=False, repr=False)
    true_range: int = dc.field(init=False, repr=False)

    false_fill: int = dc.field(init=False, repr=False)
    true_fill: int = dc.field(init=False, repr=False)


    def __post_init__(self):
        """Compute some game constants and ranges."""

        if self.holes < MIN_HOLES or self.holes > MAX_HOLES:
            raise GameConstsError(
                f'Holes out of range [{MIN_HOLES}..{MAX_HOLES}] inclusive.')
        if self.nbr_start <= 0 or self.nbr_start > MAX_SEEDS:
            raise GameConstsError(
                f'Nbr_start out of range [1..{MAX_SEEDS}] inclusive.')

        object.__setattr__(self, 'dbl_holes', self.holes * 2)
        object.__setattr__(self, 'half_holes', self.holes // 2)

        object.__setattr__(self, 'total_seeds',
                           self.dbl_holes * self.nbr_start)
        object.__setattr__(self, 'win_count', self.total_seeds//2)

        object.__setattr__(self, 'false_range', range(0, self.holes))
        object.__setattr__(self, 'true_range',
                           range(self.dbl_holes-1, self.holes-1, -1))

        order = []
        for i in range(self.holes//2):
            order += [i, -(i + 1)]
        if self.holes % 2:
            order += [self.holes//2]

        vals = list(self.false_range)
        object.__setattr__(self, 'false_fill', [vals[i] for i in order])

        vals = list(self.true_range)
        object.__setattr__(self, 'true_fill', [vals[i] for i in order])


    def __str__(self):
        """Return a nice string representation."""

        string =  f'GameConsts({self.nbr_start}, {self.holes})\n'
        string += f'   dbl_holes={self.dbl_holes}\n'
        string += f'   half_holes={self.half_holes}\n'
        string += f'   total_seeds={self.total_seeds}\n'
        string += f'   win_count={self.win_count}\n'
        string +=  '   false_range=' + repr(self.false_range) + '\n'
        string +=  '   true_range=' + repr(self.true_range) + '\n'
        string +=  '   false_fill=' + repr(self.false_fill) + '\n'
        string +=  '   true_fill=' + repr(self.true_fill)

        return string


    def get_dict(self):
        """Only need these two params to recreate."""

        return {'nbr_start': self.nbr_start,
                'holes': self.holes}


    def xlate_pos_loc(self, row, pos):
        """Convert the pos (0.. holes-1) to loc
        (array index loc, 0 .. dbl_holes-1)
        row is not turn"""

        return pos if row else self.dbl_holes - pos - 1


    def loc_to_left_cnt(self, loc):
        """Translate loc to a count from the left side,
        based on player perspective."""
        return (loc - self.holes) if loc >= self.holes else loc


    def cross_from_loc(self, loc):
        """Return the hole location across from loc."""
        return self.dbl_holes - loc - 1


    def opp_side(self, turn, loc):
        """Function to tell if loc is on opponents side of board."""

        if turn:
            return loc in self.false_range

        return loc in self.true_range


    def my_side(self, turn, loc):
        """Function to tell if loc is on my side of board."""

        if turn:
            return loc in self.true_range

        return loc in self.false_range


    def get_ranges(self, turn):
        """Return the ranges and limit:  my_range, opp_range"""

        if turn:
            return self.true_range, self.false_range

        return self.false_range, self.true_range


    def get_my_range(self, turn):
        """Return the range for the current player."""

        if turn:
            return self.true_range

        return self.false_range


    def get_opp_range(self, turn):
        """Return the range for the opposite player."""

        if turn:
            return self.false_range

        return self.true_range
