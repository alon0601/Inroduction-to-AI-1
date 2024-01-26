from package_graph import package_graph
from edge import edge


def move_agents():
    #  move all agents according to their move requests while checking for collisions
    #  turn fragile to broken
    blocked_edges = init_graph.graph_state['B']
    fragile_edges = init_graph.graph_state['F']
    does_move_succeeded = False
    for age, age_value in init_graph.graph_state['Agents'].items():
        other_agents = {key: value for key, value in init_graph.graph_state['Agents'].items() if key != age}
        others_locations = list(map(lambda ag: (ag.X, ag.Y), other_agents.values()))
        other_moves = list(map(lambda ag: ag.move_request, other_agents.values()))
        edge_to_move = edge(age_value.X, age_value.Y, age_value.move_request[0], age_value.move_request[1])
        if age_value.move_request not in others_locations or age_value.move_request not in other_moves:
            if not does_move_in_block_list(edge_to_move, blocked_edges):
                does_move_succeeded = True
        elif age_value.move_request in others_locations:
            agents_to_move = filter(lambda ag: (ag.X, ag.Y) == age_value.move_request, other_agents.values())
            for agent_to_move in agents_to_move:
                if agent_to_move.move_request != () and not does_move_in_block_list(edge_to_move, blocked_edges):
                    does_move_succeeded = True
        if does_move_succeeded:
            age_value.X = age_value.move_request[0]
            age_value.Y = age_value.move_request[1]
            age_value.move_request = ()
            if does_move_in_fragile_list(edge_to_move, fragile_edges):
                fragile_edges.remove(edge_to_move)
                blocked_edges.append(edge_to_move)
        pick_up_package()


def pick_up_package():
    packages = init_graph.graph_state['P']
    packages_that_delivered = set()
    for age, age_value in init_graph.graph_state['Agents'].items():
        for package in packages:
            if not package.picked and age_value.X == package.p_x and age_value.Y == package.p_y and init_graph.graph_state['T'] >= package.p_time:
                package.picked = True
                age_value.packages.append(package)
            elif package.picked and package in age_value.packages and age_value.X == package.d_x and age_value.Y == package.d_y and init_graph.graph_state['T'] <= package.d_time:
                packages_that_delivered.add(package)

    init_graph.graph_state['P'] = [package for package in packages if package not in packages_that_delivered]


def does_move_in_block_list(move, block_list):
    return move in block_list


def does_move_in_fragile_list(move, fragile_list):
    return move in fragile_list


if __name__ == '__main__':
    goal_state = "4,3,2,1"
    pancake_input = "4,2,3,1"
    init_graph = package_graph("test")
    time = 0
    while True:
        for agent in init_graph.graph_state['Agents'].values():
            agent.act(init_graph)
        move_agents()
        init_graph.graph_state['T'] += 1
        print(init_graph)
