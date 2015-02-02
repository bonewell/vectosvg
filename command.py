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
		(h, w) = self.params[0].split('x')
		self.adapter.size(h, w)

class LineCommand(Command):
	def execute(self):
		point1 = self.params[0].split(',')
		(x1, y1) = point1[0:2]
		point2 = self.params[1].split(',')
		(x2, y2) = point2[0:2]
		self.adapter.line(x1, y1, x2, y2)
