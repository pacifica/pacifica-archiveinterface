#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the archive interface with hpss."""
import sys
from os.path import isfile
# pylint: disable=no-name-in-module
# pylint: disable=import-error
from setuptools.extension import Extension
# pylint: enable=import-error
# pylint: enable=no-name-in-module
from setuptools import setup, find_packages
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
INSTALL_REQS = parse_requirements('requirements.txt', session='hack')

HPSS = Extension(
    'archiveinterface.archivebackends.hpss._hpssExtensions',
    sources=[
        'archiveinterface/archivebackends/hpss/hpssExtensions.c'
    ],
    include_dirs=['/opt/hpss/include'],
    library_dirs=['/opt/hpss/lib'],
    libraries=['hpss', 'tirpc'],
    extra_compile_args=['-DLINUX', '-DHPSS51', '-DLITTLEEND']
)

EXT_MODULES = []
if '--with-hpss' in sys.argv:
    EXT_MODULES.append(HPSS)
    sys.argv.remove('--with-hpss')
elif isfile('/opt/hpss/include/hpss_api.h'):
    EXT_MODULES.append(HPSS)
if '--without-hpss' in sys.argv:
    EXT_MODULES = []
    sys.argv.remove('--without-hpss')

setup(
    name='PacificaArchiveInterface',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Pacifica Archive Interface',
    author='David Brown',
    author_email='david.brown@pnnl.gov',
    packages=find_packages(),
    scripts=['ArchiveInterfaceServer.py'],
    entry_points={
        'console_scripts': ['ArchiveInterface=archiveinterface:main'],
    },
    install_requires=[str(ir.req) for ir in INSTALL_REQS],
    ext_modules=EXT_MODULES
)
