# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 14:21:46 2024
@author: Ann"""


import game_interface as gi

def gen_child_test(game):
    """Generate a test function that will return True
    if a child should be made. Used in the sower to stop
    mlap sowing and the capturer to make children, bulls
    and wegs which use mlaps, but not waldas or tuzdeks
    which don't use mlaps.

    The result is the ANDing of each functions return value."""
    # pylint: disable=too-complex

    def base_case(game, mdata):
        loc = mdata.capt_loc
        return (game.child[loc] is None
                and game.board[loc] == game.info.child_cvt)

    def weg_case(game, mdata):
        loc = mdata.capt_loc
        return (game.board[loc] == game.info.child_cvt
                and game.owner[loc] is (not game.turn))

    def bull_case(game, mdata):
        """Paired capt of child_cvt then child_cvt-1
        or just child_cvt."""
        loc = mdata.capt_loc
        prev = game.deco.incr.incr(loc, mdata.direct.opp_dir())
        return ((game.child[loc] is None
                 and game.board[loc] == game.info.child_cvt - 1
                 and game.child[prev] is None
                 and game.board[prev] == game.info.child_cvt)
                or (game.child[loc] is None
                    and game.board[loc] == game.info.child_cvt))

    def only_opp_side(game, mdata):
        """opp side board (not opp owner as in weg)"""
        return game.cts.opp_side(game.turn, mdata.capt_loc)

    def not_first_hole(_, mdata):
        return mdata.seeds > 1

    if game.info.child_type == gi.ChildType.BULL:
        func_list = [bull_case]
    elif game.info.child_type == gi.ChildType.WEG:
        func_list = [weg_case]
    else:
        func_list = [base_case]

    if game.info.child_rule == gi.ChildRule.OPP_ONLY:
        func_list += [only_opp_side]

    if game.info.child_rule == gi.ChildRule.NOT_1ST_OPP:
        func_list += [only_opp_side]
        func_list += [not_first_hole]


    def child_test(game, mdata):
        # XXXX shouldn't a call to stop_me_child be in the func list

        if game.deco.inhibitor.stop_me_child(game.turn):
            return False
        return all(f(game, mdata) for f in func_list)

    return child_test
