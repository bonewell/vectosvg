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
