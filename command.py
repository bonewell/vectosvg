#!/usr/bin/env python

from adapter import AdapterInterface

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
		self.adapter.rect(x1, y1, x2, y3)