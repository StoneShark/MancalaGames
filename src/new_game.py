# -*- coding: utf-8 -*-
"""Create a new game or round.

Created on Fri Apr  7 12:47:15 2023
@author: Ann"""


# %% imports

import abc
import random

import end_move

from game_interface import Goal
from game_interface import WinCond
from game_interface import RoundFill
from game_interface import RoundStarter
from game_log import game_log
from fill_patterns import PCLASSES

# %%  New Game interace

class NewGameIf(abc.ABC):
    """New Game Interface."""

    def __init__(self, game, decorator=None, collector=None):
        self.game = game
        self.decorator = decorator
        self.collector = collector

    @abc.abstractmethod
    def new_game(self, win_cond=None, new_round_ok=False):
        """collect seeds when game ended.

        Return False if it a new round was started.
        True if a new game was started."""



# %% base new game

class NewGame(NewGameIf):
    """Default new game reset all variables."""

    def new_game(self, _1=None, _2=False):
        """Reset the game to new state and choose random start player."""

        self.game.store = [0, 0]
        self.game.board = [self.game.cts.nbr_start] * self.game.cts.dbl_holes
        self.game.init_bprops()

        self.game.turn = random.choice([False, True])
        self.game.starter = self.game.turn
        return True


# %%  decorators

class NewGamePattern(NewGameIf):
    """A new game that sets the fill pattern based on the pattern."""

    def __init__(self, game, pattern, decorator=None, collector=None):

        super().__init__(game, decorator, collector)
        self.pattern = pattern


    def new_game(self, win_cond=None, new_round_ok=False):
        """Reset the game to new state and choose random start player."""

        self.decorator.new_game(win_cond, new_round_ok)
        self.pattern.fill_seeds(self.game)

        return True


class NewRound(NewGameIf):
    """Create a new round if allowed."""

    def __init__(self, game, decorator=None, collector=None):

        super().__init__(game, decorator, collector)

        holes = self.game.cts.holes
        dbl_holes = self.game.cts.dbl_holes

        if self.game.info.round_fill == RoundFill.RIGHT_FILL:
            self.fill_orders = [range(holes - 1, -1, -1),
                                range(dbl_holes - 1, holes, -1)]

        elif self.game.info.round_fill == RoundFill.LEFT_FILL:
            self.fill_orders = [range(holes), range(holes, dbl_holes)]

        else:   # RoundFill.OUTSIDE_FILL or user action
            self.fill_orders = [self.game.cts.false_fill,
                                self.game.cts.true_fill]


    def _set_starter(self):
        """Set the starter of the next round based on the game flag."""

        match self.game.info.round_starter:
            case RoundStarter.ALTERNATE:
                self.game.turn = not self.game.starter

            case RoundStarter.LOSER:
                self.game.turn = not self.game.turn

        self.game.starter = self.game.turn


    def new_game(self, win_cond=None, new_round_ok=False):
        """Create a new round if allowed.
        Use pre-determine pattern to distribute the seeds for the
        next round.
        Return False if it a new round was started.
        True if a new game was started."""

        if not new_round_ok or win_cond in (WinCond.WIN, WinCond.TIE, None):
            self.decorator.new_game(win_cond, new_round_ok)
            return True

        nbr_start = self.game.cts.nbr_start
        holes = self.game.cts.holes
        blocks = self.game.info.blocks
        seeds = self.collector.claim_seeds()

        self._set_starter()
        self.game.init_bprops()

        for store, brange in enumerate(self.fill_orders):

            quot, rem = divmod(seeds[store], nbr_start)
            fill = min(quot, holes)

            self.game.store[store] = rem + (quot - fill) * nbr_start

            for cnt, pos in enumerate(brange):
                if cnt < fill:
                    self.game.board[pos] = nbr_start
                else:
                    self.game.board[pos] = 0
                    if blocks:
                        self.game.blocked[pos] = True
        return False


class TerritoryNewRound(NewGameIf):
    """Wrap the existing NewGame deco chain.
    If the chain created a new game, reset the owners.
    If the chain created a new round, empty the stores,
    unblock all the holes, put the start seeds into each hole,
    and set the owners."""

    def new_game(self, win_cond=None, new_round_ok=False):
        """Adjust the game outcome."""

        nbr_start = self.game.cts.nbr_start
        false_holes = self.game.compute_owners()
        winner = self.game.turn

        if self.decorator.new_game(win_cond, new_round_ok):
            holes = self.game.cts.holes
            self.game.owner = [False] * holes + [True] * holes
            return True

        self.game.store = [0, 0]
        self.game.blocked = [False] * self.game.cts.dbl_holes

        loc = self.game.cts.holes if winner else 0
        wholes = self.game.cts.dbl_holes - false_holes if winner \
            else false_holes

        for cnt in range(self.game.cts.dbl_holes):

            self.game.board[loc] = nbr_start
            self.game.owner[loc] = winner if cnt < wholes else not winner

            loc = (loc + 1) % self.game.cts.dbl_holes

        return False


class UChooseNewRound(NewGameIf):
    """Wrap the existing NewGame deco chain.
    If the chain created a new game, do nothing else.
    If the chain created a new round, unblock all the holes,
    evenly distribute loser seeds (do same for winner),
    and set the stores.

    If none of the holes have sufficient seeds for a minimum move,
    move enough seeds into rightmost holes for a valid move,
    adjusting the store appropriately."""

    def new_game(self, win_cond=None, new_round_ok=False):
        """Adjust the game outcome."""

        winner = self.game.turn
        if self.decorator.new_game(win_cond, new_round_ok):
            return True

        cts = self.game.cts
        self.game.blocked = [False] * cts.dbl_holes

        loser_seeds = self.game.store[not winner] + \
            sum(self.game.board[loc] for loc in cts.get_my_range(not winner))

        seeds_per_hole = loser_seeds // cts.holes
        seeds_per_side = seeds_per_hole * cts.holes

        self.game.store = [loser_seeds - seeds_per_side,
                           cts.total_seeds - loser_seeds - seeds_per_side]

        for loc in range(cts.dbl_holes):
            self.game.board[loc] = seeds_per_hole

        min_move = self.game.info.min_move
        if seeds_per_hole < min_move:
            game_log.add('Adjusting seeds for minimum move.', game_log.IMPORT)

            self.game.board[0] = min_move
            self.game.store[0] -= min_move - 1

            self.game.board[cts.holes] = min_move
            self.game.board[1] -= min_move - 1

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
        if game.info.goal == Goal.TERRITORY:
            new_game = NewRound(
                game, new_game,
                end_move.TakeOwnSeeds(game, lambda loc: game.owner[loc]))

        else:
            new_game = NewRound(
                game, new_game,
                end_move.TakeOwnSeeds(game, game.cts.board_side))

    if game.info.goal == Goal.TERRITORY:
        new_game = TerritoryNewRound(game, new_game)

    elif game.info.round_fill == RoundFill.UMOVE:
        new_game = UChooseNewRound(game, new_game)

    return new_game
