import random
from node import Node

def find_root_in_children(node, rootstate, player):
    '''
    Check this node and its children.
    rootstate = state to find
    player = player that did the last move before this state
    '''
    if node.player != player:
        return None
    if node.state == rootstate:
        return node
    for n in node.children:
        option = find_root_in_children(n, rootstate, player)
        if option is not None:
            return option


def find_root_node(rootstate, prev_root, node_conf, player):
    root_node = None
    if rootstate.prev_player == player:
        assert(rootstate == prev_root.state)
        root_node = prev_root
    else:
        for n in prev_root.children:
            root_node = find_root_in_children(n, rootstate, rootstate.prev_player)
            if root_node is not None:
                break

    if root_node is not None:
        root_node.parent = None
        assert(root_node.state == rootstate)
        assert(root_node.player == rootstate.prev_player)
    return root_node


def MCTSCONT(rootstate, itermax, player, node_conf, sim_pol, prev_root):
    '''
    Do a tree search for maximumiterma iterations
    returning the best move
    '''
    assert(rootstate.next_player == player)
    rootnode = None
    if prev_root != None:
        rootnode = find_root_node(rootstate, prev_root, node_conf, player)

    if rootnode == None:
        rootnode = Node(rootstate, node_conf, None, None, player)

    nodes_added = 0
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
            nodes_added += 1

        # Rollout random play from this child node
        rollout_p = sim_pol()
        end_state, _ = rollout_p.rollout(state.clone())

        # Backpropagate the result
        while node != None:
            node.update(end_state.get_result(node.player))
            node = node.parent

    #print('added {} nodes in {} sims'.format(nodes_added, itermax))
    # Return best move
    action_root = sorted(rootnode.children, key = lambda c:c.visits) [-1]
    move = action_root.move
    return move, action_root
