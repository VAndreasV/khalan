
from node import NodeConfig
from player import PlayerID as pid
from rollout_policy import get_sim_pol_class

DEF_GAMES = 10
DEF_AGENT_TYPE = 'mcts_cont'
DEF_SIMS = 200
DEF_SIM_POL = 'rnd'
DEF_UCB_C = 1
DEF_RAVE_K = 0.5

class Configuration():
    def __init__(self, args):
        self.agent_1_type = args.a1
        self.agent_2_type = args.a2

        self.nb_games = args.g

        self.agent_1_simulations = args.sa1
        self.agent_2_simulations = args.sa2

        self.agent_1_sim_pol = args.spa1
        self.agent_2_sim_pol = args.spa2

        self.ucb_1_c = args.UCBC1
        self.ucb_2_c = args.UCBC2

        self.rave_1_k = args.RAVEK1
        self.rave_2_k = args.RAVEK2

    def get_node_conf(self, player_id):
        if player_id == pid.P1:
            return NodeConfig(self.ucb_1_c,
                              self.rave_1_k,
                              int(self.rave_1_k * self.agent_1_simulations))
        elif player_id == pid.P2:
            return NodeConfig(self.ucb_2_c,
                              self.rave_2_k,
                              int(self.rave_2_k * self.agent_2_simulations))
        assert(False)
        return None

    def get_agent_type(self, player_id):
        if player_id == pid.P1:
            return self.agent_1_type
        elif player_id == pid.P2:
            return self.agent_2_type
        assert(False)
        return None
    
    def get_max_steps(self, player_id):
        if player_id == pid.P1:
            return self.agent_1_simulations
        elif player_id == pid.P2:
            return self.agent_2_simulations
        assert(False)
        return None

    def get_sim_pol(self, player_id):
        if player_id == pid.P1:
            return get_sim_pol_class(self.agent_1_sim_pol)
        elif player_id == pid.P2:
            return get_sim_pol_class(self.agent_2_sim_pol)
        assert(False)
        return None

    def get_postfix(self, player_id):
        result = ''
        if player_id == pid.P1:
            if self.agent_1_sim_pol != DEF_SIM_POL:
                result += '_{}'.format(self.agent_1_sim_pol)

        elif player_id == pid.P2:
            if self.agent_1_sim_pol != DEF_SIM_POL:
                result += '_{}'.format(self.agent_1_sim_pol)

        else:
            assert(False)


        return result