import numpy

def dtype(t):
	if len(str(t)) == 1:
		return t
	else:
		return numpy.dtype(t).char

