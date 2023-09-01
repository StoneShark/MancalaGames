# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:09:31 2023

@author: Ann
"""
# %% imports

import enum
import sys

import pytest

sys.path.extend(['src'])

import ai_interface
import minimax


# %%  define_get_game

class EndCond(enum.Enum):

    ENDED = True

    def is_ended(self):
        return self


def define_get_game(depth):
    """Scored needs to be a class scope variable
    or it wont change/be saved during the minimax'ing
    but I do want it to reset between each test.

    scored will be True for the nodes for which the scorer was called."""

    class Small(ai_interface.AiGameIf):

        """  small test graph     node:score
        0:0
         |
        1:4   _         _        2:5   _          _
         |     |         |       |      |          |
        3:4   4:6 _     5:2      6:3   7:1  _    8:6
              |    |                    |    |
             9:8   10:9              11:0  12:3
        """

        scores = [0, 4, 5, 4, 6, 2, 3, 1, 6, 8, 9, 0, 3]
        childs = [[1, 2],
                  [3, 4, 5],
                  [6, 7, 8],
                  [],
                  [9, 10],
                  [],
                  [],
                  [11, 12],
                  [],
                  [],
                  [],
                  [],
                  []]
        scored = [False] * len(scores)

        def __init__(self, difficulty):

            assert len(Small.scores) == len(Small.childs), 'graph error'

            self.player = minimax.MiniMaxer(self)
            self.player.set_params(difficulty,
                                   {"mm_depth" : [1, 1, 2, 3]})
            self.turn = False
            self.node = 0

        def get_moves(self):
            return self.childs[self.node]

        def move(self, move):
            self.node = move
            self.turn = not self.turn
            if len(self.childs[move]) == 0:
                return EndCond.ENDED
            return None

        def is_max_player(self):
            return not self.turn

        def get_turn(self):
            return self.turn

        def score(self, _=None):
            self.scored[self.node] = True
            return self.scores[self.node]

        @property
        def state(self):
            return (self.node, self.turn)

        @state.setter
        def state(self, value):
            self.node = value[0]
            self.turn = value[1]


    return Small(depth)


# %%

class TestMinimaxer:

    def test_level1(self):

        game = define_get_game(1)

        move = game.player.pick_move()
        # print(move)
        # print(game.player.get_move_desc())
        # print(game.scored)
        assert move == 2
        assert 'm1 4, m2 5' in game.player.get_move_desc()

        all_nodes = set(range(len(game.scores)))
        scored = set([1, 2])
        assert all(game.scored[n] for n in scored) \
            and not any(game.scored[n] for n in all_nodes - scored)

    def test_level2(self):

        game = define_get_game(2)

        move = game.player.pick_move()
        # print(move)
        # print(game.player.get_move_desc())
        # print(game.scored)
        assert move == 1
        assert 'm1 2, m2 1' in game.player.get_move_desc()

        # nodes scored for minimax (no pruning)
        # scored = set([3, 4, 5, 6, 7, 8])
        # the alpha-beta pruner doesn't score all the nodes
        scored = set([3, 4, 5, 6, 7])

        all_nodes = set(range(len(game.scores)))
        assert all(game.scored[n] for n in scored) \
            and not any(game.scored[n] for n in all_nodes - scored)

    def test_level3(self):

        game = define_get_game(3)

        move = game.player.pick_move()
        # print(move)
        # print(game.player.get_move_desc())
        # print(game.scored)
        assert move == 2
        assert 'm1 2, m2 3' in game.player.get_move_desc()

        # score all terminal nodes for minimax
        # scored = set([3, 5, 6, 8, 9, 10, 11, 12])
        # the alpha-beta pruner doesn't score all the nodes
        scored = set([3, 5, 6, 8, 9, 11, 12])

        all_nodes = set(range(len(game.scores)))
        assert all(game.scored[n] for n in scored) \
            and not any(game.scored[n] for n in all_nodes - scored)


    def test_assert_error(self):

        game = define_get_game(3)
        game.node = 3  # no children

        with pytest.raises(AssertionError):
            game.player.pick_move()
