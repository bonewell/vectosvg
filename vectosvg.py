#!/usr/bin/env python
import zipfile

from converter import Converter
from vecinterpreter import VecInterpreter
from svgadapter import SvgAdapter

"""This script converts vec files of pMap to SVG"""
archive = 'Peterburg.pmz'
files = ['Avtovo.vec']

iszip = zipfile.is_zipfile(archive)

print "File is corect: %s" % iszip

def main():
	if iszip:
		zf = zipfile.ZipFile(archive, 'r')
#		files = [ f for f in zf.namelist() if isvec(f) ]
		zf.extractall('.', files)
		process(files)

def convert(fi, fo):
	fo.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n')
	fo.write('<g stroke="black" >\n')
	size=[]
	for line in fi:
		tokens = line.strip().split(' ')
		
		if tokens[0] == 'Size':
			size = tokens[1].split('x')
			size = [ int(x)/2 for x in size ]
			print size
		if tokens[0] == 'Line':
			point1 = tokens[1].split(',')
			point1[0] = int(point1[0]) + size[0]
			point1[1] = int(point1[1]) + size[1]
			point2 = tokens[2].split(',')
			point2[0] = int(point2[0]) + size[0]
			point2[1] = int(point2[1]) + size[1]
			string = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="2" />\n' % (point1[0], point1[1], point2[0], point2[1])
			fo.write(string)
	fo.write('</g>\n')
	fo.write('</svg>\n')

def process(files):
	for fname in files:
		fi = open(fname, 'r')
		fo = open(name(fname), 'w')
		svg = SvgAdapter(fo)
		vec = VecInterpreter()
		for line in fi:
			cmd = vec.interpret(line)
			cmd.write(svg)
		fo.close()
		fi.close()

def isvec(f):
	(name, ext) = f.split('.')
	return ext == 'vec'

def name(f):
	(name, ext) = f.split('.')
	return name+'.svg'

def convert(inp, out):
	con = Converter()
	vec = VecInterpreter(inp)
	svg = SvgAdapter(out)
	con.convert(vec, svg)

convert('Avtovo.vec', 'Avtovo.svg')
