#!/usr/bin/env python3

import math
import svgwrite
import colorutils
from adapter import Adapter
from adapter import Point
from adapter import Rectangle


def diff(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return math.sqrt((dx * dx) + (dy * dy))


def translate(p1, p2, t):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
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
        self.marker = None
        self.defs()
        self.root = self.image.add(self.image.g())
        self.current = self.root
        self.center = Point(0, 0)

    def __del__(self):
        self.image.save(pretty=True)

    def defs(self):
        self.marker = self.image.marker((0, 5), (4, 3), 'auto', markerUnits="strokeWidth")
        self.marker.viewbox(0, 0, 10, 10)
        self.marker.add(self.image.path("M 0 0 L 10 5 L 0 10 z"))
        self.image.defs.add(self.marker)

    def size(self, w, h):
        rectangle = Rectangle(w, h)
        self.image.attribs['width'] = rectangle.w
        self.image.attribs['height'] = rectangle.h
        self.center = rectangle.center()
        self.rect(Point(0, 0), rectangle)

    def rotate(self, a):
        self.alpha += float(a) * -1
        self.current = self.root.add(self.image.g())
        if self.alpha != 0:
            self.current.rotate(self.alpha, self.center.coordinate())

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
        self.current.rotate(self.alpha, self.center.coordinate())

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

    def ellipse(self, center, ellipse):
        ellipse = self.current.add(self.image.ellipse(center.coordinate(),
                                                      ellipse.size()))
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

    def rect(self, point, rectangle):
        rect = self.current.add(self.image.rect(point.coordinate(),
                                                rectangle.size()))
        rect.fill(self.fill).stroke('none', width=0)

    def text(self, point, text, angle):
        insert = (point.x, point.y + text.font.size)
        txt = self.current.add(self.image.text(text.string, insert))
        txt.fill(self.stroke).stroke('none', width=0)
        txt['font-family'] = text.font.name
        txt['font-size'] = text.font.size
        if angle:
            txt.rotate(angle * -1, (point.x, point.y))
