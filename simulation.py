from mcts import MCTS
from board import Board
from board_state import BoardState
from player import PlayerID as pid
import random

def get_player(all_players, id):
    for player in all_players:
        if(player.player_id == id):
            return player
    assert(False)
    return None


def simulate(player_1, player_2):
    my_board = Board(None)
    players = [player_1, player_2]
    start_player_id = pid.P1 if (random.random() > 0.5) else pid.P2
    current_player = get_player(players, start_player_id)
    state = BoardState(my_board, start_player_id)
    while state.get_moves() != [] and state.winner_is_unclear():
        move = current_player.get_move(state)
        state.do_move(move)
        current_player = get_player(players, state.next_player)

    winner_id = state.get_winner_id()
    for player in players:
        player.end_game(winner_id, state.get_score(player.player_id))
