class package():
    def __init__(self, p_x, p_y, p_time, d_x, d_y, d_time):
        self.p_x = p_x
        self.p_y = p_y
        self.point = (p_x, p_y)
        self.p_time = p_time
        self.d_x = d_x
        self.d_y = d_y
        self.delivery = (d_x, d_y)
        self.d_time = d_time
        self.picked = False

    def __hash__(self):
        # Hash based on a unique representation of the object
        return hash((self.p_x, self.p_y, self.p_time, self.d_x, self.d_y, self.picked))


    def __eq__(self, other):
        return (
                self.p_x == other.p_x
                and self.p_y == other.p_y
                and self.p_time == other.p_time
                and self.d_x == other.d_x
                and self.d_y == other.d_y  # Fixed this line
                and self.picked == other.picked
        )


    def __repr__(self):
        return ("p_x :" + str(self.p_x) + ", p_y :" + str(self.p_y) + ", p_time :"
                + str(self.p_time) + ", d_x :" + str(self.d_x) + ", d_y :" + str(self.d_y) + ", d_time :" + str(self.d_time) + "\n")