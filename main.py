import argparse
from simulation import simulate
import agents as a
from player import PlayerID as pid
import plotting as p
from node import NodeConfig

DEF_GAMES = 10
DEF_AGENT_TYPE = 'rnd'
DEF_SIMS = 200
DEF_UCB_C = 1
DEF_RAVE_K = 0.5

def make_agent(p_id, agent_type, node_conf, max_steps):
    if agent_type == 'rnd':
        return a.RandomAgent(p_id, node_conf)
    elif agent_type == 'mcts':
        return a.MCTSAgent(p_id, node_conf, max_steps)
    elif agent_type == 'rave':
        return a.RAVEAgent(p_id, node_conf, max_steps)
    elif agent_type == 'ucrave':
        return a.UCRAVEAgent(p_id, node_conf, max_steps)
    else:
        assert(False)
        return None

def get_agent_tag(agent_type, max_steps, c, k):
    if agent_type == 'rnd':
        return agent_type
    elif agent_type == 'mcts':
        return '{}-{}-c{}'.format(agent_type, max_steps, c)
    elif agent_type == 'rave':
        return '{}-{}-k{}'.format(agent_type, max_steps, k)
    elif agent_type == 'ucrave':
        return '{}-{}-c{}-k{}'.format(agent_type, max_steps, c, k)
    else:
        assert(False)
        return 'ERROR'
    

def run_simulation(args):
    a1_node_conf = NodeConfig(args.UCBC1, args.RAVEK1, int(args.RAVEK1 * args.sa1))
    agent_1 = make_agent(pid.P1, args.a1, a1_node_conf, args.sa1)

    a2_node_conf = NodeConfig(args.UCBC2, args.RAVEK2, int(args.RAVEK2 * args.sa2))
    agent_2 = make_agent(pid.P2, args.a2, a2_node_conf, args.sa2)

    total_games = args.g

    for _ in range(total_games):
        simulate(agent_1, agent_2)
    a1_tag = get_agent_tag(args.a1, args.sa1, args.UCBC1, args.RAVEK1)
    a2_tag = get_agent_tag(args.a2, args.sa2, args.UCBC2, args.RAVEK2)
    prefix = '../results/{}_VS_{}_g{}'.format(a1_tag, a2_tag, args.g)
    p.plot_simulation_results(agent_1, agent_2, prefix)
    p.plot_scores(agent_1, agent_2, prefix)
    print('Done')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-a1', default=DEF_AGENT_TYPE,
                        help="Agent 1 type\n['rnd', 'mcts', 'rave', 'ucrave']")
    parser.add_argument('-a2', default=DEF_AGENT_TYPE,
                        help="Agent 2 type\n['rnd', 'mcts', 'rave', 'ucrave']")

    parser.add_argument('-g', default=DEF_GAMES, type=int,
                        help="Games to be played")
    
    parser.add_argument('-sa1', default=DEF_SIMS, type=int,
                        help="Simulations for Agent 1")
    parser.add_argument('-sa2', default=DEF_SIMS, type=int,
                        help="Simulations for Agent 2")

    parser.add_argument('-UCBC1', default=DEF_UCB_C, type=float,
                        help="Agent 1's UCB weight for exploration")
    parser.add_argument('-UCBC2', default=DEF_UCB_C, type=float,
                        help="Agent 2's UCB weight for exploration")

    parser.add_argument('-RAVEK1', default=DEF_RAVE_K, type=float,
                        help="Agent 1's rave weight for MC/AMAF balance [0.0, 1.0]\nk=0.5 means at 50% of the simulation there's equal\ndistribution between UCB and AMAF")
    parser.add_argument('-RAVEK2', default=DEF_RAVE_K, type=float,
                        help="Agent 2's rave weight for MC/AMAF balance [0.0, 1.0]\nk=0.5 means at 50% of the simulation there's equal\ndistribution between UCB and AMAF")

    args = parser.parse_args()
    run_simulation(args)