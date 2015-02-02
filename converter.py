#!/usr/bin/env python

from interpreter import InterpreterInterface
from adapter import AdapterInterface

class Converter:
	def convert(self, inp, out):
		it = inp.interpret()
		cmd = it.next()
		while cmd != None:
			cmd.setAdapter(out)
			cmd.execute()
			cmd = it.next()
