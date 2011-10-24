cimport numpy

import mmap
import numpy

def mmap_random_access(m, numpy.ndarray[numpy.int_t, ndim=1] begin, numpy.ndarray[numpy.int_t, ndim=1] end):
	
	cdef int i
	cdef int n = len(begin)
	#cdef numpy.ndarray[achar, ndim=1] res = numpy.zeros(numpy.sum(end - begin), dtype=numpy.byte)
	cdef int sz = numpy.sum(end - begin)
	res = mmap.mmap(-1, sz)
	cdef int off = 0
	getbytes = m.__getslice__
	setbytes = res.__setslice__
	cdef int i1
	cdef int i2
	cdef int k
	for i in xrange(n):
		i1 = begin[i]
		i2 = end[i]
		k = i2 - i1
		#res[off:off+k] = numpy.fromstring(getbytes(i1, i2), dtype=char)
		setbytes(off, off+k, getbytes(i1, i2))
		off += k
	return res
