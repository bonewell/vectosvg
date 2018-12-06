#!/usr/bin/env python

import math

from adapter import AdapterInterface

def translate(x1, y1, x2, y2, t):
	dx = x2 - x1
	dy = y2 - y1
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

def iscrossed(x, t, g):
	if t > 0:
		return x > g
	else:
		return x < g

class Command:
	def __init__(self, params):
		self.params = params

	def setAdapter(self, adapter):
		self.adapter = adapter

	def execute(self):
		raise NotImplementedError()

class SizeCommand(Command):
	def execute(self):
		(w, h) = self.params[0].split('x')
		self.adapter.size(w, h)

class AngleCommand(Command):
	def execute(self):
		a = self.params[0]
		self.adapter.rotate(a)

class PenColorCommand(Command):
	def execute(self):
		if self.params:
			color = self.params[0]
			self.adapter.pencolor(color)

class BrushColorCommand(Command):
	def execute(self):
		if self.params:
			color = self.params[0]
			self.adapter.brushcolor(color)

class OpaqueCommand(Command):
	def execute(self):
		self.adapter.opaque(self.params[0])
		self.adapter.pencolor('000000')

class LineCommand(Command):
	def execute(self):
		points = []
		for i in range(len(self.params)):
			if i % 2 == 0:
				x = self.params[i]
			else:
				y = self.params[i]
				points.append((x, y))
		w = 1 if (len(self.params) % 2) == 0 else self.params[-1]
		self.adapter.polyline(points, w)

class DashedCommand(Command):
	def execute(self):
		points = []
		for i in range(len(self.params)):
			if i % 2 == 0:
				x = self.params[i]
			else:
				y = self.params[i]
				points.append((x, y))
		w = 1 if (len(self.params) % 2) == 0 else self.params[-1]
		self.adapter.polyline(points, w, True)

class PolygonCommand(Command):
	def execute(self):
		points = []
		for i in range(len(self.params)):
			if i % 2 == 0:
				x = self.params[i]
			else:
				y = self.params[i]
				points.append((x, y))
		self.adapter.polygon(points)

class EllipseCommand(Command):
	def execute(self):
		(x1, y1, x2, y2) = self.params[:4]
		self.adapter.ellipse(x1, y1, x2, y2)

class SplineCommand(Command):
	def execute(self):
		points = []
		for i in range(len(self.params)):
			if i % 2 == 0:
				x = self.params[i]
			else:
				y = self.params[i]
				points.append((x, y))
		w = 1 if (len(self.params) % 2) == 0 else self.params[-1]
		self.adapter.spline(points, w)

class ArrowCommand(Command):
	def execute(self):
		points = []
		for i in range(len(self.params)):
			if i % 2 == 0:
				x = self.params[i]
			else:
				y = self.params[i]
				points.append((x, y))
		self.adapter.arrow(points)

class StairsCommand(Command):
	def execute(self):
		(x1, y1, x2, y2, x3, y3) = self.params[:6]
		t = 4
		(tx, ty) = translate(int(x1), int(y1), int(x3), int(y3), t)
		xb = int(x1)
		yb = int(y1)
		xe = int(x2)
		ye = int(y2)
		while not iscrossed(xb, tx, int(x3)) and not iscrossed(yb, ty, int(y3)):
			self.adapter.line(xb, yb, xe, ye)
			xb += tx
			yb += ty
			xe += tx
			ye += ty

class AngleTextOutCommand(Command):
	def execute(self):
		a = self.params[0]
		font = self.params[1].strip()
		size = self.params[2]
		(x, y) = self.params[3:5]
		if len(self.params) > 5:
			text = self.params[5].strip()
		else:
			text = ''
		text = text.replace(r'\n', ' ')
		text = text.decode('windows-1251').encode('UTF-8')
		self.adapter.text(x, y, text, size, font, float(a))

class TextOutCommand(Command):
	def execute(self):
		font = self.params[0].strip()
		size = self.params[1]
		(x, y) = self.params[2:4]
		text = self.params[4].strip()
		text = text.replace(r'\n', ' ')
		text = text.decode('windows-1251').encode('UTF-8')
		self.adapter.text(x, y, text, size, font, 0)

class RailwayCommand(Command):
	def execute(self):
		self.adapter.pencolor('000000')
		w1 = self.params[0]
		w2 = self.params[1]
		t = self.params[2]
		params = self.params[3:]

		points = []
		for i in range(len(params)):
			if i % 2 == 0:
				x = params[i]
			else:
				y = params[i]
				points.append((x, y))

		p1 = points[0]
		for p2 in points[1:]:
			self.part(w1, w2, t, p1, p2)
			p1 = p2

	def part(self, w1, w2, t, p1, p2):
		(x1, y1) = p1
		(x2, y2) = p2

		(ry, rx) = translate(int(x1), int(y1), int(x2), int(y2), int(w1))

		xb1 = int(x1)
		yb1 = int(y1)
		xe1 = int(x2)
		ye1 = int(y2)
		self.adapter.line(xb1, yb1, xe1, ye1)

		xb2 = int(x1) - rx
		yb2 = int(y1) + ry
		xe2 = int(x2) - rx
		ye2 = int(y2) + ry
		self.adapter.line(xb2, yb2, xe2, ye2)

		(sy, sx) = translate(xb1, yb1, xe1, ye1, math.fabs(int(w2) - int(w1)) / 2)
		sx1 = int(xb1) + sx
		sy1 = int(yb1) - sy
		(ssy, ssx) = translate(xb1, yb1, xe1, ye1, int(w1) + math.fabs(int(w2) - int(w1)) / 2)
		sx2 = int(xb1) - ssx
		sy2 = int(yb1) + ssy
		sx3 = int(xe1) + sx
		sy3 = int(ye1) - sy

		(tx, ty) = translate(sx1, sy1, sx3, sy3, int(t))
		(txp, typ) = translate(sx1, sy1, sx3, sy3, int(t) / 2)
		xb = sx1 + txp
		yb = sy1 + typ
		xe = sx2 + txp
		ye = sy2 + typ
		while not iscrossed(xb, tx, sx3) and not iscrossed(yb, ty, sy3):
			self.adapter.line(xb, yb, xe, ye)
			xb += tx
			yb += ty
			xe += tx
			ye += ty
