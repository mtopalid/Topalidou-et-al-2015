import numpy
from distutils.core import setup, Extension
from Cython.Build import cythonize

# setup(
#    ext_modules = cythonize("c_dana.pyx"),
#    include_dirs=[numpy.get_include()], requires=['numpy', 'numpy'],)
setup(
    ext_modules=[
        Extension("c_dana", ["c_dana.c"],
                  include_dirs=[numpy.get_include()]),],
)
