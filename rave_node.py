from node import Node
import math
from board import HOUSES
import numpy as np


class RAVENode(Node):
    def __init__(self, state, conf, move=None, parent=None, player=None):
        Node.__init__(self, state, conf, move, parent, player)
        self.action_space = 2 + HOUSES * 2
        self.amaf_counts = np.zeros(self.action_space)
        self.amaf_wins = np.zeros(self.action_space)

    def get_beta(self, child):
        return math.sqrt(self.conf.BETAK / (self.conf.BETAK + 3*child.visits))

    '''def get_wins_per_branch(self, current_node, move):
        if current_node.move == move:
            return get_leaf_results(current_node)
        wins = 0
        branches = 0
        for c in current_node.children:
            w, b = self.get_wins_per_branch(c, move)
            wins += w
            branches += b
        return wins, branches'''

    def get_key(self, c):
        move = c.move
        amaf_wins = self.amaf_wins[move]
        amaf_count = self.amaf_counts[move]
        '''amaf_wins = 0
        amaf_count = 0
        for child in c.parent.children:
            wins, count = self.get_wins_per_branch(child, move)
            amaf_wins += wins
            amaf_count += count'''
        q = c.wins / c.visits
        q_rave = amaf_wins / amaf_count
        beta = self.get_beta(c)
        return (1-beta) * q + beta * q_rave

    def add_child(self, move, state, player):
        n = RAVENode(state, self.conf, move, self, player)
        self.untriedMoves.remove(move)
        self.children.append(n)
        return n

    def update(self, result, action_mask):
        super(RAVENode, self).update(result)

        for action in range(self.action_space):
            if action_mask & (1 << action):
                self.amaf_counts[action] += 1
                self.amaf_wins[action] += result

        if self.parent is not None:
            action_mask |= (1 << self.move)
        return action_mask

class UCRAVENode(RAVENode):
    def __init__(self, state, conf, move=None, parent=None, player=None):
        RAVENode.__init__(self, state, conf, move, parent, player)

    def get_key(self, c):
        q_start = super(UCRAVENode, self).get_key(c)
        return q_start + self.conf.UCBC * math.sqrt(math.log(self.visits)/c.visits)
    
    def add_child(self, move, state, player):
        n = UCRAVENode(state, self.conf, move, self, player)
        self.untriedMoves.remove(move)
        self.children.append(n)
        return n

'''
def get_leaf_results(node):
    if node.children == []:
        return min(node.wins, 1), 1
    else:
        result = 0
        leafs = 0
        for c in node.children:
            r, l = get_leaf_results(c)
            result += r
            leafs += l
        return result, leafs
'''