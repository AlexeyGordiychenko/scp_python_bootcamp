from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(name='MulMatrix',
      version='1.0',
      author='elidacon',
      description='Simple matrix multiplication module written in Cpython',
      ext_modules=cythonize([Extension('matrix', sources=['multiply.pyx'])]))
