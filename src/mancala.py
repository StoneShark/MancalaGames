# -*- coding: utf-8 -*-
"""Mancala contains the game dynamics of the mancala player.
It does not contain any UI elements or any specific ai (computer)
player information.

See Mancala class doc string for board representation and
index/variable naming conventions.

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
    mcount: int
    _turn: bool
    rturn_cnt: int = 0

    unlocked: tuple = None
    blocked: tuple = None
    child: tuple = None
    owner: tuple = None

    istate: tuple = None
    rstate: tuple = None

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

    def clear_mcount(self):
        """Clear the move count from the game states used
        as dictionary keys in the node_dict of MonteCarloTS

        The move count should be accurate for the GameNode.state"""

        object.__setattr__(self, 'mcount', 0)
        return self

    def set_mcount_from(self, game):
        """Set the move number to match that in the game."""

        object.__setattr__(self, 'mcount', game.mcount)
        return self



class MoveData:
    """A place to collect premove and move data.
    This is so the sower and capture can share some data.

                   from       from
    Field          Starter    Get Direct   Sower        Capturer
    -----          -------   -----------   -----        --------
    board                                               note 1
    move
    direct                    fill         input        input
    seeds          fill                    in/update     note 2
    _sow_loc       fill                                 note 3
    cont_sow_loc   property fills          in/update
    lap_nbr                                used
    capt_loc                               output       in/update
    capt_next                                           fill/working
    capt_change                                         fill
    captured                                            fill

    note 1: board is used to determine if a grand slam is possible
    e.g. there must be seeds on oppside before the turn

    note 2: the number seeds being sown, used in NoSignleSeedCapt

    note 3: the original start location"""

    def __init__(self, game=None, move=None):
        """Parameters are optional to make copy.copy work;
        they really are required."""

        if game:
            self.player = game.turn
            self.board = tuple(game.board)   # pre-move state
        else:
            self.player = None
            self.board = None
        self.move = move
        self.direct = None   # an intentionally invalid direction
        self.seeds = 0
        self._sow_loc = 0
        self.cont_sow_loc = 0   # use by the sower (updated for lap sows)
        self.lap_nbr = 0
        self.capt_loc = 0
        self.capt_next = 0      # used for multiple captures

        self.capt_changed = False    # capt changed state but didn't capture
        self.captured = False       # there was an actual capture
        self.end_msg = None

    def __str__(self):

        string = f"MoveData({self.board}, {self.move}):\n"
        string += f"  direct={self.direct}\n"
        string += f"  move={self.move}\n"
        string += f"  seeds={self.seeds}\n"
        string += f"  sow_loc={self.sow_loc}\n"
        string += f"  cont_sow_loc={self.cont_sow_loc}\n"
        string += f"  lap_nbr={self.lap_nbr}\n"
        string += f"  capt_loc={self.capt_loc}\n"
        string += f"  capt_next={self.capt_next}\n"
        string += f"  capt_changed={self.capt_changed}\n"
        string += f"  captured={self.captured}\n"
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


class Mancala(ai_interface.AiGameIf, gi.GameInterface):
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
    @property
    def rules(cls):
        """The rules for the class but don't build them unless we
        need them."""
        return ginfo_rules.build_rules()


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
        self.mcount = 0
        self.rturn_cnt = 0
        self.turn = random.choice([False, True])
        self.starter = self.turn
        self.last_mdata = None
        self.inhibitor = inhibitor.make_inhibitor(self)

        self.rtally = None
        if self.info.goal in round_tally.RoundTally.GOALS:
            self.rtally = round_tally.RoundTally(self.info.goal,
                                                 self.info.goal_param,
                                                 self.cts.total_seeds)

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
                      'mcount': self.mcount,
                      'rturn_cnt': self.rturn_cnt}

        if (self.info.moveunlock
                or self.info.allow_rule == gi.AllowRule.MOVE_ALL_HOLES_FIRST):
            state_dict |= {'unlocked': tuple(self.unlocked)}

        if self.info.blocks:
            state_dict |= {'blocked': tuple(self.blocked)}

        if self.info.child_cvt:
            state_dict |= {'child': tuple(self.child)}

        if self.info.goal == gi.Goal.TERRITORY:
            state_dict |= {'owner': tuple(self.owner)}

        state_dict |= {'istate': self.inhibitor.get_state()}

        if self.rtally:
            state_dict |= {'rstate': self.rtally.state}

        return GameState(**state_dict)


    @state.setter
    def state(self, value):
        """Copy the state variables back, convert the tuples
        back to lists."""

        self.board = list(value.board)
        self.store = list(value.store)
        self.turn = value.turn
        self.mcount = value.mcount
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

        if value.rstate:
            self.rtally.state = value.rstate


    def init_bprops(self):
        """Initialize the board properties but not the board or stores."""

        holes = self.cts.holes
        dbl_holes = self.cts.dbl_holes

        self.mcount = 0
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


    def new_game(self, win_cond=None, new_round_ok=False):
        """Delegate to the new_game decorators.
        Return False if it a new round was started.
        True if a new game was started."""
        return self.deco.new_game.new_game(win_cond, new_round_ok)


    def end_round(self):
        """The player has requested that the round be ended."""

        cond, winner = self.deco.ender.game_ended(repeat_turn=False,
                                                  ended='round')
        self.turn = winner
        return cond


    def end_game(self):
        """Either the player has requested that the game be ended
        or an ENDLESS conditions was detected.  End the game fairly."""

        cond, winner = self.deco.quitter.game_ended(repeat_turn=False,
                                                    ended=True)
        self.turn = winner
        return cond


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
            self.new_game(win_cond=gi.WinCond.WIN, new_round_ok=False)
            return False
        return True


    def rtally_param_func(self):
        """If we created a round tallier, return the
        func that get the param values."""

        if self.rtally:
            return self.rtally.parameter
        return None


    def win_conditions(self, repeat_turn=False):
        """Check for end game.
        Return None if no victory/tie conditions are met.
        If there is a winner, set turn to that player."""

        cond, winner = self.deco.ender.game_ended(repeat_turn=repeat_turn,
                                                  ended=False)
        if cond:
            self.turn = winner
            return cond
        return None


    def win_message(self, win_cond):
        """Return a game appropriate win message based on WinCond.
        Return a window title and message string."""

        win_param = self.info.goal_param

        reason = (" by collecting the most seeds!",
                  " by eliminating their opponent's seeds.",
                  " by claiming more holes.",
                  " by clearing all their seeds.",
                  f" by winning {win_param} rounds.",
                  f" by collecting {win_param} or more total seeds.",
                  f" by collecting at least {win_param} more seeds than opponent.",
                  f" by earning {win_param} or more points.",
                  f" by winning {win_param} rounds.",
                  f" by winning {win_param} rounds.")

        rnd_reason = ("not used",
                      " by collecting at least half the seeds.",
                      ". Round ended because there are no moves.",
                      ". Round ended because there were <= "
                          + f"{self.cts.nbr_start} seeds left",
                      ". Round ended because There were <= "
                          + f"{2 * self.cts.nbr_start} seeds left",
                      )

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

        player = 'Top' if self.turn else 'Bottom'
        if win_cond == gi.WinCond.WIN:
            message += f'{player} won {rtext}{reason[self.info.goal]}'

        elif win_cond == gi.WinCond.ROUND_WIN:
            message += f'{player} won {rtext}{rnd_reason[self.info.rounds]}'

        elif win_cond in [gi.WinCond.TIE, gi.WinCond.ROUND_TIE]:
            if self.info.goal in (gi.Goal.DEPRIVE,
                                  gi.Goal.RND_WIN_COUNT_DEP):
                message += 'Both players ended with seeds; consider it a tie.'
            elif self.info.goal == gi.Goal.TERRITORY:
                message += 'Each player controls half the holes (a tie).'
            else:
                message += f'{gtext} ended in a tie.'

        elif win_cond == gi.WinCond.ENDLESS:
            message += 'Game stuck in a loop. No winner.'

        else:
            message += f'Unexpected end condition {win_cond}.'

        return title, message


    def do_sow(self, move, single=False):
        """Do the sowing steps

        2. deal with first hole, getting start loc, seeds to sow, and
        sow start if specified.
        3. get sow direction

        if single sower, with single sower; otherwise with deco.sower
        4. sow the seeds, return updated mdata

        RETURN move data"""

        mdata = MoveData(self, move)
        mdata.sow_loc, mdata.seeds = self.deco.drawer.draw(move)
        mdata.direct = self.deco.get_dir.get_direction(move, mdata.sow_loc)

        if single:
            single_sower = self.deco.sower.get_single_sower()
            single_sower.sow_seeds(mdata)
        else:
            self.deco.sower.sow_seeds(mdata)
        game_log.step(f'Sow from {mdata.sow_loc}', self)

        return mdata


    def sim_single_sow(self, move):
        """For move simulation, just do a single sow."""

        game_log.set_simulate()
        mdata = self.do_sow(move, single=True)
        game_log.clear_simulate()
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

        game_log.set_simulate()
        mdata = self.do_sow(move)

        if mdata.capt_loc not in (gi.WinCond.REPEAT_TURN,
                                  gi.WinCond.ENDLESS):
            self.capture_seeds(mdata)
        game_log.clear_simulate()

        return mdata


    def _move(self, move):
        """Do the move:

        1. if PASS, swap turn and do nothing else
        Call do_sow for steps 2 to 4
        5. capture seeds
        6. if either player won or a tie occured, return that condition
        7. swap the turn and return None (game continues)

        On the assert, sum the stores even if they are not 'in play'
        (e.g. for Deka)."""
        self.mcount += 1
        assert sum(self.store) + sum(self.board) == self.cts.total_seeds, \
            'seed count error before move'

        if move == gi.PASS_TOKEN:
            self.turn = not self.turn
            return None

        mdata = self.do_sow(move)
        self.last_mdata = mdata   # keep this around for the win message

        if mdata.capt_loc == gi.WinCond.REPEAT_TURN:
            win_cond = self.win_conditions(repeat_turn=True)
            return win_cond if win_cond else gi.WinCond.REPEAT_TURN

        if mdata.capt_loc == gi.WinCond.ENDLESS:
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

        self.inhibitor.clear_if(self, mdata)

        win_cond = self.win_conditions()
        if win_cond:
            return win_cond

        self.turn = not self.turn
        return None


    def _log_turn(self, move_turn, move, win_cond):
        """Add to the play log and move history for the move.

        Rebuild the move with the direction computed be get_direction,
        which may have overridden an actual direction in the move tuple
        (or None)."""

        if not game_log.active:
            return

        wtext = ''
        if win_cond in (gi.WinCond.WIN, gi.WinCond.ROUND_WIN):
            sturn = 'Top' if self.turn else 'Bottom'
            wtext = f'\n{win_cond.name} by {sturn}'
        elif win_cond:
            wtext = ' ' + win_cond.name

        sturn = 'Top' if move_turn else 'Bottom'
        if isinstance(move, gi.MoveTpl):
            move = move.set_dir(self.last_mdata.direct)

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
            self.mcount += 1
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
