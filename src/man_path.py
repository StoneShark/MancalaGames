# -*- coding: utf-8 -*-
"""Low level operations dealing only with files and
directories.

Created on Sat Aug 19 08:32:38 2023
@author: Ann"""

import argparse
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


def get_cmd_ln_gamename(optional=False):
    """Get a, possibly optional, game or file name from the
    command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument('gamename',
                        nargs='?' if optional else None,
                        default=None,
                        help='Game or filename.')

    cargs = parser.parse_args()
    return cargs.gamename


def is_game_file(file):
    """Return True if the game is a game file."""

    return file != ALL_PARAMS and file[-4:] == GAME_EXT


def game_files():
    """Return the list of preconfigured games.

    Use man_config.game_files to include games listed in game_dirs
    in the ini file."""

    path = get_path(GAMEPATH)
    files = os.listdir(path)
    return [f for f in files if is_game_file(f)]
