#!/usr/bin/env python3
from abc import ABC, abstractmethod


class AdapterInterface(ABC):
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
    def line(self, x1, y1, x2, y2):
        pass

    @abstractmethod
    def polyline(self, points, w, dashed=False):
        pass

    @abstractmethod
    def polygon(self, points):
        pass

    @abstractmethod
    def ellipse(self, x1, y1, x2, y2):
        pass

    @abstractmethod
    def spline(self, points, w):
        pass

    @abstractmethod
    def arrow(self, points):
        pass

    @abstractmethod
    def rect(self, x1, y1, x2, y2):
        pass

    @abstractmethod
    def text(self, x, y, text, size, font, a):
        pass
