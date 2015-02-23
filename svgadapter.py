#!/usr/bin/env python

import cgi
import math
import svgwrite
from adapter import AdapterInterface

class SvgAdapter(AdapterInterface):
	def __init__(self, filename):
		self.image = svgwrite.Drawing(filename, profile='full')
		self.sc = 0
		self.ac = 0
		self.stroke = self.color('000000')
		self.fill = self.color('-1')
		self.opacity = 1.0
#		self.defs()

	def __del__(self):
		self.image.save()

	def write(self, data):
		pass
		#self.f.write('%s\n' % data)

	def defs(self):
		pass
		#self.arrow = self.image.marker((0, 5), (4, 3))
		#self.arrow.add(self.image.circle((0, 0), r=5))
		#self.image.defs.add(self.arrow)
#<defs>
#    <marker id="arrow"
#      viewBox="0 0 10 10" refX="0" refY="5"
#      markerUnits="strokeWidth"
#      markerWidth="4" markerHeight="3"
#      orient="auto">
#      <path d="M 0 0 L 10 5 L 0 10 z" />
#    </marker>
#</defs>

	def group(self):
		return self.image.add(self.image.g())

	def size(self, w, h):
		self.sc += 1
		self.cx = int(w)/2
		self.cy = int(h)/2
		self.rect(0, 0, w, h)

	def rotate(self, a):
		self.ac += 1
		self.a = float(a) * -1
		templ = '<g transform="rotate(%s %s %s)" >'
		data = templ % (self.a, self.cx, self.cy)
		self.write(data)

	def color(self, color):
		return 'none' if color == '-1' else '#%s' % color

	def pencolor(self, color):
		self.stroke = self.color(color)

	def brushcolor(self, color):
		self.fill = self.color(color)

	def opaque(self, v):
		self.opacity = float(v) / 100
		self.newgroup = True

	def line(self, x1, y1, x2, y2):
		line = self.image.add(self.image.line((x1, y1), (x2, y2)))
		line.stroke(self.stroke, width=1)

	def polyline(self, points, w, dashed=False):
		polyline = self.image.add(self.image.polyline(points))
		polyline.fill('none').stroke(self.stroke, width=w)
		if dashed:
			polyline.dasharray([5, 2])

	def polygon(self, points):
		polygon = self.image.add(self.image.polygon(points))
		polygon.fill(self.fill).stroke(self.stroke, width=1)

	def ellipse(self, x1, y1, x2, y2):
		rx = (int(x2) - int(x1)) / 2
		ry = (int(y2) - int(y1)) / 2
		cx = int(x1) + rx
		cy = int(y1) + ry

		ellipse = self.image.add(self.image.ellipse((cx, cy), (math.fabs(rx), math.fabs(ry))))
		ellipse.fill(self.fill).stroke(self.stroke, width=1)

	def spline(self, points, w):
		polyline = self.image.add(self.image.polyline(points))
		polyline.fill('none').stroke(self.stroke, width=w)

	def arrow(self, points):
		polyline = self.image.add(self.image.polyline(points))
		polyline.fill('none').stroke(self.stroke, width=1)
#		polyline.set_markers(self.arrow)

	def rect(self, x1, y1, x2, y2):
		w = int(x2) - int(x1)
		h = int(y2) - int(y1)
		rect = self.image.add(self.image.rect((x1, y1), (w, h)))
		rect.fill('none').stroke('none', width=0)

	def text(self, x, y, text, size, font, a):
		self.group()
		if not a:
			templ = '<text x="%s" y="%s" font-family="%s" font-size="%s" fill="#%s" stroke-width="0">%s</text>'
			data = templ % (x, float(y) + float(size), font, size, self.stroke, cgi.escape(text))
		else:
			a *= -1
			templ = '<text x="%s" y="%s" font-family="%s" font-size="%s" fill="#%s" transform="rotate(%s %s %s)" stroke-width="0">%s</text>'
			data = templ % (x, float(y) + float(size), font, size, self.stroke, a, x, y, cgi.escape(text))
		self.write(data)
