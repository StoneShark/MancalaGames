# -*- coding: utf-8 -*-
"""Release, build and version information.

Created on Thu Feb 13 07:34:32 2025
@author: Ann"""

import textwrap

VERSION = '1.8.9'

# these are auto filled when the exe is built
DATETIME = 'Wed Jul 30 07:53:05 2025'
BRANCH = 'develop'

RELEASE_TEXT = textwrap.dedent(f"""\
                Mancala Games
                License: GPL-3.0   ©Ann Davies 2024-2025
                Version: {VERSION}
                Date: {DATETIME} {BRANCH:>10}""")
