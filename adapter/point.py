class Point(object):
    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)

    def coordinate(self) -> (float, float):
        return self._x, self._y
