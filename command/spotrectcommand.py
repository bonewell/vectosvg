from .command import Command


class SpotRectCommand(Command):
    def execute(self):
        (x1, y1, w, h) = self.params[:4]
        x2 = int(x1) + int(w)
        y2 = int(y1) + int(h)
        self.adapter.rect(x1, y1, x2, y2)
