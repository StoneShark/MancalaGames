# -*- coding: utf-8 -*-
"""These tests create 'no-capture' games to test all of move
without testing the capture.

Special attention is paid to sowing results.

To run any one test with verbose mode (show all of arrays):
pytest.main(['-v', 'test_move_nocapt.py::TestMLAPS_ito_Sow::test_mlaps_basic'])


Created on Sat Mar 25 07:32:54 2023
@author: Ann
"""


# %% imports

import sys

import pytest
pytestmark = pytest.mark.integtest

sys.path.extend(['src'])

import game_interface as gi
from game_interface import WinCond
from game_interface import GameFlags
from game_interface import Direct

import game_constants as gc
import mancala
import utils


# %%

@pytest.mark.filterwarnings("ignore")
class TestCCWSowing:

    @pytest.fixture
    def ccw_game(self):
        game_consts = gc.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_ccw_f0(self, ccw_game):

        # did we build the fixture right?
        assert ccw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                   [4, 4, 4, 4, 4, 4])
        assert len(ccw_game.info.capt_on) == 0

        ccw_game.turn = False
        ccw_game.move(0)
        assert ccw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                   [0, 5, 5, 5, 5, 4])
        assert ccw_game.store == [0, 0]
        assert ccw_game.get_turn() == True

    def test_ccw_f4(self, ccw_game):

        ccw_game.turn = False
        ccw_game.move(4)
        assert ccw_game.board == utils.build_board([4, 4, 4, 5, 5, 5],
                                                   [4, 4, 4, 4, 0, 5])
        assert ccw_game.store == [0, 0]
        assert ccw_game.turn == True

    def test_ccw_t5(self, ccw_game):

        ccw_game.turn = True
        ccw_game.move(5)
        assert ccw_game.board == utils.build_board([4, 5, 5, 5, 5, 0],
                                                   [4, 4, 4, 4, 4, 4])
        assert ccw_game.store == [0, 0]
        assert ccw_game.turn == False

    def test_ccw_t0(self, ccw_game):

        assert ccw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                   [4, 4, 4, 4, 4, 4])
        assert len(ccw_game.info.capt_on) == 0

        ccw_game.turn = True
        ccw_game.move(0)
        assert ccw_game.board == utils.build_board([0, 4, 4, 4, 4, 4],
                                                   [5, 5, 5, 5, 4, 4])
        assert ccw_game.store == [0, 0]
        assert ccw_game.turn == False

    def test_ccw_f1_wrap(self, ccw_game):

        ccw_game.turn = False
        ccw_game.board = utils.build_board([0,  0, 2, 0, 1, 0],
                                           [0, 14, 0, 0, 2, 1])
        ccw_game.store = [14, 14]

        ccw_game.move(1)
        assert ccw_game.board == utils.build_board([1, 1, 3, 1, 2, 1],
                                                   [1, 1, 2, 2, 3, 2])
        assert ccw_game.store == [14, 14]
        assert ccw_game.turn == True


@pytest.mark.filterwarnings("ignore")
class TestCWSowing:

    @pytest.fixture
    def cw_game(self):
        """Game that does little but is CW."""

        game_consts = gc.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.CW),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_cw_f0(self, cw_game):

        # did we build the fixture right?
        assert cw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                  [4, 4, 4, 4, 4, 4])
        assert len(cw_game.info.capt_on) == 0

        cw_game.turn = False
        cw_game.move(1)
        assert cw_game.board == utils.build_board([5, 5, 5, 4, 4, 4],
                                                  [5, 0, 4, 4, 4, 4])
        assert cw_game.store == [0, 0]
        assert cw_game.turn == True

    def test_cw_f4(self, cw_game):

        cw_game.turn = False
        cw_game.move(4)
        assert cw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                  [5, 5, 5, 5, 0, 4])
        assert cw_game.store == [0, 0]
        assert cw_game.turn == True

    def test_ccw_t5(self, cw_game):

        cw_game.turn = True
        cw_game.move(5)
        assert cw_game.board == utils.build_board([4, 4, 4, 4, 4, 0],
                                                  [4, 4, 5, 5, 5, 5])
        assert cw_game.store == [0, 0]
        assert cw_game.turn == False

    def test_ccw_t0(self, cw_game):

        assert cw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                  [4, 4, 4, 4, 4, 4])
        assert len(cw_game.info.capt_on) == 0

        cw_game.turn = True
        cw_game.move(0)
        assert cw_game.board == utils.build_board([0, 5, 5, 5, 5, 4],
                                                  [4, 4, 4, 4, 4, 4])
        assert cw_game.store == [0, 0]
        assert cw_game.turn == False

    def test_cw_f1_wrap(self, cw_game):

        cw_game.turn = False
        cw_game.board = utils.build_board([0,  0, 2, 0, 1, 0],
                                          [0, 14, 0, 0, 2, 1])
        cw_game.store = [14, 14]

        cw_game.move(1)
        assert cw_game.board == utils.build_board([2, 1, 3, 1, 2, 1],
                                                  [2, 1, 1, 1, 3, 2])
        assert cw_game.store == [14, 14]
        assert cw_game.turn == True


class TestCCWSowingStore:

    @pytest.fixture
    def ccw_game(self):
        """Game that does little but is CCW."""

        game_consts = gc.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(stores=True,
                                                sow_direct=Direct.CCW,
                                                sow_own_store=True),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_ccw_f2(self, ccw_game):

        # did we build the fixture right?
        assert ccw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                   [4, 4, 4, 4, 4, 4])
        assert ccw_game.store == [0, 0]
        assert len(ccw_game.info.capt_on) == 0

        ccw_game.turn = False
        cond = ccw_game.move(2)
        assert cond == WinCond.END_STORE
        assert ccw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                   [4, 4, 0, 5, 5, 5])
        assert ccw_game.store == [1, 0]
        assert ccw_game.turn == False

    def test_ccw_f4(self, ccw_game):

        ccw_game.turn = False
        cond = ccw_game.move(4)
        assert cond is None
        assert ccw_game.board == utils.build_board([4, 4, 4, 4, 5, 5],
                                                   [4, 4, 4, 4, 0, 5])
        assert ccw_game.store == [1, 0]
        assert ccw_game.turn == True

    def test_ccw_f4_wrap(self, ccw_game):

        ccw_game.board = utils.build_board([3, 3, 3, 3, 3, 3],
                                           [4, 4, 4, 4, 10, 4])
        ccw_game.turn = False

        cond = ccw_game.move(4)
        assert cond is None
        assert ccw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                   [5, 5, 4, 4, 0, 5])
        assert ccw_game.store == [1, 0]
        assert ccw_game.turn == True

    def test_ccw_t3(self, ccw_game):

        ccw_game.turn = True
        cond = ccw_game.move(3)
        assert cond == WinCond.END_STORE
        assert ccw_game.board == utils.build_board([5, 5, 5, 0, 4, 4],
                                                   [4, 4, 4, 4, 4, 4])
        assert ccw_game.store == [0, 1]
        assert ccw_game.turn == True

    def test_ccw_t1(self, ccw_game):

        ccw_game.turn = True

        cond = ccw_game.move(1)
        assert cond is None
        assert ccw_game.board == utils.build_board([5, 0, 4, 4, 4, 4],
                                                   [5, 5, 4, 4, 4, 4])
        assert ccw_game.store == [0, 1]
        assert ccw_game.turn == False

    def test_ccw_t1_wrap(self, ccw_game):

        ccw_game.board = utils.build_board([4, 10, 4, 4, 4, 4],
                                           [3, 3, 3, 3, 3, 3])
        ccw_game.turn = True

        cond = ccw_game.move(1)
        assert cond is None
        assert ccw_game.board == utils.build_board([5, 0, 4, 4, 5, 5],
                                                   [4, 4, 4, 4, 4, 4])
        assert ccw_game.store == [0, 1]
        assert ccw_game.turn == False


class TestCWSowingStore:

    @pytest.fixture
    def cw_game(self):
        """Game that does little but is CW."""

        game_consts = gc.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(stores=True,
                                                sow_direct=Direct.CW,
                                                sow_own_store=True),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_cw_f4(self, cw_game):

        cw_game.turn = False

        cond = cw_game.move(4)
        assert cond is None
        assert cw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                  [5, 5, 5, 5, 0, 4])
        assert cw_game.store == [0, 0]
        assert cw_game.turn == True

    def test_cw_f1_wrap(self, cw_game):

        cw_game.turn = False

        cw_game.board = utils.build_board([3, 3, 3, 3, 4, 4],
                                          [4, 8, 4, 4, 4, 4])

        cond = cw_game.move(1)
        assert cond == WinCond.END_STORE
        assert cw_game.board == utils.build_board([4, 4, 4, 4, 5, 5],
                                                  [5, 0, 4, 4, 4, 4])
        assert cw_game.store == [1, 0]
        assert cw_game.turn == False

    def test_cw_t0(self, cw_game):

        cw_game.turn = True

        cond = cw_game.move(0)
        assert cond is None
        assert cw_game.board == utils.build_board([0, 5, 5, 5, 5, 4],
                                                  [4, 4, 4, 4, 4, 4])
        assert cw_game.store == [0, 0]
        assert cw_game.turn == False

    def test_cw_t4_wrap(self, cw_game):

        cw_game.turn = True

        cw_game.board = utils.build_board([4, 4, 4, 4, 8, 4],
                                          [3, 3, 3, 3, 4, 4])

        cond = cw_game.move(4)
        assert cond is WinCond.END_STORE
        assert cw_game.board == utils.build_board([4, 4, 4, 4, 0, 5],
                                                  [4, 4, 4, 4, 5, 5])
        assert cw_game.store == [0, 1]
        assert cw_game.turn == True


@pytest.mark.filterwarnings("ignore")
class TestStartHole:

    @pytest.fixture
    def ccw_game(self):
        """Game that does little but is CCW."""

        game_consts = gc.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                min_move=2,
                                flags=GameFlags(sow_start=True,
                                                sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def cw_game(self):
        """Game that does little but is CW."""

        game_consts = gc.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                min_move=2,
                                flags=GameFlags(sow_start=True,
                                                sow_direct=Direct.CW),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_stccw_f0(self, ccw_game):

        # did we build the fixture right?
        assert ccw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                   [4, 4, 4, 4, 4, 4])
        assert len(ccw_game.info.capt_on) == 0

        ccw_game.turn = False
        ccw_game.move(0)
        assert ccw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                   [1, 5, 5, 5, 4, 4])
        assert ccw_game.store == [0, 0]
        assert ccw_game.turn == True

    def test_stccw_f4(self, ccw_game):

        ccw_game.turn = False
        ccw_game.move(4)
        assert ccw_game.board == utils.build_board([4, 4, 4, 4, 5, 5],
                                                   [4, 4, 4, 4, 1, 5])
        assert ccw_game.store == [0, 0]
        assert ccw_game.turn == True

    def test_stcw_f0(self, cw_game):

        # did we build the fixture right?
        assert cw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                  [4, 4, 4, 4, 4, 4])
        assert len(cw_game.info.capt_on) == 0

        cw_game.turn = False
        cw_game.move(1)
        assert cw_game.board == utils.build_board([5, 5, 4, 4, 4, 4],
                                                  [5, 1, 4, 4, 4, 4])
        assert cw_game.store == [0, 0]
        assert cw_game.turn == True

    def test_stcw_f4(self, cw_game):

        cw_game.turn = False
        cw_game.move(4)
        assert cw_game.board == utils.build_board([4, 4, 4, 4, 4, 4],
                                                  [4, 5, 5, 5, 1, 4])
        assert cw_game.store == [0, 0]
        assert cw_game.turn == True


@pytest.mark.filterwarnings("ignore")
class TestSkipStart:

    @pytest.fixture
    def ccw_game(self):
        """Game that does little but is CCW."""

        game_consts = gc.GameConsts(nbr_start=4, holes=6)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(skip_start=True,
                                                sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def cw_game(self):
        """Game that does little but is CW."""

        game_consts = gc.GameConsts(nbr_start=4, holes=6)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(skip_start=True,
                                                sow_direct=Direct.CW),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_ccw_f1_wrap(self, ccw_game):

        ccw_game.turn = False
        ccw_game.board = utils.build_board([0,  0, 2, 0, 1, 0],
                                           [0, 14, 0, 0, 2, 1])
        ccw_game.store = [14, 14]

        ccw_game.move(1)
        assert ccw_game.board == utils.build_board([1, 1, 3, 1, 2, 1],
                                                   [1, 0, 2, 2, 4, 2])
        assert ccw_game.store == [14, 14]
        assert ccw_game.turn == True

    def test_cw_f1_wrap(self, cw_game):

        cw_game.turn = False
        cw_game.board = utils.build_board([0,  0, 2, 0, 1, 0],
                                          [0, 14, 0, 0, 2, 1])
        cw_game.store = [14, 14]

        cw_game.move(1)
        assert cw_game.board == utils.build_board([2, 2, 3, 1, 2, 1],
                                                  [2, 0, 1, 1, 3, 2])
        assert cw_game.store == [14, 14]
        assert cw_game.turn == True

    def test_cw_f1_2xwrap(self, cw_game):

        cw_game.turn = False
        cw_game.board = utils.build_board([0,  0, 2, 0, 1, 0],
                                          [0, 24, 0, 0, 2, 1])
        cw_game.store = [9, 9]

        cw_game.move(1)
        assert cw_game.board == utils.build_board([3, 2, 4, 2, 3, 2],
                                                  [3, 0, 2, 2, 4, 3])
        cw_game.store = [9, 9]
        assert cw_game.turn == True


@pytest.mark.filterwarnings("ignore")
class TestSpSowingNoU:
    """test split sowing without udirect/udir_holes being set."""

    @pytest.fixture
    def sgame_even(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=4)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.SPLIT),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def sgame_odd(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=3)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                udir_holes=[1],
                                flags=GameFlags(sow_direct=Direct.SPLIT,
                                                udirect=True),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_split_dirs_even(self, sgame_even):

        sgame_even.turn = False
        for pos, exp_dir in enumerate([Direct.CW, Direct.CW,
                                       Direct.CCW, Direct.CCW]):
            loc = sgame_even.cts.pos_to_loc(not sgame_even.turn, pos)
            assert sgame_even.deco.get_dir.get_direction(pos, loc) == exp_dir

        sgame_even.turn = True
        for pos, exp_dir in enumerate([Direct.CCW, Direct.CCW,
                                       Direct.CW, Direct.CW]):
            loc = sgame_even.cts.pos_to_loc(not sgame_even.turn, pos)
            assert sgame_even.deco.get_dir.get_direction(pos, loc) == exp_dir

    def test_split_dirs_odd(self, sgame_odd):
        """Cannot have odd holes w/o specifying what happens to them now.
        Direction should be ignored for all but the middle hole."""

        sgame_odd.turn = False
        for pos, exp_dir in enumerate([Direct.CW, Direct.CCW, Direct.CCW]):
            loc = sgame_odd.cts.pos_to_loc(not sgame_odd.turn, pos)
            ans = sgame_odd.deco.get_dir.get_direction((pos, Direct.CCW), loc)
            assert ans == exp_dir

        sgame_odd.turn = True
        for pos, exp_dir in enumerate([Direct.CCW, Direct.CW, Direct.CW]):
            loc = sgame_odd.cts.pos_to_loc(not sgame_odd.turn, pos)
            ans = sgame_odd.deco.get_dir.get_direction((pos, Direct.CW), loc)
            assert ans == exp_dir


@pytest.mark.filterwarnings("ignore")
class TestUdirAll:

    @pytest.fixture
    def uagame(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                udir_holes=[0, 1, 2, 3],

                                flags=GameFlags(sow_direct=Direct.SPLIT,
                                                udirect=True),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_bad_format(self, uagame):

        with pytest.raises(TypeError):
            uagame.move(2)

    def test_f0_cw(self, uagame):

        # did we build the fixture right?
        assert uagame.board == utils.build_board([3, 3, 3, 3],
                                                 [3, 3, 3, 3])
        assert len(uagame.info.capt_on) == 0

        uagame.turn = False
        uagame.move((0, Direct.CW))
        assert uagame.board == utils.build_board([4, 4, 4, 3],
                                                 [0, 3, 3, 3])
        assert uagame.store == [0, 0]
        assert uagame.turn

    def test_f0_ccw(self, uagame):

        uagame.turn = False
        uagame.move((0, Direct.CCW))

        assert uagame.board == utils.build_board([3, 3, 3, 3],
                                                 [0, 4, 4, 4])
        assert uagame.store == [0, 0]
        assert uagame.turn


@pytest.mark.filterwarnings("ignore")
class TestBlocks_ito_Sow:
    """ito = in terms of"""

    @pytest.fixture
    def bgame(self):
        """Game that does little but is CCW."""

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(blocks=True,
                                                rounds=True,
                                                sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    def test_f0(self, bgame):

        bgame.turn = False
        bgame.blocked[2] = True
        bgame.board = utils.build_board([3, 3, 3, 3],
                                        [3, 3, 0, 3])
        bgame.store = [3, 0]
        bgame.move(0)
        assert bgame.board == utils.build_board([3, 3, 3, 4],
                                                [0, 4, 0, 4])


@pytest.mark.filterwarnings("ignore")
class TestMoveunlock_ito_Sow:

    @pytest.fixture
    def mugame(self):
        """Game that does little but is CCW."""

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(moveunlock=True,
                                                sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    def test_f0(self, mugame):

        mugame.turn = False
        mugame.board = utils.build_board([3, 3, 3, 3],
                                         [3, 3, 3, 3])
        mugame.move(0)

        assert mugame.board == utils.build_board([3, 3, 3, 3],
                                                 [0, 4, 4, 4])
        assert mugame.unlocked[0] == True


@pytest.mark.filterwarnings("ignore")
class TestMLAPS_ito_Sow:

    @pytest.fixture
    def game(self):
        """Game that does little but is CCW."""

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(mlaps=True,
                                                sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_mlaps_basic(self, game):

        assert game.board == utils.build_board([3, 3, 3, 3],
                                               [3, 3, 3, 3])
        assert all(game.unlocked)

        game.turn = False
        game.move(0)

        assert game.board == utils.build_board([0, 4, 4, 4],
                                               [1, 5, 5, 1])

    def test_mlaps_lapy(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=6)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(mlaps=True,
                                                sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)

        game.board = utils.build_board([1, 4, 1, 0, 1, 2],
                                       [3, 0, 1, 1, 2, 1])
        game.store = [20, 11]
        game.turn = True
        cond = game.move(1)
        assert cond is None
        assert game.board == utils.build_board([0, 1, 0, 1, 0, 3],
                                               [5, 2, 1, 2, 0, 2])

    def test_mlaps_inf(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=6)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(mlaps=True,
                                                sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)

        game.board = utils.build_board([0, 1, 0, 1, 0, 3],
                                       [5, 2, 1, 2, 0, 2])
        game.store = [20, 11]
        game.turn = False
        cond = game.move(3)
        assert cond == WinCond.ENDLESS


@pytest.mark.filterwarnings("ignore")
class TestPASS_ito_Sow:

    @pytest.fixture
    def game(self):
        """Game that does little but is CCW."""

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(mlaps=True,
                                                sow_direct=Direct.CCW),
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    def test_mlaps_basic(self, game):

        assert game.board == utils.build_board([3, 3, 3, 3],
                                               [3, 3, 3, 3])
        assert all(game.unlocked)

        game.turn = False
        game.move(0)

        assert game.board == utils.build_board([0, 4, 4, 4],
                                               [1, 5, 5, 1])
