import random

def MCRAVE(rootstate, itermax, player, node_class, node_conf):
    '''
    Do a tree search for maximumiterma iterations
    returning the best move
    '''
    rootnode = node_class(rootstate, node_conf, None, None, player)

    for _ in range(itermax):
        # start at root
        node = rootnode
        state = rootstate.clone()

        # Select child node
        while node.untriedMoves == [] and node.children != []:
            # Go down UC-tree untill node found with untried moves
            node = node.select_child()
            # Update state along the way
            state.do_move(node.move)

        # Expand this child node
        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves)
            player = state.next_player
            state.do_move(m)
            node = node.add_child(m, state, player)

        action_mask = 0
        # Rollout random play from this child node
        while state.get_moves() != [] and state.winner_is_unclear():
            move = random.choice(state.get_moves())
            action_mask |= (1 << move)
            state.do_move(move)

        # Backpropagate the result
        while node != None:
            action_mask = node.update(state.get_result(node.player), action_mask)
            node = node.parent

    # Return best move
    return sorted(rootnode.children, key = lambda c:c.visits) [-1].move

