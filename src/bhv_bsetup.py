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
        + current prescribed openings only apply to
          the first turn

    - the inhibitor is always turned off

    - the ai player history is cleared

    - something else not anticipated :)

Created on Tue Mar 11 09:02:11 2025
@author: Ann"""


import tkinter as tk
import textwrap

import behaviors as bhv
import bhv_hold
import game_info as gi
import get_direction
import ui_utils

from game_logger import game_log


SETUPHOLD = None


class PlayAltDirControl:
    """A class to  manage the player direction for
    PLAYALTDIR games.
    If the player directions have not been set, just pick
    some."""

    def __init__(self, game):

        deco = game.deco.get_dir
        while deco and not isinstance(deco, get_direction.PlayAltDir):
            deco = deco.decorator

        assert deco, "PlayAltDir is missing"

        self._deco = deco
        if not self._deco.player_dirs[0]:
            self._deco.player_dirs = [gi.Direct.CW, gi.Direct.CCW]

    def swap_dirs(self):
        """Swap the player directions."""

        self._deco.player_dirs = list(reversed(self._deco.player_dirs))

    @property
    def north_dir_text(self):
        """Return the button text with the north direction."""
        return "Swap North Sow Dir: " + self._deco.player_dirs[1].name


class SetupHold(bhv_hold.Hold):
    """Global data to store and manage the seed holding data.

    Built on bhv_hold.Hold, with the following diffs:
        - owner isn't used
        - tally rframe is filled differently
        - a few control buttons are put in tally rframe
        - there are implementations of those operations

    This data is shared between each of the behavior objects
    created for the board (1 each holes and stores).

    Only one global instance is created."""

    def __init__(self):

        super().__init__()

        self._label = False

        self._oop_btn = None
        self.out_of_play = 0

        self._altd_btn = None
        self.alt_dir_ctrl = None


    def set_hold(self, nbr, _=None):
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


    def add_sow_dir_if(self, game_ui, tframe, rcnt, ccnt):
        """If the game is PLAYALTDIR add the direction setting
        button. This also, forces the player directions to be
        set."""

        if game_ui.game.info.sow_direct == gi.Direct.PLAYALTDIR:

            self.alt_dir_ctrl = PlayAltDirControl(game_ui.game)

            self._altd_btn = tk.Button(
                tframe,
                text=self.alt_dir_ctrl.north_dir_text,
                command=self.swap_sow_dir)
            self._altd_btn.grid(row=rcnt.value, column=ccnt.count,
                                columnspan=2,
                                padx=2, pady=2, sticky='ew')

            ccnt.increment()


    def add_collect_button(self, game_ui, tframe, rcnt, ccnt):
        """Choose and build a collection option to move seeds
        together for easier setup:
            - off board out-of-play for eliminate games
            - clear to stores for other games with visible stores
            - move to leftmost for other games"""

        if not game_ui.show_seeds_in_stores():

            tk.Button(tframe, text="Clear Board",
                      command=self.clear_board).grid(
                          row=rcnt.value, column=ccnt.count,
                          padx=2, pady=2, sticky='ew')

            self.out_of_play = sum(self.game_ui.game.store)
            self.game_ui.game.store[0] = self.out_of_play
            self.game_ui.game.store[1] = 0

            self._oop_btn = tk.Button(tframe,
                                     text=f"Off board: {self.out_of_play}",
                                     command=self.add_seeds)
            self._oop_btn.grid(
                row=rcnt.value, column=ccnt.count,
                padx=2, pady=2, sticky='ew')
            self._oop_btn.bind('<Button-3>', self.sub_seeds)

        elif game_ui.stores:
            tk.Button(tframe, text="Clear to Stores",
                      command=self.clear_to_stores).grid(
                          row=rcnt.value, column=ccnt.count,
                          padx=2, pady=2, sticky='ew')

        else:
            tk.Button(tframe, text="Move to Left",
                      command=self.move_to_left).grid(
                          row=rcnt.value, column=ccnt.count,
                          padx=2, pady=2, sticky='ew')


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
        text += '\n'

        tk.Label(frame, anchor='nw', justify='left', text=text
                 ).pack(side='top', expand=True, fill='both')

        text = f'Seeds: {self.nbr}'
        self._label = tk.Label(frame, anchor='nw', justify='left', text=text)
        self._label.pack(side='top', expand=True, fill='both')

        tframe = tk.Frame(frame)
        rcnt = ui_utils.Counter()
        ccnt = ui_utils.Counter()

        tk.Button(tframe, text="Swap Turn",
                  command=self.swap_starter).grid(
                      row=rcnt.count, column=ccnt.count,
                      padx=2, pady=2, sticky='ew')
        tk.Button(tframe, text="Rotate Board",
                  command=self.rotate_board).grid(
                      row=rcnt.value, column=ccnt.count,
                      padx=2, pady=2, sticky='ew')
        tk.Button(tframe, text="Initial Setup",
                  command=self.init_setup).grid(
                      row=rcnt.value, column=ccnt.count,
                      padx=2, pady=2, sticky='ew')

        ccnt.reset()
        rcnt.increment()

        self.add_sow_dir_if(game_ui, tframe, rcnt, ccnt)

        ginfo = self.game_ui.game.info
        if ginfo.child_type:
            tk.Button(tframe, text="Clear Child",
                      command=self.clear_child).grid(
                          row=rcnt.value, column=ccnt.count,
                          padx=2, pady=2, sticky='ew')
        if (ginfo.moveunlock
                or ginfo.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST):
            tk.Button(tframe, text="Clear Locks",
                      command=self.clear_locks).grid(
                          row=rcnt.value, column=ccnt.count,
                          padx=2, pady=2, sticky='ew')
        if ginfo.blocks:
            tk.Button(tframe, text="Clear Blocks",
                      command=self.clear_blocks).grid(
                          row=rcnt.value, column=ccnt.count,
                          padx=2, pady=2, sticky='ew')

        self.add_collect_button(game_ui, tframe, rcnt, ccnt)

        tframe.pack(side='top')

        tk.Button(frame, text='Done', command=self.done
                  ).pack(side='bottom', padx=2, pady=2)


    def swap_starter(self):
        """Swap the starter and do board refresh."""

        new_turn = not self.game_ui.game.turn
        self.game_ui.game.starter = self.game_ui.game.turn = new_turn
        self.refresh_game()


    def swap_sow_dir(self):
        """For play alt dir games, swap the sow directions."""

        self.alt_dir_ctrl.swap_dirs()
        self._altd_btn['text'] = self.alt_dir_ctrl.north_dir_text


    def clear_board(self):
        """Move the seeds off the board and do board refresh."""

        game = self.game_ui.game
        self.out_of_play = game.cts.total_seeds
        game.store[0] = self.out_of_play
        game.store[1] = 0
        self._oop_btn['text']=f"Off board: {self.out_of_play}"

        for i, _ in enumerate(game.board):
            game.board[i] = 0

        self.refresh_game()


    def clear_to_stores(self):
        """Move the seeds to the stores and do board refresh.
        Don't do anything if the stores aren't on the UI."""

        quot, rem = divmod(self.game_ui.game.cts.total_seeds , 2)

        store = self.game_ui.game.store
        store[0] = quot + rem
        store[1] = quot

        board = self.game_ui.game.board
        for i, _ in enumerate(board):
            board[i] = 0

        self.refresh_game()


    def clear_child(self):
        """Clear the child settings and do board refresh."""

        game = self.game_ui.game

        for i, _ in enumerate(game.board):
            game.child[i] = None

        self.refresh_game()


    def clear_blocks(self):
        """Clear the blocked setting and do board refresh."""

        game = self.game_ui.game

        for i, _ in enumerate(game.board):
            game.blocked[i] = False

        self.refresh_game()


    def clear_locks(self):
        """Clear the unlocked values and do board refresh."""

        game = self.game_ui.game

        for i, _ in enumerate(game.board):
            game.unlocked[i] = True

        self.refresh_game()


    def move_to_left(self):
        """Move the seeds to each player's leftmost hole.
        Use for games where stores are not visible and captured
        seeds are moved to player's children."""

        holes = self.game_ui.game.cts.holes
        board = self.game_ui.game.board
        for loc in range(1, holes):
            board[0] += board[loc]
            board[loc] = 0

        for loc in range(holes + 1, self.game_ui.game.cts.dbl_holes):
            board[holes] += board[loc]
            board[loc] = 0

        self.refresh_game()


    def init_setup(self):
        """Reset the game to the initial setup and clear the
        inhibitor."""

        self.game_ui.game.new_game()
        self.game_ui.game.inhibitor.set_off()
        self.game_ui.game.mcount = 2
        self.game_ui.game.movers = 2
        self.game_ui.player.clear_history()
        self.refresh_game()


    def rotate_board(self):
        """Rotate the board.
        AI can only play True."""

        self.game_ui.game.swap_sides()
        self.refresh_game()


    def refresh_game(self):
        """After refreshing the game with the UI, make certain
        the stores and their seeds are visible.

        The UI has games in which the stores are visible but always
        have 0 in them (used to show whose turn it is)."""

        self.game_ui.refresh()

        game = self.game_ui.game
        store = game.store
        ui_stores = self.game_ui.stores

        if ui_stores and not self.game_ui.show_seeds_in_stores():

            # stores are in game_ui.stores by row
            ui_stores[0].set_store(store[1], None)
            ui_stores[1].set_store(store[0], None)


    def add_seeds(self):
        """Add any held seeds to the out-of-play button/container."""

        if not self.nbr:
            self.game_ui.bell()
            return

        self.game_ui.game.store[0] += self.nbr
        self.set_hold(0)
        self.out_of_play = self.game_ui.game.store[0]
        self._oop_btn['text']=f"Off board: {self.out_of_play}"
        self.game_ui.config(cursor=ui_utils.NORMAL)


    def sub_seeds(self, _=None):
        """Pickup seeds from the out-of-play button/container."""

        if not self.out_of_play:
            self.game_ui.bell()
            return

        seeds = self.query_nbr_seeds(None, self.out_of_play)
        if seeds:
            self.game_ui.game.store[0] -= seeds
            self.out_of_play = self.game_ui.game.store[0]
            self._oop_btn['text']=f"Off board: {self.out_of_play}"
            self.game_ui.config(cursor=ui_utils.HOLD_SEEDS)


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

        messages = ["Do you wish to enter board setup mode?",
                   """The current game will not be tallied,
                      the inhibitor will be turned off,
                      no prescribed openings will occur,
                      and knowledge gained by the AI player
                      is cleared, and it is deactivated."""]
        do_it = ui_utils.ask_popup(game_ui,
                                   'Board Setup', messages,
                                   ui_utils.OKCANCEL)
        if not do_it:
            return False

        SETUPHOLD.hold_menu(game_ui)
        game_ui.game.inhibitor.set_off()
        game_ui.game.mcount = 2
        game_ui.game.movers = 2
        game_ui.tkvars.ai_active.set(False)

        return True


    @classmethod
    def leave_mode(cls, game_ui):
        """Test if it's ok to leave setup mode."""

        if SETUPHOLD.warn_not_empty(game_ui):
            return False

        if not any(game_ui.game.get_allowable_holes()):
            ui_utils.showerror(game_ui,
                               'Game Mode', 'The game is not playable.')
            return False

        game_ui.setup_save()
        game_log.add('\n*** Game Setup Complete', game_log.MOVE)
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
        SETUPHOLD.refresh_game()

        SETUPHOLD.empty()
        self.btn.game_ui.config(cursor=ui_utils.NORMAL)


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
        if ginfo.child_cvt:
            # only include if more children can be made (cvt not type)
            menubar.add_command(label='Child Cycle', command=self.child_cycle)
        if ginfo.child_type == gi.ChildType.RAM:
            menubar.add_command(label='Child Cycle', command=self.ram_child_toggle)
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

        if seeds:
            self.remove_seeds(seeds)
            self.btn.game_ui.config(cursor=ui_utils.HOLD_SEEDS)


    @staticmethod
    def cycle(value):
        """Cycle the value through N, F, T"""

        if value:
            return None
        if value is None:
            return False
        return True


    def child_cycle(self):
        """Cycle the child through N, F, T"""

        game = self.btn.game_ui.game
        loc = self.btn.loc
        game.child[loc] = self.cycle(game.child[loc])
        self.btn.props.ch_owner = game.child[loc]
        SETUPHOLD.refresh_game()


    def ram_child_toggle(self):
        """Toggle the child setting between RAM and not RAM"""

        game = self.btn.game_ui.game
        loc = self.btn.loc
        game.child[loc] = None if game.child[loc] else gi.NO_CH_OWNER
        self.btn.props.ch_owner = game.child[loc]
        SETUPHOLD.refresh_game()


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
        self.refresh(self.saved_state)


    def block_toggle(self):
        """Toggle the blocked status."""

        game = self.btn.game_ui.game
        loc = self.btn.loc

        if game.board[loc]:
            ui_utils.showerror(
                self.btn.game_ui,
                'Block',
                'Remove the seeds from the hole before blocking it.')
            return

        game.blocked[loc] = not game.blocked[loc]
        self.btn.props.blocked = game.blocked[loc]
        SETUPHOLD.refresh_game()


    def lock_toggle(self):
        """Toggle the blocked status."""

        game = self.btn.game_ui.game
        loc = self.btn.loc
        game.unlocked[loc] = not game.unlocked[loc]
        self.btn.props.unlocked = game.unlocked[loc]
        SETUPHOLD.refresh_game()


    def do_right_click(self):
        """If there is more than one setup operation, popup
        the a menu of options. Otherwise, pickup seeds."""

        game_ui = self.btn.game_ui
        ginfo = game_ui.game.info

        if any([ginfo.child_cvt,    # not child_type, can make more children
                ginfo.child_type == gi.ChildType.RAM,
                ginfo.goal == gi.Goal.TERRITORY,
                ginfo.blocks,
                ginfo.moveunlock,
                ginfo.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST]):

            self.do_popup_menu()

        else:
            self.pickup()
            SETUPHOLD.refresh_game()


    def refresh(self, bstate=None):
        """Refresh the button as in play mode but then override
        the state to normal (so it can be clicked)."""

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
        game_ui = self.str.game_ui
        if seeds and game_ui.show_seeds_in_stores():
            self.str['text'] = str(seeds)
        else:
            self.str['text'] = ''
        self.str.update_color(highlight)


    def do_left_click(self):
        """Drop all picked up seeds, but not for eliminate games."""

        game = self.str.game_ui.game
        if not SETUPHOLD.nbr or not self.str.game_ui.show_seeds_in_stores():
            self.str.bell()
            return

        seeds = game.store[self.str.owner] + SETUPHOLD.nbr
        self.set_store(seeds, game.turn == self.str.owner)
        game.store[self.str.owner] = seeds

        self.str.game_ui.config(cursor=ui_utils.NORMAL)
        SETUPHOLD.empty()


    def do_right_click(self):
        """Pop up the nbr seeds query, and pickup seeds if
        the user entered a valid number."""

        game = self.str.game_ui.game

        # no seeds to pick up or eliminate (don't care about seeds)
        if (not game.store[self.str.owner]
            or not self.str.game_ui.show_seeds_in_stores()):
            self.str.bell()
            return

        seeds = game.store[self.str.owner]

        if SETUPHOLD.query_nbr_seeds(None, seeds):

            game = self.str.game_ui.game
            seeds -= SETUPHOLD.nbr
            self.set_store(seeds, game.turn == self.str.owner)
            game.store[self.str.owner] = seeds

            self.str.game_ui.config(cursor=ui_utils.HOLD_SEEDS)
