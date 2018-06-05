import argparse
from simulation import simulate
import agents as a
from player import PlayerID as pid
import plotting as p
from conf import *
    

def run_simulation(conf):
    agent_1 = a.make_agent(pid.P1, conf)

    agent_2 = a.make_agent(pid.P2, conf)

    total_games = args.g

    for i in range(total_games):
        simulate(agent_1, agent_2)
    prefix = conf.get_prefix()
    p.plot_simulation_results(agent_1, agent_2, prefix)
    p.plot_scores(agent_1, agent_2, prefix)
    conf.log()
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

    parser.add_argument('-spa1', default=DEF_SIM_POL,
                        help="Simulation policyfor Agent 1\n['rnd','urg']")
    parser.add_argument('-spa2', default=DEF_SIM_POL,
                        help="Simulation policyfor Agent 2\n['rnd','urg']")

    parser.add_argument('-UCBC1', default=DEF_UCB_C, type=float,
                        help="Agent 1's UCB weight for exploration")
    parser.add_argument('-UCBC2', default=DEF_UCB_C, type=float,
                        help="Agent 2's UCB weight for exploration")

    parser.add_argument('-RAVEK1', default=DEF_RAVE_K, type=float,
                        help="Agent 1's rave weight for MC/AMAF balance [0.0, 1.0]\nk=0.5 means at 50% of the simulation there's equal\ndistribution between UCB and AMAF")
    parser.add_argument('-RAVEK2', default=DEF_RAVE_K, type=float,
                        help="Agent 2's rave weight for MC/AMAF balance [0.0, 1.0]\nk=0.5 means at 50% of the simulation there's equal\ndistribution between UCB and AMAF")

    args = parser.parse_args()
    conf = Configuration(args)
    run_simulation(conf)