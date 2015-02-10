#!/usr/bin/env python
import os
import argparse
import tempfile
import shutil
import zipfile

from converter import Converter
from vecinterpreter import VecInterpreter
from svgadapter import SvgAdapter

"""This script converts vec files of pMetro to SVG"""

def cities():
	names = []
	for dirpath, dirnames, filenames in os.walk(source):
		for fname in filenames:
			(name, ext) = os.path.splitext(fname)
			if ext == '.pmz':
				names.append(name)
	return names

def main():
	if os.path.isdir(source):
		for name in cities():
			archive = '%s/%s.pmz' % (source, name)
			run(archive, name)
	else:
		(path, ext) = os.path.splitext(source)
		if ext == '.pmz':
			name = os.path.split(path)[1]
			run(source, name)
		else:
			print 'File "%s" is not pMetro format' % source

def run(archive, name):
		iszip = zipfile.is_zipfile(archive)

		if iszip:
			zf = zipfile.ZipFile(archive, 'r')
			files = [ f for f in zf.namelist() if isvec(f) ]
			city = '%s/%s' % (tmp, name)
			os.mkdir(city)
			zf.extractall(city, files)
			process(name, files)
		else:
			print 'File \'%s\' is not corect' % archive

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

def process(city, files):
	path = '%s/%s' % (dest, city)
	shutil.rmtree(path, True)
	os.mkdir(path)

	print 'City: %s' % city
	for fname in files:
		inp = '%s/%s/%s' % (tmp, city, fname)
		out = '%s/%s/%s' % (dest, city, name(fname))
		print 'Schema: %s' % fname.split('.')[0]
		convert(inp, out)
	print

def isvec(f):
	(name, ext) = f.split('.')
	return ext == 'vec'

def name(f):
	(name, ext) = f.split('.')
	return '%s.svg' % name

def convert(inp, out):
	con = Converter()
	vec = VecInterpreter(inp)
	svg = SvgAdapter(out)
	con.convert(vec, svg)

parser = argparse.ArgumentParser(prog='vectosvg', description='Converter subway stations schemes from pMetro format into SVG images')
parser.add_argument('source', help='Input directory which contains *.pmz files or path to specific *.pmz file')
parser.add_argument('dest', help='Output directory where will be saved SVG images')
values = parser.parse_args()

source = values.source
dest = values.dest
tmp = tempfile.mkdtemp()

main()

shutil.rmtree(tmp)
