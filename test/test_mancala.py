# -*- coding: utf-8 -*-
"""Test mancala tests the logic specific to the mancala.py file.
It does not test the whole game--integration tests do that.
Concentration here is that the methods pass the real work
on to the correct decos.


added these packages:

conda install pytest
conda install coverage
conda install pytest-cov
conda install -c spyder-ide spyder-unittest

To get branch coverage in Anaconda Prompt:

coverage run --branch -m pytest
coverage html

Created on Sat Mar 25 07:32:54 2023
@author: Ann"""


# %% imports

import re

import pytest
pytestmark = pytest.mark.unittest

from context import capt_ok
from context import game_constants as gconsts
from context import game_interface as gi
from context import game_logger
from context import ginfo_rules
from context import incrementer
from context import mancala

from game_interface import AllowRule
from game_interface import ChildType
from game_interface import Direct
from game_interface import Goal
from game_interface import RoundFill
from game_interface import WinCond

# %%

TEST_COVERS = ['src\\mancala.py']

# %% constants

T = True
F = False
N = None


# %%

class TestGameState:

    @pytest.mark.parametrize(
        'board, store, turn, unlocked, blocked, '
        'child, owner, istate, ere_one, ere_two',
        [((1, 2, 3, 4), [0, 0], False,
          None, None, None, None, (F, T),
          ' *4 +3 *', ' *1 +2 +\\* *'),
         ((1, 2, 3, 4), [2, 0], True,
           None, None, None, None, F,
           ' *4 +3 +\\* *', ' *1 +2 +2 *'),
         ((1, 2, 3, 4), [0, 2], True,
           None, None, None, None, (N, N),
           ' *4 +3 +\\* +2 *', ' *1 +2 *'),
         ((1, 2, 3, 4), [0, 0], True,
          [T, F, F, T], None, None, None, None,
          ' *4 +3_ +\\* *', ' *1 +2_ *'),
         ((1, 2, 3, 4), [0, 0], True,
          None, [T, F, F, T], None, None, 123,
          ' *x +3 +\\* *', ' *x +2 *'),
         ((1, 2, 3, 4), [0, 0], True,
          None, None, [T, F, N, N], None, 'st',
          ' *4 +3 +\\* *', ' *1˄ +2˅ *'),
         ((1, 2, 3, 4), [0, 0], True,
          [T, F, F, T], None, [T, F, N, N], None, ('sd', 2),
          ' *4 +3_ +\\* *', ' *1 ˄ +2_˅ *'),
         ((1, 2, 3, 4), [0, 0], True,
          [T, F, F, T], None, None, [T, F, N, N], T,
          ' *4 +3 *_ +\\* *', ' *1 *↑ +2↓ _ *'),
         ])
    def test_state_const(self, board, store, turn,
                         unlocked, blocked, child, owner, istate,
                         ere_one, ere_two):

        state = mancala.GameState(board=board,
                                  store=store,
                                  _turn=turn,
                                  mcount=0,
                                  unlocked=unlocked,
                                  blocked=blocked,
                                  child=child,
                                  owner=owner,
                                  istate=istate)
        assert state.board == board
        assert state.store == store
        assert state._turn == turn
        assert state.turn == turn
        assert state.unlocked == unlocked
        assert state.blocked == blocked
        assert state.child == child
        assert state.owner == owner
        assert state.istate == istate
        gstrs = str(state).split('\n')
        assert re.fullmatch(ere_one, gstrs[1])
        assert re.fullmatch(ere_two, gstrs[2])


    @pytest.fixture
    def game(self):
        """Game that has access to all of the state data.
        Turn off game_info rule checking by providing empty dict!"""

        game_consts = gconsts.GameConsts(nbr_start=4, holes=2)
        game_info = gi.GameInfo(capt_on = [2],
                                blocks=True,
                                rounds=gi.Rounds.HALF_SEEDS,
                                round_fill=RoundFill.SHORTEN,  # game will use child inhibitor
                                child_type=ChildType.NORMAL,
                                child_cvt=2,
                                goal=gi.Goal.TERRITORY,
                                moveunlock=True,
                                nbr_holes = game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        game = mancala.Mancala(game_consts, game_info)
        return game

    ST_CASES = [
        ((1, 2, 3, 4), (0, 0), False, None, None, None, None, False),
        ((1, 2, 3, 4), (2, 0), True,  None, None, None, None, True),
        ((1, 2, 3, 4), (0, 2), True,  None, None, None, None, False),
        ((1, 2, 3, 4), (0, 0), True, (T, F, F, T), None, None, None, True),
        ((1, 2, 3, 4), (0, 0), True, None, (T, F, F, T), None, None, False),
        ((1, 2, 3, 4), (0, 0), True, None, None, (T, F, N, N), None, True),
        ((1, 2, 3, 4), (0, 0), True, (T, F, F, T), None, (T, F, N, N), None, True),
        ((1, 2, 3, 4), (0, 2), True, None, None, None, (T, F, F, T), True),
        ]

    @pytest.mark.parametrize(
        'board, store, turn, unlocked, blocked, child, owner, istate',
        ST_CASES)
    def test_getter(self, game, board, store, turn,
                    unlocked, blocked, child, owner, istate):
        """Adjust the game to have the input parameters, then get the
        state from the game and confirm that the state matches the values
        set. """

        game.board = board
        game.store = store
        game.turn = turn

        if unlocked:
            game.unlocked = unlocked
        else:
            object.__setattr__(game.info, 'moveunlock', False)
        if blocked:
            game.blocked = list(blocked)
        else:
            object.__setattr__(game.info, 'blocks', False)
        if child:
            game.child = list(child)
        else:
            object.__setattr__(game.info, 'child_cvt', 0)
            object.__setattr__(game.info, 'child_type', ChildType.NOCHILD)
        if owner:
            game.owner = list(owner)
        else:
            # this will only effect capturing the state
            object.__setattr__(game.info, 'goal', gi.Goal.MAX_SEEDS)

        game.inhibitor._children = istate

        state = game.state

        assert state.board == board
        assert state.store == store
        assert state._turn == turn
        assert state.turn == turn
        assert state.unlocked == unlocked
        assert state.blocked == blocked
        assert state.child == child
        assert state.istate == istate

        if owner:
            assert state.owner == owner
        else:
            assert not state.owner


    @pytest.mark.parametrize(
        'board, store, turn, unlocked, blocked, child, owner, istate',
        ST_CASES)
    def test_setter(self, game, board, store, turn,
                    unlocked, blocked, child, owner, istate):
        """Build a game state from the parameters and assign it to the game;
        then confirm that the data was put in the right places."""

        game.state = mancala.GameState(board=board,
                                       store=store,
                                       _turn=turn,
                                       mcount=0,
                                       unlocked=unlocked,
                                       blocked=blocked,
                                       child=child,
                                       owner=owner,
                                       istate=istate)

        assert game.board == list(board)
        assert game.store == list(store)
        assert game.turn == turn

        if unlocked:
            assert game.unlocked == list(unlocked)
        else:
            assert game.unlocked == [F, F, F, F]

        if blocked:
            assert game.blocked == list(blocked)
        else:
            assert game.blocked == [F, F, F, F]

        if child:
            assert game.child == list(child)
        else:
            assert game.child == [N, N, N, N]

        if owner:
            assert game.owner == list(owner)
        else:
            # game was initialized as TERRITORY
            assert game.owner == [F, F, T, T]

        assert game.inhibitor._children == istate


    def test_mcount_ops(self, game):

        assert game.mcount == 0
        assert game.state.mcount == 0

        game.mcount = 10

        # make new state and test it's mcount

        state = game.state
        assert state.mcount == 10

        state.clear_mcount()
        assert state.mcount == 0

        # change mcount in game but not the state we just collected
        game.mcount = 20

        state.set_mcount_from(game)
        assert state.mcount == 20


class TestRtally:

    @pytest.fixture(params=gi.Goal)
    def game(self, request):
        """a game of each goal type"""

        game_consts = gconsts.GameConsts(nbr_start=4, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=request.param,
                                rounds=gi.Rounds.NO_MOVES,
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_rtally(self, game):

        if 'RND' in game.info.goal.name:
            assert game.rtally
        else:
            assert not game.rtally


    @pytest.fixture
    def esgame(self, request):
        """extra seeds game goal"""

        game_consts = gconsts.GameConsts(nbr_start=4, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=gi.Goal.RND_EXTRA_SEEDS,
                                rounds=gi.Rounds.NO_MOVES,
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_state_getter(self, esgame):

        assert esgame.rtally
        assert esgame.state.rstate == ((0, 0), (0, 0), (0, 0), (0, 0))

        esgame.rtally.round_wins = [0, 3]
        esgame.rtally.seeds = [1, 4]
        esgame.rtally.diff_sums = [1, 5]
        esgame.rtally.score = [9, 2]

        assert esgame.state.rstate == ((0, 3), (1, 4), (1, 5), (9, 2))


    def test_state_setter(self, esgame):

        assert esgame.rtally
        assert esgame.state.rstate == ((0, 0), (0, 0), (0, 0), (0, 0))

        state = mancala.GameState(board=(1, 2, 3, 4),
                                  store=(10, 20),
                                  _turn=False,
                                  mcount=5,
                                  rstate=((0, 3), (1, 4), (1, 5), (9, 2)))

        esgame.state = state

        assert esgame.rtally.round_wins == [0, 3]
        assert esgame.rtally.seeds == [1, 4]
        assert esgame.rtally.diff_sums == [1, 5]
        assert esgame.rtally.score == [9, 2]


class TestMoveData:

    @pytest.fixture
    def game(self):
        """basic game"""

        game_consts = gconsts.GameConsts(nbr_start=4, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_construct(self, game):

        # this call is needed for copy of MoveData to work
        mdata = mancala.MoveData()
        assert not mdata.player
        assert not mdata.board
        assert not mdata.move

        mdata = mancala.MoveData(game, 5)

        assert mdata.board == tuple(game.board)
        assert mdata.player == game.turn
        assert not mdata.direct

        assert mdata.move == 5

        mstr = str(mdata)
        assert '4, 4, 4, 4' in mstr
        assert 'direct=None' in mstr


    def test_sow_loc_prop(self, game):

        mdata = mancala.MoveData(game, 5)

        # construction settings
        assert mdata.sow_loc == 0
        assert mdata._sow_loc == 0
        assert mdata.cont_sow_loc == 0

        # set sow start and initing cont_sow_loc
        mdata.sow_loc = 3

        assert mdata.sow_loc == 3
        assert mdata._sow_loc == 3
        assert mdata.cont_sow_loc == 3

        # update cont_sow_loc, sow_loc should not change
        mdata.cont_sow_loc = 1

        assert mdata.sow_loc == 3
        assert mdata._sow_loc == 3
        assert mdata.cont_sow_loc == 1


class TestManDeco:

    @pytest.fixture
    def game(self):
        """basic game"""

        game_consts = gconsts.GameConsts(nbr_start=4, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_deco(self, game):

        assert game.deco.new_game
        assert game.deco.allow
        assert game.deco.moves
        assert game.deco.incr
        assert game.deco.drawer
        assert game.deco.get_dir
        assert game.deco.sower
        assert game.deco.ender
        assert game.deco.quitter
        assert game.deco.capt_ok
        assert game.deco.capturer
        assert game.deco.gstr
        assert game.deco.make_child

        dstr = str(game.deco)
        for field, value in vars(game.deco).items():
            assert field in dstr


    def test_replace_deco_1(self):
        """Test replacing the head of the chain."""

        game_consts = gconsts.GameConsts(nbr_start=2, holes=5)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=3,
                                skip_start=True,
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        # confirm expected structure of deco chain
        assert isinstance(game.deco.incr,
                          incrementer.IncPastStart), 'Test conditions changed'
        assert isinstance(game.deco.incr.decorator,
                          incrementer.Increment), 'Test conditions changed'

        game.deco.replace_deco('incr', incrementer.IncPastStart,
                               incrementer.IncPastBlocks(game))

        assert isinstance(game.deco.incr, incrementer.IncPastBlocks)
        assert isinstance(game.deco.incr.decorator, incrementer.Increment)


    @pytest.fixture
    def bad_game(self):
        """Bad config but no rules are checked."""

        game_consts = gconsts.GameConsts(nbr_start=2, holes=5)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=3,
                                skip_start=True,
                                blocks=True,            # this is not valid
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())  # empty rule dict
        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_replace_deco_2(self, bad_game):
        """Test replacing the end of the deco chain."""

        # confirm expected structure of deco chain
        assert isinstance(bad_game.deco.incr,
                          incrementer.IncPastBlocks), 'Test conditions changed'
        assert isinstance(bad_game.deco.incr.decorator,
                          incrementer.IncPastStart), 'Test conditions changed'
        assert isinstance(bad_game.deco.incr.decorator.decorator,
                          incrementer.Increment), 'Test conditions changed'

        # true is not a valid decorator, but we want to assure that it
        # is replaced correctly
        new_incr = incrementer.IncPastBlocks(bad_game, True)
        assert new_incr.decorator

        bad_game.deco.replace_deco('incr', incrementer.Increment,
                                   new_incr)

        assert isinstance(bad_game.deco.incr, incrementer.IncPastBlocks)
        assert isinstance(bad_game.deco.incr.decorator,
                          incrementer.IncPastStart)
        assert isinstance(bad_game.deco.incr.decorator.decorator,
                          incrementer.IncPastBlocks)
        assert not new_incr.decorator


    def test_bad_deco_replace(self, mocker, bad_game):
        """Patch the deco chain to only a IncPastBlocks,
        but then try to replace Incrementer. It should fail."""

        bad_game.deco.incr = incrementer.IncPastBlocks(None)

        with pytest.raises(AssertionError):
            bad_game.deco.replace_deco('incr', incrementer.Increment,
                                   incrementer.IncPastBlocks(bad_game))

    def test_insert_deco_1(self):
        """Test inserting at the head of the chain."""

        game_consts = gconsts.GameConsts(nbr_start=2, holes=5)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=3,
                                skip_start=True,
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        # confirm expected structure of deco chain
        assert isinstance(game.deco.incr,
                          incrementer.IncPastStart), 'Test conditions changed'
        assert isinstance(game.deco.incr.decorator,
                          incrementer.Increment), 'Test conditions changed'

        game.deco.insert_deco('incr', incrementer.IncPastStart,
                               incrementer.IncPastBlocks(game))

        assert isinstance(game.deco.incr, incrementer.IncPastBlocks)
        assert isinstance(game.deco.incr.decorator, incrementer.IncPastStart)


    def test_insert_deco_2(self):
        """Test inserting not at the head of the chain."""

        game_consts = gconsts.GameConsts(nbr_start=2, holes=5)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=3,
                                skip_start=True,
                                capt_side=gi.CaptSide.OWN_SIDE,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        capt_ok_deco = game.deco.capt_ok

        # confirm expected structure of deco chain
        assert isinstance(capt_ok_deco,
                          capt_ok.CaptNeedSeedsNotChild), 'Test conditions changed'
        assert isinstance(capt_ok_deco.decorator,
                          capt_ok.CaptSideOk), 'Test conditions changed'
        assert isinstance(capt_ok_deco.decorator.decorator,
                          capt_ok.CaptOn), 'Test conditions changed'
        assert isinstance(capt_ok_deco.decorator.decorator.decorator,
                          capt_ok.CaptTrue), 'Test conditions changed'

        game.deco.insert_deco('capt_ok', capt_ok.CaptOn,
                               capt_ok.CaptEvens(game))

        assert isinstance(capt_ok_deco,
                          capt_ok.CaptNeedSeedsNotChild)
        assert isinstance(capt_ok_deco.decorator,
                          capt_ok.CaptSideOk)
        assert isinstance(capt_ok_deco.decorator.decorator,
                          capt_ok.CaptEvens)
        assert isinstance(capt_ok_deco.decorator.decorator.decorator,
                          capt_ok.CaptOn)
        assert isinstance(capt_ok_deco.decorator.decorator.decorator.decorator,
                          capt_ok.CaptTrue)


    def test_bad_deco_insert(self, mocker, bad_game):
        """Patch the deco chain to only a IncPastBlocks,
        but then try to replace Incrementer. It should fail."""

        bad_game.deco.incr = incrementer.IncPastBlocks(None)

        with pytest.raises(AssertionError):
            bad_game.deco.insert_deco('incr', incrementer.Increment,
                                      incrementer.IncPastBlocks(bad_game))


@pytest.mark.filterwarnings("ignore")
class TestConstruction:

    @pytest.fixture
    def min_game_if(self):
        return gi.GameInfo(nbr_holes=6,
                           rules=mancala.Mancala.rules)

    def test_bad_params(self, min_game_if):

        with pytest.raises(TypeError):
            mancala.Mancala()

        with pytest.raises(TypeError):
            mancala.Mancala(None, None)

        with pytest.raises(TypeError):
            mancala.Mancala(gconsts.GameConsts(3, 5), None)

        with pytest.raises(TypeError):
            mancala.Mancala(None, min_game_if)

        with pytest.raises(TypeError):
            mancala.Mancala(gconsts.GameConsts(3, 5), min_game_if, 5)

    def test_min_params(self, min_game_if):

        mancala.Mancala(gconsts.GameConsts(3, 5), min_game_if)


    def test_start_pat(self):
        """All start patterns are tested with new_game.
        Here confirming that the proper changes were made once."""

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                start_pattern=gi.StartPattern.ALTERNATES,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)

        assert game.cts.total_seeds == 16
        assert game.board == [0, 4, 0, 4, 0, 4, 0, 4]


class TestBasicIfs:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_turn(self, game):

        # inited randomly but one of these
        assert game.get_turn() in [False, True]

        game.turn = False
        assert not game.get_turn()
        game.turn = True
        assert game.get_turn()


    def test_param_str(self, game):
        """Contents really isn't important, if a programmer
        doesn't complain"""

        game.params_str()


class TestDelegates:
    """Confirm delegated interfaces are, well, delegated.
    Set unique return values to confirm the game object
    returns the right data. """

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_dlg_str(self, game, mocker):

        mobj = mocker.patch.object(game.deco.gstr, 'get_string')
        mobj.return_value = 'a string'
        str(game)
        mobj.assert_called_once()


    def test_dlg_get_allowables(self, game, mocker):

        mobj = mocker.patch.object(game.deco.allow, 'get_allowable_holes')
        mobj.return_value = [2, 4]

        assert game.get_allowable_holes() == [2, 4]
        mobj.assert_called_once()


    def test_dlg_get_moves(self, game, mocker):

        mobj = mocker.patch.object(game.deco.moves, 'get_moves')
        mobj.return_value = 'a list of moves'

        assert game.get_moves() == 'a list of moves'
        mobj.assert_called_once()


    def test_dlg_new_game(self, game, mocker):

        mobj = mocker.patch.object(game.deco.new_game, 'new_game')
        mobj.return_value = 123

        assert game.new_game() == 123
        mobj.assert_called_once()


    @pytest.mark.parametrize('tcase',
                             [(True, 123),
                              (False, 345)])
    def test_dlg_end_round(self, game, mocker, tcase):

        mobj = mocker.patch.object(game.deco.ender, 'game_ended')
        mobj.return_value = tcase

        assert game.end_round() == tcase[0]
        assert game.turn == tcase[1]
        mobj.assert_called_once()


    @pytest.mark.parametrize('tcase',
                             [(True, 123),
                              (False, 345)])
    def test_dlg_quitter(self, game, mocker, tcase):

        mobj = mocker.patch.object(game.deco.quitter, 'game_ended')
        mobj.return_value = tcase

        assert game.end_game() == tcase[0]
        assert game.turn == tcase[1]
        mobj.assert_called_once()


    @pytest.mark.parametrize('tcase',
                             [(234, False),
                              (345, True),
                              (False, True)])
    def test_dlg_winner(self, game, mocker, tcase):

        game.turn = 90  # a unique value

        mobj = mocker.patch.object(game.deco.ender, 'game_ended')
        mobj.return_value = tcase

        rval = game.win_conditions()
        if tcase[0]:
            assert rval == tcase[0]
            assert game.turn == tcase[1]
        else:
            assert rval is None
            assert game.turn == 90
        mobj.assert_called_once()


    @pytest.mark.parametrize('mustpass, allow, erval',
                             [(False, False, False),
                              (False, True, False),
                              (True, False, True),
                              (True, True, False)])
    def test_dlg_test_pass(self, game, mocker, mustpass, allow, erval):

        object.__setattr__(game.info, 'mustpass', mustpass)
        game.turn = False

        mobj = mocker.patch.object(game.deco.allow, 'get_allowable_holes')
        mobj.return_value = [allow]

        assert game.test_pass() == erval

        if erval:
            assert game.mcount == 1
            assert game.turn
        else:
            assert game.mcount == 0
            assert not game.turn


    def test_dlg_single_sow(self, game, mocker):

        mobj = mocker.patch.object(game, 'do_sow')
        mobj.return_value = 123

        assert game.sim_single_sow(5) == 123
        mobj.assert_called_once_with(5, single=True)


    def test_dlg_sow_capt(self, game, mocker):

        msow = mocker.patch.object(game, 'do_sow')
        mcapt = mocker.patch.object(game, 'capture_seeds')

        assert game.sim_sow_capt(5)
        msow.assert_called_once_with(5)
        mcapt.assert_called_once()


    def test_dlg_sow_capt_not(self, game, mocker):
        """capt not called"""

        msow = mocker.patch.object(game, 'do_sow')
        mdata = mancala.MoveData(game, 5)
        mdata.capt_loc = gi.WinCond.REPEAT_TURN
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')

        assert game.sim_sow_capt(5)
        msow.assert_called_once_with(5)
        mcapt.assert_not_called()


    def test_dlg_do_sow(self, game, mocker):

        mstart = mocker.patch.object(game.deco.drawer, 'draw')
        mstart.return_value = 'first', 'second'
        mgdir = mocker.patch.object(game.deco.get_dir, 'get_direction')
        mgdir.return_value = 'lost'
        msower = mocker.patch.object(game.deco.sower, 'sow_seeds')

        mdata = game.do_sow(5, False)

        mstart.assert_called_once_with(5)
        mgdir.assert_called_once_with(5, 'first')
        msower.assert_called_once()

        assert isinstance(mdata, mancala.MoveData)
        assert mdata.board == tuple(game.board)
        assert mdata.move == 5
        assert mdata.sow_loc == 'first'
        assert mdata.seeds == 'second'
        assert mdata.direct == 'lost'


    def test_dlg_do_sow_single(self, game, mocker):
        """Create a generic Mock for get_single_sower to return
        and then confirm that sow_seeds is called on the generic
        mock."""

        mstart = mocker.patch.object(game.deco.drawer, 'draw')
        mstart.return_value = 'first', 'second'

        mgdir = mocker.patch.object(game.deco.get_dir, 'get_direction')
        mgdir.return_value = 'lost'

        msingle = mocker.Mock()

        msower = mocker.patch.object(game.deco.sower, 'get_single_sower')
        msower.return_value = msingle

        mdata = game.do_sow(5, True)

        mstart.assert_called_once_with(5)
        mgdir.assert_called_once_with(5, 'first')
        msingle.sow_seeds.assert_called_once()

        assert isinstance(mdata, mancala.MoveData)
        assert mdata.board == tuple(game.board)
        assert mdata.move == 5
        assert mdata.sow_loc == 'first'
        assert mdata.seeds == 'second'
        assert mdata.direct == 'lost'


    @pytest.mark.parametrize('capted', [True, False, gi.WinCond.REPEAT_TURN])
    @pytest.mark.parametrize('changed', [True, False])
    def test_dlg_capture_seeds(self, capsys, game, mocker, capted, changed):

        mdata = mancala.MoveData(game, 4)
        mdata.capt_loc = 6
        mdata.captured = capted
        mdata.capt_changed = changed

        mobj = mocker.patch.object(game.deco.capturer, 'do_captures')
        mglog = mocker.patch.object(game_logger.game_log, 'step')

        game.capture_seeds(mdata)

        mobj.assert_called_once()
        mglog.assert_called()

        log_str = mglog.call_args.args[0]

        if capted == gi.WinCond.REPEAT_TURN:
            assert 'repeat' in log_str
        elif capted:
            assert 'Capture from' in log_str

        if not capted and changed:
            assert 'changed' in log_str
        if not capted and not changed:
            assert 'No capture' in log_str


    @pytest.fixture
    def rtgame(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                goal=gi.Goal.RND_SEED_COUNT,
                                goal_param=40,
                                rounds=gi.Rounds.NO_MOVES,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = False
        return game


    def test_dlg_rt_param(self, game, rtgame):
        """the delegate is only a lamba function."""

        assert not game.rtally
        assert game.rtally_param_func() is None

        assert rtgame.rtally
        rtgame.rtally.state = ((1, 2), (3, 4), (5, 6), (7, 8))

        pfunc = rtgame.rtally_param_func()
        assert pfunc
        assert pfunc(0) == 3
        assert pfunc(1) == 4



class TestBProp:


    @pytest.mark.parametrize('goal, moveunlock, allow_rule, eunlock, eowner',
                             [[Goal.MAX_SEEDS, False, AllowRule.NONE,
                               [T, T, T, T], [N, N, N, N]],

                              [Goal.TERRITORY, False, AllowRule.NONE,
                               [T, T, T, T], [F, F, T, T]],

                              [Goal.MAX_SEEDS, False, AllowRule.MOVE_ALL_HOLES_FIRST,
                               [F, F, F, F], [N, N, N, N]],

                              [Goal.TERRITORY, False, AllowRule.MOVE_ALL_HOLES_FIRST,
                               [F, F, F, F], [F, F, T, T]],

                              [Goal.MAX_SEEDS, True, AllowRule.NONE,
                                [F, F, F, F], [N, N, N, N]],

                               [Goal.TERRITORY, True, AllowRule.NONE,
                                [F, F, F, F], [F, F, T, T]],

                               # other two combos are invalid and tested below
                             ])
    def test_init_bprop(self, goal, moveunlock, allow_rule, eunlock, eowner):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=2)
        game_info = gi.GameInfo(goal=goal,
                                goal_param=3 if goal == Goal.TERRITORY else 0,
                                evens=True,
                                stores=True,
                                moveunlock=moveunlock,
                                allow_rule=allow_rule,
                                rounds=gi.Rounds.NO_MOVES,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game =  mancala.Mancala(game_consts, game_info)

        assert game.mcount == 0
        assert game.board == [2, 2, 2, 2]
        assert game.child == [N, N, N, N]
        assert game.blocked == [F, F, F, F]
        assert game.unlocked == eunlock
        assert game.owner == eowner


    @pytest.mark.parametrize('goal, moveunlock, allow_rule',
                             [[Goal.MAX_SEEDS, True,
                               AllowRule.MOVE_ALL_HOLES_FIRST],

                              [Goal.TERRITORY, True,
                               AllowRule.MOVE_ALL_HOLES_FIRST],

                             ])
    def test_ibprop_bad(self, goal, moveunlock, allow_rule):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=2)

        with pytest.raises(gi.GameInfoError) as error:
            gi.GameInfo(goal=goal,
                        goal_param=3 if goal == Goal.TERRITORY else 0,
                        evens=True,
                        stores=True,
                        moveunlock=moveunlock,
                        allow_rule=allow_rule,
                        rounds=gi.Rounds.NO_MOVES,
                        nbr_holes=game_consts.holes,
                        rules=mancala.Mancala.rules)
        assert 'moveall_no_locks' in str(error)


class TestWinMessage:

    @pytest.fixture
    def maxgame(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(goal=Goal.MAX_SEEDS,
                                capt_on = [2],
                                stores=True,
                                rounds=gi.Rounds.HALF_SEEDS,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def depgame(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=6)
        game_info = gi.GameInfo(goal=Goal.DEPRIVE,
                                capt_on=[4],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def tergame(self):
        game_consts = gconsts.GameConsts(nbr_start=3, holes=6)
        game_info = gi.GameInfo(goal=Goal.TERRITORY,
                                stores=True,
                                rounds=gi.Rounds.NO_MOVES,
                                goal_param=10,
                                capt_on=[4],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize('game_fixt', ['maxgame', 'depgame', 'tergame'])
    @pytest.mark.parametrize('wcond', WinCond)
    @pytest.mark.parametrize('turn', [False, True])
    def test_side_messages(self, request, game_fixt, wcond, turn):
        """test which player is considered the winner and type of win."""

        game = request.getfixturevalue(game_fixt)
        game.turn = turn

        title, message = game.win_message(wcond)

        if 'ROUND' in wcond.name:
            assert 'Round Over' == title
        else:
            assert 'Game Over' == title

        if 'WIN' in wcond.name:
            if turn:
                assert 'Top' in message
            else:
                assert 'Bottom' in message
            assert 'won' in message
            return
        else:
            assert 'Top' not in message
            assert 'Bottom' not in message

        if 'TIE' in wcond.name:
            assert 'tie' in message
            return

        if 'ENDLESS' in wcond.name:
            assert 'No winner' in message
            return

        assert 'Unexpected' in message


    @pytest.mark.parametrize('game_fixt', ['maxgame', 'depgame', 'tergame'])
    @pytest.mark.parametrize('wcond', WinCond)
    def test_goal_messages(self, request, game_fixt, wcond):
        """test that the win message is proper for the game's goal."""

        game = request.getfixturevalue(game_fixt)
        game.turn = False

        title, message = game.win_message(wcond)

        if wcond.name == 'WIN':
            if 'max' in game_fixt:
                assert 'most seeds' in message
            elif 'dep' in game_fixt:
                assert 'eliminating' in message
            elif 'ter' in game_fixt:
                assert 'claiming' in message
            return

        if wcond.name == 'ROUND_WIN':
            if 'max' in game_fixt:
                assert 'half' in message
            elif 'ter' in game_fixt:
                assert 'no moves' in message
            return


        if 'TIE' in wcond.name:
            if 'max' in game_fixt:
                assert 'ended in a tie' in message
            elif 'dep' in game_fixt:
                assert 'ended with seeds' in message
            elif 'ter' in game_fixt:
                assert 'half' in message


    @pytest.mark.parametrize('message', [False,  # no last move
                                         None,  # last move,  but no message
                                         'a message'])
    def test_last_move_win(self, maxgame, message):
        """If there was an end message in the last move,
        use it."""

        if message is None or message:
            maxgame.last_mdata = mancala.MoveData(maxgame, None)

        if message:
            maxgame.last_mdata.end_msg = message

        _, wmess = maxgame.win_message(None)

        if message:
            assert message in wmess
        else:
            assert 'Unexpected' in wmess


class TestHoleProp:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(capt_on = [2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize(
        'row, pos, eindex',
        [(0, 0, 5),
         (0, 2, 3),
         (1, 0, 0),
         (1, 2, 2)])
    def test_hole_prop(self, game, row, pos, eindex):
        """Testing the right pos->loc and array access.

        Use values that are unique to each field
        (even if invalid for an actual game) to
        confirm no field mix ups."""

        game.board = [f'board{i}' for i in range(6)]
        game.unlocked = [f'lock{i}' for i in range(6)]
        game.blocked = [f'block{i}' for i in range(6)]
        game.child = [f'child{i}' for i in range(6)]
        game.owner = [f'owner{i}' for i in range(6)]

        props = game.get_hole_props(row, pos)

        assert props.seeds == 'board' + str(eindex)
        assert props.unlocked == 'lock' + str(eindex)
        assert props.blocked == 'block' + str(eindex)
        assert props.ch_owner == 'child' + str(eindex)
        assert props.owner == 'owner' + str(eindex)


class TestMove:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    def test_move(self, mocker, game):
        """Test delegations of move."""

        game.turn = True

        m_move = mocker.patch.object(game, '_move')
        m_move.return_value = 123
        mlog = mocker.patch.object(game, '_log_turn')

        assert game.move(1) == 123

        m_move.assert_called_once()
        mlog.assert_called_once_with(True, 1, 123)



    @pytest.mark.parametrize(
        'board, store, eresult',
        [([2, 2, 2, 2], [0, 0], False),
         ([2, 2, 2, 2], [2, 0], True),  # too many, store
         ([2, 2, 4, 2], [0, 0], True),    # too many, board
         ([2, 2, 0, 2], [0, 0], True),  # too few
         ([2, 2, 0, 2], [0, 2], False),  # good, some store
         ([0, 0, 0, 0], [0, 0], True),   # none
         ([0, 0, 0, 0], [8, 0], False),  # all store
         ])
    def test_seed_count(self, game, board, store, eresult):
        """test the 'conservation of seeds' assert at the top
        of move."""

        game.board = board
        game.store = store

        assert game.cts.total_seeds == 8

        if eresult:
            with pytest.raises(AssertionError):
                game._move(2)
        else:
            game._move(2)


    @pytest.mark.parametrize('turn', [False, True])
    def test_pass(self, mocker, game, turn):
        """test that pass does not change the game, does not
        call do_sow, but does change the game turn"""

        game.turn = turn
        mobj = mocker.patch.object(game, 'do_sow')

        assert game.move(gi.PASS_TOKEN) is None

        assert game.board == [2, 2, 2, 2]
        assert game.store == [0, 0]
        assert game.turn == (not turn)
        assert not mobj.do_sow.called


    def test__move_basic (self, mocker, game):
        """basic flow, no winner"""

        game.last_mdata = None

        msow = mocker.patch.object(game, 'do_sow')
        mdata = mancala.MoveData(game, 1)
        mdata.sow_loc = 123
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')
        mwin = mocker.patch.object(game, 'win_conditions')
        mwin.return_value = False
        minh = mocker.patch.object(game.inhibitor, 'clear_if')

        assert game._move(1) is None

        assert game.last_mdata.sow_loc == 123
        msow.assert_called_once_with(1)
        mcapt.assert_called_once_with(mdata)
        mwin.assert_called_once()
        minh.assert_called_once_with(game, mdata)


    def test__move_repeat_turn (self, mocker, game):
        """do sow determines repeat turn, no winner"""

        msow = mocker.patch.object(game, 'do_sow')
        mdata = mancala.MoveData(game, 1)
        mdata.capt_loc = gi.WinCond.REPEAT_TURN
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')
        mwin = mocker.patch.object(game, 'win_conditions')
        mwin.return_value = None

        assert game._move(1) is gi.WinCond.REPEAT_TURN

        msow.assert_called_once_with(1)
        mwin.assert_called_once()
        assert not mcapt.capture_seeds.called


    def test__move_repeat_win (self, mocker, game):
        """do sow determines repeat turn and the game is won"""

        msow = mocker.patch.object(game, 'do_sow')
        mdata = mancala.MoveData(game, 1)
        mdata.capt_loc = gi.WinCond.REPEAT_TURN
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')
        mwin = mocker.patch.object(game, 'win_conditions')
        mwin.return_value = gi.WinCond.WIN

        assert game._move(1) is gi.WinCond.WIN

        msow.assert_called_once_with(1)
        mwin.assert_called_once()
        assert not mcapt.capture_seeds.called
        assert not mdata.end_msg


    def test__move_endless (self, mocker, game):
        """do sow determines endless sow"""

        msow = mocker.patch.object(game, 'do_sow')
        mdata = mancala.MoveData(game, 1)
        mdata.capt_loc = gi.WinCond.ENDLESS
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')
        mwin = mocker.patch.object(game, 'win_conditions')
        mwin.return_value = gi.WinCond.WIN
        mend = mocker.patch.object(game, 'end_game')
        mend.return_value = gi.WinCond.TIE

        assert game._move(1) is gi.WinCond.TIE

        msow.assert_called_once_with(1)
        mend.assert_called_once()
        assert mdata.end_msg

        assert not mwin.win_conditions.called
        assert not mcapt.capture_seeds.called


    def test__move_c_repeat_turn (self, mocker, game):
        """capture_seeds determines repeat turn, no winner"""

        msow = mocker.patch.object(game, 'do_sow')
        mdata = mancala.MoveData(game, 1)
        mdata.capt_loc = 3
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')
        mcapt.side_effect = lambda _ : setattr(mdata, 'captured',
                                               gi.WinCond.REPEAT_TURN)

        mwin = mocker.patch.object(game, 'win_conditions')
        mwin.return_value = None

        assert game._move(1) is gi.WinCond.REPEAT_TURN

        msow.assert_called_once_with(1)
        mwin.assert_called_once()
        mcapt.assert_called_once()


    def test__move_c_repeat_win (self, mocker, game):
        """capture_seeds determines repeat turn and the game is won"""

        msow = mocker.patch.object(game, 'do_sow')
        mdata = mancala.MoveData(game, 1)
        mdata.capt_loc = 3
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')
        mcapt.side_effect = lambda _ : setattr(mdata, 'captured',
                                               gi.WinCond.REPEAT_TURN)

        mwin = mocker.patch.object(game, 'win_conditions')
        mwin.return_value = gi.WinCond.WIN

        assert game._move(1) is gi.WinCond.WIN

        msow.assert_called_once_with(1)
        mwin.assert_called_once()
        mcapt.assert_called_once()



class TestLogMove:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=2)
        game_info = gi.GameInfo(capt_on = [2],
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.mark.parametrize('turn, move_turn',
                             [(False, False),
                              (True, False),
                              (False, True),
                              (True, True),
                              ])
    @pytest.mark.parametrize('win_cond', gi.WinCond)
    def test_log_move(self, mocker, game, turn, move_turn, win_cond,
                      logger):
        """Test conditions of turn logging.
        This is pretty specific to the actual log text;
        code changes might break it."""

        assert game_logger.game_log.active

        game.turn = turn

        mlog = mocker.patch.object(game_logger.game_log, 'turn')
        game._log_turn(move_turn, 1, win_cond)

        arg_str = mlog.call_args.args[1]

        assert win_cond.name in arg_str
        assert 'move 1' in arg_str
        if move_turn:
            assert 'Top move' in arg_str
        else:
            assert 'Bottom move' in arg_str
        if 'WIN' in arg_str:
            if turn:
                assert 'by Top' in arg_str
            else:
                assert 'by Bottom' in arg_str


    @pytest.mark.parametrize('move', [gi.MoveTpl(2, None),
                                      gi.MoveTpl(2, gi.Direct.CW)])
    def test_log_move_tpl(self, mocker, game, move, logger):
        """Test the setting of the direction in the move."""

        assert game_logger.game_log.active

        game.last_mdata = mancala.MoveData(game, 2)
        game.last_mdata.direct = gi.Direct.CCW

        mlog = mocker.patch.object(game_logger.game_log, 'turn')
        game._log_turn(True, move, None)

        arg_str = mlog.call_args.args[1]
        assert '(2, CCW)' in arg_str


    def test_log_move_inactive(self, mocker, game):
        """Test with logger in inactive."""

        assert not game_logger.game_log.active

        mlog = mocker.patch.object(game_logger.game_log, 'turn')
        game._log_turn(False, 1, None)

        mlog.assert_not_called()


class TestBadNewRound:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(goal=gi.Goal.TERRITORY,
                                goal_param=8,
                                rounds=gi.Rounds.NO_MOVES,
                                start_pattern=gi.StartPattern.TWOEMPTY,
                                evens=True,
                                stores=True,
                                multicapt=-1,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    # @pytest.mark.usefixtures("logger")
    def test_good(self, game):

        assert game.is_new_round_playable()


    def test_bad(self, game):
        """The game would have ended on the previous turn
        but it tests the condition."""

        game.board = [0, 0, 0, 0, 1, 1, 0, 0]
        game.store = [5, 9]
        game.starter = True
        game.turn = True

        game.move(gi.MoveTpl(0, 3, None))

        assert not game.is_new_round_playable()


class TestSwap:

    @pytest.mark.parametrize('size', [4, 5])
    def test_swap_terr(self, size):
        # test board, owner, children, & stores

        game_consts = gconsts.GameConsts(nbr_start=4, holes=size)
        game_info = gi.GameInfo(goal=gi.Goal.TERRITORY,
                                goal_param=8,
                                child_type = gi.ChildType.NORMAL,
                                child_cvt=4,
                                evens=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)


        dbl_size = size * 2
        game.board = list(range(dbl_size))
        game.owner[0] = True
        game.owner[dbl_size - 1] = False
        game.child[size] = True
        game.child[size - 1] = False
        game.store = [4, 6]

        print(game)
        game.swap_sides()
        print(game)

        if size == 4:
            assert game.board == [4, 5, 6, 7, 0, 1, 2, 3]
            assert game.store == [6, 4]
            assert game.owner == [T, T, T, F, T, F, F, F]
            assert game.child == [T, N, N, N, N, N, N, F]

        elif size == 5:
            assert game.board == [5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
            assert game.store == [6, 4]
            assert game.owner == [T, T, T, T, F, T, F, F, F, F]
            assert game.child == [T, N, N, N, N, N, N, N, N, F]


    @pytest.mark.parametrize('size', [4, 5])
    def test_swap_locks(self, size):
        # test board, stores, locks and blocks

        game_consts = gconsts.GameConsts(nbr_start=4, holes=size)
        game_info = gi.GameInfo(goal=gi.Goal.MAX_SEEDS,
                                rounds=gi.Rounds.NO_MOVES,
                                blocks=True,
                                moveunlock=True,
                                evens=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)


        dbl_size = size * 2
        game.board = list(range(dbl_size))
        game.unlocked[0] = True
        game.unlocked[dbl_size - 1] = True
        game.blocked[size] = True
        game.blocked[size - 1] = True
        game.store = [4, 6]

        # print(game)
        game.swap_sides()
        # print(game)

        if size == 4:
            assert game.board == [4, 5, 6, 7, 0, 1, 2, 3]
            assert game.store == [6, 4]
            assert game.unlocked == [F, F, F, T, T, F, F, F]
            assert game.blocked == [T, F, F, F, F, F, F, T]

        elif size == 5:
            assert game.board == [5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
            assert game.store == [6, 4]
            assert game.unlocked == [F, F, F, F, T, T, F, F, F, F]
            assert game.blocked == [T, F, F, F, F, F, F, F, F, T]
