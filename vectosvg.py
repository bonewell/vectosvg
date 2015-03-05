#!/usr/bin/env python
import os
import argparse
import tempfile
import shutil

from city import City
from converter import Converter
from vecinterpreter import VecInterpreter
from svgadapter import SvgAdapter

"""This script converts vec files of pMetro to SVG"""

def cities(source):
	cities = []
	if os.path.isdir(source):
		for dirpath, dirnames, filenames in os.walk(source):
			for name in filenames:
				if City.is_valid(os.path.join(dirpath, name)):
					cities.append(City(dirpath, name))
				else:
					print 'File "%s/%s" is not pMetro format' % (dirpath, name)
	else:
		if City.is_valid(source):
			cities.append(City(source))
		else:
			print 'File "%s" is not pMetro format' % source
	return cities

def main(source, dest):
	tmp = tempfile.mkdtemp()
	for city in cities(source):
		process(city, tmp, dest)
	shutil.rmtree(tmp)

def process(city, tmp, dest):
	print 'City: %s' % city.name
	city.unzip(tmp)
	path = os.path.join(dest, city.name)
	shutil.rmtree(path, True)
	os.mkdir(path)

	for station in city.stations:
		print 'Station: %s' % station
		inp = os.path.join(tmp, '%s/%s.vec' % (city.name, station))
		out = os.path.join(dest, '%s/%s.svg' % (city.name, station))
		convert(inp, out)

def convert(inp, out):
	con = Converter()
	vec = VecInterpreter(inp)
	svg = SvgAdapter(out)
	con.convert(vec, svg)

parser = argparse.ArgumentParser(prog='vectosvg', description='Converter subway stations schemes from pMetro format into SVG images')
parser.add_argument('source', help='Input directory which contains *.pmz files or path to specific *.pmz file')
parser.add_argument('dest', help='Output directory where will be saved SVG images')
values = parser.parse_args()

main(values.source, values.dest)
