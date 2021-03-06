import random
from node import Node

def MCTS(rootstate, itermax, player, node_conf, sim_pol):
    '''
    Do a tree search for maximumiterma iterations
    returning the best move
    '''
    rootnode = Node(rootstate, node_conf, None, None, player)
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

        # Rollout random play from this child node
        rollout_p = sim_pol()
        state, _ = rollout_p.rollout(state)

        # Backpropagate the result
        while node != None:
            node.update(state.get_result(node.player))
            node = node.parent

    # Return best move
    return sorted(rootnode.children, key = lambda c:c.visits) [-1].move
