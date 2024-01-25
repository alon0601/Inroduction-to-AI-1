from agent import agent
from search import bfs


class greedy_agent(agent):
    def __init__(self, x, y):
        super().__init__(x, y)

    def act(self, init_graph):
        print(init_graph)
        #  check if agent has packages, and accordingly deliver or look for a package
        if self.packages:
            step = bfs((self.X, self.Y), 'D', init_graph, self.packages)
        else:
            step = bfs((self.X, self.Y), 'P', init_graph)

        if step:
            self.move_request = step
        else:
            self.move_request = (self.X, self.Y)
