# -*- coding: utf-8 -*-
"""Interfaces that games and ai players share.

The ai_player calls into the game as defined by AiGameIf
The game calls into the ai_player as defined by AiPlayerIf

Created on Fri Aug 4 15:03:50 2023
@author: Ann
"""

import abc


class StateIf(abc.ABC):
    """Required interface for game state."""

    @property
    @abc.abstractmethod
    def turn(self):
        """Only need getter, return the current turn."""


class AiGameIf(abc.ABC):
    """The game interface required by an ai player.
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

    @abc.abstractmethod
    def is_max_player(self):
        """True if the score interface maximizes for the current player."""

    @abc.abstractmethod
    def score(self, end_cond):
        """Reduce the goodness of the game to an integer.
        Should be written from the perspective one player,
        the player for which is_max_player returns True."""

    @property
    @abc.abstractmethod
    def state(self):
        """Provide a means to get and set the state of the game.
        The state must be immutable."""


class AiPlayerIf(abc.ABC):
    """The ai player interface required by a game."""

    def __init__(self, game):
        """Save game for future use."""
        if not isinstance(game, AiGameIf):
            raise ValueError("game isn't of type AiGameIf")
        self.game = game

    @abc.abstractmethod
    def pick_move(self):
        """Return the best move for the current player."""

    @abc.abstractmethod
    def get_move_desc(self):
        """Return a description of the previous move."""

    @abc.abstractmethod
    def set_params(self, params):
        """Set the params from the config file that associate
        with the selected difficulty."""
