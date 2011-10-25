import util
import mmap
import numpy

import sys

PATH, N, SZ = sys.argv[1:]
N = int(N)
SZ = int(SZ)

f = file(PATH, 'r')
m = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ)
f_sz = len(m)
#I = numpy.array(xrange(1000000), dtype=numpy.int) * 8
I = numpy.random.randint(0, f_sz - SZ, N)
#I = numpy.array(sorted(I))
print I
print I + SZ
res = util.mmap_random_access(m, I, I + SZ)
print "%d x %d = %d bytes" % (len(I), SZ, len(res))

