# -*- coding: utf-8 -*-
"""Low level operations dealing only with files and
directories.

Created on Sat Aug 19 08:32:38 2023
@author: Ann"""

import os
import os.path

GAMEDIR = 'GameProps'
GAMEPATH = './' + GAMEDIR + '/'
ALL_PARAMS = '_all_params.txt'
GAME_EXT = '.txt'


def get_path(filename, no_error=False):
    """Find the path to the file or directory.

    Provide compatibility between different ways the
    software can be run."""

    places = ['.', '..', 'src', '../src', 'docs', '../docs',
              'help', '../help']

    for dirname in places:
        pathname = os.path.join(dirname, filename)
        if os.path.isfile(pathname) or os.path.isdir(pathname):
            break

    else:
        if no_error:
            return False

        raise FileNotFoundError(f"Can't find file {filename}.")

    return os.path.abspath(pathname)


def find_gamefile(gname, no_error=False):
    """Look in a few logical places for the file."""

    if os.path.isfile(gname):
        return gname

    places = ['./' + gname,
              './' + gname + '.txt',
              GAMEPATH + gname,
              GAMEPATH + gname + '.txt',
              '../' + GAMEPATH + gname,
              '../' + GAMEPATH + gname + '.txt']

    for fname in places:
        if os.path.isfile(fname):
            return fname

    if no_error:
        return False
    raise FileNotFoundError(f"Can't find file {gname}.")


def game_files():
    """Return the list of preconfigured games."""

    path = get_path(GAMEPATH)
    files = os.listdir(path)
    return [f for f in files if f != ALL_PARAMS and f[-4:] == GAME_EXT]
