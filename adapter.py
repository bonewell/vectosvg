#!/usr/bin/env python3


class AdapterInterface:
	def size(self, w, h):
		raise NotImplementedError()

	def rotate(self, a):
		raise NotImplementedError()

	def pencolor(self, color):
		raise NotImplementedError()

	def brushcolor(self, color):
		raise NotImplementedError()

	def opaque(self, v):
		raise NotImplementedError()

	def line(self, x1, y1, x2, y2):
		raise NotImplementedError()

	def polyline(self, points, w, dashed=False):
		raise NotImplementedError()

	def polygon(self, points):
		raise NotImplementedError()

	def ellipse(self, x1, y1, x2, y2):
		raise NotImplementedError()

	def spline(self, points, w):
		raise NotImplementedError()

	def arrow(self, points):
		raise NotImplementedError()

	def rect(self, x1, y1, x2, y2):
		raise NotImplementedError()

	def text(self, x, y, text, size, font, a):
		raise NotImplementedError()
