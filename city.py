#!/usr/bin/env python
import os
import zipfile

class Invalid:
	pass

class City:
	def __init__(self, source):
		(path, ext) = os.path.splitext(source)
		if ext != '.pmz' or not zipfile.is_zipfile(source):
			raise Invalid()
		self.stations = []
		self.source = source
		self.name = os.path.split(path)[1]

	def unzip(self, tmp):
		zf = zipfile.ZipFile(self.source, 'r')
		files = [ f for f in zf.namelist() if self.is_vec(f) ]
		directory = os.path.join(tmp, self.name)
		os.mkdir(directory)
		zf.extractall(directory, files)

	def is_vec(self, filename):
		(name, ext) = os.path.splitext(filename)
		if ext == '.vec':
			self.stations.append(name)
			return True
		else:
			return False
