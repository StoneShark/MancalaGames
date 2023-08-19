# -*- coding: utf-8 -*-
"""A simple game log.
Only gets the string from the game if the logger is active.

Created on Fri Aug 11 15:01:16 2023
@author: Ann"""


import collections as col
import datetime
import sys
import textwrap

import man_path


MOVES = 0
IMPORT = 1
STEPS = 2
INFO = 3
NOTSET = 4


class LogRecord:
    """A log record."""

    def __init__(self, text, lvl=0):

        self.text = text
        self.lvl = lvl


class GameLog:
    """Game Log."""

    def __init__(self):

        self.active = True
        self.live = False
        self.level = MOVES
        self.turn_nbr = -1
        self.log_records = col.deque()
        self.move_start = col.deque()


    def reset(self):
        """Clear the deques."""
        self.log_records.clear()
        self.move_start.clear()
        self.turn_nbr = -1


    def mark_turn(self):
        """Add the turn start location to the move_start."""

        self.move_start.append(len(self.log_records))
        self.turn_nbr += 1


    def add(self, text, lvl):
        """Add the text to the log."""

        if lvl <= self.level:
            self.log_records.append(LogRecord(text, lvl))
            if self.live:
                print(text)


    def output(self, file):
        """Output the log to file."""

        print(f'\n***** Game history. Moves = {len(self.move_start) - 1}',
              file=file)

        for lrec in self.log_records:
            print(lrec.text, file=file)


    def prev(self):
        """Dump the log the from the begining of the previous
        turn (or whatever we can do) to the end."""

        turns = len(self.move_start)
        if turns >= 2:
            start = -2
        elif turns >= 1:
            start = -1
        else:
            start = 0

        print('\n****** Previous Turn')
        for idx in range(self.move_start[start], len(self.log_records)):
            print(self.log_records[idx].text)


game_log = GameLog()


def set_active(active):
    """Set the logger state."""
    game_log.active = active


def set_live(live):
    """Have the logger write to stdio when messages are created."""
    game_log.live = live


def set_level(level):
    """Set the logging level."""
    if 0 <= level <= 4:
        game_log.level = level


def new():
    """Reset the game log."""
    game_log.reset()
    game_log.add('\n*** New game', MOVES)


def turn(game_obj, move_desc=''):
    """Log a turn in the game log (if it's active)."""
    if game_log.active:
        game_log.mark_turn()
        game_log.add(f'\n{game_log.turn_nbr}: ' + move_desc, MOVES)
        game_log.add(str(game_obj), MOVES)


def step(step_name, game_obj):
    """Add a game step to the log."""

    if game_log.active:
        game_log.add(f'\n    {step_name}:', STEPS)
        game_log.add(textwrap.indent(str(game_obj), '    '), STEPS)


def add(text, lvl=NOTSET):
    """Write a message to the game log (if it's active)."""

    if game_log.active:
        game_log.add(text, lvl)


def prev():
    """Dump the previous turn."""
    game_log.prev()


def dump():
    """Print the game log to standard out."""
    game_log.output(sys.stdout)


def save(param_string):
    """Save the log in a standard spot with a date/time stamp
    added to the filename."""

    now = datetime.datetime.now()
    filename = man_path.get_path(
        'logs/log_' + now.strftime('%Y%m%d_%H%M%S') + '.txt')

    with open(filename, 'w', encoding='utf-8') as file:
        print(param_string, file=file)
        game_log.output(file)
