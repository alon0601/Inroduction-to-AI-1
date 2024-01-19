from package_graph import package_graph
from package import package
from edge import edge


def parse_file(init_file_path):
    init_graph = package_graph()
    packages = list()
    blocked_edges = list()
    fragile_edges = list()
    init_file = open(init_file_path, mode='r', encoding='utf-8-sig')
    init_file_lines = init_file.readlines()
    for line in init_file_lines:
        line.replace(" ","")
        if line[1] == 'X':
            init_graph.graph_state['X'] = ord(line[2])
        elif line[1] == 'Y':
            init_graph.graph_state['Y'] = ord(line[2])
        elif line[1] == 'P':
            packages.append(package(ord(line[2]), ord(line[3]), ord(line[4]), ord(line[6]),ord(line[7]), ord(line[8])))
        elif line[1] == 'B':
            blocked_edges.append(edge(ord(line[2]), ord(line[3]), ord(line[4]),ord(line[5])))
        elif line[1] == 'F':
            fragile_edges.append(edge(ord(line[2]), ord(line[3]), ord(line[4]), ord(line[5])))
        else:
            init_graph.graph_state[line[1]] = (ord(line[2]),ord(line[3]))

    init_graph.graph_state['P'] = packages
    init_graph.graph_state['B'] = blocked_edges

    return init_graph


if __name__ == '__main__':
    goal_state = "4,3,2,1"
    pancake_input = "4,2,3,1"
    start_state = parse_file("test")
