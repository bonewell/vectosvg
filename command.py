#!/usr/bin/env python

import math

from adapter import AdapterInterface

def translate(x1, y1, x2, y2, t):
	dx = x2 - x1
	dy = y2 - y1
	if dx == 0:
		tx = 0
		ty = t * (dy / dy) * -1 # Oy is top to bottom
	elif dy == 0:
		tx = t * (dx / dx)
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
		pass

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
			self.adapter.pencolor(self.params[0])

class BrushColorCommand(Command):
	def execute(self):
		self.adapter.brushcolor(self.params[0])

class LineCommand(Command):
	def execute(self):
		points = []
		for i in range(len(self.params)):
			if i % 2 == 0:
				x = self.params[i]
			else:
				y = self.params[i]
				points.append((x, y))
		self.adapter.polyline(points)

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
		self.adapter.spline(points)

class ArrowCommand(Command):
	def execute(self):
		(x1, y1, x2, y2) = self.params[:4]
		self.adapter.arrow(x1, y1, x2, y2)

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
		text = self.params[5].strip()
		text = text.decode('windows-1251').encode('UTF-8')
		self.adapter.text(x, y, text, size, font, float(a))

class TextOutCommand(Command):
	def execute(self):
		font = self.params[0].strip()
		size = self.params[1]
		(x, y) = self.params[2:4]
		text = self.params[4].strip()
		text = text.decode('windows-1251').encode('UTF-8')
		self.adapter.text(x, y, text, size, font, 0)

class RailwayCommand(Command):
	def execute(self):
		(x1, y1, x2, y2) = self.params[:4]
		if len(self.params) > 4:
			(x1, y1, x2, y2, x3, y3) = self.params[:6]
		else:
			x3 = 0
			y3 = 0
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


