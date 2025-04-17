# -*- coding: utf-8 -*-
"""Handles the configuration files for mancala games and mancala ui:

Read a specified game configuration file and return the game class,
game constants, game info, and player dictionary.

Utilities to get default values and retrieve or set game configuration
value via the 'cspec' from the game_params file.

Read the parameters data files game_params and game_param_descs,
return a dictionary of  param_name: Param  (mancala games only).

Reads (or creates) the ini for UI options (mancala ui only).

Created on Tue Jul 18 12:16:20 2023
@author: Ann"""

import configparser
import csv
import dataclasses as dc
import json
import re
import os
import tkinter as tk
from tkinter import font

import ai_player
import animator
import cfg_keys as ckey
import game_constants as gconsts
import game_interface as gi
import man_path
import param_consts as pc

from ai_player import ALGORITHM_DICT
from ai_player import AI_PARAM_DEFAULTS
from game_classes import GAME_CLASSES


# %%  constants

MAX_LINES = 150
MAX_CHARS = 3000

NO_CONVERT = [ckey.NAME, ckey.ABOUT, ckey.HELP_FILE,
              ckey.UDIR_HOLES, ckey.CAPT_ON]

SP = ' '
OPT_TAG = '_'
GI_TAG = ckey.GAME_INFO + SP + OPT_TAG
AI_TAG = ckey.PLAYER + SP + ckey.AI_PARAMS + SP + OPT_TAG
SCR_TAG = ckey.PLAYER + SP + ckey.SCORER + SP + OPT_TAG

MINUS = '-'
INT_LIST_CHARS = '0123456789, '
ELIST_STR = '[]'

SKIP_TAB = 'skip'

PARAM = re.compile('^<param ([a-z0-9_]+)>')

REMOVE_TAGS = [re.compile(r'<a[^>]+>'),
               re.compile(r'</a>'),
               re.compile(r'(  \+ )?<img[^>]+>\n'),
               re.compile(r'<b[^>]+>'),
               re.compile(r'</b>'),

               # not html but used to disable the auto linker
               re.compile(r'<nolink>'),

               ]

# %% read config files

def read_game(filename):
    """Read a mancala configuration returning the
    game dictionary.  The main UI uses this to load tk widgets,
    then calls test to report any errors making it easier on the
    human to correct any errors.

    Convert the type of all of the flags to those expected by
    the dataclass. This validates enum values and provides access
    to methods on the enums."""

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    text = ''.join(lines)
    if len(lines) > MAX_LINES or len(text) > MAX_CHARS:
        raise ValueError('Input file problem.')

    game_dict = json.loads(text)

    info_dict = game_dict[ckey.GAME_INFO]
    for fdesc in dc.fields(gi.GameInfo):
        if fdesc.name in info_dict and fdesc.name not in NO_CONVERT:
            ftype = type(fdesc.default)
            info_dict[fdesc.name] = ftype(info_dict[fdesc.name])

    return game_dict


def read_game_config(filename):
    """Read a mancala configuration file and return
    the game class, constants, info and player_dict."""

    game_dict = read_game(filename)
    game_class = game_dict[ckey.GAME_CLASS] \
        if ckey.GAME_CLASS in game_dict else 'Mancala'

    game_consts = gconsts.GameConsts(**game_dict[ckey.GAME_CONSTANTS])
    info_dict = game_dict[ckey.GAME_INFO]

    gclass = GAME_CLASSES[game_class]
    game_info = gi.GameInfo(**info_dict,
                            nbr_holes=game_consts.holes,
                            rules=gclass.rules)

    return game_class, game_consts, game_info, game_dict[ckey.PLAYER]


def make_game(filename):
    """Return a constructed game from the configuration
    and the player dictionary."""

    class_name, consts, info, player_dict = read_game_config(filename)

    gclass = GAME_CLASSES[class_name]
    return gclass(consts, info), player_dict


# %% access config data and defaults

def get_config_value(game_config, config_spec, option, vtype):
    """Get the value from the configuration, if it's not there
    use the constructor default."""

    value = get_gc_value(game_config, config_spec, option)
    if value is None:
        value = get_construct_default(vtype, config_spec, option)
    return value


def get_construct_default(vtype, cspec, option):
    """The defaults in the UI parameter table yield a playable game,
    they are not the actual construction defaults.
    Return the construction default."""

    rval = False

    if cspec == GI_TAG:
        rval = gi.GameInfo.get_default(option)

    elif cspec == SCR_TAG:
        rval = ai_player.ScoreParams.get_default(option)

    elif cspec == AI_TAG:
        rval = AI_PARAM_DEFAULTS[option]

    elif option == ckey.ALGORITHM:
        rval = list(ALGORITHM_DICT.keys())[0]

    elif option == ckey.GAME_CLASS:
        rval = list(GAME_CLASSES.keys())[0]

    elif option == ckey.DIFFICULTY:
        rval = 1

    elif vtype in (pc.STR_TYPE, pc.MSTR_TYPE):
        rval = ""

    elif vtype == pc.INT_TYPE:
        rval = 0

    return rval


def get_gc_value(game_config, cspec, option):
    """Game_config_spec format is one of
        word+  or  word* _
    where option is substituted for _

    Lookup and return the value in a series of nested dictionaries."""

    tags = cspec.split(SP)

    vdict = game_config
    for tag in tags:
        if tag == OPT_TAG:
            if option in vdict:
                return vdict[option]
            return None

        if tag in vdict:
            vdict = vdict[tag]
        else:
            return None

    return vdict


def set_config_value(game_config, cspec, option, value):
    """Set the value in a series of nested dictionaries;
    create empty dictionaries as required."""

    tags = cspec.split(SP)

    vdict = game_config
    for tag in tags[:-1]:
        if tag not in vdict:
            vdict[tag] = {}
        vdict = vdict[tag]

    if tags[-1] == OPT_TAG:
        vdict[option] = value
    else:
        vdict[tags[-1]] = value


def del_default_config_tag(game_config, vtype, cspec, option):
    """If the option has the default value,
    delete it from it's parent dictionary."""

    tags = cspec.split(SP)

    vdict = game_config
    for tag in tags:
        if tag == OPT_TAG:
            if option in vdict:
                default = get_construct_default(vtype, cspec, option)
                if vdict[option] == default:
                    vdict.pop(option, None)
                return

        if tag in vdict:
            vdict = vdict[tag]
        else:
            return


# %% parameters files


@dc.dataclass
class Param:
    """A single parameter description.
    These must be in the same order that they are in the spead sheet
    (or Params shouldn't be created with positional args)."""

    tab: str
    option: str
    text: str
    cspec: str
    order: int
    vtype: str
    ui_default: object
    row: int
    col: int
    description: str = dc.field(repr=False, default='')


TAB_IDX = 0
OPTION_IDX = 1
STR_IDX = 2
UI_DEFAULT_IDX = 6
INT_IDXS = [4, 7, 8]


class ParamData(dict):
    """A dictionary of the parameter data. Keys are the 'option'
    column (parameter name); values are Param dataclass objects."""

    def __init__(self, del_tags=True, no_descs=False):

        super().__init__()
        self._read_params_table()
        if not no_descs:
            self._read_param_descriptions(del_tags)


    def _read_param_descriptions(self, del_tags):
        """Read the parameter descriptions file.
        static method because read_params_file is used outside
        mancala_games."""

        with open(man_path.get_path('game_param_descs.txt'), 'r',
                  encoding='us-ascii') as file:
            data = file.readlines()

        text = ''
        param = ''
        for line in data:

            # skip blank lines
            if not line.strip():
                continue

            pmatch = PARAM.match(line)
            if pmatch:
                # if we have a param name, save the accumulated data
                if param:
                    self[param].description = text

                param = pmatch.groups()[0]
                text = ''

                if param not in self:
                    msg = f"Description without game_params data {param}"
                    raise ValueError(msg)

            elif del_tags:
                tline = line
                for tag in REMOVE_TAGS:
                    tline, _ = tag.subn('', tline, count=5)
                text += tline

            else:
                text += line

        # add the last parameter
        self[param].description = text


    @staticmethod
    def convert_default(value):
        """Convert the ui_defaults to appropriate python values.

        NONE is an enumeration value (usually 0) not the value None."""

        convert_dict = {'true': True,
                        'false': False,
                        }
        value = value.strip()

        if (key := value.lower()) in convert_dict:
            return convert_dict[key]

        if value.isdigit() or (value[0] == MINUS and value[1:].isdigit()):
            return int(value)

        if value == ELIST_STR:
            return []

        if (value[0] == ELIST_STR[0]
                and value[-1] == ELIST_STR[-1]
                and all(c in INT_LIST_CHARS for c in value[1:-1])):
            substrs = value[1:-1].split(',')
            return [int(val.strip()) for val in substrs]

        return value


    def _read_params_table(self):
        """Read the game parameters file.
        static method because used outside mancala_games."""

        with open(man_path.get_path('game_params.csv'), 'r',
                  encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)

        fields = data[0]
        if not all(fname == pfield.name
                   for fname, pfield in zip(fields, dc.fields(Param))):
            raise ValueError("game_params columns are not as expected")

        for rec in data[1:]:
            if rec[TAB_IDX] == SKIP_TAB:
                continue

            opt_name = rec[OPTION_IDX]
            if opt_name in self:
                msg = f"Duplicate option in game_params {opt_name}."
                raise ValueError(msg)

            for idx in INT_IDXS:
                if not rec[idx].isdigit():
                    raise ValueError("Expected int for {opt_name} col {idx}.")
                rec[idx] = int(rec[idx])

            rec[UI_DEFAULT_IDX] = self.convert_default(rec[UI_DEFAULT_IDX])
            self[opt_name] = Param(*rec)



# %% read and process config ini

INI_FILENAME = 'mancala.ini'

# don't define a default for difficulty, if present it overrides game files

DEFAULTS = {
    'button_size': '100',

    'system_color': 'SystemButtonFace',
    'inactive_color': 'grey60',
    'turn_color': 'LightBlue2',
    'turn_dark_color': 'LightBlue4',
    'ai_color': 'LightBlue2',

    'rclick_color': 'grey',
    'grid_color': 'red',
    'grid_density': '25',

    'choose_color': 'pink2',
    'seed_color': 'goldenrod',
    'move_color': 'sandy brown',

    'font_family' : 'Helvetica',
    'font_size' : '14',
    'font_weight' : 'bold',

    'show_tally': 'no',
    'touch_screen': 'no',
    'facing_players': 'no',
    'ownership_arrows': 'no',

    'disable_animator': 'no',
    'ani_active': 'yes',
    'ani_delay': '250',

    'ai_active': 'no',
    'ai_delay': '1',

    'log_live': 'no',
    'log_level': 'move',
    }

DEFAULT = 'default'
DIFFICULTY = 'difficulty'
DIS_ANIMAT = 'disable_animator'
COLORS = ['system_color', 'turn_color', 'turn_dark_color', 'ai_color',
          'inactive_color', 'rclick_color', 'grid_color']

VALID_DENSITY = {'12', '25', '50', '75'}
VALID_DELAY = {'0', '1', '2'}
VALID_DIFFICULTY = {'0', '1', '2', '3'}

# intentionally not including the "too much detail" levels
VALID_LOG_LEVEL = {'move', 'import', 'step', 'info', 'detail'}


class ConfigData:
    """Read/create configuration data."""

    def __init__(self, tk_root=None, name=None):
        # pylint: disable=bare-except

        pathname = man_path.get_path(INI_FILENAME, no_error=True)
        if not pathname:
            self.create_ini_file()
            return

        self._config = configparser.ConfigParser()
        try:
            self._config.read(pathname, encoding='utf-8')
        except:
            self.create_ini_file()

        # bools, ints and fonts are interpreted in their get_ funcs
        self._check_colors(tk_root)
        self.validate('grid_density', VALID_DENSITY)
        self.validate('ai_delay', VALID_DELAY)
        self.validate('log_level', VALID_LOG_LEVEL)

        for section in self._config.sections():
            if (DIFFICULTY in self._config[section]
                    and self._config[section][DIFFICULTY]
                        not in VALID_DIFFICULTY):
                print('Deleting invalid difficulty in mancala.ini file.')
                del self._config[section][DIFFICULTY]

        self.load_game_specific(name)


    def __getitem__(self, key):
        """Get the item from the config dictionary or defaults.
        'difficulty' is not in the dictionary, it should only
        be retrieved with get_int and a default specified."""

        return self._config[DEFAULT].get(key, DEFAULTS[key])


    def _check_colors(self, tk_root):
        """Check all of the colors, delete any bad ones,
        causing __getitem__ to return default."""

        if tk_root is None:
            print("Tk app not provided, colors not tested")
            return

        for section in self._config.sections():
            for key, value in self._config[section].items():

                if key not in COLORS:
                    continue

                try:
                    tk_root.winfo_rgb(value)

                except tk.TclError:
                    print(f"{section} {key} value invalid, using default.")
                    del self._config[section][key]


    def validate(self, key, valid_values):
        """Check the value against the valid values, if
        missing or not valid, set it to a default.

        Do not check difficulty because it's absence is
        treated differently than the default."""

        for section in self._config.sections():
            value = self._config[section].get(key, DEFAULTS[key])
            if value not in valid_values:
                print(f'Revert invalid {key} in mancala.ini file to default.')
                print('Values:', valid_values)
                self._config[section][key] = DEFAULTS[key]


    def load_game_specific(self, name):
        """If there is a game specific section, bubble
        those options up to the default section.
        The rest of the software only uses the default
        section."""

        if not name:
            return

        name = name.replace(' ', '_')
        if name not in self._config.sections():
            return

        for key, value in self._config[name].items():
            self._config[DEFAULT][key] = value


    @staticmethod
    def _get_filename():
        """Find a suitable place for the ini file.
        Seperate fuction to support testing."""

        directory = os.getcwd()
        pdir, bdir = os.path.split(directory)
        if bdir in {'GameProps', 'GamePropsNoRelease', 'src'}:
            directory = pdir

        return os.path.join(directory, INI_FILENAME)


    def create_ini_file(self):
        """Create a default ini file.
        Make an attempt to put the ini file at the project root."""

        fullpath = self._get_filename()
        print(f"Creating ini file: {fullpath}")

        self._config = configparser.ConfigParser()
        self._config[DEFAULT] = DEFAULTS

        with open(fullpath, 'w', encoding='UTF-8') as configfile:
            self._config.write(configfile)


    def get_int(self, key, default=None):
        """Attempt to get an int from the config.
        If it is missing and default was provided use it.
        If there is an error converting the value from the
        ini file use the value from the dictionary."""

        if default is not None and key not in self._config[DEFAULT]:
            return default

        try:
            int_val = int(self._config[DEFAULT][key])
        except (KeyError, ValueError):
            int_val = int(DEFAULTS[key])

        if int_val < 0:
            int_val = int(DEFAULTS[key])

        return int_val


    def get_bool(self, key):
        """Interpret the value as an affirmative or not.
        If the key is not there return False"""

        if key in self._config[DEFAULT]:
            return self._config[DEFAULT][key].lower() in {'yes', 'true'}

        return False


    def get_font(self):
        """Attempt to get a font from the config.
        If it is missing return the default.
        If it invalid, 'font.Font' will pick the best match."""

        ftuple = (self['font_family'],
                  self.get_int('font_size'),
                  self['font_weight'])
        return font.Font(font=ftuple)



CONFIG = None

def read_ini_file(tk_root=None, name=None):
    """Read the ini file.
    MancalaUI cannot do it directly or we would get
    circular imports.
    tk_root is required to test the color values,
    if it is not provided the colors are not tested."""
    # pylint: disable=global-statement

    global CONFIG
    CONFIG = ConfigData(tk_root, name)



def check_disable_animator():
    """Determine if the animator should be disabled,
    if so do it.

    If there is an ini file with disable_animator = yes,
    the animator will be completely disabled.

    Doing this separately allows it to be checked
    before any Mancala or MancalaUI is created."""
    # pylint: disable=bare-except

    pathname = man_path.get_path(INI_FILENAME, no_error=True)
    config = configparser.ConfigParser()

    try:
        config.read(pathname, encoding='utf-8')
    except:
        return

    disable = False
    if DEFAULT in config and DIS_ANIMAT in config[DEFAULT]:
        disable = config[DEFAULT][DIS_ANIMAT].lower() in {'yes', 'true'}

    if disable:
        animator.ENABLED = False
