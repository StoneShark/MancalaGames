# -*- coding: utf-8 -*-
"""An ai player that uses Monte Carlo Tree Search
to select the next move.

Created on Sat Aug  5 10:31:39 2023
@author: Ann"""

import collections as col
import dataclasses as dc
import math
import random

import ai_interface
import game_log

from game_interface import WinCond

# TODO There must errors in this code (montecarlo_ts), because it plays poorly
# could be very bad choice of bias (using 0.4)


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

    next_id = 0

    def __init__(self, state, moves=(), leaf=False):

        self.node_id = GameNode.next_id
        GameNode.next_id += 1
        self.state = state

        self.reward = 0
        self.visits = 0
        self.leaf = leaf

        self.childs = {move: None for move in moves}

    def __repr__(self):
        return f'GameNode({self.node_id}, {self.leaf}, ' \
            f'{self.reward}, {self.visits}, {self.childs})'

    def __str__(self):
        string = f'Id: {self.node_id}  Reward: {self.reward}  ' \
            f'Visits: {self.visits}\n'
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

class MonteCarloTS(ai_interface.AiPlayerIf):
    """The mixin for the monte carlo tree search ai player.
    Put the start state in as node 0."""


    def __init__(self, game, bias):

        super().__init__(game)

        self.bias = bias
        self.new_nodes = 30
        self.game_nodes = col.deque()
        self.node_dict = {}
        self.move_desc = None

        self.add_node(game.state, moves=self.game.get_moves())


    def add_node(self, state, moves=(), leaf=False):
        """Add the game node to both the dict and node list.
        This must be used for all node creation to keep
        game_nodes[id].node_id == id."""

        node = GameNode(state, moves, leaf)
        self.node_dict[node.state] = node
        self.game_nodes.append(node)
        return node


    def pick_move(self):
        """Pick the best next move."""

        state = self.game.state
        if state not in self.node_dict:
            start_node = self.add_node(state, moves=self.game.get_moves())

            game_log.add('\nCreate init node:', game_log.INFO)
            game_log.add(str(start_node), game_log.INFO)
        else:
            start_node = self.node_dict[state]

        for nbr in range(self.new_nodes):

            node_hist = self.tree_policy(start_node)
            winner, reward = self.default_policy(node_hist[0])

            self.backup(node_hist, winner, reward)
            game_log.add(f'END LOOP {nbr}: {winner} {reward}',
                         game_log.INFO)

        game_log.add('\nStart node:', game_log.INFO)
        game_log.add(str(start_node), game_log.INFO)
        node = self.best_child(start_node, 0)
        return node.move


    def tree_policy(self, node):
        """Traverse down the path of 'best' nodes,
        until one of:
            1. we find a leaf node
            2. there's an incomplete node (unexplored child node)
        then build a new node.

        Return the history of move nodes (which is build with the
        newest node at the begining)."""

        node_hist = col.deque()
        node_hist.appendleft(node.node_id)

        while not node.leaf:

            if all(cstate for cstate in node.childs.values()):
                node = self.best_child(node, self.bias).node
                node_hist.appendleft(node.node_id)

            else:
                node = self.expand(node)
                node_hist.appendleft(node.node_id)
                break

        else:
            game_log.add('tree_policy stopping on leaf', game_log.STEP)

        game_log.add('Selected:')
        game_log.add(str(node))

        return node_hist


    def expand(self, pnode):
        """There is a child of node, that is not yet expanded,
        expand it by creating a new node."""

        moves = [move for move, cstate in pnode.childs.items() if not cstate]
        assert moves, "no moves, should we get here?"
        move = random.choice(moves)

        saved_state = self.game.state

        self.game.state = pnode.state
        cond = self.game.move(move)

        new_state = self.game.state

        if new_state in self.node_dict:
            game_log.add(f'Link existing node to {move}.')
            node = self.node_dict[new_state]
            pnode.add_child_state(move, node)
            return node

        game_log.add(f'Expand move {move}.')
        if cond and cond.is_ended():
            node = self.add_node(new_state, leaf=True)
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
            + ', '.join(f'm{move.move} {move.score:6.4}' for move in moves) \
            + ' '

        return max(moves, key=lambda b: b.score)


    def default_policy(self, node_id):
        """Simulate a random game from node,
        return the winner (if there was one) and reward."""
        # XXXX could choose eval func (score?) instead of random choice

        saved_state = self.game.state
        self.game.state = self.game_nodes[node_id].state
        node_hist = col.deque()

        for _ in range(300):

            node_hist.appendleft(hash(self.game.state))

            moves = self.game.get_moves()
            if not moves:
                game_log.add("No moves, but game didn't end:", game_log.IMPORT)
                game_log.add("Prev move result: {cond}", game_log.IMPORT)
                game_log.add(str(self.game), game_log.IMPORT)
                break

            move = random.choice(moves)
            cond = self.game.move(move)

            if cond and cond.is_ended():
                break

        winner, reward = None, 0
        if cond in [WinCond.WIN, WinCond.ROUND_WIN]:
            winner = self.game.get_turn()
            reward = 1

        self.game.state = saved_state

        return winner, reward


    def backup(self, node_hist, winner, reward):
        """Propagate reward back through move history
        node_hist is a deque of node_ids with newest elements first."""

        for node_id in node_hist:
            node = self.game_nodes[node_id]

            node.visits += 1
            if winner == node.state.turn:
                node.reward = node.reward + reward


    def get_move_desc(self):
        """Return a description of the previous move."""
        return self.move_desc


    def set_params(self, params):
        """Set the params from the config file that associate
        with the selected difficulty."""

        # TODO params is still mm_depth
        self.new_nodes = params * 10
