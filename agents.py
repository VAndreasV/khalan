from player import PlayerID as pid
from mcts import MCTS
from mc_rave import MCRAVE
from mcts_cont import MCTSCONT
from node import Node
from rave_node import RAVENode, UCRAVENode
import random
from conf import DEF_SIM_POL


def make_agent(p_id, conf):
    node_conf = conf.get_node_conf(p_id)
    agent_type = conf.get_agent_type(p_id)
    max_steps = conf.get_max_steps(p_id)
    sim_pol = conf.get_sim_pol(p_id)
    if agent_type == 'rnd':
        return RandomAgent(p_id, node_conf, sim_pol)
    elif agent_type == 'mcts':
        return MCTSAgent(p_id, node_conf, sim_pol, max_steps)
    elif agent_type == 'rave':
        return RAVEAgent(p_id, node_conf, sim_pol, max_steps)
    elif agent_type == 'ucrave':
        return UCRAVEAgent(p_id, node_conf, sim_pol, max_steps)
    elif agent_type == 'mcts_cont':
        return ContinuousMCTSAgent(p_id, node_conf, sim_pol, max_steps)
    else:
        assert(False)
        return None


class Agent():
    def __init__(self, player_id, node_conf, sim_pol, max_steps = 0, max_time = 0):
        self.player_id = player_id
        self.node_conf = node_conf
        self.sim_pol = sim_pol
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
    def __init__(self, player_id, node_conf, sim_pol, max_steps = 0, max_time = 0):
        assert(max_time > 0 or max_steps > 0)
        Agent.__init__(self, player_id, node_conf, sim_pol, max_steps, max_time)
        tag_id = max_steps if max_steps > 0 else max_time
        #self.tag = 'MCTS {}\nc{}'.format(tag_id, self.node_conf.UCBC)
        self.tag = 'mcts'
        if sim_pol != DEF_SIM_POL:
            self.tag += '_urg'
        
    def get_move(self, state):
        return MCTS(state, self.max_steps, self.player_id, self.node_conf, self.sim_pol)

class RandomAgent(Agent):
    def __init__(self, player_id, node_conf, sim_pol, max_steps = 0, max_time = 0):
        Agent.__init__(self, player_id, node_conf, sim_pol, max_steps, max_time)
        self.tag = 'rnd'

    def get_move(self, state):
        return random.choice(state.get_moves())

class RAVEAgent(Agent):
    def __init__(self, player_id, node_conf, sim_pol, max_steps = 0, max_time = 0):
        assert(max_time > 0 or max_steps > 0)
        Agent.__init__(self, player_id, node_conf, sim_pol, max_steps, max_time)
        tag_id = max_steps if max_steps > 0 else max_time
        #self.tag = 'RAVE {}\nk{}'.format(tag_id, self.node_conf.RAVEK)
        self.tag = 'rave'

    def get_move(self, state):
        return MCRAVE(state, self.max_steps, self.player_id, RAVENode, self.node_conf, self.sim_pol)


class UCRAVEAgent(Agent):
    def __init__(self, player_id, node_conf, sim_pol, max_steps = 0, max_time = 0):
        assert(max_time > 0 or max_steps > 0)
        Agent.__init__(self, player_id, node_conf, sim_pol, max_steps, max_time)
        tag_id = max_steps if max_steps > 0 else max_time
        #self.tag = 'ucrave {}\nc{} k{}'.format(tag_id, self.node_conf.UCBC, self.node_conf.RAVEK)
        self.tag = 'ucrave'

    def get_move(self, state):
        return MCRAVE(state, self.max_steps, self.player_id, UCRAVENode, self.node_conf, self.sim_pol)

class ContinuousMCTSAgent(Agent):
    def __init__(self, player_id, node_conf, sim_pol, max_steps = 0, max_time = 0):
        assert(max_time > 0 or max_steps > 0)
        Agent.__init__(self, player_id, node_conf, sim_pol, max_steps, max_time)
        tag_id = max_steps if max_steps > 0 else max_time
        #self.tag = 'mcts_cont {}\nc{}'.format(tag_id, self.node_conf.UCBC)
        self.tag = 'mcts_cont'
        self.prev_root = None

    def get_move(self, state):
        move, action_root = MCTSCONT(state, self.max_steps, self.player_id, self.node_conf, self.sim_pol, self.prev_root)
        self.prev_root = action_root
        return move