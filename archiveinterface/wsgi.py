#!/usr/bin/python
"""
Pacifica Archive Interface.

This is the main program that starts the WSGI server.

The core of the server code is in archive_interface.py.

Any new Backends added need to have the type argument extended
to support the new Backend Archie type

"""
from os import getenv
from archiveinterface.archive_utils import set_config_name
from archiveinterface.archive_interface import ArchiveInterfaceGenerator
from archiveinterface.archivebackends.archive_backend_factory import \
     ArchiveBackendFactory

BACKEND_TYPE = getenv('PAI_BACKEND_TYPE', 'posix')
PREFIX = getenv('PAI_PREFIX', '/tmp')

ARCHIVEI_CONFIG = getenv('ARCHIVEI_CONFIG')
if ARCHIVEI_CONFIG:
    set_config_name(ARCHIVEI_CONFIG)

# Get the specified Backend Archive
FACTORY = ArchiveBackendFactory()
BACKEND = FACTORY.get_backend_archive(
    BACKEND_TYPE,
    PREFIX
)
# Create the archive interface
GENERATOR = ArchiveInterfaceGenerator(BACKEND)
# This is a function not a constant but pylint doesn't know that
# pylint: disable=invalid-name
application = GENERATOR.pacifica_archiveinterface
# pylint: enable=invalid-name
