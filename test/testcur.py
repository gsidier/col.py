from curs import cursor, select, All, hjoin, npcur

import numpy

if __name__ == '__main__':
	
	A = npcur(numpy.array(range(10), 'float64'))
	B = npcur(numpy.array(range(0, 30, 3), 'int64'))

	x = A.select(lambda val: {'x': val})
	y = B.select(lambda val: {'y': val})
	z = hjoin(x, y)
	print z.select(lambda x, y: { 'z': x * y }).fetch(100)

