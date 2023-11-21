# -*- coding: utf-8 -*-
"""Inhibitor supports inhibiting or allowing operations.
These are not deco chains, each class does everything it needs to.

Created on Mon Nov 20 16:12:06 2023
@author: Ann"""


import abc

import game_interface as gi

from game_log import game_log


class InhibitorIf(abc.ABC):
    """Required inhibitor interfaces."""

    @abc.abstractmethod
    def new_game(self):
        """Init the inhibitor for a new game (not new round)."""

    @abc.abstractmethod
    def clear_if(self, game, mdata):
        """Clear flags based on inputs"""

    @abc.abstractmethod
    def set_on(self, turn):
        """Inhibit both for turn"""

    @abc.abstractmethod
    def set_off(self):
        """Turn off all inhibit flags."""

    @abc.abstractmethod
    def set_child(self, condition):
        """Set only inhibit child."""

    @abc.abstractmethod
    def stop_me_capt(self, turn):
        """Return True if the current player should be
        stopped from capturing."""

    @abc.abstractmethod
    def stop_me_child(self, turn):
        """Return True if the current player should be
        stopped from making children."""


class InhibitorNone(InhibitorIf):
    """Base inhibitor inhibits nothing."""

    def new_game(self):
        pass

    def clear_if(self, game, mdata):
        _ = game, mdata

    def set_on(self, turn):
        _ = turn

    def set_off(self):
        pass

    def set_child(self, condition):
        _ = condition

    def stop_me_capt(self, turn):
        _ = turn
        return False

    def stop_me_child(self, turn):
        _ = turn
        return False


class InhibitorCaptN(InhibitorIf):
    """An Inhibitor that prevents captures for a number of turns."""

    def __init__(self, expire=None):
        self.captures = True
        self.expire = expire

    def new_game(self):
        self.captures = True
        game_log.add('Inhibiting captures.', game_log.IMPORT)

    def clear_if(self, game, mdata):
        if game.mcount <= self.expire:
            self.captures = False
            game_log.add('Inhibit captures expired.', game_log.IMPORT)

    def set_on(self, turn):
        _ = turn
        self.captures = True
        game_log.add('Inhibiting captures.', game_log.IMPORT)

    def set_off(self):
        self.captures = False
        game_log.add('Allowing  captures.', game_log.IMPORT)

    def set_child(self, condition):
        _ = condition

    def stop_me_capt(self, turn):
        _ = turn
        return self.captures

    def stop_me_child(self, turn):
        _ = turn
        return False


class InhibitorShorten(InhibitorIf):
    """An Inhibitor that only deals with shortened boards.
    Example usage: disable children when the board gets too small."""

    def __init__(self):
        self.children = False

    def new_game(self):
        pass

    def clear_if(self, game, mdata):
        _ = game, mdata

    def set_on(self, turn):
        _ = turn

    def set_off(self):
        game_log.add('Clearing inhibit children (short board).',
                     game_log.IMPORT)
        self.children = False

    def set_child(self, condition):
        self.children = condition
        game_log.add(f'Setting inhibit children {condition} (short board).',
                     game_log.IMPORT)

    def stop_me_capt(self, turn):
        _ = turn
        return False

    def stop_me_child(self, turn):
        _ = turn
        return self.children


class InhibitorBoth(InhibitorIf):
    """An Inhibitor that supports shortened boards and
    limiting both children and captures."""

    def __init__(self, test_func=None):
        self.turn = None
        self.captures = False
        self.children = False
        self.child_only = False
        self.test = test_func

    def new_game(self):
        pass

    def clear_if(self, game, mdata):
        if self.test(game, mdata):
            if self.captures:
                game_log.add('Allowing children and captures.',
                             game_log.IMPORT)

            self.captures = False
            self.children = False

    def set_on(self, turn):
        self.turn = turn
        self.captures = True
        self.children = True
        game_log.add(f'inhibiting children and captures for {turn}.',
                     game_log.IMPORT)

    def set_off(self):
        self.turn = None
        self.captures = False
        self.children = False
        game_log.add('Allowing children and captures.', game_log.IMPORT)

    def set_child(self, condition):
        self.child_only = condition
        game_log.add(f'Setting inhibit children {condition}.',
                     game_log.IMPORT)

    def stop_me_capt(self, turn):
        return self.turn == turn and self.captures

    def stop_me_child(self, turn):
        return self.turn == turn and (self.children or self.child_only)


# %%  condition functions
#     params are:  game, mdata

def arnge_limit_cond(_, mdata):
    """Was there a capture or child made."""
    return mdata.captured or mdata.capt_changed


# %%  build the deco

def deco_inhibitor(game):
    """Make the inhibitor.  It's not a chain."""

    if game.info.nocaptfirst:
        return InhibitorCaptN(1)

    # Bao
    if (game.info.prescribed == gi.SowPrescribed.ARNGE_LIMIT
            and game.info.round_fill == gi.RoundFill.SHORTEN):
        return InhibitorBoth(arnge_limit_cond)

    if game.info.round_fill == gi.RoundFill.SHORTEN:
        return InhibitorShorten()

    return InhibitorNone()
