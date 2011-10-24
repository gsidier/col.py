from distutils.core import setup
from distutils.extension import Extension
from distutils.sysconfig import get_python_lib
from Cython.Distutils import build_ext
import os

if 'CFG' in os.environ and os.environ['CFG'] == 'debug':
	print "debug build"
	DEBUG = 1
else:
	DEBUG = 0

if DEBUG:
	compiler_args = ['-O0']
else:
	compiler_args = []
	
numpy_inc = os.path.join(get_python_lib(plat_specific=1), 'numpy/core/include/')

ext_modules = [Extension(
	"util",
	["util.pyx"],
	language = "c++",
	include_dirs = ['.', numpy_inc],
	libraries = ["stdc++"],
	extra_compile_args = compiler_args,
	extra_link_args = ["-L."]
)]

setup(
	name = 'db11',
	cmdclass = {'build_ext': build_ext},
	ext_modules = ext_modules
)

