class Ellipse:
    def __init__(self, rx, ry):
        self.rx = float(rx)
        self.ry = float(ry)

    def size(self) -> (float, float):
        return self.rx, self.ry
