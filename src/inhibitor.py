# -*- coding: utf-8 -*-
"""Inhibitor supports inhibiting or allowing operations.
These are not deco chains, each class does everything it needs to.

Created on Mon Nov 20 16:12:06 2023
@author: Ann"""


import abc

import animator
import game_info as gi

from game_logger import game_log


class InhibitorIf(abc.ABC):
    """Required inhibitor interfaces."""

    @abc.abstractmethod
    def new_game(self):
        """Init the inhibitor for a new game (not new round)."""

    def start_ani_msg(self):
        """Show any message for the start of the game.
        This is only called if the animator is active."""

    @abc.abstractmethod
    def get_state(self):
        """Return any state data, it must be immutable
        (single value or tuple)."""

    @abc.abstractmethod
    def set_state(self, istate):
        """Restore the inhibitor state from the istate data
        (previously collected from get_state)"""

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

    def __str__(self):
        return 'InhibitorNone()'

    def new_game(self):
        pass

    def start_ani_msg(self):
        pass

    def get_state(self):
        return None

    def set_state(self, istate):
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

    def __init__(self, expire=1):
        self._captures = True   # game state
        self._expire = expire

    def __str__(self):
        return f'InhibitorCaptN(capture={self._captures}, expire={self._expire})'

    def new_game(self):
        self._captures = True
        game_log.add('Inhibiting captures.', game_log.IMPORT)


    def start_ani_msg(self):
        animator.animator.message(
            f'Captures Inhibited for {self._expire} Move'
            + ('s' if self._expire > 1 else ''))

    def get_state(self):
        return self._captures

    def set_state(self, istate):
        self._captures = istate

    def clear_if(self, game, mdata):
        logit = self._captures
        if game.movers >= self._expire:
            self._captures = False
            if logit:
                game_log.add('Inhibit captures expired.', game_log.IMPORT)
                if animator.active():
                    animator.animator.message('Inhibit Captures Expired')

    def set_on(self, turn):
        _ = turn
        self._captures = True
        game_log.add('Inhibiting captures.', game_log.IMPORT)
        if animator.active():
            animator.animator.message('Inhibiting Captures')

    def set_off(self):
        self._captures = False
        game_log.add('Allowing  captures.', game_log.IMPORT)
        if animator.active():
            animator.animator.message('Allowing captures')

    def set_child(self, condition):
        _ = condition

    def stop_me_capt(self, turn):
        _ = turn
        return self._captures

    def stop_me_child(self, turn):
        _ = turn
        return False


class InhibitorChildrenOnly(InhibitorIf):
    """An Inhibitor that only allows turning on and off
    making of children."""

    def __init__(self):
        self._children = False   # game state

    def __str__(self):
        return f'InhibitorChildrenOnly(children={self._children})'

    def new_game(self):
        self._children = False
        game_log.add('Clearing inhibit children.', game_log.IMPORT)

    def start_ani_msg(self):
        if self._children:
            animator.animator.message('Children Inhibited')

    def get_state(self):
        return self._children

    def set_state(self, istate):
        self._children = istate

    def clear_if(self, game, mdata):
        _ = game, mdata

    def set_on(self, turn):
        _ = turn
        self._children = True
        game_log.add('Setting inhibit children.', game_log.IMPORT)
        if animator.active():
            animator.animator.message('Children Inhibited')

    def set_off(self):
        game_log.add('Clearing inhibit children.', game_log.IMPORT)
        self._children = False
        if animator.active():
            animator.animator.message('Children Allowed')

    def set_child(self, condition):
        self._children = condition
        game_log.add(f'Setting inhibit children {condition}.',
                     game_log.IMPORT)
        if animator.active():
            if condition:
                animator.animator.message('Children Inhibited')
            else:
                animator.animator.message('Children Allowed')

    def stop_me_capt(self, turn):
        _ = turn
        return False

    def stop_me_child(self, turn):
        _ = turn
        return self._children


class InhibitorBoth(InhibitorIf):
    """An Inhibitor that supports shortened boards and
    limiting both children and captures."""

    def __init__(self, test_func=None):
        self._turn = None          # game state
        self._captures = False     # game state
        self._children = False     # game state
        self._child_only = False   # game state
        self._test = test_func

    def __str__(self):

        rstr = 'InhibitorBoth:\n'
        rstr += f'  turn: {self._turn}'
        rstr += f'  capture: {self._captures}'
        rstr += f'  children: {self._children}'
        rstr += f'  child_only: {self._child_only}'
        rstr += f'  test func: {self._test}'
        return rstr

    def new_game(self):
        self._turn = None
        self._captures = False
        self._children = False
        self._child_only = False
        game_log.add('Allowing children and captures.', game_log.IMPORT)

    def start_ani_msg(self):
        """Status of this inhibitor is changed by the new game deco--
        this is required even though new_game disables the inhibitors."""

        if self._child_only:
            animator.animator.message('Children Prohibited')
            return

        if self._captures and self._children:
            animator.animator.message('Children and Captures Inhibited for '
                                      + gi.PLAYER_NAMES[self._turn])

    def get_state(self):
        return (self._turn, self._captures, self._children, self._child_only)

    def set_state(self, istate):
        self._turn, self._captures, self._children, self._child_only = istate

    def clear_if(self, game, mdata):
        logit = self._captures or self._children
        if self._test(game, mdata):
            self._captures = False
            self._children = False
            if logit:
                game_log.add('Allowing children and captures.', game_log.IMPORT)
                if animator.active():
                    animator.animator.message('Allowing Children and Captures')

    def set_on(self, turn):
        self._turn = turn
        self._captures = True
        self._children = True
        game_log.add('Inhibiting children and captures for ' \
                     + gi.PLAYER_NAMES[turn] + '.',
                     game_log.IMPORT)
        if animator.active():
            animator.animator.message('Children and Captures Inhibited for '
                                      + gi.PLAYER_NAMES[turn])

    def set_off(self):
        self._turn = None
        self._captures = False
        self._children = False
        game_log.add('Allowing children and captures.', game_log.IMPORT)
        if animator.active():
            animator.animator.message('Inhibitor Disabled')

    def set_child(self, condition):
        self._child_only = condition
        game_log.add(f'Setting inhibit children {condition} both players.',
                     game_log.IMPORT)
        if animator.active():
            if condition:
                animator.animator.message('Children Inhibited')
            else:
                animator.animator.message('Children Allowed')

    def stop_me_capt(self, turn):
        return self._turn == turn and self._captures

    def stop_me_child(self, turn):
        return (self._children and self._turn == turn) or self._child_only


# %%  condition functions
#     params are:  game, mdata

def arnge_limit_cond(_, mdata):
    """Was there a capture or child made."""
    return mdata.captured or mdata.capt_changed


# %%  build the deco

def make_inhibitor(game):
    """Make the inhibitor.  It's not a chain."""

    if game.info.nocaptmoves:
        return InhibitorCaptN(game.info.nocaptmoves)

    if game.info.prescribed == gi.SowPrescribed.ARNGE_LIMIT:
        return InhibitorBoth(arnge_limit_cond)

    if game.info.round_fill in (gi.RoundFill.SHORTEN,
                                gi.RoundFill.SHORTEN_ALL):
        return InhibitorChildrenOnly()

    return InhibitorNone()
