# -*- coding: utf-8 -*-
"""Create a new game or round.

Created on Fri Apr  7 12:47:15 2023
@author: Ann"""


# %% imports

import abc
import random

import deco_chain_if
import end_move
import game_interface as gi

from game_logger import game_log
from fill_patterns import PCLASSES


# %% set_round_starter

def set_round_starter(game):
    """Set the starter of the next round based on the game flag."""

    start_rule = game.info.round_starter
    if start_rule == gi.RoundStarter.ALTERNATE or game.turn is None:
        game.turn = not game.starter

    elif start_rule == gi.RoundStarter.LOSER:
        game.turn = not game.turn

    elif start_rule == gi.RoundStarter.LAST_MOVER:
        game.turn = game.last_mdata.player

    game.starter = game.turn


# %%  NewGame interace

class NewGameIf(deco_chain_if.DecoChainIf):
    """New Game Interface."""

    @abc.abstractmethod
    def new_game(self, win_cond=None, new_round_ok=False):
        """collect seeds when game ended.

        Return False if a new round was started.
        True if a new game was started."""


# %% base new game

class NewGame(NewGameIf):
    """Default new game reset all variables."""

    def new_game(self, _1=None, _2=False):
        """Reset the game to new state and alternate start player."""

        self.game.store = [0, 0]
        self.game.board = [self.game.cts.nbr_start] * self.game.cts.dbl_holes
        self.game.init_bprops()

        self.game.turn = not self.game.starter
        self.game.starter = self.game.turn
        return True


# %%  decorators

class NewGamePattern(NewGameIf):
    """A new game that sets the fill pattern based on the pattern."""

    def __init__(self, game, pattern, decorator=None):

        super().__init__(game, decorator)
        self.pattern = pattern

    def __str__(self):
        """A recursive func to print the whole decorator chain."""

        my_str = repr(self) + '\n   ' + str(self.pattern)

        if self.decorator:
            return my_str + '\n' + str(self.decorator)
        return my_str          # pragma: no coverage

    def new_game(self, win_cond=None, new_round_ok=False):
        """Reset the game to new state and choose random start player."""

        self.decorator.new_game(win_cond, new_round_ok)
        self.pattern.fill_seeds(self.game)

        return True


class NewRound(NewGameIf):
    """Create a new round if allowed."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)
        self.collector = end_move.ClaimOwnSeeds(game)

        holes = self.game.cts.holes
        dbl_holes = self.game.cts.dbl_holes

        if self.game.info.round_fill == gi.RoundFill.RIGHT_FILL:
            self.fill_orders = [range(holes - 1, -1, -1),
                                range(dbl_holes - 1, holes - 1, -1)]

        elif self.game.info.round_fill == gi.RoundFill.LEFT_FILL:
            self.fill_orders = [range(holes), range(holes, dbl_holes)]

        elif self.game.info.round_fill == gi.RoundFill.SHORTEN:
            self.fill_orders = [range(holes),
                                range(dbl_holes - 1, holes - 1, -1)]

        elif self.game.info.round_fill in (gi.RoundFill.NOT_APPLICABLE,
                                           gi.RoundFill.OUTSIDE_FILL,
                                           gi.RoundFill.UCHOOSE,
                                           gi.RoundFill.UMOVE):
            self.fill_orders = [self.game.cts.false_fill,
                                self.game.cts.true_fill]

        else:
            raise NotImplementedError(
                    f"RoundFill {game.info.round_fill} not implemented.")



    def _compute_fills(self):
        """Detemine how many holes to fill on each side and
        adjust the store to hold the remaining seeds.
        If SHORTEN, both sides are filled the same based on the
        number of seeds the loser has."""

        fill = [0, 0]
        seeds = self.collector.claim_seeds()

        nbr_start = self.game.cts.nbr_start
        holes = self.game.cts.holes

        if self.game.info.round_fill == gi.RoundFill.SHORTEN:

            loser = 0 if seeds[0] < seeds[1] else 1
            quot = seeds[loser] // nbr_start
            fill[0] = fill[1] = min(quot, holes)

            self.game.store[0] = seeds[0] - fill[0] * nbr_start
            self.game.store[1] = seeds[1] - fill[1] * nbr_start

        else:
            for store in (False, True):
                quot = seeds[store] // nbr_start
                fill[store] = min(quot, holes)
                self.game.store[store] = \
                    seeds[store] - fill[store] * nbr_start

        return fill


    def new_game(self, win_cond=None, new_round_ok=False):
        """Create a new round if allowed.
        Use pre-determine pattern to distribute the seeds for the
        next round.

        If the board size is 4 or move and the fill method is SHORTEN,
        stop making children if the playable board size
        is reduced to 3 or less.

        Return False if it a new round was started.
        True if a new game was started."""

        if (not new_round_ok
                or win_cond in (gi.WinCond.WIN, gi.WinCond.TIE)):
            self.decorator.new_game(win_cond, new_round_ok)
            return True

        nbr_start = self.game.cts.nbr_start
        blocks = self.game.info.blocks
        fill = self._compute_fills()

        set_round_starter(self.game)
        self.game.init_bprops()

        if (self.game.cts.holes > 3
                and self.game.info.round_fill == gi.RoundFill.SHORTEN):
            self.game.inhibitor.set_child(fill[0] <= 3)

        for store, brange in enumerate(self.fill_orders):
            for cnt, loc in enumerate(brange):
                if cnt < fill[store]:
                    self.game.board[loc] = nbr_start
                else:
                    self.game.board[loc] = 0
                    if blocks:
                        self.game.blocked[loc] = True
        return False


class TerritoryNewRound(NewGameIf):
    """If the game is over, call chained decorator.
    Otherwise, start a new round, compute the holes owned by false;
    initialize the board, store and properties; and
    assign the owners."""

    def new_game(self, win_cond=None, new_round_ok=False):
        """Adjust the game outcome."""

        if (not new_round_ok
                or win_cond in (gi.WinCond.WIN, gi.WinCond.TIE)):
            self.decorator.new_game(win_cond, new_round_ok)
            return True

        winner, wholes = self.game.compute_win_holes()
        if winner is None:
            winner = True  # tie round, either will do
        set_round_starter(self.game)

        self.game.store = [0, 0]
        self.game.board = [self.game.cts.nbr_start] * self.game.cts.dbl_holes
        self.game.init_bprops()

        loc = self.game.cts.holes if winner else 0
        direct = 1
        # loc = self.game.cts.holes - 1 if winner else \
        #     self.game.cts.dbl_holes - 1
        # direct = -1

        for cnt in range(self.game.cts.dbl_holes):
            self.game.owner[loc] = winner if cnt < wholes else not winner
            loc = (loc + direct) % self.game.cts.dbl_holes

        return False


class NewRoundEven(NewGameIf):
    """Evenly distribute the seeds based on the losers seeds.
    Leave the two sides of the board symetrical.

    If none of the holes have sufficient seeds for a minimum move,
    move the number of extra seeds that the loser has into leftmost
    holes for valid moves, adjusting the store appropriately."""

    def new_game(self, win_cond=None, new_round_ok=False):
        """Adjust the game outcome."""

        if (not new_round_ok
            or win_cond in (gi.WinCond.WIN, gi.WinCond.TIE)):
            self.decorator.new_game(win_cond, new_round_ok)
            return True

        winner = self.game.turn
        set_round_starter(self.game)
        self.game.init_bprops()

        cts = self.game.cts
        min_move = self.game.info.min_move

        loser_seeds = self.game.store[not winner] + \
            sum(self.game.board[loc] for loc in cts.get_my_range(not winner))

        seeds_per_hole = (loser_seeds - min_move) // (cts.holes - 1)
        seeds_per_side = seeds_per_hole * cts.holes

        l_store = loser_seeds - seeds_per_side
        w_store = cts.total_seeds - loser_seeds - seeds_per_side
        if winner:
            self.game.store = [l_store, w_store]
        else:
            self.game.store = [w_store, l_store]
        self.game.board = [seeds_per_hole] * self.game.cts.dbl_holes

        if seeds_per_hole < min_move:

            loser_extra = self.game.store[not winner]
            self.game.board[0] += loser_extra
            self.game.board[cts.holes] += loser_extra

            self.game.store[0] -= loser_extra
            self.game.store[1] -= loser_extra

            game_log.add('Adjusted seeds for minimum move.', game_log.IMPORT)
            assert sum(self.game.store) + sum(self.game.board) \
                == self.game.cts.total_seeds, \
                    'seed count error in new_game, adj for min move'

        return False


# %%

def deco_new_game(game):
    """Create the new_game chain."""

    new_game = NewGame(game)

    if game.info.start_pattern:
        return NewGamePattern(game,
                              PCLASSES[game.info.start_pattern],
                              new_game)

    if game.info.rounds:
        if game.info.goal == gi.Goal.TERRITORY:
            new_game = TerritoryNewRound(game, new_game)

        elif game.info.round_fill in (gi.RoundFill.EVEN_FILL,
                                      gi.RoundFill.UMOVE):
            new_game = NewRoundEven(game, new_game)

        else:
            new_game = NewRound(game, new_game)

        # catch an error in round starter at construction time
        if game.info.round_starter not in (gi.RoundStarter.ALTERNATE,
                                           gi.RoundStarter.LOSER,
                                           gi.RoundStarter.WINNER,
                                           gi.RoundStarter.LAST_MOVER):
            raise NotImplementedError(
                    f"RoundStarter {game.info.round_starter} not implemented.")

    return new_game
