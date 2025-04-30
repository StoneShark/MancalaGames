# -*- coding: utf-8 -*-
"""Create the UI for a mancala game_constants and game_info
define how the game is created and played.
The values of those two variables must not be changed during
game play.

Created on Thu Mar  2 14:38:17 2023
@author: Ann"""
# pylint: disable=too-many-lines

# %% imports

import textwrap
import traceback
import tkinter as tk
import webbrowser

import ai_player
import animator
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
import ui_utils

from game_logger import game_log


# %%   constants

AI_DELAY = [5, 1000, 4000]

NO_TALLY_OP = 0
VIS_TALLY_OP = 1
RET_TALLY_OP = 2


# %%

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

        ani_active = man_config.CONFIG.get_bool('ani_active')
        self.ani_active = tk.BooleanVar(man_ui.master, ani_active)



class GameSetup:
    """Manage a game setup.
    Support entering game setup mode and keep the setup
    so that we can return to it."""

    def __init__(self, game_ui):

        self.game_ui = game_ui
        self.state = None


    def setup_game(self):
        """Attempt to enter setup mode."""

        if self.game_ui.set_game_mode(buttons.Behavior.SETUP):
            animator.set_active(False, clear_queue=True)


    def save_setup(self):
        """Save the game setup."""

        self.state = self.game_ui.game.state


    def reset_setup(self):
        """Reset to a previous board setup."""

        if self.state:
            self.game_ui.game.state = self.state
            self.game_ui.refresh()
            self.game_ui.start_it()
            return

        ui_utils.showerror(self.game_ui,
                           'Board Setup',
                           'There has been no previous board setup.')


# %%  mancala ui

class MancalaUI(tk.Frame):
    """A manacala UI."""

    def __init__(self, game, player_dict, *, player=None, root_ui=None):
        """Create the UI for a mancala game.

        game: class built on GameInterface - provide the mechanics of
        the game w/o any UI

        player_dict: the player element from game config file;
        a dictionary of parameters to configure the ai player

        player (optional): a prebuilt ai player.
        Building the player checks the rules and MancalaGames
        pre-tests the configuration; building the player
        twice generated duplicated errors.

        root_ui (optional): if this is started as part of another
        application provide the tk root."""

        if not isinstance(game, gi.GameInterface):
            raise TypeError('Missing mancala_ui.GameInterface in game.')

        self.game = game
        self.info = self.game.info
        self.mode = buttons.Behavior.GAMEPLAY
        self.player = player if player else \
                          ai_player.AiPlayer(self.game, player_dict)
        self.setup = GameSetup(self)
        self.movers = 0
        self.wcond = None   #  used between the movers and epilogs
        self.saved_move = None

        game_log.new()
        game_log.turn(0, 'Start Game', game)

        if root_ui:
            self.master = tk.Toplevel(root_ui)
        else:
            self.master = tk.Tk()
            ui_utils.setup_styles(self.master)
        man_config.read_ini_file(self.master, self.info.name)

        self.master.title(self.info.name)
        self.master.option_add('*tearOff', False)

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

        animator.make_animator(self)
        self._reset_ani_state()
        self._reset_ani_delay()

        self._new_game()
        self.refresh()
        self.schedule_ai()


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
        # pylint: disable=too-many-statements

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        gamemenu = tk.Menu(menubar)
        gamemenu.add_command(label='New', command=self._new_game)
        gamemenu.add_separator()
        gamemenu.add_command(label='Swap Sides', command=self._pie_rule)
        gamemenu.add_separator()
        gamemenu.add_command(label='End Round', command=self.end_round)
        gamemenu.add_command(label='End Game', command=self.end_game)
        gamemenu.add_separator()
        gamemenu.add_command(label='Setup Game',
                             command=self.setup.setup_game)
        gamemenu.add_command(label='Reset to Setup',
                             command=self.setup.reset_setup)
        menubar.add_cascade(label='Game', menu=gamemenu)

        aimenu = tk.Menu(menubar)
        aimenu.add_checkbutton(label='AI Player',
                               variable=self.vars.ai_active,
                               onvalue=True, offvalue=False,
                               command=self.schedule_ai)

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
        logmenu.add_command(label='Save Log', command=self.save_file)
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
                                 command=self.refresh)
        showmenu.add_checkbutton(label='Facing Players',
                                 variable=self.vars.facing_players,
                                 onvalue=True, offvalue=False,
                                 command=self.toggle_facing)
        showmenu.add_checkbutton(label='Ownership Arrows',
                                 variable=self.vars.owner_arrows,
                                 onvalue=True, offvalue=False,
                                 command=self.refresh)

        if animator.ENABLED:
            showmenu.add_separator()
            showmenu.add_checkbutton(label='Animation Active',
                                     variable=self.vars.ani_active,
                                     onvalue=True, offvalue=False,
                                     command=self._reset_ani_state,
                                     accelerator='Ctrl-a')
            showmenu.add_command(label='Anim Speed Reset',
                                 command=self._reset_ani_delay,
                                 accelerator='=')
            showmenu.add_command(label='Anim Speed Faster',
                                 command=self._inc_ani_speed,
                                 accelerator='>')
            showmenu.add_command(label='Anim Speed Slower',
                                 command=self._dec_ani_speed,
                                 accelerator='<')

            self.master.bind("<Control-a>", self._toggle_ani_active)
            self.master.bind("<Key-equal>", self._reset_ani_delay)
            self.master.bind("<Key-greater>", self._inc_ani_speed)
            self.master.bind("<Key-less>", self._dec_ani_speed)

        menubar.add_cascade(label='Display', menu=showmenu)

        helpmenu = tk.Menu(menubar)
        helpmenu.add_command(label='Help...', command=self._help)
        helpmenu.add_command(label='About...', command=self._about)
        menubar.add_cascade(label='Help', menu=helpmenu)

        if man_config.CONFIG.get_bool('debug_menu'):

            debugmenu = tk.Menu(menubar)
            debugmenu.add_command(label='Print Params',
                                  command=lambda: print(self.game.params_str()))
            debugmenu.add_command(label='Print Consts',
                                  command=lambda: print(self.game.cts))
            debugmenu.add_command(label='Print Decos',
                                  command=lambda: print(self.game.deco))
            debugmenu.add_command(label='Print Inhibitor',
                                  command=lambda: print(self.game.inhibitor))
            debugmenu.add_command(label='Print mdata',
                                  command=lambda: print(self.game.mdata))
            debugmenu.add_separator()
            debugmenu.add_command(label='Print AI Player',
                                  command=lambda: print(self.player))
            debugmenu.add_separator()
            debugmenu.add_command(label='Swap Sides',
                                  command=lambda: self._pie_rule(force=True))
            debugmenu.add_command(label='Toggle Anim Print',
                                  command=lambda: setattr(animator,
                                                          'print_steps',
                                                          not animator.print_steps))
            menubar.add_cascade(label='Debug', menu=debugmenu)


    def ui_loop(self):
        """Call the mainloop UI - everything happens because of user input.
        This does not return until the window is killed."""

        self.master.mainloop()


    def _cancel_pending_afters(self):
        """Cancel any pending after methods."""

        afters = self.tk.eval('after info')
        # print(f"cancel pending afters: {afters or 'None'}")
        for after_id in afters.split():
            self.after_cancel(after_id)


    def destroy(self):
        """window was closed."""

        self._cancel_pending_afters()
        animator.reset()


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
        self.refresh()


    @staticmethod
    def _reset_ani_delay(_=None):
        """Set config'ed or nominal animator speed."""

        if animator.animator:
            delay = man_config.CONFIG.get_int('ani_delay', 350)
            animator.set_delay(delay)

            print("Ani Delay=", animator.animator.delay)


    @staticmethod
    def _inc_ani_speed(_=None):
        """Increase animation speed by reducing the delay between
        steps."""

        if animator.animator:
            animator.set_delay(max(50, animator.animator.delay - 50))
            print("Ani Delay=", animator.animator.delay)


    @staticmethod
    def _dec_ani_speed(_=None):
        """Decrease animation speed."""

        if animator.animator:
            animator.set_delay(animator.animator.delay + 50)
            print("Ani Delay=", animator.animator.delay)


    def _toggle_ani_active(self, _=None):
        """Toggle the animation state (active or not active).
        Used by the key board binding."""

        ani_active = not self.vars.ani_active.get()
        self.vars.ani_active.set(ani_active)
        animator.set_active(ani_active)


    def _reset_ani_state(self):
        """Reset the animation state to agree with the tk var."""

        animator.set_active(self.vars.ani_active.get())


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
             or ui_utils.QuietDialog(self, 'Help', 'Help not found.'))


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

        ui_utils.QuietDialog(self, 'About', ''.join(out_text))


    def save_file(self):
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


    def _set_ui_active(self, active, frame=None):
        """Activate or deactivate the Hole and Store Buttons,
        recursing through frames.

        Not using the tk state for Hole & Store Buttons, because
        it's overridden on every refresh."""

        if not frame:
            frame = self

        for child in frame.winfo_children():

            if isinstance(child, tk.Frame):
                self._set_ui_active(active, child)

            elif isinstance(child, (buttons.HoleButton,
                                    buttons.StoreButton)):
                child.active = active


    def show_seeds_in_stores(self):
        """Return True if the stores should be updated with a
        seed count, False otherwise."""

        return (self.stores
                and not self.info.goal in (gi.Goal.DEPRIVE,
                                           gi.Goal.CLEAR,
                                           gi.Goal.RND_WIN_COUNT_DEP,
                                           gi.Goal.RND_WIN_COUNT_CLR))


    def refresh(self, *, ani_ok=False):
        """Make UI match mancala game."""

        if ani_ok and animator.active():
            self._set_ui_active(active=False)
            animator.animator.do_animation()
            return

        self._set_ui_active(True)
        turn = self.game.get_turn()
        allows = self.game.get_allowable_holes()
        turn_row = int(not turn)
        ai_turn = self.vars.ai_active.get() and turn
        for row in range(2):

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


    def start_it(self):
        """Do the last steps in starting a new game:
        log the start and check for ai's turn."""
        game_log.new()
        game_log.turn(self.game.mcount, 'Start Game', self.game)
        self.movers = 0
        self._reset_ani_state()
        self.schedule_ai()


    def _not_playable_new_round(self):
        """The new round is not playable by the starter."""

        self.refresh()
        ui_utils.showerror(
            self,
            "New Round Not Playable",
           """The new round resulted in a unplayable game.
           New game started.""")


    def _new_game(self, win_cond=None, new_round_ok=False):
        """Start a new game and refresh the board."""
        # pylint: disable=too-complex

        self._cancel_pending_afters()
        self.master.config(cursor=ui_utils.NORMAL)
        animator.set_active(False, clear_queue=True)

        new_game = self.game.new_game(win_cond=win_cond,
                                      new_round_ok=new_round_ok)
        self.player.clear_history()
        self.set_game_mode(buttons.Behavior.GAMEPLAY, force=True)

        self.refresh()
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

        assert sum(self.game.store) + sum(self.game.board) == \
            self.game.cts.total_seeds, \
            'Seed count error on switching UI mode.'

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
            self._toggle_tally(vis_op=RET_TALLY_OP)
        else:
            self._toggle_tally(vis_op=VIS_TALLY_OP)
        return True


    def set_gameplay_mode(self):
        """The behaviors file cannot import btn_behaviors
        (circular deps), but the behavior objects have a
        pointer to the game_ui object so we'll mode
        for them here"""

        if self.set_game_mode(buttons.Behavior.GAMEPLAY):
            self._reset_ani_state()
            return True
        return False


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

            title, message = self.game.win_message(win_cond)
            message = message.split('\n')
            message = message[0] if len(message) == 1 else message

            ui_utils.WinPopup(self, title, message)


    def _pie_rule(self, force=False):
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
        if not force and self.movers != 1:
            ui_utils.showerror(self, "Swap Not Allowed",
                               """Swapping sides is only allowed by a
                               human player after the first move.
                               It counts as a move.""")
            return

        self.movers += 1
        game.mcount += 1
        game.turn = not game.turn
        with animator.animate_off():
            game.swap_sides()

        self.player.clear_history()

        self.refresh()
        game_log.turn(game.mcount, "Swap Sides (pie rule)", game)

        self.schedule_ai()


    def end_round(self):
        """End the round. Report result to user."""

        if not self.game.info.rounds or self.mode != buttons.Behavior.GAMEPLAY:
            self.end_game()
            return

        message = 'Are you sure you wish to end the round?'
        do_it = ui_utils.ask_popup(self,'End Round', message,
                                   ui_utils.OKCANCEL)
        if not do_it:
            return

        animator.set_active(False, clear_queue=True)
        win_cond = self.game.end_round()

        wtext = 'Round Ended '
        if win_cond in (gi.WinCond.WIN, gi.WinCond.ROUND_WIN):
            sturn = self.game.turn_name()
            wtext += f'\n{win_cond.name} by {sturn}'
        elif win_cond:
            wtext += ' ' + win_cond.name
        game_log.turn(self.game.mcount, wtext, self.game)

        self.refresh()
        self._win_message_popup(win_cond)
        self._new_game(win_cond=win_cond, new_round_ok=True)


    def end_game(self):
        """End the game. Report result to user."""

        if self.mode != buttons.Behavior.GAMEPLAY:
            message = 'End game during setup will force New Game. Continue?'
            do_it = ui_utils.ask_popup(self, 'End Game', message,
                                       ui_utils.OKCANCEL)
            if do_it:
                self._new_game()
            return

        message = 'Are you sure you wish to end the game?'
        do_it = ui_utils.ask_popup(self, 'End Game', message,
                                   ui_utils.OKCANCEL)
        if not do_it:
            return

        animator.set_active(False, clear_queue=True)
        win_cond = self.game.end_game()

        wtext = 'Game Ended '
        if win_cond in (gi.WinCond.WIN, gi.WinCond.ROUND_WIN):
            sturn = self.game.turn_name()
            wtext += f'\n{win_cond.name} by {sturn}'
        elif win_cond:
            wtext += ' ' + win_cond.name
        game_log.turn(self.game.mcount, wtext, self.game)

        self.refresh()
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

        self.saved_move = move
        last_turn = self.game.get_turn()
        if animator.active() and move != gi.PASS_TOKEN:
            animator.animator.flash(last_turn, move=move)

        self.wcond = self.game.move(move)

        if last_turn != self.game.get_turn():
            self.movers += 1

        self._log_turn(last_turn)

        if animator.active():
            animator.animator.queue_callback(self.move_epilog)
            self.refresh(ani_ok=True)
        else:
            self.refresh()
            self.move_epilog()


    def move_epilog(self):
        """The part of the move operation to do after the
        animation sequence completes."""

        if self.wcond and self.wcond != gi.WinCond.REPEAT_TURN:
            self._win_message_popup(self.wcond)
            self._new_game(win_cond=self.wcond, new_round_ok=True)

        if (not (self.vars.ai_active.get() and self.game.get_turn())
                and self.info.mustpass and self.game.test_pass()):

            player = self.game.turn_name()
            message = f'{player} player has no moves and must pass.'
            ui_utils.PassPopup(self, 'Must Pass', message)
            self.refresh()     # test pass updates game state

        self.schedule_ai()


    def schedule_ai(self):
        """Do AI move or schedule the AI turn (only in GAMEPLAY mode,
        and if the AI is enabled and it's the AI's turn)."""

        self.refresh()

        if (self.mode == buttons.Behavior.GAMEPLAY
                and self.vars.ai_active.get()
                and self.game.get_turn()):

            self._cancel_pending_afters()
            sel_delay = self.vars.ai_delay.get()

            self.master.config(cursor=ui_utils.AI_BUSY)
            self.after(AI_DELAY[sel_delay], self._ai_move)


    def _ai_move(self):
        """If it's the AI's turn, do a move. AI is top player."""

        if (self.mode == buttons.Behavior.GAMEPLAY
                and self.vars.ai_active.get()
                and self.game.get_turn()):

            self.master.config(cursor=ui_utils.AI_BUSY)

            if not self.vars.log_ai.get():
                game_log.set_ai_mode()

            with animator.animate_off():
                self.saved_move = self.player.pick_move()

            game_log.clear_ai_mode()

            self.move(self.saved_move)

            if animator.active():
                animator.animator.queue_callback(self._ai_move_epilog)
                self.refresh(ani_ok=True)
            else:
                self._ai_move_epilog()


    def _ai_move_epilog(self):
        """The part of the move operation to do after the
        animation sequence completes."""

        if (self.game.info.sow_direct == gi.Direct.PLAYALTDIR
            and self.game.mcount == 1):

            message = 'Player direction is ' \
                + self.saved_move[-1].opp_dir().name
            ui_utils.showinfo(self, 'Player Direction', message)

        if self.wcond != gi.WinCond.REPEAT_TURN:
            self.master.config(cursor=ui_utils.NORMAL)
