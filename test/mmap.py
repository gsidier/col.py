import util
import mmap
import numpy
f = file('/usr/local/iso/openSUSE-11.3-DVD-x86_64.iso', 'r')
m = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_COPY)#READ)
I = numpy.array(xrange(10000000), dtype=numpy.int) * 8
sz = 8
res = util.mmap_random_access(m, I, I + sz)
print "%d x %d = %d bytes" % (len(I), sz, len(res))
