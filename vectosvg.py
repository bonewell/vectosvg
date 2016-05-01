#!/usr/bin/env python
import os
import argparse
import tempfile
import shutil

from city import City, Invalid
from converter import Converter
from vecinterpreter import VecInterpreter
from svgadapter import SvgAdapter

"""Converts vec files of pMetro to SVG"""
class Vectosvg:
	def __init__(self, source):
		self.source = source

	def cities(self):
		files = [ self.source ]
		if os.path.isdir(self.source):
			files = [ os.path.join(self.source, f) for f in os.listdir(self.source) ]
		cities = []
		for f in files:
			try:
				cities.append(City(f))
			except Invalid:
				print 'File "%s" is not pMetro format' % f
		return cities

	def save(self, dest):
		self.dest = dest
		self.tmp = tempfile.mkdtemp()
		for city in self.cities():
			self.process(city)
		shutil.rmtree(self.tmp)

	def process(self, city):
		print 'City: %s' % city.name
		city.unzip(self.tmp)
		path = os.path.join(self.dest, city.name)
		shutil.rmtree(path, True)
		os.mkdir(path)
		for station in city.stations:
			print 'Station: %s' % station
			inp = os.path.join(self.tmp, '%s/%s.vec' % (city.name, station))
			out = os.path.join(self.dest, '%s/%s.svg' % (city.name, station))
			self.convert(inp, out)

	def convert(self, inp, out):
		vec = VecInterpreter(inp)
		svg = SvgAdapter(out)
		Converter().convert(vec, svg)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='vectosvg', description='Converter subway stations schemes from pMetro format into SVG images')
	parser.add_argument('source', help='Input directory which contains *.pmz files or path to specific *.pmz file')
	parser.add_argument('dest', help='Output directory where will be saved SVG images')
	values = parser.parse_args()

	Vectosvg(values.source).save(values.dest)
