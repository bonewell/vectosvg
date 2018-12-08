from .command import Command


class EllipseCommand(Command):
    def execute(self):
        (x1, y1, x2, y2) = self.params[:4]
        self.adapter.ellipse(x1, y1, x2, y2)
