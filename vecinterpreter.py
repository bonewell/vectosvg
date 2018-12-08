#!/usr/bin/env python3

from interpreter import InterpreterInterface
from interpreter import IteratorInterface
from command import *


class VecInterpreter(InterpreterInterface):
	def __init__(self, filename):
		self.f = open(filename, 'r', encoding="windows-1251")

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
		elif name == 'Opaque':
			return OpaqueCommand(params)
		elif name == 'Line':
			return LineCommand(params)
		elif name == 'Dashed':
			return DashedCommand(params)
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
		elif name == 'TextOut':
			return TextOutCommand(params)
		elif name == 'Railway':
			return RailwayCommand(params)
		elif name == 'SpotRect':
			return SpotRectCommand(params)
		elif name == 'SpotCircle':
			return SpotCircleCommand(params)
		else:
			print('Unknown command: %s' % name)
			return None


class VecIterator(IteratorInterface):
	def __init__(self, container):
		self.container = container

	def next(self):
		line = self.container.line()
		if not line:
			return None  # end file

		# print line

		tokens = line.strip().strip(',').split(' ')
		if not tokens:
			return self.next()

		name = tokens[0].strip()
		if not name or name[0] == ';':
			return self.next()

		tail = tokens[1:]
		if not tail or len(tail) == 0:
			return self.next()

		raw_params = ' '.join(tokens[1:]).split(',')
		params = []
		for p in raw_params:
			params.append(p.strip())
		# print 'Name: %s - %s' % (name, params)
		cmd = self.container.command(name, params)
		return cmd if cmd else self.next()
