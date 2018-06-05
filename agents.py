from player import PlayerID as pid
from mcts import MCTS
from mc_rave import MCRAVE
from mcts_cont import MCTSCONT
from node import Node
from rave_node import RAVENode, UCRAVENode
import random
from rollout_policy import get_sim_pol_class



def make_agent(p_id, conf):
    agent_conf = conf.get_agent_conf(p_id)
    return make_agent_from_config(agent_conf)

def make_agent_from_config(agent_conf):
    agent_type = agent_conf.agent_type
    if agent_type == 'rnd':
        return RandomAgent(agent_conf)
    elif agent_type == 'mcts':
        return MCTSAgent(agent_conf)
    elif agent_type == 'rave':
        return RAVEAgent(agent_conf)
    elif agent_type == 'ucrave':
        return UCRAVEAgent(agent_conf)
    elif agent_type == 'mcts_cont':
        return ContinuousMCTSAgent(agent_conf)
    else:
        assert(False)
        return None


class Agent():
    def __init__(self, agent_conf):
        self.player_id = agent_conf.player_id
        self.node_conf = agent_conf.node_conf
        self.sim_pol = get_sim_pol_class(agent_conf.sim_pol)
        self.max_steps = agent_conf.max_steps
        self.max_time = agent_conf.max_time
        assert(self.max_time > 0 or self.max_steps > 0)
        self.tag = agent_conf.get_tag()

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
    def __init__(self, agent_conf):
        Agent.__init__(self, agent_conf)
        
    def get_move(self, state):
        return MCTS(state, self.max_steps, self.player_id, self.node_conf, self.sim_pol)

class RandomAgent(Agent):
    def __init__(self, agent_conf):
        Agent.__init__(self, agent_conf)

    def get_move(self, state):
        return random.choice(state.get_moves())

class RAVEAgent(Agent):
    def __init__(self,agent_conf):
        Agent.__init__(self, agent_conf)

    def get_move(self, state):
        return MCRAVE(state, self.max_steps, self.player_id, RAVENode, self.node_conf, self.sim_pol)


class UCRAVEAgent(Agent):
    def __init__(self, agent_conf):
        Agent.__init__(self, agent_conf)

    def get_move(self, state):
        return MCRAVE(state, self.max_steps, self.player_id, UCRAVENode, self.node_conf, self.sim_pol)

class ContinuousMCTSAgent(Agent):
    def __init__(self, agent_conf):
        Agent.__init__(self, agent_conf)
        self.prev_root = None

    def get_move(self, state):
        move, action_root = MCTSCONT(state, self.max_steps, self.player_id, self.node_conf, self.sim_pol, self.prev_root)
        self.prev_root = action_root
        return move