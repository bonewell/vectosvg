#!/usr/bin/env python

from interpreter import InterpreterInterface
from interpreter import IteratorInterface
from command import *

class VecInterpreter(InterpreterInterface):
	def __init__(self, filename):
		self.f = open(filename, 'r')

	def __del__(self):
		self.f.close()

	def interpret(self):
		return VecIterator(self)

	def line(self):
		return self.f.readline()

	def command(self, name, params):
		if name == 'Size':
			return SizeCommand(params)
		elif name == 'Angle':
			return AngleCommand(params)
		elif name == 'PenColor':
			return PenColorCommand(params)
		elif name == 'BrushColor':
			return BrushColorCommand(params)
		elif name == 'Line':
			return LineCommand(params)
		elif name == 'Polygon':
			return PolygonCommand(params)
		elif name == 'Ellipse':
			return EllipseCommand(params)
		elif name == 'Spline':
			return SplineCommand(params)
		elif name == 'Arrow':
			return ArrowCommand(params)
		elif name == 'Stairs':
			return StairsCommand(params)
		else:
			return None

class VecIterator(IteratorInterface):
	def __init__(self, container):
		self.container = container

	def next(self):
		line = self.container.line()
		if not line:
			return None
		tokens = line.strip().split(' ')
		name = tokens[0]
		params = tokens[1:]
		cmd = self.container.command(name, params)
		if cmd == None:
			return self.next()
		else:
			return cmd
