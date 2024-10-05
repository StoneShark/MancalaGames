# -*- coding: utf-8 -*-
"""Translate the filename into an absolute path.
Determine where the filename might be.
Use for directories for logs and writing game prop file.

Created on Sat Aug 19 08:32:38 2023
@author: Ann"""

import os.path

SRC = 'src'


def get_path(filename):
    """Provide compatibility between different ways the
    software can be run."""

    places = ['.', '..', 'src', '../src', 'docs', '../docs', 'help']

    for dirname in places:
        pathname = os.path.join(dirname, filename)
        if os.path.isfile(pathname) or os.path.isdir(pathname):
            break

    else:
        raise FileNotFoundError(f"Can't file {filename}.")

    return os.path.abspath(pathname)
