# -*- coding: utf-8 -*-
"""Create a new game or round.

Created on Fri Apr  7 12:47:15 2023
@author: Ann"""


# %% imports

import abc
import random

import end_move
from game_interface import WinCond
from game_interface import RoundStarter


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

    def init_bprops(self):
        """Initialize the board properties
        but not the board or stores."""

        dbl_holes = self.game.cts.dbl_holes
        locks = not self.game.info.flags.moveunlock
        self.game.unlocked = [locks] * dbl_holes
        self.game.blocked = [False] * dbl_holes
        self.game.child = [None] * dbl_holes



# %% base new game

class NewGame(NewGameIf):
    """Default new game reset all variables."""

    def new_game(self, _1=None, _2=False):
        """Reset the game to new state and choose random start player."""

        self.game.store = [0, 0]
        self.game.board = [self.game.cts.nbr_start] * self.game.cts.dbl_holes
        self.init_bprops()

        self.game.turn = random.choice([False, True])
        self.game.starter = self.game.turn
        return True


# %%  decorators

class NewRound(NewGameIf):
    """Create a new round if allowed."""

    def set_starter(self):
        """Set the starter of the next round based on the game flag."""

        match self.game.info.flags.round_starter:
            case RoundStarter.ALTERNATE:
                self.game.turn = not self.game.starter

            case RoundStarter.LOSER:
                self.game.turn = not self.game.turn

            # case RoundStarter.WINNER:
            #     pass

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
        blocks = self.game.info.flags.blocks
        seeds = self.collector.claim_seeds()

        self.set_starter()
        self.init_bprops()

        if self.game.info.flags.rnd_left_fill:
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


# %%

def deco_new_game(game):
    """Create the new_game chain."""

    new_game = NewGame(game)

    if game.info.flags.rounds:
        new_game = NewRound(game, new_game, end_move.TakeOwnSeeds(game))

    return new_game
