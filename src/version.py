# -*- coding: utf-8 -*-
"""Release, build and version information.

Created on Thu Feb 13 07:34:32 2025
@author: Ann"""

import textwrap

VERSION = '1.9.1'

# these are auto filled when the exe is built
DATETIME = 'Fri Sep 19 11:16:03 2025'
BRANCH = 'develop'

RELEASE_TEXT = textwrap.dedent(f"""\
                Mancala Games
                License: GPL-3.0   ©Ann Davies 2024-2025
                Version: {VERSION}
                Date: {DATETIME} {BRANCH:>10}""")
