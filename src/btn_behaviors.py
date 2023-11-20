# -*- coding: utf-8 -*-
"""The Holebutton and StoreButton classes for Mancala UI with
states that allow the buttons to behave differently in different
game states.

Created on Sun Aug 13 10:06:37 2023
@author: Ann"""

import abc
import collections
import enum
import textwrap

import tkinter as tk


# %%  constants

SYSTEM_COLOR = 'SystemButtonFace'
PLAY_INACTIVE_COLOR = 'grey80'
TURN_COLOR = 'lightblue'
CHOOSE_COLOR = 'pink2'
SEED_COLOR = 'light yellow'
MOVE_COLOR = 'sandy brown'

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

        nbr = tk.simpledialog.askinteger(
            'Pickup Seeds',
            f'How many seeds to pick up (1 .. {max_seeds})?')
        if not nbr or nbr <= 0 or nbr > max_seeds:
            Hold._game_ui.bell()
            return 0

        Hold.set_hold(Hold.nbr + nbr, owner)
        return nbr


    @staticmethod
    def hold_menu(game_ui, message=None):
        """Fill the right status frame with controls."""

        if Hold._top:
            return

        Hold._game_ui = game_ui
        frame = game_ui.rframe

        text = 'Right click to pick seeds up.\n' + \
               'Left click to drop seeds from the hold.\n'
        if message:
            text = message + '\n' + text

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
            for child in Hold._game_ui.rframe.winfo_children():
                child.destroy()


    @staticmethod
    def cleanup():
        """Abandoning the game mode, cleanup."""

        Hold.empty()
        for child in Hold._game_ui.rframe.winfo_children():
            child.destroy()


# %%  Interfaces

class BehaviorIf(abc.ABC):
    """Button behavior interface.

    The button behavior class is sort of the master in determining when
    ok to leave and enter behaviors."""

    def __init__(self, button):
        self.btn = button

    @classmethod
    @abc.abstractmethod
    def ask_mode_change(cls, game_ui):
        """If the user should be asked to consent to the mode
        change, do so. Return True if the mode change is
        ok, False otherwise.

        class method because this is called before the object
        is instantiated."""

    @classmethod
    def leave_mode(cls, game_ui):
        """Is it ok to leave the mode (presumably to go back to GAMEPLAY).
        Assume it is unless this is overridden.

        class method to access any class scope vars set in ask_mode_change."""
        _ = game_ui
        return True

    @abc.abstractmethod
    def set_props(self, props, disable, cactive):
        """Set text, props and states of the hole."""

    @abc.abstractmethod
    def left_click(self):
        """Do the left click action."""

    @abc.abstractmethod
    def right_click(self):
        """Do the right click action"""


class StoreBehaviorIf(abc.ABC):
    """Store behavior interface."""

    def __init__(self, store):
        self.str = store

    @abc.abstractmethod
    def set_store(self, seeds, highlight):
        """Set text, props and states of the store."""

    @abc.abstractmethod
    def left_click(self):
        """Do the left click action."""

    @abc.abstractmethod
    def right_click(self):
        """Do the right click action"""


# %%    Hole Behaviors

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
        """Tell parent to move."""
        self.btn.game_ui.move(self.btn.left_move)


    def right_click(self):
        """Move for the right click -- unless the hole is udirect
        this is the same as a left click"""
        if self.btn['state'] == tk.DISABLED:
            return

        self.btn.game_ui.move(self.btn.right_move)


    def _refresh(self, disable=False, cactive=True):
        """Set text, props and states."""
        # pylint: disable=too-many-branches

        if self.btn.props.blocked:
            self.btn['text'] = 'x'

        else:
            otext = ''
            if self.btn.props.ch_owner is True:
                otext += '\u02c4 '
            elif self.btn.props.ch_owner is False:
                otext += '\u02c5 '

            if self.btn.props.owner is True:
                otext += '\u2191 '
            elif self.btn.props.owner is False:
                otext += '\u2193 '

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
            self.btn['state'] = tk.DISABLED
        else:
            self.btn['state'] = tk.NORMAL


class RndChooseButtonBehavior(BehaviorIf):
    """Round setup behavior. Choose which holes are blocked.

    Moving seeds is enabled on the side with blocked holes."""

    @classmethod
    def ask_mode_change(cls, game_ui):

        if not any(game_ui.game.blocked):
            return False

        ans = tk.messagebox.askquestion(
            title='Move seeds',
            message=textwrap.fill(textwrap.dedent("""\
                A new round is begining, so you may
                change the blocked holes on the loser's of the
                board. Do you wish to
                rearrange the blocks?"""), width=50),
                    parent=game_ui)

        if ans != YES_STR:
            return False

        Hold.hold_menu(game_ui,
                       'Move seeds out of holes you wish to block.')

        cls.starter = game_ui.game.turn
        loser = any(game_ui.game.blocked[l]
                    for l in range(game_ui.game.cts.holes,
                                   game_ui.game.cts.dbl_holes))
        game_ui.game.turn = loser
        return True


    @classmethod
    def leave_mode(cls, game_ui):

        # revert to the round starter that was saved
        game_ui.game.turn = cls.starter
        return True


    def set_props(self, props, disable, _2):
        """Set text, props and states of the hole."""
        self.btn.props = props
        # print(self.btn.row, self.btn.loc, disable, props.blocked)
        self._refresh(disable != props.blocked)


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

        game = self.btn.game_ui.game
        game.set_board(self.btn.loc, Hold.nbr)
        game.set_blocked(self.btn.loc, False)

        self.btn.props.blocked = False
        self.btn.props.seeds = Hold.nbr
        self._refresh()

        Hold.empty()
        self.btn.frame.config(cursor='')


    def right_click(self):
        """Pick up all of the seeds in the hole,
        unless we are already holding seeds
        or there are not any seeds to pick up."""

        if self.btn['state'] == tk.DISABLED:
            return
        if Hold.nbr or not self.btn.props.seeds:
            self.btn.bell()
            return

        Hold.set_hold(self.btn.props.seeds, self.btn.row)

        game = self.btn.game_ui.game
        game.set_board(self.btn.loc, 0)
        game.set_blocked(self.btn.loc, True)

        self.btn.props.blocked = True
        self.btn.props.seeds = 0
        self._refresh()

        self.btn.frame.config(cursor='circle')


    def _refresh(self, disable=False):
        """Make the UI match the behavior and game data."""

        if disable:
            self.btn['background'] = 'SystemButtonFace'
            self.btn['state'] = tk.DISABLED
        else:
            self.btn['background'] = CHOOSE_COLOR
            self.btn['state'] = tk.NORMAL

        if self.btn.props.blocked:
            self.btn['text'] = 'x'

        elif self.btn.props.seeds:
            self.btn['text'] = str(self.btn.props.seeds)
        else:
            self.btn['text'] = ''



class RndMoveSeedsButtonBehavior(BehaviorIf):
    """Any number of seeds my placed on the board (by the loser)
    each hole must contain at least one seed. Extra seeds may be
    left in the store. Seeds cannot be moved from one side to
    the other.
    Winner's seeds will be arranged the same."""

    starter = None
    loser = None

    @classmethod
    def ask_mode_change(cls, game_ui):
        """If the user wants to enter move mode, need to collect
        some data; need to save it in the class.

        Save turn as the starter and set the turn to the loser.
        We know that new_game left the board sides equal,
        so we can compare the stores to determine the loser.

        Note that we never go into this move mode without going
        through this function and the leave_mode function can
        undo the local changes."""

        ans = tk.messagebox.askquestion(
            title='Move seeds',
            message=textwrap.fill(textwrap.dedent("""\
                  The loser may
                  arrange the playable seeds with the restrictions that each
                  hole contain at least one seed and one hole is playable.
                  Seeds maybe added or removed from the store.
                  The winner's seeds will be arranged the same way.
                  Do you wish to rearrange the seeds?"""), width=50),
            parent=game_ui)

        if ans != YES_STR:
            return False

        Hold.hold_menu(game_ui,
                       'Each hole must contain at least one seed and\n'
                       'one hole must be playable.')

        cls.starter = game_ui.game.turn
        cls.loser = game_ui.game.store[0] > game_ui.game.store[1]
        game_ui.game.turn = cls.loser

        return True


    @classmethod
    def leave_mode(cls, game_ui):

        game = game_ui.game
        holes = game.cts.holes
        dbl_holes = game.cts.dbl_holes

        if cls.loser:
            loser_slice = slice(holes, dbl_holes)
            winner_slice = slice(0, holes)
        else:
            loser_slice = slice(0, holes)
            winner_slice = slice(holes, dbl_holes)

        if not any(seeds >= game.info.min_move
                   for seeds in game.board[loser_slice]):
            tk.messagebox.showerror(
                title='Game Mode',
                message=textwrap.fill(textwrap.dedent(f"""\
                    None of the holes have min_moves seeds
                    ({game.info.min_move}); thus the game is not playable.
                    Move more seeds back from store."""), width=40),
                parent=game_ui)
            return False

        start_seeds = sum(game.board[winner_slice])
        game.board[winner_slice] = game.board[loser_slice]
        game.store[not cls.loser] += (start_seeds -
                                      sum(game.board[winner_slice]))

        # revert to the round starter that was saved
        game_ui.game.turn = cls.starter

        return True


    def set_props(self, props, disable, _2):
        """Set text, props and states of the hole.
        Because we set turn to the loser, disable will be set
        True for the loser."""
        self.btn.props = props
        self._refresh(disable)


    def left_click(self):
        """Drop any held seeds, update the game_board and button.
        Don't drop seeds if:
            1. there are no seeds in the hold
            2. the seeds are being dropped on the wrong side of the board
               from which they were picked up."""

        if not Hold.nbr or Hold.owner != self.btn.row:
            self.btn.bell()
            return

        game = self.btn.game_ui.game
        seeds = game.get_board(self.btn.loc) + Hold.nbr
        self.btn.props.seeds = seeds
        game.set_board(self.btn.loc, seeds)
        self._refresh()

        Hold.empty()
        self.btn.game_ui.config(cursor='')


    def right_click(self):
        """Pick up some or all of the seeds, but
            1. only on loser side (game.turn is winner, row is not turn;
                                   so loser row it game.turn)
            2. if there are seeds to pick up
            3. another condition that doesn't make sense at the moment !?!?!?

            Always leave at least one seed in each hole."""
        if self.btn['state'] == tk.DISABLED:
            return

        game = self.btn.game_ui.game
        if (game.turn == self.btn.row
                or not self.btn.props.seeds
                or Hold.owner not in (None, self.btn.row)):
            self.btn.bell()
            return

        max_seeds = self.btn.props.seeds - 1
        seeds = Hold.query_nbr_seeds(self.btn.row, max_seeds)

        if seeds:
            seeds = game.get_board(self.btn.loc) - seeds
            self.btn.props.seeds = seeds
            game.set_board(self.btn.loc, seeds)
            self._refresh()

            self.btn.game_ui.config(cursor='circle')


    def _refresh(self, disable=False):
        """Make the UI match the behavior and game data."""

        if disable:
            self.btn['background'] = 'SystemButtonFace'
            self.btn['state'] = tk.DISABLED
        else:
            self.btn['background'] = SEED_COLOR
            self.btn['state'] = tk.NORMAL

        if self.btn.props.blocked:
            self.btn['text'] = 'x'

        elif self.btn.props.seeds:
            self.btn['text'] = str(self.btn.props.seeds)
        else:
            self.btn['text'] = ''


class MoveSeedsButtonBehavior(BehaviorIf):
    """Move Seeds behavior. The seeds may be rearranged as
    desired by the first player though all seeds must be
    left in play. This movement counts as the player's turn.

    This is intended to be used for Bao"""

    @classmethod
    def ask_mode_change(cls, game_ui):

        ans = tk.messagebox.askquestion(
            title='Move seeds',
            message=textwrap.fill(textwrap.dedent("""\
                  At the start of this game you may rearrange seeds on
                  your side of the board. Your opponents seeds will be
                  arranged the same. Rearranging seeds counts as your
                  first move. Do you wish to move any
                  seeds?"""), width=50),
            parent=game_ui)

        if ans != YES_STR:
            return False

        # TODO save state and check for actual movement
        Hold.hold_menu(game_ui)
        return True


    @classmethod
    def leave_mode(cls, game_ui):

        game = game_ui.game
        holes = game.cts.holes
        dbl_holes = game.cts.dbl_holes

        if game.turn:
            moved_slice = slice(holes, dbl_holes)
            other_slice = slice(0, holes)
        else:
            moved_slice = slice(0, holes)
            other_slice = slice(holes, dbl_holes)
        game.board[other_slice] = game.board[moved_slice]

        # movement was the player's turn
        game.turn = not game.turn
        return True


    def set_props(self, props, disable, _2):
        """Set text, props and states of the hole."""
        self.btn.props = props
        self._refresh(disable)


    def left_click(self):
        """Drop any held seeds, update the game_board and button.
        Don't drop seeds if:
            1. there are no seeds in the hold
            2. the seeds are being dropped on the wrong side of the board
               from which they were picked up."""

        if not Hold.nbr or Hold.owner != self.btn.row:
            self.btn.bell()
            return

        game = self.btn.game_ui.game
        seeds = game.get_board(self.btn.loc) + Hold.nbr

        game.set_board(self.btn.loc, seeds)
        self.btn.props.seeds = seeds
        self._refresh()

        Hold.empty()
        self.btn.frame.config(cursor='')


    def right_click(self):
        """Pick up some or all of the seeds."""
        if self.btn['state'] == tk.DISABLED:
            return

        if (not self.btn.props.seeds
                or Hold.owner not in (None, self.btn.row)):
            self.btn.bell()
            return

        max_seeds = self.btn.props.seeds
        seeds = Hold.query_nbr_seeds(self.btn.row, max_seeds)

        if seeds:
            game = self.btn.game_ui.game
            seeds = game.get_board(self.btn.loc) - seeds

            game.set_board(self.btn.loc, seeds)
            self.btn.props.seeds = seeds
            self._refresh()

            self.btn.frame.config(cursor='circle')


    def _refresh(self, disable=False):
        """Make the UI match the behavior and game data."""

        if disable:
            self.btn['background'] = 'SystemButtonFace'
            self.btn['state'] = tk.DISABLED
        else:
            self.btn['background'] = MOVE_COLOR
            self.btn['state'] = tk.NORMAL

        if self.btn.props.seeds:
            self.btn['text'] = str(self.btn.props.seeds)
        else:
            self.btn['text'] = ''


# %% store behaviors


class NoStoreBehavior(StoreBehaviorIf):
    """Store behavior that has no interaction.
    Background color reflects the current turn."""

    def set_store(self, seeds, highlight):
        """Set the properties of the store button."""

        self.str['state'] = tk.DISABLED

        if seeds:
            self.str['text'] = str(seeds)
        else:
            self.str['text'] = ''

        self.str['background'] = TURN_COLOR if highlight else SYSTEM_COLOR

    def left_click(self):
        """No interaction, button disabled."""

    def right_click(self):
        """No interaction."""



class RndMoveStoreBehavior(StoreBehaviorIf):
    """Store behavior interface.

    Seeds may be moved in and out of the loser's store.
    Cursor is changed on the whole game_ui, when holding seeds.

    Remember game.set(get)_store take a row not a turn or owner"""

    def set_store(self, seeds, highlight):
        """Set the properties of the store button."""

        if highlight:
            self.str['state'] = tk.NORMAL
        else:
            self.str['state'] = tk.DISABLED

        if seeds:
            self.str['text'] = str(seeds)
        else:
            self.str['text'] = ''

        self.str['background'] =  SEED_COLOR if highlight else SYSTEM_COLOR


    def left_click(self):
        """Drop all picked up seeds."""

        if not Hold.nbr and Hold.owner == self.str.owner:
            self.str.bell()
            return

        game = self.str.game_ui.game
        seeds = game.get_store(not self.str.owner) + Hold.nbr
        self.set_store(seeds, True)
        game.set_store(not self.str.owner, seeds)

        self.str.game_ui.config(cursor='')
        Hold.empty()


    def right_click(self):
        """Pop up the nbr seeds query, and pickup seeds if
        the user entered a valid number."""

        game = self.str.game_ui.game
        seeds = game.get_store(not self.str.owner)

        if (game.turn == self.str.owner
                and Hold.query_nbr_seeds(not self.str.owner, seeds)):

            game = self.str.game_ui.game
            seeds -= Hold.nbr
            self.set_store(seeds, True)
            game.set_store(not self.str.owner, seeds)

            self.str.game_ui.config(cursor='circle')


# %% enum, class list and global function

class Behavior(enum.IntEnum):
    """Enum for the button behaviors."""

    GAMEPLAY = 0
    RNDCHOOSE = 1
    RNDMOVE = 2
    MOVESEEDS = 3


BTuples = collections.namedtuple('BTuples', ['button', 'store'])

BEHAVIOR_CLASS = (BTuples(PlayButtonBehavior, NoStoreBehavior),
                  BTuples(RndChooseButtonBehavior, NoStoreBehavior),
                  BTuples(RndMoveSeedsButtonBehavior, RndMoveStoreBehavior),
                  BTuples(MoveSeedsButtonBehavior, NoStoreBehavior))


def ask_mode_change(old_behavior, new_behavior, game_ui):
    """If leaving a non-GAMEPLAY behavior, ask the button class (master)
    if it's ok to leave (this might do some side effect operations).
    If current behavior says it's ok, ask the new behavior if it's ok,
    which generally asks the user when leaving GAMEPLAY."""

    if new_behavior == Behavior.GAMEPLAY:
        if not BEHAVIOR_CLASS[old_behavior].button.leave_mode(game_ui):
            return False

    return BEHAVIOR_CLASS[new_behavior].button.ask_mode_change(game_ui)


def force_mode_change():
    """Do any cleanup because the mode change will be forced."""

    Hold.cleanup()



# %%  Button Classes


class HoleButton(tk.Button):
    """Implements a single hole on the board."""

    def __init__(self, pframe, game_ui, loc, left_move, right_move):
        """Create button.
        loc is the index to use for get/set board/blocked.
        left and right move are the moves for left/right click"""
        # pylint: disable=too-many-arguments

        self.frame = pframe
        self.game_ui = game_ui
        self.loc = loc
        self.row = int(loc < self.game_ui.game.cts.holes)
        self.left_move = left_move
        self.right_move = right_move
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

        self.behavior = BEHAVIOR_CLASS[behavior].button(self)
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



class StoreButton(tk.Button):
    """Implements one of the board stores."""

    def __init__(self, pframe, game_ui, side, owner):
        """Build the store button"""

        self.game_ui = game_ui
        self.owner = owner
        self.behavior = NoStoreBehavior(self)

        tk.Button.__init__(self, pframe, borderwidth=2, height=3, width=8,
                           text='', padx=5, pady=10,
                           disabledforeground='black', foreground='black',
                           anchor='center', font='bold', relief='ridge',
                           command=self.left_click)
        self.pack(side=side)
        self.bind('<Button-3>', self.right_click)


    def set_behavior(self, behavior):
        """Set the behavior of the store."""
        self.behavior = BEHAVIOR_CLASS[behavior].store(self)


    def set_store(self, seeds, turn):
        """Set text, props and states of the store."""
        self.behavior.set_store(seeds, turn)


    def left_click(self):
        """pass along left_click call."""
        self.behavior.left_click()


    def right_click(self, _=None):
        """pass along right_click call."""
        self.behavior.right_click()
