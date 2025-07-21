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

from context import allowables
from context import animator
from context import claimer
from context import end_move_decos as emd
from context import end_move_rounds as emr
from context import game_constants as gconsts
from context import game_info as gi
from context import game_logger
from context import mancala
from context import move_data
from context import round_tally

import utils

from game_info import AllowRule
from game_info import ChildType
from game_info import Goal
from game_info import RoundFill
from game_info import WinCond


# %%

TEST_COVERS = ['src\\mancala.py',
               'src\\man_end_msgs_mixin.py']

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

        one = state.str_one()
        assert str(state.board) in one
        assert str(state.store) in one


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
                                goal=Goal.TERRITORY,
                                moveunlock=True,
                                nbr_holes = game_consts.holes,
                                rules=lambda ginfo, holes: True)

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


    @pytest.mark.parametrize('pre', [None, move_data.MoveData(None, 8)])
    @pytest.mark.parametrize('mdata', [None, move_data.MoveData(None, 12)])
    def test_mdata_state(self, game, pre, mdata):

        game.mdata = pre
        state = game.state
        if mdata:
            object.__setattr__(state, 'mdata_state', mdata.state)
        else:
            object.__setattr__(state, 'mdata_state', None)

        game.state = state

        if mdata:
            assert game.mdata.move == 12
        else:
            assert not game.mdata


    def test_state_context(self, game):

        saved_state = game.state

        with game.save_restore_state():

            game.board = [1, 2, 3, 4]
            game.store = None
            game.unlocked = [F, T, F, F]
            game.blocked = [F, F, T, F]
            game.child = [N, N, N, N]

        assert game.state == saved_state


    def test_state_context2(self, game):
        """Test all 3 standard block/loop exits.
        saved_state is used from caller context."""

        def do_the_loop(game):

            for i in range(4):
                assert game.state == saved_state

                with game.restore_state(saved_state):

                    game.board = [1, 2, 3, 4]
                    game.store = None
                    game.unlocked = [F, T, F, F]
                    if i == 1:
                        continue
                    if i == 2:
                        break
                    if i == 3:
                        return
                    game.blocked = [F, F, T, F]
                    game.child = [N, N, N, N]


        saved_state = game.state
        do_the_loop(game)
        assert game.state == saved_state


    @pytest.mark.parametrize(
        'board, store, turn, unlocked, blocked, child, owner, istate',
        ST_CASES)
    def test_board_state(self, game, board, store, turn,
                         unlocked, blocked, child, owner, istate):
        """Use the same test cases as state tests.
        ignore istate because it is not in board_state"""

        game.board = board
        game.store = store
        game.turn = turn

        # give these bad values, they shouldn't be in board_state
        game.mcount = 7
        game.rturn_cnt = 11
        game.rtally = 13
        game.inhibitor = 17
        game.mdata = 19

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

        state = game.board_state

        assert state.board == board
        assert state.store == store
        assert state._turn == turn
        assert state.unlocked == unlocked
        assert state.blocked == blocked
        assert state.child == child
        if owner:
            assert state.owner == owner
        else:
            assert not state.owner

        assert state.mcount == 1
        assert not state.movers
        assert not state.rturn_cnt
        assert not state.rtally_state
        assert not state.istate
        assert not state.mdata_state


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
                                rules=lambda ginfo, holes: True)

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
                                goal=Goal.RND_EXTRA_SEEDS,
                                rounds=gi.Rounds.NO_MOVES,
                                nbr_holes=game_consts.holes,
                                rules=lambda ginfo, holes: True)

        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_state_getter(self, esgame):

        assert esgame.rtally
        assert esgame.state.rtally_state == ((0, 0), (0, 0), (0, 0), (0, 0))

        esgame.rtally.round_wins = [0, 3]
        esgame.rtally.seeds = [1, 4]
        esgame.rtally.diff_sums = [1, 5]
        esgame.rtally.score = [9, 2]

        assert esgame.state.rtally_state == ((0, 3), (1, 4), (1, 5), (9, 2))


    def test_state_setter(self, esgame):

        assert esgame.rtally
        assert esgame.state.rtally_state == ((0, 0), (0, 0), (0, 0), (0, 0))

        state = mancala.GameState(board=(1, 2, 3, 4),
                                  store=(10, 20),
                                  _turn=False,
                                  mcount=5,
                                  rtally_state=((0, 3), (1, 4), (1, 5), (9, 2)))

        esgame.state = state

        assert esgame.rtally.round_wins == [0, 3]
        assert esgame.rtally.seeds == [1, 4]
        assert esgame.rtally.diff_sums == [1, 5]
        assert esgame.rtally.score == [9, 2]



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
        assert game.turn_name() == 'South'
        game.turn = True
        assert game.get_turn()
        assert game.turn_name() == 'North'


    def test_param_str(self, game):
        """Contents really isn't important, if a programmer
        doesn't complain"""

        game.params_str()


    @pytest.mark.parametrize('mdata, winner', [(move_data.MoveData(), False),
                                               (move_data.MoveData(), True),
                                               (move_data.MoveData(), None),
                                               (None, None)])
    def test_get_winner(self, game, mdata, winner):

        game.mdata = mdata
        if mdata:
            game.mdata.winner = winner

        assert game.get_winner() == winner


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

        game.new_game()
        mobj.assert_called_once()


    def test_nomd_end_round(self, game, mocker):

        mobj = mocker.patch.object(game.deco.ender, 'game_ended')

        game.mdata = None
        game.end_game(quitter=False, user=True, game=False)
        mobj.assert_called_once()
        assert game.mdata.ended


    def test_user_quitter(self, game, mocker):

        mobj = mocker.patch.object(game.deco.quitter, 'game_ended')

        game.mdata = 25
        game.end_game(quitter=True, user=True)

        mobj.assert_called_once()
        assert game.mdata != 25
        assert game.mdata.ended
        assert game.mdata.user_end


    @pytest.mark.parametrize('value', [False, True])
    def test_dlg_disallow_endless(self, game, value, mocker):

        mobj = mocker.patch.object(allowables, 'deco_allowable')

        game.disallow_endless(value)

        print(mobj.calls)
        mobj.assert_called_once_with(game, no_endless=value)


    def test_dlg_end_round(self, game, mocker):

        mobj = mocker.patch.object(game.deco.ender, 'game_ended')

        game.mdata = move_data.MoveData(game, 0)
        game.end_game(quitter=False, user=True, game=False)
        mobj.assert_called_once()
        assert game.mdata.ended


    def test_dlg_quitter(self, game, mocker):

        mobj = mocker.patch.object(game.deco.quitter, 'game_ended')

        mdata = move_data.MoveData(game, 0)
        game.mdata = mdata
        game.end_game(quitter=True, user=False)

        mobj.assert_called_once()
        assert game.mdata is mdata
        assert game.mdata.ended
        assert not game.mdata.user_end


    def test_dlg_winner(self, game, mocker):

        mobj = mocker.patch.object(game.deco.ender, 'game_ended')

        game.mdata = move_data.MoveData(game, 0)
        game.win_conditions(game.mdata)
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
            assert game.mcount == 2
            assert game.turn
        else:
            assert game.mcount == 1
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
        mdata = move_data.MoveData(game, 5)
        mdata.capt_start = gi.WinCond.REPEAT_TURN
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
        mgdir.assert_called_once()
        msower.assert_called_once()

        assert isinstance(mdata, move_data.MoveData)
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
        mgdir.assert_called_once()
        msingle.sow_seeds.assert_called_once()

        assert isinstance(mdata, move_data.MoveData)
        assert mdata.board == tuple(game.board)
        assert mdata.move == 5
        assert mdata.sow_loc == 'first'
        assert mdata.seeds == 'second'
        assert mdata.direct == 'lost'


    @pytest.mark.parametrize('capted', [True, False, gi.WinCond.REPEAT_TURN])
    @pytest.mark.parametrize('changed', [True, False])
    def test_dlg_capture_seeds(self, capsys, game, mocker, capted, changed):

        mdata = move_data.MoveData(game, 4)
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
                                goal=Goal.RND_SEED_COUNT,
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


    @pytest.mark.parametrize('goal, moveunlock, allow_rule, eunlock',
                             [[Goal.MAX_SEEDS, False, AllowRule.NONE,
                               [T, T, T, T]],

                              [Goal.TERRITORY, False, AllowRule.NONE,
                               [T, T, T, T]],

                              [Goal.MAX_SEEDS, False, AllowRule.MOVE_ALL_HOLES_FIRST,
                               [F, F, F, F]],

                              [Goal.TERRITORY, False, AllowRule.MOVE_ALL_HOLES_FIRST,
                               [F, F, F, F]],

                              [Goal.MAX_SEEDS, True, AllowRule.NONE,
                                [F, F, F, F]],

                               [Goal.TERRITORY, True, AllowRule.NONE,
                                [F, F, F, F]],

                               # other two combos are invalid and tested below
                             ])
    def test_init_bprop(self, goal, moveunlock, allow_rule, eunlock):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=2)
        game_info = gi.GameInfo(goal=Goal(goal),
                                goal_param=3 if goal == Goal.TERRITORY else 0,
                                evens=True,
                                stores=True,
                                moveunlock=moveunlock,
                                allow_rule=allow_rule,
                                rounds=gi.Rounds.NO_MOVES,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game =  mancala.Mancala(game_consts, game_info)

        assert game.mcount == 1
        assert game.board == [2, 2, 2, 2]
        assert game.child == [N, N, N, N]
        assert game.blocked == [F, F, F, F]
        assert game.unlocked == eunlock
        assert game.owner == [F, F, T, T]


    @pytest.mark.parametrize('goal, moveunlock, allow_rule',
                             [[Goal.MAX_SEEDS, True,
                               AllowRule.MOVE_ALL_HOLES_FIRST],

                              [Goal.TERRITORY, True,
                               AllowRule.MOVE_ALL_HOLES_FIRST],

                             ])
    def test_ibprop_bad(self, goal, moveunlock, allow_rule):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=2)

        with pytest.raises(gi.GameInfoError) as error:
            gi.GameInfo(goal=Goal(goal),
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



    @pytest.mark.parametrize('user_end', [False, True])
    @pytest.mark.parametrize('goal', Goal)
    @pytest.mark.parametrize('win_cond', WinCond)
    def test_win_reason(self, maxgame, win_cond, goal, user_end):
        """Exercise every combination of the dependent variables."""

        object.__setattr__(maxgame.info, 'goal', goal)
        if goal in round_tally.RoundTally.GOALS:
            maxgame.rtally = round_tally.RoundTally(maxgame.info.goal,
                                                    5,
                                                    maxgame.cts.total_seeds)

        maxgame.mdata = move_data.MoveData(maxgame)
        maxgame.mdata.user_end = user_end
        maxgame.mdata.winner = True

        assert maxgame._win_reason_str(win_cond)


    @pytest.mark.parametrize('game_fixt', ['maxgame', 'depgame', 'tergame'])
    @pytest.mark.parametrize('wcond', WinCond)
    @pytest.mark.parametrize('winner', [False, True])
    def test_side_messages(self, request, game_fixt, wcond, winner):
        """test which player is considered the winner and type of win."""

        game = request.getfixturevalue(game_fixt)
        game.mdata = move_data.MoveData(game)
        game.mdata.winner = winner

        title, message = game.win_message(wcond)

        if 'ROUND' in wcond.name:
            assert 'Round Over' == title
        else:
            assert 'Game Over' == title

        if 'WIN' in wcond.name:
            if game.mdata.winner:
                assert gi.PLAYER_NAMES[True] in message
            else:
                assert gi.PLAYER_NAMES[False] in message
            assert 'won' in message
            return
        else:
            assert gi.PLAYER_NAMES[True] not in message
            assert gi.PLAYER_NAMES[False] not in message

        if 'TIE' in wcond.name:
            assert 'tie' in message
            return

        if 'ENDLESS' in wcond.name:
            # win_message no longer supports because the game is ended
            return

        assert 'Unexpected' in message


    @pytest.mark.parametrize('game_fixt', ['maxgame', 'depgame', 'tergame'])
    @pytest.mark.parametrize('wcond', WinCond)
    def test_goal_messages(self, request, game_fixt, wcond):
        """test that the win message is proper for the game's goal."""

        game = request.getfixturevalue(game_fixt)
        game.turn = False
        game.mdata = move_data.MoveData(game)
        game.mdata.winner = True

        title, message = game.win_message(wcond)
        print(title, message)

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
                assert 'more seeds' in message
            return

        if 'TIE' in wcond.name:
            if 'max' in game_fixt:
                assert 'ended in a tie' in message
            elif 'dep' in game_fixt:
                assert 'ended with seeds' in message
            elif 'ter' in game_fixt:
                assert 'half' in message


    @pytest.mark.parametrize('msg, fmsg', [(None, False),
                                           ('message 1', False),
                                           ('message 1', True)])
    def test_deco_win_msg(self, maxgame, msg, fmsg):

        maxgame.mdata = move_data.MoveData(maxgame, 0)
        maxgame.mdata.winner = True

        if msg:
            maxgame.mdata.end_msg = msg
        maxgame.mdata.fmsg = fmsg

        # use a bad WinCond to skip win and tie cases
        _, wmess = maxgame.win_message(gi.WinCond.REPEAT_TURN)

        if msg and fmsg:
            assert msg == wmess
        elif msg:
            assert len(msg) < len(wmess)
        else:
            assert 'Unexpected' in wmess


    def test_msg_subs(self, maxgame):

        maxgame.mdata = move_data.MoveData(maxgame, 0)
        maxgame.mdata.winner = True
        maxgame.mdata.end_msg = '_winner_ _loser_ _Thing_'

        # use a bad WinCond to skip win and tie cases
        _, wmess = maxgame.win_message(gi.WinCond.REPEAT_TURN)
        assert '_winner_' not in wmess
        assert '_loser_' not in wmess
        assert '_thing_' not in wmess

        # The capt'ed but not game
        assert 'North South The game' in wmess


class TestEndMessage:


    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(goal=Goal.MAX_SEEDS,
                                capt_on = [2],
                                stores=True,
                                rounds=gi.Rounds.HALF_SEEDS,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize('quitter', [False, True])
    def test_bad_message(self, mocker, game, quitter):
        """test bad config enum and force skip of deco chain test"""

        config = 25
        if quitter:
            object.__setattr__(game.info, 'quitter', config)
        else:
            object.__setattr__(game.info, 'unclaimed', config)
        game.deco.quitter = None
        game.mdata = move_data.MoveData(game, 2)

        msg = game.end_message('rtext', quitter)
        # this is the bad message used in the next text,
        # if this fails test_end_message likely needs to change too
        assert msg == 'Unclaimed seeds will .'


    @pytest.mark.parametrize('quitter', [False, True])
    @pytest.mark.parametrize('config', gi.EndGameSeeds)
    def test_end_message(self, mocker, game, quitter, config):
        """only testing that all combinations return a string
        force skip of deco chain test"""

        if quitter:
            object.__setattr__(game.info, 'quitter', config)
        else:
            object.__setattr__(game.info, 'unclaimed', config)
        game.deco.quitter = None
        game.mdata = move_data.MoveData(game, 2)

        msg = game.end_message('rtext', quitter)
        assert msg != 'Unclaimed seeds will .'


    @pytest.mark.parametrize('quitter', [False, True])
    def test_deco_message(self, mocker, game, quitter):
        """Create a deco chain with QuitToTie second."""

        object.__setattr__(game.info, 'quitter', gi.EndGameSeeds.HOLE_OWNER)
        object.__setattr__(game.info, 'unclaimed', gi.EndGameSeeds.HOLE_OWNER)

        game.deco.ender = None

        quitter = emd.QuitToTie(game)
        quitter = emr.RoundTallyWinner(game,
                                       quitter,
                                       sclaimer=claimer.ChildClaimSeeds(game))
        game.deco.quitter = quitter

        if quitter:
            assert 'tie' in game.end_message('rtext', quitter)
        else:
            assert 'tie' not in game.end_message('rtext', quitter)


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

        mdata = move_data.MoveData(game, 1)
        mdata.win_cond = 123

        m_move = mocker.patch.object(game, '_move')
        m_move.return_value = mdata

        mlog = mocker.patch.object(game, '_log_turn')

        assert game.move(1) == 123

        m_move.assert_called_once()
        mlog.assert_called_once()


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

        mdata = move_data.MoveData(game, 1)
        mdata.sow_loc = 123

        msow = mocker.patch.object(game, 'do_sow')
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')
        mwin = mocker.patch.object(game, 'win_conditions')
        minh = mocker.patch.object(game.inhibitor, 'clear_if')

        mdata = game._move(1)
        assert not mdata.win_cond
        assert mdata.sow_loc == 123

        msow.assert_called_once_with(1)
        mcapt.assert_called_once_with(mdata)
        mwin.assert_called_once_with(mdata)
        minh.assert_called_once_with(game, mdata)


    def test__move_repeat_turn (self, mocker, game):
        """do sow determines repeat turn, no winner"""

        mdata = move_data.MoveData(game, 1)
        mdata.capt_loc = gi.WinCond.REPEAT_TURN
        mdata.repeat_turn = True

        msow = mocker.patch.object(game, 'do_sow')
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')
        mwin = mocker.patch.object(game, 'win_conditions')

        mdata = game._move(1)
        assert mdata.capt_loc is gi.WinCond.REPEAT_TURN

        msow.assert_called_once_with(1)
        mwin.assert_called_once_with(mdata)
        assert not mcapt.capture_seeds.called


    def test__move_repeat_win (self, mocker, game):
        """do sow determines repeat turn and the game is won"""

        mdata = move_data.MoveData(game, 1)
        mdata.capt_loc = gi.WinCond.REPEAT_TURN
        mdata.repeat_turn = True

        msow = mocker.patch.object(game, 'do_sow')
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')
        mwin = mocker.patch.object(game, 'win_conditions')
        mwin.side_effect = lambda _ : setattr(mdata, 'win_cond',
                                              gi.WinCond.WIN)

        mdata = game._move(1)
        assert mdata.win_cond is gi.WinCond.WIN

        msow.assert_called_once_with(1)
        mwin.assert_called_once_with(mdata)
        assert not mcapt.capture_seeds.called
        assert not mdata.end_msg


    def test__move_endless (self, mocker, game):
        """do sow determines endless sow"""

        mdata = move_data.MoveData(game, 1)
        mdata.capt_start = gi.WinCond.ENDLESS

        msow = mocker.patch.object(game, 'do_sow')
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')
        mwin = mocker.patch.object(game, 'win_conditions')
        mend = mocker.patch.object(game, 'end_game')
        mend.return_value = gi.WinCond.TIE

        mdata = game._move(1)
        assert mdata.win_cond is gi.WinCond.TIE

        msow.assert_called_once_with(1)
        mend.assert_called_once()
        assert mdata.end_msg

        assert not mcapt.capture_seeds.called
        assert not mwin.win_conditions.called


    def test__move_c_repeat_turn (self, mocker, game):
        """capture_seeds determines repeat turn, no winner"""

        mdata = move_data.MoveData(game, 1)
        mdata.capt_loc = 3

        msow = mocker.patch.object(game, 'do_sow')
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')
        mcapt.side_effect = lambda _ : (
            setattr(mdata, 'captured', gi.WinCond.REPEAT_TURN),
            setattr(mdata, 'repeat_turn', True))

        mwin = mocker.patch.object(game, 'win_conditions')
        mwin.return_value = None

        mdata = game._move(1)
        assert mdata.win_cond is gi.WinCond.REPEAT_TURN
        assert mdata.captured is gi.WinCond.REPEAT_TURN
        assert mdata.repeat_turn

        msow.assert_called_once_with(1)
        mcapt.assert_called_once()
        mwin.assert_called_once()


    def test__move_c_repeat_win (self, mocker, game):
        """capture_seeds determines repeat turn and the game is won"""

        mdata = move_data.MoveData(game, 1)
        mdata.capt_loc = 3

        msow = mocker.patch.object(game, 'do_sow')
        msow.return_value = mdata

        mcapt = mocker.patch.object(game, 'capture_seeds')
        mcapt.side_effect = lambda _ : setattr(mdata, 'captured',
                                               gi.WinCond.REPEAT_TURN)

        mwin = mocker.patch.object(game, 'win_conditions')
        mwin.side_effect = lambda _ : setattr(mdata, 'win_cond',
                                              gi.WinCond.WIN)

        mdata = game._move(1)
        assert mdata.win_cond is gi.WinCond.WIN

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

    @pytest.mark.parametrize('winner, move_turn',
                             [(False, False),
                              (True, False),
                              (False, True),
                              (True, True),
                              ])
    @pytest.mark.parametrize('win_cond', gi.WinCond)
    def test_log_move(self, mocker, game, winner, move_turn, win_cond,
                      logger):
        """Test conditions of turn logging.
        This is pretty specific to the actual log text;
        code changes might break it."""

        assert game_logger.game_log.active

        mdata = utils.make_win_mdata(game, win_cond, winner)
        mdata.player = move_turn
        mdata.move = 1
        mdata.win_cond = win_cond

        mlog = mocker.patch.object(game_logger.game_log, 'turn')
        game._log_turn(mdata)

        arg_str = mlog.call_args.args[1]

        assert win_cond.name in arg_str
        assert 'move 1' in arg_str
        if move_turn:
            assert gi.PLAYER_NAMES[True] + ' move' in arg_str
        else:
            assert gi.PLAYER_NAMES[False] + ' move' in arg_str
        if 'WIN' in arg_str:
            if winner:
                assert 'by ' + gi.PLAYER_NAMES[True] in arg_str
            else:
                assert 'by ' + gi.PLAYER_NAMES[False] in arg_str


    @pytest.mark.parametrize('move', [gi.MoveTpl(2, None),
                                      gi.MoveTpl(2, gi.Direct.CW)])
    def test_log_move_tpl(self, mocker, game, move, logger):
        """Test the setting of the direction in the move."""

        assert game_logger.game_log.active

        mdata = move_data.MoveData(game, move)
        mdata.direct = gi.Direct.CCW
        mdata.player = True
        mdata.win_cond = None

        mlog = mocker.patch.object(game_logger.game_log, 'turn')
        game._log_turn(mdata)

        arg_str = mlog.call_args.args[1]
        assert '(2, CCW)' in arg_str


    def test_log_move_inactive(self, mocker, game):
        """Test with logger in inactive."""

        assert not game_logger.game_log.active

        mlog = mocker.patch.object(game_logger.game_log, 'turn')
        game._log_turn(move_data.MoveData())

        mlog.assert_not_called()


class TestBadNewRound:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(goal=Goal.TERRITORY,
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
        game_info = gi.GameInfo(goal=Goal.TERRITORY,
                                goal_param=8,
                                child_type = gi.ChildType.NORMAL,
                                child_cvt=4,
                                evens=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)
        game.turn = False


        dbl_size = size * 2
        game.board = list(range(dbl_size))
        game.owner[0] = True
        game.owner[dbl_size - 1] = False
        game.child[size] = True
        game.child[size - 1] = False
        game.store = [4, 6]

        print(game)
        game.swap_sides(is_turn=size == 4)
        print(game)

        if size == 4:
            assert game.board == [4, 5, 6, 7, 0, 1, 2, 3]
            assert game.store == [6, 4]
            # assert game.owner == [T, T, T, F, T, F, F, F]
            assert game.child == [T, N, N, N, N, N, N, F]

            assert game.turn
            assert game.movers
            assert game.mcount > 1

        elif size == 5:
            assert game.board == [5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
            assert game.store == [6, 4]
            # assert game.owner == [T, T, T, T, F, T, F, F, F, F]
            assert game.child == [T, N, N, N, N, N, N, N, N, F]

            assert not game.turn
            assert not game.movers
            assert game.mcount == 1


    @pytest.mark.parametrize('size', [4, 5])
    def test_swap_locks(self, size):
        # test board, stores, locks and blocks

        game_consts = gconsts.GameConsts(nbr_start=4, holes=size)
        game_info = gi.GameInfo(goal=Goal.MAX_SEEDS,
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


class TestAnimatorHooks:

    @pytest.mark.animator
    def test_ahooks(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(goal=Goal.MAX_SEEDS,
                                rounds=gi.Rounds.NO_MOVES,
                                blocks=True,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=4,
                                moveunlock=True,
                                evens=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        assert isinstance(game.board, animator.AniList)
        assert isinstance(game.store, animator.AniList)
        assert isinstance(game.unlocked, animator.AniList)
        assert isinstance(game.blocked, animator.AniList)
        assert isinstance(game.child, animator.AniList)


    @pytest.mark.animator
    def test_ahooks_mixed_1(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(goal=Goal.MAX_SEEDS,
                                rounds=gi.Rounds.NO_MOVES,
                                blocks=True,
                                moveunlock=True,
                                evens=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        assert isinstance(game.board, animator.AniList)
        assert isinstance(game.store, animator.AniList)
        assert isinstance(game.unlocked, animator.AniList)
        assert isinstance(game.blocked, animator.AniList)
        assert isinstance(game.child, list)

    @pytest.mark.animator
    def test_ahooks_mixed_2(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(goal=Goal.MAX_SEEDS,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=4,
                                evens=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        assert isinstance(game.board, animator.AniList)
        assert isinstance(game.store, animator.AniList)
        assert isinstance(game.unlocked, list)
        assert isinstance(game.blocked, list)
        assert isinstance(game.child, animator.AniList)


    def test_no_ahooks(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(goal=Goal.MAX_SEEDS,
                                rounds=gi.Rounds.NO_MOVES,
                                blocks=True,
                                child_type=gi.ChildType.NORMAL,
                                child_cvt=4,
                                moveunlock=True,
                                evens=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        game = mancala.Mancala(game_consts, game_info)

        assert isinstance(game.board, list)
        assert isinstance(game.store, list)
        assert isinstance(game.unlocked, list)
        assert isinstance(game.blocked, list)
        assert isinstance(game.child, list)


class TestOppTurn:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(evens=True,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    @pytest.mark.parametrize('turn', [False, True])
    def test_normal(self, game, turn):

        game.turn = turn

        with game.opp_turn():
            game.turn = 12

        assert game.turn == turn


class TestFindChildStores:

    @pytest.fixture
    def game(self):

        game_consts = gconsts.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(child_type = gi.ChildType.NORMAL,
                                child_cvt=4,
                                evens=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)
        return mancala.Mancala(game_consts, game_info)


    CASES = [((N, N, N, N, N, N), (None, None)),
             ((F, F, N, N, N, N), (0, None)),
             ((N, N, N, N, T, T), (None, 4)),
             ((N, N, N, F, T, T), (3, 4)),
             ((T, T, T, F, F, F), (3, 0)),
             ]


    @pytest.mark.parametrize('child, elocs', CASES)
    def test_find_child_stores(self, game, child, elocs):

        game.child = list(child)
        assert game.find_child_stores() == list(elocs)
