

import setuptools
from setuptools import setup, Extension


setup(name='sn-nacl',
      #      packages=setuptools.find_packages(),
      packages=['nacl', 'nacl.lib', 'nacl.models',
                'nacl.plotting', 'nacl.simulations', 'nacl.util'],
      ext_modules=[Extension('nacl.lib._libnacl',
                             ['nacl/lib/utils.c',],
                             extra_compile_args=['-std=c11', '-O3'])],
      version="0.4",
      description="Supernova empirical model training package",
      author='G. Augarde, N. Regnault, M. Betoule, S. Bongard',
      author_email='nicolas.regnault@lpnhe.in2p3.fr',
      #      package_dir={'': 'nacl'},
      zip_safe=False,

      install_requires=['numpy>=1.7', 'matplotlib', 'seaborn', 'cython', 'scikit-sparse', 'astropy', 'sparseqr'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest-3'],
)
