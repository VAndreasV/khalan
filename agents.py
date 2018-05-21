from player import PlayerID as pid
from mcts import MCTS
from mc_rave import MCRAVE
from node import Node
from rave_node import RAVENode, UCRAVENode
import random

class Agent():
    def __init__(self, player_id, node_conf, max_steps = 0, max_time = 0):
        self.player_id = player_id
        self.node_conf = node_conf
        self.max_steps = max_steps
        self.max_time = max_time
        self.games_played = 0
        self.wins = 0
        self.scores = []
        self.win_scores = []
        self.lose_scores = []

    def reset(self):
        self.wins = 0
        self.games_played = 0
        self.scores = []
        self.win_scores = []
        self.lose_scores = []

    def get_move(self, state):
        print('Override get_move function for this Agent')
        assert(False)

    def end_game(self, winner_id, score):
        self.games_played += 1
        self.scores.append(score)
        if(winner_id == self.player_id):
            self.wins += 1
            self.win_scores.append(score)
        elif winner_id is not None:
            self.lose_scores.append(score)


class MCTSAgent(Agent):    
    def __init__(self, player_id, node_conf, max_steps = 0, max_time = 0):
        assert(max_time > 0 or max_steps > 0)
        Agent.__init__(self, player_id, node_conf, max_steps, max_time)
        tag_id = max_steps if max_steps > 0 else max_time
        self.tag = 'MCTS {}\nc{}'.format(tag_id, self.node_conf.UCBC)
        
    def get_move(self, state):
        return MCTS(state, self.max_steps, self.player_id, self.node_conf)

class RandomAgent(Agent):
    def __init__(self, player_id, node_conf, max_steps = 0, max_time = 0):
        Agent.__init__(self, player_id, node_conf, max_steps, max_time)
        self.tag = 'Random'

    def get_move(self, state):
        return random.choice(state.get_moves())

class RAVEAgent(Agent):
    def __init__(self, player_id, node_conf, max_steps = 0, max_time = 0):
        assert(max_time > 0 or max_steps > 0)
        Agent.__init__(self, player_id, node_conf, max_steps, max_time)
        tag_id = max_steps if max_steps > 0 else max_time
        self.tag = 'RAVE {}\nk{}'.format(tag_id, self.node_conf.RAVEK)

    def get_move(self, state):
        return MCRAVE(state, self.max_steps, self.player_id, RAVENode, self.node_conf)


class UCRAVEAgent(Agent):
    def __init__(self, player_id, node_conf, max_steps = 0, max_time = 0):
        assert(max_time > 0 or max_steps > 0)
        Agent.__init__(self, player_id, node_conf, max_steps, max_time)
        tag_id = max_steps if max_steps > 0 else max_time
        self.tag = 'ucrave {}\nc{} k{}'.format(tag_id, self.node_conf.UCBC, self.node_conf.RAVEK)

    def get_move(self, state):
        return MCRAVE(state, self.max_steps, self.player_id, UCRAVENode, self.node_conf)
