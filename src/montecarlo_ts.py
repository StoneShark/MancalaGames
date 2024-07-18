# -*- coding: utf-8 -*-
"""An ai player that uses Monte Carlo Tree Search
to select the next move.

Created on Sat Aug  5 10:31:39 2023
@author: Ann"""

import collections
import dataclasses as dc
import math
import random

import ai_interface
import game_interface as gi


# %% constants

# these are only used if the config file does not have values
BIAS = 0.25
NBR_NODES = 300
NBR_POUTS = 2

MAX_TURNS = 500

# %% best

@dc.dataclass(frozen=True, kw_only=True)
class BestMove:
    """The best move tuple."""

    move: int
    node: object   # it will be a game node
    score: int


# %%  game nodes


class GameNode:
    """A class for keeping the game tree nodes."""

    def __init__(self, state, node_id,
                 *, leaf=False, reward=0.0, moves=()):

        self.state = state
        self.node_id = node_id
        self.leaf = leaf         # the game is over

        self.childs = {move: None for move in moves}

        self.reward = reward
        self.visits = 0


    def __str__(self):
        string = f'Id: {self.node_id}  Reward: {self.reward}  ' \
            f'Visits: {self.visits}\n'
        if self.leaf:
            string += f'Leaf: {self.leaf}\n'
        string += str(self.state) + '\n'
        string += 'Leaf  ' if self.leaf else ''
        for move, child in self.childs.items():
            ctext = f'{child.node_id},{child.reward}' if child else 'none'
            string += f'{move}: {ctext} '
        string += ' (id,reward)'
        return string


    def add_child_state(self, move, cstate):
        """Save the child state for move."""

        self.childs[move] = cstate

# %%

def clear_mcount(state):
    """Clear the move count from the game states used
    as dictionary keys in the node_dict of MonteCarloTS

    The move count should be accurate for the GameNode.state"""

    object.__setattr__(state, 'mcount', 0)
    return state


def set_mcount_from(game, state):
    """Set the move number to match that in the game."""

    object.__setattr__(state, 'mcount', game.mcount)
    return state


# %%

class MonteCarloTS(ai_interface.AiAlgorithmIf):
    """The mixin for the monte carlo tree search ai player.
    Put the start state in as node 0."""


    def __init__(self, game, player):

        super().__init__(game, player)

        self.my_turn_id = None        # record who we are (turn) on the first turn

        self.bias = BIAS
        self.new_nodes = NBR_NODES
        self.nbr_pouts = NBR_POUTS

        self.game_nodes = collections.deque()  # list of game nodes by id
        self.node_dict = {}                    # dict of game nodes by game state
        self.move_desc = None

        self.next_id = 0  # cummulative count of node ids


    def add_node(self, state, moves=(), *, leaf=False, reward=0.0):
        """Create the game node and add it to both the dict
        and node list.

        state's mcount can still be set or already cleared,
        clearing it again is ok.

        This must be used for all node creation to keep
        self.game_nodes[id].node_id == id."""

        state_nocount = clear_mcount(state)

        node = GameNode(state_nocount, self.next_id,
                        leaf=leaf, reward=reward, moves=moves)

        self.game_nodes.append(node)
        self.next_id += 1

        self.node_dict[state_nocount] = node

        return node


    def clear_history(self):
        """Reset the game tree and create a new root."""

        self.my_turn_id = None
        self.node_dict = {}
        self.game_nodes = collections.deque()
        self.next_id = 0


    def pick_move(self):
        """Pick the best next move.
        If a current game state has a node use it, otherwise
        build a node for the current game state.

        1. If first call, save who we are (my turn id), otherwise check it.
        2. Find or create a start_node representing the current game state.
        3. Do tree policy to find a new node to explore
        4. Do the rollouts
        5. Back propagate the reward
        6. Pick the best child of the start_node
        """

        if self.my_turn_id:
            assert self.my_turn_id == self.game.get_turn(), \
                "MCTS can only be used by one player"
        else:
            self.my_turn_id = self.game.turn

        game_state = clear_mcount(self.game.state)
        if game_state in self.node_dict:
            start_node = self.node_dict[game_state]
            set_mcount_from(self.game, start_node)
        else:
            start_node = self.add_node(game_state, moves=self.game.get_moves())


        for _ in range(self.new_nodes):

            node_hist = self._tree_policy(start_node)
            if not node_hist:
                break

            tree_node = self.game_nodes[node_hist[0]]
            if not tree_node.leaf:
                reward = self._rollouts(node_hist[0])
            else:
                reward = tree_node.reward

            self._backprop(node_hist, reward)

        node = self._best_child(start_node, 0.0)
        return node.move


    def _tree_policy(self, node):
        """Traverse down the path of 'best' nodes, until one of:
            1. we find a leaf node
            2. there's an incomplete node (unexplored child node)
        then build a new node.

        Return the history of move nodes (which is built with the
        newest node at the begining).
        This is kept instead of 'parents' on the tree nodes because
        repeated game states are common in Mancala causing loops."""

        # Could this get stuck finding the same leaf node?
        #   no either the game will come to an end or the other player
        #   will force the game to a new path

        # What if a move is no longer available
        #           e.g. hole closing or becomming a child
        #   can't happen, the game states are different

        node_hist = collections.deque()
        node_hist.appendleft(node.node_id)

        for _ in range(MAX_TURNS):

            if node.leaf:
                break

            if all(cstate for cstate in node.childs.values()):
                node = self._best_child(node, self.bias).node
                if node.node_id in node_hist:
                    print("Found Loop in Tree Policy; ending move search.")
                    return None

                node_hist.appendleft(node.node_id)

            else:
                node = self._expand(node)
                if node.node_id in node_hist:
                    # don't loop, expand another node
                    node.reward -= 1
                    print("Found Loop in expand:\n",
                          f"Reducing reward of {node.node_id};",
                          f"now reward= {node.reward}")
                    continue

                node_hist.appendleft(node.node_id)
                break

        else:
            print(self.game)
            print(node_hist)
            msg = f"Stuck in TREE Policy for {MAX_TURNS}"
            assert False, msg

        return node_hist


    def _expand(self, pnode):
        """There is a child of pnode that is not yet expanded,
        expand it by creating a new node from a random unexplored child."""

        moves = [move for move, cstate in pnode.childs.items() if not cstate]
        assert moves, "No moves in pnode in _expand."
        move = random.choice(moves)

        saved_state = self.game.state

        # XXXX mcount is likely too low, see ai_player rule mcts_move_nbrs
        self.game.state = set_mcount_from(self.game, pnode.state)

        cond = self.game.move(move)
        new_state = clear_mcount(self.game.state)

        if new_state in self.node_dict:
            node = self.node_dict[new_state]

        elif cond and cond.is_ended():
            reward = 1.0 if new_state.turn == self.my_turn_id else 0.0
            node = self.add_node(new_state, leaf=True, reward=reward)

        else:
            node = self.add_node(new_state, moves=self.game.get_moves())

        pnode.add_child_state(move, node)
        self.game.state = saved_state
        return node


    def _best_child(self, pnode, bias):
        """Return the move and child node associated with the best score."""

        def score(cld, bias, num):
            return cld.reward / cld.visits + bias * math.sqrt(num / cld.visits)

        # precompute this term, it doesn't vary by child
        num = 2 * math.log(pnode.visits)

        moves = [BestMove(move=move, node=cnode,
                          score=score(cnode, bias, num))
                 for move, cnode in pnode.childs.items()
                 if cnode]

        self.move_desc = 'MonteCarloTS  ' \
            + ', '.join(f'm{move.move} {move.score:6.4}' for move in moves) \
            + ' '

        return max(moves, key=lambda b: b.score)


    def _one_playout(self, node_id):
        """Simulate a random game from node,
        return the winner (if there was one) and reward."""

        saved_state = self.game.state

        # XXXX mcount is likely too low, see ai_player rule mcts_move_nbrs
        self.game.state = set_mcount_from(self.game,
                                          self.game_nodes[node_id].state)

        for _ in range(MAX_TURNS):

            moves = self.game.get_moves()
            assert moves, "No moves in _one_playout."

            move = random.choice(moves)
            cond = self.game.move(move)

            if cond and cond.is_ended():
                break

            if self.game.info.mustpass:
                self.game.test_pass()

        else:
            cond = None

        reward = 0.0
        if (cond in [gi.WinCond.WIN, gi.WinCond.ROUND_WIN]
            and self.game.get_turn() == self.my_turn_id):
            reward = 1.0

        self.game.state = saved_state
        return reward


    def _rollouts(self, node_id):
        """Do playouts.
        Do a small number of play_outs sum the rewards."""

        reward = 0.0
        for _ in range(self.nbr_pouts):
            reward += self._one_playout(node_id)

        return reward


    def _backprop(self, node_hist, reward):
        """Propagate reward back through move history
        node_hist is a deque of node_ids with newest elements first."""

        for node_id in node_hist:

            node = self.game_nodes[node_id]
            node.visits += 1
            node.reward += reward


    def get_move_desc(self):
        """Return a description of the previous move."""
        return self.move_desc


    def set_params(self, *args):
        """Set the algorithms parameters in this order:
            bias, new_nodes, nbr_pouts"""

        self.bias = BIAS
        self.new_nodes = NBR_NODES
        self.nbr_pouts = NBR_POUTS

        argc = len(args)
        if argc >= 1 and args[0] > 0:
            self.bias = args[0]

        if argc >= 2 and args[1] > 0:
            self.new_nodes = args[1]

        if argc >= 3 and args[2] > 0:
            self.nbr_pouts = args[2]
