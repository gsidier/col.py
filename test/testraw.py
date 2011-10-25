import raw
from curs import npcur, hjoin
import tempfile

if __name__ == '__main__':
	
	x = npcur(range(10), 'x')
	T = x.columns['x']
	f = tempfile.TemporaryFile()
	raw.write_raw(f, x, 'x')
	f.seek(0)
	y = raw.read_raw(f, type=T, name='y')
	z = raw.read_raw(f, type=T, name='z')
	print y.fetch()
	I = npcur([6,4,2,2,4,2,3], '_')
	print y.columns
	print z.columns
	yyI = y.select(lambda y: {'a': y, 'b': y})[I]
	print yyI.fetch(3)
