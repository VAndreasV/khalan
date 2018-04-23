import math

UCTK = 1

class Node(object):
    def __init__(self, state, move=None, parent=None, player=None):
        '''
        state   = the state at this node
        move    = the last move (how we got to this node)
        player  = the one who played the 'move'
        '''
        self.move = move
        self.parent = parent
        self.children = []
        self.state = state
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.get_moves()
        self.player = player

    def select_child(self):
        '''
        Selects a child using UCB
        '''
        s = sorted(self.children, 
                   key = lambda c: c.wins/c.visits + UCTK * math.sqrt(2*math.log(self.visits)/c.visits))
        return s[-1]

    def add_child(self, move, state, player):
        n = Node(state, move, self, player)
        self.untriedMoves.remove(move)
        self.children.append(n)
        return n

    def update(self, result):
        self.visits += 1
        self.wins += result