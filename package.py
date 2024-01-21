class package():
    def __init__(self, p_x, p_y, p_time, d_x, d_y, d_time):
        self.p_x = p_x
        self.p_y = p_y
        self.p_time = p_time
        self.d_x = d_x
        self.d_y = d_y
        self.d_time = d_time

    def __repr__(self):
        return ("p_x :" + str(self.p_x) + ", p_y :" + str(self.p_y) + ", p_time :"
                + str(self.p_time) + ", d_x :" + str(self.d_x) + ", d_y :" + str(self.p_y) + ", d_time :" + str(self.d_time) + "\n")