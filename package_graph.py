class package_graph():
    def __init__(self):
        self.graph_state = {}

    def __repr__(self):
        graph_string = ""
        for key, value in self.graph_state.items():
            graph_string += key + ": " + str(value) + "\n"
        return graph_string
