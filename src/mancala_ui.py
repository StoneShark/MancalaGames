# -*- coding: utf-8 -*-
"""Create the UI for a mancala game_constants and game_info
define how the game is created and played.
The values of those two variables must not be changed during
game play.

Created on Thu Mar  2 14:38:17 2023
@author: Ann"""


# %% imports

import textwrap
import traceback
import tkinter as tk
import webbrowser

import ai_player
import aspect_frame
import cfg_keys as ckey
import behaviors
import buttons
import game_interface as gi
import game_logger
import game_tally as gt
import man_config
import man_path
import round_tally
import version

from game_logger import game_log


# %%   constants

AI_DELAY = [5, 1000, 4000]

NO_TALLY_OP = 0
VIS_TALLY_OP = 1
RET_TALLY_OP = 2


# %%

def quiet_dialog(parent, title, text):
    """Popup a quiet dialog message.
    This is used in mancala_ui.py and mancala_games.pyw,
    so not in the class"""

    xpos = parent.winfo_rootx() + 100
    ypos = parent.winfo_rooty() + 50

    top = tk.Toplevel(parent)
    top.resizable(False, False)
    top.lift(aboveThis=parent)
    top.title(title)
    top.wm_geometry(f'+{xpos}+{ypos}')
    top.minsize(200, 100)
    top.grab_set()

    frame = tk.Frame(top, borderwidth=10)
    frame.pack(side='top', expand=True)

    tk.Label(frame, anchor='nw', justify='left', text=text
             ).pack(side='top')
    tk.Button(frame, text='Ok', command=top.destroy).pack(side='bottom')


class TkVars:
    """Collect the tk status variables here and one stray."""

    def __init__(self, man_ui, player_dict):

        # must be visible for construction
        self.show_tally = tk.BooleanVar(man_ui.master, True)
        self.tally_was_off = False

        self.facing_players = tk.BooleanVar(
            man_ui.master, man_config.CONFIG.get_bool('facing_players'))
        self.touch_screen = tk.BooleanVar(
            man_ui.master, man_config.CONFIG.get_bool('touch_screen'))
        self.owner_arrows = tk.BooleanVar(
            man_ui.master, man_config.CONFIG.get_bool('owner_arrows'))

        self.log_ai = tk.BooleanVar(man_ui.master, False)
        game_log.live = man_config.CONFIG.get_bool('log_live')

        self.live_log = tk.BooleanVar(man_ui.master, game_log.live)

        value = man_config.CONFIG['log_level']
        if value:
            game_log.level = game_logger.Level.from_name(value)
        self.log_level = tk.IntVar(man_ui.master, game_log.level)

        value = man_ui.player.difficulty
        value = man_config.CONFIG.get_int('difficulty', value)
        self.difficulty = tk.IntVar(man_ui.master, value)

        value = ((ckey.AI_ACTIVE in player_dict
                     and player_dict[ckey.AI_ACTIVE])
                    or man_config.CONFIG.get_bool('ai_active'))
        self.ai_active = tk.IntVar(man_ui.master, value)

        self.ai_delay = tk.IntVar(
            man_ui.master, min(man_config.CONFIG.get_int('ai_delay', 1), 2))
        self.ai_filter = tk.BooleanVar(man_ui.master, True)


# %%  mancala ui

class MancalaUI(tk.Frame):
    """A manacala UI."""

    def __init__(self, game, player_dict, root_ui=None):
        """Create the UI for a mancala game.

        game: class built on GameInterface -  provide the mechanics of
        the game w/o any UI

        player_dict: player element from game config file; a dictionary
        of parameters to configure the ai player"""

        if not isinstance(game, gi.GameInterface):
            raise TypeError('Missing mancala_ui.GameInterface in game.')

        self.game = game
        self.mode = buttons.Behavior.GAMEPLAY
        self.player = ai_player.AiPlayer(self.game, player_dict)

        game_log.new()
        game_log.turn(0, 'Start Game', game)

        self.info = self.game.info

        if root_ui:
            self.master = tk.Toplevel(root_ui)
        else:
            self.master = tk.Tk()
        man_config.read_ini_file(self.master, self.info.name)

        self.master.title(self.info.name)
        self.master.option_add('*tearOff', False)
        self.master.wm_geometry('+150+150')

        super().__init__(self.master)
        self.master.report_callback_exception = self._exception_callback

        self.vars = TkVars(self, player_dict)
        self._set_difficulty()

        self.pack(expand=True, fill=tk.BOTH)
        self._create_menus()

        self.tally = None
        self.rframe = None
        self._add_statuses()

        self.disp = [[None] * self.game.cts.holes,
                     [None] * self.game.cts.holes]
        self.stores = None
        self._add_board()

        tally = man_config.CONFIG.get_bool('show_tally')
        self.vars.show_tally.set(tally)
        if not tally:
            self.tally_frame.forget()

        self._new_game()
        self._refresh()
        self._schedule_ai()


    def _add_statuses(self):
        """Add status and info panes. Make them each 50% of the display."""

        self.tally_frame = tk.Frame(self)
        self.tally_frame.pack(side=tk.TOP, expand=True, fill=tk.X)

        lframe = tk.Frame(self.tally_frame, padx=5, pady=5,
                          borderwidth=3, relief=tk.RIDGE)
        lframe.grid(row=0, column=0, sticky=tk.NSEW)

        goal = self.game.info.goal
        if goal in round_tally.RoundTally.GOALS:
            self.tally = gt.GameTally(lframe,
                                      round_tally.RoundTally.PSTR[goal],
                                      self.game.info.goal_param)
        else:
            self.tally = gt.GameTally(lframe)

        self.rframe = tk.Frame(self.tally_frame, padx=5, pady=5,
                               borderwidth=3, relief=tk.RIDGE)
        self.rframe.grid(row=0, column=1, sticky=tk.NSEW)

        self.tally_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self.tally_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        self.tally_frame.grid_rowconfigure(0, weight=1)


    def _add_board(self):
        """Add the game board frame and widgets.
        Use aspect frame for the interior elements so that they
        maintain a squarish elements when resized."""

        board_frame = tk.Frame(self, borderwidth=7, relief=tk.RAISED)
        board_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

        if self.info.stores:
            b_frame = aspect_frame.AspectFrames(board_frame,
                                                aratio=0.8)
            b_frame.pad.grid(row=0, column=0, sticky="nsew")

            b_store = buttons.StoreButton(b_frame.content, self, True)
            b_store.grid(row=0, column=0, sticky="nsew")
            b_frame.row_col_config()

        land_frame = aspect_frame.AspectFrames(board_frame,
                                               aratio=self.game.cts.holes / 2)
        land_frame.pad.grid(row=0, column=1, sticky="nsew")

        for row in range(2):
            dirs = self._get_hole_dirs(row)

            for pos in range(self.game.cts.holes):
                btn = self._build_button(land_frame.content, row, pos, dirs)
                self.disp[row][pos] = btn
                self.disp[row][pos].grid(row=row, column=pos,
                                         sticky="nsew")
        land_frame.row_col_config()

        if self.info.stores:
            a_frame = aspect_frame.AspectFrames(board_frame,
                                                aratio=0.8)
            a_frame.pad.grid(row=0, column=2, sticky="nsew")

            a_store = buttons.StoreButton(a_frame.content, self, False)
            a_store.grid(row=0, column=0, sticky="nsew")
            a_frame.row_col_config()

            self.stores = [b_store, a_store]

            board_frame.grid_rowconfigure(0, weight=1)
            board_frame.grid_columnconfigure([0, 2], weight=1)
            board_frame.grid_columnconfigure(1, weight=self.game.cts.holes)

        else:
            board_frame.grid_rowconfigure(0, weight=1)
            board_frame.grid_columnconfigure('all', weight=1)


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

        return buttons.HoleButton(land_frame, self, loc, left_move, rght_move)


    @staticmethod
    def _exception_callback(*args):
        """Support debugging by printing the play_log and the traceback."""

        game_log.dump()
        traceback.print_exception(args[0], args[1], args[2])


    def _set_log_level(self):
        """Set the game log level"""

        game_log.level = self.vars.log_level.get()


    def _create_menus(self):
        """Create the game control menus."""

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        gamemenu = tk.Menu(menubar)
        gamemenu.add_command(label='New', command=self._new_game)
        gamemenu.add_separator()
        gamemenu.add_command(label='Swap Sides', command=self._pie_rule)
        gamemenu.add_separator()
        gamemenu.add_command(label='End Round', command=self._end_round)
        gamemenu.add_command(label='End Game', command=self._end_game)
        menubar.add_cascade(label='Game', menu=gamemenu)

        aimenu = tk.Menu(menubar)
        aimenu.add_checkbutton(label='AI Player',
                               variable=self.vars.ai_active,
                               onvalue=True, offvalue=False,
                               command=self._schedule_ai)

        aimenu.add_separator()
        aimenu.add_radiobutton(label='No AI Delay',
                               variable=self.vars.ai_delay, value=0)
        aimenu.add_radiobutton(label='Short AI Delay',
                               variable=self.vars.ai_delay, value=1)
        aimenu.add_radiobutton(label='Long AI Delay',
                               variable=self.vars.ai_delay, value=2)

        aimenu.add_separator()
        aimenu.add_radiobutton(label='Easy',
                               value=0, variable=self.vars.difficulty,
                               command=self._set_difficulty)
        aimenu.add_radiobutton(label='Normal',
                               value=1, variable=self.vars.difficulty,
                               command=self._set_difficulty)
        aimenu.add_radiobutton(label='Hard',
                               value=2, variable=self.vars.difficulty,
                               command=self._set_difficulty)
        aimenu.add_radiobutton(label='Expert',
                               value=3, variable=self.vars.difficulty,
                               command=self._set_difficulty)

        menubar.add_cascade(label='AI', menu=aimenu)

        logmenu = tk.Menu(menubar)
        logmenu.add_command(label='Show Prev', command=game_log.prev)
        logmenu.add_command(label='Show Log', command=game_log.dump)
        logmenu.add_command(label='Save Log', command=self._save_file)
        logmenu.add_separator()

        logmenu.add_radiobutton(
            label='Moves',
            value=game_log.MOVE, variable=self.vars.log_level,
            command=self._set_log_level)
        logmenu.add_radiobutton(
            label='Important',
            value=game_log.IMPORT, variable=self.vars.log_level,
            command=self._set_log_level)
        logmenu.add_radiobutton(
            label='Steps',
            value=game_log.STEP, variable=self.vars.log_level,
            command=self._set_log_level)
        logmenu.add_radiobutton(
            label='Information',
            value=game_log.INFO, variable=self.vars.log_level,
            command=self._set_log_level)
        logmenu.add_radiobutton(
            label='Detail',
            value=game_log.DETAIL, variable=self.vars.log_level,
            command=self._set_log_level)
        logmenu.add_radiobutton(
            label='Simulated Moves',
            value=game_log.SIMUL, variable=self.vars.log_level,
            command=self._set_log_level)
        logmenu.add_separator()
        logmenu.add_checkbutton(
            label='Live Log',
            onvalue=True, offvalue=False,
            variable=self.vars.live_log,
            command=lambda: setattr(game_log, 'live', self.vars.live_log.get()))
        logmenu.add_checkbutton(label='Log AI Analysis',
                                variable=self.vars.log_ai,
                                onvalue=True, offvalue=False)
        logmenu.add_checkbutton(label='Filter AI Scores',
                                variable=self.vars.ai_filter,
                                onvalue=True, offvalue=False,)

        menubar.add_cascade(label='Log', menu=logmenu)

        showmenu = tk.Menu(menubar)
        showmenu.add_checkbutton(label='Show Tally',
                                 variable=self.vars.show_tally,
                                 onvalue=True, offvalue=False,
                                 command=self._toggle_tally)
        showmenu.add_separator()
        showmenu.add_checkbutton(label='Touch Screen',
                                 variable=self.vars.touch_screen,
                                 onvalue=True, offvalue=False,
                                 command=self._refresh)
        showmenu.add_checkbutton(label='Facing Players',
                                 variable=self.vars.facing_players,
                                 onvalue=True, offvalue=False,
                                 command=self.toggle_facing)
        showmenu.add_checkbutton(label='Ownership Arrows',
                                 variable=self.vars.owner_arrows,
                                 onvalue=True, offvalue=False,
                                 command=self._refresh)
        menubar.add_cascade(label='Display', menu=showmenu)

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


    def _toggle_tally(self, vis_op=NO_TALLY_OP):
        """Adjust tally frame visibility."""

        if vis_op == VIS_TALLY_OP:
            # force tally to be visible (status pane is needed)
            self.tally_frame.pack(side=tk.TOP, expand=True, fill=tk.X)
            self.vars.tally_was_off = not self.vars.show_tally.get()
            self.vars.show_tally.set(True)

        elif vis_op == RET_TALLY_OP and self.vars.tally_was_off:
            # return tally to the state it was before VIS_TALLY_OP called
            self.tally_frame.forget()
            self.vars.show_tally.set(False)
            self.vars.tally_was_off = False

        elif self.mode == buttons.Behavior.GAMEPLAY:
            # only allow user toggle when in GAMEPLAY state
            if self.vars.show_tally.get():
                self.tally_frame.pack(side=tk.TOP, expand=True, fill=tk.X)
            else:
                self.tally_frame.forget()

        else:
            self.bell()
            self.vars.show_tally.set(True)


    def toggle_facing(self):
        """Players are facing eachother. Force a configure event,
        it orients and sizes the dithering (for touch screen mode)
        and then refresh to rotate the text."""

        # all hole buttons are the same size
        width = self.disp[0][0].winfo_width()
        height = self.disp[0][0].winfo_height()

        for pos in range(self.game.cts.holes):
            self.disp[0][pos].event_generate("<Configure>",
                                             width=width, height=height)
        self._refresh()


    @staticmethod
    def _try_help_file(filename, tag=None):
        """Attempt to pop open the help file.
        Return True if it no problems detected."""

        pathname = man_path.get_path(filename, no_error=True)
        if pathname:
            if tag:
                pathname += '#' + tag.replace(' ', '%20')

            webbrowser.open('file:///' + pathname)
            return True

        return False


    def _help(self):
        """If the game has a help file, open it.
        If not, try to open the about_games at the specified game name.
        If that doesn't work, try the default help file.
        If that doesn't work, pop up a "no help" message."""

        _ = ((self.info.help_file
              and self._try_help_file(self.info.help_file))
             or self._try_help_file('about_games.html', self.info.name)
             or self._try_help_file('mancala_help.html')
             or quiet_dialog(self, 'Help', 'Help not found.'))


    def _about(self):
        """Popup the about window."""

        atext = self.info.about
        if not atext or (isinstance(atext, str) and not atext.strip()):
            atext = 'Mancala Game Player'

        paragraphs = atext.split('\n')
        out_text = self.info.name + ':\n'
        for para in paragraphs:
            out_text += textwrap.fill(para, 70) + '\n'

        out_text += version.RELEASE_TEXT

        quiet_dialog(self, 'About', ''.join(out_text))


    def _save_file(self):
        """Save the game log to the file, provide a string that
        describes the game."""
        game_log.save(self.game.params_str())


    def _button_state(self, allows, ai_turn, loc, aidx):
        """Return one of the four button states.

        Cannot do East/West coloring the way North/South
        is done. Diffusion requires moves from all holes
        and Ohojichi requires moves from all holes (move
        only own holes, capture placement opps holes)."""

        turn = self.game.turn
        owner = self.game.owner[loc]
        true_hole = self.game.true_holes[loc]
        all_holes = self.info.no_sides

        player_hole = (owner == turn
                       or all_holes
                       or (not all_holes
                           and owner is None
                           and true_hole == turn))

        if player_hole and allows[aidx]:

            if ai_turn and (true_hole or all_holes):
                btnstate = behaviors.BtnState.LOOK_ACTIVE

            else:
                btnstate = behaviors.BtnState.ACTIVE

            # translate state if can only sow in one direction
            if allows[aidx] == [False, True]:
                if btnstate == behaviors.BtnState.LOOK_ACTIVE:
                    btnstate = behaviors.BtnState.LACT_CCW_ONLY
                else:
                    btnstate = behaviors.BtnState.ACT_CCW_ONLY

            elif allows[aidx] == [True, False]:
                if btnstate == behaviors.BtnState.LOOK_ACTIVE:
                    btnstate = behaviors.BtnState.LACT_CW_ONLY
                else:
                    btnstate = behaviors.BtnState.ACT_CW_ONLY

        elif player_hole and not all_holes:
            btnstate = behaviors.BtnState.PLAY_DISABLE

        else:
            btnstate = behaviors.BtnState.DISABLE

        return btnstate


    def _refresh(self):
        """Make UI match mancala game."""

        turn = self.game.get_turn()
        allows = self.game.get_allowable_holes()
        turn_row = int(not turn)
        ai_turn = self.vars.ai_active.get() and turn
        for row in range(2):

            player = row == turn_row
            if self.info.stores:
                if self.info.goal in (gi.Goal.DEPRIVE, gi.Goal.CLEAR):
                    seeds = 0
                else:
                    seeds = self.game.store[not row]
                self.stores[row].set_store(seeds, player)

            for pos in range(self.game.cts.holes):

                if self.mode != buttons.Behavior.GAMEPLAY:
                    if player:
                        btnstate = behaviors.BtnState.ACTIVE
                    else:
                        btnstate = behaviors.BtnState.DISABLE

                else:
                    aidx = pos
                    loc = self.game.cts.xlate_pos_loc(row, pos)
                    if self.game.info.mlength == 3:
                        aidx = loc

                    btnstate = self._button_state(allows, ai_turn,
                                                  loc, aidx)

                self.disp[row][pos].set_props(
                    self.game.get_hole_props(row, pos),
                    btnstate)


    def _start_it(self):
        """Do the last steps in starting a new game:
        log the start and check for ai's turn."""
        game_log.new()
        game_log.turn(0, 'Start Game', self.game)
        self._schedule_ai()


    def _not_playable_new_round(self):
        """The new round is not playable by the starter."""

        self._refresh()
        tk.messagebox.showerror(
            title="New Round Not Playable",
            message="The new round resulted in a unplayable game. " \
                "New game started.")


    def _new_game(self, win_cond=None, new_round_ok=False):
        """Start a new game and refresh the board."""
        # pylint: disable=too-complex

        self._cancel_pending_afters()

        new_game = self.game.new_game(win_cond=win_cond,
                                      new_round_ok=new_round_ok)
        self.player.clear_history()
        self.set_game_mode(buttons.Behavior.GAMEPLAY, force=True)

        self._refresh()
        if new_game:
            self._param_tally()

            if self.info.prescribed == gi.SowPrescribed.ARNGE_LIMIT:
                if self.set_game_mode(buttons.Behavior.MOVESEEDS):
                    return

        elif not self.game.is_new_round_playable():
            self._not_playable_new_round()

        elif self.info.round_fill == gi.RoundFill.UCHOOSE:
            if self.set_game_mode(buttons.Behavior.RNDCHOOSE):
                return

        elif self.info.round_fill == gi.RoundFill.UMOVE:
            if self.set_game_mode(buttons.Behavior.RNDMOVE):
                return

        elif self.info.round_fill == gi.RoundFill.UCHOWN:
            if self.set_game_mode(buttons.Behavior.RNDCHOWN):
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

        assert not force or force and mode == buttons.Behavior.GAMEPLAY, \
            "Don't force game mode change for anything but normal game play."

        if force:
            buttons.force_mode_change()

        elif not buttons.ask_mode_change(self.mode, mode, self):
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
        if mode == buttons.Behavior.GAMEPLAY:
            self._start_it()
            self._toggle_tally(vis_op=RET_TALLY_OP)
        else:
            self._toggle_tally(vis_op=VIS_TALLY_OP)
        return True


    def set_gameplay_mode(self):
        """The behaviors file cannot import btn_behaviors
        (circular deps), but the behavior objects have a
        pointer to the game_ui object so we'll set_gameplay_move
        for them here"""

        return self.set_game_mode(buttons.Behavior.GAMEPLAY)


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


    def _param_tally(self):
        """If playing a game with a param tally, updat the UI"""

        param_func = self.game.rtally_param_func()
        if param_func:
            self.tally.param_tally(param_func)


    def _win_message_popup(self, win_cond):
        """If someone won or there was a tie,
        popup the winner dialog box."""

        if win_cond:
            self.tally.tally_game(self.game.get_turn(), win_cond)
            self._param_tally()

            self._win_popup(*self.game.win_message(win_cond))


    def _pie_rule(self):
        """Allow a human player to swap sides after the first
        move, aka 'Pie Rule'.
        Only allowed on the first move of the game.
        This is often used to nutralize the unfair advantage
        that starter of some games has.  Not all mancala games
        have an advantage for the starter, but allow it for all.

        The AI history is cleared which currently only applies to
        MCTS. This does seem extreme but the AI turn and node tree
        have already been started correcting them seems error prone."""

        game = self.game
        if game.mcount != 1:
            tk.messagebox.showerror(
                title="Swap Not Allowed",
                message="Swapping sides is only allowed by a " \
                    "human player after the first move.")
            return

        game.mcount += 1
        holes = game.cts.holes
        dholes = game.cts.dbl_holes
        game.board =  game.board[holes:dholes] + game.board[0:holes]
        game.store = list(reversed(game.store))
        game.turn = not game.turn

        self.player.clear_history()

        self._refresh()
        game_log.turn(game.mcount, "Swap Sides (pie rule)", game)

        self._schedule_ai()


    def _end_round(self):
        """End the round. Report result to user."""

        if not self.game.info.rounds or self.mode != buttons.Behavior.GAMEPLAY:
            self._end_game()
            return

        message = 'Are you sure you wish to end the round?'
        do_it = tk.messagebox.askokcancel(title='End Round',
                                          message=message,
                                          parent=self)
        if not do_it:
            return

        win_cond = self.game.end_round()

        wtext = 'Round Ended '
        if win_cond in (gi.WinCond.WIN, gi.WinCond.ROUND_WIN):
            sturn = 'Top' if self.game.get_turn() else 'Bottom'
            wtext += f'\n{win_cond.name} by {sturn}'
        elif win_cond:
            wtext += ' ' + win_cond.name
        game_log.turn(self.game.mcount, wtext, self.game)

        self._refresh()
        self._win_message_popup(win_cond)
        self._new_game(win_cond=win_cond, new_round_ok=True)


    def _end_game(self):
        """End the game. Report result to user."""

        if self.mode != buttons.Behavior.GAMEPLAY:
            message = 'End game during setup will force New Game. Continue?'
            do_it = tk.messagebox.askokcancel(title='End Game',
                                              message=message,
                                              parent=self)
            if do_it:
                self._new_game()
            return

        message = 'Are you sure you wish to end the game?'
        do_it = tk.messagebox.askokcancel(title='End Game', message=message,
                                          parent=self)
        if not do_it:
            return

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

        diff = self.vars.difficulty.get()
        self.player.difficulty = diff
        game_log.add(f'Changing difficulty {diff}', game_log.INFO)


    def _log_turn(self, last_turn):
        """Add the ai description to the game log (Mancala doesn't
        know if the ai is playing)."""

        if (last_turn
                and self.vars.ai_active.get()
                and not self.vars.ai_filter.get()):
            game_log.add(self.player.get_move_desc(), game_log.MOVE)


    def move(self, move):
        """Tell game to move, refresh the UI, and
        handle any win conditions."""

        last_turn = self.game.get_turn()
        win_cond = self.game.move(move)

        self._log_turn(last_turn)
        self._refresh()

        if win_cond and win_cond != gi.WinCond.REPEAT_TURN:
            self._win_message_popup(win_cond)
            self._new_game(win_cond=win_cond, new_round_ok=True)
            return

        if self.vars.ai_active.get() and self.game.get_turn():
            self._schedule_ai()

        elif self.info.mustpass and self.game.test_pass():

            player = 'Bottom' if self.game.get_turn() else 'Top'
            message = f'{player} player has no moves and must pass.'
            tk.messagebox.showinfo(title='Pass Move', message=message,
                                   parent=self)

            self._schedule_ai()


    def _schedule_ai(self):
        """Do AI move or schedule the AI turn (if the AI is enabled
        and it's the AI's turn)."""

        if self.vars.ai_active.get() and self.game.get_turn():
            self._refresh()
            self._cancel_pending_afters()
            sel_delay = self.vars.ai_delay.get()

            self.after(AI_DELAY[sel_delay], self._ai_move)


    def _ai_move(self):
        """If it's the AI's turn, do a move. AI is top player."""

        if self.vars.ai_active.get() and self.game.get_turn():

            if not self.vars.log_ai.get():
                game_log.set_ai_mode()

            move = self.player.pick_move()
            game_log.clear_ai_mode()
            self.move(move)

            if (self.game.info.sow_direct == gi.Direct.PLAYALTDIR
                and self.game.mcount == 1):

                message = 'Player direction is ' + move[-1].opp_dir().name
                tk.messagebox.showinfo(title='Player Direction',
                                       message=message,
                                       parent=self)
