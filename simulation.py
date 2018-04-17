from game import Game
from mcts import MCTS
from board import Board
from board_state import BoardState
from player import PlayerID as pid

#my_game = Game(True)
my_board = Board(None)

player = pid.P1
state = BoardState(my_board, player)
while state.get_moves() != []:
    move = MCTS(state, 100)
    state.do_move(move)
    player = state.next_player
print('done')