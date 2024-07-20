# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:09:31 2023

@author: Ann
"""
# %% imports

import enum

import pytest
pytestmark = pytest.mark.unittest

from context import ai_interface
from context import ai_player
from context import cfg_keys as ckey
from context import game_constants as gc
from context import game_interface as gi
from context import game_logger
from context import man_config
from context import mancala
from context import montecarlo_ts as mcts


# %%

TEST_COVERS = ['src\\montecarlo_ts.py']

BIAS_x1000 = 100
NODES = 100
POUTS = 1


game_logger.game_log.active = False


# %%


class TestGameNode:

    def test_const(self):

        node = mcts.GameNode('gstate', 12)
        assert node.state == 'gstate'
        assert node.node_id == 12
        assert not node.leaf
        assert node.reward == 0.0
        assert len(node.childs) == 0

        # there is no need to check if a child exists
        node.add_child_state(2, 234)
        assert node.childs[2] == 234

        node = mcts.GameNode('gstate', 12, moves=(1, 2, 3))
        assert len(node.childs) == 3
        assert all(not node for move, node in node.childs.items())

        # leaf nodes shouldn't have children, but why complicate the code
        node = mcts.GameNode('gstate', 12, leaf=True, reward=10, moves=(2, 45))
        assert node.leaf
        assert node.reward == 10
        assert len(node.childs) == 2


    def test_str_basic(self, capsys):

        node = mcts.GameNode('gstate', 12)
        print(node)
        data = capsys.readouterr().out

        assert 'gstate' in data
        assert '12' in data
        assert 'Leaf' not in data

    def test_str_children(self, capsys):

        node = mcts.GameNode('wchild', 65, moves=(1, 2, 3))
        print(node)
        data = capsys.readouterr().out

        assert 'wchild' in data
        assert '65' in data
        assert 'Leaf' not in data
        assert all(str(mnbr) + ': none' in data for mnbr in (1, 2, 3))

    def test_str_leaf(self, capsys):

        node = mcts.GameNode('with_leaf', 21, leaf=True, reward=10, moves=(2, 45))
        print(node)
        data = capsys.readouterr().out

        assert 'with_leaf' in data
        assert '21' in data
        assert '10' in data
        assert 'Leaf' in data
        assert all(str(mnbr) + ': none' in data for mnbr in (2, 45))


    def test_rprint(self, capsys):

        node = mcts.GameNode('parent', 12, moves=(2, 45, 22))
        node.add_child_state(2, mcts.GameNode('first', 14))
        third = mcts.GameNode('third', 16)
        third.add_child_state(13, node)
        node.add_child_state(22, third)

        node.rprint()
        data = capsys.readouterr().out

        # all three nodes are printed
        assert data.count('id') == 3

        # all moves listed
        assert all('mv ' + str(nbr) + ':' in data
                   for nbr in (2, 45, 22, 13))


class TestMCountOps:
    # TODO TestMCountOps -- do later, might find better implementation
    pass


class TestMCTSBasics:
    """const, add_node, clear_history, get_move_desc & set_params"""
    # TODO TestMCTSBasics -- do later, wont improve player



#@pytest.mark.skip('messes up coverage')
class TestMonteCarloTS:

    @pytest.fixture
    def game(self):

        game_consts = gc.GameConsts(nbr_start=2, holes=3)
        game_info = gi.GameInfo(sow_own_store=6,
                                stores=True,
                                nbr_holes=game_consts.holes,
                                rules=mancala.Mancala.rules)

        game = mancala.Mancala(game_consts, game_info)
        game.turn = True
        return game

    @pytest.fixture
    def player(self, game):

        pdict = dict()
        pdict[ckey.ALGORITHM] = 'montecarlo_ts'
        pdict[ckey.AI_PARAMS] = dict()
        pdict[ckey.AI_PARAMS][ckey.MCTS_BIAS] = [BIAS_x1000] * 4
        pdict[ckey.AI_PARAMS][ckey.MCTS_NODES] = [20] * 4
        pdict[ckey.AI_PARAMS][ckey.MCTS_POUTS] = [POUTS] * 4

        player = ai_player.AiPlayer(game, pdict)
        player.difficulty = 1
        player.my_turn_id = True

        return player

    def test_first(self, game, player):
        'no test yet'


#@pytest.mark.skip('messes up coverage')
class TestMCTSLoops:

    @pytest.mark.parametrize('board, store, enodes',
                             [
                                 # no loops, make all the nodes
                                 ([4] * 12, [0, 0], NODES + 1),

                                 # game loops, stop searching when found
                                 ([0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                  [23, 23],
                                  12),
                              ],
                             ids=['no_loop', 'loop_12'])
    def test_tree_policy_loops(self, board, store, enodes):

        game, pdict = man_config.make_game('./GameProps/Wari.txt')

        game.turn = True
        game.board = board
        game.store = store

        pdict[ckey.ALGORITHM] = 'montecarlo_ts'
        pdict[ckey.AI_PARAMS][ckey.MCTS_BIAS] = [BIAS_x1000] * 4
        pdict[ckey.AI_PARAMS][ckey.MCTS_NODES] = [NODES] * 4
        pdict[ckey.AI_PARAMS][ckey.MCTS_POUTS] = [POUTS] * 4

        player = ai_player.AiPlayer(game, pdict)
        player.difficulty = 1

        algo = player.algo

        move = player.pick_move()
        game.move(move)

        # algo.game_nodes[0].rprint(pstate=True)
        assert len(algo.game_nodes) == enodes
