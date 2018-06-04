import numpy as np
import random

def get_sim_pol_class(id):
    if id == 'rnd':
        return RandomRollout
    elif id == 'urg':
        return UrgentRollout
    assert(False)
    return None

class RollOutPolicy(object):

    def rollout(self, state):
        action_mask = 0
        while state.get_moves() != [] and state.winner_is_unclear():
            move = self.select_move(state)
            action_mask |= (1 << move)
            state.do_move(move)
        return state, action_mask

    def select_move(self, state):
        print('Implement select_move')
        assert(False)


class RandomRollout(RollOutPolicy):
    def select_move(self, state):
        return random.choice(state.get_moves())


class UrgentRollout(RollOutPolicy):
    def select_move(self, state):
        possible_moves = state.get_moves()
        probs = np.zeros(len(possible_moves))
        for idx, move in enumerate(possible_moves):
            probs[idx] = state.get_move_urgency(move)
        probs /= np.sum(probs)
        sample = random.random()
        total_prob = 0.0
        for idx, prob in enumerate(probs):
            total_prob += prob
            if sample <= total_prob:
                return possible_moves[idx]
        return possible_moves[-1]

