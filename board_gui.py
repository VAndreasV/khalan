import tkinter as tk
from tkinter import messagebox
from board import Board, Store, Base
import player as p

STORE_WIDTH = 1
STORE_HEIGHT = 1

class StoreGUI(object):
    def __init__(self, frame, game, store, row_pos, col_pos):
        self.store = store
        self.button = tk.Button(frame, 
                                text=store.stones,
                                command=self.store.act,
                                width=STORE_WIDTH,
                                height=STORE_HEIGHT,
                                bg=p.get_player_color(store.owner))
        self.button.grid(row=row_pos, column=col_pos, sticky=tk.W+tk.N)
        if(store.owner == p.PlayerID.P2):
            self.button.config(state=tk.DISABLED)

    def refresh(self):
        self.button.config(text=self.store.stones)

    def enable(self, enable):
        if(enable):
            self.button.config(state=tk.NORMAL)
        else:
            self.button.config(state=tk.DISABLED)


class BaseGUI(StoreGUI):
    def __init__(self, frame, game, store, row_pos, col_pos):
        self.store = store
        self.button = tk.Button(frame, 
                                text=store.stones,
                                command=None,
                                width=STORE_WIDTH,
                                height=STORE_HEIGHT*3,
                                state=tk.DISABLED,
                                bg=p.get_player_color(store.owner))
        self.button.grid(row=row_pos, column=col_pos, rowspan=2, sticky=tk.W+tk.N)
        

class BoardGUI(tk.Frame):
    def __init__(self, master, game):
        tk.Frame.__init__(self, master)
        self.grid()

        self.game = game
        self.board = game.board
        self.store_guis = []
        '''
                H12 H11 H10 H9  H8  H7
        base 2                         base 1
                H1  H2  H3  H4  H5  H6
        '''
        # Starts at H1
        nb_houses = int((len(self.board.stores) - 2) / 2)
        base_1_id = nb_houses
        base_2_id = nb_houses*2 + 1
        base_2 = BaseGUI(self, 
                         game, 
                         self.board.stores[base_2_id], 
                         0, 
                         0)
        for idx in range(nb_houses):
            self.store_guis.append(StoreGUI(self, 
                                            game, 
                                            self.board.stores[idx], 
                                            1, 
                                            idx+1))
        self.store_guis.append(BaseGUI(self, 
                                        game, 
                                        self.board.stores[base_1_id], 
                                        0, 
                                        nb_houses + 1))
        for idx in range(nb_houses):
            self.store_guis.append(StoreGUI(self, 
                                            game, 
                                            self.board.stores[base_1_id + 1 + idx], 
                                            0, 
                                            nb_houses - idx))
        self.store_guis.append(base_2)

        # add label for current player
        current_pid = self.game.get_current_player()
        tk.Label(self, text="Current Player:").grid(sticky=tk.N+tk.W, row=0, column=nb_houses+2)
        self.player_label = tk.Label(self,
                                    text=p.get_player_name(current_pid),
                                    bg=p.get_player_color(current_pid))
        self.player_label.grid(row=1, column=nb_houses+2, sticky=tk.N)

    def refresh(self):
        for store in self.store_guis:
            store.refresh()
        current_pid = self.game.get_current_player()
        self.player_label.config(text=p.get_player_name(current_pid),
                                bg=p.get_player_color(current_pid))

        for store_id in range(self.board.nb_houses):
            self.store_guis[store_id].enable(current_pid == p.PlayerID.P1)

    def end_game(self):
        score_p1 = self.board.get_player_score(p.PlayerID.P1)
        score_p2 = self.board.get_player_score(p.PlayerID.P2)
        messagebox.showinfo("GAME ENDED!", 
                            'score P1: {}\nscore P2: {}'.format(score_p1, score_p2))