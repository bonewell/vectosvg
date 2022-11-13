from .command import Command
from adapter import Point, Rectangle


class SpotRectCommand(Command):
    def execute(self):
        (x, y, w, h) = self.params[:4]
        self.adapter.rect(Point(x, y), Rectangle(w, h))
