from package_graph import package_graph


def move_agents():
    #  move all agents according to their move requests while checking for collisions
    #  turn fragile to broken
    for age, age_value in init_graph.graph_state['Agents'].items():
        other_agents = {key: value for key, value in init_graph.graph_state['Agents'].items() if key != age}
        others_locations = list(map(lambda ag: (ag.X, ag.Y), other_agents.values()))
        other_moves = list(map(lambda ag: ag.move_request, other_agents.values()))
        if age_value.move_request not in others_locations or age_value.move_request not in other_moves:
            age_value.X = age_value.move_request[0]
            age_value.Y = age_value.move_request[1]
            age_value.move_request = ()
        elif age_value.move_request in others_locations:
            agents_to_move = filter(lambda ag: (ag.X, ag.Y) == age_value.move_request, other_agents)
            for agent_to_move in agents_to_move:
                if agent_to_move.move_request != ():
                    age_value.X = age_value.move_request[0]
                    age_value.Y = age_value.move_request[1]
                    age_value.move_request = ()


if __name__ == '__main__':
    goal_state = "4,3,2,1"
    pancake_input = "4,2,3,1"
    init_graph = package_graph("test")
    time = 0
    while True:
        for agent in init_graph.graph_state['Agents'].values():
            agent.act(init_graph)
        move_agents()
        #  pick up packages
        #  deliver packages
        init_graph.graph_state['T'] += 1
        print(init_graph)
