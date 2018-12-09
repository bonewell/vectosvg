from .command import Command
from adapter import Point, Ellipse


class SpotCircleCommand(Command):
    def execute(self):
        r, x, y = self.params[:3]
        self.adapter.ellipse(Point(x, y), Ellipse(r, r))
