import argparse
from simulation import simulate
from main import make_agent, DEF_RAVE_K, DEF_UCB_C, DEF_SIMS
from player import PlayerID as pid
import plotting as p
from node import NodeConfig
import numpy as np

DEF_EXPL_GAMES = 1000

def explore_c(args):
    # Result containers
    total_data = []

    # Constant opponent
    a2_node_conf = NodeConfig(DEF_UCB_C, DEF_RAVE_K, int(DEF_RAVE_K * DEF_SIMS))
    agent_2 = make_agent(pid.P2, args.p2_strategy, a2_node_conf, DEF_SIMS)

    for c in np.arange(args.min, args.max+args.s, args.s):
        a1_node_conf = NodeConfig(c, DEF_RAVE_K, int(DEF_RAVE_K * DEF_SIMS))
        agent_1 = make_agent(pid.P1, args.p1_strategy, a1_node_conf, DEF_SIMS)

        agent_2.reset()

        for _ in range(args.g):
            simulate(agent_1, agent_2)
        total_data.append(agent_1.scores)
        print('c = {} DONE'.format(c))
        c += args.s
    
    p.plot_exploration(total_data, args.p1_strategy, 'c', args.min, args.max, args.s, args.p2_strategy)

def explore_k(args):
    # Result containers
    total_data = []

    # Constant opponent
    a2_node_conf = NodeConfig(DEF_UCB_C, DEF_RAVE_K, int(DEF_RAVE_K * DEF_SIMS))
    agent_2 = make_agent(pid.P2, args.p2_strategy, a2_node_conf, DEF_SIMS)

    for k in np.arange(args.min, args.max+args.s, args.s):
        a1_node_conf = NodeConfig(DEF_UCB_C, k, int(k * DEF_SIMS))
        agent_1 = make_agent(pid.P1, args.p1_strategy, a1_node_conf, DEF_SIMS)

        agent_2.reset()

        for _ in range(DEF_EXPL_GAMES):
            simulate(agent_1, agent_2)
        total_data.append(agent_1.scores)
        print('k = {} DONE'.format(k))
    
    p.plot_exploration(total_data, args.p1_strategy, 'k', args.min, args.max, args.s, args.p2_strategy)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-g', default=DEF_EXPL_GAMES, type=int,
                        help="Games to play.")

    parser.add_argument('-p', default='c',
                        help="Parameter to explore {c, k}")

    parser.add_argument('-min', default = 0.0, type=float,
                        help="Minimum value (incl) for exploration")
    parser.add_argument('-max', default=1.0, type=float,
                        help="Maximum value (incl) for exploration")
    parser.add_argument('-s', default=0.1, type=float,
                        help="Step")

    parser.add_argument('-p1_strategy', default='rnd',
                        help="Strategy of the exploring player\n[rnd, mcts, rave, ucrave]")
    parser.add_argument('-p2_strategy', default='rnd',
                        help="Staregy of the opponent, with constant parameters.\n[rnd, mcts, rave, ucrave]")

    args = parser.parse_args()

    print('Parameter exploration is broken, early return.')
    return 0

    '''assert(args.p1_strategy != 'rnd')

    if args.p == 'k':
        explore_k(args)
    elif args.p == 'c':
        explore_c(args)
    else:
        assert(False)'''
