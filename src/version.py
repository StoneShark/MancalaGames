# -*- coding: utf-8 -*-
"""Release, build and version information.

Created on Thu Feb 13 07:34:32 2025
@author: Ann"""

import textwrap

DATETIME = 'Thu Feb 20 11:55:28 2025'
VERSION = '1.7.0'
BRANCH = 'main'

RELEASE_TEXT = textwrap.dedent(f"""\
                Mancala Games
                License: GPL-3.0   ©Ann Davies 2024-2025
                Version: {VERSION} {BRANCH}
                Date: {DATETIME}""")
