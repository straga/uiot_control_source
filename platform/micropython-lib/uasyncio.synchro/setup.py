import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system's.
sys.path.pop(0)
from setuptools import setup
sys.path.append("..")
import sdist_upip

setup(name='micropython-uasyncio.synchro',
      version='0.1.1',
      description='Synchronization primitives for uasyncio.',
      long_description="This is a module reimplemented specifically for MicroPython standard library,\nwith efficient and lean design in mind. Note that this module is likely work\nin progress and likely supports just a subset of CPython's corresponding\nmodule. Please help with the development if you are interested in this\nmodule.",
      url='https://github.com/pfalcon/micropython-lib',
      author='Paul Sokolovsky',
      author_email='micropython-lib@googlegroups.com',
      maintainer='Paul Sokolovsky',
      maintainer_email='micropython-lib@googlegroups.com',
      license='MIT',
      cmdclass={'sdist': sdist_upip.sdist},
      packages=['uasyncio'],
      install_requires=['micropython-uasyncio.core'])
