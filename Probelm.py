from package_graph import package_graph

class Problem(object):
    def __init__(self, path, goalstate, graph):
        self.Initial_State = package_graph(path)

        self.Initial_State.g = 0
        self.Goal_State = goalstate
