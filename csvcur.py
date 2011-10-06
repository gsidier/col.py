from curs import cursor, select, All

import csv
import numpy

class csvcur(cursor):
	
	def __init__(self, path):
		self.path = path
		f = file(path, 'r')
		r = csv.reader(f, lineterminator = '\n')
		header = r.next()
		row = [ eval(x) for x in r.next() ]
		self.columns = dict([
			(name, numpy.array([val]).dtype)
			for (name, val) in zip(header, row)
		])
		self.file = file(self.path, 'r')
		self.reader = csv.reader(self.file, lineterminator = '\n')
		self.reader.next() # skip header
	
	def fetch(self, n = None, cols = All):
		if n is None:
			n = 10
		
