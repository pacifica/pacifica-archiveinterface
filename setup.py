#!/usr/bin/env python

from distutils.core import setup, Extension

myemsl_archiveinterface = Extension('myemsl._archiveinterface', ['src/status.c'],
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
      packages=['myemsl'],
      scripts=['scripts/server.py'],
      ext_modules=[myemsl_archiveinterface]
     )
