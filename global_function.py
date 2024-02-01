import copy


number_expands = 0


def expand(node, h):
    neighbors = []
    possible_moves = ["R", "U", "D", "L"]
    for move in possible_moves:
        new_node = copy.deepcopy(node)
        current_x = new_node.graph_state["Agents"]['A'].X
        current_y = new_node.graph_state["Agents"]['A'].Y
        next_move = {}
        if move == 'R':
            next_move = {(current_x + 1, current_y), (current_x, current_y)}
            if current_x + 1 > new_node.graph_state['X'] and next_move not in new_node.graph_state['B']:
                continue
            current_x += 1
        if move == 'L':
            next_move = {(current_x - 1, current_y), (current_x, current_y)}
            if current_x - 1 < 0 and next_move not in new_node.graph_state['B']:
                continue
            current_x -= 1
        if move == 'U':
            next_move = {(current_x, current_y + 1), (current_x, current_y)}
            if current_y + 1 > new_node.graph_state['Y'] and next_move not in new_node.graph_state['B']:
                continue
            current_y += 1
        if move == 'D':
            next_move = {(current_x, current_y - 1), (current_x, current_y)}
            if current_y - 1 < 0 and next_move not in new_node.graph_state['B']:
                continue
            current_y -= 1
        if next_move in new_node.graph_state['F']:
            new_node.graph_state['F'].remove(next_move)
            new_node.graph_state['B'].append(next_move)
        number_expands += 1
        new_node.prev = node
        new_node.g = node.g + 1
        new_node.h = h(new_node)
        neighbors.append(new_node)
    return neighbors