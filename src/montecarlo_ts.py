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
NBR_NODES = 200
NBR_POUTS = 1

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
                 *, leaf=False, winner=None, moves=()):

        self.state = state
        self.node_id = node_id
        self.leaf = leaf
        self.winner = winner

        self.childs = {move: None for move in moves}

        self.reward = 0
        self.visits = 0


    def __repr__(self):
        return f'GameNode({self.node_id}, {self.leaf}, ' \
            f'{self.reward}, {self.visits}, {self.childs})'


    def __str__(self):
        string = f'Id: {self.node_id}  Reward: {self.reward}  ' \
            f'Visits: {self.visits}\n'
        string += f'Leaf: {self.leaf}  Winner: {self.winner}\n'
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

class MonteCarloTS(ai_interface.AiAlgorithmIf):
    """The mixin for the monte carlo tree search ai player.
    Put the start state in as node 0."""


    def __init__(self, game, player):

        super().__init__(game, player)

        self.bias = BIAS
        self.new_nodes = NBR_NODES
        self.nbr_pouts = NBR_POUTS

        self.game_nodes = collections.deque()
        self.node_dict = {}
        self.move_desc = None

        self.next_id = 0


    def add_node(self, state, moves=(), *, leaf=False, winner=None):
        """Create the game node and add it to both the dict
        and node list.

        This must be used for all node creation to keep
        self.game_nodes[id].node_id == id."""

        node = GameNode(state, self.next_id,
                        leaf=leaf, winner=winner, moves=moves)

        self.game_nodes.append(node)
        self.next_id += 1

        self.node_dict[node.state] = node

        return node


    def _new_root(self):
        """Reset the game tree and create a new root."""

        self.node_dict = {}
        self.game_nodes = collections.deque()
        self.next_id = 0

        state = self.game.state
        start_node = self.add_node(state, moves=self.game.get_moves())

        return start_node


    def pick_move(self):
        """Pick the best next move."""

        start_node = self._new_root()

        for _ in range(self.new_nodes):

            node_hist = self.tree_policy(start_node)

            tree_node = self.game_nodes[node_hist[0]]
            if not tree_node.leaf:
                winner, reward = self.default_policy(node_hist[0])
            else:
                winner, reward = tree_node.winner, 1

            self.backup(node_hist, winner, reward)

        node = self.best_child(start_node, 0)
        return node.move


    def tree_policy(self, node):
        """Traverse down the path of 'best' nodes, until one of:
            1. we find a leaf node
            2. there's an incomplete node (unexplored child node)
        then build a new node.

        Return the history of move nodes (which is built with the
        newest node at the begining)."""

        node_hist = collections.deque()
        node_hist.appendleft(node.node_id)

        while not node.leaf:

            if all(cstate for cstate in node.childs.values()):
                node = self.best_child(node, self.bias).node
                node_hist.appendleft(node.node_id)

            else:
                node = self.expand(node)
                node_hist.appendleft(node.node_id)
                break

        return node_hist


    def expand(self, pnode):
        """There is a child of node, that is not yet expanded,
        expand it by creating a new node."""

        moves = [move for move, cstate in pnode.childs.items() if not cstate]
        assert moves, "No moves in pnode in expand."
        move = random.choice(moves)

        saved_state = self.game.state

        self.game.state = pnode.state
        cond = self.game.move(move)

        new_state = self.game.state

        if new_state in self.node_dict:
            node = self.node_dict[new_state]
            pnode.add_child_state(move, node)
            self.game.state = saved_state
            return node

        if cond and cond.is_ended():
            node = self.add_node(new_state, leaf=True, winner=self.game.turn)
        else:
            node = self.add_node(new_state, moves=self.game.get_moves())
        pnode.add_child_state(move, node)

        self.game.state = saved_state
        return node


    def best_child(self, pnode, bias, exclude=()):
        """Return the move and child node associated with the best score."""

        def score(cld, bias, num):
            return cld.reward / cld.visits + bias * math.sqrt(num / cld.visits)

        num = 2 * math.log(pnode.visits)

        moves = [BestMove(move=move, node=cnode,
                          score=score(cnode, bias, num))
                 for move, cnode in pnode.childs.items()
                 if cnode and cnode.node_id not in exclude]

        self.move_desc = 'MonteCarloTS  ' \
            + ', '.join(f'm{move.move} {move.score:.4}' for move in moves) \
            + ' '

        return max(moves, key=lambda b: b.score)


    def _one_playout(self, node_id):
        """Simulate a random game from node,
        return the winner (if there was one) and reward."""
        # XXXX could choose eval func (score?) instead of random choice

        saved_state = self.game.state
        self.game.state = self.game_nodes[node_id].state

        for _ in range(MAX_TURNS):

            moves = self.game.get_moves()
            assert moves, "No moves in _one_playout."

            move = random.choice(moves)
            cond = self.game.move(move)

            if cond and cond.is_ended():
                break

            if self.game.info.mustpass:
                self.game.test_pass()

        winner, reward = None, 0
        if cond in [gi.WinCond.WIN, gi.WinCond.ROUND_WIN]:
            winner = self.game.get_turn()
            reward = 1

        self.game.state = saved_state
        return winner, reward


    def default_policy(self, node_id):
        """Do playouts.
        Do a small number of play_outs sum the rewards for the
        winners. Return the average reward for whichever is the
        largest reward."""

        rewards = [0, 0]
        for _ in range(self.nbr_pouts):
            winner, reward = self._one_playout(node_id)
            if winner:
                rewards[winner] += reward

        if rewards[0] > rewards[1]:
            return False, rewards[0] / self.nbr_pouts

        if rewards[0] < rewards[1]:
            return True, rewards[1] / self.nbr_pouts

        return None, 0

        # return self._one_playout(node_id)


    def backup(self, node_hist, winner, reward):
        """Propagate reward back through move history
        node_hist is a deque of node_ids with newest elements first."""

        for node_id in node_hist:
            node = self.game_nodes[node_id]

            node.visits += 1
            if winner == node.state.turn:
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
