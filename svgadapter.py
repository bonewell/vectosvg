#!/usr/bin/env python

from adapter import AdapterInterface

class SvgAdapter(AdapterInterface):
	def __init__(self, filename):
		self.f = open(filename, 'w')
		self.stroke = '000000'
		self.fill = 'FFFFFF'
		self.newgroup = True
		self.head()
		self.startgroup()

	def __del__(self):
		self.endgroup()
		self.tail()
		self.f.close()

	def write(self, data):
		self.f.write('%s\n' % data)

	def head(self):
		data = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">'
		self.write(data)

	def tail(self):
		data = '</svg>'
		self.write(data)

	def startgroup(self):
		data = '<g stroke="#%s" fill="#%s" >' % (self.stroke, self.fill)
		self.write(data)

	def endgroup(self):
		data = '</g>'
		self.write(data)

	def group(self):
		if self.newgroup == True:
			self.endgroup()
			self.startgroup()
			self.newgroup = False

	def size(self, h, w):
		self.dh = int(h)/2
		self.dw = int(w)/2

	def pencolor(self, color):
		self.stroke = color
		self.newgroup = True

	def brushcolor(self, color):
		if color == '-1':
			color = 'FFFFFF'
		self.fill = color
		self.newgroup = True

	def line(self, x1, y1, x2, y2):
		self.group()
		templ = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="2" />'
		data = templ % (int(x1) + self.dw, int(y1) + self.dh, int(x2) + self.dw, int(y2) + self.dh)
		self.write(data)

	def polyline(self, points):
		self.group()
		polyline = []
		for p in points:
			x = '%s' % (int(p[0]) + self.dw)
			y = '%s' % (int(p[1]) + self.dh)
			polyline.append(','.join([x, y]))
		text = ' '.join(polyline)
		templ = '<polyline points="%s" stroke-width="2" />'
		data = templ % text
		self.write(data)

	def polygon(self, points):
		self.group()
		polygon = []
		for p in points:
			x = '%s' % (int(p[0]) + self.dw)
			y = '%s' % (int(p[1]) + self.dh)
			polygon.append(','.join([x, y]))
		text = ' '.join(polygon)
		templ = '<polygon points="%s" stroke-width="2" />'
		data = templ % text
		self.write(data)

	def ellipse(self, cx, cy, rx, ry):
		self.group()
		templ = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" />'
		cx = int(cx) + self.dw
		cy = int(cy) + self.dh
		data = templ % (cx, cy, rx, ry)
		self.write(data)
