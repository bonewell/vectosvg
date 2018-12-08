#!/usr/bin/env python3


class Converter:
	def convert(self, inp, out):
		it = inp.interpret()
		cmd = it.next()
		while cmd:
			cmd.setAdapter(out)
			cmd.execute()
			cmd = it.next()
