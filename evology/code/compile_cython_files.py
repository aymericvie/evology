from matplotlib.pyplot import annotate
from setuptools import Extension, setup
import os

from Cython.Build import cythonize

# import numpy

include_dirs = [os.getcwd()]
extensions = [
    Extension(e, [f"{e}.pyx"], include_dirs=include_dirs)
    for e in [
        "cythonized",
        "data",
        "market",
        "balance_sheet_cython",
        "investment",
        "fitness",
    ]
]

setup(
    ext_modules=cythonize(extensions, annotate=True),
    # include_dirs=[numpy.get_include()],
)
