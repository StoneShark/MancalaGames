# -*- coding: utf-8 -*-
"""Play games and collect results.

Created on Sun Jul 28 12:33:30 2024
@author: Ann"""

# %% imports

import collections
import enum
import random
import time

import tqdm

from context import game_interface as gi
from context import game_logger

from game_logger import game_log


# %%  constants

BOOL_STR = ['f', 't']


class GameResult(enum.Enum):
    """Game results.  Use the same values as the
    game_interface WinCond for the values that overlap."""

    WIN = gi.WinCond.WIN.value
    TIE = gi.WinCond.TIE.value
    GAME_OVER = gi.WinCond.GAME_OVER.value
    ENDLESS = gi.WinCond.ENDLESS.value

    MAX_TURNS = enum.auto()
    LOOPED = enum.auto()


def result_name(starter, result, winner):
    """Create a short string for the game result"""

    if result == GameResult.WIN:
        return f'WIN{BOOL_STR[winner]}-S{BOOL_STR[starter]}'

    if result == GameResult.TIE:
        return f'TIE-S{BOOL_STR[starter]}'

    return result.name


# define a list of game result strings
# without making assumptions about result_name is written

GAME_RESULTS = sorted(list(set([result_name(starter, result, winner)
                                for starter in (False, True)
                                for winner in (False, True)
                                for result in GameResult])))


# %%  helper classes


class GameStats:
    """Collect the game results here."""

    def __init__(self):
        self.stats = {name: 0 for name in GAME_RESULTS}
        self.total = 0

    def __str__(self):
        return f'Games Played: {self.total}\n' \
               + '\n'.join([f'{key:15} {value:10}'
                            for key, value in sorted(self.stats.items(),
                                                     key=lambda p: p[0])])

    def tally(self, starter, result, winner):
        """Tally the game result."""
        self.stats[result_name(starter, result, winner)] += 1
        self.total += 1


class FindLoops:
    """A class to help find cycles in games."""

    def __init__(self, max_cycle=15, max_loop=20):
        """
        max_cycle =  number of states to keep in the deque
        max_loop = error, if we haven't changed the deque
        contents in this many moves
        """

        self.max_loop = max_loop
        self.game_states = collections.deque(maxlen=max_cycle)
        self.dupl_cnt = 0

    def game_state_loop(self, game):

        gstate = game.state.clear_mcount()

        if gstate in self.game_states:
            self.dupl_cnt += 1

            if self.dupl_cnt > self.max_loop:
                print(f"Game cycle found {len(self.game_states)}")
                return True
        else:
            self.game_states.append(game.state)
            self.dupl_cnt = 0

        return False


# %% play the game


def play_one_game(game, tplayer, fplayer, save_logs=False):
    """Play one game between the two players, returning the results.
    If either/both is None, use random choice moves.
    Otherwise use the player."""

    stuck = FindLoops()

    for _ in range(2000 if game.info.rounds else 500):

        if game.turn and tplayer:
            game_log.active = False
            move = tplayer.pick_move()
            game_log.active = save_logs
        elif not game.turn and fplayer:
            game_log.active = False
            move = fplayer.pick_move()
            game_log.active = save_logs
        else:
            moves = game.get_moves()
            assert moves, "Game didn't end right."
            move = random.choice(moves)

        cond = game.move(move)
        if cond in (gi.WinCond.WIN, gi.WinCond.TIE, gi.WinCond.ENDLESS):
            return GameResult(cond.value), game.turn

        if cond in (gi.WinCond.ROUND_WIN, gi.WinCond.ROUND_TIE):
            if game.new_game(cond, new_round_ok=True):
                return GameResult(cond.value), game.turn

        if stuck.game_state_loop(game):
            return GameResult.LOOPED, None

        if game.info.mustpass:
            game.test_pass()
            if stuck.game_state_loop(game):
                return GameResult.LOOPED, None

    return GameResult.MAX_TURNS, None


def play_games(game, tplayer, fplayer, nbr_runs, save_logs,
               result_func=None):
    """Play a bunch of games between two players."""

    game_results = GameStats()

    for cnt in tqdm.tqdm(range(nbr_runs)):

        game.new_game()

        if cnt < nbr_runs // 2:
            starter = game.starter = game.turn = True
        else:
            starter = game.starter = game.turn = False

        result, winner = play_one_game(game, tplayer, fplayer, save_logs)
        if save_logs:
            game_logger.game_log.save(
                'Simulate Game.\n'
                + f'T Player: {tplayer}\nF Player: {fplayer}\n'
                + f'Starter: {game.starter}\n\n'
                + game.params_str())
            game_logger.game_log.new()
            time.sleep(1)

        game_results.tally(starter, result, winner)
        if result_func:
            result_func(starter, result, winner)

    return game_results
