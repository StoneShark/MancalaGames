# -*- coding: utf-8 -*-
"""The Holebutton and StoreButton classes for Mancala UI with
states that allow the buttons to behave differently in different
game states.

Created on Sun Aug 13 10:06:37 2023
@author: Ann"""

import abc
import enum

import tkinter as tk

from game_interface import MoveTpl


# TODO board and blocked are being referenced directly not via GameInterface


# %%  constants

SYSTEM_COLOR = 'SystemButtonFace'
PLAY_INACTIVE_COLOR = 'grey80'
MOVE_COLOR = 'lightblue'
SEED_COLOR = 'light yellow'

YES_STR = 'yes'
NO_STR = 'no'


# %%  global data for mover

class Hold:
    """Global data to store the seed holding data.

    This is not intended to be instatiated or used outside this file."""

    nbr = 0
    owner = None

    # for the popup
    _top = None
    _game_ui = None
    _label = None


    @staticmethod
    def set_hold(nbr, owner):
        """Set the hold data and update the UI label"""
        Hold.nbr = nbr
        Hold.owner = owner
        Hold._label.config(text=f'Seeds: {Hold.nbr}\nRow: {Hold.owner}')


    @staticmethod
    def empty():
        """Remove seeds and owner."""
        Hold.nbr = 0
        Hold.owner = None
        if Hold._label:
            Hold._label.config(text=f'Seeds: {Hold.nbr}\nRow: na')


    @staticmethod
    def query_nbr_seeds(owner, max_seeds):
        """Get the number of seeds from the user.
        Store them in the hold, but the board is not updated."""

        if max_seeds == 1:
            Hold.set_hold(Hold.nbr + 1, owner)
            return 1

        nbr = tk.simpledialog.askinteger('Pickup Seeds',
                                         'How many seeds to pick up?')
        if not nbr or nbr <= 0 or nbr > max_seeds:
            Hold._game_ui.bell()
            return 0

        Hold.set_hold(Hold.nbr + nbr, owner)
        return nbr


    @staticmethod
    def hold_menu(game_ui):
        """Popup the hold window."""

        if Hold._top:
            return

        Hold._game_ui = game_ui

        xpos = game_ui.winfo_rootx() + game_ui.winfo_width() + 20
        ypos = game_ui.winfo_rooty()

        Hold._top = tk.Toplevel(game_ui)
        Hold._top.wm_overrideredirect(1)
        Hold._top.resizable(False, False)
        Hold._top.title('Seed Hold')
        Hold._top.wm_geometry(f'+{xpos}+{ypos}')
        Hold._top.minsize(200, 100)

        frame = tk.Frame(Hold._top,
                         relief=tk.SOLID,
                         borderwidth=1)
        frame.pack(side='top', expand=True, fill='both')

        text = 'Right to pick seeds up.\n' + \
               'Left to drop seeds from the hold.\n\n'
        tk.Label(frame, anchor='nw', justify='left', text=text
                 ).pack(side='top', expand=True, fill='both')

        text = f'Seeds: {Hold.nbr}\nRow: {Hold.owner}'
        Hold._label = tk.Label(frame, anchor='nw', justify='left', text=text)
        Hold._label.pack(side='top', expand=True, fill='both')
        tk.Button(frame, text='Done', command=Hold.done
                  ).pack(side='bottom')


    @staticmethod
    def done():
        """Go back to game play mode."""

        if Hold._game_ui.set_game_mode(Behavior.GAMEPLAY):
            Hold._top.destroy()
            Hold._label = None
            Hold._top = None


    @staticmethod
    def cleanup():
        """Abandoning the game mode, cleanup."""

        Hold.empty()
        Hold._top.destroy()
        Hold._label = None
        Hold._top = None


# %%  Behavior Interface

class BehaviorIf(abc.ABC):
    """Button behavior interface."""

    def __init__(self, button):
        self.btn = button

    @classmethod
    @abc.abstractmethod
    def ask_mode_change(cls, game_ui):
        """If the user should be asked to cnsent to the mode
        change, do so. Return True if the mode change is
        ok, False otherwise."""

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

class PlayButtonBehavior(BehaviorIf):
    """The button behavior during game play."""

    @classmethod
    def ask_mode_change(cls, game_ui):
        """The hold must be empty.
        Note: if the game is going to be reset (e.g. end game
        or new game) this wont even be called."""

        if Hold.nbr:
            tk.messagebox.showerror(
                title='Game Mode',
                message='Hold is not empty;'
                'place seeds before returning to game mode.',
                parent=game_ui)
            return False
        return True


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


class RndSetupButtonBehavior(BehaviorIf):
    """Round setup behavior. All occupied holes must have the
    start number of seeds in them. Right click picks them all up
    and left click drops them all."""

    @classmethod
    def ask_mode_change(cls, game_ui):

        if not any(game_ui.game.blocked):
            return False

        ans = tk.messagebox.askquestion(
            title='Move seeds',
            message='A new round is begining so you may change\n'
                    'the occupied holes on each side of the board.\n\n'
                    'A right click picks up seeds.\n'
                    'A left click drops those seeds.\n'
                    'Use Round -> Start Round to play.\n\n'
                    'Do you wish to move any seeds?',
                    parent=game_ui)

        if ans == YES_STR:
            Hold.hold_menu(game_ui)
            return True
        return False


    def set_props(self, props, _1, _2):
        """Set text, props and states of the hole."""
        self.btn.props = props
        self._refresh()


    def left_click(self):
        """Drop any held seeds, update the game_board and button.
        Don't drop seeds if:
            1. there are no seeds in the hold
            2. there are already seeds in the hole
            3. the seeds are being dropped on the wrong side of the board
               from which they were picked up."""

        if not Hold.nbr or self.btn.props.seeds or Hold.owner != self.btn.row:
            self.btn.bell()
            return

        loc = self.btn.game_ui.game.cts.pos_to_loc(self.btn.row,
                                                   self.btn.pos)

        self.btn.game_ui.game.board[loc] = Hold.nbr
        self.btn.game_ui.game.blocked[loc] = False
        self.btn.props.blocked = False
        self.btn.props.seeds = Hold.nbr
        self._refresh()
        Hold.empty()
        self.btn.frame.config(cursor='')


    def right_click(self):
        """Pick up all of the seeds in the hole,
        unless we are already holding seeds
        or there are not any seeds to pick up."""

        if Hold.nbr or not self.btn.props.seeds:
            self.btn.bell()
            return

        Hold.set_hold(self.btn.props.seeds, self.btn.row)

        loc = self.btn.game_ui.game.cts.pos_to_loc(self.btn.row,
                                                   self.btn.pos)
        self.btn.game_ui.game.board[loc] = 0
        self.btn.game_ui.game.blocked[loc] = True
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


class MoveSeedsButtonBehavior(BehaviorIf):
    """Move Seeds behavior. The seeds may be rearranged as
    desired."""

    @classmethod
    def ask_mode_change(cls, game_ui):

        ans = tk.messagebox.askquestion(
            title='Move seeds',
            message='At the start of this game you may  rearrange seeds\n'
            'on your side of the board. Your opponents seeds\n'
            'will be arrangedd the same.\n\n'
            'Rearranging seeds counts as your first move.\n\n'
            'A right click will query how many seeds to pick (or\n'
            'pick-up a single seed).\n'
            'A left click will drop any seeds held.\n'
            'Do you wish to move any seeds?\n',
            parent=game_ui)

        if ans == YES_STR:
            Hold.hold_menu(game_ui)
            return True
        return False


    def set_props(self, props, _1, _2):
        """Set text, props and states of the hole."""
        self.btn.props = props
        self._refresh()


    def left_click(self):
        """Drop any held seeds, update the game_board and button.
        Don't drop seeds if:
            1. there are no seeds in the hold
            2. the seeds are being dropped on the wrong side of the board
               from which they were picked up."""

        if not Hold.nbr or Hold.owner != self.btn.row:
            self.btn.bell()
            return
        loc = self.btn.game_ui.game.cts.pos_to_loc(self.btn.row,
                                                   self.btn.pos)

        self.btn.game_ui.game.board[loc] += Hold.nbr
        self.btn.props.seeds = self.btn.game_ui.game.board[loc]
        self._refresh()
        Hold.empty()
        self.btn.frame.config(cursor='')


    def right_click(self):
        """Pick up some or all of the seeds."""

        if (not self.btn.props.seeds
                or Hold.owner not in (None, self.btn.row)):
            self.btn.bell()
            return

        max_seeds = self.btn.props.seeds
        seeds = Hold.query_nbr_seeds(self.btn.row, max_seeds)

        if seeds:

            loc = self.btn.game_ui.game.cts.pos_to_loc(self.btn.row,
                                                       self.btn.pos)
            self.btn.game_ui.game.board[loc] -= seeds
            self.btn.props.seeds = self.btn.game_ui.game.board[loc]
            self._refresh()
            self.btn.frame.config(cursor='circle')


    def _refresh(self):
        """Make the UI match the behavior and game data."""

        self.btn['background'] = SEED_COLOR
        self.btn['state'] = 'normal'

        if self.btn.props.blocked:
            self.btn['text'] = 'x'

        elif self.btn.props.seeds:
            self.btn['text'] = str(self.btn.props.seeds)
        else:
            self.btn['text'] = ''


# %% enum, class list and global function

class Behavior(enum.IntEnum):
    """Enum for the button behaviors."""

    GAMEPLAY = 0
    RNDSETUP = 1
    MOVESEEDS = 2


BEHAVIOR_CLASS = (PlayButtonBehavior,
                  RndSetupButtonBehavior,
                  MoveSeedsButtonBehavior)


def ask_mode_change(behavior, game_ui):
    """Call the ask_mode_change for the specified behavior.
    Return it's result."""

    return BEHAVIOR_CLASS[behavior].ask_mode_change(game_ui)


def force_mode_change():
    """Do any cleanup because the mode change will be forced."""

    Hold.cleanup()

# %%  Button Class


class HoleButton(tk.Button):
    """Implements a single hole on the board."""

    def __init__(self, pframe, game_ui, row, position,
                 bidir=False, dirs=None):
        """Create button.
        game_ui: link to parent game UI
        position 0 .. ? left to right.
        side: False for bottom, True for top (some behaviors need this)
        bidir : boolean - a game property, must be the same for
            all holes in a game
        dirs: list - if this button supports multiple directions
            [left_dir, right_dir]"""
        # pylint: disable=too-many-arguments

        self.frame = pframe
        self.game_ui = game_ui
        self.pos = position
        self.row = row
        self.bidir = bidir
        self.dirs = dirs
        self.props = 0
        self.behavior = PlayButtonBehavior(self)

        tk.Button.__init__(self, pframe, borderwidth=2, height=3, width=10,
                           text='',
                           disabledforeground='black', foreground='black',
                           anchor='center', font='bold',
                           command=self.left_click)

        self.bind('<Button-3>', self.right_click)


    def set_behavior(self, behavior):
        """Set the behavior of the button."""

        self.behavior = BEHAVIOR_CLASS[behavior](self)
        Hold.empty()


    def set_props(self, props, disable, cactive):
        """Pass along set_props call."""
        self.behavior.set_props(props, disable, cactive)


    def left_click(self):
        """Pass along left_click call."""
        self.behavior.left_click()


    def right_click(self, _=None):
        """Pass along right_click call.
        Don't care about the possible event parameter."""
        self.behavior.right_click()
