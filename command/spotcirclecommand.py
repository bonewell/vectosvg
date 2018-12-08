from .command import Command


class SpotCircleCommand(Command):
    def execute(self):
        (r, xc, yc) = self.params[:3]
        x1, y1 = int(xc) - int(r), int(yc) - int(r)
        x2, y2 = int(xc) + int(r), int(yc) + int(r)
        self.adapter.ellipse(x1, y1, x2, y2)
