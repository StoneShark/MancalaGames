# -*- coding: utf-8 -*-
"""A multiline message formatter.

This is used for both log messages and popup messages via ui_utils.

Created on Thu May 22 22:03:35 2025
@author: Ann"""

import re
import textwrap

LINE_SEP = '\n\n'

RECOMP = re.compile('\n *')
TEXTFILL = textwrap.TextWrapper(width=50)

def fmsg(message):
    """Format a message.

    message may be a string or list of strings

    Each string might be of the format:
        var = ***this is the first line of text
              a second and subsequent lines will be indented for
              readability
              stars in this example are double quotes***
    or any simple string.

    If a string, format it.
    Otherwise, format each individual string as a paragraph.
    Join them together with two blank lines."""

    if isinstance(message, list):
        return LINE_SEP.join(TEXTFILL.fill(RECOMP.sub(' ', m))
                             for m in message)
    return TEXTFILL.fill(RECOMP.sub(' ', message))
