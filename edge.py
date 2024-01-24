class edge():
    def __init__(self, f_x, f_y, t_x, t_y):
        # self.f_X = f_x
        # self.f_Y = f_y
        # self.t_X = t_x
        # self.t_Y = t_y

        self.points = {(f_x, f_y), (t_x, t_y)}

    def __eq__(self, other):
        return self.points == other.values

    def __repr__(self):
        return str(self.points)
        # return str("f_x :" + str(self.f_X) + ", f_y :" + str(self.f_Y) + ", t_x :" + str(self.t_X) + ", t_y :" + str(self.t_Y) + "\n")