from .point import Point


class Rectangle:
    def __init__(self, w, h):
        self.w = float(w)
        self.h = float(h)

    def size(self) -> (float, float):
        return self.w, self.h

    def center(self) -> Point:
        return Point(self.w / 2, self.h / 2)
