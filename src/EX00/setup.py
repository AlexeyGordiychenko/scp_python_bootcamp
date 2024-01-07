from setuptools import setup, Extension

setup(name='Calculator',
      version='1.0',
      author='elidacon',
      description='Simple calculator module for Python written in C',
      ext_modules=[
          Extension('calculator', sources=['calculator.c']),
          Extension('calculator_float', sources=['calculator_float.c']),
      ])
