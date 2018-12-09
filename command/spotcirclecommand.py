from .command import Command
from adapter import Point


class SpotCircleCommand(Command):
    def execute(self):
        (r, xc, yc) = self.params[:3]
        x1, y1 = int(xc) - int(r), int(yc) - int(r)
        x2, y2 = int(xc) + int(r), int(yc) + int(r)
        self.adapter.ellipse(Point(x1, y1), Point(x2, y2))
