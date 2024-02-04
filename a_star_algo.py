from graph_grid import grid_to_graph, create_distance_graph, kruskal,dijkstra
import copy
import heapq
from edge import edge
from agent import agent

num_of_expands = None

class a_star_agent(agent):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.path = None
        self.move_count = 0

    def act(self, init_graph):
        if not self.path:
            self.path = best_first_search(init_graph, h)
        if len(self.path) >= 2:
            self.move_count = min(self.move_count+1, len(self.path) - 1)
            self.move_request = self.path[self.move_count]


class Node:
    def __init__(self, graph, h, g=0):
        self.graph = graph
        self.h = h
        self.g = g
        self.prev = None

    def __lt__(self, other):
        return self.g + self.h < other.g + other.h

    def __repr__(self):
        return str(self.graph) + ", h: " + str(self.h) + ",g: " + str(self.g)


def expand(node):
    global num_of_expands
    # do not expand further if some undelivered package is overdue
    for package in node.graph.graph_state['P']:
        if node.graph.graph_state['T'] > package.d_time:
            return []

    successors = []
    possible_moves = ["R", "U", "D", "L"]
    for move in possible_moves:
        new_node = copy.deepcopy(node)
        current_x = new_node.graph.graph_state["Agents"]['R'].X
        current_y = new_node.graph.graph_state["Agents"]['R'].Y
        next_move = None
        if move == 'R':
            next_move = edge(current_x + 1, current_y, current_x, current_y)
            if current_x + 1 >= new_node.graph.graph_state['X'] or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"]['R'].X += 1
        if move == 'L':
            next_move = edge(current_x - 1, current_y, current_x, current_y)
            if current_x - 1 < 0 or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"]['R'].X -= 1
        if move == 'U':
            next_move = edge(current_x, current_y + 1, current_x, current_y)
            if current_y + 1 >= new_node.graph.graph_state['Y'] or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"]['R'].Y += 1
        if move == 'D':
            next_move = edge(current_x, current_y - 1, current_x, current_y)
            if current_y - 1 < 0 or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"]['R'].Y -= 1
        if next_move in new_node.graph.graph_state['F']:
            new_node.graph.graph_state['F'].remove(next_move)
            new_node.graph.graph_state['B'].append(next_move)
        new_node.prev = node
        new_node.graph.graph_state['T'] += 1
        new_node.g = node.g + 1
        new_node.graph.pick_up_package()
        new_node.h = h(new_node.graph)
        successors.append(new_node)
    num_of_expands += len(successors)
    return successors


def best_first_search(init_state, h):
    global num_of_expands
    num_of_expands = 0
    limit = 3000000
    init_node = Node(init_state, h(init_state))
    open_nodes = [init_node]
    close = []
    while limit > num_of_expands:
        if not open_nodes:
            return None  # failure
        else:
            node = heapq.heappop(open_nodes)
            if goal_test(node.graph):
                return retrieve_path(node)
            equal_state = list(filter(lambda other_node: other_node.graph == node.graph, close))
            need_to_expand = False
            if len(equal_state) == 0:
                heapq.heappush(close, node)
                need_to_expand = True
            elif len(equal_state) >= 1:
                for other_node in equal_state:
                    if other_node > node:
                        close.remove(other_node)
                        heapq.heappush(close, node)
                        need_to_expand = True
            if need_to_expand:
                successors = expand(node)
                for successor in successors:
                    heapq.heappush(open_nodes, successor)
    return "pass limit expansion"


def goal_test(state):
    return not state.graph_state['P']


def retrieve_path(node):
    path = []
    while node:
        path.insert(0, (node.graph.graph_state["Agents"]['R'].X, node.graph.graph_state["Agents"]['R'].Y, node.h + node.g))
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
