from .command import Command
from adapter import Point


class EllipseCommand(Command):
    def execute(self):
        (x1, y1, x2, y2) = self.params[:4]
        self.adapter.ellipse(Point(x1, y1), Point(x2, y2))
