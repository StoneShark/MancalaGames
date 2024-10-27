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
       via ClearWinner.
    2. Check for end condition: no outcome change, not playable,
       mustshare, or cannot pass (not mustpass).
    3. If the game has ended, collect seeds and determine if
       round/game winner or round/game tie.

Log a step if anything is changed on the board, e.g. TakeOwnSeeds.

Created on Fri Apr  7 07:43:19 2023
@author: Ann"""

# %% imports

import abc

import deco_chain_if
import game_interface as gi

from game_logger import game_log


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
        # seeds moved into stores, then added in later
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
    """Ignore unclaimed seeds; count stores and children.
    NoSides uses this."""

    def claim_seeds(self):

        seeds = self.game.store.copy()

        for loc in range(self.game.cts.dbl_holes):

            if self.game.child[loc] is True:
                seeds[True] += self.game.board[loc]

            elif self.game.child[loc] is False:
                seeds[False] += self.game.board[loc]

            else:
                self.game.board[loc] = 0

        game_log.step('Take seeds', self.game)
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


# %%  end turn interface

class EndTurnIf(deco_chain_if.DecoChainIf):
    """Interface for determining if the game is over."""

    def __init__(self, game, decorator=None, claimer=None):

        super().__init__(game, decorator)
        self.claimer = claimer
        self.win_seeds = self.compute_win_seeds(game)


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
        """Return the end condition and winner.
        End condition will be one of None, WIN, TIE,
        ROUND_WIN and ROUND_TIE. The other values of
        WinCond are not generated here."""


    def compute_win_holes(self):
        """Compute the number of holes that winner should own
        based on number of seeds. Seeds have already been collected
        from non-children.

        Return: fill start side for greater_holes (winner or True, for tie)
        and number of winner holes.

        This is used by the new_game deco."""

        game = self.game
        nbr_start = game.cts.nbr_start

        seeds = game.store.copy()
        for loc in range(game.cts.dbl_holes):
            if game.child[loc] is True:
                seeds[True] += game.board[loc]
            elif game.child[loc] is False:
                seeds[False] += game.board[loc]

        if seeds[True] == seeds[False]:
            # doesn't matter where fill starts for tie
            return True, game.cts.holes

        greater = seeds[True] > seeds[False]
        greater_holes = (seeds[greater] + nbr_start // 2) // nbr_start

        game_log.add(f"{greater} holes = {greater_holes}", game_log.IMPORT)
        return greater, greater_holes


    @staticmethod
    def round_seeds_for_win(req_holes, nbr_start):
        """Seeds required for round win in territory games."""

        return req_holes * nbr_start - nbr_start + nbr_start // 2 + 1


    @staticmethod
    def compute_win_seeds(game):
        """Compute the number of seeds a player needs for an
        outright win (or round win). A player collecting more
        that win_seeds wins.

        DEPRIVE games do not use this value, so -1."""

        game_goal = game.info.goal
        win_seeds = -1

        if game.info.rounds == gi.Rounds.NO_MOVES:
            win_seeds = game.cts.total_seeds - 1

        elif game_goal == gi.Goal.TERRITORY:
            win_seeds = EndTurnIf.round_seeds_for_win(game.info.gparam_one,
                                                      game.cts.nbr_start)

        elif game_goal == gi.Goal.MAX_SEEDS:
            # do this math in case a start_pattern leaves an odd total seeds
            half, rem = divmod(game.cts.total_seeds, 2)
            win_seeds = half + rem

        return win_seeds


    def has_seeds_for_win(self, seeds):
        """Determine if seed counts result in an
        end game condition."""

        if seeds[True] > self.win_seeds:
            return gi.WinCond.WIN, True

        if seeds[False] > self.win_seeds:
            return gi.WinCond.WIN, False

        if (seeds[False] == self.win_seeds
                and seeds[False] == seeds[True]):
            return gi.WinCond.TIE, self.game.turn

        return None, self.game.turn


# %%

class ClearWinner(EndTurnIf):
    """Determine if the seed counts result in a clear winner.
    There must be decorators in the chain below this."""

    def game_ended(self, repeat_turn, ended=False):

        if ended:
            return self.decorator.game_ended(repeat_turn, ended)

        cond, winner = self.has_seeds_for_win(self.claimer.claim_seeds())
        if cond:
            return cond, winner

        return self.decorator.game_ended(repeat_turn, False)


class RoundWinner(EndTurnIf):
    """"If the game is played in rounds, let the rest of the
    chain decide the outcome, then adjust for end of game or
    end of round. Additionally, the game is over if either player
    does not have the minimum seeds to continue the game.

    This is near the top of the deco chain. If ended is True
    actually end the game (not the round)."""

    def __init__(self, game, decorator=None, claimer=None):
        """Init the parent deco's; then fill:

        req_seeds: the number of seeds required to keep playing
        the game.

        msg: message to log if either player has fewer
        than win_seeds"""

        super().__init__(game, decorator, claimer)

        nbr_start = game.cts.nbr_start
        gparam_one = game.info.gparam_one
        intro = "Game, not round, ended (too few seeds to fill "

        if game.info.goal == gi.Goal.TERRITORY:
            req_holes = game.cts.dbl_holes - gparam_one + 1
            self.req_seeds = self.round_seeds_for_win(req_holes, nbr_start)
            self.msg = intro + f"at least {req_holes} holes)."

        elif game.info.round_fill == gi.RoundFill.UMOVE:
            self.req_seeds = game.cts.holes + game.info.min_move - 1
            self.msg = intro + "a playable side)."

        elif game.info.gparam_one > 0:
            # max seeds games do not round seeds
            self.req_seeds = game.info.gparam_one * nbr_start
            self.msg = intro + f"at least {gparam_one} holes)."

        else:
            self.req_seeds = nbr_start
            self.msg = intro + "a hole)."

    def game_ended(self, repeat_turn, ended=False):

        cond, player = self.decorator.game_ended(repeat_turn, ended)
        if ended or not cond:
            return cond, player

        seeds = self.claimer.claim_seeds()
        if seeds[True] < self.req_seeds or seeds[False] < self.req_seeds:
            game_log.add(self.msg, game_log.IMPORT)
            return cond, player

        if cond == gi.WinCond.WIN:
            return gi.WinCond.ROUND_WIN, player

        # if cond == gi.WinCond.TIE:
        return gi.WinCond.ROUND_TIE, player


class EndTurnNoMoves(EndTurnIf):
    """No Pass, end game if there are no moves for the next player
    OR on repeat turn, the current player has no moves."""

    def game_ended(self, repeat_turn, ended=False):

        if ended:
            return self.decorator.game_ended(repeat_turn, ended)

        if repeat_turn:
            ended = not any(self.game.get_allowable_holes())
            msg = "No moves for repeat turn; game ended."
        else:
            self.game.turn = not self.game.turn
            ended = not any(self.game.get_allowable_holes())
            self.game.turn = not self.game.turn
            msg = "No moves for next player; game ended."

        if ended:
            game_log.add(msg, game_log.INFO)

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
    have the minimum seeds required for a move, it's over.
    This is faster than simulating allowable moves and is
    needed for games w/o either mustshare or mustpass .

    This ends most territory games and rounds."""

    def game_ended(self, repeat_turn, ended=False):

        if ended:
            return self.decorator.game_ended(repeat_turn, ended)

        ended = not any(self.game.board[loc] >= self.game.info.min_move
                        and self.game.child[loc] is None
                        for loc in range(self.game.cts.dbl_holes))

        if ended:
            game_log.add("No moves available, round/game ended.",
                         game_log.IMPORT)

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
    """Determine if a deprive game is over.
    If the opp doesn't have a move, the game IS over.
    Base TIE versus WIN on who has seeds, thus separating
    having seeds and having a move.

    If opponent does not have seeds, current player WINS.

    If opponent cannot move and both players have seeds, TIE.

    If oppenent cannot move but current player does not have seeds,
    the opponents WINS because they have forced the current player
    to give away all their seeds.

    This is not to be used with stores or children."""

    def game_ended(self, repeat_turn, ended=False):
        """Check for end game."""

        cts = self.game.cts

        op_seeds = sum(self.game.board[loc]
                       for loc in cts.get_opp_range(self.game.turn))
        if not op_seeds:
            return gi.WinCond.WIN, self.game.turn

        self.game.turn = not self.game.turn
        no_opp_moves = not any(self.game.get_allowable_holes())
        self.game.turn = not self.game.turn
        if no_opp_moves:
            my_seeds = sum(self.game.board[loc]
                           for loc in cts.get_my_range(self.game.turn))

            if my_seeds:
                return gi.WinCond.TIE, self.game.turn

            return gi.WinCond.WIN, not self.game.turn

        return None, self.game.turn


class NoOutcomeChange(EndTurnIf):
    """Call the deco chain to decide if the game ends by normal
    means. If the game hasn't ended by normal means, determine
    if there can be any change in outcome based on seeds still
    in play.

    Games that use this class must either employ Waldas or have
    stores. In the case of Waldas, WaldaEndMove will cleanup."""

    def __init__(self, game, decorator=None, claimer=None):

        super().__init__(game, decorator, claimer)
        self.min_needed = self._min_for_change(game)


    @staticmethod
    def _min_for_change(game):
        """Select a minimum number of seeds that must be on the
        board for a capture or to claim territory."""
        # pylint: disable=too-many-branches

        if game.info.child_type:
            # presence of children checked at play-time
            min_needed = game.info.child_cvt
        else:
            min_needed = game.cts.total_seeds  # max possible and flag

        if (game.info.evens
                or game.info.capt_next
                or game.info.crosscapt):
            min_needed = min(2, min_needed)

        if game.info.capttwoout:
            if game.info.mlaps:
                min_needed = min(2, min_needed)
            else:
                min_needed = min(3, min_needed)

        if game.info.capt_on:
            if game.info.evens:
                min_needed = min(cval for cval in game.info.capt_on
                                    if not cval % 1)
            else:
                min_needed = min(*game.info.capt_on, min_needed)

        # a capt_min value overrides any other
        if game.info.capt_min:
            if min_needed == game.cts.total_seeds:
                min_needed = game.info.capt_min
            else:
                min_needed = max(game.info.capt_min, min_needed)

        if min_needed == game.cts.total_seeds:
            raise gi.GameInfoError("NoOutcomeChange included but unused.")

        return min_needed


    def _too_few_for_change(self):
        """Determine if the game outcome can change.
        If min_needed feature was disabled (== -1), return False.
        If there are any children, return False (can sow into children).
        If there are not any seeds, return False (this isn't called
        when there are no seeds).

        If there are too few seeds left to change the outcome,
        return True."""

        remaining = 0
        for loc in range(self.game.cts.dbl_holes):
            if self.game.child[loc] is None:
                remaining += self.game.board[loc]
            else:
                return False

        if 0 < remaining < self.min_needed:
            game_log.add(
                f'Too few seeds for outcome change (< {self.min_needed}).',
                game_log.IMPORT)
            return True

        return False


    def game_ended(self, repeat_turn, ended=False):
        """Determine if the game ended."""

        cond, winner = self.decorator.game_ended(repeat_turn, ended)

        if not ended and not cond and self._too_few_for_change():
            return self.decorator.game_ended(repeat_turn, True)

        return cond, winner


class EndGameWinner(EndTurnIf):
    """This is intended to be at the bottom of the deco chain.
    If any deco has determined that the game should end,
    this will end the game and pick a winner.

    The claimer should be a taker.
    The seeds for win is checked again (after running claimer/taker).

    Any child deco is ignored."""

    def game_ended(self, repeat_turn, ended=False):

        if not ended:
            return None, self.game.turn

        # check for clear win condition
        seeds = self.claimer.claim_seeds()
        cond, winner = self.has_seeds_for_win(seeds)

        if cond:
            return cond, winner

        # no clear win condition, pick player with most seeds
        if seeds[0] > seeds[1]:
            return gi.WinCond.WIN, False

        if seeds[0] < seeds[1]:
            return gi.WinCond.WIN, True

        return gi.WinCond.TIE, self.game.turn


class QuitToTie(EndTurnIf):
    """Force the game to end in a tie; don't change the board.
    Used for DEPRIVE games."""

    def game_ended(self, repeat_turn, ended=False):
        """Determine if the game ended."""
        return gi.WinCond.TIE, self.game.turn


# %% build decorator chains

def deco_add_bottom_winner(game):
    """Start the deco chain by adding the bottom Winner
    and MoreSeedsWinner (if needed)."""

    if game.info.no_sides:
        ender = EndGameWinner(
            game, claimer=TakeOnlyChildNStores(game))

    elif game.info.goal == gi.Goal.TERRITORY:
        ender = EndGameWinner(
            game, claimer=TakeOwnSeeds(game, lambda loc: game.owner[loc]))
    else:
        ender = EndGameWinner(
            game, claimer=TakeOwnSeeds(game, game.cts.board_side))

    return ender


def deco_end_move(game):
    """Return a chain of move enders."""

    if game.info.goal == gi.Goal.DEPRIVE:
        return DepriveSeedsEndGame(game)

    ender = deco_add_bottom_winner(game)

    if not game.info.mustpass:
        ender = EndTurnNoMoves(game, ender)

    if game.info.mustshare:
        if game.info.goal == gi.Goal.TERRITORY:
            ender = EndTurnMustShare(game, lambda loc: game.owner[loc], ender)
        else:
            ender = EndTurnMustShare(game, game.cts.board_side, ender)

    ender = EndTurnNotPlayable(game, ender)

    if not any([game.info.sow_own_store,
                game.info.mustshare,
                game.info.pickextra == gi.CaptExtraPick.PICKLASTSEEDS,
                game.info.pickextra == gi.CaptExtraPick.PICK2XLASTSEEDS,
                ]):
        ender = NoOutcomeChange(game, ender)

    claimer = ChildClaimSeeds(game) if game.info.child_cvt else ClaimSeeds(game)
    ender = ClearWinner(game, ender, claimer)

    if game.info.rounds:
        ender = RoundWinner(game, ender, ClaimOwnSeeds(game))

    if game.info.child_type == gi.ChildType.WALDA:
        ender = WaldaEndMove(game, ender)

    return ender


def deco_quitter(game):
    """Return a quitter. Used when either the user ended game or
    the game reached an ENDLESS condition.

    Do something that seems fair. Assume that seeds in play could
    belong to either player."""

    if game.info.stores:
        quitter = EndGameWinner(game, claimer=DivvySeedsStores(game))

    elif game.info.child_cvt:
        quitter = EndGameWinner(game, claimer=DivvySeedsChildOnly(game))

    else:
        quitter = QuitToTie(game)

    return quitter
