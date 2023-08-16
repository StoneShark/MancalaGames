# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 15:00:05 2023

@author: Ann
"""

# %% imports

import sys

import pytest

sys.path.extend(['src'])

import capturer
import game_constants as gc
import game_interface as gi
from game_interface import GameFlags
from game_interface import Direct
from game_interface import GrandSlam
import mancala
import utils


# %%

T = True
F = False
N = None

# %%


class TestNoCapts:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                flags=GameFlags(stores=True))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_no_capt_warn(self):

        with pytest.warns(UserWarning):
            gi.GameInfo(nbr_holes=3,
                        flags=GameFlags(stores=True))

    @pytest.mark.filterwarnings("ignore")
    def test_no_capt(self, game):
        game.board = utils.build_board([3, 3, 3, 3],
                                       [0, 4, 4, 2])
        game.store = [1, 1]
        game.capture_seeds(3, Direct.CCW)
        assert game.board == utils.build_board([3, 3, 3, 3],
                                               [0, 4, 4, 2])
        assert game.store == [1, 1]


class TestSingleCapts:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[4],
                                flags=GameFlags(stores=True))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_no_capt(self, game):
        game.board = utils.build_board([3, 3, 3, 3],
                                       [0, 4, 4, 2])
        game.store = [1, 1]
        game.capture_seeds(3, Direct.CCW)
        assert game.board == utils.build_board([3, 3, 3, 3],
                                               [0, 4, 4, 2])
        assert game.store == [1, 1]


    def test_capt(self, game):
        game.board = utils.build_board([3, 3, 3, 3],
                                       [0, 4, 4, 4])
        game.store = [0, 0]
        game.capture_seeds(3, Direct.CCW)
        assert game.board == utils.build_board([3, 3, 3, 3],
                                               [0, 4, 4, 0])
        assert game.store == [4, 0]



class TestRevDirCapts:

    @pytest.fixture
    def ccw_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)
        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                flags=GameFlags(sow_direct=Direct.CCW,
                                                multicapt=True,
                                                stores=True))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_cap0(self, ccw_game):

        # did we build the fixture right?
        assert ccw_game.board == utils.build_board([3, 3, 3, 3],
                                                   [3, 3, 3, 3])
        assert len(ccw_game.info.capt_on) == 1

        ccw_game.move(0)
        assert ccw_game.board == utils.build_board([3, 3, 3, 3],
                                                   [0, 4, 4, 4])
        assert ccw_game.store == [0, 0]

    def test_cap1(self, ccw_game):
        ccw_game.board = utils.build_board([3, 3, 3, 3],
                                           [3, 3, 3, 1])
        ccw_game.store = [1, 1]
        ccw_game.move(0)
        assert ccw_game.board == utils.build_board([3, 3, 3, 3],
                                                   [0, 4, 4, 0])
        assert ccw_game.store == [3, 1]

    def test_cap_more(self, ccw_game):
        ccw_game.board = utils.build_board([3, 3, 3, 3],
                                           [3, 1, 1, 1])
        ccw_game.store = [3, 3]
        ccw_game.move(0)
        assert ccw_game.board == utils.build_board([3, 3, 3, 3],
                                                   [0, 0, 0, 0])
        assert ccw_game.store == [9, 3]


class TestSameDirCapts:

    @pytest.fixture
    def ccw_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(name='my name',
                                nbr_holes=game_consts.holes,
                                capt_on=[2],
                                flags=GameFlags(sow_direct=Direct.CCW,
                                                capsamedir=True,
                                                multicapt=True,
                                                stores=True))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_cap0(self, ccw_game):

        # did we build the fixture right?
        assert ccw_game.board == utils.build_board([3, 3, 3, 3],
                                                   [3, 3, 3, 3])
        assert len(ccw_game.info.capt_on) == 1

        ccw_game.move(0)
        assert ccw_game.board == utils.build_board([3, 3, 3, 3],
                                                   [0, 4, 4, 4])
        assert ccw_game.store == [0, 0]

    def test_cap1(self, ccw_game):
        ccw_game.board = utils.build_board([3, 3, 3, 3],
                                           [3, 3, 3, 1])
        ccw_game.store = [1, 1]
        ccw_game.move(0)
        assert ccw_game.board == utils.build_board([3, 3, 3, 3],
                                                   [0, 4, 4, 0])
        assert ccw_game.store == [3, 1]

    def test_cap_more(self, ccw_game):
        ccw_game.board = utils.build_board([3, 3, 2, 2],
                                           [3, 3, 3, 1])
        ccw_game.store = [2, 2]
        ccw_game.move(0)
        assert ccw_game.board == utils.build_board([3, 3, 0, 0],
                                                   [0, 4, 4, 0])
        assert ccw_game.store == [8, 2]


class TestOppSideCapts:

    @pytest.fixture
    def ccw_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(name='my name',
                                nbr_holes=game_consts.holes,
                                capt_on=[2],
                                flags=GameFlags(mustpass=True,
                                                sow_direct=Direct.CCW,
                                                oppsidecapt=True,
                                                multicapt=True,
                                                stores=True))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_cap0(self, ccw_game):
        ccw_game.board = utils.build_board([3, 3, 3, 3],
                                           [3, 3, 3, 1])
        ccw_game.store = [1, 1]
        ccw_game.move(0)
        assert ccw_game.board == utils.build_board([3, 3, 3, 3],
                                                   [0, 4, 4, 2])
        assert ccw_game.store == [1, 1]

    def test_cap_more(self, ccw_game):
        ccw_game.board = utils.build_board([1, 1, 1, 1],
                                           [3, 3, 3, 3])
        ccw_game.store = [4, 4]
        ccw_game.move(3)
        assert ccw_game.board == utils.build_board([1, 0, 0, 0],
                                                   [3, 3, 3, 0])
        assert ccw_game.store == [10, 4]

    def test_cap_not_mine(self, ccw_game):
        ccw_game.board = utils.build_board([1, 1, 1, 1],
                                           [3, 3, 5, 1])
        ccw_game.store = [4, 4]
        ccw_game.move(2)
        assert ccw_game.board == utils.build_board([0, 0, 0, 0],
                                                   [3, 3, 0, 2])
        assert ccw_game.store == [12, 4]


class TestEvenCapts:

    @pytest.fixture
    def ccw_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(name='my name',
                                nbr_holes=game_consts.holes,
                                flags=GameFlags(mustpass=True,
                                                sow_direct=Direct.CCW,
                                                evens=True,
                                                multicapt=True,
                                                stores=True))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_cap0(self, ccw_game):
        ccw_game.board = utils.build_board([3, 3, 3, 3],
                                           [3, 3, 3, 2])
        ccw_game.store = [0, 1]
        ccw_game.move(0)
        assert ccw_game.board == utils.build_board([3, 3, 3, 3],
                                                   [0, 4, 4, 3])
        assert ccw_game.store == [0, 1]

    def test_cap_more(self, ccw_game):
        ccw_game.board = utils.build_board([3, 3, 3, 3],
                                           [3, 3, 3, 1])
        ccw_game.store = [1, 1]
        ccw_game.move(0)
        assert ccw_game.board == utils.build_board([3, 3, 3, 3],
                                                   [0, 0, 0, 0])
        assert ccw_game.store == [11, 1]

    def test_cap_bothsides(self, ccw_game):
        """Confirm capture of start."""
        ccw_game.board = utils.build_board([2, 2, 2, 2],
                                           [3, 3, 0, 2])
        ccw_game.store = [4, 4]
        ccw_game.capture_seeds(7, Direct.CCW)
        assert ccw_game.board == utils.build_board([0, 0, 0, 0],
                                                   [3, 3, 0, 0])
        assert ccw_game.store == [14, 4]


class TestLockCapts:

    @pytest.fixture
    def cw_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(name='my name',
                                nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.CW,
                                                evens=True,
                                                moveunlock=True,
                                                multicapt=True,
                                                stores=True))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_locked(self, cw_game):

        assert cw_game.unlocked[6] == False
        assert cw_game.unlocked[1] == False
        assert cw_game.board == utils.build_board([3, 3, 3, 3],
                                                  [3, 3, 3, 3])

        cw_game.move(1)
        assert cw_game.board == utils.build_board([4, 4, 3, 3],
                                                  [4, 0, 3, 3])
        assert cw_game.store == [0, 0]
        assert cw_game.unlocked[6] == False
        assert cw_game.unlocked[1] == True

    def test_unlocked(self, cw_game):

        assert cw_game.board == utils.build_board([3, 3, 3, 3],
                                                  [3, 3, 3, 3])
        cw_game.unlocked[6] = True

        cw_game.move(1)
        assert cw_game.board == utils.build_board([4, 0, 3, 3],
                                                  [4, 0, 3, 3])
        assert cw_game.store == [4, 0]
        assert cw_game.unlocked[1] == True


class TestCrossCapts:

    @pytest.fixture
    def cw_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(name='my name',
                                nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.CW,
                                                crosscapt=True,
                                                stores=True))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def cw_xcp_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(name='my name',
                                nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.CW,
                                                crosscapt=True,
                                                xcpickown=True,
                                                stores=True)
                                )

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    def test_nocapt(self, cw_game):

        assert cw_game.board == utils.build_board([3, 3, 3, 3],
                                                  [3, 3, 3, 3])

        cw_game.move(1)
        assert cw_game.board == utils.build_board([4, 4, 3, 3],
                                                  [4, 0, 3, 3])
        assert cw_game.store == [0, 0]

    def test_nocapt_nopic(self, cw_game):

        cw_game.board = utils.build_board([0, 3, 3, 3],
                                          [0, 3, 3, 3])
        cw_game.store = [3, 3]

        cw_game.move(3)
        assert cw_game.board == utils.build_board([0, 3, 3, 3],
                                                  [1, 4, 4, 0])
        assert cw_game.store == [3, 3]

    def test_capt(self, cw_game):

        cw_game.board = utils.build_board([4, 3, 3, 3],
                                          [0, 3, 3, 3])
        cw_game.store = [1, 1]

        cw_game.move(3)
        assert cw_game.board == utils.build_board([0, 3, 3, 3],
                                                  [1, 4, 4, 0])
        assert cw_game.store == [5, 1]

    def test_xcp_nocapt(self, cw_xcp_game):

        assert cw_xcp_game.board == utils.build_board([3, 3, 3, 3],
                                                      [3, 3, 3, 3])

        cw_xcp_game.move(1)
        assert cw_xcp_game.board == utils.build_board([4, 4, 3, 3],
                                                      [4, 0, 3, 3])
        assert cw_xcp_game.store == [0, 0]

    def test_xcp_nocapt_nopic(self, cw_xcp_game):

        cw_xcp_game.board = utils.build_board([0, 3, 3, 3],
                                              [0, 3, 3, 3])
        cw_xcp_game.store = [3, 3]

        cw_xcp_game.move(3)
        assert cw_xcp_game.board == utils.build_board([0, 3, 3, 3],
                                                      [1, 4, 4, 0])
        assert cw_xcp_game.store == [3, 3]

    def test_xcp_capt(self, cw_xcp_game):

        cw_xcp_game.board = utils.build_board([4, 3, 3, 3],
                                              [0, 3, 3, 3])
        cw_xcp_game.store = [1, 1]

        cw_xcp_game.move(3)
        assert cw_xcp_game.board == utils.build_board([0, 3, 3, 3],
                                                      [0, 4, 4, 0])
        assert cw_xcp_game.store == [6, 1]


class TestMultiCrossCapts:

    @pytest.fixture
    def cw_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(name='my name',
                                nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.CW,
                                                crosscapt=True,
                                                capsamedir=True,
                                                multicapt=True,
                                                oppsidecapt=True,
                                                stores=True))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    @pytest.fixture
    def cw_xcp_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(name='my name',
                                nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.CW,
                                                crosscapt=True,
                                                xcpickown=True,
                                                multicapt=True,
                                                stores=True)
                                )

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    def test_nocapt(self, cw_game):

        assert cw_game.board == utils.build_board([3, 3, 3, 3],
                                                  [3, 3, 3, 3])

        cw_game.move(1)
        assert cw_game.board == utils.build_board([4, 4, 3, 3],
                                                  [4, 0, 3, 3])
        assert cw_game.store == [0, 0]

    def test_capt(self, cw_game):

        cw_game.board = utils.build_board([4, 3, 3, 3],
                                          [0, 3, 3, 3])
        cw_game.store = [1, 1]

        cw_game.move(3)
        assert cw_game.board == utils.build_board([0, 3, 3, 3],
                                                  [1, 4, 4, 0])
        assert cw_game.store == [5, 1]

    def test_capt_mult(self, cw_game):

        cw_game.board = utils.build_board([4, 3, 3, 3],
                                          [0, 0, 1, 0])
        cw_game.store = [8, 2]

        cw_game.capture_seeds(2, Direct.CW)
        assert cw_game.board == utils.build_board([0, 0, 0, 3],
                                                  [0, 0, 1, 0])
        assert cw_game.store == [18, 2]

    def test_xcp_nocapt(self, cw_xcp_game):

        assert cw_xcp_game.board == utils.build_board([3, 3, 3, 3],
                                                      [3, 3, 3, 3])

        cw_xcp_game.move(1)
        assert cw_xcp_game.board == utils.build_board([4, 4, 3, 3],
                                                      [4, 0, 3, 3])
        assert cw_xcp_game.store == [0, 0]


    def test_xcp_capt(self, cw_xcp_game):

        cw_xcp_game.board = utils.build_board([4, 3, 3, 3],
                                              [0, 3, 3, 3])
        cw_xcp_game.store = [1, 1]

        cw_xcp_game.move(3)
        assert cw_xcp_game.board == utils.build_board([0, 3, 3, 3],
                                                      [0, 4, 4, 0])
        assert cw_xcp_game.store == [6, 1]

    def test_xcp_capt_mult(self, cw_xcp_game):

        cw_xcp_game.board = utils.build_board([4, 3, 3, 3],
                                              [0, 0, 1, 0])
        cw_xcp_game.store = [8, 2]

        cw_xcp_game.capture_seeds(2, Direct.CW)
        assert cw_xcp_game.board == utils.build_board([4, 3, 0, 0],
                                                      [0, 0, 0, 0])
        assert cw_xcp_game.store == [15, 2]


class TestBlockCapts:

    @pytest.fixture
    def cw_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(name='my name',
                                nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.CW,
                                                evens=True,
                                                blocks=True,
                                                multicapt=True,
                                                stores=True))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    def test_not_blocked(self, cw_game):

        assert not any(cw_game.blocked)
        assert cw_game.board == utils.build_board([3, 3, 3, 3],
                                                  [3, 3, 3, 3])

        cw_game.move(1)
        assert cw_game.board == utils.build_board([0, 0, 3, 3],
                                                  [0, 0, 3, 3])
        assert cw_game.store == [12, 0]

    def test_blocked(self, cw_game):

        cw_game.board = utils.build_board([4, 0, 4, 3],
                                          [4, 0, 3, 3])
        cw_game.store = [2, 1]
        cw_game.blocked[6] = True

        cw_game.capture_seeds(5, Direct.CW)
        assert cw_game.board == utils.build_board([0, 0, 0, 3],
                                                  [0, 0, 3, 3])
        assert cw_game.store == [14, 1]



class TestChildCapts:

    @pytest.fixture
    def cw_game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=4)

        game_info = gi.GameInfo(name='my name',
                                nbr_holes=game_consts.holes,
                                flags=GameFlags(sow_direct=Direct.CW,
                                                evens=True,
                                                convert_cnt=4,
                                                child=True,
                                                stores=True))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    def test_make_f_child(self, cw_game):

        assert not any(cw_game.child)
        assert cw_game.board == utils.build_board([3, 3, 3, 3],
                                                  [3, 3, 3, 3])
        assert cw_game.store == [0, 0]

        cw_game.move(1)
        assert cw_game.board == utils.build_board([4, 4, 3, 3],
                                                  [4, 0, 3, 3])
        assert cw_game.store == [0, 0]
        assert cw_game.child == utils.build_board([N, F, N, N],
                                                  [N, N, N, N])

    def test_make_t_child(self, cw_game):

        cw_game.turn = True
        assert not any(cw_game.child)
        assert cw_game.board == utils.build_board([3, 3, 3, 3],
                                                  [3, 3, 3, 3])
        assert cw_game.store == [0, 0]

        cw_game.move(1)
        assert cw_game.board == utils.build_board([3, 0, 4, 4],
                                                  [3, 3, 3, 4])
        assert cw_game.store == [0, 0]
        assert cw_game.child == utils.build_board([N, N, N, N],
                                                  [N, N, N, T])

    def test_already_child(self, cw_game):

        cw_game.board = utils.build_board([3, 0, 3, 3],
                                          [3, 3, 3, 3])
        cw_game.store = [2, 1]
        cw_game.child[6] = False

        cw_game.move(1)
        assert cw_game.board == utils.build_board([4, 1, 3, 3],
                                                  [4, 0, 3, 3])
        assert cw_game.store == [2, 1]
        assert cw_game.child == utils.build_board([N, F, N, N],
                                                  [N, N, N, N])


    def test_dont_make1(self, cw_game):
        """don't make child but capture"""

        cw_game.board = utils.build_board([3, 1, 3, 3],
                                          [3, 3, 3, 3])
        cw_game.store = [1, 1]

        cw_game.move(1)
        assert cw_game.board == utils.build_board([4, 0, 3, 3],
                                                  [4, 0, 3, 3])
        assert cw_game.store == [3, 1]
        assert not any(cw_game.child)


    def test_dont_make2(self, cw_game):
        """don't make child and don't capture"""

        cw_game.board = utils.build_board([3, 2, 3, 3],
                                          [3, 3, 3, 3])
        cw_game.store = [1, 0]

        cw_game.move(1)
        assert cw_game.board == utils.build_board([4, 3, 3, 3],
                                                  [4, 0, 3, 3])
        assert cw_game.store == [1, 0]
        assert not any(cw_game.child)


    def test_dont_make3(self, cw_game):
        """don't make child because end on own side"""

        cw_game.board = utils.build_board([3, 0, 3, 3],
                                          [3, 3, 3, 3])
        cw_game.store = [2, 1]

        cw_game.move(3)
        assert cw_game.board == utils.build_board([3, 0, 3, 3],
                                                  [0, 4, 4, 0])
        assert cw_game.store == [6, 1]
        assert not any(cw_game.child)



class TestGrandSlam:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=3, holes=3)

        game_info = gi.GameInfo(nbr_holes=game_consts.holes,
                                capt_on=[2],
                                flags=GameFlags(sow_direct=Direct.CW,
                                                multicapt=True,
                                                stores=True))

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game

    def test_no_seeds(self, game):

        game.board = utils.build_board([0, 0, 0], [1, 0, 0])

        object.__setattr__(game.info.flags, 'grandslam', GrandSlam.NO_CAPT)
        captor = capturer.deco_capturer(game)

        assert not captor.is_grandslam(0, Direct.CW)



    @pytest.mark.parametrize('grandslam', [GrandSlam.NO_CAPT,
                                           GrandSlam.OPP_GETS_REMAIN,
                                           GrandSlam.LEAVE_LEFT])
    def test_no_gs(self, game, grandslam):

        object.__setattr__(game.info.flags, 'grandslam', grandslam)
        captor = capturer.deco_capturer(game)

        assert not captor.is_grandslam(0, Direct.CW)
        print(captor.is_grandslam(0, Direct.CW))

        captor.do_captures(0, Direct.CW)
        assert game.board == [3, 3, 3, 3, 3, 3]


    @pytest.mark.parametrize('grandslam, eboard, estore',
                             [(GrandSlam.NO_CAPT,
                               utils.build_board([3, 0, 0],
                                                 [2, 0, 0]),
                               [3, 4]),

                              (GrandSlam.OPP_GETS_REMAIN,
                               utils.build_board([0, 0, 0],
                                                 [0, 0, 0]),
                               [6, 6]),

                              (GrandSlam.LEAVE_LEFT,
                               utils.build_board([3, 0, 0],
                                                 [0, 0, 0]),
                               [3, 6]),

                              (GrandSlam.LEAVE_RIGHT,
                               utils.build_board([3, 0, 0],
                                                 [2, 0, 0]),
                               [3, 4]),
                               ])
    def test_gs_one(self, game, grandslam, eboard, estore):

        game.turn = True
        game.board = utils.build_board([3, 0, 0],
                                       [2, 0, 0])
        game.store = [3, 4]

        object.__setattr__(game.info.flags, 'grandslam', grandslam)
        captor = capturer.deco_capturer(game)

        captor.do_captures(0, Direct.CW)
        assert game.board == eboard
        assert game.store == estore


    @pytest.mark.parametrize('grandslam, eboard, estore',
                             [(GrandSlam.NO_CAPT,
                               utils.build_board([2, 2, 2],
                                                 [1, 0, 0]),
                               [2, 3]),

                              (GrandSlam.OPP_GETS_REMAIN,
                               utils.build_board([0, 0, 0],
                                                 [0, 0, 0]),
                               [8, 4]),

                              (GrandSlam.LEAVE_LEFT,
                               utils.build_board([2, 0, 0],
                                                 [1, 0, 0]),
                               [6, 3]),

                              (GrandSlam.LEAVE_RIGHT,
                               utils.build_board([0, 0, 2],
                                                 [1, 0, 0]),
                               [6, 3]),

                               ])
    def test_gs_two(self, game, grandslam, eboard, estore):

        game.turn = False
        game.board = utils.build_board([2, 2, 2],
                                       [1, 0, 0])
        game.store = [2, 3]

        object.__setattr__(game.info.flags, 'grandslam', grandslam)
        captor = capturer.deco_capturer(game)

        captor.do_captures(5, Direct.CCW)   # does not match game, it's fine
        assert game.board == eboard
        assert game.store == estore
