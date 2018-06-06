import player as p
from board import HOUSES, INIT_STONES
import numpy as np

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
    return HOUSES if player_id == p.PlayerID.P1 else HOUSES*2 + 1

class BoardState():
    '''
    One state of the game
    Contains info on:
        - the board
        - current and previous player
    '''
    def __init__(self, board, next_player):
        self.next_player = next_player
        self.prev_player = None
        self.stores = []
        self.stones_to_win = HOUSES * INIT_STONES
        if board:
            for store in board.stores:
                self.stores.append(store.stones)

    def __eq__(self, other):
        return (self.next_player == other.next_player and
                self.stores == other.stores)

    def clone(self):
        st = BoardState(None, None)
        st.prev_player = self.prev_player
        st.next_player = self.next_player
        st.stores = self.stores[:]
        return st

    def do_move(self, move):
        player = self.next_player
        self.prev_player = player
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

    def winner_is_unclear(self):
        '''
        When a player has more than half the stones in the game collected
        in his base, he wins, whatever play follows.
        So we say the winner is unclear when none of the players has this amount 
        collected
        '''
        p1_score = self.get_score(p.PlayerID.P1)
        if(p1_score > self.stones_to_win):
            return False
        p2_score = self.get_score(p.PlayerID.P2)
        return p2_score <= self.stones_to_win


    def get_result(self, player):
        player_score = self.get_score(player)
        opp_score = self.get_score(p.get_other_player(player))
        if player_score > opp_score:
            return 1.0
        elif opp_score > player_score:
            return 0.0
        if self.get_moves() == []:
            return 0.5
        assert(False)

    def get_score(self, player_id):
        base = get_base_id(player_id)
        return self.stores[base]

    def get_winner_id(self):
        p1_score = self.get_score(p.PlayerID.P1)
        p2_score = self.get_score(p.PlayerID.P2)
        if(p1_score == p2_score):
            return None
        elif(p1_score > p2_score):
            return p.PlayerID.P1
        return p.PlayerID.P2

    def get_end_score_str(self):
        p1_score = self.get_score(p.PlayerID.P1)
        p2_score = self.get_score(p.PlayerID.P2)
        return ('score P1: {}\nscore P2: {}'.format(p1_score, p2_score))

    def get_expected_gain(self, move):
        total_gain = 0
        player = self.next_player
        assert(is_owner(move, player))
        assert(not is_base(move))
        assert(self.stores[move] > 0)
        stones = self.stores[move]
        current_store = move
        drop_ids = np.zeros(len(self.stores))
        while stones > 0:
            current_store = (current_store+1) % len(self.stores)
            # don't drop in opponents base
            if is_base(current_store):
                if not is_owner(current_store, player):
                    continue
                else:
                    total_gain += 1
            # drop 1 in all others
            drop_ids[current_store] += 1
            stones -= 1

        # Check for bonus: if we dropped one in one of our empty stores
        if (is_owner(current_store, player) and
            (self.stores[current_store] == 0) and
            (not is_base(current_store))):
            opp_id = get_opposite_id(current_store)
            # increment total gain
            total_gain += 1 # last dropped stone
            total_gain += self.stores[opp_id] # opposite store bonus
            total_gain += drop_ids[opp_id] # potential extra drop
        return total_gain

    def get_prevented_loss(self, move):
        # See if the opposite store is empty
        # = possible use for opponent bonus
        opp_id = get_opposite_id(move)
        if(self.stores[opp_id] == 0):
            return self.stores[move]
        return 0

    def get_move_urgency(self, move):
        # Capture escape = stones that can be captured by playing this move + 
        #                  stones that we prevent from being captured by playing this move
        expected_gain = self.get_expected_gain(move)
        prevented_loss = self.get_prevented_loss(move)
        return expected_gain + prevented_loss
