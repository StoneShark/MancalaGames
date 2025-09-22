# -*- coding: utf-8 -*-
"""Move Data is the data shared among the decorators.

Created on Wed Apr 23 12:19:33 2025
@author: Ann
"""

import format_msg

class MoveData:
    """A place to collect premove and move data.
    This is so the decos can share data.

                   from       from
    Field          Starter    Get Direct   Sower        Capturer       Ender
    -----          -------   -----------   -----        --------       -----
    board                                               note 1
    move
    direct                    fill         input        input
    seeds          fill                    in/update    note 2
    _sow_loc       fill                                 note 3
    cont_sow_loc   property fills          in/update
    lap_nbr                                used

    _capt_start                            output
    capt_loc                               output       in/update
    capt_next                                           fill/working
    capt_change                                         fill
    captured                                            fill

    repeat_turn                                         fill           fill
    ended                                                              fill
    win_cond
    winner                                                             fill

    end_msg                                                            fill
    fin_msg                                                            fill
    user_end

    note 1: board is used to determine if a grand slam is possible
    e.g. there must be seeds on oppside before the turn

    note 2: the number seeds being sown, used in NoSignleSeedCapt

    note 3: the original start location"""

    def __init__(self, game=None, move=None):
        """Parameters are optional to make copy.copy work;
        they really are required."""

        if game:
            self.player = game.turn
            self.board = tuple(game.board)   # pre-move state
        else:
            self.player = None
            self.board = None
        self.move = move
        self.direct = None   # an intentionally invalid direction
        self.seeds = 0

        self._sow_loc = 0
        self.cont_sow_loc = 0   # use by the sower (updated for lap sows)
        self.lap_nbr = 0

        self._capt_start = 0      # if end in store -(store_idx + 1), else loc
        self.capt_loc = 0
        self.capt_next = 0      # used for multiple captures

        self.capt_changed = False    # capt changed state but didn't capture
        self.captured = False       # there was an actual capture
        self.repeat_turn = False

        self.end_msg = ''
        self.fin_msg = False      # end_msg is all that needs to be said

        self.ended = False
        self.win_cond = None
        self.winner = None
        self.user_end = False   # when the user used the End Game command


    def __str__(self):

        string = f"MoveData({self.board}, {self.move}):\n"
        string += f"  direct={self.direct}\n"
        string += f"  move={self.move}\n"
        string += f"  seeds={self.seeds}\n"
        string += f"  sow_loc={self.sow_loc}\n"
        string += f"  cont_sow_loc={self.cont_sow_loc}\n"
        string += f"  lap_nbr={self.lap_nbr}\n"
        string += f"  capt_start={self.capt_start}\n"
        string += f"  capt_loc={self.capt_loc}\n"
        string += f"  capt_next={self.capt_next}\n"
        string += f"  capt_changed={self.capt_changed}\n"
        string += f"  captured={self.captured}\n"
        string += f"  repeat_turn={self.repeat_turn}\n"
        string += f"  end_msg={self.end_msg}\n"
        string += f"  fin_msg={self.fin_msg}\n"
        string += f"  ended={self.ended}\n"
        string += f"  win_cond={self.win_cond}\n"
        string += f"  winner={self.winner}\n"
        string += f"  user_end={self.user_end}"
        return string


    @classmethod
    def pass_move(cls, turn):
        """Create a pass move data for turn,
        suitable for log_turn."""
        pass_data = cls()
        pass_data.player = turn
        pass_data.move = 'PASS'
        return pass_data


    @classmethod
    def make_move(cls, turn, move):
        """Create a skeleton move data for turn,
        suitable for log_turn."""
        move_data = cls()
        move_data.player = turn
        move_data.move = move
        return move_data


    @property
    def sow_loc(self):
        """sow_loc property"""
        return self._sow_loc

    @sow_loc.setter
    def sow_loc(self, value):
        """When sow_loc is set, also set the cont_sow_loc
        for the capturer."""
        self._sow_loc = value
        self.cont_sow_loc = value


    @property
    def capt_start(self):
        """capt_start property."""
        return self._capt_start

    @capt_start.setter
    def capt_start(self, value):
        """When capt_start is set -- only the sower should set!
        Also set the capt_loc for the capturer."""
        self._capt_start = value
        self.capt_loc = value


    @property
    def state(self):
        """Return the mdata state. It must be immutable."""

        return tuple(vars(self).values())

    @state.setter
    def state(self, value):
        """Set the current state to value."""

        for var, val in zip(vars(self).keys(), value):
            setattr(self, var, val)


    def add_end_msg(self, msg, final=False):
        """Possibly add msg to the end_msg.

        If final is not falsy, ignore fin_msg.
        If fin_msg is set and final is not truthy, do not add the msg.
        If final is true, set fin_msg and add the message."""

        if self.fin_msg and not final:
            return
        if final is True:
            self.fin_msg = final

        self.end_msg += format_msg.LINE_SEP if self.end_msg else ''
        self.end_msg += msg
