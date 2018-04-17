import player as p

INIT_STONES = 4
HOUSES = 6

class Store(object):
    def __init__(self, game, owner, id):
        self.game = game
        self.owner = owner
        self.stones = INIT_STONES
        self.id = id

    def is_base(self):
        return False

    def empty(self):
        stones = self.stones
        self.stones = 0
        return stones

    def deposit(self, player, stones):
        self.stones += stones

    def act(self):
        self.game.act(self)


class Base(Store):
    def __init__(self, game, owner, id):
        Store.__init__(self, game, owner, id)
        self.stones = 0

    def is_base(self):
        return True

    def empty(self):
        assert(False)

    def deposit(self, player, stones):
        assert player == self.owner
        Store.deposit(self, player, stones)

    def act(self):
        assert(False)

class Board(object):
    def __init__(self, game): 
        self.game = game
        self.nb_houses = HOUSES 
        self.reset()       

    def reset(self):
        '''
                H12 H11 H10 H9  H8  H7
        base 2                            base 1
                H1  H2  H3  H4  H5  H6
        '''
        self.stores = []
        id = 0
        for _ in range(self.nb_houses):
            self.stores.append(Store(self.game,
                                     p.PlayerID.P1, 
                                     id))
            id += 1
        self.stores.append(Base(self.game,
                                p.PlayerID.P1,
                                id))
        id += 1
        for _ in range(self.nb_houses):
            self.stores.append(Store(self.game,
                                     p.PlayerID.P2,
                                     id))
            id += 1
        self.stores.append(Base(self.game,
                                p.PlayerID.P2,
                                id))

    def get_store(self, inId):
        return self.stores[inId]

    def get_next_valid_store(self, current_id, current_pid):
        '''
        CCW order
        do NOT deposit in other players' base
        '''
        next_id = current_id
        while True:
            next_id = (next_id + 1) % len(self.stores)
            store = self.stores[next_id]
            if(not(store.is_base() and 
                   store.owner != current_pid)):
                return store
    
    def divide_stones(self, stones, current_store):
        '''
        Divide the stones in CCW order
        return last store we put a stone in
        '''
        assert(stones > 0)
        store_id = current_store.id
        current_pid = self.game.get_current_player()
        while stones > 0:
            store = self.get_next_valid_store(store_id, current_pid)
            store.deposit(current_pid, 1)
            stones -= 1
            store_id = store.id
        return self.stores[store_id]

    def get_opposite_store(self, store):
        assert( not(store.is_base()))
        store_id = store.id
        opposite_id = -1
        if store_id > self.nb_houses:
            opposite_id = self.nb_houses - (store_id - self.nb_houses)
        else:
            opposite_id = self.nb_houses*2 - store_id
        return self.stores[opposite_id]


    def bonus_deposit(self, current_pid, stones):
        '''
        Put stones in this players base
        '''
        base_id = self.nb_houses if current_pid == p.PlayerID.P1 else self.nb_houses*2 + 1
        self.stores[base_id].deposit(current_pid, stones)

    def get_player_score(self, player_id):
        base_id = self.nb_houses if player_id == p.PlayerID.P1 else self.nb_houses*2 + 1
        return self.stores[base_id].stones

    def get_possible_actions(self, player_id):
        possible_stores = []
        for store in self.stores:
            if store.is_base() or store.owner != player_id:
                continue
            if store.stones > 0:
                possible_stores.append(store)
        return possible_stores