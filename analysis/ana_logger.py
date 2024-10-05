# -*- coding: utf-8 -*-
"""Convinience functions for the analysis software logger.
It adds date/timestamp to all messages and can
output to both the console and a file.

use logger.info for output

Created on Sat Oct  5 13:51:41 2024
@author: Ann"""

import logging

def config(logger, outfile):
    """Configure the logger to do a brief date/timestamp,
    logger name, and message.
    If outfile, create a second handler to output messages
    to a log file."""

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)s: %(message)s',
                                  datefmt='%m-%d %H:%M')

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    if outfile:
        ofile = logging.FileHandler(outfile)
        ofile.setFormatter(formatter)
        logger.addHandler(ofile)

    logger.info('*** Log Start ***')


def close(logger):
    """Close the handlers and remove them from the logger."""

    logger.info('*** Log End ***')
    handlers = logger.handlers[:]
    for handler in handlers:
        logger.removeHandler(handler)
        handler.close()
