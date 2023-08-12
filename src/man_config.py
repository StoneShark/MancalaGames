# -*- coding: utf-8 -*-
"""Read a mancala configuration file and return
the game class, game constants and game info.

Created on Tue Jul 18 12:16:20 2023
@author: Ann"""

import json

import cfg_keys as ckey
import game_constants as gc
import game_interface as gi

from game_classes import GAME_CLASSES
from game_interface import Direct


MAX_LINES = 150
MAX_CHARS = 2000


def read_game(filename):
    """Read a mancala configuration returning the
    game dictionary.  The main UI uses this to load tk widgets,
    then calls test to report any errors making it easier on the
    human to correct any errors."""

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    text = ''.join(lines)
    if len(lines) > MAX_LINES or len(text) > MAX_CHARS:
        raise ValueError('Input file problem.')

    game_dict = json.loads(text)

    info_dict = game_dict[ckey.GAME_INFO]
    info_dict[ckey.NBR_HOLES] = game_dict[ckey.GAME_CONSTANTS][ckey.HOLES]

    if ckey.FLAGS in info_dict:
        flags_dict = info_dict[ckey.FLAGS]

        if ckey.SOW_DIRECT in flags_dict:
            flags_dict[ckey.SOW_DIRECT] = Direct(flags_dict[ckey.SOW_DIRECT])

    return game_dict


def read_game_config(filename):
    """Read a mancala configuration file and return
    the game class, constants and info."""

    game_dict = read_game(filename)
    game_class = game_dict[ckey.GAME_CLASS] \
        if ckey.GAME_CLASS in game_dict else 'Mancala'

    game_consts = gc.GameConsts(**game_dict[ckey.GAME_CONSTANTS])
    info_dict = game_dict[ckey.GAME_INFO]

    if ckey.FLAGS in info_dict:
        flags_dict = info_dict[ckey.FLAGS]
        info_dict[ckey.FLAGS] = gi.GameFlags(**flags_dict)
    else:
        info_dict[ckey.FLAGS] = gi.GameFlags()

    if ckey.SCORER in info_dict:
        info_dict[ckey.SCORER] = gi.Scorer(**info_dict[ckey.SCORER])
    else:
        info_dict[ckey.SCORER] = gi.Scorer()

    game_info = gi.GameInfo(**info_dict)

    return game_class, game_consts, game_info


def make_game(filename):
    """Return a constructed game from the configuration."""

    class_name, consts, info = read_game_config(filename)

    gclass = GAME_CLASSES[class_name]
    return gclass(consts, info)
