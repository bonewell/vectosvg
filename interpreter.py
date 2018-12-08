#!/usr/bin/env python


class InterpreterInterface:
	def interpret(self):
		raise NotImplementedError()


class IteratorInterface:
	def next(self):
		raise NotImplementedError()
