import proxy

import sys

All = type("All", (), {})()
type(All).__init__ = NotImplemented

class cursor(object):
	
	columns = None # [ ( "name" or None, "type" ) ]
	
	def fetch(self, n = None, cols = All):
		raise NotImplementedError
	
	def select(self, expr):
		
		return select(self, expr)


class select(cursor):
	
	def __init__(self, c, expr):
		self.c = c
		self.expr = expr
		self.columns = get_refs(expr, c.columns)
	
	def fetch(self, n = None, cols = All):
		pass

def get_refs(f, names):
	
	for name in names:
		f.__globals__[name] = proxy.ref_tracking_proxy()
	
	f.__globals__['len'] = lambda x: proxy.ref_tracking_proxy(x)
	f.__globals__['int'] = lambda x: proxy.ref_tracking_proxy(x)
	f.__globals__['float'] = lambda x: proxy.ref_tracking_proxy(x)
	f.__globals__['bool'] = lambda x: proxy.ref_tracking_proxy(x)
	
	refcounts1 = dict( (name, sys.getrefcount(f.__globals__[name])) for name in names )
	res = f()
	refcounts2 = dict( (name, sys.getrefcount(f.__globals__[name])) for name in names )
	
	changed = [ name for name in names if refcounts1[name] != refcounts2[name] ]
	return changed


