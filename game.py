import numpy as np
import tkinter as tk
from board import Board
from board_gui import BoardGUI
from board_state import BoardState
from player import PlayerID as pid
import player as p
import time
from agents import make_agent_from_config

class Game(object):
    def __init__(self, createGUI, agent_conf):
        self.board = Board(self)
        self.current_player = pid.P1
        self.has_ended = False
        self.agent = make_agent_from_config(agent_conf)

        if createGUI:
            self.root = tk.Tk()
            self.root.title("Kalah")
            self.root.geometry("400x50")

            self.board_GUI = BoardGUI(self.root, self)

            self.root.mainloop()
        else:
            self.board_GUI = None
            self.root = None

    def act(self, store):
        # Validate
        assert(store.owner == self.current_player)
        assert(not(store.is_base()))
        assert(store.stones > 0)

        # empty store
        stones = store.empty()

        last_store = self.board.divide_stones(stones, store)

        # See if we capture bonus
        # this happens when we drop our last stone
        # in an empty store on our side
        if(last_store.owner == self.current_player and
            last_store.stones == 1 and
            not last_store.is_base()):
            # Put last stone in our base
            last_store.empty()
            self.board.bonus_deposit(self.current_player, 1)
            # Put stones of store at opposite side in our base
            opp_store = self.board.get_opposite_store(last_store)
            stones = opp_store.empty()
            self.board.bonus_deposit(self.current_player, stones)

        # Determine next player
        if not(last_store.is_base()):
            self.current_player = p.get_other_player(self.current_player)   

        # refresh gui
        if self.board_GUI:
            self.board_GUI.refresh()

        self.post_act()

    def post_act(self):
        '''
        evaluate game state after each action
        '''
        possible_moves_p1 = self.board.get_possible_actions(pid.P1)
        possible_moves_p2 = self.board.get_possible_actions(pid.P2)
        game_finished = (len(possible_moves_p1) == 0 or
                         len(possible_moves_p2) == 0)
        if(game_finished):
            self.end_game(possible_moves_p1, possible_moves_p2)
            return

        # let the bot play
        if(self.current_player == pid.P2):
            state = BoardState(self.board, self.current_player)
            move = self.agent.get_move(state)
            store = self.board.get_store(move)
            self.act(store)
            
    def end_game(self, moves_p1, moves_p2):
        for store in moves_p1:
            stones = store.empty()
            self.board.bonus_deposit(pid.P1, stones)
        for store in moves_p2:
            stones = store.empty()
            self.board.bonus_deposit(pid.P2, stones)

        if self.board_GUI:
            self.board_GUI.refresh()
            self.board_GUI.end_game()
            self.root.destroy()
        self.has_ended = True

    def get_current_player(self):
        return self.current_player