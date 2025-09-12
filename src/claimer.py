# -*- coding: utf-8 -*-
"""Define the claimers, takers and divviers used by the enders.

Claimers can always use the stores:

    1. If the game is configured without stores but with children
       then ChildNoStoresEnder, will move the seeds back to
       the board.

    2. If it's a clear or deprive game (no stores and no children),
       claimers are not used in the enders.

    3. Other games without stores or children are dumb.


Naming convensions:

    Claim_*:    don't move any seeds, but count them
    Take_*:     move/remove unclaimed seeds, but don't move child seeds
    Divvy_*:    the game is over, do something fair with unclaimed seeds

Created on Sun Nov 10 07:22:16 2024
@author: Ann"""


# %%  imports

import abc

import game_info as gi

from game_logger import game_log


# %% claim seeds

class ClaimSeedsIf(abc.ABC):
    """Interface for seed claimer.
    This is not a decorator chain, one class must do all the work."""

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
    """Claim seeds in stores, any owned childrens, and
    owned holes.  Don't move any."""

    def claim_seeds(self):
        seeds = self.game.store.copy()

        for loc in range(self.game.cts.dbl_holes):
            if self.game.child[loc] is True:
                seeds[True] += self.game.board[loc]

            elif self.game.child[loc] is False:
                seeds[False] += self.game.board[loc]

            else:
                seeds[self.game.owner[loc]] += self.game.board[loc]

        return seeds


class ClaimBoardSeeds(ClaimSeedsIf):
    """Claim only the seeds on the board for each player.
    Use get ranges in case the ranges were set different than
    the two sides.  Don't move any seeds.

    Intendend for conceding eliminate goal games (e.g. clear).
    Not suitable for territory games or games with children."""

    def claim_seeds(self):
        seeds = [0, 0]

        frange, trange = self.game.cts.get_ranges(False)

        for loc in frange:
            seeds[False] += self.game.board[loc]

        for loc in trange:
            seeds[True] += self.game.board[loc]

        return seeds


class TakeOwnSeeds(ClaimSeedsIf):
    """The game has ended, move the unowned seeds (non-child)
    to the stores.  Count all of the owned seeds."""


    def claim_seeds(self):
        # seeds moved into stores, then added in later
        seeds = [0, 0]

        for loc in range(self.game.cts.dbl_holes):

            if self.game.child[loc] is True:
                seeds[True] += self.game.board[loc]

            elif self.game.child[loc] is False:
                seeds[False] += self.game.board[loc]

            elif self.game.child[loc] == gi.NO_CH_OWNER:
                pass

            else:
                self.game.store[self.game.owner[loc]] += self.game.board[loc]
                self.game.board[loc] = 0

        seeds[False] += self.game.store[False]
        seeds[True] += self.game.store[True]

        if seeds != self.game.store:
            game_log.step('Collected seeds', self.game)
        return seeds


class TakeOnlyChildNStores(ClaimSeedsIf):
    """Ignore unclaimed seeds; count stores and children.
    NoSides and DONT_SCORE use this."""

    def claim_seeds(self):

        seeds = self.game.store.copy()

        for loc in range(self.game.cts.dbl_holes):

            if self.game.child[loc] is True:
                seeds[True] += self.game.board[loc]

            elif self.game.child[loc] is False:
                seeds[False] += self.game.board[loc]

            elif self.game.child[loc] == gi.NO_CH_OWNER:
                pass

            else:
                self.game.board[loc] = 0

        if seeds != self.game.store:
            game_log.step('Take seeds', self.game)
        return seeds


class TakeAllUnclaimed(ClaimSeedsIf):
    """The game has ended, move the unowned seeds (non-child)
    to the stores.  Count all of the owned seeds."""

    def __init__(self, game):
        super().__init__(game)

        if game.info.unclaimed == gi.EndGameSeeds.LAST_MOVER:
            self.collector = lambda tgame: tgame.mdata.player

        elif game.info.unclaimed == gi.EndGameSeeds.UNFED_PLAYER:
            # make certain turn is set properly before call
            self.collector = lambda tgame: tgame.turn

        else:
            raise gi.GameInfoError(
                "Don't know who collector should be in TakeAllUnclaimedSeeds")

    def claim_seeds(self):
        # seeds moved into stores, then added in later
        seeds = [0, 0]
        collector = self.collector(self.game)

        for loc in range(self.game.cts.dbl_holes):

            if self.game.child[loc] is True:
                seeds[True] += self.game.board[loc]

            elif self.game.child[loc] is False:
                seeds[False] += self.game.board[loc]

            elif self.game.child[loc] == gi.NO_CH_OWNER:
                pass

            else:
                self.game.store[collector] += self.game.board[loc]
                self.game.board[loc] = 0

        seeds[False] += self.game.store[False]
        seeds[True] += self.game.store[True]

        if seeds != self.game.store:
            game_log.step(f'Take all seeds by {collector}', self.game)
        return seeds


class DivvySeedsStores(ClaimSeedsIf):
    """Split the unclaimed seeds between the two players
    putting them in their stores.
    Return the count of seeds owned by each player including
    those is in children (don't move those to the stores)."""

    def claim_seeds(self):

        seeds = [0, 0]
        unclaimed = 0

        for loc in range(self.game.cts.dbl_holes):

            if self.game.child[loc] is True:
                seeds[True] += self.game.board[loc]

            elif self.game.child[loc] is False:
                seeds[False] += self.game.board[loc]

            elif self.game.child[loc] == gi.NO_CH_OWNER:
                pass

            else:
                unclaimed += self.game.board[loc]
                self.game.board[loc] = 0

        quot, rem = divmod(unclaimed, 2)
        self.game.store[False] += quot
        self.game.store[True] += quot

        if self.game.store[True] > self.game.store[False]:
            self.game.store[False] += rem
        else:
            self.game.store[True] += rem

        seeds[False] += self.game.store[False]
        seeds[True] += self.game.store[True]

        if unclaimed:
            game_log.step('Divvied seeds to stores', self.game)
        return seeds


class DivvySeedsChildOnly(ClaimSeedsIf):
    """When there are no stores, split the unclaimed seeds
    between the two players putting them in available
    children.
    Return the count of seeds owned by each player.
    If there are no owned stores, return half the total seed
    to force a tie (win_count might not be half)."""

    def claim_seeds(self):

        board = self.game.board
        seeds = [0, 0]
        unclaimed = 0
        children = [-1, -1]

        for loc in range(self.game.cts.dbl_holes):
            ch_owner = self.game.child[loc]
            if ch_owner is None:
                unclaimed += board[loc]
                board[loc] = 0
            else:
                seeds[ch_owner] += board[loc]
                children[ch_owner] = loc

        if children[False] >= 0 and children[True] >= 0:
            quot, rem = divmod(unclaimed, 2)
            seeds[False] += quot
            seeds[True] += quot
            board[children[False]] += quot
            board[children[True]] += quot

            if seeds[True] > seeds[False]:
                seeds[False] += rem
                board[children[False]] += rem
            else:
                seeds[True] += rem
                board[children[True]] += rem

        elif children[False] >= 0:
            seeds[False] += unclaimed
            board[children[False]] += unclaimed

        elif children[True] >= 0:
            seeds[True] += unclaimed
            self.game.board[children[True]] += unclaimed

        if any(seeds):
            if unclaimed:
                game_log.step('Divvied seeds to children', self.game)
            return seeds

        game_log.step('Divvy forcing tie (no children)', self.game)
        half = self.game.cts.total_seeds // 2
        return [half, half]
