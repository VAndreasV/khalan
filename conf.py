from player import PlayerID as pid
import pprint

DEF_GAMES = 10
DEF_AGENT_TYPE = 'mcts'
DEF_SIMS = 100
DEF_SIM_POL = 'rnd'
DEF_UCB_C = 1
DEF_RAVE_K = 0.5

DEF_PATH = '../results/'

class Configuration():
    def __init__(self, args):
        self.nb_games = args.g

        self.a1_conf = AgentConfig(pid.P1,
                                   args.a1,
                                   args.UCBC1,
                                   args.RAVEK1,
                                   args.spa1,
                                   args.sa1)
        self.a2_conf = AgentConfig(pid.P2,
                                   args.a2,
                                   args.UCBC2,
                                   args.RAVEK2,
                                   args.spa2,
                                   args.sa2)

    def get_agent_conf(self, p_id):
        if p_id == pid.P1:
            return self.a1_conf
        elif p_id == pid.P2:
            return self.a2_conf
        assert(False)
        return None
    
    def get_prefix(self):
        prefix = DEF_PATH
        prefix += '{}_VS_{}_g{}'.format(self.a1_conf.get_tag(),
                                        self.a2_conf.get_tag(),
                                        self.nb_games)
        return prefix

    def log(self):
        filename = self.get_prefix()
        filename += '_conf.txt'
        file = open(filename, 'w')

        file.write('General config:\n')
        file.write(pprint.pformat(vars(self)))
        file.write('\nAgent 1:\n')
        file.write(self.a1_conf.get_log())
        file.write('\nAgent 2:\n')
        file.write(self.a2_conf.get_log())

        file.close
        

class AgentConfig(object):
    def __init__(self, id, agent_type, c, k, sim_pol, max_steps):
        self.player_id = id
        self.agent_type = agent_type
        self.c = c
        self.k = k
        self.sim_pol = sim_pol
        self.max_steps = max_steps
        self.max_time = 0
        self.node_conf = NodeConfig(c, k, int(k * max_steps))
    
    def get_tag(self):
        tag = self.agent_type

        if self.sim_pol != DEF_SIM_POL:
            tag += '-{}'.format(self.sim_pol)
        if self.max_steps != DEF_SIMS:
            tag += '-{}'.format(self.max_steps)
        if self.node_conf.UCBC != DEF_UCB_C:
            tag += '-c{}'.format(self.node_conf.UCBC)
        if self.node_conf.RAVEK != DEF_RAVE_K:
            tag += '-{}'.format(self.node_conf.RAVEK)

        return tag

    def get_log(self):
        return pprint.pformat(vars(self))

class NodeConfig(object):
    def __init__(self, UCBC, RAVEK, BETAK):
        self.UCBC = UCBC
        self.RAVEK = RAVEK
        self.BETAK = BETAK