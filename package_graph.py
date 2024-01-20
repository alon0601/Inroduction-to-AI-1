class package_graph():
    def __init__(self):
        self.graph_state = {}

    def __repr__(self):
        stringTostring = ""
        for key, value in self.graph_state.items():
            stringTostring += key + ": " + str(value) + "\n"
        return stringTostring