# -*- coding: utf-8 -*-
"""Claim the seeds on each players side of the board.
Use the counts to determine if the game is over.

Base: if there are no seeds on the board the game is over,
claim the seeds.

Decorators: each decorator can decide to end the game early,
pass the end condition down the chain collection is done at the base
of the chain.

Created on Fri Apr  7 07:43:19 2023
@author: Ann"""

# %% imports

import abc

# %%  seed collector interface


class SeedCollIf(abc.ABC):
    """Interface for seed collection, not capture."""

    def __init__(self, game, decorator=None):
        self.game = game
        self.decorator = decorator

    @abc.abstractmethod
    def claim_own_seeds(self, repeat_turn, ended=False):
        """Claim own seeds.
        Return the number of seeds each player owns."""


# %% base collectors


class SeedCollector(SeedCollIf):
    """Base seed collector."""

    def claim_own_seeds(self, _, ended=False):
        """Claim own seeds.
        Return the number of seeds each player owns."""

        if not ended:
            playable = any(self.game.board[loc] >= self.game.info.min_move
                           for loc in range(self.game.cts.dbl_holes))

        if ended or not playable:

            for side, side_range in enumerate([self.game.cts.false_range,
                                               self.game.cts.true_range]):
                for loc in side_range:
                    self.game.store[side] += self.game.board[loc]
                    self.game.board[loc] = 0

        return self.game.store[False], self.game.store[True]


class ChildSeedCollector(SeedCollIf):
    """Base seed collector that handles child holes."""

    def claim_own_seeds(self, _, ended=False):
        """Claim own seeds.
        Return the number of seeds each player owns."""

        if not ended:
            playable = any(self.game.board[loc] >= self.game.info.min_move
                           and self.game.child[loc] is None
                           for loc in range(self.game.cts.dbl_holes))

        if ended or not playable:

            for side, side_range in enumerate([self.game.cts.false_range,
                                               self.game.cts.true_range]):
                for loc in side_range:
                    if self.game.child[loc] is None:
                        self.game.store[side] += self.game.board[loc]
                        self.game.board[loc] = 0

        store_f, store_t = self.game.store[False], self.game.store[True]

        for loc in range(self.game.cts.dbl_holes):
            if self.game.child[loc] is True:
                store_t += self.game.board[loc]
            elif self.game.child[loc] is False:
                store_f += self.game.board[loc]

        return store_f, store_t


# %% collector decorators

class SeedCollNoPass(SeedCollIf):
    """No Pass, end game if there are no seeds for the next player."""

    def claim_own_seeds(self, repeat_turn, ended=False):

        if ended:
            return self.decorator.claim_own_seeds(repeat_turn, ended)

        if repeat_turn:
            cont_game = any(self.game.board[loc] >= self.game.info.min_move
                            for loc in
                            self.game.cts.get_my_range(self.game.turn)
                            if self.game.child[loc] is None)
        else:
            cont_game = any(self.game.board[loc] >= self.game.info.min_move
                            for loc in
                            self.game.cts.get_opp_range(self.game.turn)
                            if self.game.child[loc] is None)

        return self.decorator.claim_own_seeds(repeat_turn,
                                              ended=not cont_game)


class SeedColMustShare(SeedCollIf):
    """collect seeds on end game"""

    def claim_own_seeds(self, repeat_turn, ended=False):
        """If opp player has no seeds and the current player cannot make
        any available, end the game."""

        if ended:
            return self.decorator.claim_own_seeds(repeat_turn, ended)

        if repeat_turn:
            opp_rng, my_rng = self.game.cts.get_ranges(self.game.turn)
        else:
            my_rng, opp_rng = self.game.cts.get_ranges(self.game.turn)

        my_sum = sum(self.game.board[loc]
                     for loc in my_rng
                     if self.game.child[loc] is None)
        opp_sum = sum(self.game.board[loc]
                      for loc in opp_rng
                      if self.game.child[loc] is None)

        if not my_sum and opp_sum > 0:

            self.game.turn = not self.game.turn
            poses = self.game.get_allowable_holes()
            self.game.turn = not self.game.turn

            return self.decorator.claim_own_seeds(repeat_turn,
                                                  ended=not any(poses))

        return self.decorator.claim_own_seeds(repeat_turn)


# %% build decorator chain


def deco_seed_collector(game):
    """Return a chain of seed_collector."""

    if game.info.flags.child:
        collector = ChildSeedCollector(game)
    else:
        collector = SeedCollector(game)

    if not game.info.flags.mustpass:
        collector = SeedCollNoPass(game, collector)

    if game.info.flags.mustshare:
        collector = SeedColMustShare(game, collector)

    return collector
