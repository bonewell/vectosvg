#!/usr/bin/env python

class AdapterInterface:
	def size(self, w, h):
		pass

	def pencolor(self, color):
		pass

	def brushcolor(self, color):
		pass

	def line(self, x1, y1, x2, y2):
		pass

	def polyline(self, points):
		pass

	def polygon(self, points):
		pass

	def ellipse(self, x1, y1, x2, y2):
		pass

	def spline(self, points):
		pass

	def arrow(self, x1, y1, x2, y2):
		pass

	def rect(self, x1, y1, x2, y2):
		pass
