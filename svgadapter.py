#!/usr/bin/env python

import cgi
from adapter import AdapterInterface

class SvgAdapter(AdapterInterface):
	def __init__(self, filename):
		self.f = open(filename, 'w')
		self.stroke = '000000'
		self.fill = 'none'
		self.newgroup = False
		self.head()
		self.defs()

	def __del__(self):
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
		data = '<g stroke="#%s" fill="%s" >' % (self.stroke, self.fill)
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
		self.cx = int(w)/2
		self.cy = int(h)/2

	def rotate(self, a):
		self.a = int(a) * -1
		self.root()
		self.startgroup()

	def root(self):
		templ = '<g transform="rotate(%s %s %s)" >'
		data = templ % (self.a, self.cx, self.cy)
		self.write(data)

	def pencolor(self, color):
		self.stroke = color
		self.newgroup = True

	def brushcolor(self, color):
		if color == '-1':
			self.fill = 'none'
		else:
			self.fill = '#%s' % color
		self.newgroup = True

	def line(self, x1, y1, x2, y2):
		self.group()
		templ = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="1" />'
		data = templ % (x1, y1, x2, y2)
		self.write(data)

	def polyline(self, points):
		self.group()
		polyline = []
		for p in points:
			polyline.append('%s,%s' % p[:2])
		text = ' '.join(polyline)
		templ = '<polyline points="%s" stroke-width="1" fill="white" />'
		data = templ % text
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
		data = templ % (cx, cy, rx, ry)
		self.write(data)

	def spline(self, points):
		self.group()
		polyline = []
		for p in points:
			polyline.append('%s,%s' % p[:2])
		text = ' '.join(polyline)
		templ = '<path d="%s" stroke-width="1" />'
		templ = '<polyline points="%s" stroke-width="1" /> <!-- spline -->'
		data = templ % text
		self.write(data)

	def arrow(self, x1, y1, x2, y2):
		self.group()
		templ = '<line x1="%s" y1="%s" x2="%s" y2="%s" marker-end="url(#arrow)" stroke-width="1" />'
		data = templ % (x1, y1, x2, y2)
		self.write(data)

	def rect(self, x1, y1, x2, y2):
		self.group()
		w = int(x2) - int(x1)
		h = int(y2) - int(y1)
		templ = '<rect x="%s" y="%s" width="%s" height="%s" stroke-width="1" />'
		data = templ % (x1, y1, w, h)
		self.write(data)

	def text(self, x, y, text, size, font):
		self.group()
		templ = '<text x="%s" y="%s" font-family="%s" font-size="%s" fill="#%s" stroke-width="0">%s</text>'
		data = templ % (x, int(y) + int(size), font, size, self.stroke, cgi.escape(text))
		self.write(data)
