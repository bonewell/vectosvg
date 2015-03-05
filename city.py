#!/usr/bin/env python
import os
import zipfile

class City:
	def __init__(self, dirpath, filename=None):
		self.stations = []
		if (filename):
			self.source = os.path.join(dirpath, filename)
			(self.name, extension) = os.path.splitext(filename)
		else:
			self.source = dirpath
			(path, extension) = os.path.splitext(self.source)
			self.name = os.path.split(path)[1]

	@staticmethod
	def is_valid(source):
		(name, extension) = os.path.splitext(source)
		if extension == '.pmz':
			return zipfile.is_zipfile(source)
		else:
			return False

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
