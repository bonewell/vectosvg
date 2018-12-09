from .command import Command
from adapter import Point


class LineCommand(Command):
    def execute(self):
        points = []
        for i in range(len(self.params)):
            if i % 2 == 0:
                x = self.params[i]
            else:
                y = self.params[i]
                points.append(Point(x, y))
        w = 1 if (len(self.params) % 2) == 0 else self.params[-1]
        self.adapter.polyline(points, w)
