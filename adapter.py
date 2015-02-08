#!/usr/bin/env python

class AdapterInterface:
	def size(self, w, h):
		pass

	def rotate(self, a):
		pass

	def pencolor(self, color):
		pass

	def brushcolor(self, color):
		pass

	def opaque(self, v):
		pass

	def line(self, x1, y1, x2, y2):
		pass

	def polyline(self, points, w, dashed=False):
		pass

	def polygon(self, points):
		pass

	def ellipse(self, x1, y1, x2, y2):
		pass

	def spline(self, points, w):
		pass

	def arrow(self, points):
		pass

	def rect(self, x1, y1, x2, y2):
		pass

	def text(self, x, y, text, size, font, a):
		pass
