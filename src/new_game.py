# -*- coding: utf-8 -*-
"""Create a new game or round.

Created on Fri Apr  7 12:47:15 2023
@author: Ann"""


# %% imports

import abc

import claimer
import deco_chain_if
import game_info as gi
import round_tally

from game_logger import game_log
from fill_patterns import PCLASSES


# %% set_round_starter

def set_round_starter(game):
    """Set the starter of the next round based on the game flag."""

    # make turn equal to legacy value (when it was winner)
    if game.mdata and game.mdata.winner is not None:
        game.turn = game.mdata.winner

    start_rule = game.info.round_starter
    if start_rule == gi.RoundStarter.ALTERNATE or game.turn is None:
        game.turn = not game.starter

    elif start_rule == gi.RoundStarter.LOSER:
        if game.mdata and game.mdata.winner is not None:
            game.turn = not game.mdata.winner
        else:
            game.turn = not game.turn

    elif start_rule == gi.RoundStarter.LAST_MOVER:
        game.turn = game.mdata.player

    game.starter = game.turn


# %%  NewGame interace

class NewGameIf(deco_chain_if.DecoChainIf):
    """New Game Interface."""

    @abc.abstractmethod
    def new_game(self, new_round=False):
        """Start a new game."""


# %% base new game

class NewGame(NewGameIf):
    """Default new game reset all variables."""

    def new_game(self, new_round=None):
        """Reset the game to new state and alternate start player."""
        _ = new_round

        self.game.store = [0, 0]
        self.game.board = [self.game.cts.nbr_start] * self.game.cts.dbl_holes
        self.game.init_bprops()

        self.game.turn = not self.game.starter
        self.game.starter = self.game.turn


# %%  decorators

class NewGamePattern(NewGameIf):
    """A new game that sets the fill pattern based on the pattern."""

    def __init__(self, game, pattern, decorator=None):

        super().__init__(game, decorator)
        self.pattern = pattern


    def __str__(self):
        """A recursive func to print the whole decorator chain."""

        return self.str_deco_detail(str(self.pattern))


    def new_game(self, new_round=False):
        """Reset the game to new state and choose random start player."""

        self.decorator.new_game(new_round)
        self.pattern.fill_seeds(self.game)


class NewRound(NewGameIf):
    """Create a new round if allowed."""

    def __init__(self, game, decorator=None):

        super().__init__(game, decorator)
        self.collector = claimer.ClaimOwnSeeds(game)

        holes = self.game.cts.holes
        dbl_holes = self.game.cts.dbl_holes

        if self.game.info.round_fill == gi.RoundFill.RIGHT_FILL:
            self.fill_orders = [range(holes - 1, -1, -1),
                                range(dbl_holes - 1, holes - 1, -1)]

        elif self.game.info.round_fill == gi.RoundFill.LEFT_FILL:
            self.fill_orders = [range(holes), range(holes, dbl_holes)]

        elif self.game.info.round_fill in (gi.RoundFill.SHORTEN,
                                           gi.RoundFill.SHORTEN_ALL):
            self.fill_orders = [range(holes),
                                range(dbl_holes - 1, holes - 1, -1)]

        elif self.game.info.round_fill in (gi.RoundFill.NOT_APPLICABLE,
                                           gi.RoundFill.OUTSIDE_FILL,
                                           gi.RoundFill.UCHOOSE,
                                           gi.RoundFill.UMOVE):
            self.fill_orders = [self.game.cts.false_fill,
                                self.game.cts.true_fill]

        else:
            raise NotImplementedError(
                    f"RoundFill {game.info.round_fill} not implemented.")


    def _compute_fills(self):
        """Detemine how many holes to fill on each side and
        adjust the store to hold the remaining seeds.
        If SHORTEN, both sides are filled the same based on the
        number of seeds the loser has."""

        fill = [0, 0]
        seeds = self.collector.claim_seeds()

        game = self.game
        nbr_start = game.cts.nbr_start
        holes = game.cts.holes
        extra = 0

        if game.info.round_fill in (gi.RoundFill.SHORTEN,
                                    gi.RoundFill.SHORTEN_ALL):

            loser = 0 if seeds[0] < seeds[1] else 1
            quot = seeds[loser] // nbr_start
            fill[0] = fill[1] = min(quot, holes)

            if game.info.round_fill == gi.RoundFill.SHORTEN_ALL:
                winner = not loser
                game.store[loser] = 0
                extra = seeds[loser] - fill[loser] * nbr_start
                game.store[winner] = seeds[winner] - fill[winner] * nbr_start
                game.store[winner] -= extra
            else:
                game.store[0] = seeds[0] - fill[0] * nbr_start
                game.store[1] = seeds[1] - fill[1] * nbr_start

        else:
            for store in (False, True):
                quot = seeds[store] // nbr_start
                fill[store] = min(quot, holes)
                game.store[store] = seeds[store] - fill[store] * nbr_start

        return fill, extra


    def new_game(self, new_round=False):
        """Create a new round if allowed.
        Use pre-determine pattern to distribute the seeds for the
        next round.

        If the board size is 4 or move and the fill method is SHORTEN,
        stop making children if the playable board size
        is reduced to 3 or less."""

        if not new_round:
            self.decorator.new_game(new_round)
            return

        nbr_start = self.game.cts.nbr_start
        blocks = self.game.info.blocks
        fill, extra = self._compute_fills()

        set_round_starter(self.game)
        self.game.init_bprops()

        if (self.game.cts.holes > 3
                and self.game.info.round_fill in (gi.RoundFill.SHORTEN,
                                                  gi.RoundFill.SHORTEN_ALL)):
            self.game.inhibitor.set_child(fill[0] <= 3)

        for store, brange in enumerate(self.fill_orders):
            eside = extra
            for cnt, loc in enumerate(brange):
                if cnt < fill[store]:
                    self.game.board[loc] = nbr_start
                elif eside:
                    self.game.board[loc] = eside
                    eside = 0
                else:
                    self.game.board[loc] = 0
                    if blocks:
                        self.game.blocked[loc] = True


class TerritoryNewRound(NewGameIf):
    """If the game is over, call chained decorator.
    Otherwise, start a new round, compute the holes owned by false;
    call the deco chain to init the board; and then
    assign the owners."""

    def new_game(self, new_round=False):
        """Adjust the game outcome."""

        if not new_round:
            self.decorator.new_game(new_round)
            return

        winner, wholes = self.game.deco.ender.compute_win_holes()

        set_round_starter(self.game)
        saved_starter = self.game.starter
        saved_turn = self.game.turn

        self.decorator.new_game(new_round=True)
        self.game.starter = saved_starter
        self.game.turn = saved_turn

        loc = self.game.cts.holes if winner else 0
        direct = 1

        for cnt in range(self.game.cts.dbl_holes):
            self.game.owner[loc] = winner if cnt < wholes else not winner
            loc = (loc + direct) % self.game.cts.dbl_holes


class NewRoundEven(NewGameIf):
    """Evenly distribute the seeds based on the losers seeds.
    Leave the two sides of the board symetrical.

    If none of the holes have sufficient seeds for a minimum move,
    move the number of extra seeds that the loser has into leftmost
    holes for valid moves, adjusting the store appropriately.

    Ginfo rule assures that min_move is <= the number of holes
    (rule: high_min_moves).

    Ender assures that there are sufficient seeds for UMOVE rules of
    1 see per hole and one playable hole and EVEN_FILL of one playable
    hole (see RoundWinner)."""

    def new_game(self, new_round=False):
        """Adjust the game outcome."""

        if not new_round:
            self.decorator.new_game(new_round)
            return

        winner = self.game.mdata.winner if self.game.mdata else self.game.turn
        set_round_starter(self.game)
        self.game.init_bprops()

        cts = self.game.cts
        min_move = self.game.info.min_move

        loser_seeds = self.game.store[not winner] + \
            sum(self.game.board[loc] for loc in cts.get_my_range(not winner))

        seeds_per_hole, l_store = divmod(loser_seeds, cts.holes)
        if seeds_per_hole < min_move and not l_store:
            seeds_per_hole -= 1
            l_store += cts.holes

        seeds_per_side = seeds_per_hole * cts.holes
        w_store = cts.total_seeds - loser_seeds - seeds_per_side

        if winner:
            self.game.store = [l_store, w_store]
        else:
            self.game.store = [w_store, l_store]
        self.game.board = [seeds_per_hole] * self.game.cts.dbl_holes

        if seeds_per_hole < min_move:

            self.game.board[0] += l_store
            self.game.board[cts.holes] += l_store

            self.game.store[0] -= l_store
            self.game.store[1] -= l_store

            game_log.add('Adjusted seeds for minimum move.', game_log.IMPORT)


class NewRoundTally(NewGameIf):
    """New game for tally games. If starting a new game (not round)
    clear the round tallies."""

    def new_game(self, new_round=False):
        """Adjust the game outcome.

        NewGame alternates starters, we want to follow the
        round_starter method, so save and restore starter &
        turn info, then call set_round_starter"""

        starter = self.game.starter
        winner = self.game.mdata.winner if self.game.mdata else self.game.turn
        self.decorator.new_game(new_round)

        self.game.starter = starter
        self.game.turn = winner
        set_round_starter(self.game)

        if not new_round:
            self.game.rtally.clear()


class NewFixedChildren(NewGameIf):
    """Currently only support fixed children in rightmost hole."""

    def new_game(self, new_round=False):

        self.decorator.new_game(new_round)

        self.game.child[self.game.cts.holes - 1] = False
        self.game.child[self.game.cts.dbl_holes - 1] = True


class SeedCountCheck(NewGameIf):
    """Check to make certain that the board is setup acceptably."""

    def new_game(self, new_round=False):

        new_round = self.decorator.new_game(new_round)

        store = self.game.store
        board = self.game.board

        assert (all(cnt >= 0 for cnt in board + store)
                and sum(store) + sum(board) == self.game.cts.total_seeds
                ), f"seed count error in new_game\n{store}\n{board}"


# %%

def deco_new_game(game):
    """Create the new_game chain."""

    new_game = NewGame(game)

    if game.info.child_locs == gi.ChildLocs.FIXED_ONE_RIGHT:
        new_game = NewFixedChildren(game, new_game)

    if game.info.start_pattern:
        new_game = NewGamePattern(game,
                                  PCLASSES[game.info.start_pattern],
                                  new_game)

    if game.info.rounds:
        if game.info.goal == gi.Goal.TERRITORY:
            new_game = TerritoryNewRound(game, new_game)

        elif game.info.goal in round_tally.RoundTally.GOALS:
            new_game = NewRoundTally(game, new_game)

        elif game.info.round_fill in (gi.RoundFill.EVEN_FILL,
                                      gi.RoundFill.UMOVE):
            new_game = NewRoundEven(game, new_game)

        else:
            new_game = NewRound(game, new_game)

        # catch an error in round starter at construction time
        if game.info.round_starter not in (gi.RoundStarter.ALTERNATE,
                                           gi.RoundStarter.LOSER,
                                           gi.RoundStarter.WINNER,
                                           gi.RoundStarter.LAST_MOVER):
            raise NotImplementedError(
                    f"RoundStarter {game.info.round_starter} not implemented.")

    if __debug__:    # pragma: no coverage
        new_game = SeedCountCheck(game, new_game)

    return new_game
