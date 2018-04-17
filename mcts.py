from node import Node
import random

def MCTS(rootstate, itermax):
    '''
    Do a tree search for maximumiterma iterations
    returning the best move
    '''
    rootnode = Node(rootstate)

    for i in range(itermax):
        # start at root
        node = rootnode
        state = rootstate.clone()

        # Select child node
        while node.untriedMoves == [] and node.children != []:
            # Go down tree untill node found with untried moves
            node = node.select_child()
            # Update state along the way
            state.do_move(node.move)

        # Expand this child node
        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves)
            state.do_move(m)
            node = node.add_child(m, state)

        # Rollout random play from this child node
        while state.get_moves() != []:
            state.do_move(random.choice(state.get_moves()))

        # Backpropagate the result
        while node != None:
            node.update(state.get_result(node.player))
            node = node.parent

        # Return best move
        return sorted(rootnode.children, key = lambda c:c.visits) [-1].move

