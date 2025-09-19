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
WIDEFILL = textwrap.TextWrapper(width=75)

def fmsg(message, wide=False):
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
        if wide:
            new_text = [WIDEFILL.fill(RECOMP.sub(' ', m)) for m in message]
        else:
            new_text = [TEXTFILL.fill(RECOMP.sub(' ', m)) for m in message]
        return LINE_SEP.join(new_text)

    if wide:
        return WIDEFILL.fill(RECOMP.sub(' ', message))
    return TEXTFILL.fill(RECOMP.sub(' ', message))


def build_paras(text):
    """Build paragraphs. \n\n are paragraphs \n are not."""

    text = text.replace(LINE_SEP, '@@@@')
    text = text.replace('\n', ' ')
    text = text.replace('@@@@', '\n')
    return text
