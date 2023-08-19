# -*- coding: utf-8 -*-
"""Translate the filename into an absolute path.

Created on Sat Aug 19 08:32:38 2023
@author: Ann"""

import os.path

SRC = 'src'

def get_path(filename):
    """Provide compatibility between code run directly
    (in the source dir) and the exe. If running from
    the source dir, remove the src from the path.
    Otherwise the data files are parallel to the exe."""

    file_dirn, _ = os.path.split(__file__)
    parent_dirn, dirn = os.path.split(file_dirn)

    if dirn == SRC:
        pathname = os.path.join(parent_dirn, filename)
    else:
        pathname = os.path.join(os.getcwd(), filename)

    return os.path.abspath(pathname)
