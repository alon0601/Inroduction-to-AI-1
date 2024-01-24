from collections import deque

from package_graph import package_graph
from package import package
from edge import edge
from agent import agent
import re

init_graph = package_graph()


def bfs(start, destination, deliveries=None):
    gathered_points = set()
    queue = deque([(start, [])])

    while queue:
        point, path = queue.popleft()
        if destination == 'P':
            for p in init_graph.graph_state['P']:
                if p.point == point:
                    if time >= p.p_time:
                        return path[0] if path else path
                    else:
                        break  # unless there can be two packs on the same point?
        elif destination == 'D':
            for d in deliveries:
                if d.delivery == point:
                    if time <= d.d_time:
                        return path[0] if path else path
                    else:
                        break  # unless there can be two deliveries to the same point?
        elif destination == 'F':
            for fe in init_graph.graph_state['F']:
                if point in fe.values:
                    return path[0] if path else path

        if point in gathered_points:
            continue
        gathered_points.add(point)
        x, y = point
        neighbors = [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]

        for neighbor in neighbors:
            nx, ny = neighbor
            if (0 <= nx <= init_graph.graph_state['X'] and 0 <= ny <= init_graph.graph_state['Y'] and
                    edge(nx, ny, x, y) not in init_graph.graph_state['B'] and neighbor not in gathered_points):
                queue.append(((nx, ny), path + [neighbor]))

    return []


def parse_file(init_file_path):
    packages = list()
    blocked_edges = list()
    fragile_edges = list()
    agents = {}
    init_file = open(init_file_path, mode='r', encoding='utf-8-sig')
    init_file_lines = init_file.readlines()
    for line in init_file_lines:
        all_numbers_in_line = re.findall(r'-?\b\d+\b', line)
        if line[1] == 'X':
            init_graph.graph_state['X'] = int(all_numbers_in_line[0])
        elif line[1] == 'Y':
            init_graph.graph_state['Y'] = int(all_numbers_in_line[0])
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
            agents[line[1]] = agent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), normal_agent, line[1])
        elif line[1] == 'H':
            agents[line[1]] = agent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), normal_agent, line[1])
        elif line[1] == 'I':
            agents[line[1]] = agent(int(all_numbers_in_line[0]), int(all_numbers_in_line[1]), normal_agent, line[1])

    init_graph.graph_state['P'] = packages
    init_graph.graph_state['B'] = blocked_edges
    init_graph.graph_state['F'] = fragile_edges
    init_graph.graph_state['Agents'] = agents

    return init_graph


def move_agents():
    #  move all agents according to their move requests while checking for collisions
    #  turn fragile to broken
    return


if __name__ == '__main__':
    goal_state = "4,3,2,1"
    pancake_input = "4,2,3,1"
    start_state = parse_file("test")
    time = 0
    while True:
        for agent in init_graph.graph_state['Agents']:
            agent.act()
        move_agents()
        #  pick up packages
        #  deliver packages
        time += 1
        print(start_state)
