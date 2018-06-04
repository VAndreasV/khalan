import math

class NodeConfig(object):
    def __init__(self, UCBC, RAVEK, BETAK):
        self.UCBC = UCBC
        self.RAVEK = RAVEK
        self.BETAK = BETAK

class Node(object):
    def __init__(self, state, conf, move=None, parent=None, player=None):
        '''
        state   = the state at this node
        move    = the last move (how we got to this node)
        player  = the one who played the 'move'
        '''
        self.move = move
        self.parent = parent
        self.children = []
        self.state = state
        self.conf = conf
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.get_moves()
        self.player = player

    def matches(self, state, conf):
        return (state == self.state and
                conf == self.conf)

    def get_key(self, c):
        return c.wins/c.visits + self.conf.UCBC * math.sqrt(2*math.log(self.visits)/c.visits)

    def select_child(self):
        '''
        Selects a child using UCB
        '''
        s = sorted(self.children, 
                   key = lambda c: self.get_key(c))
        return s[-1]

    def add_child(self, move, state, player):
        n = Node(state, self.conf, move, self, player)
        self.untriedMoves.remove(move)
        self.children.append(n)
        return n

    def update(self, result):
        self.visits += 1
        self.wins += result