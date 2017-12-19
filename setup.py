#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the archive interface with hpss."""
import sys
# pylint: disable=no-name-in-module
# pylint: disable=import-error
from distutils.core import setup, Extension
# pylint: enable=import-error
# pylint: enable=no-name-in-module
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
INSTALL_REQS = parse_requirements('requirements.txt', session='hack')

HPSS = Extension('archiveinterface.archivebackends.hpss._hpssExtensions',
                 sources=[
                     'archiveinterface/archivebackends/hpss/hpssExtensions.c'],
                 include_dirs=['/opt/hpss/include'],
                 library_dirs=['/opt/hpss/lib'],
                 libraries=['hpss', 'tirpc'],
                 extra_compile_args=['-DLINUX', '-DHPSS51', '-DLITTLEEND'])

EXT_MODULES = []
if '--hpss' in sys.argv:
    EXT_MODULES.append(HPSS)
    sys.argv.remove('--hpss')

setup(name='PacificaArchiveInterface',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      description='Pacifica Archive Interface',
      author='David Brown',
      author_email='david.brown@pnnl.gov',
      packages=['archiveinterface', 'archiveinterface.archivebackends',
                'archiveinterface.archivebackends.abstract',
                'archiveinterface.archivebackends.posix',
                'archiveinterface.archivebackends.hpss',
                'archiveinterface.archivebackends.oracle_hms_sideband'],
      scripts=['ArchiveInterfaceServer.py'],
      entry_point={
          'console_scripts': ['ArchiveInterface=archiveinterface:main'],
      },
      install_requires=[str(ir.req) for ir in INSTALL_REQS],
      ext_modules=EXT_MODULES)
