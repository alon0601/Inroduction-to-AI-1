from graph_grid import grid_to_graph, dijkstra, create_distance_graph, kruskal
from edge import edge
import copy


def goal_test(state):
    return not state.graph_state['P']


def retrieve_path(node, agent_char):
    path = []
    while node:
        path.insert(0, (node.graph.graph_state["Agents"][agent_char].X, node.graph.graph_state["Agents"][agent_char].Y, node.h + node.g))
        node = node.prev
    return path


def h(graph):
    graph_grid = grid_to_graph(graph.graph_state['X']+1, graph.graph_state['Y']+1)
    important_points = [(graph.graph_state['Agents']['R'].X, graph.graph_state['Agents']['R'].Y)] + list(map(lambda pack: pack.point, list(filter(lambda p: not p.picked, graph.graph_state['P'])))) + [package.delivery for package in graph.graph_state['P']]
    distances = []
    for i in range(len(important_points)):
        for j in range(i + 1, len(important_points)):
            distances.append((important_points[i], important_points[j], len(dijkstra(graph_grid, important_points[i], important_points[j])) - 1))

    graph_grid = create_distance_graph(distances)
    graph_grid = kruskal(graph_grid)
    h_value = sum(map(lambda x: x[2], graph_grid))
    return h_value


def expand(node, agent_char):
    global num_of_expands
    # do not expand further if some undelivered package is overdue
    for package in node.graph.graph_state['P']:
        if node.graph.graph_state['T'] > package.d_time:
            return []

    successors = []
    possible_moves = ["R", "U", "D", "L"]
    for move in possible_moves:
        new_node = copy.deepcopy(node)
        current_x = new_node.graph.graph_state["Agents"][agent_char].X
        current_y = new_node.graph.graph_state["Agents"][agent_char].Y
        next_move = None
        if move == 'R':
            next_move = edge(current_x + 1, current_y, current_x, current_y)
            if current_x + 1 >= new_node.graph.graph_state['X'] or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"][agent_char].X += 1
        if move == 'L':
            next_move = edge(current_x - 1, current_y, current_x, current_y)
            if current_x - 1 < 0 or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"][agent_char].X -= 1
        if move == 'U':
            next_move = edge(current_x, current_y + 1, current_x, current_y)
            if current_y + 1 >= new_node.graph.graph_state['Y'] or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"][agent_char].Y += 1
        if move == 'D':
            next_move = edge(current_x, current_y - 1, current_x, current_y)
            if current_y - 1 < 0 or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"][agent_char].Y -= 1
        if next_move in new_node.graph.graph_state['F']:
            new_node.graph.graph_state['F'].remove(next_move)
            new_node.graph.graph_state['B'].append(next_move)
        new_node.prev = node
        new_node.graph.graph_state['T'] += 1
        new_node.g = node.g + 1
        new_node.graph.pick_up_package()
        new_node.h = h(new_node.graph)
        successors.append(new_node)
    return successors
