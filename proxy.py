
# Lifted from http://docs.python.org/reference/datamodel.html#specialnames
special_methods = set([ 
	'__new__',
	'__init__',
	'__del__',
	'__repr__',
	'__str__',
	'__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', 
	'__cmp__', '__rcmp__',
	'__hash__',
	'__nonzero__', '__unicode__',
	'__getattr__', '__setattr__', '__delattr__',
	'__getattribute__', 
	'__get__', '__set__', '__delete_',
	'__slots__',
	'__instancecheck__',
	'__subclasshook__',
	'__call__',
	'__len__', '__getitem__', '__setitem__', '__delitem__', '__iter__', '__reversed__', '__contains__',
	'__getslice__', '__setslice__', '__delslice__', 
	'__add__', '__sub__', '__mul__', '__floordiv__', '__mod__', '__divmod__', '__pow__', 
	'__lshift__', '__rshift__', '__and__', '__xor__', '__or__', '__div__', '__truediv__', 
	'__radd__', '__rsub__', '__rmul__', '__rdiv__', '__rtruediv__', '__rfloordiv__', '__rmod__', '__rdivmod__', '__rpow__', 
	'__rlshift__', '__rrshift__', '__rand__', '__rxor__', '__ror__', 
	'__iadd__', '__isub__', '__imul__', '__idiv__', '__itruediv__', '__ifloordiv__', '__imod__', '__ipow__', 
	'__ilshift__', '__irshift__', '__iand__', '__ixor__', '__ior__', 
	'__neg__', '__pos__', '__abs__', '__invert__',
	'__complex__', '__int__', '__long__', '__float__',
	'__oct__', '__hex__', 
	'__index__',
	'__coerce__',
	'__enter__', '__exit__',
])

special_attrs = set([
	'__metaclass__',
])

class ref_tracking_proxy(object):
	
	def __init__(self, deps = None):
		self.deps = deps
	
	class Str(str):
		pass
	def __str__(self):
		res = self.Str()
		res.deps = self
		return res
	def __repr__(self):
		res = self.Str()
		res.deps = self
		return res
	
	class Int(int):
		pass
	def __int__(self):
		res = self.Int()
		res.deps = self
		return res
	
	class Float(float):
		pass
	def __float__(self):
		res = self.Float()
		res.deps = self
		return res
	
	class Long(long):
		pass
	def __long__(self):
		res = self.Long()
		res.deps = self
		return res

import inspect
no_override = set(['__new__', '__del__', '__init__', '__instancecheck__', '__subclasshook__', '__getattr__', '__getattribute__', '__setattr__', '__str__', '__repr__'])
for m in special_methods - no_override:
	if m not in ref_tracking_proxy.__dict__:
		def proxyfunc(self, *args, **kwargs):
			#try:
			#	print inspect.stack()[0]
			#except:
			#	pass
			deps = (self, args, kwargs)
			return ref_tracking_proxy(deps)
		proxyfunc.__name__ = 'PROXY__' + m
		setattr(ref_tracking_proxy, m, proxyfunc)


