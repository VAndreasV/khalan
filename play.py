from game import Game
from conf import *
import argparse

from player import PlayerID as pid


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-atype', default=DEF_AGENT_TYPE,
                        help="Agent type\n['rnd', 'mcts', 'rave', 'ucrave']")
    
    parser.add_argument('-s', default=DEF_SIMS, type=int,
                        help="Simulations for Agent")

    parser.add_argument('-sp', default=DEF_SIM_POL,
                        help="Simulation policyfor Agent\n['rnd','urg']")

    parser.add_argument('-UCBC', default=DEF_UCB_C, type=float,
                        help="Agent's UCB weight for exploration")

    parser.add_argument('-RAVEK', default=DEF_RAVE_K, type=float,
                        help="Agent's rave weight for MC/AMAF balance [0.0, 1.0]\nk=0.5 means at 50% of the simulation there's equal\ndistribution between UCB and AMAF")

    args = parser.parse_args()

    agent_conf = AgentConfig(pid.P2,
                             args.atype,
                             args.UCBC,
                             args.RAVEK,
                             args.sp,
                             args.s)
    
    Game(True, agent_conf)