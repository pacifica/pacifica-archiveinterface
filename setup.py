#!/usr/bin/env python

from distutils.core import setup, Extension

pacifica_archiveinterface = Extension('pacifica._archiveinterface', ['src/status.c'],
      include_dirs = ['/opt/hpss/include'],
      library_dirs=['/opt/hpss/lib'],
      libraries=['hpss'],
      extra_compile_args = ['-DLINUX', '-DHPSS51', '-DLITTLEEND']
)

setup(name='MyEMSLArchiveInterface',
      version='1.0',
      description='MyEMSL Archive Interface',
      author='David Brown',
      author_email='david.brown@pnnl.gov',
      packages=['pacifica'],
      scripts=['scripts/server.py'],
      ext_modules=[pacifica_archiveinterface]
     )
