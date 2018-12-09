from .command import Command
from adapter import Point


class SpotRectCommand(Command):
    def execute(self):
        (x1, y1, w, h) = self.params[:4]
        x2 = int(x1) + int(w)
        y2 = int(y1) + int(h)
        self.adapter.rect(Point(x1, y1), Point(x2, y2))
