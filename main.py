from package_graph import package_graph
from package import package
from edge import edge
import re


def parse_file(init_file_path):
    init_graph = package_graph()
    packages = list()
    blocked_edges = list()
    fragile_edges = list()
    init_file = open(init_file_path, mode='r', encoding='utf-8-sig')
    init_file_lines = init_file.readlines()
    for line in init_file_lines:
        all_numbers_in_line = re.findall(r'-?\b\d+\b', line)
        if line[1] == 'X':
            init_graph.graph_state['X'] = int(all_numbers_in_line[0])
        elif line[1] == 'Y':
            init_graph.graph_state['Y'] = int(all_numbers_in_line[0])
        elif line[1] == 'P':
            packages.append(package(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), int(all_numbers_in_line[2]),
                                    int(all_numbers_in_line[3]), int(all_numbers_in_line[4]), int(all_numbers_in_line[5])))
        elif line[1] == 'B':
            blocked_edges.append(edge(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), int(all_numbers_in_line[2]),
                                    int(all_numbers_in_line[3])))
        elif line[1] == 'F':
            fragile_edges.append(edge(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), int(all_numbers_in_line[2]),
                                    int(all_numbers_in_line[3])))
        else:
            init_graph.graph_state[line[1]] = (int(all_numbers_in_line[0]), int(all_numbers_in_line[1]))

    init_graph.graph_state['P'] = packages
    init_graph.graph_state['B'] = blocked_edges

    return init_graph


if __name__ == '__main__':
    goal_state = "4,3,2,1"
    pancake_input = "4,2,3,1"
    start_state = parse_file("test")
    print(start_state)