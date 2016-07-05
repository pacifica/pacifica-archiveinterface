#!/usr/bin/env python
"""
Setup and install the archive interface with hpss.
"""

from distutils.core import setup, Extension

PAI = Extension('pacifica._archiveinterface', ['src/status.c'],
                include_dirs=['/opt/hpss/include'],
                library_dirs=['/opt/hpss/lib'],
                libraries=['hpss', 'tirpc'],
                extra_compile_args=['-DLINUX', '-DHPSS51', '-DLITTLEEND']
               )

setup(name='PacificaArchiveInterface',
      version='1.0',
      description='Pacifica Archive Interface',
      author='David Brown',
      author_email='david.brown@pnnl.gov',
      packages=['pacifica'],
      scripts=['scripts/server.py'],
      ext_modules=[PAI]
     )
