#!/usr/bin/env python

import math
import svgwrite
from adapter import AdapterInterface

def diff((x1, y1), (x2, y2)):
	dx = int(x2) - int(x1)
	dy = int(y2) - int(y1)
	return math.sqrt((dx * dx) + (dy * dy))

def translate((x1, y1), (x2, y2), t):
	dx = int(x2) - int(x1)
	dy = int(y2) - int(y1)
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
	return (tx, ty)

class SvgAdapter(AdapterInterface):
	def __init__(self, filename):
		self.image = svgwrite.Drawing(filename, profile='full')
		self.stroke = self.color('000000')
		self.fill = self.color('-1')
		self.opacity = 1.0
		self.defs()
		self.root = self.image.add(self.image.g())
		self.current = self.root

	def __del__(self):
		self.image.save()

	def defs(self):
		self.marker = self.image.marker((0, 5), (4, 3), 'auto', markerUnits = "strokeWidth")
		self.marker.viewbox(0, 0, 10, 10)
		self.marker.add(self.image.path("M 0 0 L 10 5 L 0 10 z"))
		self.image.defs.add(self.marker)

	def size(self, w, h):
		self.cx = int(w)/2
		self.cy = int(h)/2
		self.rect(0, 0, w, h)

	def rotate(self, a):
		alfa = float(a) * -1
		self.root.rotate(alfa, (self.cx, self.cy))

	def color(self, color):
		return 'none' if color == '-1' else '#%s' % color

	def pencolor(self, color):
		self.stroke = self.color(color)

	def brushcolor(self, color):
		self.fill = self.color(color)

	def opaque(self, v):
		self.opacity = float(v) / 100
		self.current = self.root.add(self.image.g())
		self.current.fill(self.fill, opacity=self.opacity).stroke(self.stroke, opacity=self.opacity)

	def line(self, x1, y1, x2, y2):
		line = self.current.add(self.image.line((x1, y1), (x2, y2)))
		line.stroke(self.stroke, width=1)

	def polyline(self, points, w, dashed=False):
		polyline = self.current.add(self.image.polyline(points))
		polyline.fill('none').stroke(self.stroke, width=w)
		if dashed:
			polyline.dasharray([5, 2])

	def polygon(self, points):
		polygon = self.current.add(self.image.polygon(points))
		polygon.fill(self.fill).stroke(self.stroke, width=1)

	def ellipse(self, x1, y1, x2, y2):
		rx = (int(x2) - int(x1)) / 2
		ry = (int(y2) - int(y1)) / 2
		cx = int(x1) + rx
		cy = int(y1) + ry
		ellipse = self.current.add(self.image.ellipse((cx, cy), (math.fabs(rx), math.fabs(ry))))
		ellipse.fill(self.fill).stroke(self.stroke, width=1)

	def spline(self, points, w):
		b = points[0]
		cpb = b
		d = 'M%s,%s ' % b
		for i in range(len(points[1:])):
			e = points[i]
			n = points[i+1]

			delta = diff(b, n)
			(tx, ty) = translate(b, n, delta/6)
			(ex, ey) = e
			cpex = (int(ex) - tx)
			cpey = (int(ey) - ty)

			d += 'C%s,%s %s,%s %s,%s ' % (cpb[0], cpb[1], cpex, cpey, ex, ey)

			b = e
			(bx, by) = b
			cpb = ((int(bx) + tx), (int(by) + ty))
		e = points[-1]
		cpe = e
		d += 'C%s,%s %s,%s %s,%s ' % (cpb[0], cpb[1], cpe[0], cpe[1], e[0], e[1])

		spline = self.current.add(self.image.path(d))
		spline.fill('none').stroke(self.stroke, width=w)

	def arrow(self, points):
		polyline = self.current.add(self.image.polyline(points))
		polyline.fill('none').stroke(self.stroke, width=1)
		polyline['marker-end'] = self.marker.get_funciri()

	def rect(self, x1, y1, x2, y2):
		w = int(x2) - int(x1)
		h = int(y2) - int(y1)
		rect = self.current.add(self.image.rect((x1, y1), (w, h)))
		rect.fill('none').stroke('none', width=0)

	def text(self, x, y, text, size, font, a):
		insert = (x, float(y) + float(size))
		txt = self.current.add(self.image.text(text, insert))
		txt.fill(self.stroke).stroke('none', width=0)
		txt['font-family'] = font
		txt['font-size'] = size
		if a:
			txt.rotate(a * -1, (x, y))
