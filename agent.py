class agent():
    def __init__(self, x, y, act, type):
        self.X = x
        self.Y = y
        self.Act = act
        self.Type = type
        self.Score = 0

    def __repr__(self):
        return "x :" + str(self.X) + ", y :" + str(self.Y)  + ", type :" + str(self.Type) + ", score :" + str(self.Score)+ "\n"