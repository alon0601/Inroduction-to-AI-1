class agent():
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.Score = 0
        self.packages = list()
        self.move_request = None

    def act(self, init_graph):
        return

    def __repr__(self):
        return "x :" + str(self.X) + ", y :" + str(self.Y) + ", type :" + str(self.Type) + ", score :" + str(self.Score)+ "\n"