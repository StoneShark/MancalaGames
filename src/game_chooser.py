# -*- coding: utf-8 -*-
"""A UI that allows play of any of the games in the GameProps directory.

Created on Thu Mar 23 08:10:28 2023
@author: Ann"""

# %% imports

import abc
import copy
import dataclasses as dc
import enum
import functools as ft
import itertools as it
import os.path
import random
import textwrap
import tkinter as tk
from tkinter import ttk

import ai_player
import animator
import cfg_keys as ckey
import favorites
import game_info as gi
import man_config
import man_path
import mancala_ui
import round_tally
import ui_utils
import variants


# %% constants

PATH = man_path.get_path(man_path.GAMEDIR) + '/'
MANCALA = 'Mancala'

COLON = ':'
STAR = '🟊'
DESC_WIDTH = 72
COL_WIDTH = 30
FIL_COLS = 3

TINY = 4
SMALL = 6
LARGER = 7
LARGEST = 9

FAVS = None

#  Filter control (0x4) and both alt keys (0x20000 & 0x40000)
#  ('Shift', 'Lock', 'Control', 'Mod1', 'Mod2', 'Mod3', 'Mod4', 'Mod5',
#   'Button1', 'Button2', 'Button3', 'Button4', 'Button5')
TK_KEYMOD_MASK = 0xffff0004


# %%  filter dicts

GCLASS = {'Mancala': lambda gclass: gclass == MANCALA,
          'Other': lambda gclass: gclass != MANCALA}

SIZES = {'Tiny (< 4)': lambda holes: holes < TINY,
         'Small (4 - 5)': lambda holes: TINY <= holes < SMALL,
         'Medium (6)': lambda holes: holes == SMALL,
         'Larger (7 - 8)': lambda holes: LARGER <= holes < LARGEST,
         'Largest (>= 9)': lambda holes: holes >= LARGEST}


GOALS = {'Max Seeds': lambda goal: goal == gi.Goal.MAX_SEEDS,
         'Max Seeds Tally': lambda goal: goal in (gi.Goal.RND_SEED_COUNT,
                                                  gi.Goal.RND_EXTRA_SEEDS,
                                                  gi.Goal.RND_POINTS,
                                                  gi.Goal.RND_WIN_COUNT_MAX),
         'Clear Own': lambda goal: goal in (gi.Goal.CLEAR,
                                            gi.Goal.RND_WIN_COUNT_CLR),
         'Deprive Opponent': lambda goal: goal in (gi.Goal.DEPRIVE,
                                                   gi.Goal.RND_WIN_COUNT_DEP),
         'Immoblize Opp': lambda goal: goal in (gi.Goal.IMMOBILIZE,
                                                   gi.Goal.RND_WIN_COUNT_IMB),
         'Territory': lambda goal: goal == gi.Goal.TERRITORY,
        }

CAPTS = {'Basic Capture': lambda ginfo: (any([ginfo.get(ckey.CAPT_MAX, 0),
                                              ginfo.get(ckey.CAPT_MIN, 0),
                                              ginfo.get(ckey.CAPT_ON, 0),
                                              ginfo.get(ckey.EVENS, 0)])
                                 and not any([ginfo.get(ckey.CROSSCAPT, 0),
                                              ginfo.get(ckey.CAPT_TYPE, 0)])),
         'Cross Capture': lambda ginfo: ginfo.get(ckey.CROSSCAPT, 0),
         'Capt Type Set': lambda ginfo: ginfo.get(ckey.CAPT_TYPE, 0),
         'Other': lambda ginfo: not any([ginfo.get(ckey.CAPT_MAX, 0),
                                         ginfo.get(ckey.CAPT_MIN, 0),
                                         ginfo.get(ckey.CAPT_ON, 0),
                                         ginfo.get(ckey.EVENS, 0),
                                         ginfo.get(ckey.CROSSCAPT, 0),
                                         ginfo.get(ckey.CAPT_TYPE, 0)]),
         }

SOWRS = {'None': lambda sow_rule: not sow_rule,
         'Sow Closed': lambda sow_rule: sow_rule in (
             gi.SowRule.SOW_BLKD_DIV,
             gi.SowRule.SOW_BLKD_DIV_NR),
         'Take when Sowing': lambda sow_rule: sow_rule in (
             gi.SowRule.SOW_CAPT_ALL,
             gi.SowRule.OWN_SOW_CAPT_ALL),
         'Capture on Laps': lambda sow_rule: sow_rule in (
             gi.SowRule.LAP_CAPT,
             gi.SowRule.LAP_CAPT_OPP_GETS,
             gi.SowRule.LAP_CAPT_SEEDS),
         'Skip some holes': lambda sow_rule: sow_rule in (
             gi.SowRule.NO_SOW_OPP_NS,
             gi.SowRule.MAX_SOW,
             gi.SowRule.NO_OPP_CHILD,
             gi.SowRule.OPP_CHILD_ONLY1,
             gi.SowRule.NO_CHILDREN),
         'Other': lambda sow_rule: sow_rule not in (
             gi.SowRule.NONE,
             gi.SowRule.SOW_BLKD_DIV,
             gi.SowRule.SOW_BLKD_DIV_NR,
             gi.SowRule.SOW_CAPT_ALL,
             gi.SowRule.OWN_SOW_CAPT_ALL,
             gi.SowRule.LAP_CAPT,
             gi.SowRule.LAP_CAPT_OPP_GETS,
             gi.SowRule.LAP_CAPT_SEEDS,
             gi.SowRule.NO_SOW_OPP_NS,
             gi.SowRule.MAX_SOW,
             gi.SowRule.NO_OPP_CHILD,
             gi.SowRule.OPP_CHILD_ONLY1,
             gi.SowRule.NO_CHILDREN),
        }

SOWDIR = {'CW': lambda ginfo: ginfo.get(ckey.SOW_DIRECT, 1) == -1,
          'CCW': lambda ginfo: ginfo.get(ckey.SOW_DIRECT, 1) == 1,
          'SPLIT': lambda ginfo: not ginfo.get(ckey.SOW_DIRECT, 1),
          'Toward Center': lambda ginfo: ginfo.get(ckey.SOW_DIRECT, 1) == \
              gi.Direct.TOCENTER,
          'Players Alt Dir': lambda ginfo: ginfo.get(ckey.SOW_DIRECT, 1) == 2,
          'Even Odd Dir': lambda ginfo: ginfo.get(ckey.SOW_DIRECT, 1) == 3,
          }

FEATS = {'No Sides': lambda ginfo: ginfo.get(ckey.NO_SIDES, 0),
         'Start Pattern': lambda ginfo: ginfo.get(ckey.START_PATTERN, 0),
         'Prescribed Open': lambda ginfo: ginfo.get(ckey.PRESCRIBED, 0),
         'Move Restrictions': lambda ginfo:
             (ginfo.get(ckey.ALLOW_RULE, 0)
              or ginfo.get(ckey.MIN_MOVE, 0) > 1),
         'Must Pass': lambda ginfo: ginfo.get(ckey.MUSTPASS, 0),
         'Must Share': lambda ginfo: ginfo.get(ckey.MUSTSHARE, 0),
         'Inhibitor': lambda ginfo:
             (ginfo.get(ckey.NOCAPTMOVES, 0)
              or ginfo.get(ckey.PRESCRIBED, 0) == gi.SowPrescribed.ARNGE_LIMIT
              or ginfo.get(ckey.ROUND_FILL, 0) in (gi.RoundFill.SHORTEN,
                                                   gi.RoundFill.SHORTEN_ALL)),
         'User Sow Direct': lambda ginfo:
             len(ginfo.get(ckey.UDIR_HOLES, [])) >= 1,
         'Pre-sow Capture': lambda ginfo: ginfo.get(ckey.PRESOWCAPT, 0),
         'Repeat Turn': lambda ginfo: any([ginfo.get(ckey.CAPT_RTURN, 0),
                                           ginfo.get(ckey.SOW_OWN_STORE, 0),
                                           ginfo.get(ckey.XC_SOWN, 0)]),
         'Grand Slam': lambda ginfo: ginfo.get(ckey.GRANDSLAM, 0),
         'Multiple Capt': lambda ginfo: ginfo.get(ckey.MULTICAPT, 0),
         'Take More': lambda ginfo: ginfo.get(ckey.PICKEXTRA, 0),
         'Rounds': lambda ginfo: ginfo.get(ckey.ROUNDS, 0),
         'Round Tally': lambda ginfo: ginfo.get(ckey.GOAL, 0) in \
                                         round_tally.RoundTally.GOALS,
         }

# pylint: disable=magic-value-comparison
GNOTES = {
    'Named Variants': lambda gdict: gdict.get(ckey.VARIANTS, 0),
    'Variations': lambda gdict: (gdict.get(ckey.VARI_PARAMS, 0)
                                     or gdict.get(ckey.VARIANTS, 0)),
    'Deviations': lambda gdict: any('deviat' in key.lower()
                                    for key in gdict.keys()),
    'Notes': lambda gdict: (any('note' in key.lower()
                                for key in gdict.keys())
                            or 'lagniappe' in gdict.keys()
                            or 'reference' in gdict.keys()
                            or 'question' in gdict.keys()),
    }


# pylint: disable=magic-value-comparison
RULES = {

    'Russ': lambda gdict: 'Russ' in gdict.get('rules', ''),
    'Valdez': lambda gdict: 'Valdez' in gdict.get('rules', ''),
    'Man World': lambda gdict: 'mancala.fandom' in gdict.get('rules', ''),
    'Davies': lambda gdict: 'Davies' in gdict.get('rules', ''),
    'Other': lambda gdict: ('Russ' not in gdict.get('rules', '')
                            and 'Valdez' not in gdict.get('rules', '')
                            and 'mancala.fandom' not in gdict.get('rules', '')
                            and 'Davies' not in gdict.get('rules', '')),

    }

# pylint: disable=magic-value-comparison
ORIGIN = {
        'Traditional': lambda gdict: 'traditional' in gdict.get('origin', ''),
        'Modern': lambda gdict: 'modern' in gdict.get('origin', ''),
        'Example': lambda gdict: 'example' in gdict.get('origin', ''),
        'Other': lambda gdict: ('origin' in gdict
                                and gdict['origin'] not in
                                    ['traditional', 'modern', 'example']),
        'Not Specified': lambda gdict: 'origin' not in gdict,
        }

RATINGS = {STAR * 1: lambda gname: FAVS.rating(gname) == 1,
           STAR * 2: lambda gname: FAVS.rating(gname) == 2,
           STAR * 3: lambda gname: FAVS.rating(gname) == 3,
           STAR * 4: lambda gname: FAVS.rating(gname) == 4,
           STAR * 5: lambda gname: FAVS.rating(gname) >= 5,
           'Not Rated': lambda gname: not FAVS.rating(gname),
           }


# pylint: disable=magic-value-comparison
def build_regions():
    """Build the dictionary to test for regions.

    Maps used:
        https://www.worldatlas.com/geography/regions-of-africa.html
        https://www.worldatlas.com/geography/what-are-the-five-regions-of-asia.html
    """

    world_regions = ['Africa', 'Eastern Africa', 'Central Africa',
                     'Northern Africa', 'Western Africa',
                     'Asia', 'Central Asia', 'South Asia', 'Southeast Asia',
                     'Americas', 'Caribbean',
                     'Europe']
    indent = ['Eastern Africa', 'Central Africa',
              'Northern Africa', 'Western Africa',
              'Central Asia', 'South Asia', 'Southeast Asia',
              'Caribbean']

    def region_test_func(rname):
        """Return a function that tests that the rname is in the
        region key of the game dict."""

        def _region_test(gdict):
            """Do the test:
                1. if no region specified in game dict, return False
                2. if rname is Africa or Asia, return True for all games
                with the word Africa or Asia in the region string
                3. if rname is Americas, include any games that list Caribbean,
                return True
                4. return exact match in the region list

            This allows selections such as
                "Africa" but not "Eastern Africa"
                "Americas" but not "Caribbean"
            """

            region =  gdict.get('region', None)
            if region is None:
                return False

            if rname in {'Africa', 'Asia'}:
                return rname in region

            if rname == 'Americas' and 'Caribbean' in region:
                return True

            return rname in region.split(', ')

        return _region_test

    def other_region(gdict):
        """True if there is a region specified but it is not in
        world_regions."""

        region = gdict.get('region', None)
        if region is None:
            return False

        return not any(rname in region for rname in world_regions)

    rdict = {('   ' + rname) if rname in indent else rname:
             region_test_func(rname)
             for rname in world_regions}
    rdict |= {'Other': other_region}
    rdict |= {'Not Specified': lambda gdict: 'region' not in gdict}

    return rdict


REGIONS = build_regions()


def build_dir_filter():
    """If there are additional directories specified in the ini
    file add a filter for them."""

    man_config.read_ini_file()
    game_dirs = man_config.CONFIG.get_game_dirs()
    if not game_dirs:
        return None

    def game_dir_func(dir_name):
        """Return a function that tests to see if a filename
        (full path) is has dir_name as it's lowest directory"""

        def _test_dir(filename):

            dname = os.path.dirname(filename)
            base_dir = os.path.basename(dname)
            return base_dir == dir_name

        return _test_dir

    dir_dict = {man_path.GAMEDIR: game_dir_func(man_path.GAMEDIR)}
    for dname in game_dirs:
        dir_dict |= {dname: game_dir_func(dname)}

    return dir_dict


DIR_DICT = build_dir_filter()


# %% GameFilters frame & classes

class BaseFilter(ttk.Frame, abc.ABC):
    """A filter category.  Checkboxes are created for each
    name, value pair return from the parent's items method.

    A dictionary of the tkvariables for the checkboxes is
    created. The keys will be either the value or the name
    based on value_keys."""

    def __init__(self, parent, filt_obj, label, param_key, value_keys):

        super().__init__(parent, borderwidth=3)
        self.parent = parent
        self.filt_obj = filt_obj
        self.param_key = param_key

        row = ui_utils.Counter()

        lbl = ttk.Label(self, text=label, style='Title.TLabel')
        lbl.grid(row=row.count, column=0, columnspan=FIL_COLS, sticky='ew')
        lbl.configure(anchor='center')  # anchor in style is ignored

        self.filt_var = self.build_filters(filt_obj, row, value_keys)

        rnbr = row.count
        ttk.Button(self, text='All',
                   command=self.not_filtered,
                   style='Filt.TButton'
                   ).grid(row=rnbr, column=0, padx=1, pady=1)
        ttk.Button(self, text='Inv',
                   command=self.invert,
                   style='Filt.TButton'
                   ).grid(row=rnbr, column=1, padx=1, pady=1)
        ttk.Button(self, text='None',
                   command=self.all_filtered,
                   style='Filt.TButton'
                   ).grid(row=rnbr, column=2, padx=1, pady=1)


    def build_filters(self, filt_obj, row, value_keys):
        """Build the filter checkboxes and their variables.
        Seperate so that it can speciallized by derived classes.

        filter_var must have set and get methods."""

        filt_var = {}

        for name, value in self.items():

            key = value if value_keys else name
            filt_var[key] = tk.BooleanVar(self, value=1)

            ttk.Checkbutton(self, text=name,
                            variable=filt_var[key],
                            command=filt_obj.update_list
                            ).grid(row=row.count, column=0,
                                   columnspan=FIL_COLS, sticky='ew')
        return filt_var


    def not_filtered(self):
        """Set all of the filter variables."""

        for var in self.filt_var.values():
            var.set(1)
        self.filt_obj.update_list()


    def all_filtered(self):
        """Clear all of the filter variables."""

        for var in self.filt_var.values():
            var.set(0)
        self.filt_obj.update_list()


    def invert(self):
        """Invert the filters."""

        for var in self.filt_var.values():
            var.set(not var.get())
        self.filt_obj.update_list()


    def param(self, game_dict):
        """Get the value from the game_dict.
        If param_key is in the PARAMS structure, use that data to
        get the value or its default.
        Otherwise, the param_key is a top level element in the
        game_dict."""

        if self.param_key in man_config.PARAMS:
            value = man_config.get_config_value(
                        game_dict,
                        man_config.PARAMS[self.param_key].cspec,
                        self.param_key,
                        man_config.PARAMS[self.param_key].vtype)

        elif self.param_key is not True:
            value = game_dict[self.param_key]

        else:
            value = game_dict

        return value


    @abc.abstractmethod
    def items(self):
        """Return name, value pairs for each filter option.
        Name is shown on the UI for the filter option.
        Value can be what ever the show method will use to
        decide if a game should be included.

        If value is not immutable, be sure to create with
        value_keys of False."""


class VListFilter(BaseFilter):
    """A filter category based on a list of values."""

    def __init__(self, parent, filt_obj, label, val_list, param_key):

        self.val_list = val_list
        super().__init__(parent, filt_obj, label, param_key, value_keys=True)


    def items(self):
        """Return the this name and value pairs for this filter"""

        for evalue in self.val_list:
            yield evalue, evalue


    def show(self, game_dict):
        """Determine if the game associated with value
        should be shown.

        value: the enum value to test (an int)"""

        value = self.param(game_dict)
        return self.filt_var[value].get()


class EnumFilter(VListFilter):
    """A filter category based on enum values."""

    def items(self):
        """Return the name and value pairs for this filter"""

        for evalue in self.val_list:
            yield evalue.name, evalue.value


class DictFilter(BaseFilter):
    """A filter category based on a dictionary of rule_name: test"""

    def __init__(self, parent, filt_obj, label, filt_dict, param_key):

        self.filt_dict = filt_dict
        super().__init__(parent, filt_obj, label, param_key, value_keys=False)


    def items(self):
        """Return the name and value pairs for this filter"""

        return self.filt_dict.items()


    def show(self, game_dict):
        """Determine if the game associated should be shown."""

        value = self.param(game_dict)
        return any(test_func(value)
                   for test_name, test_func in self.filt_dict.items()
                   if self.filt_var[test_name].get())


class TriStateFilter(DictFilter):
    """Build a feature filter.

    These do not break the game list into non-overlapping sets."""

    def build_filters(self, filt_obj, row, _):
        """Build the tristate checkbuttons for
        the filter dictionary

        The TriStateCheckbuttons maintain their
        own state and have the same interfaces used for
        tk variables (get and set) so we don't need tk variables.

        value_keys is ignored, it must be False."""

        filt_var = {}

        for name in self.filt_dict.keys():

            filt_var[name] = \
                ui_utils.TriStateCheckbutton(self,
                                             text=name,
                                             update_cmd=filt_obj.update_list)
            filt_var[name].grid(row=row.count, column=0, columnspan=FIL_COLS,
                                sticky='ew')

        return filt_var


    def show(self, game_dict):
        """Determine if the game associated with value
        should be shown.

        value: value of the associated parameter to test"""

        for test_name, test_func in self.filt_dict.items():

            filt_val = self.filt_var[test_name].get()

            if filt_val is None:
                # don't care condition
                continue

            if filt_val != bool(test_func(self.param(game_dict))):
                return False

        return True


    def invert(self):
        """Invert the filters, but only those either True or False.
        Don't change the 'don't cares'."""

        for var in self.filt_var.values():
            val = var.get()
            if val is True:
                var.set(False)
            elif val is False:
                var.set(True)
        self.filt_obj.update_list()


@dc.dataclass
class FilterDesc:
    """Description of filters."""

    title: str
    fclass: type
    value_keys: object
    param_key: str

    tab: int
    col: int


MAX_COLUMNS = 7
fcol = ui_utils.Counter()  # count: increments; value: no increment

# can't build the tk objects yet, but build a table of filter groups
# so they are easier to move around
FILTERS = [
    FilterDesc('Game Class', DictFilter, GCLASS, ckey.GAME_CLASS,
               0, fcol.count),
    FilterDesc('Goal', DictFilter, GOALS, ckey.GOAL, 0, fcol.value),

    FilterDesc('Board Size', DictFilter, SIZES, ckey.HOLES, 0, fcol.count),
    FilterDesc('Lap Type', EnumFilter, gi.LapSower, ckey.MLAPS, 0, fcol.value),

    FilterDesc('Sow Rule', DictFilter, SOWRS, ckey.SOW_RULE, 0, fcol.count),
    FilterDesc('Sow Direct', DictFilter, SOWDIR, ckey.GAME_INFO,
               0, fcol.value),

    FilterDesc('Child Type', EnumFilter, gi.ChildType, ckey.CHILD_TYPE,
               0, fcol.count),

    FilterDesc('Capture Types', DictFilter, CAPTS, ckey.GAME_INFO,
               0, fcol.count),

    FilterDesc('Features', TriStateFilter, FEATS, ckey.GAME_INFO,
               0, fcol.count),
    ]

assert fcol.value < MAX_COLUMNS, F"Too many filter columns used {MAX_COLUMNS}."
fcol.reset()

FILTERS += [

    FilterDesc('Ratings', DictFilter, RATINGS, ckey.NAME, 1, fcol.count),
    # DIR_DICT filter, if it will be included

    FilterDesc('Origin', DictFilter, ORIGIN, True, 1, fcol.count),

    FilterDesc('Region', TriStateFilter, REGIONS, True, 1, fcol.count),

    FilterDesc('Rules Source', DictFilter, RULES, True, 1, fcol.count),

    FilterDesc('Configuration', TriStateFilter, GNOTES, True, 1, fcol.count),

    FilterDesc('AI Player', VListFilter,
               list(ai_player.ALGORITHM_DICT.keys()),
               ckey.ALGORITHM, 1, fcol.count),

    ]

if DIR_DICT:
    FILTERS += [FilterDesc('Directory', DictFilter, DIR_DICT, ckey.FILENAME,
                1, 0)]

assert fcol.value < MAX_COLUMNS, F"Too many filter columns used {MAX_COLUMNS}."
del fcol


class GameFilters(ttk.Frame):
    """A pane to collect all the game filters and the PLAY button."""

    def __init__(self, parent):

        super().__init__(parent, padding=3)
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)

        filt_frame = ttk.Notebook(self)
        filt_frame.grid(row=0, column=0, sticky=tk.NSEW)

        rule_tab = ttk.Frame(filt_frame, padding=3)
        filt_frame.add(rule_tab, text='Rules', padding=5, sticky=tk.NSEW)

        info_tab = ttk.Frame(filt_frame, padding=3)
        filt_frame.add(info_tab, text='About', padding=5, sticky=tk.NSEW)

        cframes = [[None] * MAX_COLUMNS, [None] * MAX_COLUMNS]
        for tidx, tab in enumerate([rule_tab, info_tab]):
            for idx in range(MAX_COLUMNS):
                cframes[tidx][idx] = ttk.Frame(tab)
                cframes[tidx][idx].grid(row=0, column=idx, sticky='ns')

        self.filters = [None] * len(FILTERS)
        for idx, fdesc in enumerate(FILTERS):

            self.filters[idx] = fdesc.fclass(cframes[fdesc.tab][fdesc.col],
                                             self,
                                             fdesc.title,
                                             fdesc.value_keys,
                                             fdesc.param_key)
            self.filters[idx].pack(side=tk.TOP, fill=tk.Y, expand=True)

        filt_frame.columnconfigure(tk.ALL, weight=1)
        rule_tab.columnconfigure(tk.ALL, weight=1)
        info_tab.columnconfigure(tk.ALL, weight=1)

        ttk.Button(self, text='Play',
                   command=parent.play_game,
                   style='Play.TButton').grid(
                       row=0, column=1, sticky='ns')

        self.columnconfigure(tk.ALL, weight=1)


    def not_filtered(self, _=None):
        """Clear all of the filters."""

        for filt in self.filters:
            filt.not_filtered()


    def all_filtered(self, _=None):
        """Set all of the filters."""

        for filt in self.filters:
            filt.all_filtered()


    def show_game(self, game_dict):
        """Test if the game should be shown based on the filter
        settings and the game_dict"""

        return all(filt.show(game_dict) for filt in self.filters)


    def update_list(self):
        """Update the parent's list of filtered games."""

        self.parent.filter_games()


# %% SelectList Frame

class SelectList(ttk.Labelframe):
    """Scrollable tree list for list of filtered games.
    Selecting one tells the parent it was selected."""

    def __init__(self, parent):

        super().__init__(parent, text='Game List', labelanchor='nw',
                         padding=4)
        self.parent = parent

        self.game_list = ttk.Treeview(self, show='tree', selectmode='browse',
                                      height=20)

        scroll = ttk.Scrollbar(self,
                               orient='vertical',
                               command=self.game_list.yview)
        self.game_list.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.Y)

        self.game_list.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)

        self.game_list.bind('<<TreeviewSelect>>', self.select_game)
        self.game_list.bind('<Button-3>', self.right_click)
        self.game_list.bind('<Double-Button-1>', self.play_game)


    def set_title(self, count=0):
        """Put the game count into the label frame text."""

        if count:
            self['text'] = f"Game List ({count})"
        else:
            self['text'] = "Game List"


    def select_game(self, _=None):
        """The user has selected a game, tell the parent
        it was selected."""

        game_name = self.game_list.selection()

        if game_name:
            game_name = game_name[0]
            self.parent.select_game(game_name)


    def play_game(self, _=None):
        """Play the game."""

        self.select_game()
        self.parent.play_game()


    def clear_glist(self):
        """Clear the game list."""

        for item in self.game_list.get_children():
            self.game_list.delete(item)


    def fill_glist(self, games):
        """Put the games in the treeview"""

        self.clear_glist()
        self.set_title(len(games))
        for name in games:
            self.game_list.insert('', tk.END, iid=name, text=name)


    def select(self, gname):
        """Select the game in the treeview."""

        self.game_list.selection_set(gname)
        self.game_list.focus(gname)
        self.game_list.see(gname)


    def right_click(self, event):
        """Right click on a game, do popup."""

        gamename = self.game_list.identify_row(event.y)
        if not gamename:
            return

        self.game_list.selection_set(gamename)

        menubar = tk.Menu(self)

        vnames = self.parent.get_variant_names(gamename)
        if vnames:

            varimenu = tk.Menu(menubar)
            for vname in vnames:
                varimenu.add_command(label=vname,
                                     command=ft.partial(self.parent.play_variant,
                                                        gamename, vname))
            menubar.add_cascade(label='Play Variant', menu=varimenu)

        ratemenu = tk.Menu(menubar)
        for rating in range(1, 6):
            ratemenu.add_command(label=STAR * rating,
                                 command=ft.partial(self.parent.set_rating,
                                                    rating))
        ratemenu.add_command(label='Clear',
                             command=ft.partial(self.parent.set_rating, 0))
        menubar.add_cascade(label='Rate Game', menu=ratemenu)

        menubar.add_command(label='Edit...', command=self.parent.edit_game)
        menubar.post(event.x_root, event.y_root)


    def jump_to_first(self, _):
        """Select and view first element of the treeview."""

        first = self.game_list.get_children()[0]
        if self.game_list.focus() != first:
            self.select(first)


    def jump_to_last(self, _):
        """Select and view last element of the treeview."""

        last = self.game_list.get_children()[-1]
        if self.game_list.focus() != last:
            self.select(last)


    def jump_up(self, event):
        """Move up item in the treeview."""

        current = self.game_list.focus()
        if event.widget is self.game_list or not current:
            return

        children = self.game_list.get_children()
        prev_idx = max(children.index(current) - 1, 0)
        self.select(children[prev_idx])


    def jump_down(self, event):
        """Move down one item in the treeview."""

        current = self.game_list.focus()
        if event.widget is self.game_list or not current:
            return

        children = self.game_list.get_children()
        next_idx = min(children.index(current) + 1, len(children) - 1)
        self.select(children[next_idx])


    def key_pressed(self, event):
        """If a key with a keysym of length 1 is pressed,
        select the next element that starts with that key,
        wrapping the search. If no elements start with that
        key; don't change the selection."""

        if len(event.keysym) > 1 or event.state & TK_KEYMOD_MASK:
            return
        key = event.keysym[0].lower()

        children = self.game_list.get_children()
        count = len(children)
        current = self.game_list.focus()
        if current:
            start = children.index(current)
            search = it.chain(range(start + 1, count), range(start))
        else:
            search = range(count)

        for cidx in search:
            child = children[cidx]

            if child[0].lower() == key:
                self.select(child)
                return


# %% AboutPane Frame

class AboutPane(ttk.Labelframe):
    """A pane for the game help text (called the 'about' text)."""

    def __init__(self, parent):

        super().__init__(parent, text='Game Overview', labelanchor='nw',
                         padding=4)

        self.text_box = tk.Text(self)

        scroll = ttk.Scrollbar(self,
                               orient='vertical',
                               command=self.text_box.yview)
        self.text_box.configure(yscrollcommand=scroll.set)
        self.text_box.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)
        self.text_box.configure(state=tk.DISABLED)

        scroll.config(command=self.text_box.yview)
        scroll.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.Y)


    def set_title(self, name=''):
        """Put the game count into the label frame text."""

        if name:
            self['text'] = f"Game Overview — {name}"
        else:
            self['text'] = "Game Overview"


    def clear_text(self):
        """Clear the text in the box."""

        self.text_box.configure(state=tk.NORMAL)
        self.text_box.delete('1.0', tk.END)
        self.text_box.configure(state=tk.DISABLED)
        self.set_title()


    def set_text(self, name, text):
        """Set the text in the box"""

        self.set_title(name)
        self.text_box.configure(state=tk.NORMAL)
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert('1.0', text)
        self.text_box.configure(state=tk.DISABLED)


    @staticmethod
    def game_prop_text(game_dict):
        """Collect text strings for the game properties in the
        config dict. Return a list of strings that can be formatted
        in two columns. Do not inlcude new lines."""

        holes = game_dict[ckey.GAME_CONSTANTS][ckey.HOLES]
        start = game_dict[ckey.GAME_CONSTANTS][ckey.NBR_START]
        goal = game_dict[ckey.GAME_INFO].get(ckey.GOAL, gi.Goal.MAX_SEEDS)

        ptxt = [f'Holes per side:  {holes}',
                f'Start seeds:  {start}',
                f'Goal: {goal.name}']

        if (ckey.GAME_CLASS in game_dict
                and game_dict[ckey.GAME_CLASS] != MANCALA):
            game_class  = game_dict[ckey.GAME_CLASS]
            ptxt += [f'Game Class: {game_class}']

        if ckey.HELP_FILE in game_dict[ckey.GAME_INFO]:
            help_file  = game_dict[ckey.GAME_INFO][ckey.HELP_FILE]
            ptxt += [f'Help File:  {help_file}']

        for param, value in sorted(game_dict[ckey.GAME_INFO].items(),
                                   key=lambda pair: pair[0]):

            if param in (ckey.NAME, ckey.ABOUT, ckey.GOAL, ckey.HELP_FILE):
                continue

            if param == ckey.CAPT_ON:
                vstr = ' '.join(str(val) for val in value)

            elif param == ckey.UDIR_HOLES:
                if len(value) == holes:
                    vstr = 'all'
                else:
                    vstr = ' '.join(str(val) for val in value)

            elif value is True:
                vstr = 'Yes'

            elif isinstance(value, enum.Enum):
                vstr = value.name

            else:
                vstr = str(value)

            lines = textwrap.fill(f'{man_config.PARAMS[param].text}: {vstr}',
                                  COL_WIDTH)
            ptxt += [line.strip() for line in lines.split('\n')]

        return ptxt


    @staticmethod
    def format_para(text):
        """Format a paragraph for the description."""

        paragraphs = text.split('\n')
        out_text = []
        for para in paragraphs:
            out_text += [textwrap.fill(man_config.remove_tags(para),
                                       DESC_WIDTH)]

        if not out_text[-1]:
            out_text.pop()
        return '\n'.join(out_text)


    def describe_game(self, game_name, game_dict):
        """Build a description of the game for the text window.
        Use the about text and any extra keys (not the standard
        game config keys)."""

        dtext = ''
        if (ckey.GAME_INFO in game_dict
                and ckey.ABOUT in game_dict[ckey.GAME_INFO]):

            dtext = self.format_para(game_dict[ckey.GAME_INFO][ckey.ABOUT])
        dtext += '\n'

        ptext = self.game_prop_text(game_dict)
        items = len(ptext)
        col1, rem = divmod(items, 2)
        if rem:
            col1 += 1
        if ptext[col1 - 1][-1] == COLON:
            col1 += 1
        for c1text, c2text in it.zip_longest(ptext[:col1], ptext[col1:],
                                             fillvalue=''):
            dtext += f"\n{c1text:{COL_WIDTH}}    {c2text:{COL_WIDTH}}"

        dtext += '\n'
        for key, text in game_dict.items():
            if key not in [ckey.GAME_CLASS, ckey.GAME_CONSTANTS,
                           ckey.GAME_INFO, ckey.PLAYER, ckey.FILENAME,
                           ckey.VARI_PARAMS, ckey.VARIANTS]:

                dtext += '\n'
                dtext += self.format_para(key.title() + ':  ' + text)
                dtext += '\n'

        rating = FAVS.rating(game_name)
        rtext = (STAR * rating) if rating else 'None'
        dtext += '\n'
        dtext += 'Rating:  ' + rtext

        self.set_text(game_name, dtext)


# %%  GameChooser - application frame

class GameChooser(ttk.Frame):
    """Main UI frame for new play_mancala.
    Includes filter, game list, and about panes.

    all_games: dictionary of game name: game dictionary

    games: list of currently filtered game names

    selected: the currently selected game name

    game_filter: filter panel and play button. Filter panel
    contains filters and contains a test for filter given
    a game dictionary.

    select_list: tree view of selectable games

    about_text: pane for show selected game description
    """

    def __init__(self, master, editor_class):

        global FAVS

        self.master = master
        self.editor_class = editor_class
        self.all_games = None
        self.games = None
        self.selected = None

        ui_utils.setup_styles(master)

        self.master.title('Play Mancala - Game Chooser')
        super().__init__(self.master, padding=3)
        self.master.resizable(False, True)
        self.pack(expand=tk.TRUE, fill=tk.BOTH)

        ui_utils.do_error_popups(self.master)

        self.game_filter = GameFilters(self)
        self.game_filter.grid(row=0, column=0, columnspan=2, sticky='ew')

        self.select_list = SelectList(self)
        self.select_list.grid(row=1, column=0, sticky='ns')

        self.about_text = AboutPane(self)
        self.about_text.grid(row=1, column=1, sticky=tk.NSEW)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(tk.ALL, weight=1)

        self.create_menus()

        man_config.check_disable_animator()

        # load these now so that errors can be reported via the UI
        man_config.read_params_data(need_descs=False)
        FAVS = favorites.GameFavorites(self)

        self.load_game_files()
        self.select_list.fill_glist(self.all_games.keys())


    def load_game_files(self):
        """Get a list of the game files, read the game_dict,
        create a dictionary of game name and about text."""

        self.all_games = {}
        for file in man_config.game_files():

            build_context = ui_utils.ReportError(self)
            with build_context:
                game_dict = man_config.read_game(file)
                game_name = game_dict[ckey.GAME_INFO][ckey.NAME]

            if build_context.error:
                print(f"Skipping {file} due to error.")
                continue

            if game_name in self.all_games:
                print(f'Skipping duplicate game name {game_name} from {file}.')
                continue

            self.all_games[game_name] = game_dict

        self.all_games = dict(sorted(self.all_games.items()))
        self.games = list(self.all_games.keys())


    def get_variant_names(self, gamename):
        """Return the list variant names defined for gamename."""

        game_dict = self.all_games[gamename]
        var_dict = game_dict.get(ckey.VARIANTS, None)
        return list(var_dict.keys()) if var_dict else None


    def create_menus(self):
        """Create the game control menus."""

        self.master.option_add('*tearOff', False)

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        gamemenu = tk.Menu(menubar)
        gamemenu.add_command(label='Play...', command=self.play_game,
                             accelerator='Ctrl-p')
        gamemenu.add_command(label='Edit...', command=self.edit_game,
                             accelerator='Ctrl-Shft-E')

        ratemenu = tk.Menu(menubar)
        for rating in range(1, 6):
            ratemenu.add_command(label=STAR * rating,
                                 command=ft.partial(self.set_rating, rating))
        ratemenu.add_command(label='Clear',
                             command=ft.partial(self.set_rating, 0))
        gamemenu.add_cascade(label='Rate Game', menu=ratemenu)

        gamemenu.add_separator()
        gamemenu.add_command(label='Random Game', command=self.select_random,
                             accelerator='Ctrl-r')

        menubar.add_cascade(label='Game', menu=gamemenu)

        filtmenu = tk.Menu(menubar)
        filtmenu.add_command(label='Show All',
                             command=self.game_filter.not_filtered,
                             accelerator='Ctrl-Shft-A')
        filtmenu.add_command(label='Clear All',
                             command=self.game_filter.all_filtered,
                             accelerator='Ctrl-Shft-C')
        menubar.add_cascade(label='Filters', menu=filtmenu)

        ui_utils.add_help_menu(menubar, self)
        self._key_bindings(self)


    def _key_bindings(self, active=True):
        """Bind or unbind the keys."""

        bindings = [('<Control-C>', self.game_filter.all_filtered),
                    ('<Control-A>', self.game_filter.not_filtered),
                    ('<Control-p>', self.play_game),
                    ('<Control-r>', self.select_random),
                    ('<Control-E>', self.edit_game),
                    ('<Return>', self.play_game),
                    ('<Home>', self.select_list.jump_to_first),
                    ('<End>', self.select_list.jump_to_last),
                    ('<Up>', self.select_list.jump_up),
                    ('<Down>', self.select_list.jump_down),
                    ('<Key>', self.select_list.key_pressed),
                    ]
        ui_utils.key_bindings(self, bindings, active)


    def select_game(self, game_name):
        """On game selection from the tree view,
        put it's help into the about_pane"""

        game_dict = self.all_games[game_name]
        self.about_text.describe_game(game_name, game_dict)
        self.selected = game_name


    def do_select(self, game_name):
        """Select a game that might not be visible.
        Used for select_random and select from the editor."""

        if game_name not in self.all_games:
            return

        self.select_list.select(game_name)
        self.select_game(game_name)


    def select_random(self, _=None):
        """Select a random game from the list of games in
        the game tree. Just select it, the user determine
        if they want to play it first."""

        self.do_select(random.choice(self.games))


    def filter_games(self):
        """Update the games in select_list to reflect the current
        filter settings."""

        self.games = [name
                      for name, gdict in self.all_games.items()
                      if self.game_filter.show_game(gdict)]
        self.select_list.fill_glist(self.games)

        if self.selected in self.games:
            self.select_list.select(self.selected)
        else:
            self.about_text.clear_text()
            self.selected = ''


    def set_rating(self, rating):
        """Set the rating for the game and reselect it to
        update the description."""

        if not self.selected:
            return

        FAVS.rate_game(self.selected, rating)
        self.select_game(self.selected)


    def _build_game_steps(self, game_dict, variant=None):
        """Do the steps to verify and build the game.
        If successful, return the game_ui."""

        variants.test_variation_config(game_dict, no_var_error=False)
        game = man_config.game_from_config(game_dict, variant)
        player_dict = game_dict[ckey.PLAYER]
        game.filename = game_dict[ckey.FILENAME]
        return mancala_ui.MancalaUI(game, player_dict, root_ui=self.master)


    def _build_and_play_game(self, game_dict, variant=None):
        """Build the game catching any build errors and play it.

        If there were no errors, allow the game to be played
        in a modal window."""

        build_context = ui_utils.ReportError(self)
        with build_context:
            game_ui = self._build_game_steps(game_dict, variant)

        if not build_context.error:
            game_ui.grab_set()
            game_ui.wait_window()


    def play_game(self, _=None):
        """Create the game and game_ui; which allows playing it."""

        if not self.selected:
            return

        game_dict = self.all_games[self.selected]
        self._build_and_play_game(game_dict)


    def play_variant(self, gamename, variant):
        """Create the game and game_ui; which allows playing it.
        The game dictionary is modified for the variant, so do a
        deep copy of the one in the all_games dict."""

        game_dict = copy.deepcopy(self.all_games[gamename])
        self._build_and_play_game(game_dict, variant)


    def edit_game(self, _=None):
        """Delete ourself and create the editor for the selected game."""

        if self.selected:
            quest = f'Do you wish to launch {self.selected} in the editor?'
        else:
            quest = 'Do you wish to switch to the Game Editor?'

        message = [quest,  'The chooser will be closed.']
        do_it = ui_utils.ask_popup(self.master,
                                   'Swap to Editor', message,
                                   ui_utils.YESNO)
        if not do_it:
            return

        self.destroy()
        animator.reset()
        self._key_bindings(active=False)

        man_games = self.editor_class(self.master, GameChooser)
        if self.selected:
            filename = self.all_games[self.selected]['filename']
            man_games.load_game(filename)
