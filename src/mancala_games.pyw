# -*- coding: utf-8 -*-
"""Create a window that collects the mancala parameters
and then plays the game. Saving and loading parameter
sets to files is supported.

A few parameters can only be changed via the file (e.g.
minimaxer depths and default difficulty).

Created on Thu Mar 30 13:43:39 2023
@author: Ann"""


# %% import

import dataclasses as dc
import json
import os.path
import traceback
import warnings

import tkinter as tk
import tkinter.filedialog as tkfile

import cfg_keys as ckey
import game_constants as gc
import game_interface as gi
from game_log import game_log
import mancala
import mancala_ui
import man_config
import man_path

from game_classes import GAME_CLASSES
from game_constants import MAX_HOLES
from game_constants import MIN_HOLES
from game_constants import MAX_SEEDS
from game_interface import CrossCaptOwn
from game_interface import Direct
from game_interface import Goal
from game_interface import GrandSlam
from game_interface import RoundStarter

# %% support func

def inv_dict(adict):
    """Invert the keys and values for a reverse lookup."""

    vals = adict.values()
    assert len(vals) == len(set(vals)), 'values not unique for adict'
    return {value: key for key, value in adict.items()}


# %%  Constants

# max constants
MHOLES_RTOP = MAX_HOLES + 1
MSEEDS_RTOP = MAX_SEEDS + 1

# defaults
DEF_NAME = 'Mancala'
DEF_HOLES = 3
DEF_SEEDS = 2


# widget states
DISABLED = 'disabled'
ACTIVE = 'active'
NORMAL = 'normal'

# options for pull-down menus
SIZES = list(range(MIN_HOLES, MHOLES_RTOP))
SEEDS = list(range(1, MSEEDS_RTOP))
MIN_MOVE = list(range(1, 4))
CONVERT = [0] + list(range(2, 2*MAX_HOLES+1))
MULTS = list(range(-9, 9))
EASYVALS = [0, 1] + list(range(2, 27, 2))
REPEATVALS = list(range(0, 101, 20))
MAX_CAPT = 6

# string for enumerations
SOW_DIR = {'Clockwise': Direct.CW,
           'Counter-clockwise': Direct.CCW,
           'Split': Direct.SPLIT}
INV_SOW_DIR = inv_dict(SOW_DIR)

GRANDSLAM = {"Legal": GrandSlam.LEGAL,
             "Not Legal": GrandSlam.NOT_LEGAL,
             "Legal but no capture": GrandSlam.NO_CAPT,
             "Legal but opp takes remaining": GrandSlam.OPP_GETS_REMAIN,
             "Legal but leave leftmost": GrandSlam.LEAVE_LEFT,
             "Legal but leave rightmost": GrandSlam.LEAVE_RIGHT}
INV_GRANDSLAM = inv_dict(GRANDSLAM)

RSTARTER = {'Alternate': RoundStarter.ALTERNATE,
            'Round Winner': RoundStarter.WINNER,
            'Round Loser': RoundStarter.LOSER}
INV_RSTARTER = inv_dict(RSTARTER)

CROSSCAPTOWN = {'Leave': CrossCaptOwn.LEAVE,
                'Pick on Capture': CrossCaptOwn.PICK_ON_CAPT,
                'Alway Pick': CrossCaptOwn.ALWAYS_PICK}
INV_XCOWN = inv_dict(CROSSCAPTOWN)


# %%  helper classes

@dc.dataclass(eq=False)
class GameParams:
    """The tk vars for game parameters.
    These names must match the GameInfo names."""

    name: tk.StringVar
    about: tk.StringVar
    game_class: tk.IntVar

    # board
    holes: tk.IntVar
    seeds: tk.IntVar
    stores: tk.BooleanVar

    # game dynamic
    rounds: tk.BooleanVar
    round_starter: tk.StringVar
    blocks: tk.BooleanVar
    child: tk.BooleanVar
    convert_cnt: tk.IntVar

    # sow
    min_move: tk.IntVar
    sow_direct: tk.StringVar
    sow_start: tk.BooleanVar
    skip_start: tk.BooleanVar
    sow_own_store: tk.BooleanVar
    mlaps: tk.BooleanVar
    visit_opp: tk.BooleanVar
    mustshare: tk.BooleanVar
    mustpass: tk.BooleanVar
    udir_holes: list

    # capture
    capsamedir: tk.BooleanVar
    oppsidecapt: tk.BooleanVar
    moveunlock: tk.BooleanVar
    evens: tk.BooleanVar
    crosscapt: tk.BooleanVar
    xcpickown: tk.StringVar
    multicapt: tk.BooleanVar
    capt_on: list
    grandslam: tk.StringVar
    capt_min: tk.IntVar
    nosinglecapt: tk.BooleanVar

    # scores
    stores_m: tk.IntVar
    child_cnt_m: tk.IntVar
    access_m: tk.IntVar
    seeds_m: tk.IntVar
    empties_m: tk.IntVar
    evens_m: tk.IntVar
    easy_rand: tk.IntVar
    repeat_turn: tk.IntVar


    def get_dict(self):
        """Return the dataclass as a dict.
        asdict doesn't work because the values are not serializable.
        The dataclasses doc says to use this create shallow copies."""

        return dict((field.name, getattr(self, field.name))
                    for field in dc.fields(self))


    def get_items(self):
        """Return the items in the dataclass."""

        return self.get_dict().items()


    def get_info_items(self):
        """Return the dictionary with items that are in the
        GameInfo structure."""

        def del_key_if(key, idict):
            if key in idict:
                del idict[key]

        info_dict = self.get_dict()
        del_key_if('game_class', info_dict)
        del_key_if('holes', info_dict)
        del_key_if('seeds', info_dict)
        del_key_if('stores_m', info_dict)
        del_key_if('child_cnt_m', info_dict)
        del_key_if('access_m', info_dict)
        del_key_if('seeds_m', info_dict)
        del_key_if('empties_m', info_dict)
        del_key_if('evens_m', info_dict)
        del_key_if('easy_rand', info_dict)
        del_key_if('repeat_turn', info_dict)
        return info_dict.items()


class Counter:
    """A little class so that row usage is consistent and easy to code."""

    def __init__(self):
        self.cnt = -1

    def nrow(self):
        """Increment row and return it."""
        self.cnt += 1
        return self.cnt

    def row(self):
        """Return the current row without increment."""
        return self.cnt


@dc.dataclass
class NonUiData:
    """Keep a local copy of game info data from the config file
    that is not available on the UI or tkvars maintaining it's
    persistence.

    other_dict will be the the keys parallel to game class, constants
    and info. These are effectively comments."""

    difficulty: int = 1
    help_file: str = ''
    rnd_left_fill: bool = False
    rnd_umove: bool = False
    no_sides: bool = False
    waldas: bool = False
    goal: Goal = Goal.MAX_SEEDS
    sow_blkd_div: bool = False
    capttwoout: bool = False
    one_child: bool = False
    move_one: bool = False

    ai_params: dict  = dc.field(default_factory=dict)
    other_dict: dict = dc.field(default_factory=dict)

    def get_items(self):
        """Return the items in the dataclass.
        asdict doesn't work because the values are not serializable.
        The dataclasses doc says to use this create shallow copies."""

        return dict((field.name, getattr(self, field.name))
                    for field in dc.fields(self)).items()


# %%  game params UI

class MancalaGames(tk.Frame):
    """Main interface to select game parameters, save & load games,
    and play Mancala games."""

    def __init__(self):

        self.game_consts = None
        self.game_info = None
        self.game = None
        self.game_ui = None

        self.non_ui_data = NonUiData()
        self.filename = None
        self.param_changed = False

        self.master = tk.Tk()

        self.master.title('Choose Mancala Options')
        self.master.resizable(False, False)
        self.master.wm_geometry('+400+200')
        super().__init__(self.master)
        self.master.report_callback_exception = self._exception_callback
        warnings.showwarning = self._warning
        self.pack()

        self._create_menus()

        self.tkvars = self._build_tkvars()

        name_frame = tk.Frame(self.master, padx=3, pady=3, borderwidth=3)
        name_frame.pack(side='top', expand=True, fill='x')
        tk.Label(name_frame, text="Game Name").pack(side='left')
        tk.Entry(name_frame, textvariable=self.tkvars.name
                 ).pack(side='right', expand=True, fill='x')

        self.opt_frame = tk.Frame(self.master, padx=3, pady=3,
                                  borderwidth=3, relief='ridge')
        self.opt_frame.pack(side='top', expand=True, fill='both')
        self.lft_frame = tk.Frame(self.opt_frame, padx=3, pady=3,
                                  borderwidth=3)
        self.lft_frame.pack(side='left', expand=True, fill='y')
        self.rgt_frame = tk.Frame(self.opt_frame, padx=3, pady=3,
                                  borderwidth=3)
        self.rgt_frame.pack(side='right', expand=True, fill='y')

        # save these
        self.about_text = None
        self.but_frame = None
        self.udir_frame = None

        self._build_gclass_ui(self.lft_frame)
        self._build_board_ui(self.lft_frame)
        self._build_sow_params_ui(self.lft_frame)
        self._build_scorer_ui(self.lft_frame)
        self._build_game_dyn_ui(self.rgt_frame)
        self._build_capt_params_ui(self.rgt_frame)
        self._build_about_ui(self.rgt_frame)

        self._add_commands_ui()


    @staticmethod
    def _exception_callback(*args):
        """Support debugging by printing the play_log and the traceback."""

        game_log.dump()
        traceback.print_exception(args[0], args[1], args[2])


    @staticmethod
    def _help():
        """Have the os pop open the help file in a browser."""

        os.startfile(man_path.get_path('mancala_help.html'))


    @staticmethod
    def _add_named_frame(frame, name):
        """Create a named frame and return it"""

        bfrm = tk.LabelFrame(frame, text=name, labelanchor='nw')
        bfrm.pack(side='top', expand=True, fill='both')

        return bfrm


    @staticmethod
    def _add_opts(frame, name, var, values, row_col):
        """Add an option menu item."""

        rcnt, lcol = row_col
        tk.Label(frame, text=name).grid(row=rcnt.nrow(), column=lcol)
        opmenu = tk.OptionMenu(frame, var, *values)
        opmenu.config(width=2 + max(len(str(val)) for val in values))
        opmenu.grid(row=rcnt.row(), column=lcol + 1)


    @staticmethod
    def _add_bool(frame, name, var, rcnt, lcol=0):
        """Add an checkbox item."""

        tk.Label(frame, text=name).grid(row=rcnt.nrow(), column=lcol)
        tk.Checkbutton(frame, variable=var
                       ).grid(row=rcnt.row(), column=lcol + 1)


    @staticmethod
    def _add_radio(frame, name, var, val, rcnt):
        """Add an checkbox item."""

        tk.Radiobutton(frame, text=name, variable=var, value=val,
                       ).grid(row=0, column=rcnt.nrow())


    def _create_menus(self):
        """Create the game control menus."""

        self.master.option_add('*tearOff', False)

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        gamemenu = tk.Menu(menubar)

        gamemenu.add_command(label='Help ...', command=self._help)
        menubar.add_cascade(label='Game', menu=gamemenu)


    def _build_gclass_ui(self, frame):
        """Build a frame to select the game class."""

        bfrm = self._add_named_frame(frame, 'Game Class')

        rcnt = Counter()
        for idx, game in enumerate(GAME_CLASSES.keys()):

            self._add_radio(bfrm, game,
                            self.tkvars.game_class, idx,
                            rcnt)


    def _build_board_ui(self, frame):
        """Build board frame."""

        bfrm = self._add_named_frame(frame, 'Board Props')
        tkv = self.tkvars

        rcnt = Counter()
        self._add_opts(bfrm, 'Holes per Side', tkv.holes, SIZES,
                       (rcnt, 0))
        self._add_bool(bfrm, 'Stores Present', tkv.stores, rcnt)

        rcnt = Counter()
        self._add_opts(bfrm, 'Start Seeds', tkv.seeds, SEEDS, (rcnt, 2))


    def _build_game_dyn_ui(self, frame):
        """Build the game dynamic frame."""

        bfrm = self._add_named_frame(frame, 'Game Dynamic')
        tkv = self.tkvars

        rcnt = Counter()
        self._add_bool(bfrm, 'Play in Rounds', tkv.rounds, rcnt)
        self._add_bool(bfrm, 'Block Unused Holes', tkv.blocks, rcnt)

        tk.Label(bfrm, text='Round Starter').grid(row=rcnt.nrow(), column=0)
        opmenu = tk.OptionMenu(bfrm, tkv.round_starter, *RSTARTER)
        opmenu.config(width=2 + max(len(str(val)) for val in RSTARTER))
        opmenu.grid(row=rcnt.row(), column=1, columnspan=3)

        rcnt = Counter()
        self._add_bool(bfrm, 'Enable Child Holes', tkv.child, rcnt, 2)
        self._add_opts(bfrm, 'Convert Count', tkv.convert_cnt, CONVERT,
                       (rcnt, 2))


    def _build_sow_params_ui(self, frame):
        """Bulid sow params frame."""

        bfrm = self._add_named_frame(frame, 'Sow Parameters')
        tkv = self.tkvars

        rcnt = Counter()
        self._add_opts(bfrm, 'Minimum Move', tkv.min_move, MIN_MOVE,
                       (rcnt, 0))
        self._add_opts(bfrm, 'Sow Direction', tkv.sow_direct, SOW_DIR,
                       (rcnt, 0))
        self._add_bool(bfrm, 'Must Share', tkv.mustshare, rcnt)
        self._add_bool(bfrm, 'Must Pass', tkv.mustpass, rcnt)

        rcnt = Counter()
        self._add_bool(bfrm, 'Sow into Start', tkv.sow_start, rcnt, 2)
        self._add_bool(bfrm, 'Sow Skip Start', tkv.skip_start, rcnt, 2)
        self._add_bool(bfrm, 'Sow Own Store', tkv.sow_own_store, rcnt, 2)
        self._add_bool(bfrm, 'Multi-Lap Sow', tkv.mlaps, rcnt, 2)
        self._add_bool(bfrm, 'Visit Opp for MLaps', tkv.visit_opp, rcnt, 2)

        tk.Label(bfrm, text='User Control Dir').grid(row=rcnt.nrow(),
                                                     column=0)
        self.udir_frame = tk.Frame(bfrm)
        self.udir_frame.grid(row=rcnt.row(), column=1, columnspan=3)
        for nbr in range(1, DEF_HOLES + 1):
            tk.Checkbutton(self.udir_frame, text=str(nbr),
                           variable=tkv.udir_holes[nbr - 1]
                           ).pack(side='left')


    def _build_capt_params_ui(self, frame):
        """Build capture params frame"""

        bfrm = self._add_named_frame(frame, 'Capture Parameters')
        tkv = self.tkvars

        rcnt = Counter()
        self._add_bool(bfrm, 'Capture in Sow Direct', tkv.capsamedir, rcnt)
        self._add_bool(bfrm, 'Capture Opp Side Only', tkv.oppsidecapt, rcnt)
        self._add_bool(bfrm, 'Move Unlocks for Capture', tkv.moveunlock, rcnt)
        self._add_bool(bfrm, 'Capture Evens', tkv.evens, rcnt)

        tk.Label(bfrm, text='Cross Capt Own').grid(row=rcnt.nrow(), column=0)
        opmenu = tk.OptionMenu(bfrm, tkv.xcpickown, *CROSSCAPTOWN)
        opmenu.config(width=2 + max(len(str(val)) for val in CROSSCAPTOWN))
        opmenu.grid(row=rcnt.row(), column=1, columnspan=3)

        tk.Label(bfrm, text='Capture On').grid(row=rcnt.nrow(), column=0)
        coframe = tk.Frame(bfrm)
        coframe.grid(row=rcnt.row(), column=1, columnspan=3)
        for nbr in range(1, MAX_CAPT):
            tk.Checkbutton(coframe, text=str(nbr),
                           variable=tkv.capt_on[nbr - 1]
                           ).pack(side='left')

        tk.Label(bfrm, text='Grand Slam Rule').grid(row=rcnt.nrow(), column=0)
        opmenu = tk.OptionMenu(bfrm, tkv.grandslam, *GRANDSLAM)
        opmenu.config(width=2 + max(len(str(val)) for val in GRANDSLAM))
        opmenu.grid(row=rcnt.row(), column=1, columnspan=3)

        rcnt = Counter()
        self._add_bool(bfrm, 'Do Multiple Captures', tkv.multicapt, rcnt, 2)
        self._add_bool(bfrm, 'Do Cross Capture', tkv.crosscapt, rcnt, 2)
        self._add_opts(bfrm, 'Capt Greater or Equal to', tkv.capt_min,
                       SEEDS, (rcnt, 2))
        self._add_bool(bfrm, 'No Single Seed Capt', tkv.nosinglecapt, rcnt, 2)


    def _build_scorer_ui(self, frame):
        """add the scorer params."""

        bfrm = self._add_named_frame(frame, 'Scorer Params')
        tkv = self.tkvars

        rcnt = Counter()
        self._add_opts(bfrm, 'Stores Mult', tkv.stores_m, MULTS, (rcnt, 0))
        self._add_opts(bfrm, 'Seeds Mult', tkv.seeds_m, MULTS, (rcnt, 0))
        self._add_opts(bfrm, 'Empties Mult', tkv.empties_m, MULTS, (rcnt, 0))
        self._add_opts(bfrm, 'Evens Mult', tkv.evens_m, MULTS, (rcnt, 0))

        rcnt = Counter()
        self._add_opts(bfrm, 'Child Count Mult', tkv.child_cnt_m, MULTS,
                       (rcnt, 2))
        self._add_opts(bfrm, 'Access (d>1) Mult', tkv.access_m, MULTS,
                       (rcnt, 2))
        self._add_opts(bfrm, 'Easy Error Random', tkv.easy_rand, EASYVALS,
                       (rcnt, 2))
        self._add_opts(bfrm, 'Repeat Turn Add in', tkv.repeat_turn, REPEATVALS,
                       (rcnt, 2))


    def _build_about_ui(self, frame):
        """Create a ui window to allow the about string to be edited."""

        bfrm = self._add_named_frame(frame, 'About')

        self.about_text = tk.Text(bfrm, width=45, height=8)
        self.about_text.pack(side='right')

        scroll = tk.Scrollbar(bfrm)
        self.about_text.configure(yscrollcommand=scroll.set)
        self.about_text.pack(side='left')

        scroll.config(command=self.about_text.yview)
        scroll.pack(side='right', fill='y')


    def _add_commands_ui(self):
        """Add buttons for commands."""

        self.but_frame = tk.Frame(self.master, padx=3, pady=3,
                                  borderwidth=3)
        self.but_frame.pack(side='bottom', expand=True, fill='both')

        tk.Button(self.but_frame, text='Test', command=self._test,
                  ).pack(side='left', expand=True, fill='x')
        tk.Button(self.but_frame, text='Load', command=self._load
                  ).pack(side='left', expand=True, fill='x')
        tk.Button(self.but_frame, text='Save', command=self._save
                  ).pack(side='left', expand=True, fill='x')
        tk.Button(self.but_frame, text='Play', command=self._play
                  ).pack(side='left', expand=True, fill='x')


    def _add_tkvar_str(self, tkvar_dict, name, default):
        """Add a string to the vars dict"""

        tkvar_dict[name] = tk.StringVar(self.master, default, name=name)


    def _add_tkvar_bool(self, tkvar_dict, name, default):
        """Add a boolean to the vars dict"""

        tkvar_dict[name] = tk.BooleanVar(self.master, default, name=name)


    def _add_tkvar_int(self, tkvar_dict, name, default):
        """Add an int to the vars dict"""

        tkvar_dict[name] = tk.IntVar(self.master, default, name=name)


    def _build_tkvars(self):
        """Create the tk variables for each input field
        giving them names so the trace's are easier to deal with.
        Setup traces so we know when they change."""

        tkvars_dict = {}

        self._add_tkvar_str(tkvars_dict, ckey.NAME, DEF_NAME)

        self._add_tkvar_int(tkvars_dict, ckey.HOLES, DEF_HOLES)
        self._add_tkvar_int(tkvars_dict, 'seeds', DEF_SEEDS)
        self._add_tkvar_bool(tkvars_dict, 'stores', True)

        self._add_tkvar_bool(tkvars_dict, 'rounds', False)
        self._add_tkvar_str(tkvars_dict, ckey.ROUND_STARTER,
                            INV_RSTARTER[RoundStarter.ALTERNATE])
        self._add_tkvar_bool(tkvars_dict, 'blocks', False)
        self._add_tkvar_bool(tkvars_dict, 'child', False)
        self._add_tkvar_int(tkvars_dict, 'convert_cnt', 0)

        self._add_tkvar_int(tkvars_dict, 'min_move', 1)
        self._add_tkvar_str(tkvars_dict, ckey.SOW_DIRECT,
                            INV_SOW_DIR[Direct.CCW])
        self._add_tkvar_bool(tkvars_dict, 'sow_start', False)
        self._add_tkvar_bool(tkvars_dict, 'skip_start', True)
        self._add_tkvar_bool(tkvars_dict, 'sow_own_store', False)
        self._add_tkvar_bool(tkvars_dict, 'mlaps', False)
        self._add_tkvar_bool(tkvars_dict, 'visit_opp', False)
        self._add_tkvar_bool(tkvars_dict, 'mustshare', False)
        self._add_tkvar_bool(tkvars_dict, 'mustpass', False)
        tkvars_dict[ckey.UDIR_HOLES] = \
            [tk.BooleanVar(self.master, False,
                           name='udir_' + str(idx + 1))
             for idx in range(MHOLES_RTOP)]

        self._add_tkvar_bool(tkvars_dict, 'capsamedir', False)
        self._add_tkvar_bool(tkvars_dict, 'oppsidecapt', False)
        self._add_tkvar_bool(tkvars_dict, 'moveunlock', False)
        self._add_tkvar_bool(tkvars_dict, 'evens', False)
        self._add_tkvar_bool(tkvars_dict, 'crosscapt', False)
        self._add_tkvar_bool(tkvars_dict, 'multicapt', False)
        self._add_tkvar_int(tkvars_dict, 'capt_min', 0)
        self._add_tkvar_bool(tkvars_dict, 'nosinglecapt', False)
        self._add_tkvar_str(tkvars_dict, 'xcpickown',
                            INV_XCOWN[CrossCaptOwn.LEAVE])
        tkvars_dict[ckey.CAPT_ON] = \
            [tk.BooleanVar(self.master, dval,
                           name='capt_on_' + str(idx + 1))
             for idx, dval in enumerate([False, True, False, False, False])]
        self._add_tkvar_str(tkvars_dict, 'grandslam',
                            INV_GRANDSLAM[GrandSlam.LEGAL])

        self._add_tkvar_int(tkvars_dict, 'stores_m', 4)
        self._add_tkvar_int(tkvars_dict, 'access_m', 0)
        self._add_tkvar_int(tkvars_dict, 'seeds_m', 0)
        self._add_tkvar_int(tkvars_dict, 'empties_m', 0)
        self._add_tkvar_int(tkvars_dict, 'evens_m', 0)
        self._add_tkvar_int(tkvars_dict, 'child_cnt_m', 0)
        self._add_tkvar_int(tkvars_dict, 'easy_rand', 0)
        self._add_tkvar_int(tkvars_dict, 'repeat_turn', 0)

        self._add_tkvar_str(tkvars_dict, 'about', '')
        self._add_tkvar_int(tkvars_dict, 'game_class', 0)

        for name, var in tkvars_dict.items():
            if name in (ckey.CAPT_ON, ckey.UDIR_HOLES):
                for cvar in var:
                    cvar.trace_add('write', self._tkvalue_changed)
            else:
                var.trace_add('write', self._tkvalue_changed)

        return GameParams(**tkvars_dict)


    def _tkvalue_changed(self, var, index, mode):
        """Called-back whenever any tkvar is changed."""

        _ = (index, mode)

        self.param_changed = True

        if var == ckey.NAME:
            self.filename = self.tkvars.name.get() + '.txt'

        elif var == ckey.HOLES:
            self._resize_udirs()


    def _resize_udirs(self):
        """Change the number of the checkboxes on the screen.
        All the variables were built with the tkvars.
        Destroy any extra widgets or make any required new ones."""

        widgets = self.udir_frame.winfo_children()

        prev_holes = len(widgets)
        holes = self.tkvars.holes.get()

        for idx in range(holes, prev_holes):
            widgets[idx].destroy()

        for idx in range(prev_holes + 1, holes + 1):
            tk.Checkbutton(self.udir_frame, text=str(idx),
                           variable=self.tkvars.udir_holes[idx - 1]
                           ).pack(side='left')


    def destroy(self):
        """Remove the traces from the tk variables."""

        for name, var in self.tkvars.get_items():
            if name in (ckey.CAPT_ON, ckey.UDIR_HOLES):
                for cvar in var:
                    cvar.trace_remove(*cvar.trace_info()[0])
            else:
                var.trace_remove(*var.trace_info()[0])


    def _prepare_about(self):
        """Return the about text."""

        return self.about_text.get('1.0', 'end')


    def _prepare_scorer(self):
        """Collect the scorer parameters."""

        return gi.Scorer(stores_m=self.tkvars.stores_m.get(),
                         access_m=self.tkvars.access_m.get(),
                         seeds_m=self.tkvars.seeds_m.get(),
                         evens_m=self.tkvars.evens_m.get(),
                         empties_m=self.tkvars.empties_m.get(),
                         child_cnt_m=self.tkvars.child_cnt_m.get(),
                         easy_rand=self.tkvars.easy_rand.get(),
                         repeat_turn=self.tkvars.repeat_turn.get())


    def _prepare_info_dict(self):
        """Build the value dict of the """

        vdict = {}

        vdict[ckey.RND_LEFT_FILL] = self.non_ui_data.rnd_left_fill
        vdict[ckey.RND_UMOVE] = self.non_ui_data.rnd_umove
        vdict[ckey.NO_SIDES] = self.non_ui_data.no_sides
        vdict[ckey.CAPTTWOOUT] = self.non_ui_data.capttwoout
        vdict[ckey.WALDAS] = self.non_ui_data.waldas
        vdict[ckey.ONE_CHILD] = self.non_ui_data.one_child
        vdict[ckey.MOVE_ONE] = self.non_ui_data.move_one
        vdict[ckey.SOW_BLKD_DIV] = self.non_ui_data.sow_blkd_div
        vdict[ckey.GOAL] = self.non_ui_data.goal
        vdict[ckey.HELP_FILE] = self.non_ui_data.help_file
        vdict[ckey.DIFFICULTY] = self.non_ui_data.difficulty
        vdict[ckey.AI_PARAMS] = self.non_ui_data.ai_params

        vdict[ckey.ABOUT] = self._prepare_about()
        vdict[ckey.SCORER] = self._prepare_scorer()

        for name, var in self.tkvars.get_info_items():

            if name == ckey.CAPT_ON:
                vdict[name] = [idx + 1
                               for idx, cvar in enumerate(var)
                               if cvar.get()]

            elif name == ckey.UDIR_HOLES:
                holes = self.tkvars.holes.get()
                vdict[name] = [idx for idx in range(holes)
                               if var[idx].get()]

            elif name == ckey.SOW_DIRECT:
                vdict[name] = SOW_DIR[var.get()]

            elif name == ckey.GRANDSLAM:
                vdict[name] = GRANDSLAM[var.get()]

            elif name == ckey.ROUND_STARTER:
                vdict[name] = RSTARTER[var.get()]

            elif name == ckey.XCPICKOWN:
                vdict[name] = CROSSCAPTOWN[var.get()]

            elif name not in [ckey.ABOUT, ckey.SCORER]:
                vdict[name] = var.get()

        return vdict


    def _prepare_game(self):
        """Build the two game variables: constants and info
        and then build the game.
        This function should be wrapped with a try because
        exceptions/warnings might be raised."""

        gclass = list(GAME_CLASSES.values())[self.tkvars.game_class.get()]

        self.game_consts = gc.GameConsts(self.tkvars.seeds.get(),
                                         self.tkvars.holes.get())
        vdict = self._prepare_info_dict()
        self.game_info = gi.GameInfo(nbr_holes=self.game_consts.holes,
                                     rules=gclass.rules,
                                     **vdict)

        self.game = gclass(self.game_consts, self.game_info)

        self.param_changed = False


    def _test(self):
        """Try to build the game params and game,
        trap any exceptions, report to user."""

        self.param_changed |= self.about_text.edit_modified()
        if (self.game_consts and self.game_info and self.game
                and not self.param_changed):
            return

        try:
            self._prepare_game()

        except (gc.GameConstsError, gi.GameInfoError, NotImplementedError
                ) as error:
            message = error.__class__.__name__ + ':  ' + str(error)
            tk.messagebox.showerror('Parameter Error', message)

            self.game_consts = None
            self.game_info = None
            self.game = None

    @staticmethod
    def _warning(message, *_):
        """Notify user of warnings during parameter test."""

        tk.messagebox.showwarning('Parameter Warning', message)

    def _fill_capts_and_udirs(self, game_dict):
        """Copy capt on and udir data from game_info into tkvars
        self.tkvars.holes must be set before this is called."""

        for var in self.tkvars.capt_on:
            var.set(False)
        for var in self.tkvars.udir_holes:
            var.set(False)

        if ckey.CAPT_ON in game_dict[ckey.GAME_INFO]:
            for capt in game_dict[ckey.GAME_INFO][ckey.CAPT_ON]:
                self.tkvars.capt_on[capt - 1].set(True)

        if ckey.UDIR_HOLES in game_dict[ckey.GAME_INFO]:
            for udir in game_dict[ckey.GAME_INFO][ckey.UDIR_HOLES]:
                self.tkvars.udir_holes[udir].set(True)


    def _fill_tkvars_nonui(self, game_dict):
        """Copy data from game_dict into tkvars to update the ui.
        The top three dict values are required; and both
        game_const values (holes, nbr_start) are required.
        Everything else is optional (all data in game_info, except
        nbr_holes, but we have that in consts) so use a GameInfo
        object created w/o optional parameters to get the defaults
        (capt_on is optional, but not having it generates a
        warning which confuses the user)."""

        self.tkvars.name.set(game_dict[ckey.GAME_INFO].get('name',
                                                           'Mancala'))

        self.tkvars.holes.set(game_dict[ckey.GAME_CONSTANTS]['holes'])
        self.tkvars.seeds.set(game_dict[ckey.GAME_CONSTANTS]['nbr_start'])

        gi_defaults = gi.GameInfo(
            nbr_holes=game_dict[ckey.GAME_CONSTANTS]['nbr_start'],
            capt_on=[2],
            rules=mancala.Mancala.rules)

        self._fill_capts_and_udirs(game_dict)

        ginfo = game_dict[ckey.GAME_INFO]
        for fname in gi.GameInfo.get_fields():

            if fname not in [ckey.UDIRECT, ckey.SOW_DIRECT,
                             ckey.GRANDSLAM, ckey.NO_SIDES, ckey.WALDAS,
                             ckey.MOVE_ONE, ckey.ONE_CHILD,
                             ckey.GOAL, ckey.SOW_BLKD_DIV, ckey.CAPTTWOOUT,
                             ckey.RND_LEFT_FILL, ckey.ROUND_STARTER,
                             ckey.RND_UMOVE, ckey.XCPICKOWN,
                             ckey.SCORER, ckey.DIFFICULTY,
                             ckey.HELP_FILE, ckey.UDIR_HOLES,
                             ckey.CAPT_ON, ckey.AI_PARAMS]:
                var = getattr(man_games.tkvars, fname)
                if fname in ginfo:
                    var.set(ginfo[fname])
                else:
                    var.set(getattr(gi_defaults, fname))

        self.tkvars.sow_direct.set(
            INV_SOW_DIR[game_dict[ckey.GAME_INFO].get(
                ckey.SOW_DIRECT, gi_defaults.sow_direct)])
        self.tkvars.grandslam.set(
            INV_GRANDSLAM[game_dict[ckey.GAME_INFO].get(
                ckey.GRANDSLAM, gi_defaults.grandslam)])
        self.tkvars.round_starter.set(
            INV_RSTARTER[game_dict[ckey.GAME_INFO].get(
                ckey.ROUND_STARTER, gi_defaults.round_starter)])
        self.tkvars.xcpickown.set(
            INV_XCOWN[game_dict[ckey.GAME_INFO].get(
                ckey.XCPICKOWN, gi_defaults.xcpickown)])

        gi_scorer = game_dict[ckey.GAME_INFO]['scorer']
        self.tkvars.stores_m.set(
            gi_scorer.get('stores_m', gi_defaults.scorer.stores_m))
        self.tkvars.access_m.set(
            gi_scorer.get('access_m', gi_defaults.scorer.access_m))
        self.tkvars.seeds_m.set(
            gi_scorer.get('seeds_m', gi_defaults.scorer.seeds_m))
        self.tkvars.empties_m.set(
            gi_scorer.get('empties_m', gi_defaults.scorer.empties_m))
        self.tkvars.evens_m.set(
            gi_scorer.get('evens_m', gi_defaults.scorer.evens_m))
        self.tkvars.child_cnt_m.set(
            gi_scorer.get('child_cnt_m', gi_defaults.scorer.child_cnt_m))
        self.tkvars.easy_rand.set(
            gi_scorer.get('easy_rand', gi_defaults.scorer.easy_rand))
        self.tkvars.repeat_turn.set(
            gi_scorer.get('repeat_turn', gi_defaults.scorer.repeat_turn))

        self.about_text.delete('1.0', 'end')
        self.about_text.insert('1.0', game_dict[ckey.GAME_INFO]['about'])

        self.tkvars.game_class.set(
            list(GAME_CLASSES.keys()).index(game_dict[ckey.GAME_CLASS]))

        self.non_ui_data.difficulty = \
            game_dict[ckey.GAME_INFO].get(ckey.DIFFICULTY,
                                          gi_defaults.difficulty)
        self.non_ui_data.help_file = \
            game_dict[ckey.GAME_INFO].get(ckey.HELP_FILE,
                                          gi_defaults.help_file)
        self.non_ui_data.ai_params = \
            game_dict[ckey.GAME_INFO].get(ckey.AI_PARAMS,
                                          gi_defaults.ai_params)
        self.non_ui_data.rnd_left_fill = \
            game_dict[ckey.GAME_INFO].get(
                ckey.RND_LEFT_FILL, gi_defaults.rnd_left_fill)
        self.non_ui_data.rnd_umove = \
            game_dict[ckey.GAME_INFO].get(
                ckey.RND_UMOVE, gi_defaults.rnd_umove)
        self.non_ui_data.no_sides = \
            game_dict[ckey.GAME_INFO].get(
                ckey.NO_SIDES, gi_defaults.no_sides)
        self.non_ui_data.capttwoout = \
            game_dict[ckey.GAME_INFO].get(
                ckey.CAPTTWOOUT, gi_defaults.capttwoout)
        self.non_ui_data.waldas = \
            game_dict[ckey.GAME_INFO].get(
                ckey.WALDAS, gi_defaults.waldas)
        self.non_ui_data.one_child = \
            game_dict[ckey.GAME_INFO].get(
                ckey.ONE_CHILD, gi_defaults.one_child)
        self.non_ui_data.move_one = \
            game_dict[ckey.GAME_INFO].get(
                ckey.MOVE_ONE, gi_defaults.move_one)
        self.non_ui_data.sow_blkd_div = \
            game_dict[ckey.GAME_INFO].get(
                ckey.SOW_BLKD_DIV, gi_defaults.sow_blkd_div)
        self.non_ui_data.goal = \
            game_dict[ckey.GAME_INFO].get(
                ckey.GOAL, gi_defaults.goal)

        del game_dict[ckey.GAME_CLASS]
        del game_dict[ckey.GAME_CONSTANTS]
        del game_dict[ckey.GAME_INFO]
        self.non_ui_data.other_dict = game_dict

    def _load(self):
        """Load params from file. Check size for reasonableness.
        Translate the json string. Convert non-primitive types.
        Build game_consts and game_info.
        json.JSONDecodeError is dervied from ValueError."""

        filename = tkfile.askopenfilename(
            parent=self.master,
            title='Load Parameters',
            initialdir=man_path.get_path('GameProps'))
        if not filename:
            return

        self.filename = os.path.basename(filename)

        try:
            game_dict = man_config.read_game(filename)
        except ValueError as error:
            tk.messagebox.showerror('JSON File Error', error)
            return

        self._fill_tkvars_nonui(game_dict)
        self._test()

    def _save(self):
        """Save params to file.
        Remove udirect from info dict to reduce
        duplication: udirect is derived from udir_holes."""

        self._test()
        if not self.game_consts or not self.game_info:
            return

        info_dict = dc.asdict(self.game_info)
        del info_dict[ckey.UDIRECT]

        game_dict = {ckey.GAME_CLASS:
                     list(GAME_CLASSES.keys())[self.tkvars.game_class.get()],
                     ckey.GAME_CONSTANTS: self.game_consts.get_dict(),
                     ckey.GAME_INFO: info_dict
                     }
        game_dict.update(self.non_ui_data.other_dict)

        if not self.filename:
            self.filename = info_dict['name'] + '.txt'

        filename = tkfile.asksaveasfilename(
            parent=self.master,
            title='Save Parameters',
            confirmoverwrite=True,
            initialdir=man_path.get_path('GameProps'),
            initialfile=self.filename,
            filetypes=[('text file', '.txt')],
            defaultextension='.txt')
        if not filename:
            return

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(game_dict, file, indent=3)

    def _set_frame_active(self, frame, new_state):
        """Activate or deactivate wigets, recursing through frames."""

        for child in frame.winfo_children():

            if isinstance(child, (tk.Frame, tk.LabelFrame)):
                self._set_frame_active(child, new_state)

            elif isinstance(child, tk.Scrollbar):
                pass

            elif isinstance(child, tk.Text):
                tstate = new_state if new_state == DISABLED else NORMAL
                child.configure(state=tstate)

            else:
                child.configure(state=new_state)

    def _set_active(self, activate):
        """Activate or deactivate main window wingets."""

        new_state = ACTIVE if activate else DISABLED

        self._set_frame_active(self.opt_frame, new_state)
        self._set_frame_active(self.but_frame, new_state)

    def _play(self):
        """Create and play the game. deactivate param ui and block
        while the game is being played. reactivate when the game
        is exited."""

        self._test()
        if not self.game_consts or not self.game_info or not self.game:
            return

        self.game_ui = mancala_ui.MancalaUI(self.game, self.master)
        self._set_active(False)

        self.game_ui.grab_set()
        self.game_ui.wait_window()
        self._set_active(True)

# %%  main

if __name__ == '__main__':

    man_games = MancalaGames()
    man_games.mainloop()
