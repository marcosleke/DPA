#! /usr/bin/env python
"""Density Peak Advanced clustering algorithm, scikit-learn compatible."""

import codecs
import os
import numpy 
from glob import glob
from os.path import basename, dirname, join, relpath, splitext
from setuptools import find_packages, setup, Extension
import warnings

try:
    from Cython.Build import cythonize
    HAVE_CYTHON = True
except ImportError as e:
    warnings.warn(e.args[0])
    HAVE_CYTHON = False

if not HAVE_CYTHON:
    warnings.warn('Cython is required in order to build the DPApipeline package')
    raise ImportError('Cython not found! Please install cython and try again')


# get __version__ from _version.py
for root, _, _ in os.walk('src'):
    for path in glob(join(root, '_version.py')):
        ver_file = path
with open(ver_file) as f:
    exec(f.read())

DISTNAME = 'DPApipeline'
DESCRIPTION = 'The Density Peak Advanced packages.'
with codecs.open('README.rst', encoding='utf-8-sig') as f:
    LONG_DESCRIPTION = f.read()
with open('requirements.txt') as f:
    INSTALL_REQUIRES = f.read().splitlines()
CLASSIFIERS = ['Intended Audience :: Science/Research',
               'Intended Audience :: Developers',
               'License :: OSI Approved',
               'Programming Language :: Python',
               'Topic :: Software Development',
               'Topic :: Scientific/Engineering',
               'Operating System :: Microsoft :: Windows',
               'Operating System :: POSIX',
               'Operating System :: Unix',
               'Operating System :: MacOS',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               'Programming Language :: Python :: 3.7']
EXTRAS_REQUIRE = {
    'tests': [
        'pytest',
        'pytest-cov'],
    'docs': [
        'sphinx',
        'sphinx-gallery',
        'sphinx_rtd_theme',
        'numpydoc',
        'matplotlib'
    ]
}
EXTENSIONS = [Extension(splitext(relpath(path, 'src').replace(os.sep, '.'))[0],
                 sources=[path],
                 include_dirs=[numpy.get_include()])
             for root, _, _ in os.walk('src')
             for path in glob(join(root, '*.pyx'))]

setup(name=DISTNAME,
      description=DESCRIPTION,
      author="Maria d'Errico",
      license='new BSD',
      version=__version__,
      long_description=LONG_DESCRIPTION,
      zip_safe=False,  # the package can run out of an .egg file
      classifiers=CLASSIFIERS,
      packages=find_packages('src')+find_packages('Examples')+find_packages('DP'),
      package_dir={'': 'src'},
      py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      ext_modules = cythonize(EXTENSIONS))
