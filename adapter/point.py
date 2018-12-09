class Point(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def coordinate(self) -> (float, float):
        return self.x, self.y
