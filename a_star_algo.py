import heapq
from ai_global_functions import *
from agent import agent

num_of_expands = None


class a_star_agent(agent):
    def __init__(self, x, y, limit):
        super().__init__(x, y)
        self.path = None
        self.limit = limit
        self.move_count = 0

    def act(self, init_graph):
        if not self.path:
            self.path = best_first_search(init_graph, h, self.limit)
        if self.path == "fail":
            self.move_request = (self.X, self.Y)
        elif len(self.path) >= 2:
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


def best_first_search(init_state, h, limit):
    global num_of_expands
    num_of_expands = 0
    init_node = Node(init_state, h(init_state))
    open_nodes = [init_node]
    close = []
    while limit > num_of_expands:
        if not open_nodes:
            return None  # failure
        else:
            node = heapq.heappop(open_nodes)
            if goal_test(node.graph):
                print("number of total expand is :", num_of_expands)
                return retrieve_path(node, 'R')
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
                successors = expand(node, 'R')
                num_of_expands += len(successors)
                for successor in successors:
                    heapq.heappush(open_nodes, successor)
    return "fail"
