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
from game_interface import RoundStarter
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

    def set_starter(self):
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

        self.set_starter()
        self.game.init_bprops()

        if self.game.info.rnd_left_fill:
            orders = [range(holes), range(holes, self.game.cts.dbl_holes)]
        else:
            orders = [self.game.cts.false_fill, self.game.cts.true_fill]

        for store, brange in enumerate(orders):

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

    return new_game
