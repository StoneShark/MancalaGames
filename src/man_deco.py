# -*- coding: utf-8 -*-
"""Collect the decorator chains into ManDeco to limit
the number of variables in Mancala.

ManDeco includes operations to allow editing the
deco chain for classes derived from Mancala.

Created on Sat Jun 14 05:52:40 2025
@author: Ann"""


import allowables
import capt_ok
import capturer
import drawer
import end_move
import game_str
import get_direction
import get_moves
import incrementer
import make_child
import new_game
import sower


class ManDeco:
    """Collect the decorator chains into one variable,
    build them all together.

    Decorator chains can save data unique to the game
    on startup/creation, but they should not store
    state data that would be changed during the game.
    Decos are not told about a new game or round
    being started.

    Deco are not told to re-initialized on new game."""

    def __init__(self, game):

        self.new_game = new_game.deco_new_game(game)
        self.allow = allowables.deco_allowable(game)
        self.moves = get_moves.deco_moves(game)
        self.incr = incrementer.deco_incrementer(game)
        self.drawer = drawer.deco_drawer(game)
        self.get_dir = get_direction.deco_dir_getter(game)
        self.sower = sower.deco_sower(game)
        self.ender = end_move.deco_end_move(game)
        self.quitter = end_move.deco_quitter(game)
        self.capt_ok = capt_ok.deco_capt_ok(game)
        self.capturer = capturer.deco_capturer(game)
        self.gstr = game_str.deco_get_string(game)
        self.make_child = make_child.deco_child(game)


    def __str__(self):

        rval = ''
        for dname, dobj in vars(self).items():
            rval += f'{dname}:\n' + str(dobj) + '\n\n'
        return rval


    def replace_deco(self, deco_name, old_class, new_deco):
        """Replace old_class with the new_deco (deco instance)
        in the deco_name chain"""

        deco = getattr(self, deco_name)

        # replacing the head of the deco chain
        if isinstance(deco, old_class):
            new_deco.decorator = deco.decorator
            setattr(self, deco_name, new_deco)
            return

        while (deco.decorator
               and not isinstance(deco.decorator, old_class)):
            deco = deco.decorator
        assert deco.decorator, f"Didn't find ({old_class}) in deco chain."

        new_deco.decorator = deco.decorator.decorator
        deco.decorator = new_deco


    def insert_deco(self, deco_name, post_class, new_deco):
        """Insert the new_deco before the deco of type post_class
         in the deco_name chain."""

        deco = getattr(self, deco_name)

        # inserting new head of the deco chain
        if isinstance(deco, post_class):
            new_deco.decorator = deco
            setattr(self, deco_name, new_deco)
            return

        while (deco.decorator
               and not isinstance(deco.decorator, post_class)):
            deco = deco.decorator
        assert deco.decorator, f"Didn't find ({post_class}) in deco chain."

        new_deco.decorator = deco.decorator
        deco.decorator = new_deco


    def append_deco(self, deco_name, pre_classes, new_deco):
        """Put the new_deco right after any decos in pre_classes.

         This works with optional decos by moving past any
         decos in the pre_classes, and then insterting the
         new_deco before the first deco not in the
         pre_classes list."""

        deco = tdeco = getattr(self, deco_name)
        while isinstance(tdeco, pre_classes):
            deco = tdeco
            tdeco = tdeco.decorator

        if tdeco is deco:
            new_deco.decorator = deco
            setattr(self, deco_name, new_deco)
        else:
            new_deco.decorator = deco.decorator
            deco.decorator = new_deco
