# -*- coding: utf-8 -*-
"""The Holebutton and StoreButton classes for Mancala UI with
states that allow the buttons to behave differently in different
game states.

Created on Sun Aug 13 10:06:37 2023
@author: Ann"""

import abc
import dataclasses as dc
import enum

import tkinter as tk

from game_interface import MoveTpl

# %%  constants and enums

SYSTEM_COLOR = 'SystemButtonFace'
PLAY_INACTIVE_COLOR = 'grey80'
MOVE_COLOR = 'lightblue'


class Behavior(enum.Enum):
    """Enum for the button behaviors."""

    GAMEPLAY = 1
    RNDSETUP = 2


# %%  global data for mover

@dc.dataclass
class Holding:
    """Global data to store the sedd holding data."""

    nbr: int = 0
    owner: bool = None


    def empty(self):
        """Remove seeds and owner."""
        self.nbr = 0
        self.owner = None

    @staticmethod
    def query_nbr_seeds(owner, max_seeds):
        """Get the number of seeds from the user.
        Store them in the hold."""

        if hold.nbr > 0:
            return False

        if max_seeds == 1:
            hold.nbr = 1
            hold.owner = owner
            return True

        nbr = tk.simpledialog.askinteger('Pickup Seeds',
                                         'How many seeds to pick up?',
                                         default=None)
        if nbr <= 0 or max_seeds >= nbr:
            return False

        hold.nbr = nbr
        hold.owner = owner
        return True


hold = Holding()


def game_mode_ok():
    """Is it ok to return to game mode from move mode."""

    return not hold.nbr


# %%  Behavior Interface

class BehaviorIf(abc.ABC):
    """Button behavior interface."""

    def __init__(self, button):
        self.btn = button

    @abc.abstractmethod
    def set_props(self, props, disable, cactive):
        """Set text, props and states of the hole."""

    @abc.abstractmethod
    def left_click(self):
        """Do the left click action."""

    @abc.abstractmethod
    def right_click(self):
        """Do the right click action"""


# %%    Behaviors

class PlayButtonBehave(BehaviorIf):
    """The button behavior during game play."""


    def set_props(self, props, disable, cactive):
        """Set the number of seeds and properties, then refresh the hole.

        active_color: boolean - color as though active (even if it's not)
        disable: boolean - should the user be able to select the button
        (always no for AI)"""

        self.btn.props = props
        self._refresh(disable, cactive)


    def left_click(self):
        """Tell parent to move.
        If bidir is true, the move must be a tuple.
        If the user isn't selecting the direction, it's determined
        someplace else (e.g. get_direction) so use None."""
        if self.btn.bidir:
            if self.btn.dirs:
                self.btn.game_ui.move(MoveTpl(self.btn.pos, self.btn.dirs[0]))
            else:
                self.btn.game_ui.move(MoveTpl(self.btn.pos, None))
        else:
            self.btn.game_ui.move(self.btn.pos)


    def right_click(self):
        """If user can choose direction;
        player right click goes counter-clockwise"""

        if self.btn.bidir and self.btn.dirs:
            self.btn.game_ui.move(MoveTpl(self.btn.pos, self.btn.dirs[1]))


    def _refresh(self, disable=False, cactive=True):
        """Set text, props and states."""

        if self.btn.props.blocked:
            self.btn['text'] = 'x'

        else:
            otext = ''
            if self.btn.props.ch_owner is True:
                otext = '\u02c4'
            elif self.btn.props.ch_owner is False:
                otext = '\u02c5'

            if self.btn.props.seeds:
                self.btn['text'] = otext + str(self.btn.props.seeds)
            else:
                self.btn['text'] = otext + ''

        if not self.btn.props.unlocked:
            self.btn['relief'] = 'ridge'
        else:
            self.btn['relief'] = 'raised'

        if cactive:
            self.btn['background'] = 'SystemButtonFace'
        else:
            self.btn['background'] = 'grey80'

        if disable:
            self.btn['state'] = 'disabled'
        else:
            self.btn['state'] = 'normal'


class RndSetupButtonBehave(BehaviorIf):
    """Button behavior interface."""

    def set_props(self, props, _1, _2):
        """Set text, props and states of the hole."""
        self.btn.props = props
        self._refresh()

    def left_click(self):
        """Drop any held seeds, update the game_board and button.
        Don't dropw seeds if:
            1. there are already seeds in the hold
            2. there are no seeds in the hold
            3. the seeds are being dropped on the wrong side of the board
               from which they were picked up."""

        if self.btn.props.seeds or not hold.nbr:
            return

        if (hold.owner is True
                and self.btn.pos < self.btn.game_ui.game.cts.holes
            or hold.owner is False
                and self.btn.pos >= self.btn.game_ui.game.cts.holes):
            self.btn.bell()
            return

        # TODO game references are not in the GameInterface
        self.btn.game_ui.game.board[self.btn.pos] = hold.nbr
        self.btn.game_ui.game.blocked[self.btn.pos] = False
        self.btn.props.blocked = False
        self.btn.props.seeds = hold.nbr
        self._refresh()
        hold.empty()
        self.btn.frame.config(cursor='')


    def right_click(self):
        """Pick up all of the seeds will be nbr_start."""

        if not self.btn.props.seeds:
            self.btn.bell()
            return

        hold.nbr = self.btn.props.seeds
        hold.owner = self.btn.pos >= self.btn.game_ui.game.cts.holes

        self.btn.game_ui.game.board[self.btn.pos] = 0
        self.btn.game_ui.game.blocked[self.btn.pos] = True
        self.btn.props.blocked = True
        self.btn.props.seeds = 0
        self._refresh()
        self.btn.frame.config(cursor='circle')


    def _refresh(self):
        """Make the UI match the behavior and game data."""

        self.btn['background'] = MOVE_COLOR
        self.btn['state'] = 'normal'

        if self.btn.props.blocked:
            self.btn['text'] = 'x'

        elif self.btn.props.seeds:
            self.btn['text'] = str(self.btn.props.seeds)
        else:
            self.btn['text'] = ''


# %%  Button Class

class HoleButton(tk.Button):
    """Implements a single hole on the board."""

    def __init__(self, pframe, game_ui, position, bi_data=(False, None)):
        """Create button.
        game_ui: link to parent game UI
        position 0 .. ? left to right.
        bidir : boolean - a game property, must be the same for
            all holes in a game
        dirs: list - if this button supports multiple directions
            [left_dir, right_dir]"""

        self.frame = pframe
        self.game_ui = game_ui
        self.pos = position
        self.bidir = bi_data[0]
        self.dirs = bi_data[1]
        self.props = 0
        self.behavior = PlayButtonBehave(self)

        tk.Button.__init__(self, pframe, borderwidth=2, height=3, width=10,
                           text='',
                           disabledforeground='black', foreground='black',
                           anchor='center', font='bold',
                           command=self.left_click)

        self.bind('<Button-3>', self.right_click)


    def set_behavior(self, behave):
        """Set the behavior of the button."""

        if behave == Behavior.GAMEPLAY:
            self.behavior = PlayButtonBehave(self)

        elif behave == Behavior.RNDSETUP:
            self.behavior = RndSetupButtonBehave(self)

        hold.empty()

    def set_props(self, props, disable, cactive):
        """pass along set_props call."""
        self.behavior.set_props(props, disable, cactive)


    def left_click(self):
        """pass along left_click call."""
        self.behavior.left_click()


    def right_click(self, _=None):
        """pass along right_click call."""
        self.behavior.right_click()
