# -*- coding: utf-8 -*-
"""Create the UI for a mancala game_constants and game_info
define how the game is created and played.
The values of those two variables must not be changed during
game play.

Created on Thu Mar  2 14:38:17 2023
@author: Ann"""


# %% imports

import functools as ft
import tkinter as tk
import warnings

import ai_player
import animator
import aspect_frame
import cfg_keys as ckey
import behaviors
import buttons
import format_msg as fmt
import game_info as gi
import game_logger
import game_tally as gt
import inhibitor
import mancala
import man_config
import man_history
import man_ui_cmd_mixins as ui_cmds
import round_tally
import sower
import ui_utils

from game_logger import game_log


# %%   constants

AI_DELAY = [5, 1000, 4000]

RTURN_QUERY = 10
RTURN_QFREQ = 5

ROUND = 'round'


# %%

class TkVars:
    """Collect the tk status variables here and one stray."""

    def __init__(self, man_ui, player_dict):

        self.no_endless = tk.BooleanVar(
            man_ui.master, man_config.CONFIG.get_bool('no_endless'))

        # must be visible for construction
        self.show_tally = tk.BooleanVar(man_ui.master, True)
        self.tally_was_off = False

        self.facing_players = tk.BooleanVar(
            man_ui.master, man_config.CONFIG.get_bool('facing_players'))
        self.touch_screen = tk.BooleanVar(
            man_ui.master, man_config.CONFIG.get_bool('touch_screen'))
        self.owner_arrows = tk.BooleanVar(
            man_ui.master, man_config.CONFIG.get_bool('owner_arrows'))

        # if available, must be visible for construction
        iavail = InhibitIndicator.needed(man_ui.game.inhibitor)
        self.show_inhibit = tk.BooleanVar(man_ui.master, iavail)

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

        ani_active = man_config.CONFIG.get_bool('ani_active')
        self.ani_active = tk.BooleanVar(man_ui.master, ani_active)


# %%  mancala ui

class MancalaUI(ui_cmds.GameCmdsMixin,
                ui_cmds.VariCmdsMixin,
                ui_cmds.SetupCmdsMixin,
                ui_cmds.MoveMenuMixin,
                ui_cmds.AiCtrlMenuMixin,
                ui_cmds.ShowMenuMixin,
                ui_cmds.AniMenuMixin,
                ui_cmds.GLogMenuMixin,
                ui_cmds.DebugMenuMixin,
                ui_cmds.HelpMenuMixin,
                tk.Frame):
    """A manacala UI."""

    def __init__(self, game, player_dict,
                 *, player=None, root_ui=None, pcleanup=None):
        """Create the UI for a mancala game.

        game: class to provide the mechanics of the game w/o any UI

        player_dict: the player element from game config file;
        a dictionary of parameters to configure the ai player

        player (optional): a prebuilt ai player.
        Building the player checks the rules and MancalaGames
        pre-tests the configuration; building the player
        twice generated duplicated errors.

        root_ui (optional): if this is started as part of another
        application provide the tk root.

        pcleanup (optional): if provided, call to tell the parent
        to cleanup on destroy.
        It is not called if the game is reconfigured via variants,
        but is passed on to the next MancalaUI instance.
        This should be a parameterless function/method."""
        # pylint: disable=too-many-statements

        self.game = game
        self.info = self.game.info
        self.mode = buttons.Behavior.GAMEPLAY
        self.player = player if player else \
                          ai_player.AiPlayer(self.game, player_dict)
        self.swap_ok = True
        self.wcond = None   #  used between the movers and epilogs
        self.saved_move = None
        self.pcleanup = pcleanup

        game_log.new()
        game_log.turn(0, 'Start Game', game)

        if root_ui:
            self.root = root_ui
            self.master = tk.Toplevel(root_ui)
        else:
            self.root = tk.Tk()
            self.master = self.root
            ui_utils.setup_styles(self.root)
            warnings.showwarning = ft.partial(self.vari_show_error, self)
            warnings.simplefilter('always', UserWarning)

        man_config.read_ini_file(self.master, self.info.name)
        super().__init__(self.master)
        self.master.title(self.info.name)
        self.pack(expand=True, fill=tk.BOTH)

        ui_utils.do_error_popups(self.root, self)

        hsize = man_config.CONFIG.get_int('history_size')
        self.history = man_history.HistoryManager(hsize,
                                                  mancala.GameState.str_one)
        self.tkvars = TkVars(self, player_dict)
        self.ai_set_difficulty()

        self.tally = None
        self.rframe = None
        self._add_statuses()

        self.disp = [[None] * self.game.cts.holes,
                     [None] * self.game.cts.holes]
        self.stores = None
        self.inhibits = None
        self._add_board()

        self._menubar = None
        self._create_menus()
        self._key_bindings(active=True)

        self.show_update_after_const()

        animator.make_animator(self)
        animator.configure(font=man_config.CONFIG.get_ani_font(),
                           msg_mult=man_config.CONFIG.get_int('ani_msg_mult'),
                           bg_color=man_config.CONFIG['ani_background'])
        self.ani_reset_state()
        self.ani_reset_delay()

        buttons.build_behaviors()

        self.no_endless_sows()
        self.new_game()
        self.schedule_ai()


    def _add_statuses(self):
        """Add status and info panes. Make them each 50% of the display."""

        self.tally_frame = tk.Frame(self)
        self.tally_frame.pack(side=tk.TOP, expand=True, fill=tk.X)

        # create this and never hide it, to force resizing
        tk.Frame(self.tally_frame, width=1, height=1).grid(row=1, column=0)

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
        # create this and never hide it, to force resizing
        tk.Frame(self.rframe, width=1, height=1).pack()

        self.tally_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self.tally_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        self.tally_frame.grid_rowconfigure(0, weight=1)


    def _add_board(self):
        """Add the game board frame and widgets.
        Use aspect frame for the interior elements so that they
        maintain a squarish elements when resized."""

        board_frame = tk.Frame(self, borderwidth=7, relief=tk.RAISED)
        board_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

        land_frame = aspect_frame.AspectFrames(board_frame,
                                               aratio=self.game.cts.holes / 2)
        land_frame.pad.grid(row=0, column=1, sticky="nsew")

        for row in range(2):
            dirs = self._get_hole_dirs(row)

            for pos in range(self.game.cts.holes):
                btn = self._build_button(land_frame.content, row, pos, dirs)
                self.disp[row][pos] = btn
                self.disp[row][pos].grid(row=row, column=pos, sticky="nsew")
        land_frame.row_col_config()

        # add the stores and indicator widgets
        need_inhibit = InhibitIndicator.needed(self.game.inhibitor)
        if self.info.stores or need_inhibit:
            left_frame = tk.Frame(board_frame)
            left_frame.grid(row=0, column=0, sticky="nsew")
            right_frame = tk.Frame(board_frame)
            right_frame.grid(row=0, column=2, sticky="nsew")

            # create these and never remove them to force resizing
            tk.Frame(left_frame, width=1, height=1).grid(row=0, column=3)
            tk.Frame(right_frame, width=1, height=1).grid(row=0, column=3)

        if self.info.stores:
            tstore = self._build_store(left_frame, True)
            fstore = self._build_store(right_frame, False)
            self.stores = [tstore, fstore]

        if need_inhibit:
            tinhibit = InhibitIndicator(left_frame, True, self.game.inhibitor)
            finhibit = InhibitIndicator(right_frame, False, self.game.inhibitor)
            self.inhibits = [tinhibit, finhibit]

        if self.info.stores or need_inhibit:
            left_frame.grid_rowconfigure(0, weight=1)
            left_frame.grid_columnconfigure('all', weight=1)

            right_frame.grid_rowconfigure(0, weight=1)
            right_frame.grid_columnconfigure('all', weight=1)

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


    def _build_store(self, parent, side):
        """Build a store for the board in an aspect_frame,
        return the store object."""

        frame = aspect_frame.AspectFrames(parent, aratio=0.8)
        frame.pad.grid(row=0, column=0, sticky="nsew")

        store = buttons.StoreButton(frame.content, self, side)
        store.grid(row=0, column=0, sticky="nsew")

        frame.row_col_config()

        return store


    def _create_menus(self):
        """Create the game control menus.

        Do keybinds that should be disabled during animations
        in _key_bindings."""

        self.master.option_add('*tearOff', False)

        self._menubar = tk.Menu(self.master)
        self.master.config(menu=self._menubar)

        gamemenu = tk.Menu(self._menubar, name='game')
        self.game_add_menu_cmds(gamemenu)
        self.vari_add_menu_cmds(gamemenu)
        self.setup_add_menu_cmds(gamemenu)
        self._menubar.add_cascade(label='Game', menu=gamemenu)

        self.move_add_menu(self._menubar)
        self.ai_add_menu(self._menubar)
        self.show_add_menu(self._menubar)
        self.ani_add_menu(self._menubar)
        self.glog_add_menu(self._menubar)
        self.help_add_menu(self._menubar)
        self.dbg_add_menu(self._menubar)


    def menubar_state(self, active=True):
        """Activate or deactivate the menus.
        The animator menu is left active."""

        state = tk.NORMAL if active else tk.DISABLED

        self._menubar.entryconfig('Game', state=state)
        self._menubar.entryconfig('Move', state=state)
        self._menubar.entryconfig('Player', state=state)
        self._menubar.entryconfig('Display', state=state)
        self._menubar.entryconfig('Log', state=state)
        self._menubar.entryconfig('Help', state=state)

        # if ui_cmds.DEBUG in self._menubar.children:
        #     self._menubar.entryconfig('Debug', state=state)


    def _key_bindings(self, active=True):
        """Bind or unbind the keys that should not be active
        while the animations are running."""

        bindings = [('<Control-z>', self.move_undo),
                    ('<Control-Z>', self.move_redo),
                    ]
        ui_utils.key_bindings(self, bindings, active)


    def _cancel_pending_afters(self):
        """Cancel any pending after methods."""

        afters = self.tk.eval('after info')
        # print(f"cancel pending afters: {afters or 'None'}")
        for after_id in afters.split():
            self.after_cancel(after_id)


    def destroy(self):
        """Window was closed.

        Cancel any pending afters, destroy the behavior globals,
        tell the error_popups to stop dumping the game on errors,
        and reset the animator.

        If a cleanup method was provided call it."""

        self._cancel_pending_afters()
        buttons.destroy_behaviors()
        ui_utils.game_ui = None
        animator.reset()

        if self.pcleanup:
            self.pcleanup()


    def rebuild(self, newgame, pdict, player):
        """Destory and rebuild the game. This is used by the
        VariCmdsMixin--it must be here for the scope of MancalaUI.

        Do not call the parent cleanup function, but pass it on to
        the next MancalaUI instance."""

        pcleanup = self.pcleanup
        self.pcleanup = None

        if self.root is self.master:
            self.root.destroy()
            self.root = None
        else:
            self.master.destroy()
        del self.game

        MancalaUI(newgame, pdict,
                  player=player, root_ui=self.root, pcleanup=pcleanup)


    def _button_state(self, allows, ai_turn, loc, aidx):
        """Return one of the four button states.

        Cannot do East/West coloring the way North/South
        is done. Diffusion requires moves from all holes
        and Ohojichi requires moves from all holes (move
        only own holes, capture placement opps holes)."""

        turn = self.game.turn
        owner = self.game.owner[loc]
        true_hole = self.game.cts.board_side(loc)
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


    def set_ui_active(self, active, frame=None):
        """Activate or deactivate the Hole and Store Buttons,
        recursing through frames. Also, on the first call,
        activate/deactivate the key bindings and menus
        (animation controls are always active).

        Not using the tk state for Hole & Store Buttons, because
        it's overridden on every refresh."""

        if not frame:
            self._key_bindings(active)
            self.menubar_state(active)
            frame = self

        for child in frame.winfo_children():

            if isinstance(child, tk.Frame):
                self.set_ui_active(active, child)

            elif isinstance(child, (buttons.HoleButton,
                                    buttons.StoreButton)):
                child.active = active


    def show_seeds_in_stores(self):
        """Return True if the stores should be updated with a
        seed count, False otherwise."""

        return (self.stores
                and (not self.info.goal.eliminate()
                     or self.info.start_pattern == gi.StartPattern.AZIGO))


    def refresh(self, *, ani_ok=False):
        """Make UI match mancala game."""

        if ani_ok and animator.active():
            self.set_ui_active(active=False)
            animator.do_animation()
            return

        self.set_ui_active(True)
        turn = self.game.turn

        allows = self.game.get_allowable_holes()
        turn_row = int(not turn)
        ai_turn = self.tkvars.ai_active.get() and turn
        for row in range(2):

            if self.inhibits:
                self.inhibits[row].update()

            player = row == turn_row
            if self.info.stores:
                if self.show_seeds_in_stores():
                    seeds = self.game.store[not row]
                else:
                    seeds = 0
                self.stores[row].set_store(seeds, player)

            for pos in range(self.game.cts.holes):

                if self.mode in (buttons.Behavior.GAMEPLAY,
                                 buttons.Behavior.SETUP):
                    aidx = pos
                    loc = self.game.cts.xlate_pos_loc(row, pos)
                    if self.game.info.mlength == 3:
                        aidx = loc

                    btnstate = self._button_state(allows, ai_turn,
                                                  loc, aidx)

                elif player:
                    btnstate = behaviors.BtnState.ACTIVE
                else:
                    btnstate = behaviors.BtnState.DISABLE

                self.disp[row][pos].set_props(
                    self.game.get_hole_props(row, pos),
                    btnstate)


    def _startup_msgs(self):
        """Return true if there should be a startup delay for
        a start up message."""

        if not animator.active() or self.game.movers:
            # movers > 0 when exiting setup
            return False

        return (self.game.inhibitor.stop_me_capt(self.game.turn)
                or self.game.inhibitor.stop_me_child(self.game.turn)
                or self.game.info.prescribed in (gi.SowPrescribed.SOW1OPP,
                                                 gi.SowPrescribed.PLUS1MINUS1,
                                                 gi.SowPrescribed.NO_UDIR_FIRSTS)
                or self.game.deco.new_game.startup_msg)


    def start_it(self):
        """Do the last steps in starting a new game: log the start,
        reset the animator state, and check for ai's turn.
        If the animator is active and anything is inhibited,
        delay the inhibitor start message until the main
        window is displayed.

        Check movers count so that we do not show start up animation
        after setup."""

        game_log.new()
        game_log.turn(0, 'Start Game', self.game)
        self.history.record(self.game.state)

        self.ani_reset_state()
        if self._startup_msgs():
            self.update_idletasks()
            self.after(100, self._ani_delayed_startup)
        else:
            self.schedule_ai()


    def _ani_delayed_startup(self):
        """Delay the inhibitor message until after the main
        window is fully rendered.  Use the animator queue to
        do a final refresh and schedule the ai."""

        self.game.deco.new_game.start_ani_msg()
        self.game.inhibitor.start_ani_msg()
        sower.start_ani_msg(self.game)
        animator.queue_callback(self.refresh)
        animator.queue_callback(self.schedule_ai)
        self.refresh(ani_ok=True)


    def _not_playable_new_round(self):
        """The new round is not playable by the starter."""

        self.refresh()
        ui_utils.showerror(
            self,
            "New Round Not Playable",
           """The new round resulted in a unplayable game.
           New game started.""")


    def _set_swap_ok(self, new_round):
        """Set swap ok. Only allowed for the first round for
        TERRITORY games and games with rounds and blocks."""

        self.swap_ok = not (new_round
                            and (self.game.info.goal == gi.Goal.TERRITORY
                                 or (self.game.info.rounds
                                     and self.game.info.blocks)))


    def _mode_check_start_game(self, new_round):
        """Check and execute mode change, return False.
        If game is not playable, return True.
        Otherwise, return True"""

        rval = True
        if not new_round:
            self.param_tally()

            if (self.info.prescribed == gi.SowPrescribed.ARNGE_LIMIT
                    and self.set_game_mode(buttons.Behavior.MOVESEEDS)):
                rval = False

        elif not self.game.is_new_round_playable():
            self._not_playable_new_round()

        elif (self.info.round_fill in (gi.RoundFill.UCHOOSE,
                                       gi.RoundFill.LOSER_ONLY)
                  and self.set_game_mode(buttons.Behavior.RNDCHOOSE)):
            rval = False

        elif (self.info.round_fill == gi.RoundFill.UMOVE
                  and self.set_game_mode(buttons.Behavior.RNDMOVE)):
            rval = False

        elif (self.info.round_fill == gi.RoundFill.UCHOWN
                  and self.set_game_mode(buttons.Behavior.RNDCHOWN)):
            rval = False

        return rval


    def new_game(self, new_round=False):
        """Start a new game and refresh the board."""

        self._cancel_pending_afters()
        self.master.config(cursor=ui_utils.NORMAL)
        animator.set_active(False, reset_queue=True)

        end_state = self.history.end_game_state()
        if end_state:
            self.game.state = end_state
            self.param_tally()
        self.history.clear()

        self.player.clear_history()
        self._set_swap_ok(new_round)
        self.game.new_game(new_round)
        self.set_game_mode(buttons.Behavior.GAMEPLAY, force=True)

        self.refresh()
        if self._mode_check_start_game(new_round):
            self.start_it()


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

        mismatch = (sum(self.game.store) + sum(self.game.board) !=
                    self.game.cts.total_seeds)
        if mismatch:
            if mode == buttons.Behavior.SETUP:
                # some games remove seeds from the board in the ender
                # if a player uses 'wait' and then tries to enter setup
                # there can be a legitimate mis-match
                msg = """Seeds are missing from the board;
                      the initial board will be setup."""
                ui_utils.showwarning(self, 'Seed Count Error', msg)
                self.new_game()
            else:
                assert not mismatch, 'Seed count mismatch during UI mode change.'

        self.mode = mode
        for button_row in self.disp:
            for btn in button_row:
                btn.set_behavior(mode)
        if self.stores:
            self.stores[0].set_behavior(mode)
            self.stores[1].set_behavior(mode)

        self.refresh()
        if mode == buttons.Behavior.GAMEPLAY:
            self.start_it()
            self.show_toggle_tally(vis_op=ui_cmds.RET_TALLY_OP)
        else:
            self.show_toggle_tally(vis_op=ui_cmds.VIS_TALLY_OP)
        return True


    def set_gameplay_mode(self):
        """The behaviors file cannot import btn_behaviors
        (circular deps), but the behavior objects have a
        pointer to the game_ui object so we'll mode
        for them here"""

        if self.set_game_mode(buttons.Behavior.GAMEPLAY):
            self.ani_reset_state()
            return True
        return False


    def param_tally(self):
        """If playing a game with a param tally, update the UI"""

        param_func = self.game.rtally_param_func()
        if param_func:
            self.tally.param_tally(param_func)


    def _win_message_popup(self, win_cond):
        """If someone won or there was a tie,
        popup the winner dialog box."""

        if win_cond:
            self.tally.tally_game(self.game.turn, win_cond)
            self.param_tally()

            title, message = self.game.win_message(win_cond)
            message = message.split(fmt.LINE_SEP)
            message = message[0] if len(message) == 1 else message

            start_new = ui_utils.win_popup_new_game(self, title, message,
                                                    win_cond.is_round_over())
            if start_new:
                self.new_game(not win_cond.is_game_over())
            else:
                # don't let the players do anything dangerous
                # call with a frame so that only the buttons are disabled
                self.set_ui_active(False, self)


    def no_endless_sows(self):
        """Rebuild the allowable deco with or without the
        deco to prevent moves from holes that would be endless
        sows."""

        self.game.disallow_endless(self.tkvars.no_endless.get())
        self.refresh()


    def end_game(self, *, game, quitter):
        """End the round or game. Report result to user.
        Then start a new game or round.

        game     if true end the game, otherwise, try to end the
                 round, which might end up ending the game

        quitter  True if the user requested an end/quit,
                 False if they requested a concede.
                 concede uses the ender/unclaimed and quit
                 uses the quitter"""

        thing = 'game' if game else 'round'
        request = 'end' if quitter else 'concede'
        wtitle = request.title() + ' ' + thing.title()

        if self.mode != buttons.Behavior.GAMEPLAY:
            message = wtitle + ' during setup will force New Game. Continue?'
            do_it = ui_utils.ask_popup(self, wtitle, message,
                                       ui_utils.OKCANCEL)
            if do_it:
                self.new_game()
            return

        message = [self.game.end_message(thing, quitter),
                   f'Are you sure you wish to {request} the {thing}?']
        do_it = ui_utils.ask_popup(self, wtitle, message,
                                   ui_utils.OKCANCEL)
        if not do_it:
            return

        animator.set_active(False, reset_queue=True)
        win_cond = self.game.end_game(quitter=quitter, user=True, game=game)

        wtext = thing + ' Ended '
        if win_cond and win_cond.is_win():
            sturn = self.game.turn_name()
            wtext += f'\n{win_cond.name} by {sturn}'
        elif win_cond:
            wtext += ' ' + win_cond.name
        game_log.turn(self.game.mcount, wtext, self.game)

        self.refresh()
        self._win_message_popup(win_cond)


    def _log_ai_desc(self, last_turn):
        """Add the ai description to the game log (Mancala doesn't
        know if the ai is playing)."""

        if (last_turn
                and self.tkvars.ai_active.get()
                and not self.tkvars.ai_filter.get()):
            game_log.add(self.player.get_move_desc(), game_log.MOVE)


    def move(self, move):
        """Tell game to move, refresh the UI, and
        handle any win conditions."""

        self.saved_move = move
        last_turn = self.game.turn

        self.wcond = self.game.move(move)
        self.history.record(self.game.state)
        self._log_ai_desc(last_turn)

        if animator.active():
            if (self.game.mdata
                    and self.game.mdata.ended == gi.WinCond.ENDLESS):
                animator.clear_queue()

            else:
                animator.queue_callback(self.move_epilog)
                self.refresh(ani_ok=True)
                return

        self.move_epilog()


    def move_epilog(self):
        """The part of the move operation to do after the
        animation sequence completes."""

        self.refresh()

        if self.wcond and self.wcond.is_ended():
            self._win_message_popup(self.wcond)
            return

        if (not (self.tkvars.ai_active.get() and self.game.turn)
                and self.info.mustpass and self.game.test_pass()):

            player = gi.PLAYER_NAMES[not self.game.turn]
            message = f'{player} has no moves and must pass.'
            quit_round = bool(self.game.info.rounds)
            ui_utils.PassPopup(self, 'Must Pass', message, quit_round)
            self.refresh()     # test_pass updates game state

        self.schedule_ai()


    def schedule_ai(self):
        """Do AI move or schedule the AI turn (only in GAMEPLAY mode,
        and if the AI is enabled and it's the AI's turn)."""

        self.refresh()

        if (self.mode == buttons.Behavior.GAMEPLAY
                and self.tkvars.ai_active.get()
                and self.game.turn):

            self._cancel_pending_afters()
            sel_delay = self.tkvars.ai_delay.get()

            self.master.config(cursor=ui_utils.AI_BUSY)
            self.after(AI_DELAY[sel_delay], self._ai_move)


    def _ai_move(self):
        """If it's the AI's turn, do a move. AI is top player."""

        if (self.mode == buttons.Behavior.GAMEPLAY
                and self.tkvars.ai_active.get()
                and self.game.turn):

            self.master.config(cursor=ui_utils.AI_BUSY)

            if not self.tkvars.log_ai.get():
                game_log.set_ai_mode()

            with animator.animate_off(), self.history.off():
                self.saved_move = self.player.pick_move()

            game_log.clear_ai_mode()

            self.move(self.saved_move)

            if animator.active():
                animator.queue_callback(self._ai_move_epilog)
                self.refresh(ani_ok=True)
            else:
                self._ai_move_epilog()

        else:
            self.master.config(cursor=ui_utils.NORMAL)


    def _ai_move_epilog(self):
        """The part of the move operation to do after the
        animation sequence completes."""

        self.refresh()  # UI isn't active after AI PASS

        if (self.game.info.sow_direct == gi.Direct.PLAYALTDIR
            and self.game.mcount == 2):

            message = 'Player direction is ' \
                + self.saved_move[-1].opp_dir().name
            ui_utils.showinfo(self, 'Player Direction', message)

        if self.wcond == gi.WinCond.REPEAT_TURN:
            self._ask_stop_repeating()
        else:
            self.master.config(cursor=ui_utils.NORMAL)


    def _ask_stop_repeating(self):
        """Catch an ai repeat turning for too long."""

        if (self.game.rturn_cnt >= RTURN_QUERY
                and not self.game.rturn_cnt % RTURN_QFREQ):

            self._cancel_pending_afters()

            thing = ROUND if self.game.info.rounds else 'game'
            message = [f"""The AI has played {self.game.rturn_cnt}
                           repeated turns. Would you like to end
                           the {thing}?""",
                       f"""You will be asked again in {RTURN_QFREQ}
                           turns."""]
            self._cancel_pending_afters()
            do_it = ui_utils.ask_popup(self, 'AI Repeating Turns',
                                       message, ui_utils.YESNO)
            if do_it:
                self.end_game(game=self.game.info.rounds, quitter=True)
                self.master.config(cursor=ui_utils.NORMAL)

            else:
                self.schedule_ai()


class InhibitIndicator(tk.Frame):
    """An indictor for the state of the inhibitor.
    Use needed to see if this widget should be created."""

    def __init__(self, parent, turn, inhibit):

        super().__init__(parent)
        self.inhibit = inhibit
        self.turn = turn

        self.capts = self.child = None
        col = ui_utils.Counter()

        if isinstance(inhibit, (inhibitor.InhibitorCaptN,
                                inhibitor.InhibitorBoth)):
            self.capts = tk.Label(self, text='Captures',
                                  anchor='center')
            self.capts.grid(row=0, column=col.count, padx=2, pady=2)

        if isinstance(inhibit, (inhibitor.InhibitorChildrenOnly,
                                inhibitor.InhibitorBoth)):
            self.child = tk.Label(self, text='Children',
                                  anchor='center')
            self.child.grid(row=0, column=col.count, padx=2, pady=2)

        self.grid(row=1, column=0)

        self.icolor = man_config.CONFIG['inhibit_color']
        self.ncolor = man_config.CONFIG['no_inhi_color']


    @classmethod
    def needed(cls, inhibit):
        """Return True if the inhibitor indicators are useful."""

        return not isinstance(inhibit, inhibitor.InhibitorNone)


    def hide(self):
        """Hide the frame."""
        self.grid_remove()


    def show(self):
        """Show the frame"""
        self.grid()


    def update(self):
        """Update the indicator backgrounds to show the state
        of the indicators."""

        if self.capts:
            if self.inhibit.stop_me_capt(self.turn):
                self.capts['background'] = self.icolor
            else:
                self.capts['background'] = self.ncolor

        if self.child:
            if self.inhibit.stop_me_child(self.turn):
                self.child['background'] = self.icolor
            else:
                self.child['background'] = self.ncolor
