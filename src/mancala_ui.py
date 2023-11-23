# -*- coding: utf-8 -*-
"""Create the UI for a mancala game_constants and game_info
define how the game is created and played.
The values of those two variables must not be changed during
game play.

Created on Thu Mar  2 14:38:17 2023
@author: Ann"""


# %% imports

import os
import textwrap
import traceback
import tkinter as tk

import ai_player
import cfg_keys as ckey
import btn_behaviors as btnb
import game_interface as gi
import game_tally as gt

from game_log import game_log


# %%   constants

AI_DELAY = [0, 1000, 3000]


# %%  mancala ui

class MancalaUI(tk.Frame):
    """A manacala UI."""

    def __init__(self, game, player_dict, root_ui=None):
        """Create the UI for a mancala game.

        game : class built on GameInterface -  provide the mechanics of
        the game w/o any UI"""

        if not isinstance(game, gi.GameInterface):
            raise TypeError('Missing mancala_ui.GameInterface in game.')

        self.game = game
        self.mode = btnb.Behavior.GAMEPLAY
        self.player = ai_player.AiPlayer(self.game, player_dict)

        game_log.new()
        game_log.turn(0, 'Start Game', game)

        self.info = self.game.get_game_info()

        if root_ui:
            self.master = tk.Toplevel(root_ui)
        else:
            self.master = tk.Tk()

        self.log_ai = tk.BooleanVar(self.master, False)
        self.live_log = tk.BooleanVar(self.master, game_log.live)
        self.log_level = tk.IntVar(self.master, game_log.level)

        self.master.title(self.info.name)
        self.master.option_add('*tearOff', False)
        self.master.resizable(False, False)
        self.master.wm_geometry('+500+300')

        super().__init__(self.master)
        self.master.report_callback_exception = self._exception_callback

        self.difficulty = tk.IntVar(self.master,
                                    value=self.player.difficulty)
        self._set_difficulty()

        start_ai = (ckey.AI_ACTIVE in player_dict
                    and player_dict[ckey.AI_ACTIVE])
        self.ai_active = tk.IntVar(self.master, value=start_ai)
        self.ai_delay = tk.BooleanVar(self.master, value=2)

        self.pack()
        self._create_menus()

        self.tally = None
        self.rframe = None
        self._add_statuses()

        self.disp = [[None] * self.game.cts.holes,
                     [None] * self.game.cts.holes]
        self.stores = None
        self._add_board()

        self._new_game()
        self._refresh()
        self._ai_move()


    def _add_statuses(self):
        """Add status and info panes. Make them each 50% of the display."""

        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, expand=True, fill=tk.X)

        lframe = tk.Frame(top_frame, padx=5, pady=5,
                          borderwidth=3, relief=tk.RIDGE)
        lframe.grid(row=0, column=0, sticky=tk.NSEW)
        self.tally = gt.GameTally(lframe)

        self.rframe = tk.Frame(top_frame, padx=5, pady=5,
                               borderwidth=3, relief=tk.RIDGE)
        self.rframe.grid(row=0, column=1, sticky=tk.NSEW)

        top_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        top_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        top_frame.grid_rowconfigure(0, weight=1)


    def _add_board(self):
        """Add the game board frame and widgets."""

        board_frame = tk.Frame(self, borderwidth=7, relief=tk.RAISED)
        board_frame.pack(side=tk.BOTTOM)

        if self.info.stores:
            b_store = btnb.StoreButton(board_frame, self, tk.LEFT, True)

        land_frame = tk.Frame(board_frame, padx=3, pady=3)
        land_frame.pack(side=tk.LEFT)

        for row in range(2):
            dirs = self._get_hole_dirs(row)

            for pos in range(self.game.cts.holes):

                btn = self._build_button(land_frame, row, pos, dirs)
                self.disp[row][pos] = btn
                self.disp[row][pos].grid(row=row, column=pos)

        if self.info.stores:
            a_store = btnb.StoreButton(board_frame, self, tk.RIGHT, False)
            self.stores = [b_store, a_store]


    def _get_hole_dirs(self, row):
        """Return the directions to use when creating the hole buttons."""

        dirs = None
        if self.info.udirect:
            if row:
                dirs = [gi.Direct.CW, gi.Direct.CCW]
            else:
                dirs = [gi.Direct.CCW, gi.Direct.CW]

        return dirs


    def _build_button(self, land_frame, row, pos, dirs):
        """Generate moves to return when the button is selected and
        build the button.

        Note that if the hole is not udirect, the left and right
        buttons do the same thing."""

        loc = self.game.cts.xlate_pos_loc(row, pos)

        if self.info.udirect:

            cnt = self.game.cts.loc_to_left_cnt(loc)
            if cnt in self.info.udir_holes:
                left_move = gi.MoveTpl(pos, dirs[0])
                rght_move = gi.MoveTpl(pos, dirs[1])
            else:
                left_move = gi.MoveTpl(pos, None)
                rght_move = left_move

            if self.info.mlength == 3:
                left_move = gi.MoveTpl(row, *left_move)
                rght_move = gi.MoveTpl(row, *rght_move)

        elif self.info.mlength == 3:
            left_move = gi.MoveTpl(row, pos, None)
            rght_move = left_move

        else:
            left_move = pos
            rght_move = pos

        return btnb.HoleButton(land_frame, self, loc, left_move, rght_move)


    @staticmethod
    def _exception_callback(*args):
        """Support debugging by printing the play_log and the traceback."""

        game_log.dump()
        traceback.print_exception(args[0], args[1], args[2])


    def _create_menus(self):
        """Create the game control menus."""

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        gamemenu = tk.Menu(menubar)
        gamemenu.add_command(label='New', command=self._new_game)
        gamemenu.add_command(label='End Game', command=self._end_game)
        menubar.add_cascade(label='Game', menu=gamemenu)

        aimenu = tk.Menu(menubar)

        aimenu.add_checkbutton(label='AI Player', variable=self.ai_active,
                               onvalue=True, offvalue=False,
                               command=self._ai_move)

        aimenu.add_separator()
        aimenu.add_radiobutton(label='No AI Delay', variable=self.ai_delay,
                               value=0)
        aimenu.add_radiobutton(label='Short AI Delay', variable=self.ai_delay,
                               value=1)
        aimenu.add_radiobutton(label='Long AI Delay', variable=self.ai_delay,
                               value=2)

        aimenu.add_separator()
        aimenu.add_radiobutton(label='Easy',
                               value=0, variable=self.difficulty,
                               command=self._set_difficulty)
        aimenu.add_radiobutton(label='Normal',
                               value=1, variable=self.difficulty,
                               command=self._set_difficulty)
        aimenu.add_radiobutton(label='Hard',
                               value=2, variable=self.difficulty,
                               command=self._set_difficulty)
        aimenu.add_radiobutton(label='Expert',
                               value=3, variable=self.difficulty,
                               command=self._set_difficulty)

        menubar.add_cascade(label='AI', menu=aimenu)

        logmenu = tk.Menu(menubar)
        logmenu.add_command(label='Show Prev', command=game_log.prev)
        logmenu.add_command(label='Show Log', command=game_log.dump)
        logmenu.add_command(label='Save Log', command=self._save_file)
        logmenu.add_separator()

        logmenu.add_radiobutton(
            label='Moves',
            value=game_log.MOVE, variable=self.log_level,
            command=lambda: setattr(game_log, 'level', self.log_level.get()))
        logmenu.add_radiobutton(
            label='Important',
            value=game_log.IMPORT, variable=self.log_level,
            command=lambda: setattr(game_log, 'level', self.log_level.get()))
        logmenu.add_radiobutton(
            label='Steps',
            value=game_log.STEP, variable=self.log_level,
            command=lambda: setattr(game_log, 'level', self.log_level.get()))
        logmenu.add_radiobutton(
            label='Information',
            value=game_log.INFO, variable=self.log_level,
            command=lambda: setattr(game_log, 'level', self.log_level.get()))
        logmenu.add_radiobutton(
            label='Detail',
            value=game_log.DETAIL, variable=self.log_level,
            command=lambda: setattr(game_log, 'level', self.log_level.get()))
        logmenu.add_radiobutton(
            label='All',
            value=game_log.SHOWALL, variable=self.log_level,
            command=lambda: setattr(game_log, 'level', self.log_level.get()))
        logmenu.add_separator()
        logmenu.add_checkbutton(
            label='Live Log',
            onvalue=True, offvalue=False,
            variable=self.live_log,
            command=lambda: setattr(game_log, 'live', self.live_log.get()))
        logmenu.add_checkbutton(label='Log AI Analysis',
                                variable=self.log_ai,
                                onvalue=True, offvalue=False)

        menubar.add_cascade(label='Log', menu=logmenu)

        helpmenu = tk.Menu(menubar)
        helpmenu.add_command(label='Help...', command=self._help)
        helpmenu.add_command(label='About...', command=self._about)
        menubar.add_cascade(label='Help', menu=helpmenu)


    def ui_loop(self):
        """Call the mainloop UI - everything happens because of user input.
        This does not return until the window is killed."""

        self.master.mainloop()


    def _cancel_pending_afters(self):
        """Cancel any pending after methods."""

        for after_id in self.tk.eval('after info').split():
            self.after_cancel(after_id)


    def destroy(self):
        """window was closed."""

        self._cancel_pending_afters()


    def _quiet_dialog(self, title, text):
        """Popup a quiet dialog message."""

        xpos = self.winfo_rootx() + 100
        ypos = self.winfo_rooty() + 50

        top = tk.Toplevel(self)
        top.resizable(False, False)
        top.lift(aboveThis=self)
        top.title(title)
        top.wm_geometry(f'+{xpos}+{ypos}')
        top.minsize(200, 100)
        top.grab_set()

        frame = tk.Frame(top, borderwidth=10)
        frame.pack(side='top', expand=True)

        tk.Label(frame, anchor='nw', justify='left', text=text
                 ).pack(side='top')
        tk.Button(frame, text='Ok', command=top.destroy).pack(side='bottom')


    def _help(self):
        """Have the os pop open the help file in a browser,
        if there's a problem popup a 'no help' window."""

        no_help = True
        if os.path.isfile(self.info.help_file):
            no_help = False
            try:
                os.startfile(self.info.help_file)

            except FileNotFoundError:
                no_help = True

        if no_help:
            self._quiet_dialog('Help', 'Help not provided.')


    def _about(self):
        """Popup the about window."""

        atext = self.info.about
        if not atext or (isinstance(atext, str) and not atext.strip()):
            atext = 'Mancala Game Player'

        paragraphs = atext.split('\n')
        out_text = self.info.name + ':\n'
        for para in paragraphs:
            out_text += textwrap.fill(para, 45) + '\n'

        self._quiet_dialog('About', ''.join(out_text))


    def _save_file(self):
        """Save the game log to the file, provide a string that
        describes the game."""
        game_log.save(self.game.params_str())


    def _refresh(self):
        """Make UI match mancala game.

        If the ai is active and it's the ai's turn (True), disable all holes.
        Additionally, disable holes that:
            1. are not the current players hole
            2. are not available for play (e.g. no allowable move)"""

        turn = self.game.get_turn()
        actives = self.game.get_allowable_holes()
        turn_row = int(not turn)
        ai_turn = self.ai_active.get() and turn
        for row in range(2):

            player = row == turn_row
            if self.info.stores:
                self.stores[row].set_store(self.game.get_store(row),
                                           player)

            for pos in range(self.game.cts.holes):

                if self.game.info.mlength == 3:
                    loc = self.game.cts.xlate_pos_loc(row, pos)
                    cactive = actives[loc]
                    disable = not actives[loc]
                else:
                    cactive = player and actives[pos]
                    disable = ai_turn or not cactive

                self.disp[row][pos].set_props(
                    self.game.get_hole_props(row, pos),
                    disable, cactive)


    def _start_it(self):
        """Do the last steps in starting a new game:
        log the start and check for ai's turn."""
        game_log.new()
        game_log.turn(0, 'Start Game', self.game)
        self._schedule_ai()


    def _new_game(self, win_cond=None, new_round_ok=False):
        """Start a new game and refresh the board."""

        self._cancel_pending_afters()
        self.set_game_mode(btnb.Behavior.GAMEPLAY, force=True)
        new_game = self.game.new_game(win_cond=win_cond,
                                      new_round_ok=new_round_ok)

        self._refresh()
        self.update()
        if new_game:
            if self.info.prescribed == gi.SowPrescribed.ARNGE_LIMIT:
                if self.set_game_mode(btnb.Behavior.MOVESEEDS):
                    return

        elif self.info.round_fill == gi.RoundFill.UCHOOSE:
            if self.set_game_mode(btnb.Behavior.RNDCHOOSE):
                return

        elif self.info.round_fill == gi.RoundFill.UMOVE:
            if self.set_game_mode(btnb.Behavior.RNDMOVE):
                return

        self._start_it()


    def set_game_mode(self, mode, force=False):
        """Change the game mode.
        ask_mode_change checks if it's ok to and/or
        asks the user if they want to change.
        Assert will catch any programming error, that caused
        a seed gain or loss."""

        if mode == self.mode:
            return True

        assert not force or force and mode == btnb.Behavior.GAMEPLAY, \
            "Don't force game mode change for anything but normal game play."

        if force:
            btnb.force_mode_change()

        elif not btnb.ask_mode_change(self.mode, mode, self):
            return False

        assert sum(self.game.store) + sum(self.game.board) == \
            self.game.cts.total_seeds, \
            'Seed count error on switching UI mode.'

        self.mode = mode
        for button_row in self.disp:
            for btn in button_row:
                btn.set_behavior(mode)
        self.stores[0].set_behavior(mode)
        self.stores[1].set_behavior(mode)

        self._refresh()
        if mode == btnb.Behavior.GAMEPLAY:
            self._start_it()
        return True


    def _win_popup(self, title, message):
        """Popup the win window with a game dump option."""

        self.bell()

        xpos = self.winfo_rootx() + 100
        ypos = self.winfo_rooty() + 50

        top = tk.Toplevel(self)
        top.resizable(False, False)
        top.grab_set()
        top.title(title)
        top.wm_geometry(f'+{xpos}+{ypos}')

        frame = tk.Frame(top, borderwidth=10)
        frame.pack(side='top', fill='both', expand=True)

        tk.Label(frame, text=message).pack(side='top')

        bframe = tk.Frame(top, borderwidth=20)
        bframe.pack(side='bottom', fill='both', expand=True)
        tk.Button(bframe, text='Dump Game', command=game_log.dump,
                  width=12).pack(side='left')
        tk.Button(bframe, text='Save Game', command=self._save_file,
                  width=12).pack(side='left')
        tk.Button(bframe, text='Ok', command=top.destroy,
                  width=12).pack(side='right')
        top.wait_window()


    def _win_message_popup(self, win_cond):
        """If someone won or there was a tie,
        popup the winner dialog box."""

        self.tally.tally_game(self.game.get_turn(), win_cond)

        if win_cond:
            self._win_popup(*self.game.win_message(win_cond))


    def _end_game(self):
        """End the game. Report result to user."""

        message = 'Are you sure you wish to end the game?'
        do_it = tk.messagebox.askokcancel(title='End Game', message=message,
                                          parent=self)
        if not do_it:
            return
        self.update()
        self.set_game_mode(btnb.Behavior.GAMEPLAY, force=True)

        win_cond = self.game.end_game()

        wtext = 'Game Ended '
        if win_cond in (gi.WinCond.WIN, gi.WinCond.ROUND_WIN):
            sturn = 'Top' if self.game.get_turn() else 'Bottom'
            wtext += f'\n{win_cond.name} by {sturn}'
        elif win_cond:
            wtext += ' ' + win_cond.name
        game_log.turn(self.game.mcount, wtext, self.game)

        self._refresh()
        self._win_message_popup(win_cond)
        self._new_game()


    def _set_difficulty(self):
        """Set the difficulty for the ai player."""

        diff = self.difficulty.get()
        self.player.difficulty = diff
        game_log.add(f'Changing difficulty {diff}', game_log.INFO)


    def _log_turn(self, last_turn):
        """Add the ai description to the game log (Mancala doesn't
        know if the ai is playing)."""

        if self.ai_active.get() and last_turn:
            game_log.add(self.player.get_move_desc(), game_log.MOVE)


    def move(self, move):
        """Tell game to move, refresh the UI, and
        handle any win conditions."""

        last_turn = self.game.get_turn()
        win_cond = self.game.move(move)

        self._log_turn(last_turn)
        self._refresh()

        if win_cond and win_cond != gi.WinCond.REPEAT_TURN:
            # self._save_file()   # for testing auto save the logs
            self._win_message_popup(win_cond)
            self._new_game(win_cond=win_cond, new_round_ok=True)
            return

        if self.ai_active.get() and self.game.get_turn():
            self._schedule_ai()

        elif self.info.mustpass and self.game.test_pass():

            player = 'Bottom' if self.game.get_turn() else 'Top'
            message = f'{player} player has no moves and must pass.'
            tk.messagebox.showinfo(title='Pass Move', message=message,
                                   parent=self)

            self._refresh()
            self._schedule_ai()


    def _schedule_ai(self):
        """Do AI move or schedule the AI turn (if the AI is enabled
        and it's the AI's turn)"""

        if self.ai_active.get() and self.game.get_turn():
            self._cancel_pending_afters()
            sel_delay = self.ai_delay.get()

            if sel_delay:
                self.after(AI_DELAY[sel_delay], self._ai_move)
            else:
                self.update()
                self._ai_move()


    def _ai_move(self):
        """If it's the AI's turn, do a move. AI is top player."""

        if self.ai_active.get() and self.game.get_turn():
            saved_active = game_log.active

            game_log.active = self.log_ai.get()
            move = self.player.pick_move()
            game_log.active = saved_active

            self.move(move)
