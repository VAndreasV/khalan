from player import PlayerID as pid
from mcts import MCTS
import random

class Agent():
    def __init__(self, player_id, max_steps = 0, max_time = 0):
        self.player_id = player_id
        self.max_steps = max_steps
        self.max_time = max_time
        self.games_played = 0
        self.wins = 0

    def get_move(self, state):
        print('Override get_move function for this Agent')
        assert(False)

    def end_game(self, winner_id):
        self.games_played += 1
        if(winner_id == self.player_id):
            self.wins += 1


class MCTSAgent(Agent):    
    def __init__(self, player_id, max_steps = 0, max_time = 0):
        assert(max_time > 0 or max_steps > 0)
        Agent.__init__(self, player_id, max_steps, max_time)
        tag_id = max_steps if max_steps > 0 else max_time
        self.tag = 'MCTS {}'.format(tag_id)
    def get_move(self, state):
        return MCTS(state, self.max_steps, self.player_id)

class RandomAgent(Agent):
    def __init__(self, player_id, max_steps = 0, max_time = 0):
        Agent.__init__(self, player_id, max_steps, max_time)
        self.tag = 'Random'
    def get_move(self, state):
        return random.choice(state.get_moves())
