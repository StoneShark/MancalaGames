# -*- coding: utf-8 -*-
"""At the end of each turn determine if the game is over.

Return win/end-game-condition, winner from ender.game_ended.
self.game.turn is the player that just finished moving.

Process is as follows:
    0. RoundWinner defers to the rest of the chain
       (on returns it adjusts the outcome).
    1. Determine outright game winner or game tie
       via Winner.
    2. Check for end condition: not playable, mustshare, or
       cannot pass (not mustpass).
    3. If the game has ended, collect seeds and determine if
       round/game winner or round/game tie.

Winner is used in steps 1 and 3 of the deco chain with
a different seed claimer and follow-on decorator.

Log a step if anything is changed on the board, e.g. TakeOwnSeeds.

Created on Fri Apr  7 07:43:19 2023
@author: Ann"""

# %% imports

import abc

import game_log
from game_interface import WinCond


# %% claim seeds

class ClaimSeedsIf(abc.ABC):
    """Interface for seed claimer."""

    def __init__(self, game):
        self.game = game

    @abc.abstractmethod
    def claim_seeds(self):
        """Return the number seeds controlled by the each player."""


class ClaimSeeds(ClaimSeedsIf):
    """Only claim seeds in the stores."""

    def claim_seeds(self):
        return self.game.store


class ChildClaimSeeds(ClaimSeedsIf):
    """Claim the stores and any owned children."""

    def claim_seeds(self):
        seeds = self.game.store.copy()

        for loc in range(self.game.cts.dbl_holes):
            if self.game.child[loc] is True:
                seeds[True] += self.game.board[loc]
            elif self.game.child[loc] is False:
                seeds[False] += self.game.board[loc]

        return seeds


class ClaimOwnSeeds(ClaimSeedsIf):
    """The game has ended, count number of seeds each player
    controls--used to determine if the round is over.

    Count all of the owned seeds."""

    def claim_seeds(self):
        seeds = self.game.store.copy()

        for side, side_range in enumerate([self.game.cts.false_range,
                                           self.game.cts.true_range]):
            for loc in side_range:
                if self.game.child[loc] is None:
                    seeds[side] += self.game.board[loc]
                elif self.game.child[loc] is True:
                    seeds[True] += self.game.board[loc]
                elif self.game.child[loc] is False:
                    seeds[False] += self.game.board[loc]

        return seeds


# XXXX seed collection options:
#         all, own, opps (for XCaptSowOwn), even split (to intgrate end)

class TakeOwnSeeds(ClaimSeedsIf):
    """The game has ended, move the unowned seeds (non-child)
    to the stores.

    Count all of the owned seeds."""

    def claim_seeds(self):
        seeds = [0, 0]

        for side, side_range in enumerate([self.game.cts.false_range,
                                           self.game.cts.true_range]):
            for loc in side_range:
                if self.game.child[loc] is None:
                    self.game.store[side] += self.game.board[loc]
                    self.game.board[loc] = 0

                elif self.game.child[loc] is True:
                    seeds[True] += self.game.board[loc]
                elif self.game.child[loc] is False:
                    seeds[False] += self.game.board[loc]

        seeds[False] += self.game.store[False]
        seeds[True] += self.game.store[True]

        game_log.step('Collected seeds', self.game)

        return seeds


# %%  end turn interface

class EndTurnIf(abc.ABC):
    """Interface for determining if the game is over."""

    def __init__(self, game, decorator=None, claimer=None):
        self.game = game
        self.claimer = claimer
        self.decorator = decorator

    @abc.abstractmethod
    def game_ended(self, repeat_turn, ended=False):
        """Return the end condition and winner."""

    def test_seed_cnts(self, seeds):
        """Determine if seed counts result in an
        end game condition."""

        if seeds[True] > self.game.cts.win_count:
            return WinCond.WIN, True

        if seeds[False] > self.game.cts.win_count:
            return WinCond.WIN, False

        if (seeds[False] == self.game.cts.win_count
                and seeds[False] == seeds[True]):
            return WinCond.TIE, self.game.turn

        return None, self.game.turn


# %%

class Winner(EndTurnIf):
    """If either player has won based on seed count returned by
    the claimer, return the end game conditions.

    This needs to be able to run at the top and bottom of the
    deco chain. In both cases ended can be True or False.

    At the top (first/second), the decorator will exist and
    the claimer will be one of ClaimSeeds or ChildClaimSeeds.

    At the bottom of deco chain, the decorator will be None
    and the claimer will count all the seeds, therefore the
    game will end via the test_seed_cnts."""

    def game_ended(self, repeat_turn, ended=False):

        if ended and self.decorator:
            return self.decorator.game_ended(repeat_turn, ended)

        if not ended and not self.decorator:
            return None, self.game.turn

        cond, winner = self.test_seed_cnts(self.claimer.claim_seeds())
        if cond:
            return cond, winner

        return self.decorator.game_ended(repeat_turn, False)


class RoundWinner(EndTurnIf):
    """"If the game is played in rounds, let the rest of the
    chain decide the outcome, then adjust for end of game or
    end of round. The game is over if either player does not
    have the minimum seeds to fill a hole for the start of
    the game."""

    def game_ended(self, repeat_turn, ended=False):

        cond, player = self.decorator.game_ended(repeat_turn, ended)

        if not cond:
            return cond, player

        seeds = self.claimer.claim_seeds()
        if (seeds[True] < self.game.cts.nbr_start
                or seeds[False] < self.game.cts.nbr_start):
            game_log.add("Game, not round, ended.", game_log.INFO)
            return cond, player

        if cond == WinCond.WIN:
            return WinCond.ROUND_WIN, player

        # if cond == WinCond.TIE:
        return WinCond.ROUND_TIE, player


class EndTurnNoPass(EndTurnIf):
    """No Pass, end game if there are no seeds for the next player."""

    def game_ended(self, repeat_turn, ended=False):

        if ended:
            return self.decorator.game_ended(repeat_turn, ended)

        if repeat_turn:
            ended = not any(self.game.get_allowable_holes())
        else:
            self.game.turn = not self.game.turn
            ended = not any(self.game.get_allowable_holes())
            self.game.turn = not self.game.turn

        if ended:
            game_log.add("Next player can't pass, game ended.", game_log.INFO)

        return self.decorator.game_ended(repeat_turn, ended)


class EndTurnMustShare(EndTurnIf):
    """With MUSTSHARE, the game is over if
    the current player does not have seeds and the opponent
    cannot make any seeds available to the current player."""

    def game_ended(self, repeat_turn, ended=False):

        if ended:
            return self.decorator.game_ended(repeat_turn, ended)

        my_rng, opp_rng = self.game.cts.get_ranges(self.game.turn)
        if repeat_turn:
            opp_rng, my_rng = my_rng, opp_rng

        player_seeds = any(self.game.board[loc]
                           for loc in my_rng
                           if self.game.child[loc] is None)
        opp_seeds = any(self.game.board[loc]
                        for loc in opp_rng
                        if self.game.child[loc] is None)

        if not player_seeds and opp_seeds:
            self.game.turn = not self.game.turn
            ended = not any(self.game.get_allowable_holes())
            self.game.turn = not self.game.turn

            if ended:
                game_log.add("Next player can't share, game ended.",
                             game_log.INFO)

            return self.decorator.game_ended(repeat_turn, ended)
        return self.decorator.game_ended(repeat_turn, False)


class EndTurnNotPlayable(EndTurnIf):
    """If the game is no longer playable in any circustances,
    end it. Specifically, if none of the holes on the board
    have the minimum seeds required for a move, it's over."""

    def game_ended(self, repeat_turn, ended=False):

        if ended:
            return self.decorator.game_ended(repeat_turn, ended)

        ended = not any(self.game.board[loc] >= self.game.info.min_move
                        and self.game.child[loc] is None
                        for loc in range(self.game.cts.dbl_holes))

        if ended:
            game_log.add("No moves available, game ended.", game_log.INFO)

        return self.decorator.game_ended(repeat_turn, ended)


# %% build decorator chain

def deco_end_move(game):
    """Return a chain of move enders."""

    if game.info.flags.child:
        claimer = ChildClaimSeeds(game)
    else:
        claimer = ClaimSeeds(game)

    ender = Winner(game, None, TakeOwnSeeds(game))

    if not game.info.flags.mustpass:
        ender = EndTurnNoPass(game, ender, None)
    if game.info.flags.mustshare:
        ender = EndTurnMustShare(game, ender, None)
    ender = EndTurnNotPlayable(game, ender, None)

    ender = Winner(game, ender, claimer)

    if game.info.flags.rounds:
        ender = RoundWinner(game, ender, ClaimOwnSeeds(game))

    return ender