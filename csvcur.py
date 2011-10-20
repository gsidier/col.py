from curs import cursor, select, All

import csv
import numpy

def _take(i, n):
	for _ in xrange(n):
		yield i.next()

class CsvCur(cursor):
	
	def __init__(self, f, colnames, coltypes):
		self.file = f
		self.reader = csv.reader(f, lineterminator = '\n')
		self.colnames = [ c for c in colnames ]
		self.coltypes = [ numpy.dtype(t) for t in coltypes ]
		self.columns = dict(zip(self.colnames, self.coltypes))
		self.col_index = dict( (c,i) for (i,c) in enumerate(self.colnames) )
	
	def fetch(self, n = None, cols = All):
		if n is None:
			n = 100
		if cols is All:
			cols = self.colnames
		I = [ self.col_index[c] for c in cols ]
		print I
		#rows = [ self.reader.next() for _ in xrange(n) ]
		rows = list(_take(self.reader, n))
		res = dict( (self.colnames[i], numpy.array([self.coltypes[i].type(r[i]) for r in rows])) for i in I )
		return res

