# -*- coding: utf-8 -*-
"""Game class the mancala game NamNam.
No stores are used instead 'walda's are created during
game play.

Created on Thu Jan  5 03:15:41 2023
@author: Ann"""


# %% imports

import functools as ft

import end_move
import game_interface as gi
import game_str
import ginfo_rules
import mancala
import new_game
import sower

from game_interface import WinCond
from game_log import game_log


# %%

def build_namnam_rules():
    """Refine the GameInfo rules for NamNam."""

    def rev_getattr(name, obj):
        return getattr(obj.flags, name)

    rules = ginfo_rules.RuleDict()

    rules.add_rule(
        'need_rounds',
        rule=lambda ginfo: not ginfo.flags.rounds,
        msg='NamNam requires rounds.',
        excp=gi.GameInfoError)

    rules.add_rule(
        'need_convert_cnt',
        rule=lambda ginfo: ginfo.flags.convert_cnt <= ginfo.nbr_holes,
        msg='NamNam requires convert_cnt to define victory condition'
            ' (number of owned houses > holes per side).',
        excp=gi.GameInfoError)

    rules.add_rule(
        'convert_cnt_limit',
        rule=lambda ginfo: ginfo.flags.convert_cnt > ginfo.nbr_holes * 2,
        msg='The number of houses owned for victory must be less than or '
            'equal to the total number of holes.',
        excp=gi.GameInfoError)

    rules.add_rule(
        'need_capt_on',
        rule=lambda ginfo: not any(ginfo.capt_on),
        msg='NamNam needs at least one capt_on checked.',
        excp=gi.GameInfoError)

    rules.add_rule(
        'need_stores',
        rule=lambda ginfo: not ginfo.flags.stores,
        msg='NamNam requires stores.',
        excp=gi.GameInfoError)

    rules.add_rule(
        'min_move_one',
        rule=lambda ginfo: ginfo.min_move != 1,
        msg='NamNam requires a minimum move of 1.',
        excp=gi.GameInfoError)

    bad_flags = ['blocks', 'capsamedir', 'child', 'crosscapt', 'evens',
                 'grandslam', 'multicapt', 'oppsidecapt', 'sow_own_store',
                 'xcpickown']
    for flag in bad_flags:
        rules.add_rule(
            f'bad_{flag}',
            rule=ft.partial(rev_getattr, flag),
            msg=f'NamNam cannot be used with {flag.upper()}.',
            excp=gi.GameInfoError)

    rules |= ginfo_rules.build_rules()
    del rules['rounds_wo_blocks']
    del rules['mlap_capt_on_incomp']

    return rules


# %%

class HoleMarkerOwner(game_str.HoleMarkerIF):
    """Create a hole string for games with hole owners."""

    def get_hole_str(self, loc):
        """Return mark for hole"""
        return game_str.CHILD[self.game.owner[loc]] + \
            self.decorator.get_hole_str(loc)


class SowSeeds(sower.SowMethodIf):
    """Any holes sown to capt_on values are captured by the hole's
    owner, except for the last seed. The last hole may be captured
    from the opponent's hole (leave that to the capturer).

    Need to use this in the lap sower as base sower."""

    def sow_seeds(self, start, direct, seeds):
        """Sow seeds."""

        loc = start
        for scnt in range(seeds, 0, -1):

            loc = self.game.deco.incr.incr(loc, direct, start)
            self.game.board[loc] += 1

            if (self.game.unlocked[loc] and
                self.game.board[loc] in self.game.info.capt_on):
                turn = self.game.turn
                if scnt > 1:
                    if self.game.owner[loc] == turn:
                        game_log.add(f'      Catpure from {loc}.')
                        self.game.store[turn] += self.game.board[loc]
                        self.game.board[loc] = 0
                else:
                    game_log.add(f'      Catpure from {loc}.')
                    self.game.store[turn] += self.game.board[loc]
                    self.game.board[loc] = 0

        return loc


class RoundGameWinner(end_move.EndTurnIf):
    """When there are fewer than nbr_start seeds on the board,
    give the remaining seeds to the current player.
    Determine if there is a game winner by territory (convert_cnt)
    or compare the seeds to determine a round winner.
    Otherwise call the deco chain; we need EndTurnMustShare and/or
    EndTurnNoPass to decide if the game has ended.
    Note that win_count is patched so Winner will not end the game."""

    def compare_seed_cnts(self, seeds):
        """All of the seeds have been collected and the
        game is not over, determine the round outcome."""

        if seeds[True] > seeds[False]:
            return WinCond.ROUND_WIN, True

        if seeds[False] > seeds[True]:
            return WinCond.ROUND_WIN, False

        # if seeds[False] == seeds[True]:
        return WinCond.ROUND_TIE, self.game.turn


    def game_ended(self, repeat_turn, ended=False):
        """Round the false holes to deal with non-mod-4 seeds."""

        remaining = sum(self.game.board)
        if remaining <= self.game.cts.nbr_start:
            game_log.add(
                f'Too few seeds, remaining going to {self.game.turn}.',
                game_log.INFO)
            self.game.store[self.game.turn] += remaining

            tot_holes = self.game.cts.dbl_holes
            nbr_start = self.game.cts.nbr_start
            convert_cnt = self.game.info.flags.convert_cnt

            self.game.board = [0] * tot_holes
            self.game.false_holes = (self.game.store[False] + 1) // nbr_start

            if self.game.false_holes >= convert_cnt:
                return WinCond.WIN, False
            if tot_holes - self.game.false_holes >= convert_cnt:
                return WinCond.WIN, True

            return self.compare_seed_cnts(self.game.store)

        return self.decorator.game_ended(repeat_turn, ended)


class NewRound(new_game.NewGameIf):
    """Wrap the existing NewGame deco chain.
    If the mancala chain created a new game, reset the owners.
    If the mancala chain created a new round, empty the stores,
    unblock all the holes, put the start seeds into each hole,
    and set the owners."""

    def new_game(self, win_cond=None, new_round_ok=False):
        """Adjust the game outcome."""

        if self.decorator.new_game(win_cond, new_round_ok):
            holes = self.game.cts.holes
            self.game.owner = [False] * holes + [True] * holes
            return True

        self.game.store = [0, 0]
        self.game.blocked = [False] * self.game.cts.dbl_holes

        nbr_start = self.game.cts.nbr_start
        for loc in range(self.game.cts.dbl_holes):
            if loc < self.game.false_holes:
                self.game.board[loc] = nbr_start
                self.game.owner[loc] = False
            else:
                self.game.board[loc] = nbr_start
                self.game.owner[loc] = True

        return False


# %%  game class

class NamNam(mancala.Mancala):
    """The NamNam game dynamics."""

    rules = build_namnam_rules()

    def __init__(self, game_consts, game_info):
        """Patch the win_count so that the default EndTurn.Winner doesn't
        decide there was a win.
        Call parent init.
        Set the default owners.  Init false_holes (ender computes it
        and new_game uses it).
        Update the decorators."""

        object.__setattr__(game_consts, 'win_count', game_consts.total_seeds)

        super().__init__(game_consts, game_info)
        self.owner = [False] * self.cts.holes + [True] * self.cts.holes
        self.false_holes = 0

        sower.deco_replace_base_sower(self, SowSeeds(self))
        self.deco.ender = RoundGameWinner(self, self.deco.ender)
        self.deco.new_game = NewRound(self, self.deco.new_game)
        hole_str = HoleMarkerOwner(self, self.deco.gstr.hole_str)
        self.deco.gstr.hole_str = hole_str


    def get_hole_props(self, row, pos):
        """Return the number of seeds for each side/position.
        row : 0 for top row, 1 for bottom  (opposite of player/turn)
        position : 0 .. 5 from left to right.
        Use owner for child owner."""

        loc = self.cts.pos_to_loc(row, pos)
        return gi.HoleProps(seeds=self.board[loc],
                            unlocked=self.unlocked[loc],
                            blocked=self.blocked[loc],
                            ch_owner=self.owner[loc])
