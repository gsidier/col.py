from curs import cursor, All
import dtype
from util import mmap_read_offsets

import mmap
import numpy

class RawCur(cursor):
	
	def __init__(self, data, type, name = '_'):
		self.data = data
		self.type = dtype.dtype(type)
		self.name = name
		self.columns = { self.name: self.type }
		self.itemsize = numpy.dtype(self.type).itemsize
		self.off = 0
	
	def fetch(self, n = None, cols = All):
		if hasattr(n, '__iter__'):
			I = numpy.array(n)
			T = numpy.dtype(self.type)
			begin = I * T.itemsize
			end = begin + T.itemsize
			print begin
			print end
			print end - begin
			bytes = mmap_read_offsets(self.data, begin, end)
			res = numpy.fromstring(bytes, dtype=T)
			return {
				self.name: res
			}
		
		else:
			n = n or 1024
			bytes = self.data[self.off:self.off + n * self.itemsize]
			a = numpy.fromstring(bytes, self.type)
			nread = len(a)
			self.off += len(bytes)
			return {
				self.name : a
			}

def write_raw(f, curs, col):
	fetchsz = 4096
	while 1:
		cols = curs.fetch(fetchsz, [ col ])
		a = cols[col]
		if len(a) == 0:
			break
		a.tofile(f)

def read_raw(f, type, name = '_'):
	data = mmap.mmap(f.fileno(), 0, access = mmap.ACCESS_READ)
	return RawCur(data, type, name)

