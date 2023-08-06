from distutils.core import setup
from Cython.Build import cythonize
setup(
        name = 'metbees',
        version = '1.0.0',
        description = 'Private',
        author = 'michaelheiden',
        ext_modules=cythonize("metbees.pyx")

        )

