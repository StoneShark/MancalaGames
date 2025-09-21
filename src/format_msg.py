# -*- coding: utf-8 -*-
"""A multiline message formatter.

This is used for both log messages and popup messages via ui_utils.

Created on Thu May 22 22:03:35 2025
@author: Ann"""

import re
import textwrap

NL = '\n'
LINE_SEP = '\n\n'

PRE_TAG = '<pre'
PRE_END = '</pre'

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


def build_paras(text, html=False):
    """Build paragraphs and yield them one at a time

    \n\n are paragraphs \n are not.

    <pre... and </pre... braket preformated text
    if html is true, include the tags; if false do not."""

    para = ''
    fix_form = False

    for line in text.split(NL):

        if line[:4] == PRE_TAG:
            yield para
            fix_form = True
            if html:
                para = line + NL
            else:
                para = ''

        elif line[:5] == PRE_END:
            if html:
                yield para + line + NL
            else:
                yield para + NL
            fix_form = False
            para = ''

        elif fix_form:
            if html:
                nline = line.replace('<', '&lt;')
                nline = nline.replace('>', '&gt;')
                para += nline + NL
            else:
                para += line + NL

        elif not line.rstrip():
            yield para
            para = ''

        else:
            para += line + ' '

    if para:
        yield para + NL
