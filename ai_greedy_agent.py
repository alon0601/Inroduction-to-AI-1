from ai_global_functions import *
import heapq
from agent import agent


class search_agent(agent):
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
    def __init__(self, graph, h):
        self.graph = graph
        self.h = h
        self.g = 0
        self.prev = None

    def __lt__(self, other):
        return self.h < other.h

    def __repr__(self):
        return str(self.graph) + ", h: " + str(self.h) + ",g: " + str(self.g)


def best_first_search(init_state, h):
    init_node = Node(init_state, h(init_state))
    open_nodes = [init_node]
    close = []
    while True:
        if not open_nodes:
            return None  # failure
        else:
            node = heapq.heappop(open_nodes)
            if goal_test(node.graph):
                return retrieve_path(node, 'S')
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
                successors = expand(node, 'S')
                for successor in successors:
                    heapq.heappush(open_nodes, successor)

