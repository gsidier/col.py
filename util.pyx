cimport numpy
from libc.string cimport memcpy

import mmap
import numpy

cdef extern from "Python.h":
	ctypedef Py_ssize_t (*readbufferproc)(object, Py_ssize_t, void **)
	ctypedef Py_ssize_t (*writebufferproc)(object, Py_ssize_t, void **)
	
	ctypedef struct PyBufferProcs:
		readbufferproc bf_getreadbuffer
		writebufferproc bf_getwritebuffer
	
	ctypedef struct PyTypeObject:
		PyBufferProcs * tp_as_buffer
	
# the "object[...] m" syntax means m supports the buffer protocol
# which gives efficient access to the underlying data.
# (see http://docs.python.org/c-api/buffer.html for the python side of things)
# (and http://wiki.cython.org/enhancements/buffer for the cython side)
def mmap_read_offsets(m, numpy.ndarray[numpy.int_t, ndim=1] begin, numpy.ndarray[numpy.int_t, ndim=1] end):
	"""
	res = mmap_read_offets(m, begin, end)
	
	If m supports the buffer interface, then this function will return a 
	memory-mapped file containing the concatenation of the data byte sequences 
	m[begin[i]:end[i]] for all i in range.
	
	Inputs:
		* m: python object that implements the buffer interface
		* begin: list of start offsets
		* end: list of end offsets
	
	Output:
		* res: a memory-mapped file
	"""
	
	cdef int i
	cdef int n = len(begin)
	cdef int sz = numpy.sum(end - begin)
	
	cdef PyTypeObject * m_t = <PyTypeObject*> m.__class__
	cdef void * src_v
	cdef PyBufferProcs * m_buf = <PyBufferProcs *> m_t.tp_as_buffer
	cdef readbufferproc read_b = m_buf.bf_getreadbuffer
	read_b(m, 0, & src_v)
	cdef char * src = <char*> src_v
	
	cdef res = mmap.mmap(-1, sz)
	cdef PyTypeObject * res_t = <PyTypeObject*> res.__class__
	cdef void * dst_v
	cdef PyBufferProcs * res_buf = <PyBufferProcs *> res_t.tp_as_buffer
	cdef writebufferproc write_b = m_buf.bf_getwritebuffer
	write_b(res, 0, & dst_v)
	cdef char * dst = <char*> dst_v

	cdef size_t off = 0
	cdef size_t i1
	cdef size_t i2
	cdef size_t k
	cdef size_t j
	for i in xrange(n):
		i1 = begin[i]
		i2 = end[i]
		k = i2 - i1
		memcpy(dst + off, src + i1, k)
		off += k
	return res

def has_old_buffer_interface(x):
	"""
	Python supports a so-called "Buffer Interface" that allows efficient 
	access to the C implementation of an object that is implemented in C and 
	implements the interface.
	
	Furthermore as is often the case in Python there are 2 competing versions 
	of the buffer interface, the "old-style interface" and the "new-style" 
	interface. A python object can presumably implement either, none or both 
	of these.
	
	This function returns True iff the argument supports the old-style buffer 
	interface.
	"""
	cdef PyTypeObject * t = <PyTypeObject*> x.__class__
	cdef PyBufferProcs * buf = <PyBufferProcs *> t.tp_as_buffer
	return buf != <PyBufferProcs*>0

def has_new_buffer_interface(x):
	"""
	Python supports a so-called "Buffer Interface" that allows efficient 
	access to the C implementation of an object that is implemented in C and 
	implements the interface.
	
	Furthermore as is often the case in Python there are 2 competing versions 
	of the buffer interface, the "old-style interface" and the "new-style" 
	interface. A python object can presumably implement either, none or both 
	of these.
	
	This function returns True iff the argument supports the new-style buffer 
	interface.
	"""
	cdef object[char] y
	y = x

