#!/usr/bin/python
"""Setup and install the archive interface with hpss."""
import sys
from pip.req import parse_requirements
from distutils.core import setup, Extension

# parse_requirements() returns generator of pip.req.InstallRequirement objects
INSTALL_REQS = parse_requirements('requirements.txt')

HPSS = Extension('archiveinterface.archivebackends.hpss._hpssExtensions',
                 sources=['archiveinterface/archivebackends/hpss/hpssExtensions.c'],
                 include_dirs=['/opt/hpss/include'],
                 library_dirs=['/opt/hpss/lib'],
                 libraries=['hpss', 'tirpc'],
                 extra_compile_args=['-DLINUX', '-DHPSS51', '-DLITTLEEND'])

EXT_MODULES = []
if '--hpss' in sys.argv:
    EXT_MODULES.append(HPSS)
    sys.argv.remove('--hpss')

setup(name='PacificaArchiveInterface',
      version='1.0',
      description='Pacifica Archive Interface',
      author='David Brown',
      author_email='david.brown@pnnl.gov',
      packages=['archiveinterface', 'archiveinterface.archivebackends',
                'archiveinterface.archivebackends.abstract',
                'archiveinterface.archivebackends.posix',
                'archiveinterface.archivebackends.hpss',
                'archiveinterface.archivebackends.oracle_hms_sideband'],
      scripts=['scripts/archiveinterfaceserver.py'],
      install_requires=[str(ir.req) for ir in INSTALL_REQS],
      ext_modules=EXT_MODULES)
