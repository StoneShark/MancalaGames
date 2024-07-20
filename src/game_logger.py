# -*- coding: utf-8 -*-
"""A simple game log.
Only gets the string from the game if the logger is active.

Created on Fri Aug 11 15:01:16 2023
@author: Ann"""

import collections
import datetime
import enum
import sys
import textwrap

import man_path


class LogMode(enum.Enum):
    """The states that the logger may be in."""

    OFF = 0
    ACTIVE = 1
    ACT_IN_AI = 2  # active but supressed for AI
    SIMULATE = 3   # active but move all log items to SIMUL (sort of)


    def do_log(self):
        """Is there an active logging mode."""
        return self in {self.ACTIVE, self.SIMULATE}



class GameLog:
    """A simple game log that can keep track of where turns start,
    knows about turns and moves, and supports logging steps within
    moves.  The game object is passed in, it's "str" is printed in
    the log."""

    # Log levels
    MOVE = 0
    IMPORT = 1
    STEP = 2
    INFO = 3
    DETAIL = 4
    SIMUL = 5
    SHOWALL = SIMUL


    def __init__(self):

        self._state = LogMode.ACTIVE
        self._live = False
        self._level = GameLog.MOVE
        self._sim_count = 0   # count of nested set_simulate calls

        self._log_records = collections.deque()
        self._move_start = collections.deque()


    @property
    def active(self):
        """Get active property."""
        return self._state == LogMode.ACTIVE

    @active.setter
    def active(self, value):
        """Set logging active -- value a boolean."""

        if value is True and self._state in (LogMode.OFF, LogMode.ACTIVE):
            self._state = LogMode.ACTIVE

        elif value is False and self._state in (LogMode.OFF, LogMode.ACTIVE):
            self._state = LogMode.OFF

        else:
            print(f'Ignoring log active set prop (_state={self._state})')


    @property
    def live(self):
        """Get live property."""
        return self._live

    @live.setter
    def live(self, value):
        """Set live."""
        self._live = value

    @property
    def level(self):
        """Get level property."""
        return self._level

    @level.setter
    def level(self, value):
        """Set level."""
        if 0 <= value <= self.SIMUL:
            self._level = value


    def new(self):
        """Reset the game log."""

        self._log_records.clear()
        self._move_start.clear()
        self._sim_count = 0
        self.add('\n*** New game', GameLog.MOVE)


    def _add(self, text, lvl):
        """Already know the log is active.
        Add the text to the log.
        If simulate is on set the log lvl to SIMUL"""

        if self._state == LogMode.SIMULATE:
            lvl = self.SIMUL

        if lvl <= self._level:
            self._log_records.append(text)
            if self._live:
                print(text)


    def add(self, text, lvl=DETAIL):
        """Check if active, if so call _add"""

        if self._state.do_log():
            self._add(text, lvl)


    def add_ai(self, text, lvl=DETAIL):
        """Call during ACT_IN_AI to force an entry to be
        added to the log.  Use sparingly!"""

        if self._state in {LogMode.ACT_IN_AI,
                           LogMode.ACTIVE}:
            self._add(text, lvl)


    def _mark_turn(self):
        """Add the turn start location to the move_start."""

        self._move_start.append(len(self._log_records))


    def turn(self, turn_nbr, move_desc, game_obj):
        """Log a turn in the game log (if it's active)."""
        if self._state.do_log():
            self._mark_turn()
            self._add(f'\n{turn_nbr}: ' + move_desc, GameLog.MOVE)
            self._add(str(game_obj), GameLog.MOVE)


    def step(self, step_name, game_obj=None, lvl=None):
        """Add a game step to the log."""

        if self._state.do_log():
            lvl = lvl if lvl else GameLog.STEP

            if not game_obj:
                self._add(f'\n    {step_name}.', GameLog.STEP)

            elif lvl > GameLog.STEP and lvl > self._level:
                self._add(f'    {step_name}.', GameLog.STEP)

            else:
                self._add(f'\n    {step_name}:', lvl)
                self._add(textwrap.indent(str(game_obj), '    '), lvl)


    def prev(self):
        """Dump the log the from the begining of the previous
        turn (or whatever we can do) to the end."""

        turns = len(self._move_start)
        if turns >= 2:
            start = -2
        elif turns >= 1:
            start = -1
        else:
            print('No moves')
            return

        print('\n****** Previous Turn')
        for idx in range(self._move_start[start], len(self._log_records)):
            print(self._log_records[idx])


    def _output(self, file):
        """Output the log to file."""

        print(f'\n***** Game history. Moves = {len(self._move_start) - 1}',
              file=file)

        for lrec in self._log_records:
            print(lrec, file=file)


    def dump(self):
        """Print the game log to standard out."""
        self._output(sys.stdout)


    def save(self, param_string):
        """Save the log in a standard spot with a date/time stamp
        added to the filename."""

        now = datetime.datetime.now()
        dir_name = man_path.get_path('logs')
        filename = dir_name + '/' + now.strftime('%Y%m%d_%H%M%S') + '.txt'


        with open(filename, 'w', encoding='utf-8') as file:
            print(param_string, file=file)
            self._output(file)


    def set_simulate(self):
        """While in SIMULATE mode change the logging level
        of any logged text during simulated ops to SIMUL.
        Use this when moves are being simulated to test
        game conditions, e.g. must share, grand slam not
        legal.

        If set_simulate calls are nested, the mode will
        remain active the same number of calls have been
        made to clear_simulate.

        Do not use this for AI moves."""

        if self._state == LogMode.ACTIVE:
            self._state = LogMode.SIMULATE
            self.add('*** SIMULATE STARTED', self.SIMUL)

        if self._state == LogMode.SIMULATE:
            self._sim_count += 1


    def clear_simulate(self):
        """Turn simulate mode off."""

        if self._state == LogMode.SIMULATE:
            self._sim_count -= 1

            if not self._sim_count:
                self._state = LogMode.ACTIVE
                self.add('*** SIMULATE STOPPED', self.SIMUL)


    def set_ai_mode(self):
        """When in AI mode most output is prevented."""

        if self._state == LogMode.ACT_IN_AI:
            raise NotImplementedError(
                "Nested set_ai_mode calls not supported.")

        if self._state == LogMode.ACTIVE:
            self._state = LogMode.ACT_IN_AI


    def clear_ai_mode(self):
        """Turn simulate mode off."""

        if self._state == LogMode.ACT_IN_AI:
            self._state = LogMode.ACTIVE


# the global game_log

game_log = GameLog()
