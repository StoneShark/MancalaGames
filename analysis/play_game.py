# -*- coding: utf-8 -*-
"""Play games and collect results.

Created on Sun Jul 28 12:33:30 2024
@author: Ann"""

# %% imports

import collections
import enum
import logging
import random
import time

import tqdm

from context import animator
from context import game_interface as gi
from context import game_logger


# %%  house keeping

# get the logger
logger = logging.getLogger(__name__)

# completely disable the animator
animator.ENABLED = False


# %%  constants

BOOL_STR = ['f', 't']


class GameResult(enum.Enum):
    """Game results.  Use the same values as the
    game_interface WinCond for the values that overlap."""

    WIN = gi.WinCond.WIN.value
    TIE = gi.WinCond.TIE.value

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

GAME_RESULTS = sorted(list({result_name(starter, result, winner)
                                for starter in (False, True)
                                for winner in (False, True)
                                for result in GameResult}))


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

    @property
    def wins(self):
        """Return a tuple of (wins by False, wins by True) independent
        of starter"""
        return [sum(self.stats[result_name(starter, GameResult.WIN, winner)]
                    for starter in (False, True))
                for winner in (False, True)]

    @property
    def ties(self):
        """Return the number of ties independent of starter"""
        return sum(self.stats[result_name(starter, GameResult.TIE, None)]
                   for starter in (False, True))


class FindLoops:
    """A class to help find cycles in games.

    Doesn't exactly find a loop, but doesn't do much
    extra processing. If we don't find a new state in
    dupl_states moves; assume that we have a cycle."""

    def __init__(self, qsize=18, dupl_states=12):
        """Parameters:
        qsize =  number of states to keep in the deque
        dupl_states = error, if we haven't changed the deque
        contents in this many moves"""

        self.dupl_states = dupl_states
        self.qsize = qsize
        self.game_states = collections.deque(maxlen=qsize)
        self.dupl_cnt = 0

    def __repr__(self):
        return f"FindLoops(qsize={self.qsize}, dupl_states={self.dupl_states})"

    def game_state_loop(self, game):
        """The queue only gets unique states.
        Clear the move count, because they wont match in
        future comparisons. For most games, they don't
        matter after the first move."""

        gstate = game.state.clear_mcount()

        if gstate in self.game_states:
            self.dupl_cnt += 1

            if self.dupl_cnt > self.dupl_states:
                game_logger.game_log.add(f"Likely game cycle found by {self}.",
                                         game_logger.game_log.IMPORT)
                return True
        else:
            self.game_states.append(gstate)
            self.dupl_cnt = 0

        return False



# %% play the game


def make_one_move(game, move):
    """
    Make a move for the next player.

    Parameters
    ----------
    game : Mancala
        The game being played.

    move : gi.MoveTpl or int

    Returns
    -------
    (result, winner) : tuple(GameResult, bool/None)
        Game result and winner (or None).
    None : game not over
    """

    cond = game.move(move)
    if cond in (gi.WinCond.WIN, gi.WinCond.TIE):
        return GameResult(cond.value), game.turn

    if cond in (gi.WinCond.ROUND_WIN, gi.WinCond.ROUND_TIE):
        if game.new_game(cond, new_round_ok=True):
            return GameResult(cond.value), game.turn
        game_logger.game_log.turn(0, 'Start Game', game)

    if game.info.mustpass:
        game.test_pass()

    return None, game.turn


def play_one_game(game, fplayer, tplayer,
                  *, save_logs=False, move_limit=0, end_all=False):
    """Play one game between the two players, returning the results.
    If either/both is None, use random choice moves.
    Otherwise use the player.

    Parameters
    ----------
    game : Mancala
        The game to play.

    fplayer : AiPlayer
        The configuration to use for the False player.

    tplayer : AiPlayer
        The configuration to use for the True player.

    save_logs : bool
        True if the game_logger should be used for this game.
        Records the start turn of the game.
        The game_logger is disabled while the AiPlayers are
        selecting a move, the logger state will be returned
        to this value afterward.

    move_limit : int (optional)
        Number of turns to limit each game to. Games which
        exceed this are tallied as MAX_TURNS

    end_all : bool
        Force all games to end in a WIN or TIE.

    Returns
    -------
    (result, winner) : tuple(GameResult, bool/None)
        Game result and winner (or None).
    """
    # pylint: disable=too-many-branches

    stuck = FindLoops(qsize=game.cts.holes * 3,
                      dupl_states=game.cts.holes * 2)
    game_logger.game_log.turn(0, 'Start Game', game)

    if not move_limit:
        move_limit = 500
        if game.info.rounds:
            move_limit *= 4
        if game.info.capt_rturn or game.info.sow_own_store:
            move_limit *= 2

    for _ in range(move_limit):

        if game.turn and tplayer:
            game_logger.game_log.active = False
            move = tplayer.pick_move()
            game_logger.game_log.active = save_logs
        elif not game.turn and fplayer:
            game_logger.game_log.active = False
            move = fplayer.pick_move()
            game_logger.game_log.active = save_logs
        else:
            moves = game.get_moves()
            assert moves, "Game didn't end right."
            move = random.choice(moves)

        cond, winner = make_one_move(game, move)
        if cond:
            return cond, winner

        if stuck.game_state_loop(game):
            if end_all:
                cond = game.end_game()
                return GameResult(cond.value), game.turn

            return GameResult.LOOPED, None

    if end_all:
        cond = game.end_game()
        return GameResult(cond.value), game.turn
    return GameResult.MAX_TURNS, None


def play_games(game, fplayer, tplayer, nbr_runs, *,
               save_logs=False, move_limit=0, end_all=False, result_func=None):
    """Play a nbr_runs games between two players. Half will be
    started by False and half by True.

    Parameters
    ----------
    game : Mancala
        The game to play.

    fplayer : AiPlayer
        The configuration to use for the False player.

    tplayer : AiPlayer
        The configuration to use for the True player.

    nbr_runs : int
        The number of runs to perform.

    save_logs : bool
        If True, the game logger is set to DETAIL. Each log
        will be pre-pended with the player configurations
        and the game configuration.
        Only one game will be played per second (to avoid
        filename conflicts in the game logger).

    move_limit : int (optional)
        Number of turns to limit each game to. Games which
        exceed this are tallied as MAX_TURNS

    result_func : function, optional
                  prototype: result_func(starter, result, winner)
        starter: bool - player that started the game
        result: TODO
        winner: bool or None - player that won the game

        If this function is provided, it will be called after
        every game played.

    end_all : bool
        Force all games to end in a WIN or TIE.

    Returns
    -------
    game_results : GameStats
        Accumulated game results in GameStats.
    """
    # pylint: disable=too-many-arguments

    game_results = GameStats()

    if save_logs:
        game_logger.game_log.active = True
        game_logger.game_log.level = game_logger.game_log.DETAIL
    else:
        game_logger.game_log.active = False

    for cnt in tqdm.tqdm(range(nbr_runs)):

        game.new_game()
        starter = game.starter = game.turn = bool(cnt < nbr_runs // 2)

        result, winner = play_one_game(game, fplayer, tplayer,
                                       save_logs=save_logs,
                                       move_limit=move_limit,
                                       end_all=end_all)
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


def get_win_percent(game, player1, player2, nbr_runs):
    """Play a number of games of player1 against player2.
    This is a small wrapper around play_games.
    Games that do not complete for any reason, are not included.

    Parameters
    ----------
    game : Mancala
        The game to play.

    fplayer : AiPlayer
        The configuration to use for the False player.

    tplayer : AiPlayer
        The configuration to use for the True player.

    nbr_runs : int
        The number of runs to perform.

    Returns
    -------
    win percentage : float
         player2's win percentages: wins 1 point, ties 0.5 point
         divided by the total games play (not those that ended in
         win or tie).
    """

    gstats = play_games(game, player1, player2, nbr_runs, save_logs=False)
    if gstats.stats['MAX_TURNS'] > nbr_runs // 2:
        logger.info("Many MAX_TURNS games %d", gstats.stats['MAX_TURNS'])

    return (gstats.wins[True] + (gstats.ties * 0.5)) / gstats.total
