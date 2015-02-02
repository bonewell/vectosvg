#!/usr/bin/env python

from adapter import AdapterInterface

class SvgAdapter(AdapterInterface):
	def __init__(self, filename):
		self.f = open(filename, 'w')
		self.head()

	def __del__(self):
		self.tail()
		self.f.close()

	def write(self, data):
		self.f.write('%s\n' % data)

	def head(self):
		data = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">'
		self.write(data)
		data = '<g stroke="black" >'
		self.write(data)

	def tail(self):
		data = '</g>'
		self.write(data)
		data = '</svg>'
		self.write(data)

	def size(self, h, w):
		self.dh = int(h)/2
		self.dw = int(w)/2

	def line(self, x1, y1, x2, y2):
		templ = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="2" />'
		data = templ % (int(x1) + self.dw, int(y1) + self.dh, int(x2) + self.dw, int(y2) + self.dh)
		self.write(data)

	def polygon(self, points):
		pass
