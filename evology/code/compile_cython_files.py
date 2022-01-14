from setuptools import Extension, setup
import os

from Cython.Build import cythonize
#import numpy

include_dirs = [os.getcwd()]
extensions = [
    Extension("cythonized", ["cythonized.pyx"], include_dirs=include_dirs),
    Extension("data", ["data.pyx"], include_dirs=include_dirs),
]

setup(
    ext_modules=cythonize(extensions, annotate=False),
    #include_dirs=[numpy.get_include()],
)
