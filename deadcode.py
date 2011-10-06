
# Track which variables are mentioned in a piece of code
# by checking refcounts to dependency-tracking proxies.
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


# Track variable usage with special proxy
# that logs __getitem__
class column_ref_tracker(object):
	
	class column_ref(object):
		def __init__(self, table_ref, path):
			self.table_ref = table_ref
			self.path = path
			
		def __getitem__(self, name):
			self.path += '.' + name
			return self
		
	def __init__(self):
		self.refs = set()
	
	def __getitem__(self, name):
		refs.add(name)
		return proxy.passthru()

def get_refs(f, names):
	
	tracker = column_ref_tracker()
	f(tracker)
	return column_ref_tracker.refs.insersection(names)


