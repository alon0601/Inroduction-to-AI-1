from agent import agent
from search import bfs


class interfering_agent(agent):
    def __init__(self, x, y):
        super().__init__(x, y)

    def act(self, init_graph):
        #  check if agent is already next to a fragile edge, then traverse it.
        for fe in init_graph.graph_state['F']:
            if (self.X, self.Y) in fe.points:
                for point in fe.points:
                    if point != (self.X, self.Y):
                        self.move_request = point
                        return

        #  find the closest point that's on a fragile edge
        step = bfs((self.X, self.Y), 'F', init_graph)

        if step:
            self.move_request = step
        else:
            self.move_request = (self.X, self.Y)
