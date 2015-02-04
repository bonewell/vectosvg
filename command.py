#!/usr/bin/env python

import math

from adapter import AdapterInterface

# Helpers function. Need to remove Command interface into other file
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
		tga = dx / dy
		a = math.atan(tga)
		tx = t * math.sin(a) * -1 # Oy is top to bottom
		ty = t * math.cos(a) * -1 # Oy is top to bottom
	return (tx, ty)

def isborder(x, y, tx, ty, xg, yg):
	return True
	#if tx < 0:
	#	return x >= gx
	#	
	#else:
	#		
	#else:
	#	xg = x1


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
		self.adapter.pencolor(self.params[0])

class BrushColorCommand(Command):
	def execute(self):
		self.adapter.brushcolor(self.params[0])

class LineCommand(Command):
	def execute(self):
		points = []
		for p in self.params:
			if p.find(',') != -1: # end value can be no point
				(x, y) = p.strip(',').split(',')
			points.append((x, y))
		self.adapter.polyline(points)

class PolygonCommand(Command):
	def execute(self):
		points = []
		for p in self.params:
			(x, y) = p.strip(',').split(',')
			points.append((x, y))
		self.adapter.polygon(points)

class EllipseCommand(Command):
	def execute(self):
		(x1, y1) = self.params[0].strip(',').split(',')
		(x2, y2) = self.params[1].strip(',').split(',')
		self.adapter.ellipse(x1, y1, x2, y2)

class SplineCommand(Command):
	def execute(self):
		points = []
		for p in self.params:
			(x, y) = p.strip(',').split(',')
			points.append((x, y))
		self.adapter.spline(points)

class ArrowCommand(Command):
	def execute(self):
		(x1, y1) = self.params[0].strip(',').split(',')
		(x2, y2) = self.params[1].strip(',').split(',')
		self.adapter.arrow(x1, y1, x2, y2)

class StairsCommand(Command):
	def execute(self):
		(x1, y1) = self.params[0].strip(',').split(',')
		(x2, y2) = self.params[1].strip(',').split(',')
		(x3, y3) = self.params[2].strip(',').split(',')
		t = 4
		(tx, ty) = translate(int(x1), int(y1), int(x3), int(y3), t)
		xb = int(x1)
		yb = int(y1)
		xe = int(x2)
		ye = int(y2)
		while not isborder(xb, yb, tx, ty, int(x3), int(y3)):
			self.adapter.line(xb, yb, xe, ye)
			xb += tx
			yb += ty
			xe += tx
			ye += ty
