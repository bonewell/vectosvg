#!/usr/bin/env python3

import math
import svgwrite
import colorutils
from adapter import Adapter
from adapter import Point


def diff(p1, p2):
    x1, y1 = p1.coordinate()
    x2, y2 = p2.coordinate()
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt((dx * dx) + (dy * dy))


def translate(p1, p2, t):
    x1, y1 = p1.coordinate()
    x2, y2 = p2.coordinate()
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        z = -1 if dy < 0 else 1
        tx = 0
        ty = t * z
    elif dy == 0:
        z = -1 if dx < 0 else 1
        tx = t * z
        ty = 0
    else:
        a = math.atan2(dx, dy)
        tx = t * math.sin(a)
        ty = t * math.cos(a)
    return tx, ty


class SvgAdapter(Adapter):
    def __init__(self, filename):
        self.image = svgwrite.Drawing(filename, profile='full')
        self.stroke = self.color('000000')
        self.fill = self.color('')
        self.opacity = 1.0
        self.alpha = 0.0
        self.defs()
        self.root = self.image.add(self.image.g())
        # self.root.scale(0.5) # for website
        self.current = self.root

    def __del__(self):
        self.image.save(pretty=True)

    def defs(self):
        self.marker = self.image.marker((0, 5), (4, 3), 'auto', markerUnits="strokeWidth")
        self.marker.viewbox(0, 0, 10, 10)
        self.marker.add(self.image.path("M 0 0 L 10 5 L 0 10 z"))
        self.image.defs.add(self.marker)

    def size(self, w, h):
        self.cx = int(w) / 2
        self.cy = int(h) / 2
        self.rect(Point(0, 0), Point(w, h))

    def rotate(self, a):
        self.alpha += float(a) * -1
        self.current = self.root.add(self.image.g())
        if self.alpha != 0:
            self.current.rotate(self.alpha, (self.cx, self.cy))

    def color(self, color):
        try:
            return colorutils.Color(hex=color).hex
        except ValueError:
            return 'none'

    def pencolor(self, color):
        self.stroke = self.color(color)

    def brushcolor(self, color):
        self.fill = self.color(color)

    def opaque(self, v):
        self.opacity = float(v) / 100
        self.current = self.root.add(self.image.g())
        self.current.fill(self.fill, opacity=self.opacity).stroke(self.stroke, opacity=self.opacity)
        self.current.rotate(self.alpha, (self.cx, self.cy))

    def line(self, p1, p2):
        line = self.current.add(self.image.line(p1.coordinate(),
                                                p2.coordinate()))
        line.stroke(self.stroke, width=1)

    def polyline(self, points, w, dashed=False):
        ps = [p.coordinate() for p in points]
        polyline = self.current.add(self.image.polyline(ps))
        polyline.fill('none').stroke(self.stroke, width=w)
        if dashed:
            polyline.dasharray([5, 2])

    def polygon(self, points):
        ps = [p.coordinate() for p in points]
        polygon = self.current.add(self.image.polygon(ps))
        polygon.fill(self.fill).stroke(self.stroke, width=1)

    def ellipse(self, p1, p2):
        x1, y1 = p1.coordinate()
        x2, y2 = p2.coordinate()
        rx = (x2 - x1) / 2
        ry = (y2 - y1) / 2
        cx = x1 + rx
        cy = y1 + ry
        ellipse = self.current.add(self.image.ellipse((cx, cy), (math.fabs(rx), math.fabs(ry))))
        ellipse.fill(self.fill).stroke(self.stroke, width=1)

    def spline(self, points, w):
        b = points[0]
        cpb = b
        d = 'M%s,%s ' % b.coordinate()
        for i in range(len(points[1:])):
            e = points[i]
            n = points[i + 1]

            delta = diff(b, n)
            (tx, ty) = translate(b, n, delta / 6)
            (ex, ey) = e.coordinate()
            cpex = (ex - tx)
            cpey = (ey - ty)

            d += 'C%s,%s %s,%s %s,%s ' % (cpb.coordinate() + (cpex, cpey, ex, ey))

            b = e
            (bx, by) = b.coordinate()
            cpb = Point((bx + tx), (by + ty))
        e = points[-1]
        cpe = e
        d += 'C%s,%s %s,%s %s,%s ' % (cpb.coordinate() + cpe.coordinate() + e.coordinate())

        spline = self.current.add(self.image.path(d))
        spline.fill('none').stroke(self.stroke, width=w)

    def arrow(self, points):
        ps = [p.coordinate() for p in points]
        polyline = self.current.add(self.image.polyline(ps))
        polyline.fill('none').stroke(self.stroke, width=1)
        polyline['marker-end'] = self.marker.get_funciri()

    def rect(self, p1, p2):
        x1, y1 = p1.coordinate()
        x2, y2 = p2.coordinate()
        w = x2 - x1
        h = y2 - y1
        rect = self.current.add(self.image.rect(p1.coordinate(), (w, h)))
        rect.fill(self.fill).stroke('none', width=0)

    def text(self, p, text, size, font, a):
        x, y = p.coordinate()
        insert = (x, y + float(size))
        txt = self.current.add(self.image.text(text, insert))
        txt.fill(self.stroke).stroke('none', width=0)
        txt['font-family'] = font
        txt['font-size'] = size
        if a:
            txt.rotate(a * -1, (x, y))
