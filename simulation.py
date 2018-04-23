from mcts import MCTS
from board import Board
from board_state import BoardState
from player import PlayerID as pid
import agents as a
import random
import plotting as p

def get_player(all_players, id):
    for player in all_players:
        if(player.player_id == id):
            return player
    assert(False)
    return None

p1_started_games = 0

def simulate(player_1, player_2):
    global p1_started_games
    my_board = Board(None)
    players = [player_1, player_2]
    start_player_id = pid.P1 if (random.random() > 0.5) else pid.P2
    if(start_player_id == pid.P1):
        p1_started_games += 1
    current_player = get_player(players, start_player_id)
    state = BoardState(my_board, start_player_id)
    while state.get_moves() != [] and state.winner_is_unclear():
        move = current_player.get_move(state)
        state.do_move(move)
        current_player = get_player(players, state.next_player)

    winner_id = state.get_winner_id()
    for player in players:
        player.end_game(winner_id)

agent_1 = a.MCTSAgent(pid.P1, max_steps=100)
agent_2 = a.MCTSAgent(pid.P2, max_steps=1000)
#agent_2 = a.RandomAgent(pid.P2)

total_games = 100

for _ in range(total_games):
    simulate(agent_1, agent_2)
p.plot_simulation_results(agent_1, agent_2)
print('p1 started {} of {} games'.format(p1_started_games, total_games))
print('Done')
