from agent import agent


class human_agent(agent):
    def __init__(self, x, y):
        super().__init__(x, y)

    def act(self, init_graph):
        next_move = input("Please Enter your next move: ")
        if next_move == 'R':
            if init_graph.graph_state["Agents"]['A'].X + 1 > init_graph.graph_state['X']:
                return
            self.move_request = (self.X+1, self.Y)
        if next_move == 'L':
            if init_graph.graph_state["Agents"]['A'].X - 1 < 0:
                return
            self.move_request = (self.X-1, self.Y)
        if next_move == 'U':
            if init_graph.graph_state["Agents"]['A'].Y + 1 > init_graph.graph_state['Y']:
                return
            self.move_request = (self.X, self.Y+1)
        if next_move == 'D':
            if init_graph.graph_state["Agents"]['A'].Y - 1 < 0:
                return
            self.move_request = (self.X, self.Y-1)
