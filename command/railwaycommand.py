import math
from .command import Command
from .mathhelper import translate, is_crossed


class RailwayCommand(Command):
    def execute(self):
        self.adapter.pencolor('000000')
        w1 = self.params[0]
        w2 = self.params[1]
        t = self.params[2]
        params = self.params[3:]

        points = []
        for i in range(len(params)):
            if i % 2 == 0:
                x = params[i]
            else:
                y = params[i]
                points.append((x, y))

        p1 = points[0]
        for p2 in points[1:]:
            self.part(w1, w2, t, p1, p2)
            p1 = p2

    def part(self, w1, w2, t, p1, p2):
        (x1, y1) = p1
        (x2, y2) = p2

        (ry, rx) = translate(int(x1), int(y1), int(x2), int(y2), int(w1))

        xb1 = int(x1)
        yb1 = int(y1)
        xe1 = int(x2)
        ye1 = int(y2)
        self.adapter.line(xb1, yb1, xe1, ye1)

        xb2 = int(x1) - rx
        yb2 = int(y1) + ry
        xe2 = int(x2) - rx
        ye2 = int(y2) + ry
        self.adapter.line(xb2, yb2, xe2, ye2)

        (sy, sx) = translate(xb1, yb1, xe1, ye1, math.fabs(int(w2) - int(w1)) / 2)
        sx1 = int(xb1) + sx
        sy1 = int(yb1) - sy
        (ssy, ssx) = translate(xb1, yb1, xe1, ye1, int(w1) + math.fabs(int(w2) - int(w1)) / 2)
        sx2 = int(xb1) - ssx
        sy2 = int(yb1) + ssy
        sx3 = int(xe1) + sx
        sy3 = int(ye1) - sy

        (tx, ty) = translate(sx1, sy1, sx3, sy3, int(t))
        (txp, typ) = translate(sx1, sy1, sx3, sy3, int(t) / 2)
        xb = sx1 + txp
        yb = sy1 + typ
        xe = sx2 + txp
        ye = sy2 + typ
        while not is_crossed(xb, tx, sx3) and not is_crossed(yb, ty, sy3):
            self.adapter.line(xb, yb, xe, ye)
            xb += tx
            yb += ty
            xe += tx
            ye += ty
