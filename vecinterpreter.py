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
		if name == 'Size' or name == 'size':
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
		elif name == 'AngleTextOut':
			return AngleTextOutCommand(params)
#		elif name == 'Railway':
#			return RailwayCommand(params)
		else:
			print 'Unknown command: %s' % name
			return None

class VecIterator(IteratorInterface):
	def __init__(self, container):
		self.container = container

	def next(self):
		line = self.container.line()
		if not line:
			return None # end file

		print line

		tokens = line.strip().split(' ')
		if not tokens:
			return self.next()

		name = tokens[0].strip()
		if not name or name[0] == ';':
			return self.next()

		params = tokens[1:]
		cmd = self.container.command(name, params)
		if cmd == None:
			return self.next()
		else:
			return cmd
