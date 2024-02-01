class edge():
    def __init__(self, f_x, f_y, t_x, t_y, w=1):
        self.points = {(f_x, f_y), (t_x, t_y)}
        self.weight = w

    def __eq__(self, other):
        return other.points == self.points

    def __repr__(self):
        return str(self.points) + " Weight:" + str(self.weight)
