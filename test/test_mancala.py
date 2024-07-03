# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 07:32:54 2023

@author: Ann


added these packages:

conda install pytest
conda install coverage
conda install pytest-cov
conda install -c spyder-ide spyder-unittest

To get branch coverage in Anaconda Prompt:

coverage run --branch -m pytest
coverage html

"""


# %% imports

import re

import pytest
pytestmark = pytest.mark.unittest

from context import game_constants as gc
from context import game_interface as gi
from context import game_log
from context import ginfo_rules
from context import mancala

from game_interface import ChildType
from game_interface import Direct
from game_interface import Goal
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
        'board, store, turn, unlocked, blocked, child, owner, ere_one, ere_two',
        [((1, 2, 3, 4), [0, 0], False,
          None, None, None, None,
          ' *4 +3 *', ' *1 +2 +\\* *'),
         ((1, 2, 3, 4), [2, 0], True,
           None, None, None, None,
           ' *4 +3 +\\* *', ' *1 +2 +2 *'),
         ((1, 2, 3, 4), [0, 2], True,
           None, None, None, None,
           ' *4 +3 +\\* +2 *', ' *1 +2 *'),
         ((1, 2, 3, 4), [0, 0], True,
          [T, F, F, T], None, None, None,
          ' *4 +3_ +\\* *', ' *1 +2_ *'),
         ((1, 2, 3, 4), [0, 0], True,
          None, [T, F, F, T], None, None,
          ' *x +3 +\\* *', ' *x +2 *'),
         ((1, 2, 3, 4), [0, 0], True,
          None, None, [T, F, N, N], None,
          ' *4 +3 +\\* *', ' *1˄ +2˅ *'),
         ((1, 2, 3, 4), [0, 0], True,
          [T, F, F, T], None, [T, F, N, N], None,
          ' *4 +3_ +\\* *', ' *1 ˄ +2_˅ *'),
         ((1, 2, 3, 4), [0, 0], True,
          [T, F, F, T], None, None, [T, F, N, N],
          ' *4 +3 *_ +\\* *', ' *1 *↑ +2↓ _ *'),
         ])
    def test_state_const(self, board, store, turn,
                         unlocked, blocked, child, owner,
                         ere_one, ere_two):

        state = mancala.GameState(board=board,
                                  store=store,
                                  _turn=turn,
                                  mcount=0,
                                  unlocked=unlocked,
                                  blocked=blocked,
                                  child=child,
                                  owner=owner)
        assert state.board == board
        assert state.store == store
        assert state._turn == turn
        assert state.turn == turn
        assert state.unlocked == unlocked
        assert state.blocked == blocked
        assert state.child == child
        assert state.owner == owner
        gstrs = str(state).split('\n')
        assert re.fullmatch(ere_one, gstrs[1])
        assert re.fullmatch(ere_two, gstrs[2])


    @pytest.fixture
    def game(self):
        """Game that has access to all of the state data.
        Turn off game_info rule checking by providing empty dict!"""

        game_consts = gc.GameConsts(nbr_start=4, holes=2)
        game_info = gi.GameInfo(capt_on = [2],
                                blocks=True,
                                rounds=True,
                                child_type=ChildType.NORMAL,
                                child_cvt=2,
                                goal=gi.Goal.TERRITORY,
                                moveunlock=True,
                                nbr_holes = game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        game = mancala.Mancala(game_consts, game_info)
        return game


    @pytest.mark.parametrize(
        'board, store, turn, unlocked, blocked, child, owner',
        [((1, 2, 3, 4), (0, 0), False, None, None, None, None),
         ((1, 2, 3, 4), (2, 0), True,  None, None, None, None),
         ((1, 2, 3, 4), (0, 2), True,  None, None, None, None),
         ((1, 2, 3, 4), (0, 0), True, (T, F, F, T), None, None, None),
         ((1, 2, 3, 4), (0, 0), True, None, (T, F, F, T), None, None),
         ((1, 2, 3, 4), (0, 0), True, None, None, (T, F, N, N), None),
         ((1, 2, 3, 4), (0, 0), True, (T, F, F, T), None, (T, F, N, N), None),
         ((1, 2, 3, 4), (0, 0), True, None, None, None, (T, F, F, T)),
         ])
    def test_getter(self, game, board, store, turn,
                    unlocked, blocked, child, owner):

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
            print(game.owner)
        else:
            # this will only effect capturing the state
            object.__setattr__(game.info, 'goal', gi.Goal.MAX_SEEDS)


        state = game.state
        print(state)

        assert state.board == board
        assert state.store == store
        assert state._turn == turn
        assert state.turn == turn
        assert state.unlocked == unlocked
        assert state.blocked == blocked
        assert state.child == child

        if owner:
            assert state.owner == owner
        else:
            assert not state.owner


    @pytest.mark.parametrize(
        'board, store, turn, unlocked, blocked, child, owner',
        [((1, 2, 3, 4), (0, 0), False, None, None, None, None),
         ((1, 2, 3, 4), (2, 0), True,  None, None, None, None),
         ((1, 2, 3, 4), (0, 2), True,  None, None, None, None),
         ((1, 2, 3, 4), (0, 0), True,  (T, F, F, T), None, None, None),
         ((1, 2, 3, 4), (0, 0), True,  None, (T, F, F, T), None, None),
         ((1, 2, 3, 4), (0, 0), True,  None, None, (T, F, N, N), None),
         ((1, 2, 3, 4), (0, 0), True,  (T, F, F, T), None, (T, F, N, N), None),
         ((1, 2, 3, 4), (0, 2), True,  None, None, None, (T, F, F, T)),
         ])
    def test_setter(self, game, board, store, turn,
                    unlocked, blocked, child, owner):

        game.state = mancala.GameState(board=board,
                                       store=store,
                                       _turn=turn,
                                       mcount=0,
                                       unlocked=unlocked,
                                       blocked=blocked,
                                       child=child,
                                       owner=owner)

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


class TestMoveData:

    @pytest.fixture
    def game(self):
        """basic game"""

        game_consts = gc.GameConsts(nbr_start=4, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_construct(self, game):

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

        game_consts = gc.GameConsts(nbr_start=4, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_deco(self, game):

        assert game.deco.new_game
        assert game.deco.allow
        assert game.deco.moves
        assert game.deco.incr
        assert game.deco.starter
        assert game.deco.get_dir
        assert game.deco.sower
        assert game.deco.ender
        assert game.deco.quitter
        assert game.deco.capt_ok
        assert game.deco.capturer
        assert game.deco.gstr
        assert game.deco.inhibitor
        assert game.deco.make_child

        dstr = str(game.deco)
        for field, value in vars(game.deco).items():
            assert field in dstr


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
            mancala.Mancala(gc.GameConsts(3, 5), None)

        with pytest.raises(TypeError):
            mancala.Mancala(None, min_game_if)

        with pytest.raises(TypeError):
            mancala.Mancala(gc.GameConsts(3, 5), min_game_if, 5)

    def test_min_params(self, min_game_if):

        mancala.Mancala(gc.GameConsts(3, 5), min_game_if)


    def test_start_pat(self):
        """All start patterns are tested with new_game.
        Here confirming that the proper changes were made once."""

        game_consts = gc.GameConsts(nbr_start=4, holes=4)
        game_info = gi.GameInfo(capt_on=[2],
                                start_pattern=gi.StartPattern.ALTERNATES,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)

        assert game.cts.total_seeds == 16
        assert game.board == [0, 4, 0, 4, 0, 4, 0, 4]


class TestBasicIfs:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(capt_on=[2],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        return game


    def test_board(self, game):

        assert all(game.get_board(loc) == 4 for loc in range(game.cts.holes))

        game.set_board(0, 2)
        assert game.get_board(0) == 2

        game.set_board(8, 5)
        assert game.get_board(8) == 5

        #                     0  1  2  3  4  5  6  7  8  9  0  1
        assert game.board == [2, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4]


    def test_store(self, game):

        assert game.store == [0, 0]
        game.set_store(0, 4)   # 1st param is row not turn
        assert game.store == [0, 4]
        game.set_store(1, 6)
        assert game.store == [6, 4]

        game.store = [3, 4]
        assert game.get_store(0) == 4
        assert game.get_store(1) == 3


    def test_blocks(self, game):

        assert not any(game.blocked)

        game.set_blocked(0, True)
        assert game.blocked[0]

        game.set_blocked(7, True)
        assert game.blocked[7]

        #                       0  1  2  3  4  5  6  7  8  9  0  1
        assert game.blocked == [T, F, F, F, F, F, F, T, F, F, F, F]


    def test_turn(self, game):

        # inited randomly but one of these
        assert game.get_turn() in [False, True]

        game.turn = False
        assert not game.get_turn()
        game.turn = True
        assert game.get_turn()


    def test_get_info(self, game):

        info = game.get_game_info()
        assert isinstance(info, gi.GameInfo)

        assert info.capt_on == [2]
        assert info.sow_direct == Direct.CCW


    def test_param_str(self, game):
        """Contents really isn't important, if a programmer
        doesn't complain"""

        game.params_str()


class TestDelegates:
    """Confirm delegates interfaces are, well, delegated.
    Set unique return values to confirm the game object
    returns the right data. """

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=4, holes=6)
        game_info = gi.GameInfo(capt_on=[2],
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

        assert game.do_single_sow(5) == 123
        mobj.assert_called_once_with(5, single=True)


    def test_dlg_do_sow(self, game, mocker):

        mstart = mocker.patch.object(game.deco.starter, 'start_sow')
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

        mstart = mocker.patch.object(game.deco.starter, 'start_sow')
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


    @pytest.mark.parametrize('capted', [True, False])
    @pytest.mark.parametrize('changed', [True, False])
    def test_dlg_capture_seeds(self, capsys, game, mocker, capted, changed):
        """Not really testing exactly what is put in the log."""

        mdata = mancala.MoveData(game, 4)
        mdata.capt_loc = 6
        mdata.captured = capted
        mdata.capt_changed = changed

        mobj = mocker.patch.object(game.deco.capturer, 'do_captures')
        mglog = mocker.patch.object(game_log.game_log, 'step')

        game.capture_seeds(mdata)

        mobj.assert_called_once()
        mglog.assert_called_once()


class TestWinHoles:

    @pytest.fixture
    def game(self):
        """basic game"""

        game_consts = gc.GameConsts(nbr_start=3, holes=2)
        game_info = gi.GameInfo(capt_on=[2],
                                nbr_holes=game_consts.holes,
                                rules=ginfo_rules.RuleDict())

        game = mancala.Mancala(game_consts, game_info)
        return game

    WH_CASES = [((0, 0, 0, 0), [6, 6], (N, N, N, N), None, 2),
                ((0, 0, 0, 0), [3, 3], (N, N, N, N), None, 2),
                ((0, 0, 0, 0), [9, 3], (N, N, N, N), False, 3),
                ((0, 0, 0, 0), [3, 9], (N, N, N, N), True, 3),
                ((0, 0, 0, 0), [3, 8], (N, N, N, N), True, 3),
                ((0, 0, 0, 0), [3, 7], (N, N, N, N), True, 2),
                ((0, 1, 1, 0), [3, 7], (N, T, F, N), True, 3),
                ]

    @pytest.mark.parametrize('board, store, child, winner, holes',
                             WH_CASES,
                             ids=[f'case_{cnbr}'
                                  for cnbr in range(len(WH_CASES))])
    def test_win_holes(self, game, board, store, child, winner, holes):

        game.board = board
        game.store = store
        game.child = child

        assert game.compute_win_holes() == (winner, holes)


class TestWinMessage:

    @pytest.fixture
    def maxgame(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(goal=Goal.MAX_SEEDS,
                                capt_on = [2],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def depgame(self):
        game_consts = gc.GameConsts(nbr_start=3, holes=6)
        game_info = gi.GameInfo(goal=Goal.DEPRIVE,
                                capt_on=[4],
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        return mancala.Mancala(game_consts, game_info)

    @pytest.fixture
    def tergame(self):
        game_consts = gc.GameConsts(nbr_start=3, holes=6)
        game_info = gi.GameInfo(goal=Goal.TERRITORY,
                                stores=True,
                                gparam_one=10,
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

        if wcond.name in ['WIN', 'ROUND_WIN']:
            if 'max' in game_fixt:
                assert 'most seeds' in message
            elif 'dep' in game_fixt:
                assert 'eliminating' in message
            elif 'ter' in game_fixt:
                assert 'claiming' in message
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

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(capt_on = [2],
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
