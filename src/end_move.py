# -*- coding: utf-8 -*-
"""There are two  deco chains defined here:
    1. ender:  at the end of each turn determine if the game is over.
    2. quitter:  user ended the game, do something fair.

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

from game_log import game_log
from game_interface import Goal
from game_interface import ChildType
from game_interface import RoundFill
from game_interface import WinCond


# %% claim seeds

# Naming convensions:

#  Claim_*:    don't move any seeds, but count them
#  Take_*:     move/remove unclaimed seeds, but don't move child seeds
#  Divvy_*:    the game is over, do something fair with unclaimed seeds


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
    """Claim seeds in stores, any owned childrens, and
    own side of the board.  Don't move any."""

    def claim_seeds(self):
        seeds = self.game.store.copy()

        for side, side_range in enumerate([self.game.cts.false_range,
                                           self.game.cts.true_range]):
            for loc in side_range:
                if self.game.child[loc] is True:
                    seeds[True] += self.game.board[loc]
                elif self.game.child[loc] is False:
                    seeds[False] += self.game.board[loc]
                else:
                    seeds[side] += self.game.board[loc]

        return seeds


class TakeOwnSeeds(ClaimSeedsIf):
    """The game has ended, move the unowned seeds (non-child)
    to the stores.  Count all of the owned seeds."""

    def __init__(self, game, owner_func):
        super().__init__(game)
        self.owner = owner_func

    def claim_seeds(self):
        seeds = [0, 0]

        for loc in range(self.game.cts.dbl_holes):

            if self.game.child[loc] is True:
                seeds[True] += self.game.board[loc]

            elif self.game.child[loc] is False:
                seeds[False] += self.game.board[loc]

            else:
                self.game.store[self.owner(loc)] += self.game.board[loc]
                self.game.board[loc] = 0

        seeds[False] += self.game.store[False]
        seeds[True] += self.game.store[True]

        game_log.step('Collected seeds', self.game)
        return seeds


class TakeOnlyChildNStores(ClaimSeedsIf):
    """Ignore unclaimed seeds; count stores and children

    Duplicated code from DivvySeedsStores, can this be consolidated?"""

    def claim_seeds(self):

        seeds = self.game.store.copy()

        for loc in range(self.game.cts.dbl_holes):

            if self.game.child[loc] is True:
                seeds[True] += self.game.board[loc]

            elif self.game.child[loc] is False:
                seeds[False] += self.game.board[loc]

            else:
                # XXXX is removing unclaimed seeds right for game play?
                # the game is over so we don't need preserve seed count
                self.game.board[loc] = 0

        game_log.step('Divvied seeds', self.game)
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

        game_log.step('Divvied seeds', self.game)
        return seeds


class DivvySeedsNoStores(ClaimSeedsIf):
    """When there are no stores, split the unclaimed seeds
    between the two players putting them in available
    children.
    Return the count of seeds owned by each player.
    If there are no owned stores, return win_count's
    to force a tie."""

    def claim_seeds(self):

        board = self.game.board
        seeds = [0, 0]
        unclaimed = 0
        children = [-1, -1]

        for loc in range(self.game.cts.dbl_holes):
            owner = self.game.child[loc]
            if owner is None:
                unclaimed += board[loc]
                board[loc] = 0
            else:
                seeds[owner] += board[loc]
                children[owner] = loc

        if all(children[i] >= 0 for i in range(2)):

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
            game_log.step('Divvied seeds', self.game)
            return seeds

        game_log.step('Divvy forcing tie', self.game)
        half = self.game.cts.win_count
        return [half, half]


class DivvyIgnoreSeeds(ClaimSeedsIf):
    """If there are no stores or children, ignore
    any seeds still in play.
    Return win_count to force a tie."""

    def claim_seeds(self):
        half = self.game.cts.win_count
        return [half, half]



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
    game will end via the test_seed_cnts (unless ...).

    At the bottom of deco chain in a game which does not
    end the game via test_seed_cnts, return GAME_OVER.
    A deco higher in the chain, must translate to an actual
    game result and winner. In this case we do want to call
    the claimer to collect the seeds."""

    def game_ended(self, repeat_turn, ended=False):

        if ended and self.decorator:
            return self.decorator.game_ended(repeat_turn, ended)

        if not ended and not self.decorator:
            return None, self.game.turn

        cond, winner = self.test_seed_cnts(self.claimer.claim_seeds())
        if cond:
            return cond, winner

        if ended and not self.decorator:
            return WinCond.GAME_OVER, None

        return self.decorator.game_ended(repeat_turn, False)


class MaxWinner(EndTurnIf):
    """In some games not all seeds count towards the win,
    i.e. the game is over but neither player will have
    win_count seeds. The player with the max seeds wins.

    This should only be used to wrap Winner with a seed
    taker; the same claimer is used here."""

    def game_ended(self, repeat_turn, ended=False):

        cond, winner = self.decorator.game_ended(repeat_turn, ended)

        if cond != WinCond.GAME_OVER:
            return cond, winner

        seeds = self.decorator.claimer.claim_seeds()

        if seeds[0] > seeds[1]:
            return WinCond.WIN, False

        if seeds[0] < seeds[1]:
            return WinCond.WIN, True

        return WinCond.TIE, None


class RoundWinner(EndTurnIf):
    """"If the game is played in rounds, let the rest of the
    chain decide the outcome, then adjust for end of game or
    end of round. The game is over if either player does not
    have the minimum seeds to continue the game.

    For UMOVE / Giuthi rules contradict: game doesn't end
    until <= 4 seeds for loser, but in rearrangement rules all
    holes must contain a seed. Also, the winner's side is
    setup reversed of loser's side, so both players
    must have enough seeds for a valid move. Therefore, the
    game will end when there are not enough seeds for loser
    to have a valid move.

    This is near the top of the deco chain. If ended is True
    actually end the game (not the round)."""

    def __init__(self, game, decorator=None, claimer=None):

        super().__init__(game, decorator, claimer)

        if game.info.round_fill == RoundFill.UMOVE:
            self.req_seeds = game.cts.holes + game.info.min_move - 1
            self.msg = "Game, not round, ended (too few seeds for valid move)."

        else:
            self.req_seeds = game.cts.nbr_start
            self.msg = "Game, not round, ended (too few seeds to fill a hole)."


    def game_ended(self, repeat_turn, ended=False):

        cond, player = self.decorator.game_ended(repeat_turn, ended)

        if not cond or cond == WinCond.GAME_OVER or ended:
            return cond, player

        seeds = self.claimer.claim_seeds()
        if seeds[True] < self.req_seeds or seeds[False] < self.req_seeds:
            game_log.add(self.msg, game_log.INFO)
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

    def __init__(self, game, owner_func, decorator=None):
        super().__init__(game, decorator)
        self.owner = owner_func

    def game_ended(self, repeat_turn, ended=False):

        if ended:
            return self.decorator.game_ended(repeat_turn, ended)

        opponent = not self.game.turn if repeat_turn else self.game.turn

        player_seeds = opp_seeds = False
        for loc in range(self.game.cts.dbl_holes):

            if (self.game.board[loc] >= self.game.info.min_move
                    and self.game.child[loc] is None):

                if self.owner(loc) == opponent:
                    opp_seeds = True
                else:
                    player_seeds = True
                    break

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


class WaldaEndMove(EndTurnIf):
    """The rest of the deco chain may collect seeds into
    the stores (if the game has ended). Move any seeds
    from the stores into available waldas.

    Note that this code is only used if mustpass False."""

    @staticmethod
    def _find_waldas(game):
        """Find and return a walda for each side, if one exists."""

        walda_locs = [-1, -1]
        for side in (False, True):
            for walda in range(game.cts.dbl_holes):
                if game.child[walda] == side:
                    walda_locs[int(side)] = walda
                    break

        return walda_locs

    def game_ended(self, repeat_turn, ended=False):
        """Walda end move wrapper."""

        end_cond, winner = self.decorator.game_ended(repeat_turn, ended)

        if any(self.game.store):
            walda_locs = self._find_waldas(self.game)

            if all(loc >= 0 for loc in walda_locs):
                self.game.board[walda_locs[0]] += self.game.store[0]
                self.game.board[walda_locs[1]] += self.game.store[1]

            elif walda_locs[0] >= 0:
                self.game.board[walda_locs[0]] += sum(self.game.store)

            elif walda_locs[1] >= 0:
                self.game.board[walda_locs[1]] += sum(self.game.store)

            else:    # end_cond == WinCond.WIN:
                loc = self.game.cts.holes if winner else 0
                self.game.board[loc] += sum(self.game.store)

            self.game.store = [0, 0]

        assert sum(self.game.board) == self.game.cts.total_seeds, \
            'Walda: seeds missing from board.'

        return end_cond, winner


class DepriveSeedsEndGame(EndTurnIf):
    """Determine if either player has been deprived of seeds.
    This is not used with stores or children."""

    def game_ended(self, repeat_turn, ended=False):
        """Check for end game."""

        if all(self.game.board[loc] < self.game.info.min_move
               for loc in self.game.cts.get_opp_range(self.game.turn)):
            return WinCond.WIN, self.game.turn

        if all(self.game.board[loc] < self.game.info.min_move
               for loc in self.game.cts.get_my_range(self.game.turn)):
            return WinCond.WIN, not self.game.turn

        return None, None



class TerritoryRoundGameWinner(EndTurnIf):
    """When there are fewer than nbr_start seeds on the board,
    give the remaining seeds to the current player
    (they just did the last possible capture).
    Determine if there is a game winner by territory (gparam_one)
    or compare the seeds to determine a round winner.
    Otherwise call the deco chain; we need EndTurnMustShare and/or
    EndTurnNoPass to decide if the game has ended.
    Note that win_count is patched so Winner will not end the game."""

    def _compare_seed_cnts(self, seeds):
        """All of the seeds have been collected and the
        game is not over, determine the round outcome."""

        if seeds[True] > seeds[False]:
            return WinCond.ROUND_WIN, True

        if seeds[False] > seeds[True]:
            return WinCond.ROUND_WIN, False

        return WinCond.ROUND_TIE, self.game.turn


    def _test_winner(self):
        """Winner check is done before and after the rest of the
        deco chain, don't duplicate the code."""

        tot_holes = self.game.cts.dbl_holes
        gparam_one = self.game.info.gparam_one

        self.game.board = [0] * tot_holes

        false_holes = self.game.compute_owners()

        if false_holes >= gparam_one:
            return WinCond.WIN, False
        if tot_holes - false_holes >= gparam_one:
            return WinCond.WIN, True

        return None, None


    def _test_end_game(self):
        """The game is over, determine if there is an outright
        winner or a round winner."""

        cond, winner = self._test_winner()
        if cond:
            return cond, winner

        return self._compare_seed_cnts(self.game.store)


    def game_ended(self, repeat_turn, ended=False):
        """Determine if the game ended."""

        remaining = sum(self.game.board)
        if remaining <= self.game.cts.nbr_start:
            game_log.add(
                f'Too few seeds, remaining going to {self.game.turn}.',
                game_log.INFO)
            self.game.store[self.game.turn] += remaining

            return self._test_end_game()

        cond, winner = self.decorator.game_ended(repeat_turn, ended)

        if cond == WinCond.GAME_OVER:
            return self._test_end_game()

        return cond, winner



# %% build decorator chains


def deco_add_bottom_winner(game):
    """Start the deco chain by adding the bottom Winner
    and MaxWinner (if needed)."""

    if game.info.no_sides:
        ender = Winner(game, claimer=TakeOnlyChildNStores(game))

    elif game.info.goal == Goal.TERRITORY:
        ender = Winner(game,
                       claimer=TakeOwnSeeds(game, lambda loc: game.owner[loc]))
    else:
        ender = Winner(game, claimer=TakeOwnSeeds(game, game.cts.board_side))

    if game.info.goal == Goal.MAX_SEEDS:
        ender = MaxWinner(game, ender)

    return ender


def deco_end_move(game):
    """Return a chain of move enders."""

    if game.info.goal == Goal.DEPRIVE:
        return DepriveSeedsEndGame(game)

    if game.info.child_cvt:
        claimer = ChildClaimSeeds(game)
    else:
        claimer = ClaimSeeds(game)

    ender = deco_add_bottom_winner(game)

    if not game.info.mustpass:
        ender = EndTurnNoPass(game, ender)

    if game.info.mustshare:
        if game.info.goal == Goal.TERRITORY:
            ender = EndTurnMustShare(game, lambda loc: game.owner[loc], ender)
        else:
            ender = EndTurnMustShare(game, game.cts.board_side, ender)

    ender = EndTurnNotPlayable(game, ender)
    ender = Winner(game, ender, claimer)

    if game.info.rounds:
        ender = RoundWinner(game, ender, ClaimOwnSeeds(game))

    if game.info.child_type == ChildType.WALDA:
        ender = WaldaEndMove(game, ender)

    if game.info.goal == Goal.TERRITORY:
        ender = TerritoryRoundGameWinner(game, ender)

    return ender


def deco_quitter(game):
    """Return a chain for the quitter (user ended game).

    When no_sides: include MaxWinner because, CountOnlySeedsStores
    might move seeds off the board."""

    if game.info.no_sides:
        return MaxWinner(game,
                         Winner(game, claimer=TakeOnlyChildNStores(game)))

    if game.info.stores:
        return Winner(game, claimer=DivvySeedsStores(game))

    if game.info.child_cvt:
        return Winner(game, claimer=DivvySeedsNoStores(game))

    return Winner(game, claimer=DivvyIgnoreSeeds(game))
