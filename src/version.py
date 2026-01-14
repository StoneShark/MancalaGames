# -*- coding: utf-8 -*-
"""Release, build and version information.

Created on Thu Feb 13 07:34:32 2025
@author: Ann"""

import textwrap

VERSION = '1.10.1'

# these are auto filled when the exe is built
DATETIME = 'Wed Jan 14 12:17:59 2026'
BRANCH = 'main'

RELEASE_TEXT = textwrap.dedent(f"""\
                Mancala Games
                License: GPL-3.0   ©Ann Davies 2024-2026
                Version: {VERSION}
                Date: {DATETIME} {BRANCH:>10}""")
