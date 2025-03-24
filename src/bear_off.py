# -*- coding: utf-8 -*-
"""A game class that does Backgammon-like bear off board clearing
after the game reaches a state where only singletons are left.
Any seeds left in a sow after it reaches the player's end of the
board are removed from play (actually moved to their store).

This is intendend for clear and deprive games, though not enforced.
It turns the end game into a race to see which player accomplishes
the goal first.

The transition from normal sow to bear-off sowing is made on the
first move when all of the seeds on the board are singletons
(e.g. all holes <=1 seeds). Games may ended via an outright win
before this conditions is achieved!

Even if a future moves starts with > 1 seeds in a hole, the
normal sow is not resumed.

The sower must be written to move back and forth between
normal and bear-off sowing to support the AI's search algos.

Created on Sat Nov  2 15:39:39 2024
@author: Ann"""

import dataclasses as dc
import end_move_decos
import game_interface as gi
import mancala
import sower_decos

from game_logger import game_log


# %% add to the rules

def build_rules():
    """Build the rules for BearOff game class.
    """

    rules = mancala.Mancala.rules

    rules.add_rule(
        'bo_no_sides',
        rule=lambda ginfo: ginfo.no_sides,
        msg='BearOff is not supported for NO_SIDES',
        excp=NotImplementedError)
        # where would the bear off be done

    rules.add_rule(
        'bo_min_move_g1',
        rule=lambda ginfo: ginfo.min_move != 1,
        msg='BearOff requires that MIN_MOVE be 1',
        excp=gi.GameInfoError)

    return rules


# %% deco replacements

class BearOffSow(sower_decos.SowMethodIf):
    """Sow seeds off the board when leaving our own side."""

    def sow_seeds(self, mdata):
        """Sow seeds."""

        if self.game.normal_sow:
            self.decorator.sow_seeds(mdata)
            return

        loc = mdata.cont_sow_loc
        for rem_seeds in range(mdata.seeds, 0, -1):

            ploc = loc
            loc = self.game.deco.incr.incr(loc,
                                           mdata.direct,
                                           mdata.cont_sow_loc)

            if self.game.cts.opp_side(self.game.turn, loc):
                self.game.store[not self.game.turn] += rem_seeds
                mdata.capt_loc = ploc
                mdata.captured = True
                return

            self.game.board[loc] += 1

        mdata.capt_loc = loc


class NoSeedsEnder(end_move_decos.EndTurnIf):
    """If we are past the normal_sow and the current player
    has no seeds, the opponent has won. Don't need to wait
    for opponents sow because they cannot be forced to give
    us seeds."""

    def game_ended(self, repeat_turn, ended=False):

        if (ended
            or self.game.normal_sow
            or any(self.game.board[loc]
                   for loc in self.game.cts.get_my_range(self.game.turn))):

            return self.decorator.game_ended(repeat_turn, ended)

        return gi.WinCond.WIN, not self.game.turn


# %% BearOff game class


# TODO update the makefile
# TODO return board size to 12

@dc.dataclass(frozen=True, kw_only=True)
class BearOffState(mancala.GameState):
    """Create a state for the BearOff game class"""

    normal_sow: bool = True


class BearOff(mancala.Mancala):
    """Sow per game configuration until there are only singltons
    on the board, then switch to using the BearOff sower."""

    @classmethod
    @property
    def rules(cls):
        """The rules for the class but don't build them unless we
        need them."""
        return build_rules()


    def __init__(self, game_consts, game_info):

        super().__init__(game_consts, game_info)

        self.normal_sow = True
        self.deco.ender = NoSeedsEnder(self, self.deco.ender)

        base_sow_class = type(self.deco.sower.get_single_sower())
        self.deco.insert_deco('sower',
                              base_sow_class,
                              BearOffSow(self))


    @property
    def state(self):
        """Create an SSGameState"""
        return BearOffState(normal_sow=self.normal_sow,
                            **(dc.asdict(super().state)))


    @state.setter
    def state(self, state):
        """Fill current state.
        The mancala state setter ignores fields in the dataclass
        that it doesn't know about."""

        mancala.Mancala.state.fset(self, state)
        self.normal_sow = state.normal_sow


    def new_game(self, win_cond=None, new_round_ok=False):
        """Reset sow to normal and rebuild the deco chain,
        then call the parent to do a new_game."""

        self.normal_sow = True
        super().new_game(win_cond, new_round_ok)


    def move(self, move):
        """Change the base sower if conditions are right,
        then call the parent to move."""

        if (self.normal_sow
                and not any(self.board[loc] > 1
                            for loc in range(self.cts.dbl_holes))):

            self.normal_sow = False
            game_log.add("Swapping to BearOff sower.", game_log.IMPORT)

        return super().move(move)
