# -*- coding: utf-8 -*-
"""There are two  deco chains defined here:
    1. ender:  at the end of each turn determine if the game is over.
    2. quitter:  user ended the game or a sow resulted in ENDLESS,
    do something fair.

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

import deco_chain_if
import game_interface as gi

from game_log import game_log


# %% claim seeds

# Naming convensions:

#  Claim_*:    don't move any seeds, but count them
#  Take_*:     move/remove unclaimed seeds, but don't move child seeds
#  Divvy_*:    the game is over, do something fair with unclaimed seeds


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
        self.get_owner = owner_func

    def claim_seeds(self):
        seeds = [0, 0]

        for loc in range(self.game.cts.dbl_holes):

            if self.game.child[loc] is True:
                seeds[True] += self.game.board[loc]

            elif self.game.child[loc] is False:
                seeds[False] += self.game.board[loc]

            else:
                self.game.store[self.get_owner(loc)] += self.game.board[loc]
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


class DivvyIgnoreSeeds(ClaimSeedsIf):
    """For DEPRIVE games: If there are seeds on the board
    (which there are or the game would have ended),
    end the game in a TIE."""

    def claim_seeds(self):
        half = self.game.cts.total_seeds // 2
        return [half, half]


# %%  end turn interface

class EndTurnIf(deco_chain_if.DecoChainIf):
    """Interface for determining if the game is over."""

    def __init__(self, game, decorator=None, claimer=None):

        super().__init__(game, decorator)
        self.claimer = claimer

    def __str__(self):
        """A recursive func to print the whole decorator chain."""

        my_str = repr(self)
        if self.claimer:
            my_str += '\n   ' + repr(self.claimer)

        if self.decorator:
            return my_str + '\n' + str(self.decorator)
        return my_str

    @abc.abstractmethod
    def game_ended(self, repeat_turn, ended=False):
        """Return the end condition and winner."""

    def test_seed_cnts(self, seeds):
        """Determine if seed counts result in an
        end game condition."""

        if seeds[True] > self.game.cts.win_count:
            return gi.WinCond.WIN, True

        if seeds[False] > self.game.cts.win_count:
            return gi.WinCond.WIN, False

        if (seeds[False] == self.game.cts.win_count
                and seeds[False] == seeds[True]):
            return gi.WinCond.TIE, self.game.turn

        return None, self.game.turn


# %%

class Winner(EndTurnIf):
    """If either player has won based on seed count returned by
    the claimer, return the end game conditions.

    This needs to be able to run at the top and bottom of the
    deco chain. In both cases ended can be True or False.

    At the top (first/second), the decorator will exist and
    the claimer will be one of ClaimSeeds or ChildClaimSeeds.

    At the bottom of deco chain (called later), the decorator
    will be None and the claimer will count all the seeds,
    therefore the game will end via the test_seed_cnts
    (unless ...).

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
            return gi.WinCond.GAME_OVER, self.game.turn

        return self.decorator.game_ended(repeat_turn, False)


class MaxWinner(EndTurnIf):
    """In some games not all seeds count towards the win,
    i.e. the game is over but neither player will have
    win_count seeds. The player with the max seeds wins.

    This should only be used to wrap Winner with a seed
    taker; the same claimer is used here."""

    def game_ended(self, repeat_turn, ended=False):

        cond, winner = self.decorator.game_ended(repeat_turn, ended)

        if cond != gi.WinCond.GAME_OVER:
            return cond, winner

        seeds = self.decorator.claimer.claim_seeds()

        if seeds[0] > seeds[1]:
            return gi.WinCond.WIN, False

        if seeds[0] < seeds[1]:
            return gi.WinCond.WIN, True

        return gi.WinCond.TIE, self.game.turn


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
    game will end when there are not enough seeds for the loser
    to fill their side with a valid move.

    This is near the top of the deco chain. If ended is True
    actually end the game (not the round)."""

    def __init__(self, game, decorator=None, claimer=None):

        super().__init__(game, decorator, claimer)

        intro = 'Game, not round, ended '
        if game.info.round_fill == gi.RoundFill.UMOVE:
            self.req_seeds = game.cts.holes + game.info.min_move - 1
            self.msg = intro + "(too few seeds to fill side)."

        else:
            self.req_seeds = game.cts.nbr_start
            self.msg = intro + "(too few seeds to fill a hole)."


    def game_ended(self, repeat_turn, ended=False):

        cond, player = self.decorator.game_ended(repeat_turn, ended)

        if not cond or cond == gi.WinCond.GAME_OVER or ended:
            return cond, player

        seeds = self.claimer.claim_seeds()
        if seeds[True] < self.req_seeds or seeds[False] < self.req_seeds:
            game_log.add(self.msg, game_log.IMPORT)
            return cond, player

        if cond == gi.WinCond.WIN:
            return gi.WinCond.ROUND_WIN, player

        # if cond == WinCond.TIE:
        return gi.WinCond.ROUND_TIE, player


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
    cannot make any seeds available to the current player.

    If the game has ended or if we are going to go again (repeat turn--
    can't share seeds with self), delegate to the deco chain.
    Next do a scan to see if the current player is without seeds
    and the opponent has seeds -- don't bother to simulate if we
    don't need to.
    Finally, check to see if the opponent can share. If not,
    the game is over."""

    def __init__(self, game, owner_func, decorator=None):
        super().__init__(game, decorator)
        self.owner = owner_func

    def game_ended(self, repeat_turn, ended=False):

        if ended or repeat_turn:
            return self.decorator.game_ended(repeat_turn, ended)

        opponent = not self.game.turn
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
            no_share = not any(self.game.get_allowable_holes())
            self.game.turn = not self.game.turn

            if no_share:
                game_log.add("Next player can't share, game ended.",
                             game_log.INFO)
            return self.decorator.game_ended(repeat_turn, no_share)

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
            game_log.add("No moves available, game ended.", game_log.IMPORT)

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
            return gi.WinCond.WIN, self.game.turn

        if all(self.game.board[loc] < self.game.info.min_move
               for loc in self.game.cts.get_my_range(self.game.turn)):
            return gi.WinCond.WIN, not self.game.turn

        return None, self.game.turn



class TerritoryGameWinner(EndTurnIf):
    """If the game has already been determined to be ended,
    pick the winner:
        Rounds: if there is a game winner by territory (gparam_one)
    or compare the seeds to determine a round winner.
        No Rounds: determine soley based on territory > holes

    Otherwise call the deco chain; we need EndTurnMustShare and/or
    EndTurnNoPass to decide if the game has ended.

    If they decide the game is over, use the same criteria to
    determine the round winner.

    Note that win_count is patched so Winner will not end the game."""


    def __init__(self, game, decorator=None, claimer=None):

        super().__init__(game, decorator, claimer)
        self.min_occ = self._min_occupy(game)

        if game.info.rounds:
            self.winner_test = self._test_round_winner
        else:
            self.winner_test = self._test_winner

    @staticmethod
    def _min_occupy(game):
        """Select a minimum number of seeds that can claim
        or occupy more territory. Disable with min_occ of -1,
        if this feature shouldn't be used (sow_own_store)."""

        if game.info.sow_own_store:
            return -1

        if game.info.child_type:
            min_occ = game.info.child_cvt
        else:
            min_occ = game.cts.total_seeds  # max possible and flag

        if (game.info.evens
                or game.info.capt_next
                or game.info.capttwoout
                or game.info.crosscapt):
            min_occ = min(2, min_occ)

        if game.info.capt_on:
            if game.info.evens:
                min_occ = min(cval for cval in game.info.capt_on
                                    if not cval % 1)
            else:
                min_occ = min(*game.info.capt_on, min_occ)

        # a capt_min value overrides any other
        if game.info.capt_min:
            if min_occ == game.cts.total_seeds:
                min_occ = game.info.capt_min
            else:
                min_occ = max(game.info.capt_min, min_occ)

        if min_occ == game.cts.total_seeds:
            min_occ = -1

        return min_occ


    def _cant_occupy_more(self):
        """Determine if we can occupy more territory.
        If min_occ feature was disabled (== -1), return False.
        If there are any children, return False (sowing into children
        may claim more territory).
        If there are too few seeds left to claim more territory,
        return True.

        If we can't move unclaimed seeds to the current player's store."""

        if self.min_occ < 0:
            return False

        remaining = 0
        for loc in range(self.game.cts.dbl_holes):
            if self.game.child[loc] is None:
                remaining += self.game.board[loc]
            else:
                return False

        if remaining < self.min_occ:
            game_log.add(
                'Too few seeds for more territory to be claimed '
                f'(<= {self.min_occ}); remaining going to {self.game.turn}.',
                game_log.IMPORT)

            self.game.store[self.game.turn] += remaining
            return True

        return False


    def _test_round_winner(self):
        """The round has ended, determine if their is a game
        winner, or the round outcome."""

        winner, wholes = self.game.compute_win_holes()

        if winner is None:
            return gi.WinCond.ROUND_TIE, self.game.turn
        if wholes >= self.game.info.gparam_one:
            return gi.WinCond.WIN, winner
        return gi.WinCond.ROUND_WIN, winner


    def _test_winner(self):
        """The game has ended, decide who won or if a TIE."""

        winner, _ = self.game.compute_win_holes()
        if winner is None:
            return gi.WinCond.TIE, self.game.turn
        return gi.WinCond.WIN, winner


    def game_ended(self, repeat_turn, ended=False):
        """Determine if the game ended."""

        if ended or self._cant_occupy_more():
            return self.winner_test()

        cond, winner = self.decorator.game_ended(repeat_turn, ended)

        if cond == gi.WinCond.GAME_OVER:
            return self.winner_test()

        return cond, winner


class DepriveEndGame(EndTurnIf):
    """We are forcing the game to end, end in a tie."""

    def game_ended(self, repeat_turn, ended=False):
        """Determine if the game ended."""
        return gi.WinCond.TIE, self.game.turn


class TerritoryEndGame(EndTurnIf):
    """We are forcing the game to end, call the decorator
    to collect the seeds and then decide who wins."""

    def _test_winner(self):
        """The game has ended, decide who won or if a TIE."""

        winner, _ = self.game.compute_win_holes()
        if winner is None:
            return gi.WinCond.TIE, self.game.turn
        return gi.WinCond.WIN, winner


    def game_ended(self, repeat_turn, ended=False):
        """Determine if the game ended."""

        # call this to execute the divier
        self.decorator.game_ended(repeat_turn, ended)

        # win_count is patched to total_seeds so determine the winner here
        return self._test_winner()



# %% build decorator chains

def deco_add_bottom_winner(game):
    """Start the deco chain by adding the bottom Winner
    and MaxWinner (if needed)."""

    if game.info.no_sides:
        ender = Winner(game, claimer=TakeOnlyChildNStores(game))

    elif game.info.goal == gi.Goal.TERRITORY:
        ender = Winner(game,
                       claimer=TakeOwnSeeds(game, lambda loc: game.owner[loc]))
    else:
        ender = Winner(game, claimer=TakeOwnSeeds(game, game.cts.board_side))

    if game.info.goal == gi.Goal.MAX_SEEDS:
        ender = MaxWinner(game, ender)

    return ender


def deco_end_move(game):
    """Return a chain of move enders."""

    if game.info.goal == gi.Goal.DEPRIVE:
        return DepriveSeedsEndGame(game)

    ender = deco_add_bottom_winner(game)

    if not game.info.mustpass:
        ender = EndTurnNoPass(game, ender)

    if game.info.mustshare:
        if game.info.goal == gi.Goal.TERRITORY:
            ender = EndTurnMustShare(game, lambda loc: game.owner[loc], ender)
        else:
            ender = EndTurnMustShare(game, game.cts.board_side, ender)

    ender = EndTurnNotPlayable(game, ender)

    if game.info.child_cvt:
        claimer = ChildClaimSeeds(game)
    else:
        claimer = ClaimSeeds(game)
    ender = Winner(game, ender, claimer)

    if game.info.rounds:
        ender = RoundWinner(game, ender, ClaimOwnSeeds(game))

    if game.info.child_type == gi.ChildType.WALDA:
        ender = WaldaEndMove(game, ender)

    if game.info.goal == gi.Goal.TERRITORY:
        ender = TerritoryGameWinner(game, ender)

    return ender


def deco_quitter(game):
    """Return a chain for the quitter (user ended game or reached
    an ENDLESS condition). Do something that seems fair. Assume that
    seeds in play could belong to either player.

    DEPRIVE: end in a TIE. Don't change the board.

    TERRITORY: divvy the seeds and compute territory for each with
    rounding rules. If outright winner based on gparam_one go with it,
    otherwise TIE.

    MAX_SEEDS: divvy the seeds, use MaxWinner to computer winner or TIE.

    When divvying seeds move them to stores or children
    (TERRITORY & MAX_SEEDS games must have one or both)."""

    if game.info.goal == gi.Goal.DEPRIVE:
        return DepriveEndGame(game)

    if game.info.stores:
        quitter = Winner(game, claimer=DivvySeedsStores(game))
    elif game.info.child_cvt:
        quitter = Winner(game, claimer=DivvySeedsChildOnly(game))
    else:
        return Winner(game, claimer=DivvyIgnoreSeeds(game))

    if game.info.goal == gi.Goal.MAX_SEEDS:
        quitter = MaxWinner(game, quitter)
    else:  # elif game.info.goal == gi.Goal.TERRITORY:
        quitter = TerritoryEndGame(game, quitter)

    return quitter
