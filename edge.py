class edge():
    def __init__(self, f_x, f_y, t_x, t_y):
        self.points = {(f_x, f_y), (t_x, t_y)}

    def __eq__(self, other):
        return other.points == self.points

    def __repr__(self):
        return str(self.points)
