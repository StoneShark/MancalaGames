# -*- coding: utf-8 -*-
"""Create a new game or round.

Created on Fri Apr  7 12:47:15 2023
@author: Ann"""


# %% imports

import abc
import random


# %%  New Game interace

class NewGameIf(abc.ABC):
    """New Game Interface."""

    def __init__(self, game, decorator=None):
        self.game = game
        self.decorator = decorator

    @abc.abstractmethod
    def new_game(self, new_round_ok=False):
        """collect seeds when game ended"""


# %% base new game

class NewGame(NewGameIf):
    """Default new game reset all variables."""

    def new_game(self, _=False):
        """Reset the game to new state and choose random start player."""

        self.game.board = [self.game.cts.nbr_start] * self.game.cts.dbl_holes
        locks = not self.game.info.flags.moveunlock
        self.game.unlocked = [locks] * self.game.cts.dbl_holes
        self.game.blocked = [False] * self.game.cts.dbl_holes
        self.game.child = [None] * self.game.cts.dbl_holes

        self.game.store = [0, 0]
        self.game.turn = random.choice([False, True])
        self.game.starter = self.game.turn


# %%  decorators

class NewRound(NewGameIf):
    """Create a new round if allowed."""

    def new_game(self, new_round_ok=False):
        """Create a new round if allowed."""

        seeds = self.game.store[:]
        for loc in range(self.game.cts.dbl_holes):

            if self.game.child[loc] is True:
                seeds[True] += self.game.board[loc]

            elif self.game.child[loc] is False:
                seeds[False] += self.game.board[loc]

            elif loc < self.game.cts.holes:
                seeds[False] += self.game.board[loc]

            else:
                seeds[True] += self.game.board[loc]

        game_over = True
        if new_round_ok:

            game_over = seeds[True] < self.game.cts.nbr_start or \
                seeds[False] < self.game.cts.nbr_start

        if game_over:
            self.decorator.new_game()
            return

        self.game.turn = not self.game.starter
        self.game.starter = self.game.turn

        locks = not self.game.info.flags.moveunlock
        self.game.unlocked = [locks] * self.game.cts.dbl_holes
        self.game.blocked = [False] * self.game.cts.dbl_holes
        self.game.child = [None] * self.game.cts.dbl_holes

        for store, brange in enumerate([self.game.cts.false_fill,
                                        self.game.cts.true_fill]):

            quot, rem = divmod(seeds[store], self.game.cts.nbr_start)
            fill = min(quot, self.game.cts.holes)

            self.game.store[store] = \
                rem + (quot - fill) * self.game.cts.nbr_start

            for cnt, pos in enumerate(brange):
                if cnt < fill:
                    self.game.board[pos] = self.game.cts.nbr_start
                else:
                    self.game.board[pos] = 0
                    self.game.blocked[pos] = True


# %%

def deco_new_game(game):
    """Create the new_game chain."""

    new_game = NewGame(game)

    if game.info.flags.rounds:
        new_game = NewRound(game, new_game)

    return new_game
