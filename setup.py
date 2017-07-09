import sys
from setuptools import setup

if sys.version_info < (3, 2):
        print('Module requires Python 3.2 or greater')
        sys.exit(1)

setup(name='transfinite',
      version='0.1',
      description='Transfinite ordinals for Python',
      author='Alex Riley',
      license='MIT',
      packages=['transfinite'],
      zip_safe=False)
