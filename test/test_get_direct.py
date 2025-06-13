# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 09:48:59 2023
@author: Ann"""

import itertools as it

import pytest
pytestmark = pytest.mark.unittest

import utils
from context import game_constants as gconsts
from context import game_info as gi
from context import mancala

from game_info import Direct


# %%

TEST_COVERS = ['src\\get_direction.py']

CW = Direct.CW
CCW = Direct.CCW


# %%

class TestGetDirection:


    @pytest.mark.parametrize('holes, start, direct, exp_dir',
                             [
                              (3, 0, Direct.CW, Direct.CW),
                              (3, 2, Direct.CW, Direct.CW),
                              (3, 3, Direct.CW, Direct.CW),
                              (3, 4, Direct.CW, Direct.CW),
                              (3, 5, Direct.CW, Direct.CW),

                              (4, 0, Direct.CW, Direct.CW),
                              (4, 3, Direct.CW, Direct.CW),
                              (4, 4, Direct.CW, Direct.CW),
                              (4, 5, Direct.CW, Direct.CW),
                              (4, 7, Direct.CW, Direct.CW),

                              (3, 0, Direct.CCW, Direct.CCW),
                              (3, 2, Direct.CCW, Direct.CCW),
                              (3, 3, Direct.CCW, Direct.CCW),
                              (3, 4, Direct.CCW, Direct.CCW),
                              (3, 5, Direct.CCW, Direct.CCW),

                              (4, 0, Direct.CCW, Direct.CCW),
                              (4, 3, Direct.CCW, Direct.CCW),
                              (4, 4, Direct.CCW, Direct.CCW),
                              (4, 5, Direct.CCW, Direct.CCW),
                              (4, 7, Direct.CCW, Direct.CCW),

                              (3, 0, Direct.SPLIT, Direct.CW),
                              (3, 1, Direct.SPLIT, None),  # None stuffed below
                              (3, 2, Direct.SPLIT, Direct.CCW),
                              (3, 3, Direct.SPLIT, Direct.CW),
                              (3, 4, Direct.SPLIT, None),  # None stuffed below
                              (3, 5, Direct.SPLIT, Direct.CCW),

                              (4, 0, Direct.SPLIT, Direct.CW),
                              (4, 1, Direct.SPLIT, Direct.CW),
                              (4, 2, Direct.SPLIT, Direct.CCW),
                              (4, 3, Direct.SPLIT, Direct.CCW),
                              (4, 4, Direct.SPLIT, Direct.CW),
                              (4, 5, Direct.SPLIT, Direct.CW),
                              (4, 6, Direct.SPLIT, Direct.CCW),
                              (4, 7, Direct.SPLIT, Direct.CCW),

                              (4, 0, Direct.TOCENTER, Direct.CCW),
                              (4, 1, Direct.TOCENTER, Direct.CCW),
                              (4, 2, Direct.TOCENTER, Direct.CW),
                              (4, 3, Direct.TOCENTER, Direct.CW),
                              (4, 4, Direct.TOCENTER, Direct.CCW),
                              (4, 5, Direct.TOCENTER, Direct.CCW),
                              (4, 6, Direct.TOCENTER, Direct.CW),
                              (4, 7, Direct.TOCENTER, Direct.CW),
                              ])
    def test_common(self, holes, start, direct, exp_dir):
        """Stuff None in for udir moves, it should only be
        used if the hole is in udir_holes."""

        udir_holes = []
        if direct == Direct.SPLIT and holes == 3:
            udir_holes = [1]

        game_consts = gconsts.GameConsts(nbr_start=4, holes=holes)
        game_info = gi.GameInfo(capt_on=[2],
                                sow_direct=direct,
                                udir_holes=udir_holes,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        move = start
        if direct == Direct.SPLIT and holes == 3:
            move = (game_consts.loc_to_left_cnt(start), None)

        mdata = utils.make_get_dir_mdata(game, move, start)
        assert game.deco.get_dir.get_direction(mdata) == exp_dir


    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.parametrize('holes, start, direct, udir_holes, exp_dir',
                             [
                              (4, 0, Direct.CW, [3], Direct.CW),  # 0
                              (4, 3, Direct.CW, [3], None),
                              (4, 4, Direct.CW, [3], Direct.CW),
                              (4, 7, Direct.CW, [3], None),

                              (4, 0, Direct.CCW, [3], Direct.CCW),  # 4
                              (4, 3, Direct.CCW, [3], None),
                              (4, 4, Direct.CCW, [3], Direct.CCW),
                              (4, 7, Direct.CCW, [3], None),

                              (4, 0, Direct.SPLIT, [3], Direct.CW), # 8
                              (4, 3, Direct.SPLIT, [3], None),
                              (4, 4, Direct.SPLIT, [3], Direct.CW),
                              (4, 7, Direct.SPLIT, [3], None),

                              (3, 5, Direct.SPLIT, [0, 1, 2], None),  # 12
                              ],
                             ids= [f'case_{cnbr}' for cnbr in range(13)])
    def test_not_middle(self, holes, start, direct, udir_holes, exp_dir):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=holes)
        game_info = gi.GameInfo(capt_on=[2],
                                sow_direct=direct,
                                udir_holes=udir_holes,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        move = (game_consts.loc_to_left_cnt(start), None)
        mdata = utils.make_get_dir_mdata(game, move, start)

        assert game.deco.get_dir.get_direction(mdata) == exp_dir


    @pytest.mark.filterwarnings("ignore")
    @pytest.mark.parametrize('holes, start, direct, udir_holes, exp_dir',
                             [
                              (4, 0, Direct.CW, [3], Direct.CW),  # 0
                              (4, 3, Direct.CW, [3], None),
                              (4, 4, Direct.CW, [3], Direct.CW),
                              (4, 7, Direct.CW, [3], None),

                              (4, 0, Direct.CCW, [3], Direct.CCW),  # 4
                              (4, 3, Direct.CCW, [3], None),
                              (4, 4, Direct.CCW, [3], Direct.CCW),
                              (4, 7, Direct.CCW, [3], None),

                              (4, 0, Direct.SPLIT, [3], Direct.CW), # 8
                              (4, 3, Direct.SPLIT, [3], None),
                              (4, 4, Direct.SPLIT, [3], Direct.CW),
                              (4, 7, Direct.SPLIT, [3], None),

                              (3, 5, Direct.SPLIT, [0, 1, 2], None),  # 12
                              ],
                             ids= [f'case_{cnbr}' for cnbr in range(13)])
    def test_no_sides(self, holes, start, direct, udir_holes, exp_dir):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=holes)
        game_info = gi.GameInfo(capt_on=[2],
                                no_sides=True,
                                stores=True,
                                sow_direct=direct,
                                udir_holes=udir_holes,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        move = (start < holes, game_consts.loc_to_left_cnt(start), None)
        mdata = utils.make_get_dir_mdata(game, move, start)

        assert game.deco.get_dir.get_direction(mdata) == exp_dir


    @pytest.mark.parametrize('turn', [True, False])
    @pytest.mark.parametrize('moves',
                             [
                              (gi.MoveTpl(2, Direct.CW), Direct.CW,
                               gi.MoveTpl(2, None), Direct.CCW,
                               gi.MoveTpl(2, None), Direct.CW,
                               gi.MoveTpl(2, None), Direct.CCW),

                              (gi.MoveTpl(2, Direct.CCW), Direct.CCW,
                               gi.MoveTpl(2, None), Direct.CW,
                               gi.MoveTpl(2, Direct.CW), Direct.CCW,
                               gi.MoveTpl(2, Direct.CCW), Direct.CW),

                              (gi.MoveTpl(True, 2, Direct.CW), Direct.CW,
                               gi.MoveTpl(False, 2, None), Direct.CCW,
                               gi.MoveTpl(False, 2, None), Direct.CW,
                               gi.MoveTpl(True, None), Direct.CCW),

                              (gi.MoveTpl(True, 2, Direct.CCW), Direct.CCW,
                               gi.MoveTpl(True, 2, None), Direct.CW,
                               gi.MoveTpl(True, 2, Direct.CW), Direct.CCW,
                               gi.MoveTpl(True, 2, Direct.CCW), Direct.CW),

                              ])
    def test_players_alt(self, turn, moves):
        """After the first move, the direction in the move doesn't
        matter.
        Test both MoveTpl lengths.
        The starting play does not matter, but test it."""

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                sow_direct=Direct.PLAYALTDIR,
                                no_sides=len(moves[0]) == 3,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn

        for move_nbr, (move, edir) in enumerate(it.batched(moves, 2)):
            game.mcount = move_nbr + 1
            game.turn = not game.turn

            mdata = utils.make_get_dir_mdata(game, move, 1)
            assert game.deco.get_dir.get_direction(mdata) == edir



    @pytest.mark.parametrize('turn', [True, False])
    @pytest.mark.parametrize('moves',
                             [
                              (gi.MoveTpl(2, Direct.CW), Direct.CW,
                               gi.MoveTpl(2, None), Direct.CCW,
                               gi.MoveTpl(2, None), Direct.CW,
                               gi.MoveTpl(2, None), Direct.CCW,
                               gi.MoveTpl(2, Direct.CCW), Direct.CCW,  # reset move_nbr here
                               gi.MoveTpl(2, None), Direct.CW,
                               gi.MoveTpl(2, Direct.CW), Direct.CCW,
                               gi.MoveTpl(2, Direct.CCW), Direct.CW),

                              (gi.MoveTpl(True, 2, Direct.CW), Direct.CW,
                               gi.MoveTpl(False, 2, None), Direct.CCW,
                               gi.MoveTpl(False, 2, None), Direct.CW,
                               gi.MoveTpl(True, None), Direct.CCW,
                               gi.MoveTpl(True, 2, Direct.CCW), Direct.CCW,  # reset move_nbr here
                               gi.MoveTpl(True, 2, None), Direct.CW,
                               gi.MoveTpl(True, 2, Direct.CW), Direct.CCW,
                               gi.MoveTpl(True, 2, Direct.CCW), Direct.CW),

                              ])
    def test_players_alt_reset(self, turn, moves):
        """test that the directions are collected again when
        mcount is reset to 1."""

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                sow_direct=Direct.PLAYALTDIR,
                                no_sides=len(moves[0]) == 3,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn

        for move_nbr, (move, edir) in enumerate(it.batched(moves, 2)):
            game.mcount = (move_nbr % 4) + 1
            game.turn = not game.turn

            mdata = utils.make_get_dir_mdata(game, move, 1)
            assert game.deco.get_dir.get_direction(mdata) == edir


    @pytest.mark.parametrize('turn', [False, True])
    def test_even_odd_dirs(self, turn):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(capt_on=[2],
                                sow_direct=Direct.EVEN_ODD_DIR,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = turn
        game.board = [2, 3, 4, 4, 3, 2]
        edir = [CW, CCW, CW, CW, CCW, CW]

        for move, sow_loc in zip(range(3),
                                 range(3, 6) if turn else range(3)):

            mdata = utils.make_get_dir_mdata(game, move, sow_loc)
            assert game.deco.get_dir.get_direction(mdata) == edir[sow_loc]
