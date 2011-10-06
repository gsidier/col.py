import proxy

import sys
import numpy

All = type("All", (), {})()
type(All).__init__ = NotImplemented

class cursor(object):
	
	columns = NotImplemented # { name: dtype }
	
	# n - If not specified, return as many rows as you want.
	#     If specified then try to return n rows unless eof was 
	#     reached in the process.
	# 
	# cols - subset of columns to fetch, or All
	def fetch(self, n = None, cols = All):
		raise NotImplementedError
	
	def select(self, expr):
		# General select syntax:
		# 
		# table.select(lambda a, b, .., z: {
		#    col1: expr1(a, b, .. z),
		#    col2: expr2(a, b, .. z),
		#    ...
		#  }
		# 
		# where a, b, ... z are columns of this cursor.
		return select(self, expr)

class select(cursor):
	
	def __init__(self, c, expr):
		self.c = c
		self.expr = expr
		self.refs = get_refs(expr, c.columns) # list of c's cols in the order they appear as lambda arguments
		self.columns = calc_column_types(expr, c.columns)
		
	def fetch(self, n = None, cols = All):
		data = self.c.fetch(n, self.refs)
		args = [ data[col] for col in self.refs ]
		res = self.expr(* args)
		return res
	
def get_refs(f, names):
	co = f.func_code
	argnames = co.co_varnames[:co.co_argcount]
	for arg in argnames:
		if arg not in names:
			raise NameError(arg)
	return argnames

def shandy(dtype):
	return numpy.array([], dtype)

def calc_column_types(f, col_types):
	co = f.func_code
	argnames = co.co_varnames[:co.co_argcount]
	for arg in argnames:
		if arg not in col_types:
			raise NameError(arg)
	
	args = [ shandy(col_types[a]) for a in argnames ]
	res = f(* args)
	res_types = dict( (k, v.dtype) for (k, v) in res.iteritems() )
	return res_types

def transpose_dict(d):
	# [ (k, v) ] -> [ (v, [ k ]) ]
	# A problem that crops up. Sometimes.
	V = set(d.values())
	b = dict([ (v, []) for v in V])
	for (k, v) in d.iteritems():
		b[v].append(k)
	return b

# Horizontal join
class hjoin(cursor):
	
	def __init__(self, *cursors):
		self.cursors = cursors
		self.columns = dict(
			[ (name, typ) 
				for c in self.cursors 
				for (name, typ) in c.columns.iteritems() 
			] 
		)
		self.col_src = dict(
			[ (name, c)
				for c in self.cursors
				for (name, typ) in c.columns.iteritems()
			]
		)
	
	def fetch(self, n = None, cols = All):
		if cols is All:
			cols = self.columns.keys()
		
		cols_curs = dict([(c, self.col_src[c]) for c in cols])
		curs_cols = transpose_dict(cols_curs)
		
		res = {}
		
		for curs_i, cols_i in curs_cols.iteritems():
			res_i = curs_i.fetch(n, cols_i)
			res.update(res_i)
		
		return res

hj = hjoin

class npcur(cursor):
	
	def __init__(self, arr, name = 'val'):
		self.name = name
		self.arr = numpy.array(arr)
		self.columns = { self.name: self.arr.dtype }
		self.i = 0
	
	def fetch(self, n = None, cols = All):
		if cols is All:
			cols = self.columns.keys()
		
		n = n or 128
		n = min(n, 128)
		
		i = self.i
		
		res = self.arr[i : i + n]
		i += len(res)
		
		self.i = i
		return { self.name: res }


