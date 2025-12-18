# -*- coding: utf-8 -*-
"""Mixin classes that make up the thin venier between the
mancala_ui and the support objects grouped by functionality.

Each makes either a few commands to be put on another
menu (*CmdsMixin) or makes a full menu (MenuMixin).

These mixin are NOT independent of MancalaUI and are not intended
to be reusable with other classes. They break the functionality
of the MancalaUI into some managable pieces.

Any data declared in these routines is class scope data!
Re-init it when the menu is made.

Created on Wed Jun  4 15:45:37 2025
@author: Ann"""

import functools as ft
import tkinter as tk
import webbrowser

import ai_player
import animator
import buttons
import cfg_keys as ckey
import format_msg
import game_info as gi
import man_config
import man_path
import montecarlo_ts
import ui_utils
import variants

from game_logger import game_log


# %% game

class GameCmdsMixin:
    """New, concede and end menu commands and an extra.
    All commands are in MancalaUI"""

    def game_add_menu_cmds(self, menu):
        """Add the new, conceded and end menu commands."""

        rounds = self.game.info.rounds
        menu.add_command(label='New Round',
                             command=ft.partial(self.new_game, new_round=True),
                             state=tk.NORMAL if rounds else tk.DISABLED)
        menu.add_command(label='New Game', command=self.new_game)

        menu.add_separator()

        menu.add_command(
            label='Concede Round',
            command=ft.partial(self.end_game, quitter=False, game=False),
            state=tk.NORMAL if rounds else tk.DISABLED)
        menu.add_command(
            label='Concede Game',
            command=ft.partial(self.end_game, quitter=False, game=True))
        menu.add_command(
            label='End Round (quit)',
            command=ft.partial(self.end_game, quitter=True, game=False),
            state=tk.NORMAL if rounds else tk.DISABLED)
        menu.add_command(
            label='End Game (quit)',
            command=ft.partial(self.end_game, quitter=True, game=True))

        menu.add_separator()

        enable_no_endless = self.game.info.mlaps and not self.game.info.udirect
        menu.add_checkbutton(
            label='Disallow Endless Sows',
            variable=self.tkvars.no_endless,
            onvalue=True, offvalue=False,
            command=self.no_endless_sows,
            state=tk.NORMAL if enable_no_endless else tk.DISABLED)


# %% variations

class VariCmdsMixin:
    """The vari menu commands.
    Prefix for public methods is 'vari'."""

    _varier = None

    @staticmethod
    def vari_show_error(parent, message, *_):
        """Notify user of warnings during parameter test."""

        ui_utils.showwarning(parent, 'Varations Warning', str(message))


    def vari_add_menu_cmds(self, menu):
        """Add the variant menu commands."""
        self._varier = None

        from_file = self._test_vari_avail()

        menu.add_separator()
        menu.add_command(label='Config Variant...',
                         command=self._reconfigure,
                         state=tk.NORMAL if from_file else tk.DISABLED )
        menu.add_command(label='Variant Settings...',
                         command=self._var_settings,
                         state=tk.NORMAL if from_file else tk.DISABLED )
        menu.add_command(label='Revert Variant...',
                         command=self._revert_variant,
                         state=tk.NORMAL if from_file else tk.DISABLED )


    def _test_vari_avail(self):
        """Determine if the animation commands should be available:
        the game needs to have been loaded from a file and the file
        must configure variations."""

        from_file = hasattr(self.game, ckey.FILENAME)

        if from_file:
            with open(self.game.filename, 'r', encoding='utf-8') as file:
                text = ' '.join(file.readlines())

            variations = ckey.VARI_PARAMS in text or ckey.VARIANTS in text
            from_file &= variations

        return from_file


    def _reconfigure(self):
        """Do popup to ask for reconfiguration and then
        posibly rebuild self.

        Do not call this if the game was not loaded from a file.
        The filename attribute will not exist, it's added silently
        by the game loader in man_config (hence the getattr below)."""

        if not self._varier:
            self._varier = variants.GameVariations(
                                self, getattr(self.game, ckey.FILENAME))
            if self._varier.failed:
                self._varier = None
                return

        with animator.animate_off():
            game_objs = self._varier.reconfigure()
            if not game_objs:
                return

        self._varier = None
        self.rebuild(*game_objs)


    def _revert_variant(self):
        """Revert to the game configuration."""

        title = 'Revert Variant'
        message = 'Are you sure you wish to revert to the main variant?'
        do_it = ui_utils.ask_popup(self, title, message, ui_utils.OKCANCEL)
        if not do_it:
            return

        if not self._varier:
            self._varier = variants.GameVariations(
                                self, getattr(self.game, ckey.FILENAME))
            if self._varier.failed:
                self._varier = None
                return

        game_objs = self._varier.rebuild_variant()
        self._varier = None
        self.rebuild(*game_objs)


    def _var_settings(self):
        """Popup the variation settings."""

        if not self._varier:
            self._varier = variants.GameVariations(
                                self, getattr(self.game, ckey.FILENAME))
            if self._varier.failed:
                self._varier = None
                return

        self._varier.settings()


# %%  setup

class SetupCmdsMixin:
    """The setup menu commands.
    Prefix for public methods is 'setup'."""

    _setup_state = None


    def setup_add_menu_cmds(self, menubar):
        """Add the setup commands."""

        self._setup_state = None

        menubar.add_separator()
        menubar.add_command(label='Setup Game', command=self.setup_game)
        menubar.add_command(label='Reset to Setup', command=self.setup_reset)


    def setup_game(self):
        """Attempt to enter setup mode."""

        if self.set_game_mode(buttons.Behavior.SETUP):
            animator.set_active(False, reset_queue=True)


    def setup_save(self):
        """Save the game setup."""

        self._setup_state = self.game.state


    def setup_reset(self):
        """Reset to a previous board setup."""

        if self._setup_state:
            self.game.state = self._setup_state
            self.refresh()
            self.start_it()
            return

        ui_utils.showerror(self, 'Board Setup',
                           """There has been no previous board setup.
                           Use Setup Game to setup the board.""")


# %%   Move mixin

class MoveMenuMixin:
    """The move menu and commands.
    Prefix for public methods is 'move'."""

    def move_add_menu(self, menubar):
        """Add the move menu."""

        movemenu = tk.Menu(menubar, name='move')
        movemenu.add_command(label='Undo Move', command=self.move_undo,
                             accelerator='Ctrl-z')
        movemenu.add_command(label='Redo Move', command=self.move_redo,
                             accelerator='Ctrl-Shift-z')
        movemenu.add_separator()
        movemenu.add_command(label='Swap Sides', command=self.move_swap_sides)
        menubar.add_cascade(label='Move', menu=movemenu)


    def move_undo(self, _=None):
        """Return to the previous state."""

        state = self.history.undo()
        if state:
            self.game.state = state
            self.refresh()
            self.param_tally()
            game_log.add('Move undone:\n' + str(state), game_log.IMPORT)
        else:
            self.bell()


    def move_redo(self, _=None):
        """Return to an undone state state.
        Disable the UI when the redone move ended the game."""

        state = self.history.redo()
        if state:
            self.game.state = state
            self.refresh()
            self.param_tally()
            game_log.add('Move redone:\n' + str(state), game_log.IMPORT)

            if (self.game.mdata
                    and self.game.mdata.win_cond
                    and self.game.mdata.win_cond.is_ended()):
                self.set_ui_active(False, self)
        else:
            self.bell()


    def move_swap_sides(self, force=False):
        """Allow a player to swap sides after the first
        move, aka 'Pie Rule'.

        Force is used in the debugging menu to always allow a
        swap.

        swap_ok is init'ed to False for second and subsequent
        rounds of TERRITORY and rounds/blocks games.

        When MOVE_RANDOM, test movers against 2 because the
        first move was done automatically.

        This is often used to neutralize the unfair advantage
        that starter of some games has.  Not all mancala games
        have an advantage for the starter, but allow it for all.

        The AI history is cleared which currently only applies to
        MCTS. This does seem extreme but the AI turn and node tree
        have already been started and are dependent on the player
        they are playing; correcting them seems error prone."""

        game = self.game
        allowed = self.swap_ok
        if game.info.start_pattern in (gi.StartPattern.RANDOM,
                                       gi.StartPattern.RANDOM_ZEROS,
                                       gi.StartPattern.MOVE_RANDOM):
            allowed &= game.movers < 2
        else:
            allowed &= game.movers == 1

        if not force and not allowed:
            ui_utils.showerror(self, "Swap Not Allowed",
                ["Swapping sides is only allowed:",
                 """1. Once per round (see rule 3).""",
                 """2. Before or after the first move for games
                 using RANDOM or RANDOM_ZEROS start patterns.""",
                 """3. After the first move of the opening round
                 of TERRITORY and rounds/blocks games.
                 It is prohibited for subsequent round starts.""",
                 "4. After the first move for other games.",
                 """A swap counts as a move."""])
            return

        self.swap_ok = False
        with animator.animate_off():
            game.swap_sides(is_turn=True)
        self.history.record(self.game.state)

        self.player.clear_history()
        self.refresh()
        game_log.turn(game.mcount, "Swap Sides (pie rule)", game)
        self.schedule_ai()


# %% ai control

class AiCtrlMenuMixin:
    """The ai player menu and commands.
    Prefix for public methods is 'ai'."""

    _algo = None

    def ai_add_menu(self, menubar):
        """Add the Player menu.

        Include the algorithm change if we can get the player dictionary
        from a file and if there is more than one possible algo."""

        aimenu = tk.Menu(menubar, name='player')
        aimenu.add_checkbutton(label='AI Player Active',
                               variable=self.tkvars.ai_active,
                               onvalue=True, offvalue=False,
                               command=self.schedule_ai)

        nega = not ai_player.negamax_no_repeat_turn(self.game)
        mcts = not ai_player.mcts_no_hidden_state(self.game)
        from_file = hasattr(self.game, ckey.FILENAME)
        algo_change =  from_file and (nega or mcts)

        self._algo = tk.StringVar(self, self._get_algo_name())

        aimenu.add_separator()
        algmenu = tk.Menu(menubar)
        algmenu.add_radiobutton(label="Minimaxer", command=self._change_algo,
                                variable=self._algo, value='minimaxer')

        algmenu.add_radiobutton(label="Negamaxer", command=self._change_algo,
                                variable=self._algo, value='negamaxer',
                                state=tk.NORMAL if nega else tk.DISABLED)

        algmenu.add_radiobutton(label="Monte Carlo Tree Search",
                                command=self._change_algo,
                                variable=self._algo, value='montecarlo_ts',
                                state=tk.NORMAL if mcts else tk.DISABLED)

        aimenu.add_cascade(label='Algorithm', menu=algmenu,
                           state=tk.NORMAL if algo_change else tk.DISABLED)

        aimenu.add_separator()
        aimenu.add_radiobutton(label='No AI Delay',
                               variable=self.tkvars.ai_delay, value=0)
        aimenu.add_radiobutton(label='Short AI Delay',
                               variable=self.tkvars.ai_delay, value=1)
        aimenu.add_radiobutton(label='Long AI Delay',
                               variable=self.tkvars.ai_delay, value=2)

        aimenu.add_separator()
        aimenu.add_radiobutton(label='Easy',
                               value=0, variable=self.tkvars.difficulty,
                               command=self.ai_set_difficulty)
        aimenu.add_radiobutton(label='Normal',
                               value=1, variable=self.tkvars.difficulty,
                               command=self.ai_set_difficulty)
        aimenu.add_radiobutton(label='Hard',
                               value=2, variable=self.tkvars.difficulty,
                               command=self.ai_set_difficulty)
        aimenu.add_radiobutton(label='Expert',
                               value=3, variable=self.tkvars.difficulty,
                               command=self.ai_set_difficulty)
        menubar.add_cascade(label='Player', menu=aimenu)


    def ai_set_difficulty(self):
        """Set the difficulty for the ai player."""

        diff = self.tkvars.difficulty.get()
        self.player.difficulty = diff
        game_log.add(f'Changing difficulty {diff}', game_log.INFO)


    def _get_algo_name(self):
        """Return the algorithm name"""

        for name, aclass in ai_player.ALGORITHM_DICT.items():
            if isinstance(self.player.algo, aclass):
                return name

        assert False, 'Unknown AI algorithm'


    def _change_algo(self):
        """Change the player algorithm.

        If the game was created via variants, the algo might no longer
        be valid; rebuild the player and catch any errors.

        Start a new game to keep things tidy."""

        title = 'Change Player Algorithm'
        message = """Changing the AI player algorithm will start a new game.
                  Do you wish to proceed?"""
        do_it = ui_utils.ask_popup(self, title, message, ui_utils.OKCANCEL)
        if not do_it:
            self._algo.set(self._get_algo_name())
            return

        game_config = man_config.read_game(self.game.filename)
        player_dict = game_config[ckey.PLAYER]
        player_dict[ckey.ALGORITHM] = self._algo.get()

        with ui_utils.ReportError(self) as build_context:
            self.player = ai_player.AiPlayer(self.game, player_dict)

        if build_context.error:
            self._algo.set(self._get_algo_name())
            return

        self.new_game()


# %% show / display menu

NO_TALLY_OP = 0
VIS_TALLY_OP = 1
RET_TALLY_OP = 2


class ShowMenuMixin:
    """The display menu and commands.
    Prefix for public methods is 'show'."""

    def show_add_menu(self, menubar):
        """Add the show menu."""

        showmenu = tk.Menu(menubar, name='display')
        showmenu.add_checkbutton(label='Show Tally Pane',
                                 variable=self.tkvars.show_tally,
                                 onvalue=True, offvalue=False,
                                 command=self.show_toggle_tally)
        active = tk.NORMAL if self.inhibits else tk.DISABLED
        showmenu.add_checkbutton(label='Show Inhibitor Status',
                                 variable=self.tkvars.show_inhibit,
                                 onvalue=True, offvalue=False,
                                 command=self._toggle_inhibitor,
                                 state=active)
        showmenu.add_command(label='Min Size Window',
                             command=self.show_min_size)
        showmenu.add_separator()
        showmenu.add_checkbutton(label='Touch Screen',
                                 variable=self.tkvars.touch_screen,
                                 onvalue=True, offvalue=False,
                                 command=self.refresh)
        active = tk.DISABLED if self.game.info.no_sides else tk.NORMAL
        showmenu.add_checkbutton(label='Facing Players',
                                 variable=self.tkvars.facing_players,
                                 onvalue=True, offvalue=False,
                                 command=self.show_toggle_facing,
                                 state=active)
        showmenu.add_checkbutton(label='Ownership Arrows',
                                 variable=self.tkvars.owner_arrows,
                                 onvalue=True, offvalue=False,
                                 command=self._toggle_ownership)

        # complicated decision so that the child markers are not
        # misleading for TERRITORY games
        active = tk.DISABLED
        if (self.game.info.child_type
                and (self.game.info.goal != gi.Goal.TERRITORY
                     or (self.game.info.goal == gi.Goal.TERRITORY
                         and self.game.info.child_rule
                                     in (gi.ChildRule.NONE,
                                         gi.ChildRule.OPP_SIDE_ONLY,
                                         gi.ChildRule.OWN_SIDE_ONLY)))):
            active = tk.NORMAL
        showmenu.add_checkbutton(label='Static Child Locations',
                                 variable=self.tkvars.child_locs,
                                 onvalue=True, offvalue=False,
                                 command=self._toggle_child_locs,
                                 state=active)

        menubar.add_cascade(label='Display', menu=showmenu)


    def show_update_after_const(self):
        """Update the items that must be visible when created with
        the appropriate visibility for the game and configuration
        file."""

        tally = man_config.CONFIG.get_bool('show_tally')
        self.tkvars.show_tally.set(tally)
        if not tally:
            self.tally_frame.forget()

        show_inhi = bool(self.inhibits
                         and man_config.CONFIG.get_bool('show_inhibit'))
        self.tkvars.show_inhibit.set(show_inhi)
        self._toggle_inhibitor()
        if self.game.info.child_type:
            self._toggle_child_locs()


    def show_min_size(self):
        """Make the windows it's minimum size."""

        self.master.minsize(0, 0)


    def show_toggle_tally(self, vis_op=NO_TALLY_OP):
        """Adjust tally frame visibility."""

        if vis_op == VIS_TALLY_OP:
            # force tally to be visible (status pane is needed)
            self.tally_frame.pack(side=tk.TOP, expand=True, fill=tk.X)
            self.tkvars.tally_was_off = not self.tkvars.show_tally.get()
            self.tkvars.show_tally.set(True)

        elif vis_op == RET_TALLY_OP and self.tkvars.tally_was_off:
            # return tally to the state it was before VIS_TALLY_OP called
            self.tally_frame.forget()
            self.tkvars.show_tally.set(False)
            self.tkvars.tally_was_off = False
            self.show_min_size()

        elif self.mode == buttons.Behavior.GAMEPLAY:
            # only allow user toggle when in GAMEPLAY state
            if self.tkvars.show_tally.get():
                self.tally_frame.pack(side=tk.TOP, expand=True, fill=tk.X)
            else:
                self.tally_frame.forget()
                self.show_min_size()

        else:
            self.bell()
            self.tkvars.show_tally.set(True)



    def show_toggle_facing(self):
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


    def _toggle_ownership(self):
        """Popup a message, if we guess that ownership arrows
        don't mean anything."""

        if (self.tkvars.owner_arrows.get()
                and self.game.info.no_sides
                and not self.game.info.goal.eliminate()):

            msg = f"""For {self.info.name},
                   ownership arrows might not be meaningful
                   and could be misleading; check game rules."""
            ui_utils.QuietDialog(self, 'Ownership Arrows', msg)

        self.refresh()


    def _toggle_inhibitor(self):
        """Show or hide the inhibitor frame."""

        if self.inhibits:
            if self.tkvars.show_inhibit.get():
                self.inhibits[0].show()
                self.inhibits[1].show()
            else:
                self.inhibits[0].hide()
                self.inhibits[1].hide()
                self.show_min_size()


    def _toggle_child_locs(self):
        """Show or hide the statically allowable child locations."""

        state = self.tkvars.child_locs.get()

        for button_row in self.disp:
            for btn in button_row:
                btn.show_child_locs(state)


# %%  animator

ANI_STEP = 25


class AniMenuMixin:
    """The animator menu and commands.
    Prefix for public methods is 'ani'."""

    def ani_add_menu(self, menubar):
        """Add the menu commands for the animator."""

        if animator.ENABLED:

            animenu = tk.Menu(menubar, name='animator')
            animenu.add_checkbutton(label='Animation Active',
                                     variable=self.tkvars.ani_active,
                                     onvalue=True, offvalue=False,
                                     command=self.ani_reset_state,
                                     accelerator='Ctrl-a')
            animenu.add_separator()
            animenu.add_command(label='Anim Speed Reset',
                                 command=self.ani_reset_delay,
                                 accelerator='=')
            animenu.add_command(label='Anim Speed Fastest',
                                 command=self._ani_speed_fastest,
                                 accelerator='}')
            animenu.add_command(label='Anim Speed Faster',
                                 command=self._ani_inc_speed,
                                 accelerator='>')
            animenu.add_command(label='Anim Speed Slower',
                                 command=self._ani_dec_speed,
                                 accelerator='<')

            # these are always active when the animator is ENABLED
            self.master.bind("<Control-a>", self._toggle_ani_active)
            self.master.bind("<Key-equal>", self.ani_reset_delay)
            self.master.bind("<Key-braceright>", self._ani_speed_fastest)
            self.master.bind("<Key-greater>", self._ani_inc_speed)
            self.master.bind("<Key-less>", self._ani_dec_speed)
            menubar.add_cascade(label='Animator', menu=animenu)


    @staticmethod
    def ani_reset_delay(_=None):
        """Set config'ed or nominal animator speed."""

        if animator.active():
            delay = man_config.CONFIG.get_int('ani_delay', 350)
            animator.set_delay(delay)


    @staticmethod
    def _ani_speed_fastest(_=None):
        """set animation speed to it fastest"""

        if animator.active():
            animator.set_delay(ANI_STEP)


    @staticmethod
    def _ani_inc_speed(_=None):
        """Increase animation speed by reducing the delay between
        steps."""

        if animator.active():
            animator.set_delay(max(ANI_STEP,
                                   animator.get_delay() - ANI_STEP))


    @staticmethod
    def _ani_dec_speed(_=None):
        """Decrease animation speed."""

        if animator.active():
            animator.set_delay(animator.get_delay() + ANI_STEP)


    def _toggle_ani_active(self, _=None):
        """Toggle the animation state (active or not active).
        Used by the key board binding."""

        ani_active = not self.tkvars.ani_active.get()
        self.tkvars.ani_active.set(ani_active)
        animator.set_active(ani_active)


    def ani_reset_state(self):
        """Reset the animation state to agree with the tk var."""

        animator.set_active(self.tkvars.ani_active.get())


# %%  game log

class GLogMenuMixin:
    """The game log menu and commands.
    Prefix for public methods is 'glog'."""

    def glog_add_menu(self, menubar):
        """Add the game log control menu."""

        logmenu = tk.Menu(menubar, name='log')
        logmenu.add_checkbutton(
            label='Live Log',
            onvalue=True, offvalue=False,
            variable=self.tkvars.live_log,
            command=lambda: setattr(game_log, 'live',
                                    self.tkvars.live_log.get()))
        logmenu.add_command(label='Show Prev', command=game_log.prev)
        logmenu.add_command(label='Show Log', command=game_log.dump)
        logmenu.add_command(label='Save Log ...', command=self.glog_save_log)
        logmenu.add_separator()
        logmenu.add_radiobutton(
            label='Moves',
            value=game_log.MOVE, variable=self.tkvars.log_level,
            command=self._set_log_level)
        logmenu.add_radiobutton(
            label='Important',
            value=game_log.IMPORT, variable=self.tkvars.log_level,
            command=self._set_log_level)
        logmenu.add_radiobutton(
            label='Steps',
            value=game_log.STEP, variable=self.tkvars.log_level,
            command=self._set_log_level)
        logmenu.add_radiobutton(
            label='Information',
            value=game_log.INFO, variable=self.tkvars.log_level,
            command=self._set_log_level)
        logmenu.add_radiobutton(
            label='Detail',
            value=game_log.DETAIL, variable=self.tkvars.log_level,
            command=self._set_log_level)
        logmenu.add_separator()
        logmenu.add_checkbutton(label='Filter AI Scores',
                                variable=self.tkvars.ai_filter,
                                onvalue=True, offvalue=False,)
        logmenu.add_checkbutton(label='Log AI Analysis',
                                variable=self.tkvars.log_ai,
                                onvalue=True, offvalue=False)
        menubar.add_cascade(label='Log', menu=logmenu)


    def _set_log_level(self):
        """Set the game log level"""

        game_log.level = self.tkvars.log_level.get()


    def glog_save_log(self):
        """Save the game log to the file, provide a string that
        describes the game."""
        game_log.save(self.game.params_str())


# %% debug

DEBUG = 'debug'
ALL = 'all'


class DebugMenuMixin:
    """The debug menu and commands.
    Prefix for public methods is 'dbg'."""

    def dbg_add_menu(self, menubar):
        """Add the debug menu."""

        if not man_config.CONFIG.get_bool('debug_menu'):
            return

        debugmenu = tk.Menu(menubar, name=DEBUG)
        debugmenu.add_command(label='Print Params',
                              command=lambda: print(self.game.params_str()))
        debugmenu.add_command(label='Print Consts',
                              command=lambda: print(self.game.cts))
        pmenu = tk.Menu(menubar)
        pmenu.add_command(label='Print All',
                          command=ft.partial(self._print_deco, ALL))

        pmenu.add_separator()
        for vname in sorted(vars(self.game.deco).keys()):
            name = vname.title()
            pmenu.add_command(label=f"Print {name}",
                              command=ft.partial(self._print_deco, vname))
        debugmenu.add_cascade(label='Print Decos', menu=pmenu)
        debugmenu.add_command(label='Print State',
                              command=lambda: print(self.game.state))
        debugmenu.add_command(label='Print Inhibitor',
                              command=lambda: print(self.game.inhibitor))
        debugmenu.add_command(label='Print Round Tally',
                              command=lambda: print(self.game.rtally))
        debugmenu.add_command(label='Print mdata',
                              command=lambda: print(self.game.mdata))
        debugmenu.add_separator()
        debugmenu.add_command(label='Print AI Player',
                              command=lambda: print(self.player))
        debugmenu.add_command(label='Print AI Scorers',
                              command=self._print_scorers)
        debugmenu.add_command(label='Eval Moves',
                              command=self._eval_moves)
        debugmenu.add_command(label='Print History',
                              command=lambda: print(self.history))
        debugmenu.add_command(label='Force UI Active',
                              command=ft.partial(self.set_ui_active, True))

        debugmenu.add_separator()
        debugmenu.add_command(
            label='Swap Sides',
            command=lambda: self.move_swap_sides(force=True))
        debugmenu.add_command(
            label='Toggle Anim Print',
            command=lambda: setattr(animator,
                                    'PRINT_STEPS',
                                    not animator.PRINT_STEPS))
        menubar.add_cascade(label='Debug', menu=debugmenu)


    def _print_deco(self, deco):
        """Print the decoration with name."""

        if deco == ALL:
            print(self.game.deco)
        else:
            print(f'\n{deco.title()}:\n')
            print(getattr(self.game.deco, deco))


    def _print_scorers(self):
        """Print the names of the ai scorer functions."""

        for scorer in self.player.scorers:
            print(scorer.__name__)


    def _eval_moves(self):
        """Use the AI player to pick a move.

        Turn off the animator, history and game_log while evaluating.

        MCTS can only be used with one player, must be True because
        the AI would play True. Activating the AI player after a False
        eval will throw an exception."""

        if isinstance(self.player.algo, montecarlo_ts.MonteCarloTS):
            if self.game.turn is False:
                print("\nCan only eval with MCTS for North.\n")
                return

            gvals = '++'
        else:
            #  same for both minimaxer and negamaxer
            #  XXXX picked move doesn't agree with this good vals print

            gvals = '--' if self.player.is_max_player() else '++'

        pname = gi.PLAYER_NAMES[self.game.turn]
        print(f"\nEvaluating moves for {pname} ({gvals} good) ...")
        with animator.animate_off(), self.history.off(), game_log.simulate():

            move = self.player.pick_move()
            print(self.player.get_move_desc())
            print(f"Move picked {move}.\n")



# %% help

class HelpMenuMixin:
    """The help menu and commands.
    Prefix for public methods is 'help'."""

    def help_add_menu(self, menubar):
        """Add the help menu."""

        helpmenu = tk.Menu(menubar, name='name')
        helpmenu.add_command(label='Help...', command=self._help)
        helpmenu.add_command(label='About Game...', command=self._about)
        helpmenu.add_command(label='About...',
                             command=ft.partial(ui_utils.show_release, self))
        menubar.add_cascade(label='Help', menu=helpmenu)


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

        text = ''.join(format_msg.build_paras(
                                man_config.remove_tags(self.info.about)))
        ui_utils.QuietDialog(self, f'About {self.info.name}', text,
                             fixed_form=True)
