# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 05:28:35 2023
@author: Ann"""


from context import mancala


def build_board(trow, frow):
    return frow + trow[::-1]


def make_state(board, store, turn=False, **kwargs):
    """Helper function to make game states.
    Don't care about mcount, const > 1 is fine."""

    return mancala.GameState(board=board,
                             store=store,
                             _turn=turn,
                             mcount=25,
                             **kwargs)
