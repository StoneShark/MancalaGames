# -*- coding: utf-8 -*-
"""Unit tests for the monte carlo tree search algorithm.

A simplified connect 4 (with small board) is tested.
Stubbing the game and player helped find issues with the
montecarlo_ts implementation.
Patching in game states is easy to create the needed
test conditions.

Created on Tue Mar 28 09:09:31 2023
@author: Ann"""

# %% imports

import re

import pytest
pytestmark = pytest.mark.unittest

import connect_game
from context import ai_player
from context import cfg_keys as ckey
from context import game_logger
from context import man_config
from context import montecarlo_ts as mcts


# %% constants

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


    @pytest.mark.parametrize('test_state', [True, False])
    def test_rprint(self, capsys, test_state):

        node = mcts.GameNode('parent', 12, moves=(2, 45, 22))
        node.add_child_state(2, mcts.GameNode('first', 14))
        third = mcts.GameNode('third', 16)
        third.add_child_state(13, node)
        node.add_child_state(22, third)

        node.rprint(pstate=test_state)
        data = capsys.readouterr().out

        # all three nodes are printed
        assert data.count('id') == 3

        # all moves listed
        assert all('mv ' + str(nbr) + ':' in data
                   for nbr in (2, 45, 22, 13))

        if not test_state:
            assert 'parent' not in data
            assert 'third' not in data
        else:
            assert 'parent' in data
            assert 'third' in data


class TestMonteCarloTS:

    @staticmethod
    def my_random_choice(values):
        """return the last value"""
        return values[-1]

    @pytest.fixture
    def game(self):
        game = connect_game.ConnectFour()
        game.turn = connect_game.PLAYERS[0]
        return game

    @pytest.fixture
    def player(self):
        return connect_game.DumbPlayer(None, None)

    @pytest.fixture
    def algo(self, game, player, mocker):
        mocker.patch('random.choice', TestMonteCarloTS.my_random_choice)
        return mcts.MonteCarloTS(game, player)


    @pytest.mark.parametrize('params, egood',
                             [
                              # these values should be set
                              ((), True),
                              ([0.3], True),
                              ((0.4, 20), True),
                              ((0.5, 300, 5), True),

                              # type errors should be raised
                              ([20], False),
                              ((0.3, 0.4), False),
                              ((0.3, 200, 0.4), False),

                              # different values are set
                              ((-1, 2, 2),
                               (mcts.BIAS, 2, 2)),
                              ((0.2, -1, 2),
                               (0.2, mcts.NBR_NODES, 2)),
                              ((0.2, 2, -1),
                               (0.2, 2, mcts.NBR_POUTS)),

                              ])
    def test_set_params(self, algo, params, egood):

        if egood is True:
            algo.set_params(*params)
            if len(params) >= 1:
                assert int(algo.bias * 1000) == int(params[0] * 1000)
            if len(params) >= 2:
                assert algo.new_nodes == params[1]
            if len(params) >= 3:
                assert algo.nbr_pouts == params[2]

        elif egood is False:
            with pytest.raises(TypeError):
                algo.set_params(*params)

        else:
            algo.set_params(*params)
            assert int(algo.bias * 1000) == int(egood[0] * 1000)
            algo.new_nodes == egood[1]
            algo.nbr_pouts == egood[2]


    @pytest.mark.parametrize('turn', [True, False])
    def test_setup(self, game, algo, turn):

        assert not algo.game_nodes
        game.turn = turn

        node = algo._setup()
        assert algo.my_turn_id == turn
        assert node == algo.game_nodes[0]
        assert len(algo.game_nodes) == 1
        assert node.state
        assert node.state.board
        assert node.state.turn == turn

        node = algo.game_nodes[0]
        assert node.node_id == 0
        assert node.state in algo.node_dict

        # don't create another game node
        node = algo._setup()
        assert node == algo.game_nodes[0]
        assert len(algo.game_nodes) == 1

        # create another game node
        game.board = 'different'   # and also invalid, but it's ok
        node = algo._setup()
        assert node == algo.game_nodes[1]
        assert len(algo.game_nodes) == 2

        node = algo.game_nodes[1]
        assert node.node_id == 1
        assert node.state in algo.node_dict

        # call _setup with the wrong game turn
        game.turn = not turn
        with pytest.raises(AssertionError):
            algo._setup()


    @pytest.mark.parametrize('force_dupl', [False, True])
    def test_expand(self, game, algo, force_dupl):
        """two game continuing cases:
        else case: expanded node is not in the game tree
        if case: new node is already in the game tree;
        force by putting the opening move in game tree"""

        saved_state = game.state

        start_node = algo._setup()
        assert len(algo.game_nodes) == 1

        if force_dupl:
            algo.add_node(
                connect_game.ConnectState(board=(0, 0, 0, 0,
                                                 0, 0, 0, 0,
                                                 0, 0, 0, 0,
                                                 0, 0, 0, 1),
                                         _turn=2),
                [0, 1, 2, 3])
            assert len(algo.game_nodes) == 2

        node = algo._expand(start_node)

        assert game.state == saved_state     # game state not changed
        assert start_node.childs[3] == node   # random picks the last child
        assert node.leaf == False
        assert node.reward == 0
        assert len(node.childs) == 4
        assert len(algo.game_nodes) == 2


    def test_expand_ended(self, game, algo):
        """elif case: expanded node ends the game.
        Create a node that will result in picking a winning move."""

        saved_state = game.state
        algo._setup()

        start_node = algo.add_node(
            connect_game.ConnectState(board=(0, 0, 0, 0,
                                             0, 0, 2, 1,
                                             0, 0, 2, 1,
                                             0, 0, 2, 1),
                                     _turn=1),
            [0, 1, 2, 3])

        node = algo._expand(start_node)

        assert game.state == saved_state     # game state not changed
        assert start_node.childs[3] == node   # random picks the last child
        assert node.leaf == True
        assert node.reward == 1


    @pytest.mark.parametrize('all_nodes', [False, True])
    def test_best_child(self, algo, all_nodes):
        """Test two cases: all children expanded and not all
        children expanded.  Results same both ways."""

        def set_params(node_id, reward, visits):
            algo.game_nodes[node_id].reward = reward
            algo.game_nodes[node_id].visits = visits

        start_node = algo._setup()    # node 0
        algo._expand(start_node)      # node 1, move 3
        algo._expand(start_node)      # node 2, move 2
        algo._expand(start_node)      # node 3, move 1
        if all_nodes:
            algo._expand(start_node)  # node 4, move 0
        # print(start_node)

        # set the parameters directly
        set_params(0, 2, 20)
                                  # score       sqrt(2 * ln(20) / c_visits)
        set_params(1, 1, 5)       #  0.2 + bias * 1.0947
        set_params(2, 0, 2)       #  0.0 + bias * 1.7306
        set_params(3, 1, 10)      #  0.1 + bias * 0.7740
        if all_nodes:
            set_params(4, 0, 3)   #  0.0 + bias * 1.4132
        # start_node.rprint(pstate=True)

        # nodes 1 & 2:  0.0 + 0.4 * 1.7306 > 0.2 + 0.4 * 1.0947

        best = algo._best_child(start_node, 0.4)
        assert best.move == 2

        best = algo._best_child(start_node, 0.0)
        assert best.move == 3

        move_desc = algo.get_move_desc()
        assert 'MonteCarloTS' in move_desc
        assert '0.0' in move_desc
        assert '0.1' in move_desc
        assert '0.2' in move_desc
        assert re.search('m1.*0.1.*m2.*0.0.*m3.*0.2', move_desc)


    @pytest.mark.parametrize('board, moves, ereward',
                             [
                              ((0, 0, 2, 0,    # will playout as draw
                                1, 2, 1, 0,
                                1, 2, 1, 2,
                                2, 1, 1, 2), (0, 1, 3), 0),

                              ((0, 0, 0, 0,    # 1 will win
                                1, 2, 1, 1,
                                1, 1, 2, 1,
                                1, 2, 1, 1), (0, 1, 2, 3), 1),

                              ((0, 0, 0, 0,    # 2 will win
                                2, 0, 2, 0,
                                2, 1, 2, 2,
                                1, 2, 2, 2), (0, 1, 2, 3), 0),

                              ])
    def test_one_playout(self, algo, board, moves, ereward):
        """Test two cases: all children expanded and not all
        children expanded.  Results same both ways."""

        algo._setup()
        node = algo.add_node(connect_game.ConnectState(board=board, _turn=1),
                             moves)

        assert algo._one_playout(node) == ereward


    def test_one_playout_loop(self, game, algo, mocker):
        """Mock the move method so that none of the moves are
        actually done, this will exercise the else on the for loop."""

        mocker.patch.object(game, 'move', lambda m : None)

        node = algo._setup()
        assert algo._one_playout(node) == 0


    def test_rollouts(self, game, algo, mocker):
        """Stub _one_playout so that it always returns a win."""

        mocker.patch.object(algo, '_one_playout', lambda m : 1)
        algo.nbr_pouts = 100

        start_node = algo._setup()
        assert len(algo.game_nodes) == 1

        reward =  algo._rollouts(start_node)

        assert reward == 100
        assert len(algo.game_nodes) == 1  # no nodes should be added


    def test_tree_policy(self, algo, mocker):
        """don't try to test the loop conditions here"""

        def my_best_child(node, bias):
            """The children should be fully expanded or _tree_policy
            wouldn't call this."""

            for move, cnode in node.childs.items():
                if cnode:
                    return mcts.BestMove(move=move, node=cnode, score=0.4)


        mocker.patch.object(algo, '_best_child', my_best_child)

        start_node = algo._setup()
        algo._tree_policy(start_node)
        algo._tree_policy(start_node)
        algo._tree_policy(start_node)
        algo._tree_policy(start_node)

        assert len(algo.game_nodes) == 5

        # _tree_policy fills all child nodes before going deeper (depth 2)
        assert all(child for child in start_node.childs.values())
        assert all(gchild is None
                       for child in start_node.childs.values()
                           for gchild in child.childs.values())

        for _ in range(45):
            algo._tree_policy(start_node)

        # we should have found at least one leaf
        assert any(cnode.leaf for cnode in algo.game_nodes)

        # print(len(algo.game_nodes))
        # start_node.rprint(pstate=True)



    @pytest.mark.parametrize('move_seq, winner, result', [
        ([2, 1, 1, 1, 1], 2, 'WIN'),
                                          ])
    def test_pick_move(self, game, algo, move_seq, result, winner):
        """Exercise pick move -- only doing a few expansions per move,
        so play is bad."""

        while True:

            print(game)
            if game.turn == connect_game.PLAYERS[0]:
                cond = game.move(algo.pick_move())
                # print(algo.get_move_desc())

                if not move_seq: # op has no more planned moves
                    break

            else:
                cond = game.move(move_seq.pop(0))

            if cond and cond.is_ended():
                break

        # print(game)
        # print(cond)

        if cond:
            assert result in cond.name
            assert game.turn == winner

        algo.clear_history()
        assert not algo.game_nodes
        assert not algo.node_dict
        assert algo.next_id == 0
        assert algo.move_desc is ''
        assert algo.my_turn_id is None


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
