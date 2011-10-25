cimport numpy
from libc.string cimport memcpy

import mmap
import numpy

cdef extern from "Python.h":
	#ctypedef Py_ssize_t (*readbufferproc)(PyObject *, Py_ssize_t, void **)
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
def mmap_random_access(m, numpy.ndarray[numpy.int_t, ndim=1] begin, numpy.ndarray[numpy.int_t, ndim=1] end):
	
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
	write_b(m, 0, & dst_v)
	cdef char * dst = <char*> dst_v

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
		memcpy(dst + off, src + i1, k)
		off += k
	return res
