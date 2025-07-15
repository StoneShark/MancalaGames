# -*- coding: utf-8 -*-
"""Some utilities for dealing with algorithm parameters
independent of the algorithm. Parameters values are
stored as integers in a dictionary.

add_algo_name must be called once before any other function.

Created on Sun Oct  6 08:08:35 2024
@author: Ann"""

import dataclasses
import enum
import logging

from context import ai_player
from context import cfg_keys as ckey
from context import minimax
from context import montecarlo_ts as mcts
from context import negamax


logger = logging.getLogger(__name__)


MCTS_BIAS_DIV = ai_player.MCTS_BIAS_DIV


class Algo(enum.Enum):
    """use enums to id algo's"""

    MCTS = enum.auto()
    MINIMAX = enum.auto()
    NEGAMAX = enum.auto()


def add_algo_name(player):
    """Add the algo name to the players.
    enum equality check is faster than isinstance calls."""

    if isinstance(player.algo, mcts.MonteCarloTS):
        player.ana_algo = Algo.MCTS

    elif isinstance(player.algo, minimax.MiniMaxer):
        player.ana_algo = Algo.MINIMAX

    elif isinstance(player.algo, negamax.NegaMaxer):
        player.ana_algo = Algo.NEGAMAX

    else:
        logger.info("Algorithm not supported for %s",
                    player.algo.__class__.__name__)


def set_depth(player, depth):
    """If depth is meaningful, set it."""

    if player.ana_algo in (Algo.MINIMAX, Algo.NEGAMAX):
        player.algo.set_params(depth)


def get_pnames(player, pdict):
    """Get the names of the parameters that effect the algo."""

    param_names = []

    if player.ana_algo == Algo.MCTS:
        param_names = [ckey.MCTS_BIAS, ckey.MCTS_NODES, ckey.MCTS_POUTS]

    elif player.ana_algo in (Algo.MINIMAX, Algo.NEGAMAX):
        param_names = list(pdict['scorer'].keys())
        if 'mx_easy_rand_a' in param_names:
            param_names.remove('mx_easy_rand_a')

    return param_names


def get_params(player):
    """Return the current params from player in dictionary form."""

    param_dict = {}

    if player.ana_algo == Algo.MCTS:
        param_dict = {ckey.MCTS_BIAS: int(player.algo.bias * MCTS_BIAS_DIV),
                      ckey.MCTS_NODES: player.algo.new_nodes,
                      ckey.MCTS_POUTS: player.algo.nbr_pouts}

    elif player.ana_algo in (Algo.MINIMAX, Algo.NEGAMAX):
        param_dict = dataclasses.asdict(player.sc_params)

    return param_dict


def update_player(player, param_dict):
    """Update the player with params in the param_dict"""

    if player.ana_algo == Algo.MCTS:
        player.algo.set_params(param_dict[ckey.MCTS_BIAS] / MCTS_BIAS_DIV,
                               param_dict[ckey.MCTS_NODES],
                               param_dict[ckey.MCTS_POUTS])

    elif player.ana_algo in (Algo.MINIMAX, Algo.NEGAMAX):

        player.sc_params = ai_player.ScoreParams(**param_dict)
        player.collect_scorers()
