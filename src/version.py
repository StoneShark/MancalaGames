# -*- coding: utf-8 -*-
"""Release, build and version information.

Created on Thu Feb 13 07:34:32 2025
@author: Ann"""

import textwrap

VERSION = '1.8.5'

# these are auto filled when the exe is built
DATETIME = 'Sat May  3 13:45:39 2025'
BRANCH = 'main'

RELEASE_TEXT = textwrap.dedent(f"""\
                Mancala Games
                License: GPL-3.0   ©Ann Davies 2024-2025
                Version: {VERSION}
                Date: {DATETIME} {BRANCH:>10}""")
