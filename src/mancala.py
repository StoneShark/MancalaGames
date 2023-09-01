# -*- coding: utf-8 -*-
"""Mancala is contains the key game dynamics of the mancala player.
Game constants and info define how the game is created and played.

Created on Sun Mar 19 09:58:36 2023
@author: Ann"""

import dataclasses as dc
import pprint
import random
import warnings

import ai_interface
import allowables
import capt_ok
import capturer
import cfg_keys as ckey
import end_move
import game_constants as gc
import game_interface as gi
import game_log
import game_str
import get_direction
import get_moves
import ginfo_rules
import incrementer
import minimax
import new_game
import sow_starter
import sower

from game_interface import WinCond
from game_interface import PASS_TOKEN


LOCK = ['_', ' ']
CHILD = {True: '˄',
         False: '˅',
         None: ' '}


@dc.dataclass(frozen=True, kw_only=True)
class GameState(ai_interface.StateIf):
    """A simplified immuatble game state but enough to save
    and restore the game state."""

    board: tuple
    store: tuple
    _turn: bool

    unlocked: tuple = None
    blocked: tuple = None
    child: tuple = None

    @property
    def turn(self):
        return self._turn

    def __str__(self):

        dbl_holes = len(self.board)
        holes = dbl_holes // 2

        string = ''
        for side, side_range in enumerate([range(dbl_holes - 1, holes - 1, -1),
                                           range(holes)]):
            for loc in side_range:

                if self.blocked and self.blocked[loc]:
                    string += '  x'
                else:
                    string += f' {self.board[loc]:2}'
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


class ManDeco:
    """Collect the decorator chains into one variable,
    build them all together."""

    def __init__(self, game):

        self.new_game = new_game.deco_new_game(game)
        self.allow = allowables.deco_allowable(game)
        self.moves = get_moves.deco_moves(game)
        self.incr = incrementer.deco_incrementer(game)
        self.starter = sow_starter.deco_sow_starter(game)
        self.get_dir = get_direction.deco_dir_getter(game)
        self.sower = sower.deco_sower(game)
        self.ender = end_move.deco_end_move(game)
        self.capt_ok = capt_ok.deco_capt_ok(game)
        self.capturer = capturer.deco_capturer(game)
        self.gstr = game_str.deco_get_string(game)


class Mancala(ai_interface.AiGameIf, gi.GameInterface):
    """An attempt to implement a wide variety of mancala games.
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

    def __init__(self, game_consts, game_info, player=None):

        if not isinstance(game_consts, gc.GameConsts):
            raise TypeError(
                'game_consts not built on game_constants.GameConsts.')
        if not isinstance(game_info, gi.GameInfo):
            raise TypeError('game_info not built on game_info.GameInfo.')

        if player and not isinstance(player, ai_interface.AiPlayerIf):
            raise TypeError('player not built on ai_interface.AiPlayerIf.')

        self.cts = game_consts
        self.info = game_info
        self.player = player or minimax.MiniMaxer(self)

        self.board = [self.cts.nbr_start] * self.cts.dbl_holes
        locks = not self.info.flags.moveunlock
        self.unlocked = [locks] * self.cts.dbl_holes
        self.blocked = [False] * self.cts.dbl_holes
        self.child = [None] * self.cts.dbl_holes
        self.store = [0, 0]
        self.turn = random.choice([False, True])

        self.difficulty = 1
        self.starter = self.turn

        self.deco = ManDeco(self)


    def __str__(self):
        """ascii print of board for game logs."""

        return self.deco.gstr.get_string()


    @property
    def state(self):
        """Return an immutable copy of the state variables,
        these must be able to completely return the game
        state to a previous position.
        Always return stores, because they may be used
        even if not displayed (e.g. Deka)."""

        state_dict = {'board': tuple(self.board),
                      '_turn': self.turn,
                      'store': tuple(self.store)}

        if self.info.flags.moveunlock:
            state_dict |= {'unlocked': tuple(self.unlocked)}

        if self.info.flags.blocks:
            state_dict |= {'blocked': tuple(self.blocked)}

        if self.info.flags.child:
            state_dict |= {'child': tuple(self.child)}

        return GameState(**state_dict)


    @state.setter
    def state(self, value):

        self.board = list(value.board)
        self.store = list(value.store)
        self.turn = value.turn

        if value.child:
            self.child = list(value.child)
        if value.blocked:
            self.blocked = list(value.blocked)
        if value.unlocked:
            self.unlocked = list(value.unlocked)


    def set_player(self, player):
        """Save the new player.
        Call set_difficulty to confirm new player is using the
        desired difficulty and paramters."""

        if not isinstance(player, ai_interface.AiPlayerIf):
            raise TypeError('player not built on ai_interface.AiPlayerIf.')

        self.player = player
        self.set_difficulty(self.difficulty)


    def params_str(self):
        """Generate a string describing the game parameters.
        Delete duplicate/derived parameters and things that don't
        effect game play."""

        strings = ckey.GAME_CLASS + ': ' + self.__class__.__name__ + '\n'
        strings += repr(self.cts) + '\n'

        info_dict = dc.asdict(self.info)
        del info_dict[ckey.ABOUT]
        info_dict[ckey.DIFFICULTY] = f'{self.difficulty} played'
        del info_dict[ckey.FLAGS][ckey.UDIRECT]
        del info_dict[ckey.HELP_FILE]
        # del info_dict[ckey.NAME]  might not match all params
        del info_dict[ckey.NBR_HOLES]

        pprinter = pprint.PrettyPrinter(indent=4)
        strings += 'GameInfo\n'
        strings += pprinter.pformat(info_dict) + '\n'

        return strings


    def get_game_info(self):
        """Return the GameInfo named tuple."""

        return self.info


    def set_difficulty(self, diff):
        """Set game difficulty"""

        game_log.add(f'Changing difficulty {diff}', game_log.INFO)
        self.difficulty = diff
        msg = self.player.set_params(diff, self.info.ai_params)
        game_log.add(f'AI Param Error: {msg}', game_log.IMPORT)
        return msg


    def new_game(self, win_cond=None, new_round_ok=False):
        """Delegate to the new_game decorators.
        Return False if it a new round was started.
        True if a new game was started."""

        return self.deco.new_game.new_game(win_cond, new_round_ok)


    def _get_seeds_for_divvy(self):
        """Collect all of the seeds from non-child holes and
        zero the holes;
        return the number seeds collected"""

        seeds = 0
        for loc in range(self.cts.dbl_holes):
            if self.child[loc] is None:
                seeds += self.board[loc]
                self.board[loc] = 0

        return seeds


    def end_game(self):
        """The user has requested that the game be ended.
        Split the seeds on the board between the two stores.
        return WinCond  """

        if not self.info.flags.stores:
            warnings.warn(
                'Hidden stores will be used to determine outcome.')

        seeds = self._get_seeds_for_divvy()
        quot, rem = divmod(seeds, 2)

        self.store[False] += quot
        self.store[True] += quot
        store_f, store_t = self.store[False], self.store[True]

        if self.info.flags.child:
            store_f += sum(self.board[loc] for loc in self.cts.false_range
                           if self.child[loc] is False)
            store_t += sum(self.board[loc] for loc in self.cts.true_range
                           if self.child[loc] is True)

        if store_t > store_f:
            self.store[False] += rem
        else:
            self.store[True] += rem

        win_cond = self.win_conditions()
        return win_cond


    def win_conditions(self, repeat_turn=False):
        """Check for end game.

        Return None if no victory/tie conditions are met.
        If there is a winner, turn must be that player!"""

        cond, winner = self.deco.ender.game_ended(repeat_turn)
        if cond:
            self.turn = winner
            return cond

        return None


    def win_message(self, win_cond):
        """Return a game appropriate win message based on WinCond.
        Return a window title and message strings."""

        rtext = 'the game'
        gtext = 'Game'
        title = 'Game Over'
        if win_cond in (WinCond.ROUND_WIN, WinCond.ROUND_TIE):
            rtext = 'the round'
            gtext = 'The round'
            title = 'Round Over'

        if win_cond in [WinCond.WIN, WinCond.ROUND_WIN]:
            player = 'Top' if self.turn else 'Bottom'
            message = f'{player} won {rtext} by collecting the most seeds!'

        elif win_cond in [WinCond.TIE, WinCond.ROUND_TIE]:
            message = f'{gtext} ended in a tie.'

        elif win_cond == WinCond.ENDLESS:
            message = 'Game stuck in a loop. No winner.'

        return title, message


    def do_sow(self, move):
        """Do the sowing steps:

        2. deal with first hole, getting start loc and seeds to sow
        3. get sow direction
        4. sow the seeds, return if something bad/interesting happened

        RETURN end locations and sow direction"""

        if self.info.flags.udirect:
            pos, _ = move
        else:
            pos = move

        start, seeds = self.deco.starter.start_sow(pos)
        direct = self.deco.get_dir.get_direction(move, start)
        end_loc = self.deco.sower.sow_seeds(start, direct, seeds)

        return end_loc, direct


    def capture_seeds(self, loc, direct):
        """Hand off the capture to the capturer deco."""

        self.deco.capturer.do_captures(loc, direct)


    def move(self, move):
        """Do the move.
        If pass, then change turn and return None (game continues).
        Otherwise:

        1. parse the move and PASS if specified
        Call do_sow for steps 2 to 4
        5. capture seeds
        6. if either player won or a tie occured, return that condition
        7. swap the turn and return None (game continues)

        On the assert, sum the stores even if they are not 'in play'
        (for Deka)."""

        assert sum(self.store) + sum(self.board) == self.cts.total_seeds, \
            'seed count error before move'

        if (move == PASS_TOKEN
                or (self.info.flags.udirect and move[0] == PASS_TOKEN)):
            self.turn = not self.turn
            return None

        loc, direct = self.do_sow(move)
        game_log.step('Sow', self)

        if loc is WinCond.END_STORE:
            win_cond = self.win_conditions(repeat_turn=True)
            return win_cond if win_cond else WinCond.END_STORE

        if loc is WinCond.ENDLESS:
            game_log.add('MLAP game ENDLESS', game_log.IMPORT)
            return WinCond.ENDLESS

        self.capture_seeds(loc, direct)
        game_log.step('Capture', self)

        win_cond = self.win_conditions()
        # win_conditions does log step if it changes anything

        if win_cond:
            return win_cond

        self.turn = not self.turn
        return None


    def get_ai_move(self):
        """Return the ai move position"""
        return self.player.pick_move()


    def get_ai_move_desc(self):
        """Return the move description from the player."""
        return self.player.get_move_desc()


    def test_pass(self):
        """If no valid moves, swap turn and return True.
        Can't put this in move or it will break the AiPlayer.
        This method is likely only useable by the Ai
        because of the side effect of swapping turns."""

        if self.info.flags.mustpass:
            if not any(self.get_allowable_holes()):

                self.turn = not self.turn
                return True

        return False


    def get_hole_props(self, row, pos):
        """return the number of seeds for side / position.
        row : 0 for top row, 1 for bottom   (opposite of player)
        position : 0 .. 5 from left to right"""

        loc = self.cts.pos_to_loc(row, pos)
        return gi.HoleProps(seeds=self.board[loc],
                            unlocked=self.unlocked[loc],
                            blocked=self.blocked[loc],
                            ch_owner=self.child[loc])


    def get_store(self, row):
        """return the number of seeds in the store for side.
        row : 0 for top row, 1 for bottom  (opposite of player)"""

        return self.store[(row + 1) % 2]


    def get_turn(self):
        """Return current turn."""

        return self.turn


    def get_allowable_holes(self):
        """Determine what holes are legal moves."""

        return self.deco.allow.get_allowable_holes()


    # AiGameIf interface support methods


    def _score_stores(self):
        """Score the stores and children."""
        sval = 0

        if self.info.scorer.stores_m:
            store_f = self.store[False]
            store_t = self.store[True]

            if self.info.flags.child:
                store_f += sum(self.board[loc]
                               for loc in self.cts.false_range
                               if self.child[loc] is False)
                store_t += sum(self.board[loc]
                               for loc in self.cts.true_range
                               if self.child[loc] is True)
            sval += (store_f - store_t) * self.info.scorer.stores_m

        if self.info.flags.child and self.info.scorer.child_cnt_m:
            child_f = self.child.count(False)
            child_t = self.child.count(True)
            sval += (child_f - child_t) * self.info.scorer.child_cnt_m

        return sval


    def _get_access_count(self):
        """Return the difference between the number opponents cells that
        false and true can access.

        Do not support multilap games!"""

        if self.info.flags.mlaps:
            return 0

        access = [set(), set()]
        saved_state = self.state

        for pos in range(self.cts.holes):
            for turn in (True, False):

                self.turn = turn
                end, _ = self.do_sow(pos)

                if self.cts.opp_side(self.turn, end):
                    access[turn] |= set([end])

                self.state = saved_state

        return len(access[False]) - len(access[True])


    def _score_endgame(self, end_cond):
        """Score the end game conditions.
        return None if not scored."""

        if end_cond == WinCond.WIN:
            return -1000 if self.turn else 1000

        if end_cond == WinCond.TIE:
            return -5 if self.turn else 5

        if end_cond == WinCond.ENDLESS:
            return 0

        return None


    # interfaces for the AiGameIf


    def get_moves(self):
        """Return the list of allowable moves."""

        return self.deco.moves.get_moves()


    # def move(self, move):
    #     """Do the move. Defined above."""


    def is_max_player(self):
        """Return True if 'score' maximizes for the current player."""
        return self.turn is False


    def score(self, end_cond):
        """Statically evaluate the playing position in terms of the bottom
        player (i.e. False).
        end_cond is the result of the last move."""

        sval = self._score_endgame(end_cond)
        if sval is not None:
            return sval

        sval = 0

        if end_cond == WinCond.END_STORE:
            mult = -1 if self.turn else 1
            sval += mult * self.info.scorer.repeat_turn

        if self.info.scorer.evens_m:
            even_t = sum(1 for loc in self.cts.true_range
                         if self.board[loc] > 0 and not self.board[loc] % 2)
            even_f = sum(1 for loc in self.cts.false_range
                         if self.board[loc] > 0 and not self.board[loc] % 2)
            sval += (even_f - even_t) * self.info.scorer.evens_m

        if self.info.scorer.seeds_m:
            sum_t = sum(self.board[loc] for loc in self.cts.true_range)
            sum_f = sum(self.board[loc] for loc in self.cts.false_range)
            sval += (sum_f - sum_t) * self.info.scorer.seeds_m

        if self.info.scorer.empties_m:
            empty_t = sum(1 for loc in self.cts.true_range
                          if not self.board[loc])
            empty_f = sum(1 for loc in self.cts.false_range
                          if not self.board[loc])
            sval += (empty_f - empty_t) * self.info.scorer.empties_m

        sval += self._score_stores()

        easy = self.info.scorer.easy_rand
        if easy:
            if not self.difficulty and sum(self.store) <= self.cts.win_count:
                sval += random.randrange(-easy, easy)

        if self.info.scorer.access_m and self.difficulty > 1:
            sval += self._get_access_count() * self.info.scorer.access_m

        return sval
