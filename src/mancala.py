# -*- coding: utf-8 -*-
"""Mancala contains the game dynamics of the mancala player.
It does not contain any UI elements or any specific ai (computer)
player information.

Created on Sun Mar 19 09:58:36 2023
@author: Ann"""

import dataclasses as dc
import pprint
import random

import ai_interface
import allowables
import capt_ok
import capturer
import cfg_keys as ckey
import end_move
import game_constants as gc
import game_interface as gi
import game_str
import get_direction
import get_moves
import ginfo_rules
import inhibitor
import incrementer
import new_game
import sow_starter
import sower

from fill_patterns import PCLASSES
from game_log import game_log


LOCK = ['_', ' ']
CHILD = {True: '˄',
         False: '˅',
         None: ' '}
OWNER = {True: '\u2191 ',
         False: '\u2193 ',
         None: ' '}


@dc.dataclass(frozen=True, kw_only=True)
class GameState(ai_interface.StateIf):
    """A simplified immuatble game state but enough to save
    and restore the game state.
    Use this instead of copying the Mancala class, copying
    all of the deco's is slow due to recursive references."""

    board: tuple
    store: tuple
    mcount: int
    _turn: bool

    unlocked: tuple = None
    blocked: tuple = None
    child: tuple = None
    owner: tuple = None

    @property
    def turn(self):
        return self._turn

    def __str__(self):

        dbl_holes = len(self.board)
        holes = dbl_holes // 2

        string = f'Move number: {self.mcount}\n'
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


class MoveData:
    """A place to collect premove and move data.
    This is so the sower and capture can share some data.

                   from       from
    Field          Starter    Get Direct   Sower        Capturer
    -----          -------   -----------   -----        --------
    board                                               note 1
    move
    direct                    fill         input        input
    seeds          fill                    input        note 2
    _sow_loc       fill                                 note 3
    cont_sow_loc   property fills          in/update
    capt_loc                               output       in/update
    capt_change                                         filled
    captured                                            filled

    note 1: board is used to determine if a grand slam is possible
    e.g. there must be seeds on oppside before the turn

    note 2: the number seeds being sown, used in NoSignleSeedCapt

    note 3: the original start location"""

    def __init__(self, game, move):

        self.board = tuple(game.board)   # pre-move state
        self.move = move
        self.direct = None   # an intentionally invalid direction
        self.seeds = 0
        self._sow_loc = 0
        self.cont_sow_loc = 0   # use by the sower (updated for lap sows)
        self.capt_loc = 0

        self.capt_changed = False    # capt changed state but didn't capture
        self.captured = False       # there was an actual capture
        self.end_msg = None

    def __str__(self):

        string = f"MoveData({self.board}, {self.move}):\n"
        string += f"  direct={self.direct}\n"
        string += f"  seeds={self.seeds}\n"
        string += f"  sow_loc={self.sow_loc}\n"
        string += f"  cont_sow_loc={self.cont_sow_loc}\n"
        string += f"  capt_loc={self.capt_loc}\n"
        string += f"  capt_changed={self.capt_changed}\n"
        string += f"  captured={self.captured}"
        string += f"  end_msg={self.end_msg}"
        return string

    @property
    def sow_loc(self):
        """sow_loc property"""
        return self._sow_loc

    @sow_loc.setter
    def sow_loc(self, value):
        """When sow_loc is set, also set the cont_sow_loc
        for the capturer."""
        self._sow_loc = value
        self.cont_sow_loc = value


class ManDeco:
    """Collect the decorator chains into one variable,
    build them all together.

    Decorator chains can save data unique to the game
    on startup/creation, but they should not store
    state data that would be changed during the game.
    Decos are not told about a new game or round
    being started.

    The inhibitor deco is told re-initialized."""

    def __init__(self, game):

        self.new_game = new_game.deco_new_game(game)
        self.allow = allowables.deco_allowable(game)
        self.moves = get_moves.deco_moves(game)
        self.incr = incrementer.deco_incrementer(game)
        self.starter = sow_starter.deco_sow_starter(game)
        self.get_dir = get_direction.deco_dir_getter(game)
        self.sower = sower.deco_sower(game)
        self.ender = end_move.deco_end_move(game)
        self.quitter = end_move.deco_quitter(game)
        self.capt_ok = capt_ok.deco_capt_ok(game)
        self.capturer = capturer.deco_capturer(game)
        self.gstr = game_str.deco_get_string(game)
        self.inhibitor = inhibitor.deco_inhibitor(game)
        self.make_child = self.gen_child_test(game)


    @staticmethod
    def gen_child_test(game):
        """Generate a test function that will return True
        if a child should be made. Used in the sower to stop
        mlap sowing. Used in the capturer to make children
        and bulls, but not waldas, wegs or tuzdeks.

        The result is the ANDing of each functions return value."""

        def base_case(game, mdata):
            loc = mdata.capt_loc
            return (game.child[loc] is None
                    and game.board[loc] == game.info.child_cvt)

        def weg_case(game, mdata):
            loc = mdata.capt_loc
            return not (game.board[loc] == game.info.child_cvt
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


class Mancala(ai_interface.AiGameIf, gi.GameInterface):
    """Implement the dynamics of a wide variety of mancala games.
    Details of the game are defined in the game_constants and
    game_info parameters.

    The board is represented so that the next cell to sow or
    capture is +- away from the current location.

    All game interface calls and responses will be 0, 0 upper/left of
    display to 1, holes bottom/right of display.

    |      bottom : False   |     top : True        |    Turn
    | 0 | 1 | 2 | 3 | 4 | 5 | 5 | 4 | 3 | 2 | 1 | 0 |    Location

    store [ bottom/False,  top/True ]
    turn = bottom/False,  top/True"""
    # pylint: disable=too-many-public-methods

    rules = ginfo_rules.build_rules()

    def __init__(self, game_consts, game_info):

        if not isinstance(game_consts, gc.GameConsts):
            raise TypeError(
                'game_consts not built on game_constants.GameConsts.')
        if not isinstance(game_info, gi.GameInfo):
            raise TypeError('game_info not built on game_info.GameInfo.')

        if game_info.start_pattern:
            game_consts.adjust_total_seeds(
                PCLASSES[game_info.start_pattern].nbr_seeds(
                    game_consts.holes,
                    game_consts.nbr_start))

        if (game_info.goal == gi.Goal.TERRITORY
                or game_info.round_fill
                    in (gi.RoundFill.UMOVE, gi.RoundFill.SHORTEN)):
            game_consts.set_win_all_seeds()

        self.cts = game_consts
        self.info = game_info

        self.board = [self.cts.nbr_start] * self.cts.dbl_holes
        self.store = [0, 0]
        self.mcount = 0
        self.turn = random.choice([False, True])
        self.starter = self.turn
        self.last_mdata = None

        self.deco = ManDeco(self)
        self.init_bprops()

        if game_info.start_pattern:
            self.deco.new_game.new_game(None, False)


    def __str__(self):
        """Ascii print of board for game logs."""
        return self.deco.gstr.get_string()


    @property
    def state(self):
        """Return an immutable copy of the state variables,
        these must be able to completely return the game
        state to a previous position.
        Always return stores, because they may be used
        even if not displayed (e.g. Deka).
        If the lists aren't used don't include them."""

        state_dict = {'board': tuple(self.board),
                      '_turn': self.turn,
                      'store': tuple(self.store),
                      'mcount': self.mcount}

        if self.info.moveunlock:
            state_dict |= {'unlocked': tuple(self.unlocked)}

        if self.info.blocks:
            state_dict |= {'blocked': tuple(self.blocked)}

        if self.info.child_cvt:
            state_dict |= {'child': tuple(self.child)}

        if self.info.goal == gi.Goal.TERRITORY:
            state_dict |= {'owner': tuple(self.owner)}

        return GameState(**state_dict)


    @state.setter
    def state(self, value):
        """Copy the state variables back, convert the tuples
        back to lists."""

        self.board = list(value.board)
        self.store = list(value.store)
        self.turn = value.turn
        self.mcount = value.mcount

        if value.child:
            self.child = list(value.child)
        if value.blocked:
            self.blocked = list(value.blocked)
        if value.unlocked:
            self.unlocked = list(value.unlocked)
        if value.owner:
            self.owner = list(value.owner)


    def init_bprops(self):
        """Initialize the board properties but not the board or stores."""

        holes = self.cts.holes
        dbl_holes = self.cts.dbl_holes

        self.mcount = 0
        locks = not self.info.moveunlock
        self.unlocked = [locks] * dbl_holes
        self.blocked = [False] * dbl_holes
        self.child = [None] * dbl_holes

        if self.info.goal == gi.Goal.TERRITORY:
            self.owner = [False] * holes + [True] * holes
        else:
            self.owner = [None] * dbl_holes
        self.deco.inhibitor.new_game()


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


    def get_game_info(self):
        """Return the GameInfo."""
        return self.info


    def get_board(self, loc):
        """Return the seeds at location."""
        return self.board[loc]


    def set_board(self, loc, seeds):
        """Set the seeds at location."""
        self.board[loc] = seeds


    def get_store(self, row):
        """Return the number of seeds in the store for side.
        row : 0 for top row, 1 for bottom  (opposite of player)"""
        return self.store[(row + 1) % 2]


    def set_store(self, row, seeds):
        """Set the store seeds of owner."""
        self.store[(row + 1) % 2] = seeds


    def set_blocked(self, loc, blocked):
        """Set the blocked status location."""
        self.blocked[loc] = blocked


    def compute_owners(self):
        """Compute the number of holes that False should own
        based on number of seeds. Called on new round for
        Territory game.
        Seeds have already been collected from non-children"""

        # XXXX I think there's duplication of this collection
        seeds = self.store.copy()
        for loc in range(self.cts.dbl_holes):
            if self.child[loc] is True:
                seeds[True] += self.board[loc]
            elif self.child[loc] is False:
                seeds[False] += self.board[loc]

        nbr_start = self.cts.nbr_start
        false_holes, rem = divmod(seeds[False], nbr_start)
        if rem > nbr_start // 2:
            false_holes += 1
        game_log.add(f"False holes = {false_holes}", game_log.DETAIL)

        return false_holes, seeds


    def new_game(self, win_cond=None, new_round_ok=False):
        """Delegate to the new_game decorators.
        Return False if it a new round was started.
        True if a new game was started."""
        return self.deco.new_game.new_game(win_cond, new_round_ok)


    def end_game(self):
        """Either the player has requested that the game be ended
        or an ENDLESS conditions was detected.  End the game fairly."""

        cond, winner = self.deco.quitter.game_ended(repeat_turn=False,
                                                    ended=True)
        self.turn = winner
        return cond


    def win_conditions(self, repeat_turn=False, ended=False):
        """Check for end game.
        Return None if no victory/tie conditions are met.
        If there is a winner, set turn to that player."""

        cond, winner = self.deco.ender.game_ended(repeat_turn=repeat_turn,
                                                  ended=ended)
        if cond:
            self.turn = winner
            return cond
        return None


    def win_message(self, win_cond):
        """Return a game appropriate win message based on WinCond.
        Return a window title and message string."""

        reason = ("by collecting the most seeds!",
                  "by eliminating their opponent's seeds.",
                  "by claiming more holes.")

        rtext = 'the game'
        gtext = 'Game'
        title = 'Game Over'
        if win_cond in (gi.WinCond.ROUND_WIN, gi.WinCond.ROUND_TIE):
            rtext = 'the round'
            gtext = 'The round'
            title = 'Round Over'

        message = ''
        if self.last_mdata and self.last_mdata.end_msg:
            message = self.last_mdata.end_msg

        if win_cond in [gi.WinCond.WIN, gi.WinCond.ROUND_WIN]:
            player = 'Top' if self.turn else 'Bottom'
            message += f'{player} won {rtext} {reason[self.info.goal]}'

        elif win_cond in [gi.WinCond.TIE, gi.WinCond.ROUND_TIE]:
            if self.info.goal == gi.Goal.MAX_SEEDS:
                message += f'{gtext} ended in a tie.'
            elif self.info.goal == gi.Goal.DEPRIVE:
                message += 'Both players ended with seeds; consider it a tie.'
            elif self.info.goal == gi.Goal.TERRITORY:
                message += 'Each player controls half the holes (a tie).'

        elif win_cond == gi.WinCond.ENDLESS:
            message += 'Game stuck in a loop. No winner.'

        else:
            message += f'Unexpected end condition {win_cond}.'

        return title, message


    def do_sow(self, move):
        """Do the sowing steps:

        2. deal with first hole, getting start loc, seeds to sow, and
        sow start if specified.
        3. get sow direction
        4. sow the seeds, return updated mdata

        RETURN move data"""

        mdata = MoveData(self, move)
        mdata.sow_loc, mdata.seeds = self.deco.starter.start_sow(move)
        mdata.direct = self.deco.get_dir.get_direction(move, mdata.sow_loc)
        self.deco.sower.sow_seeds(mdata)

        game_log.step(f'Sow from {mdata.sow_loc}', self)
        return mdata


    def do_single_sow(self, move):
        """For move simulation, just do the a single sow."""

        mdata = MoveData(self, move)
        mdata.sow_loc, mdata.seeds = self.deco.starter.start_sow(move)
        mdata.direct = self.deco.get_dir.get_direction(move, mdata.sow_loc)
        single_sower = self.deco.sower.get_single_sower()
        single_sower.sow_seeds(mdata)
        return mdata


    def capture_seeds(self, mdata):
        """Hand off the capture to the capturer deco;
        update the game log on return."""

        self.deco.capturer.do_captures(mdata)

        loc = mdata.capt_loc
        if mdata.captured:
            game_log.step(f'Capture from {loc}', self)
        elif mdata.capt_changed:
            game_log.step('Capture changed state', self)
        else:
            game_log.step(f'No captures @ {loc}')


    def _move(self, move):
        """Do the move:

        1. if PASS, swap turn and do nothing else
        Call do_sow for steps 2 to 4
        5. capture seeds
        6. if either player won or a tie occured, return that condition
        7. swap the turn and return None (game continues)

        On the assert, sum the stores even if they are not 'in play'
        (for Deka)."""
        self.mcount += 1
        assert sum(self.store) + sum(self.board) == self.cts.total_seeds, \
            'seed count error before move'

        if move == gi.PASS_TOKEN:
            self.turn = not self.turn
            return None

        mdata = self.do_sow(move)
        self.last_mdata = mdata   # keep this around for the win message

        if mdata.capt_loc is gi.WinCond.REPEAT_TURN:
            win_cond = self.win_conditions(repeat_turn=True)
            return win_cond if win_cond else gi.WinCond.REPEAT_TURN

        if mdata.capt_loc is gi.WinCond.ENDLESS:
            cond = self.end_game()
            mdata.end_msg = \
                'Game ended due to detecting endless sow condition.\n'
            game_log.add(f'MLAP game ENDLESS, called end_game {cond}.',
                         game_log.IMPORT)
            return cond

        self.capture_seeds(mdata)

        if mdata.captured == gi.WinCond.REPEAT_TURN:
            win_cond = self.win_conditions(repeat_turn=True)
            return win_cond if win_cond else gi.WinCond.REPEAT_TURN

        self.deco.inhibitor.clear_if(self, mdata)

        win_cond = self.win_conditions()
        if win_cond:
            return win_cond

        self.turn = not self.turn
        return None


    def _log_turn(self, move_turn, move, win_cond):
        """Add to the play log and move history for the move."""

        wtext = ''
        if win_cond in (gi.WinCond.WIN, gi.WinCond.ROUND_WIN):
            sturn = 'Top' if self.get_turn() else 'Bottom'
            wtext = f'\n{win_cond.name} by {sturn}'
        elif win_cond:
            wtext = ' ' + win_cond.name

        sturn = 'Top' if move_turn else 'Bottom'
        move_desc = f'{sturn} move {move}{wtext}'

        game_log.turn(self.mcount, move_desc, self)


    def move(self, move):
        """Call the _move method to do most of the work
        (move has several returns this wraps them all),
        log the turn here."""

        cur_turn = self.turn
        wcond = self._move(move)
        self._log_turn(cur_turn, move, wcond)
        return wcond


    def test_pass(self):
        """If no valid moves, swap turn and return True.
        Can't put this in move or it will break the AiPlayer.

        If simulating games, call this after checking the
        return value of move."""

        if self.info.mustpass and not any(self.get_allowable_holes()):
            self.turn = not self.turn
            self._log_turn(not self.turn, 'PASS', None)
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


    def get_turn(self):
        """Return current turn."""
        return self.turn


    def get_allowable_holes(self):
        """Determine what holes are legal moves."""
        return self.deco.allow.get_allowable_holes()


    def get_moves(self):
        """Return the list of allowable moves."""
        return self.deco.moves.get_moves()
