'''
Simplified version of the boardstate,
used for MCTS
'''
import player as p
from board import HOUSES, INIT_STONES

def is_owner(store_id, player_id):
    return ((store_id <= HOUSES and player_id == p.PlayerID.P1) or
            (store_id > HOUSES and player_id == p.PlayerID.P2))

def is_base(store_id):
    return (store_id == HOUSES or
            store_id == HOUSES*2 +1)

def get_opposite_id(store_id):
    assert( not is_base(store_id))
    opposite_id = -1
    if store_id > HOUSES:
        opposite_id = HOUSES - (store_id - HOUSES)
    else:
        opposite_id = HOUSES*2 - store_id
    return opposite_id

def get_base_id(player_id):
    return HOUSES if player_id == p.PlayerID.P1 else HOUSES*2 - 1

class BoardState():
    def __init__(self, board, next_player):
        self.next_player = next_player
        self.stores = []
        if board:
            for store in board.stores:
                self.stores.append(store.stones)

    def clone(self):
        st = BoardState(None, None)
        st.next_player = self.next_player
        st.stores = self.stores[:]
        return st

    def do_move(self, move):
        player = self.next_player
        assert(is_owner(move, player))
        assert(not is_base(move))
        assert(self.stores[move] > 0)
        stones = self.stores[move]
        self.stores[move] = 0
        current_store = move
        while stones > 0:
            current_store = (current_store+1) % len(self.stores)
            # don't drop in opponents base
            if(is_base(current_store) and
                not is_owner(current_store, player)):
                continue
            # drop 1 in all others
            self.stores[current_store] += 1
            stones -= 1

        # Check for bonus: if we dropped one in one of our empty stores
        if (is_owner(current_store, player) and
            (self.stores[current_store] == 1) and
            (not is_base(current_store))):
            opp_id = get_opposite_id(current_store)
            # empty these two into the base
            base_id = get_base_id(player)
            self.stores[base_id] += self.stores[opp_id]
            self.stores[opp_id] = 0
            self.stores[base_id] += self.stores[current_store]
            self.stores[current_store] = 0

        self.end_game()

        # bonus turn for ending in our own base
        if is_base(current_store) and is_owner(current_store, player):
            return

        # no bonus turn
        self.next_player = p.get_other_player(player)  

    def end_game(self):
        '''
        Check if for one of the players all his stores are empty
        '''
        moves_p1 = []
        moves_p2 = []
        for i in range(HOUSES):
            if(self.stores[i] > 0):
                moves_p1.append(i)
            if(self.stores[i+HOUSES+1] > 0):
                moves_p2.append(i+HOUSES+1)
        if moves_p1 == [] or moves_p2 == []:
            base_p1 = get_base_id(p.PlayerID.P1)
            for m in moves_p1:
                self.stores[base_p1] += self.stores[m]
                self.stores[m] = 0
            base_p2 = get_base_id(p.PlayerID.P2)
            for m in moves_p2:
                self.stores[base_p2] += self.stores[m]
                self.stores[m] = 0

    def get_moves(self):
        moves = []
        if self.next_player == p.PlayerID.P1:
            for i in range(HOUSES):
                if(self.stores[i] > 0):
                    moves.append(i)
        else:
            for i in range(HOUSES+1, HOUSES*2+1):
                if(self.stores[i] > 0):
                    moves.append(i)
        return moves

    def get_result(self, player):
        player_base = get_base_id(player)
        player_score = self.stores[player_base]
        opp_base = p.get_other_player(player)
        opp_score = self.stores[opp_base]
        if player_score > opp_score:
            return 1.0
        elif opp_score > player_score:
            return 0.0
        if self.get_moves() == []:
            return 0.5
        assert(False)