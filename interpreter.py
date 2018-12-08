#!/usr/bin/env python3


class InterpreterInterface:
	def interpret(self):
		raise NotImplementedError()


class IteratorInterface:
	def next(self):
		raise NotImplementedError()
