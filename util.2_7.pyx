cimport numpy
from libc.string cimport memcpy

import mmap
import numpy

# the "object[...] m" syntax means m supports the buffer protocol
# which gives efficient access to the underlying data.
# (see http://docs.python.org/c-api/buffer.html for the python side of things)
# (and http://wiki.cython.org/enhancements/buffer for the cython side)
def mmap_random_access(object[char] m, numpy.ndarray[numpy.int_t, ndim=1] begin, numpy.ndarray[numpy.int_t, ndim=1] end):
	
	cdef int i
	cdef int n = len(begin)
	cdef int sz = numpy.sum(end - begin)
	cdef object[char, ndim=1, mode="c", negative_indices=False] res = mmap.mmap(-1, sz)
	cdef int off = 0
	#getbytes = m.__getslice__
	#setbytes = res.__setslice__
	cdef int i1
	cdef int i2
	cdef int k
	cdef int j
	for i in xrange(n):
		i1 = begin[i]
		i2 = end[i]
		k = i2 - i1
		#setbytes(off, off+k, getbytes(i1, i2))
		##for j in xrange(k):
		##	res[off + j] = m[i1 + k]
		memcpy(& res[off], & m[i1], k)
		off += k
	return res
