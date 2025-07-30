# -*- coding: utf-8 -*-
"""Translate the filename into an absolute path.
Determine where the filename might be.
Use for directories for logs and writing game prop file.

Created on Sat Aug 19 08:32:38 2023
@author: Ann"""

import os.path


def get_path(filename, no_error=False):
    """Provide compatibility between different ways the
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


def find_gamefile(gname):
    """Look in a few logical places for the file."""

    if os.path.isfile(gname):
        return gname

    places = ['./' + gname,
              './' + gname + '.txt',
              './GameProps/' + gname,
              './GameProps/' + gname + '.txt',
              '../GameProps/' + gname,
              '../GameProps/' + gname + '.txt']

    for fname in places:
        if os.path.isfile(fname):
            return fname

    raise FileNotFoundError(f"Can't find file {gname}.")
