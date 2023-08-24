# -*- coding: utf-8 -*-
"""Create a new game or round.

Created on Fri Apr  7 12:47:15 2023
@author: Ann"""


# %% imports

import abc
import random

import end_move
from game_interface import WinCond


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

        self.game.board = [self.game.cts.nbr_start] * self.game.cts.dbl_holes
        locks = not self.game.info.flags.moveunlock
        self.game.unlocked = [locks] * self.game.cts.dbl_holes
        self.game.blocked = [False] * self.game.cts.dbl_holes
        self.game.child = [None] * self.game.cts.dbl_holes

        self.game.store = [0, 0]
        self.game.turn = random.choice([False, True])
        self.game.starter = self.game.turn
        return True


# %%  decorators

class NewRound(NewGameIf):
    """Create a new round if allowed."""

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
        seeds = self.collector.claim_seeds()

        self.game.turn = not self.game.starter
        self.game.starter = self.game.turn

        locks = not self.game.info.flags.moveunlock
        self.game.unlocked = [locks] * self.game.cts.dbl_holes
        self.game.blocked = [False] * self.game.cts.dbl_holes
        self.game.child = [None] * self.game.cts.dbl_holes

        for store, brange in enumerate([self.game.cts.false_fill,
                                        self.game.cts.true_fill]):

            quot, rem = divmod(seeds[store], nbr_start)
            fill = min(quot, self.game.cts.holes)

            self.game.store[store] = \
                rem + (quot - fill) * nbr_start

            for cnt, pos in enumerate(brange):
                if cnt < fill:
                    self.game.board[pos] = nbr_start
                else:
                    self.game.board[pos] = 0
                    self.game.blocked[pos] = True
        return False


# %%

def deco_new_game(game):
    """Create the new_game chain."""

    new_game = NewGame(game)

    if game.info.flags.rounds:
        new_game = NewRound(game, new_game, end_move.TakeOwnSeeds(game))

    return new_game
