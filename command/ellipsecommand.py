from .command import Command
from adapter import Point, Ellipse


class EllipseCommand(Command):
    def execute(self):
        (x1, y1, x2, y2) = self.params[:4]
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        rx = (p2.x - p1.x) / 2
        ry = (p2.y - p1.y) / 2
        center = Point(p1.x + rx, p1.y + ry)
        self.adapter.ellipse(center, Ellipse(rx, ry))
