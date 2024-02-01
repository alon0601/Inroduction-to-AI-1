from package import package
from edge import edge
from human_agent import human_agent
from interfering_agent import interfering_agent
from greedy_agent import greedy_agent
from ai_greedy_agent import search_agent
import re


class package_graph():
    def __init__(self, init_file_path):
        self.graph_state = {}
        packages = list()
        blocked_edges = list()
        fragile_edges = list()
        agents = {}
        init_file = open(init_file_path, mode='r', encoding='utf-8-sig')
        init_file_lines = init_file.readlines()
        for line in init_file_lines:
            all_numbers_in_line = re.findall(r'-?\b\d+\b', line)
            if line[1] == 'X':
                self.graph_state['X'] = int(all_numbers_in_line[0])
            elif line[1] == 'Y':
                self.graph_state['Y'] = int(all_numbers_in_line[0])
            elif line[1] == 'P':
                packages.append(
                    package(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), int(all_numbers_in_line[2]),
                            int(all_numbers_in_line[3]), int(all_numbers_in_line[4]), int(all_numbers_in_line[5])))
            elif line[1] == 'B':
                blocked_edges.append(
                    edge(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), int(all_numbers_in_line[2]),
                         int(all_numbers_in_line[3])))
            elif line[1] == 'F':
                fragile_edges.append(
                    edge(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), int(all_numbers_in_line[2]),
                         int(all_numbers_in_line[3])))
            elif line[1] == 'A':
                agents[line[1]] = human_agent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]))
            elif line[1] == 'H':
                agents[line[1]] = greedy_agent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]))
            elif line[1] == 'I':
                agents[line[1]] = interfering_agent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]))
            elif line[1] == 'S':
                agents[line[1]] = search_agent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]))
        self.graph_state['Edge'] = set()
        self.graph_state['V'] = []
        self.graph_state['P'] = packages
        self.graph_state['B'] = blocked_edges
        self.graph_state['F'] = fragile_edges
        self.graph_state['Agents'] = agents
        self.graph_state['T'] = 0

    # I moved pick_up_package to here to use it in the search tree
    def pick_up_package(self):
        packages = self.graph_state['P']
        packages_that_delivered = set()
        for age, age_value in self.graph_state['Agents'].items():
            for package in packages:
                if not package.picked and age_value.X == package.p_x and age_value.Y == package.p_y and self.graph_state['T'] >= package.p_time:
                    package.picked = True
                    print("a package has been picked!")
                    age_value.packages.append(package)
                elif package.picked and package in age_value.packages and age_value.X == package.d_x and age_value.Y == package.d_y and self.graph_state['T'] <= package.d_time:
                    packages_that_delivered.add(package)
                    print("a package has been delivered!")

        self.graph_state['P'] = [package for package in packages if package not in packages_that_delivered]

    def add_edge(self, u, v, w):
        self.graph_state['Edge'].add((u, v, w))

    # A utility function to find set of an element i
    # (truly uses path compression technique)
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def KruskalMST(self):
        # This will store the resultant MST
        result = []

        # An index variable, used for sorted edges
        i = 0

        # An index variable, used for result[]
        e = 0

        # Sort all the edges in
        # non-decreasing order of their
        # weight
        edge_list = sorted(list(self.graph_state['Edge']), key=lambda item: item[2])

        parent = []
        rank = []

        # Create V subsets with single elements
        for node in range(len(self.graph_state['V'])):
            parent.append(node)
            rank.append(0)

            # Number of edges to be taken is less than to V-1
        while e < len(self.graph_state['V']) - 1:

            # Pick the smallest edge and increment
            # the index for next iteration
            u, v, w = edge_list[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            # If including this edge doesn't
            # cause cycle, then include it in result
            # and increment the index of result
            # for next edge
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
                # Else discard the edge

        minimumCost = 0
        for u, v, weight in result:
            minimumCost += weight
        print("Minimum Spanning Tree cost: ", minimumCost)
        return minimumCost

    def __repr__(self):
        graph_string = ""
        for key, value in self.graph_state.items():
            graph_string += key + ": " + str(value) + "\n"
        return graph_string
