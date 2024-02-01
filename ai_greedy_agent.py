import copy
import heapq
from edge import edge
from agent import agent


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
        return str(self.graph) + ", " + str(self.h) + ", " + str(self.g)


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
            if current_x + 1 > new_node.graph.graph_state['X'] or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"]['S'].X += 1
        if move == 'L':
            next_move = edge(current_x - 1, current_y, current_x, current_y)
            if current_x - 1 < 0 or next_move in new_node.graph.graph_state['B']:
                continue
            new_node.graph.graph_state["Agents"]['S'].X -= 1
        if move == 'U':
            next_move = edge(current_x, current_y + 1, current_x, current_y)
            if current_y + 1 > new_node.graph.graph_state['Y'] or next_move in new_node.graph.graph_state['B']:
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
            print("current node", node)
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
    mst = {}
    graph.graph_state['Edge'] = set()
    number_of_vertex = 0
    vertex_to_number = {}
    for agent in graph.graph_state['Agents'].values():
        if not vertex_to_number.get((agent.X, agent.Y)):
            vertex_to_number[(agent.X, agent.Y)] = number_of_vertex
            number_of_vertex += 1
        agent_vertex = vertex_to_number[(agent.X, agent.Y)]
        for package in graph.graph_state['P']:
                if not vertex_to_number.get(package.point):
                    vertex_to_number[package.point] = number_of_vertex
                    number_of_vertex += 1
                if not vertex_to_number.get(package.delivery):
                    vertex_to_number[package.delivery] = number_of_vertex
                    number_of_vertex += 1
                package_p_vertex = vertex_to_number[package.point]
                package_d_vertex = vertex_to_number[package.delivery]
                weight = abs(agent.X - package.p_x) + abs(agent.Y - package.p_y)
                if not (package_p_vertex, agent_vertex, weight) in graph.graph_state['Edge']:
                    graph.add_edge(agent_vertex, package_p_vertex, weight)
                    weight = abs(agent.X - package.d_x) + abs(agent.Y - package.d_y)
                if not (package_d_vertex, agent_vertex, weight) in graph.graph_state['Edge']:
                    graph.add_edge(agent_vertex, package_d_vertex, weight)
    package_pairs = [(a, b) for idx, a in enumerate(graph.graph_state['P']) for b in graph.graph_state['P'][idx + 1:]]
    for package_pair in package_pairs:
        package_p_vertex_1 = vertex_to_number[package_pair[0].point]
        package_p_vertex_2 = vertex_to_number[package_pair[1].point]
        package_d_vertex_1 = vertex_to_number[package_pair[0].delivery]
        package_d_vertex_2 = vertex_to_number[package_pair[1].delivery]
        weight_p = abs(package_pair[0].p_x - package_pair[1].p_x) + abs(package_pair[0].p_y - package_pair[1].p_y)
        if not (package_p_vertex_2, package_p_vertex_1, weight_p) in graph.graph_state['Edge']:
            graph.add_edge(package_p_vertex_1, vertex_to_number[package_pair[1].point], weight_p)
        weight_d = abs(package_pair[0].d_x - package_pair[1].d_x) + abs(package_pair[0].d_y - package_pair[1].d_y)
        if not (package_d_vertex_2, package_d_vertex_1, weight_d) in graph.graph_state['Edge']:
            graph.add_edge(package_d_vertex_1, package_d_vertex_2, weight_d)
        if not (package_d_vertex_2, package_p_vertex_1, weight_d) in graph.graph_state['Edge']:
            graph.add_edge(package_p_vertex_1, package_d_vertex_2, weight_d)
        if not (package_p_vertex_2, package_d_vertex_1, weight_d) in graph.graph_state['Edge']:
            graph.add_edge(package_d_vertex_1, package_p_vertex_2, weight_d)
        if not (package_d_vertex_1, package_p_vertex_1, weight_d) in graph.graph_state['Edge']:
            graph.add_edge(package_p_vertex_1, package_d_vertex_1, weight_d)
        if not (package_d_vertex_2, package_p_vertex_2, weight_d) in graph.graph_state['Edge']:
            graph.add_edge(package_p_vertex_2, package_d_vertex_2, weight_d)
    graph.graph_state['V'] = list(range(number_of_vertex))
    return graph.KruskalMST()


# f is the distance of the node so far + h
def f(node):
    return node.g + node.h
