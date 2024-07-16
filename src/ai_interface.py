# -*- coding: utf-8 -*-
"""Interfaces that games, ai players and ai algorithms share.

The player ties together a game dynamic class (Mancala)
with an ai algorithm class.

The ai_algorithm doesn't care what game it's playing.
The game dynamic class doesn't care who it's players are.

Created on Fri Aug 4 15:03:50 2023
@author: Ann"""

import abc


class StateIf(abc.ABC):
    """Required interface for game state."""

    @property
    @abc.abstractmethod
    def turn(self):
        """Only need getter, return the current turn."""


class AiGameIf(abc.ABC):
    """The game interface required by an ai algorithm.
    This game class should inherit this (i.e. mixedin)."""

    @abc.abstractmethod
    def get_moves(self):
        """Return a list of possible moves for the current player.
        Each will be sent to the apply interface.

        Return an empty list if the game is over."""

    @abc.abstractmethod
    def move(self, move):
        """Apply the move to the game.

        Return end_cond: WinCond how the move ended or
        None to continue."""

    @property
    @abc.abstractmethod
    def state(self):
        """Provide a means to get and set the state of the game.
        The state must be immutable."""


class AiPlayerIf(abc.ABC):
    """Required interfaces for a player by
    both the game and the algorithm.

    The player is a 'friend' of the game class, e.g. it's interface
    isn't specified and it accesses the public data directly."""

    def __init__(self, game, player_dict):
        """Derived classes should use the player_dict
        to create and configure an algorithm."""
        _ = player_dict

        if not isinstance(game, AiGameIf):
            raise ValueError("game isn't of type AiGameIf")
        self.game = game

    @property
    @abc.abstractmethod
    def difficulty(self):
        """The player difficulty."""

    @abc.abstractmethod
    def is_max_player(self):
        """True if the score interface maximizes for the current player."""

    @abc.abstractmethod
    def score(self, end_cond):
        """Reduce the goodness of the game to an integer.
        Should be written from the perspective one player,
        the player for which is_max_player returns True."""

    @abc.abstractmethod
    def pick_move(self):
        """Return the best move for the current player."""

    @abc.abstractmethod
    def get_move_desc(self):
        """Return a description of the previous move."""

    @abc.abstractmethod
    def clear_history(self):
        """Clear any game state or history (called when
        a new game is started)."""


class AiAlgorithmIf(abc.ABC):
    """The ai algorithm interfaces required by a player."""

    def __init__(self, game, player):
        """Save game for future use."""
        if not isinstance(game, AiGameIf):
            raise ValueError("game isn't of type AiGameIf")
        if not isinstance(player, AiPlayerIf):
            raise ValueError("scorer isn't of type AiPlayerConfIf")
        self.game = game
        self.player = player

    @abc.abstractmethod
    def pick_move(self):
        """Return the best move for the current player."""

    @abc.abstractmethod
    def get_move_desc(self):
        """Return a description of the previous move."""

    @abc.abstractmethod
    def set_params(self, *args):
        """Set the parameters for the player."""

    def clear_history(self):
        """Clear any game state or history (called when
        a new game is started).

        Don't require an implementation. If no state is
        maintained between moves, this method does not
        need to be implemented."""
