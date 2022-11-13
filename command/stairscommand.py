from .command import Command
from .mathhelper import translate, is_crossed
from adapter import Point


class StairsCommand(Command):
    def execute(self):
        (x1, y1, x2, y2, x3, y3) = self.params[:6]
        t = 4
        (tx, ty) = translate(int(x1), int(y1), int(x3), int(y3), t)
        xb = int(x1)
        yb = int(y1)
        xe = int(x2)
        ye = int(y2)
        while not is_crossed(xb, tx, int(x3)) and not is_crossed(yb, ty, int(y3)):
            self.adapter.line(Point(xb, yb), Point(xe, ye))
            xb += tx
            yb += ty
            xe += tx
            ye += ty
