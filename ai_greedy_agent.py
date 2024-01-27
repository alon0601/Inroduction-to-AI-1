import copy


def expand(node):
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
        new_node.prev = node
        new_node.g = node.g + 1
        new_node.h = h(new_node)
        neighbors.append(new_node)
    return neighbors


def greedy_heuristic_agent(problem, h):
    open = [problem.Initial_State]
    close = []
    while(True):
        if len(open) == 0:
            return "failure"
        else:
            state = open.pop(0)
            if problem.Goal_Test(state, h):
                return state
            expand_array = expand(state)
            print("FINISH EXPAND")
            open = open + expand_array
            sort_by_h(open, h)


def sort_by_h(open, h):
    new_state = open.pop(0)
    minimum = h(new_state)
    for state in open:
        heuristic = h(state)
        if heuristic < minimum:
            minimum = heuristic
            open.insert(0, new_state)
            new_state = state
            open.remove(state)
    open.insert(0, new_state)


def h(node):
    return node.g + node.h