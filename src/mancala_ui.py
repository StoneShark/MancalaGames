# -*- coding: utf-8 -*-
"""Create the UI for a mancala game_constants and game_info
define how the game is created and played.
The values of those two variables must not be changed during
game play.

Created on Thu Mar  2 14:38:17 2023
@author: Ann
"""


# %% imports

import os
import traceback

import tkinter as tk

import hole_button as hb
import game_interface as gi
import game_log

from hole_button import Behavior
from game_interface import WinCond
from game_interface import Direct
from game_interface import PASS_TOKEN

# %%   constants

AI_DELAY = [0, 1000, 3000]
NO_STR = 'no'


# %%  GameTally

class GameTally:
    """Class to collect game data across multiple games."""

    def __init__(self):
        """Set the counts to 0."""

        self.games = 0
        self.game_wins = [0, 0]
        self.game_ties = 0

        self.rounds = 0
        self.round_wins = [0, 0]
        self.round_ties = 0


    def get_str(self):
        """Return a string with win info."""

        if self.rounds > 0:
            return f'\n\nBottom: Rounds: {self.round_wins[0]} ' \
                   f'Ties: {self.round_ties}   ' \
                   f'Losses: {self.round_wins[1]}   ' \
                   f'{self.round_wins[0]/self.rounds:6.1%}'

        if self.games > 0:
            return f'\n\nBottom: Wins: {self.game_wins[0]} ' \
                   f'Ties: {self.game_ties}   ' \
                   f'Losses: {self.game_wins[1]}   ' \
                   f'{self.game_wins[0]/self.games:6.1%}'

        return ''


    def tally_game(self, winner, win_cond):
        """Ignore the odd outcomes.

        If we get round results tally them, but a game result
        ends the rounds (so reset the round numbers).

        winner: boolean - player that won if win.
        win_cond: WinCond - outcome of the game."""

        if win_cond in [WinCond.END_STORE, WinCond.ENDLESS]:
            return

        if win_cond is WinCond.ROUND_WIN:
            self.rounds += 1
            self.round_wins[winner] += 1

        if win_cond is WinCond.ROUND_TIE:
            self.rounds += 1
            self.round_ties += 1

        if win_cond is WinCond.WIN:
            self.games += 1
            self.game_wins[winner] += 1

        if win_cond is WinCond.TIE:
            self.games += 1
            self.game_ties += 1

        if win_cond in [WinCond.WIN, WinCond.TIE]:
            self.rounds = 0
            self.round_wins = [0, 0]
            self.round_ties = 0


# %% store

class Store:
    """Graphic for the seed storage spots."""

    def __init__(self, parent, side):
        """Create the Seed storage graphic."""
        store_frame = tk.Frame(parent, padx=20, pady=20,
                               borderwidth=3, relief='ridge')
        store_frame.pack(side=side)

        self.label = tk.Label(store_frame, width=3, text='',
                              font='bold')
        self.label.pack()


    def set_store(self, seeds):
        """Update the number of seeds in the store."""
        self.label['text'] = str(seeds)


# %%  mancala ui

class MancalaUI(tk.Frame):
    """A manacala UI."""

    def __init__(self, game, root_ui=None):
        """Create the UI for a mancala game.

        game : class built on GameInterface -  provide the mechanics of
        the game w/o any UI
        """

        if not isinstance(game, gi.GameInterface):
            raise TypeError('Missing mancala_ui.GameInterface in game.')

        self.game = game
        self.mode = Behavior.GAMEPLAY

        game_log.new()
        game_log.turn(game, 'Start Game')

        self.info = self.game.get_game_info()
        self.tally = GameTally()

        if root_ui:
            self.master = tk.Toplevel(root_ui)
        else:
            self.master = tk.Tk()

        self.log_ai = tk.BooleanVar(self.master, False)
        self.live_log = tk.BooleanVar(self.master, False)
        self.log_level = tk.IntVar(self.master, game_log.MOVES)
        game_log.set_level(self.log_level.get())

        self.master.title(self.info.name)
        self.master.option_add('*tearOff', False)
        self.master.resizable(False, False)
        self.master.wm_geometry('+500+300')

        super().__init__(self.master)
        self.master.report_callback_exception = self._exception_callback

        self.difficulty = tk.IntVar(self.master, value=self.info.difficulty)
        self.game.set_difficulty(self.info.difficulty)

        self.ai_delay = tk.BooleanVar(self.master, value=2)
        self.ai_player = tk.IntVar(self.master, value=False)

        self.pack()
        self._create_menus()

        if self.info.flags.stores:
            b_store = Store(self, 'left')

        land_frame = tk.Frame(self, padx=3, pady=3)
        land_frame.pack(side='left')

        self.disp = [[None] * self.game.cts.holes,
                     [None] * self.game.cts.holes]
        for row in range(2):
            dirs = self._get_hole_dirs(row)

            for pos in range(self.game.cts.holes):
                if self.info.flags.udirect:

                    if pos in self.info.udir_holes:
                        btn = hb.HoleButton(land_frame, self, pos,
                                            (True, dirs))
                    else:
                        btn = hb.HoleButton(land_frame, self, pos,
                                            (True, None))
                else:
                    btn = hb.HoleButton(land_frame, self, pos)

                self.disp[row][pos] = btn
                self.disp[row][pos].grid(row=row, column=pos)

        self.stores = None
        if self.info.flags.stores:
            a_store = Store(self, 'right')
            self.stores = [b_store, a_store]

        # do not call new game
        # either it's already new or it's been set to a desired state
        self._refresh()


    def _get_hole_dirs(self, row):
        """Return the directions to use when creating the hole buttons."""

        dirs = None
        if self.info.flags.udirect:
            if row:
                dirs = [Direct.CW, Direct.CCW]
            else:
                dirs = [Direct.CCW, Direct.CW]

        return dirs


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

        aimenu.add_checkbutton(label='AI Player', variable=self.ai_player,
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
            value=game_log.MOVES, variable=self.log_level,
            command=lambda: game_log.set_level(self.log_level.get()))
        logmenu.add_radiobutton(
            label='Important',
            value=game_log.IMPORT, variable=self.log_level,
            command=lambda: game_log.set_level(self.log_level.get()))
        logmenu.add_radiobutton(
            label='Steps',
            value=game_log.STEPS, variable=self.log_level,
            command=lambda: game_log.set_level(self.log_level.get()))
        logmenu.add_radiobutton(
            label='Information',
            value=game_log.INFO, variable=self.log_level,
            command=lambda: game_log.set_level(self.log_level.get()))
        logmenu.add_radiobutton(
            label='All',
            value=game_log.NOTSET, variable=self.log_level,
            command=lambda: game_log.set_level(self.log_level.get()))
        logmenu.add_separator()
        logmenu.add_checkbutton(
            label='Live Log',
            onvalue=True, offvalue=False,
            variable=self.live_log,
            command=lambda: game_log.set_live(self.live_log.get()))
        logmenu.add_checkbutton(label='Log AI Analysis',
                                variable=self.log_ai,
                                onvalue=True, offvalue=False)

        menubar.add_cascade(label='Log', menu=logmenu)

        if self.info.flags.rounds:
            rndmenu = tk.Menu(menubar)
            rndmenu.add_command(
                label='Start Round',
                command=lambda: self.set_game_mode(Behavior.GAMEPLAY))
            menubar.add_cascade(label='Round', menu=rndmenu)

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

        xpos, ypos, _, width = self.bbox("insert")
        xpos = xpos + self.winfo_rootx() + 100
        ypos = ypos + width + self.winfo_rooty() + 50

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

        self._quiet_dialog('About', atext)


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
        turn_row = int(not turn)
        actives = self.game.get_allowable_holes()
        ai_turn = self.ai_player.get() and turn

        for row in range(2):

            if self.info.flags.stores:
                self.stores[row].set_store(self.game.get_store(row))

            player = row == turn_row
            for pos in range(self.game.cts.holes):

                cactive = player and actives[pos]
                disable = ai_turn or not cactive

                self.disp[row][pos].set_props(
                    self.game.get_hole_props(row, pos),
                    disable, cactive)


    def _start_it(self):
        """Do the last steps in starting a new game:
        log the start and check for ai's turn."""
        game_log.new()
        game_log.turn(self.game, 'Start Game')
        self._ai_move()


    def _new_game(self, win_cond=None, new_round_ok=False):
        """Start a new game and refresh the board."""

        self._cancel_pending_afters()
        new_game = self.game.new_game(win_cond=win_cond,
                                      new_round_ok=new_round_ok)

        self._refresh()
        self.update()
        if not new_game:
            self.set_game_mode(Behavior.RNDSETUP)
            return
        self._start_it()


    def set_game_mode(self, mode):
        """Change the game mode.

        If switching to game play (from rndsetup) check that
        all seeds have been placed, and switch.
        Assert will catch any programming error, that caused
        a seed gain or loss.
        If all is ok, reconfig the buttons to GAMEPLAY mode.

        If switching to round setup (from gameplay),
        ask the user if they wish to move any seeds.
        If they do reconfig the buttons to RNDSETUP mode."""

        if mode == self.mode:
            return

        if mode == Behavior.GAMEPLAY:
            if not hb.game_mode_ok():
                tk.messagebox.showerror(
                    title='Game Mode',
                    message='Hold is not empty;'
                    'place seeds before returning to game mode.',
                    parent=self)
                return
            assert sum(self.game.store) + sum(self.game.board) == \
                self.game.cts.total_seeds, \
                'Seed count error on switching back to GAMEPLAY mode.'

        if mode == Behavior.RNDSETUP:
            ans = tk.messagebox.askquestion(
                title='Move seeds',
                message='A new round is begining so you may change\n'
                        'the occupied holes on each side of the board.\n'
                        'A right click picks up seeds.\n'
                        'A left click drops those seeds.\n'
                        'Use Round -> Start Round to play.\n'
                        'Do you wish to move any seeds?',
                        parent=self)
            if ans == NO_STR:
                self._start_it()
                return

        self.mode = mode
        for button_row in self.disp:
            for btn in button_row:
                btn.set_behavior(mode)

        self._refresh()
        if mode == Behavior.GAMEPLAY:
            self._start_it()


    def _win_popup(self, title, message):
        """Popup the win window with a game dump option."""

        self.bell()

        xpos, ypos, _, width = self.bbox("insert")
        xpos = xpos + self.winfo_rootx() + 100
        ypos = ypos + width + self.winfo_rooty() + 50

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

        title, message = self.game.win_message(win_cond)
        if win_cond:
            self._win_popup(title=title,
                            message=message + self.tally.get_str())
            self._new_game(win_cond=win_cond, new_round_ok=True)


    def _end_game(self):
        """End the game. Report result to user."""

        message = 'Are you sure you wish to end the game?'
        do_it = tk.messagebox.askokcancel(title='End Game', message=message,
                                          parent=self)
        if not do_it:
            return
        self.update()

        winner = self.game.end_game()
        self._refresh()
        self._win_message_popup(winner)

        self._new_game()


    def _set_difficulty(self):
        """Set the max search depth for the minimaxer and
        the delay before the AI plays."""

        self.game.set_difficulty(self.difficulty.get())


    def _log_turn(self, last_turn, pos, win_cond=None):
        """Add to the play log and move history for the last turn."""

        wtext = ''
        if win_cond in (WinCond.WIN, WinCond.ROUND_WIN):
            sturn = 'Top' if self.game.get_turn() else 'Bottom'
            wtext = f'\n{win_cond.name} by {sturn}'
        elif win_cond:
            wtext = ' ' + win_cond.name

        if self.ai_player.get() and last_turn:
            move_desc = self.game.get_ai_move_desc() + f'move {pos}{wtext}'
        else:
            sturn = 'Top' if last_turn else 'Bottom'
            move_desc = f'{sturn} player move {pos}{wtext}'

        game_log.turn(self.game, move_desc)


    def move(self, move):
        """Tell game to move, refresh the UI, and
        handle any win conditions."""

        last_turn = self.game.get_turn()
        win_cond = self.game.move(move)

        self._log_turn(last_turn, move, win_cond)
        self._refresh()

        if win_cond and win_cond != WinCond.END_STORE:
            self._win_message_popup(win_cond)
            return

        if self.ai_player.get() and self.game.get_turn():
            self._schedule_ai()

        elif self.info.flags.mustpass and self.game.test_pass():

            player = 'Bottom' if self.game.get_turn() else 'Top'
            message = f'{player} player has no moves and must pass.'
            tk.messagebox.showinfo(title='Pass Move', message=message,
                                   parent=self)

            self._refresh()
            self._log_turn(self.game.get_turn(), PASS_TOKEN)
            self._schedule_ai()


    def _schedule_ai(self):
        """Do AI move or schedule the AI turn (if the AI is enabled
        and it's the AI's turn)"""

        if self.ai_player.get() and self.game.get_turn():
            self._cancel_pending_afters()
            sel_delay = self.ai_delay.get()

            if sel_delay:
                self.after(AI_DELAY[sel_delay], self._ai_move)
            else:
                self.update()
                self._ai_move()


    def _ai_move(self):
        """If it's the AI's turn, do a move. AI is top player."""

        if self.ai_player.get() and self.game.get_turn():
            game_log.set_active(self.log_ai.get())
            move = self.game.get_ai_move()
            game_log.set_active(True)

            self.move(move)
