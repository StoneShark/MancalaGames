# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 05:28:35 2023
@author: Ann"""


from context import mancala
from context import move_data


def build_board(trow, frow):
    return frow + trow[::-1]


def make_state(board, store=(0, 0), turn=False, **kwargs):
    """Helper function to make game states.
    Don't care about mcount, const > 1 is fine."""

    return mancala.GameState(board=board,
                             store=store,
                             _turn=turn,
                             mcount=25,
                             **kwargs)


def make_get_dir_mdata(game, move, sow_loc):
    """Build move_data suitable for get_direction.
    Needs board, move, sow_loc"""

    mdata = move_data.MoveData(game, move)
    mdata.sow_loc = sow_loc
    return mdata


def make_ender_mdata(game, repeat_turn,  ended):
    """Build a MoveData suitable for the ender."""

    mdata = move_data.MoveData(game, 0)
    mdata.repeat_turn = repeat_turn
    mdata.ended = ended
    return mdata


def make_win_mdata(game, win_cond, winner):
    """Build a MoveData suitable for the win_message."""

    mdata = move_data.MoveData(game, 0)
    mdata.win_cond = win_cond
    mdata.winner = winner
    return mdata
