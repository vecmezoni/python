import inspect
import unittest

def curry(function, *args, **kwargs):
	"""
	Returns function or value, depending on set arguments.
	If values of all positional arguments are set returns value of function.
	Otherwise returns function with not noted arguments
	"""
	pargs = inspect.getargspec(function)[0]
	default_values = inspect.getargspec(function)[3]
	if default_values != None:
		defaults = {key: value for key, value in zip(pargs[-len(default_values):],default_values)}
	else:
		defaults = {}
	filled = (set(kwargs) | set(defaults)) & set(pargs)
	if len(args) + len(filled) >= len(pargs):
		return function(*args, **kwargs)
	elif len(args) + len(filled) + len(defaults) >= len(pargs):
		pass
	return lambda *x, **y: curry(function, *(args + x), **dict(kwargs, **y))
	
	
class TestCurrying(unittest.TestCase):
	def setUp(self):
		@curry
		def add(x, y, z, d = 4, **kwargs):
			result = x + y + z + d
			for key in kwargs:
				result += kwargs[key]
			return result
		self.function = add
	def test_args(self):
		self.assertEqual(self.function(1, 2, 3, 4), 10)
		self.assertEqual(self.function(1, 2)(3, 4), 10)
	def test_defaults(self):
		self.assertEqual(self.function(1)(2)(3), 10)
		self.assertEqual(self.function(1, 2, 3), 10)
		self.assertEqual(self.function(1)(2, 3), 10)
	def test_kwargs(self):
		self.assertEqual(self.function(x = 1)(y = 2)(z = 3), 10)
		self.assertEqual(self.function(kwarg = 5)(1, 2, 3, 4), 15)
		self.assertEqual(self.function(kwarg = 5)(another_kwarg = 5)(1, 2, 3), 20)
		self.assertEqual(self.function(kwarg = 5)(1)(2, 3, 4), 15)
		self.assertEqual(self.function(kwarg = 5)(another_kwarg = 5)(1)(2)(3), 20)

if __name__ == '__main__':
    unittest.main()	

