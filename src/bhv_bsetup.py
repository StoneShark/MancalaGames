# -*- coding: utf-8 -*-
"""Allow free setup of the board, e.g. for problem solving.

Seeds maybe moved and children, owners, locks and blocks
may be changed.

There are only a few checks to keep the board valid,
a few examples of possible errors:

    - children maybe put in places the game does not
      allow them.

    - a game with only even captures can have an odd
      number of seeds placed in a store.

    - win conditions may already be met for a game.

There are some game states items that are maybe not handled
the best, but more UI options would be required:

    - mcount is reset to 2
        + sow opp dirs will reaquire sow directions
          on the first move
        + current prescribed openings only apply to
          the first turn

    - the inhibitor is always turned off

    - the ai player history is not cleared

    - something else not anticipated :)

Created on Tue Mar 11 09:02:11 2025
@author: Ann"""


import tkinter as tk
import textwrap

import behaviors as bhv
import bhv_hold
import game_interface as gi
import man_config
import ui_utils


class SetupHold(bhv_hold.Hold):
    """Global data to store and manage the seed holding data.

    Built on bhv_hold.Hold, with the following diffs:
        - owner isn't used
        - tally rframe is filled differently
        - a few control buttons are put in tally rframe
        - there are implementations of those operations

    This data is shared between each of the behavior objects
    created for the board (holes and stores).

    Only one global instance is created."""

    def __init__(self):

        super().__init__()
        self._label = False


    def set_hold(self, nbr, _):
        """Set the hold data and update the UI label"""
        self.nbr = nbr
        self._label.config(text=f'Seeds held: {self.nbr}')


    def empty(self):
        """Remove seeds and owner."""
        self.nbr = 0
        if self._label:
            self._label.config(text=f'Seeds held: {self.nbr}')


    def destroy_ui(self):
        """Don't keep local copies of ui elements that are
        destroyed."""

        super().destroy_ui()
        self._label = None


    def hold_menu(self, game_ui, _=None):
        """Fill the right status frame with controls."""

        self.active = True
        self.game_ui = game_ui
        frame = game_ui.rframe

        text = textwrap.fill(textwrap.dedent(
                    """\
                    Setup the board.
                    There is no check that a given setup is allowed
                    by the game (e.g. children in disallowed places).
                    The game must be left playable by the starter."""),
                    width=bhv.FILL_HINTS)
        text += '\n\n'
        text += textwrap.fill(textwrap.dedent(
                    """\
                    Right click:
                    If children, blocks, locks, or owners are used
                    right click popups a menu of options. Otherwise,
                    the right click picks up seeds."""),
                    width=bhv.FILL_HINTS)
        text += '\n\n'
        text += "Left click to drop seeds any seeds held."

        tk.Label(frame, anchor='nw', justify='left', text=text
                 ).pack(side='top', expand=True, fill='both')

        text = f'Seeds: {self.nbr}'
        self._label = tk.Label(frame, anchor='nw', justify='left', text=text)
        self._label.pack(side='top', expand=True, fill='both')

        tframe = tk.Frame(frame)
        rcnt = ui_utils.Counter()
        ccnt = ui_utils.Counter()
        row = rcnt.count

        tk.Button(tframe, text="Top's Turn",
                  command=self.set_starter_true).grid(
                      row=row, column=ccnt.count, padx=2, pady=2, sticky='ew')
        tk.Button(tframe, text="Bottom's Turn",
                  command=self.set_starter_false).grid(
                      row=row, column=ccnt.count, padx=2, pady=2, sticky='ew')
        tk.Button(tframe, text="Rotate Board",
                  command=self.rotate_board).grid(
                      row=row, column=ccnt.count, padx=2, pady=2, sticky='ew')
        row = rcnt.count
        ccnt.reset()
        tk.Button(tframe, text="Initial Setup",
                  command=self.init_setup).grid(
                      row=row, column=ccnt.count, padx=2, pady=2, sticky='ew')
        tk.Button(tframe, text="Clear to Stores",
                  command=self.clear_to_stores).grid(
                      row=row, column=ccnt.count, padx=2, pady=2, sticky='ew')

        tframe.pack(side='top')

        tk.Button(frame, text='Done', command=self.done
                  ).pack(side='bottom', padx=2, pady=2)


    def set_starter_true(self):
        """Set the starter to True and do board refresh."""

        self.game_ui.game.starter = self.game_ui.game.turn = True
        self.game_ui.refresh()


    def set_starter_false(self):
        """Set the starter to False and do board refresh."""

        self.game_ui.game.starter = self.game_ui.game.turn = False
        self.game_ui.refresh()


    def clear_to_stores(self):
        """Move the seeds to the stores and do board refresh.
        Don't do anything if the stores aren't on the UI."""

        if not self.game_ui.stores:
            self.game_ui.bell()
            return

        quot, rem = divmod(self.game_ui.game.cts.total_seeds , 2)

        store = self.game_ui.game.store
        store[0] = quot + rem
        store[1] = quot

        board = self.game_ui.game.board
        for i, _ in enumerate(board):
            board[i] = 0

        self.game_ui.refresh()

        # the UI has games in which the stores are visible but always
        # have 0 in them (used to show whose turn it is)
        ui_stores = self.game_ui.stores
        if ui_stores:
            # stores are in game_ui.stores by row
            ui_stores[0].set_store(store[1], None)
            ui_stores[1].set_store(store[0], None)


    def init_setup(self):
        """Reset the game to the initial setup and clear the
        inhibitor."""

        self.game_ui.game.new_game()
        self.game_ui.game.inhibitor.set_off()
        self.game_ui.game.mcount = 2
        self.game_ui.refresh()


    def rotate_board(self):
        """Rotate the board.
        AI can only play True."""

        self.game_ui.game.swap_sides()
        self.game_ui.refresh()


SETUPHOLD = SetupHold()


# %% behaviors

class SetupButtonBehavior(bhv.BehaviorIf):
    """Setup the board.
    The only limit is that the game must be playable
    by the starter."""


    def __init__(self, button):

        super().__init__(button)
        self.saved_state = None
        self.game_ui = None


    @classmethod
    def ask_mode_change(cls, game_ui):
        """Setup was requested always allow."""

        message = "Do you wish to enter board setup mode?\n\n" \
                   + textwrap.dedent("""\
                        The current game will not be tallied,
                        the inhibitor will be turned off,
                        move count will be reset to 2
                        (no prescribed openings will occur),
                        and knowledge gained by AI player
                        is not cleared.""")

        do_it = tk.messagebox.askokcancel(
            title='Board Setup',
            message=message,
            parent=game_ui)

        if not do_it:
            return False

        SETUPHOLD.hold_menu(game_ui)
        game_ui.game.inhibitor.set_off()
        game_ui.game.mcount = 2

        return True


    @classmethod
    def leave_mode(cls, game_ui):
        """Test if it's ok to leave setup mode."""

        if SETUPHOLD.warn_not_empty(game_ui):
            return False

        if not any(game_ui.game.get_allowable_holes()):
            tk.messagebox.showerror(
                title='Game Mode',
                message='The game is not playable.',
                parent=game_ui)
            return False

        game_ui.setup.save_setup()
        return True


    def do_left_click(self):
        """Drop any held seeds, update the game_board and button."""

        if not SETUPHOLD.nbr:
            self.btn.bell()
            return

        game = self.btn.game_ui.game
        seeds = game.board[self.btn.loc] + SETUPHOLD.nbr
        self.btn.props.seeds = seeds
        game.board[self.btn.loc] = seeds
        self.refresh()

        SETUPHOLD.empty()
        self.btn.game_ui.config(cursor='')


    def do_popup_menu(self):
        """Build the right click menu.
        Only include the options that apply to the game.

        XXXX Should this popup only be created in once and
        reused? The problem is that we don't have game UI when
        this class is instantiated and ask_mode_change is class
        scope so we don't exit yet. There isn't any other
        behavior interface that gets the game_ui."""

        game_ui = self.btn.game_ui
        ginfo = game_ui.game.info

        menubar = tk.Menu(game_ui)
        menubar.add_command(label='Pickup Seeds', command=self.pickup)
        if ginfo.child_type:
            menubar.add_command(label='Child Cycle', command=self.child_cycle)
        if ginfo.goal == gi.Goal.TERRITORY:
            menubar.add_command(label='Owner Toggle', command=self.owner_toggle)
        if ginfo.blocks:
            menubar.add_command(label='Block Toggle', command=self.block_toggle)
        if (ginfo.moveunlock
                or ginfo.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST):
            menubar.add_command(label='Lock Toggle', command=self.lock_toggle)

        button = self.btn
        xpos = button.winfo_rootx() + 20
        ypos = button.winfo_rooty() + 20

        menubar.post(xpos, ypos)


    def pickup(self):
        """Pickup seeds from the hole."""

        if not self.btn.props.seeds:
            self.btn.bell()
            return

        seeds = SETUPHOLD.query_nbr_seeds(None, self.btn.props.seeds)
        self.remove_seeds(seeds)
        self.btn.game_ui.config(cursor='circle')


    @staticmethod
    def cycle(value):
        """Cycle the value through N, F, T"""

        if value:
            return None
        if value is None:
            return False
        return True


    def child_cycle(self):
        """Cycle the child throug N, F, T"""

        game = self.btn.game_ui.game
        loc = self.btn.loc
        game.child[loc] = self.cycle(game.child[loc])
        self.btn.props.ch_owner = game.child[loc]
        self.refresh()


    def owner_toggle(self):
        """Toggle the owner and the active saved status of the button"""

        game = self.btn.game_ui.game
        loc = self.btn.loc
        game.owner[loc] = not game.owner[loc]
        self.btn.props.owner = game.owner[loc]

        if self.saved_state == bhv.BtnState.ACTIVE:
            self.saved_state = bhv.BtnState.DISABLE
        else:
            self.saved_state = bhv.BtnState.ACTIVE
        self.refresh()


    def block_toggle(self):
        """Toggle the blocked status."""

        game = self.btn.game_ui.game
        loc = self.btn.loc

        if game.board[loc]:
            tk.messagebox.showerror(
                title='Block',
                message='Remove the seeds from the hole before blocking it.',
                parent=self.btn.game_ui)
            return

        game.blocked[loc] = not game.blocked[loc]
        self.btn.props.blocked = game.blocked[loc]
        self.refresh()


    def lock_toggle(self):
        """Toggle the blocked status."""

        game = self.btn.game_ui.game
        loc = self.btn.loc
        game.unlocked[loc] = not game.unlocked[loc]
        self.btn.props.unlocked = game.unlocked[loc]
        self.refresh()


    def do_right_click(self):
        """If there is more than one setup operation, popup
        the a menu of options. Otherwise, pickup seeds."""

        game_ui = self.btn.game_ui
        ginfo = game_ui.game.info

        if any([ginfo.child_type,
                ginfo.goal == gi.Goal.TERRITORY,
                ginfo.blocks,
                ginfo.moveunlock,
                ginfo.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST]):

            self.do_popup_menu()

        else:
            self.pickup()


    def refresh(self, bstate=None):
        """Refresh the button as in play mode
        but then override the state to normal."""

        if bstate is None:
            if self.saved_state is None:
                bstate = bhv.BtnState.ACTIVE
            else:
                bstate = self.saved_state
        self.saved_state = bstate

        self.refresh_play(bstate)

        self.btn['state'] = tk.NORMAL


class SetupStoreBehavior(bhv.StoreBehaviorIf):
    """Behavior for the board setup mode.

    Remember game.set(get)_store takes a row not a turn or owner"""

    def set_store(self, seeds, highlight):
        """Set the properties of the store button.
        Seeds are always visible even if they aren't during game play"""

        self.str['state'] = tk.NORMAL
        self.str['text'] = str(seeds)

        if highlight is not None:
            if highlight:
                self.str['background'] = man_config.CONFIG['turn_color']
            else:
                self.str['background'] = man_config.CONFIG['system_color']


    def do_left_click(self):
        """Drop all picked up seeds."""

        if not SETUPHOLD.nbr:
            self.str.bell()
            return

        game = self.str.game_ui.game
        seeds = game.store[self.str.owner] + SETUPHOLD.nbr
        self.set_store(seeds, game.turn == self.str.owner)
        game.store[self.str.owner] = seeds

        self.str.game_ui.config(cursor='')
        SETUPHOLD.empty()


    def do_right_click(self):
        """Pop up the nbr seeds query, and pickup seeds if
        the user entered a valid number."""

        game = self.str.game_ui.game

        if not game.store[self.str.owner]:
            self.str.bell()
            return

        seeds = game.store[self.str.owner]

        if SETUPHOLD.query_nbr_seeds(None, seeds):

            game = self.str.game_ui.game
            seeds -= SETUPHOLD.nbr
            self.set_store(seeds, game.turn == self.str.owner)
            game.store[self.str.owner] = seeds

            self.str.game_ui.config(cursor='circle')
