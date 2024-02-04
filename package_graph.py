from package import package
from edge import edge
from human_agent import human_agent
from interfering_agent import interfering_agent
from greedy_agent import greedy_agent
from ai_greedy_agent import search_agent
from a_star_algo import a_star_agent
from real_time_a_star import rta_agent
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
            elif line[1] == 'R':
                agents[line[1]] = a_star_agent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]))
            elif line[1] == 'D':
                agents[line[1]] = rta_agent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]))
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
                    age_value.packages.append(package)
                elif package.picked and package in age_value.packages and age_value.X == package.d_x and age_value.Y == package.d_y and self.graph_state['T'] <= package.d_time:
                    packages_that_delivered.add(package)

        self.graph_state['P'] = [package for package in packages if package not in packages_that_delivered]

    def __repr__(self):
        graph_string = ""
        for key, value in self.graph_state.items():
            graph_string += key + ": " + str(value) + "\n"
        return graph_string

    def __eq__(self, other):
        return (
                self.graph_state['P'] == other.graph_state['P']
                and self.graph_state['B'] == other.graph_state['B']
                and self.graph_state['F'] == other.graph_state['F']
                and self.graph_state['Agents'] == other.graph_state['Agents']
        )
