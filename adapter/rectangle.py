class Rectangle:
    def __init__(self, w, h):
        self.w = float(w)
        self.h = float(h)

    def size(self) -> (float, float):
        return self.w, self.h
