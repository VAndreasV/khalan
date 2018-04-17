import math

class Node(object):
    def __init__(self, state, move=None, parent=None):
        self.move = move
        self.parent = parent
        self.children = []
        self.state = state
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.get_moves()
        self.player = state.next_player

    def select_child(self):
        '''
        Selects a child using UCB
        '''
        s = sorted(self.children, 
                   key = lambda c: c.wins/c.visits + math.sqrt(2*math.log(self.visits)/c.visits))[-1]
        return s

    def add_child(self, move, state):
        n = Node(state, move, self)
        self.untriedMoves.remove(move)
        self.children.append(n)
        return n

    def update(self, result):
        self.visits += 1
        self.wins += result