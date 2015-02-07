#!/usr/bin/env python

import cgi
import math
from adapter import AdapterInterface

class SvgAdapter(AdapterInterface):
	def __init__(self, filename):
		self.f = open(filename, 'w')
		self.sc = 0
		self.ac = 0
		self.stroke = '000000'
		self.fill = 'none'
		self.opacity = 1.0
		self.newgroup = False
		self.head()
		self.defs()
		self.startgroup()

	def __del__(self):
		for x in range(0, self.ac):
			self.endgroup()
		if self.sc:
			self.endgroup()
		self.endgroup()
		self.tail()
		self.f.close()

	def write(self, data):
		self.f.write('%s\n' % data)

	def head(self):
		data = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">'
		self.write(data)

	def defs(self):
		data = """<defs>
    <marker id="arrow"
      viewBox="0 0 10 10" refX="0" refY="5"
      markerUnits="strokeWidth"
      markerWidth="4" markerHeight="3"
      orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" />
    </marker>
  </defs>"""
		self.write(data)

	def tail(self):
		data = '</svg>'
		self.write(data)

	def startgroup(self):
		data = '<g stroke="#%s" fill="%s" fill-opacity="%s">' % (self.stroke, self.fill, self.opacity)
		self.write(data)

	def endgroup(self):
		data = '</g>'
		self.write(data)

	def group(self):
		if self.newgroup == True:
			self.endgroup()
			self.startgroup()
			self.newgroup = False

	def size(self, w, h):
		self.sc += 1
		self.cx = int(w)/2
		self.cy = int(h)/2
		self.rect(0, 0, w, h)
		self.startgroup()

	def rotate(self, a):
		self.ac += 1
		self.a = float(a) * -1
		self.endgroup()
		templ = '<g transform="rotate(%s %s %s)" >'
		data = templ % (self.a, self.cx, self.cy)
		self.write(data)
		self.startgroup()

	def pencolor(self, color):
		self.stroke = color
		self.newgroup = True

	def brushcolor(self, color):
		if color == '-1':
			self.fill = 'none'
		else:
			self.fill = '#%s' % color
		self.newgroup = True

	def opaque(self, v):
		self.opacity = float(v) / 100
		self.newgroup = True

	def line(self, x1, y1, x2, y2):
		self.group()
		templ = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="1" />'
		data = templ % (x1, y1, x2, y2)
		self.write(data)

	def polyline(self, points, dashed=False):
		self.group()
		polyline = []
		for p in points:
			polyline.append('%s,%s' % p[:2])
		text = ' '.join(polyline)
		dasharray = ''
		if dashed:
			dasharray = 'stroke-dasharray="5,2"'
		templ = '<polyline points="%s" stroke-width="1" fill="none" %s />'
		data = templ % (text, dasharray)
		self.write(data)

	def polygon(self, points):
		self.group()
		polygon = []
		for p in points:
			polygon.append('%s,%s' % p[:2])
		text = ' '.join(polygon)
		templ = '<polygon points="%s" stroke-width="1" />'
		data = templ % text
		self.write(data)

	def ellipse(self, x1, y1, x2, y2):
		self.group()
		rx = (int(x2) - int(x1)) / 2
		ry = (int(y2) - int(y1)) / 2
		cx = int(x1) + rx
		cy = int(y1) + ry
		templ = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" />'
		data = templ % (cx, cy, math.fabs(rx), math.fabs(ry))
		self.write(data)

	def spline(self, points):
		self.group()
		polyline = []
		for p in points:
			polyline.append('%s,%s' % p[:2])
		text = ' '.join(polyline)
		templ = '<path d="%s" stroke-width="1" />'
		templ = '<polyline points="%s" stroke-width="1" fill="none"/> <!-- spline -->'
		data = templ % text
		self.write(data)

	def arrow(self, points):
		self.group()
		polyline = []
		for p in points:
			polyline.append('%s,%s' % p[:2])
		text = ' '.join(polyline)
		templ = '<polyline points="%s" marker-end="url(#arrow)" stroke-width="1" fill="none" />'
		data = templ % text
		self.write(data)

	def rect(self, x1, y1, x2, y2):
		self.group()
		w = int(x2) - int(x1)
		h = int(y2) - int(y1)
		templ = '<rect x="%s" y="%s" width="%s" height="%s" stroke-width="0" fill="none" />'
		data = templ % (x1, y1, w, h)
		self.write(data)

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
