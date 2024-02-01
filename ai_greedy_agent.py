import copy
import heapq
from edge import edge
from agent import agent
from graph_grid import grid_to_graph, create_distance_graph, kruskal


class search_agent(agent):
    def __init__(self, x, y):
        super().__init__(x, y)

    def act(self, init_graph):
        print(best_first_search(init_graph, h))
        # print(init_graph)


class Node:
    def __init__(self, graph, h, g=0):
        self.graph = graph
        self.h = h
        self.g = g
        self.prev = None

    def __lt__(self, other):
        return self.h < other.h

    def __repr__(self):
        return str(self.graph) + ", h: " + str(self.h) + ",g: " + str(self.g)


def expand(node):
    if node.graph.graph_state['T'] > 100: #change to the undelivered package with earliest time (failed to deliver)
        return []

    successors = []
    possible_moves = ["R", "U", "D", "L"]
    for move in possible_moves:
        new_node = copy.deepcopy(node)
        current_x = new_node.graph.graph_state["Agents"]['S'].X
        current_y = new_node.graph.graph_state["Agents"]['S'].Y
        next_move = None
        if move == 'R':
            next_move = edge(current_x + 1, current_y, current_x, current_y)
            if current_x + 1 >= new_node.graph.graph_state['X'] or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"]['S'].X += 1
        if move == 'L':
            next_move = edge(current_x - 1, current_y, current_x, current_y)
            if current_x - 1 < 0 or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"]['S'].X -= 1
        if move == 'U':
            next_move = edge(current_x, current_y + 1, current_x, current_y)
            if current_y + 1 >= new_node.graph.graph_state['Y'] or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"]['S'].Y += 1
        if move == 'D':
            next_move = edge(current_x, current_y - 1, current_x, current_y)
            if current_y - 1 < 0 or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"]['S'].Y -= 1
        if next_move in new_node.graph.graph_state['F']:
            new_node.graph.graph_state['F'].remove(next_move)
            new_node.graph.graph_state['B'].append(next_move)
        new_node.prev = node
        new_node.graph.graph_state['T'] += 1
        new_node.g = node.g + 1
        new_node.h = h(new_node.graph)
        new_node.graph.pick_up_package()
        successors.append(new_node)
    return successors


def best_first_search(init_state, h):  # we can use the same function for greedy search and A* by giving h or h+g
    init_node = Node(init_state, h(init_state))
    open_nodes = [init_node]
    # close = []
    while True:
        if not open_nodes:
            return None  # failure
        else:
            node = heapq.heappop(open_nodes)
            # check goal state
            if goal_test(node.graph):
                return retrieve_path(node)
            successors = expand(node)
            for successor in successors:
                heapq.heappush(open_nodes, successor)


def goal_test(state):
    return not state.graph_state['P']


def retrieve_path(node):
    path = []
    while node:
        path.insert(0, (node.graph.graph_state["Agents"]['S'].X, node.graph.graph_state["Agents"]['S'].Y))
        node = node.prev
    return path


def h(graph):
    #  dumb heuristic func
    graph_grid = grid_to_graph(graph.graph_state['X'], graph.graph_state['Y'])
    important_points = [(agent.X, agent.Y) for agent in graph.graph_state['Agents'].values()] + list(map(lambda pack: pack.point, list(filter(lambda p: not p.picked, graph.graph_state['P'])))) + [package.delivery for package in graph.graph_state['P']]
    distances = []
    for i in range(len(important_points)):
        for j in range(i + 1,len(important_points)):
            distances.append((important_points[i], important_points[j], len(dijkstra(graph_grid, important_points[i], important_points[j])) - 1))

    graph_grid = create_distance_graph(distances)
    graph_grid = kruskal(graph_grid)
    h_value = sum(map(lambda x: x[2], graph_grid))
    return h_value


# f is the distance of the node so far + h
def f(node):
    return node.g + node.h
