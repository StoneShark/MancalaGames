# -*- coding: utf-8 -*-
"""Mancala contains the game dynamics of the mancala player.
It does not contain any UI elements or any specific ai (computer)
player information.

See Mancala class doc string for board representation and
index/variable naming conventions.

Created on Sun Mar 19 09:58:36 2023
@author: Ann"""

import contextlib
import dataclasses as dc
import pprint
import random

import ai_interface
import allowables
import animator
import capt_ok
import capturer
import cfg_keys as ckey
import drawer
import end_move
import game_constants as gconsts
import game_interface as gi
import game_str
import get_direction
import get_moves
import ginfo_rules
import inhibitor
import incrementer
import make_child
import man_end_msgs_mixin
import move_data
import new_game
import round_tally
import sower

from fill_patterns import PCLASSES
from game_logger import game_log


LOCK = ['_', ' ']
CHILD = {True: '˄',
         False: '˅',
         None: ' '}
OWNER = {True: '↑ ',     # \u2191
         False: '↓ ',    # \u2193
         None: ' '}


@dc.dataclass(frozen=True, kw_only=True)
class GameState(ai_interface.StateIf):
    """A simplified immuatble game state but enough to save
    and restore the game state.
    Use this instead of copying the Mancala class, copying
    all of the deco's is slow due to recursive references."""

    board: tuple
    store: tuple
    mcount: int = 1
    movers: int = 0
    _turn: bool
    rturn_cnt: int = 0

    unlocked: tuple = None
    blocked: tuple = None
    child: tuple = None
    owner: tuple = None

    istate: tuple = None
    rtally_state: tuple = None
    mdata_state: tuple = None

    @property
    def turn(self):
        return self._turn

    def __str__(self):

        dbl_holes = len(self.board)
        holes = dbl_holes // 2

        string = f'Move number: {self.mcount}  '
        string += f'Movers: {self.movers}  '
        string += f'Repeat count: {self.rturn_cnt}\n'
        for side, side_range in enumerate([range(dbl_holes - 1, holes - 1, -1),
                                           range(holes)]):
            for loc in side_range:

                if self.blocked and self.blocked[loc]:
                    string += '  x'
                else:
                    string += f' {self.board[loc]:2}'
                if self.owner:
                    string += OWNER[self.owner[loc]]
                if self.unlocked:
                    string += LOCK[self.unlocked[loc]]
                if self.child:
                    string += CHILD[self.child[loc]]

            string += '  *' if int(not self.turn) == side else '   '
            loc = (side + 1) % 2
            string += f'  {self.store[loc]:3}' \
                      if self.store[loc] else ''
            if not side:
                string += '\n'
        return string


    def str_one(self):
        """Return a one line summary of the state"""

        string = f'    {self.mcount:3} {self.turn:3} '
        string += f'{str(self.store):8} {self.board}'
        return string


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
        in the deco_name chain.

        This is used in game classes derived from Mancala."""

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
        """insert the new_deco before the deco of type post_class
         in the deco_name chain.

        This is used in game classes derived from Mancala."""

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


class Mancala(ai_interface.AiGameIf,
              man_end_msgs_mixin.ManMsgsMixin):
    """Implement the dynamics of a wide variety of mancala games.
    Details of the game are defined in the game_constants and
    game_info parameters.

    All game interface calls and responses will be (row, pos),
    e.g. (0, 0) upper/left of display to (1, holes) bottom/right of display.

    The board is represented so that the next cell to sow or
    capture is +- away from the current location.

    Board index conventions for game logic:

    |      bottom : False   |     top : True          | Turn
    |      bottom : 1       |     top : 0             | row
    | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | loc
    | 0 | 1 | 2 | 3 | 4 | 5 | 5 | 4 | 3 | 2 |  1 |  0 | pos
    | 0 | 1 | 2 | 3 | 4 | 5 | 0 | 1 | 2 | 3 |  4 |  5 | cnt (from player left)

    store [ bottom/False,  top/True ]
    turn = bottom/False,  top/True"""
    # pylint: disable=too-many-public-methods

    @classmethod
    def rules(cls, ginfo, holes, skip=None):
        """Test the rules. This is run before the game class
        is created."""
        ginfo_rules.test_rules(ginfo, holes, skip)


    def __init__(self, game_consts, game_info):

        if not isinstance(game_consts, gconsts.GameConsts):
            raise TypeError(
                'game_consts not built on game_constants.GameConsts.')
        if not isinstance(game_info, gi.GameInfo):
            raise TypeError('game_info not built on game_info.GameInfo.')

        if game_info.start_pattern:
            game_consts.adjust_total_seeds(
                PCLASSES[game_info.start_pattern].nbr_seeds(
                    game_consts.holes,
                    game_consts.nbr_start))

        self.cts = game_consts
        self.info = game_info

        self.board = [self.cts.nbr_start] * self.cts.dbl_holes
        self.store = [0, 0]
        self.unlocked = []
        self.blocked = []
        self.child = []
        self.owner = []
        self.mcount = 1      # count of moves
        self.movers = 0      # count of players that have moved
        self.rturn_cnt = 0    # repeat turns for one move
        self.turn = random.choice([False, True])
        self.starter = self.turn    # starter of current round
        self.mdata = None
        self.inhibitor = inhibitor.make_inhibitor(self)

        self.rtally = None
        if self.info.goal in round_tally.RoundTally.GOALS:
            self.rtally = round_tally.RoundTally(self.info.goal,
                                                 self.info.goal_param,
                                                 self.cts.total_seeds)

        self.deco = ManDeco(self)
        self.deco.new_game.new_game()


    def __str__(self):
        """Ascii print of board for game logs."""
        return self.deco.gstr.get_string()


    @property
    def board(self):
        """Hide the actual board in this property. It might be
        a simple list or animator list.
        _board should not be accessed except by the property methods."""
        return self._board

    @board.setter
    def board(self, value):

        if animator.ENABLED:
            self._board = animator.AniList('board', value)

        else:
            self._board = value


    @property
    def store(self):
        """Hide the actual store in this property. It might be
        a simple list or animator list.  Use the animator list
        if we want to animate the assignments.
        _store should not be accessed except by the property methods."""
        return self._store

    @store.setter
    def store(self, value):

        if animator.ENABLED and self.info.stores:
            self._store = animator.AniList('store', value)

        else:
            self._store = value


    @property
    def unlocked(self):
        """Hide the actual unlocked list in this property. It might be
        a simple list or animator list.  Use the animator list
        if we want to animate the assignments.
        _unlocked should not be accessed except by the property methods."""
        return self._unlocked

    @unlocked.setter
    def unlocked(self, value):

        if (animator.ENABLED
                and (self.info.moveunlock
                     or self.info.allow_rule ==
                               gi.AllowRule.MOVE_ALL_HOLES_FIRST)):
            self._unlocked = animator.AniList('unlocked', value)

        else:
            self._unlocked = value


    @property
    def blocked(self):
        """Hide the actual blocked list in this property. It might be
        a simple list or animator list.  Use the animator list
        if we want to animate the assignments.
        _blocked should not be accessed except by the property methods."""
        return self._blocked

    @blocked.setter
    def blocked(self, value):

        if animator.ENABLED and self.info.blocks:
            self._blocked = animator.AniList('blocked', value)

        else:
            self._blocked = value


    @property
    def child(self):
        """Hide the actual child list in this property. It might be
        a simple list or animator list. Use the animator list
        if we want to animate the assignments.
        _child should not be accessed except by the property methods."""
        return self._child

    @child.setter
    def child(self, value):

        if animator.ENABLED and self.info.child_type:
            self._child = animator.AniList('child', value)

        else:
            self._child = value


    @property
    def state(self):
        """Return an immutable copy of the state variables,
        these must be able to completely return the game
        state to a previous position."""

        unlocked = None
        if (self.info.moveunlock
                or self.info.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST):
            unlocked = tuple(self.unlocked)

        blocked = None
        if self.info.blocks:
            blocked = tuple(self.blocked)

        child = None
        if self.info.child_type:
            child = tuple(self.child)

        owner = None
        if self.info.goal == gi.Goal.TERRITORY:
            owner = tuple(self.owner)

        return GameState(
            board=tuple(self.board),
            _turn=self.turn,
            store=tuple(self.store),
            mcount=self.mcount,
            movers=self.movers,
            rturn_cnt=self.rturn_cnt,
            unlocked=unlocked,
            blocked=blocked,
            child=child,
            owner=owner,
            istate=self.inhibitor.get_state(),
            rtally_state=self.rtally.state if self.rtally else None,
            mdata_state=self.mdata.state if self.mdata else None,
            )


    @state.setter
    def state(self, value):
        """Copy the state variables back, convert the tuples
        back to lists."""

        self.board = list(value.board)
        self.store = list(value.store)
        self.turn = value.turn
        self.mcount = value.mcount
        self.movers = value.movers
        self.rturn_cnt = value.rturn_cnt

        if value.child:
            self.child = list(value.child)
        if value.blocked:
            self.blocked = list(value.blocked)
        if value.unlocked:
            self.unlocked = list(value.unlocked)
        if value.owner:
            self.owner = list(value.owner)

        self.inhibitor.set_state(value.istate)

        if value.rtally_state:
            self.rtally.state = value.rtally_state

        if value.mdata_state:
            if not self.mdata:
                self.mdata = move_data.MoveData()
            self.mdata.state = value.mdata_state

        else:
            self.mdata = None


    @contextlib.contextmanager
    def save_restore_state(self):
        """A context manager that saves and restores state."""

        saved_state = self.state
        game_log.set_simulate()

        try:
            yield
        finally:
            game_log.clear_simulate()
            self.state = saved_state


    @contextlib.contextmanager
    def restore_state(self, state):
        """Use this when you've saved the state, but might want
        to restore it serveral times. For example,in a loop:

            saved = game.state
            for thing in things:
                with game.restore_state(saved):
                    <code block>

        All exits from code block will restore the state."""

        yield
        self.state = state


    @property
    def board_state(self):
        """Return an immutable copy of the board state variables,
        but only those that unique identify the board position.
        Do not include any dynamic move information.

        This state is smaller and suitable for use in detecting
        repeating game situations. It must not be used to restore
        state information in games that require the hidden state
        information. This includes games that use game.mdata directly
        (not passed as parameter), mcount, movers, rturn_cnt,
        or an inhibitor other than InhibitorNone.

        See limitations on monte carlo tree search game rule
        in ai_player.py: mcts_no_hidden_state.
        This is also used in the 'loop' detector in the analysis
        scripts."""

        unlocked = None
        if (self.info.moveunlock
                or self.info.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST):
            unlocked = tuple(self.unlocked)

        blocked = None
        if self.info.blocks:
            blocked = tuple(self.blocked)

        child = None
        if self.info.child_type:
            child = tuple(self.child)

        owner = None
        if self.info.goal == gi.Goal.TERRITORY:
            owner = tuple(self.owner)

        return GameState(
            board=tuple(self.board),
            _turn=self.turn,
            store=tuple(self.store),
            unlocked=unlocked,
            blocked=blocked,
            child=child,
            owner=owner,
            )


    def init_bprops(self):
        """Initialize the board properties but not the board or stores."""

        holes = self.cts.holes
        dbl_holes = self.cts.dbl_holes

        self.mcount = 1
        self.movers = 0
        self.rturn_cnt = 0

        if self.info.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST:
            locks = False
        else:
            locks = not self.info.moveunlock
        self.unlocked = [locks] * dbl_holes

        self.blocked = [False] * dbl_holes
        self.child = [None] * dbl_holes

        if self.info.goal == gi.Goal.TERRITORY:
            self.owner = [False] * holes + [True] * holes
        else:
            self.owner = [None] * dbl_holes
        self.inhibitor.new_game()


    def params_str(self):
        """Generate a string describing the game parameters.
        Delete duplicate/derived parameters and things that don't
        effect game play."""

        strings = ckey.GAME_CLASS + ': ' + self.__class__.__name__ + '\n'
        strings += repr(self.cts) + '\n'

        info_dict = dc.asdict(self.info)
        del info_dict[ckey.ABOUT]
        del info_dict[ckey.HELP_FILE]
        del info_dict[ckey.UDIRECT]
        del info_dict[ckey.MLENGTH]

        pprinter = pprint.PrettyPrinter(indent=4)
        strings += 'GameInfo\n'
        strings += pprinter.pformat(info_dict) + '\n'

        return strings


    def new_game(self, new_round=False):
        """Delegate to the new_game decorators"""

        self.deco.new_game.new_game(new_round)


    def end_game(self, *, quitter, user, game=True):
        """Either the player has requested that the game
        or round be ended or an ENDLESS conditions was detected.
        Use the appropriate ender/quitter to end the game."""

        if user or not game:
            self.mdata = move_data.MoveData(self)
            self.mdata.user_end = True
        self.mdata.ended = True if game else 'round'

        if quitter:
            self.deco.quitter.game_ended(self.mdata)
        else:
            self.deco.ender.game_ended(self.mdata)

        return self.mdata.win_cond


    def swap_sides(self):
        """Swap the board sides. This would implement a pie rule if
        mcount and turn are also swapped, but it's also used by
        board setup."""

        holes = self.cts.holes
        dholes = self.cts.dbl_holes

        self.board = self.board[holes:dholes] + self.board[0:holes]
        self.child = self.child[holes:dholes] + self.child[0:holes]
        self.blocked = self.blocked[holes:dholes] + self.blocked[0:holes]
        self.unlocked = self.unlocked[holes:dholes] + self.unlocked[0:holes]
        self.owner = self.owner[holes:dholes] + self.owner[0:holes]
        self.store = list(reversed(self.store))


    def is_new_round_playable(self):
        """Determine if the new round is not playable.
        Territory games with specific start_patterns or allow_rules
        might not be playable for the first player.

        Force a new game, if it is not."""

        if (self.info.goal == gi.Goal.TERRITORY
                and not any(self.get_allowable_holes())):

            game_log.add('New round not playable by starter.',
                         game_log.IMPORT)
            self.turn = not self.turn  # winner
            self.new_game()
            return False
        return True


    def rtally_param_func(self):
        """If we created a round tallier, return the
        func that get the param values."""

        if self.rtally:
            return self.rtally.parameter
        return None


    def win_conditions(self, mdata):
        """Check for end game."""

        self.deco.ender.game_ended(mdata)


    def do_sow(self, move, single=False):
        """Do the sowing steps

        2. deal with first hole, getting start loc, seeds to sow, and
        sow start if specified.
        3. get sow direction

        if single sower, with single sower; otherwise with deco.sower
        4. sow the seeds, return updated mdata

        RETURN move data"""

        mdata = move_data.MoveData(self, move)
        mdata.sow_loc, mdata.seeds = self.deco.drawer.draw(move)
        mdata.direct = self.deco.get_dir.get_direction(mdata)

        if single:
            single_sower = self.deco.sower.get_single_sower()
            single_sower.sow_seeds(mdata)
        else:
            self.deco.sower.sow_seeds(mdata)
        game_log.step(f'Sow from {mdata.sow_loc}', self)

        return mdata


    def sim_single_sow(self, move):
        """For move simulation, just do a single sow."""

        with game_log.simulate():
            mdata = self.do_sow(move, single=True)
        return mdata


    def capture_seeds(self, mdata):
        """Hand off the capture to the capturer deco;
        update the game log on return."""

        self.deco.capturer.do_captures(mdata)

        if mdata.captured == gi.WinCond.REPEAT_TURN:
            game_log.step(f'Capture from {mdata.capt_loc}', self)
            game_log.step('Capture: repeat turn')
        elif mdata.captured is True:
            game_log.step(f'Capture from {mdata.capt_loc}', self)
        elif mdata.capt_changed:
            game_log.step('Capture changed state', self)
        else:
            game_log.step(f'No captures @ {mdata.capt_loc}')


    def sim_sow_capt(self, move):
        """Simulate only the sowing and capturing steps.
        Do not call an ender"""

        with game_log.simulate():
            mdata = self.do_sow(move)

            if mdata.capt_loc not in (gi.WinCond.REPEAT_TURN,
                                      gi.WinCond.ENDLESS):
                self.capture_seeds(mdata)

        return mdata


    def _move(self, move):
        """Do the move:

        1. if PASS, swap turn and do nothing else
        Call do_sow for steps 2 to 4
        5. capture seeds
        6. if either player won or a tie occured, return that condition
        7. swap the turn

        On the assert, sum the stores even if they are not 'in play'
        (e.g. for Deka).

        Return the created mdata."""

        assert (all(cnt >= 0 for cnt in self.board + self.store)
                and sum(self.store) + sum(self.board) == self.cts.total_seeds
                ), f"seed count error before move\n{self.store}\n{self.board}"

        if move == gi.PASS_TOKEN:
            self.turn = not self.turn
            self.mcount += 1
            self.movers += 1
            return move_data.MoveData.pass_move(not self.turn)

        mdata = self.do_sow(move)
        self.mdata = mdata

        if not mdata.repeat_turn:

            if mdata.capt_loc == gi.WinCond.ENDLESS:
                mdata.win_cond = self.end_game(quitter=True, user=False)
                mdata.end_msg = \
                    'Game ended due to detecting endless sow condition.\n'
                game_log.add(
                    f'MLAP game ENDLESS, called end_game {mdata.win_cond}.',
                    game_log.IMPORT)
                mdata.ended = gi.WinCond.ENDLESS
                return mdata

            self.capture_seeds(mdata)
            if not mdata.repeat_turn:
                self.inhibitor.clear_if(self, mdata)

        # inc these here so that they are right for any calls to allow deco's
        self.mcount += 1
        if not mdata.repeat_turn:
            self.movers += 1

        self.win_conditions(mdata)
        if mdata.win_cond:
            return mdata

        if mdata.repeat_turn:
            self.rturn_cnt += 1
            mdata.win_cond = gi.WinCond.REPEAT_TURN
            return mdata

        self.turn = not self.turn
        self.rturn_cnt = 0
        return mdata


    def _log_turn(self, mdata):
        """Add to the play log and move history for the move.

        Rebuild the move with the direction computed be get_direction,
        which may have overridden an actual direction in the move tuple
        (or None)."""

        if not game_log.active:
            return

        wtext = ''
        if mdata.win_cond and mdata.win_cond.is_win():
            winner = gi.PLAYER_NAMES[mdata.winner]
            wtext = f'\n{mdata.win_cond.name} by {winner}'
        elif mdata.win_cond and mdata.win_cond.is_tie():
            wtext = ' \n' + mdata.win_cond.name
        elif mdata.win_cond:
            wtext = ' ' + mdata.win_cond.name

        sturn = gi.PLAYER_NAMES[mdata.player]
        if isinstance(mdata.move, gi.MoveTpl):
            move = mdata.move.set_dir(mdata.direct)
        else:
            move = mdata.move
        move_desc = f'{sturn} move {move}{wtext}'

        game_log.turn(self.mcount - 1, move_desc, self)


    def move(self, move):
        """Call the _move method to do most of the work
        (move has several returns this wraps them all),
        log the turn here."""

        mdata = self._move(move)
        self._log_turn(mdata)
        return mdata.win_cond


    def test_pass(self):
        """If no valid moves, swap turn and return True.
        Can't put this in move or it will break the AiPlayer.

        If simulating games, call this after checking the
        return value of move."""

        if self.info.mustpass and not any(self.get_allowable_holes()):
            self.mcount += 1
            self.movers += 1
            self.turn = not self.turn
            self._log_turn(move_data.MoveData.pass_move(not self.turn))
            return True
        return False


    def get_hole_props(self, row, pos):
        """return the number of seeds for side / position.
        row : 0 for top row, 1 for bottom   (opposite of player)
        position : 0 .. 5 from left to right"""

        loc = self.cts.xlate_pos_loc(row, pos)
        return gi.HoleProps(seeds=self.board[loc],
                            unlocked=self.unlocked[loc],
                            blocked=self.blocked[loc],
                            ch_owner=self.child[loc],
                            owner=self.owner[loc])


    @contextlib.contextmanager
    def opp_turn(self):
        """Do an operation for the opposite turn, return
        turn to the correct turn afterward."""

        saved = self.turn
        self.turn = not self.turn
        try:
            yield
        finally:
            self.turn = saved


    def get_turn(self):
        """Return current turn."""
        return self.turn


    def get_winner(self):
        """Return the game winner."""

        if self.mdata:
            return self.mdata.winner
        return None


    def get_allowable_holes(self):
        """Determine what holes are legal moves."""
        return self.deco.allow.get_allowable_holes()


    def disallow_endless(self, disallow):
        """Rebuild the allowable deco chain with or without
        the prohibition for endless sows."""

        self.deco.allow = allowables.deco_allowable(self, no_endless=disallow)


    def get_moves(self):
        """Return the list of allowable moves."""
        return self.deco.moves.get_moves()


    def turn_name(self):
        """Return the name of the current player."""

        return gi.PLAYER_NAMES[self.turn]
