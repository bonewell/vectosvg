from abc import ABC, abstractmethod


class Adapter(ABC):
    @abstractmethod
    def size(self, w, h):
        pass

    @abstractmethod
    def rotate(self, a):
        pass

    @abstractmethod
    def pencolor(self, color):
        pass

    @abstractmethod
    def brushcolor(self, color):
        pass

    @abstractmethod
    def opaque(self, v):
        pass

    @abstractmethod
    def line(self, p1, p2):
        pass

    @abstractmethod
    def polyline(self, points, w, dashed=False):
        pass

    @abstractmethod
    def polygon(self, points):
        pass

    @abstractmethod
    def ellipse(self, center, ellipse):
        pass

    @abstractmethod
    def spline(self, points, w):
        pass

    @abstractmethod
    def arrow(self, points):
        pass

    @abstractmethod
    def rect(self, point, rectangle):
        pass

    @abstractmethod
    def text(self, point, text, angle):
        pass
