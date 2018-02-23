#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Pacifica Archive Interface.

This is the main program that starts the WSGI server.

The core of the server code is in archive_interface.py.

Any new Backends added need to have the type argument extended
to support the new Backend Archie type

"""
from os import getenv
import cherrypy
from archiveinterface import error_page_default
from archiveinterface.archive_utils import set_config_name
from archiveinterface.archive_interface import ArchiveInterfaceGenerator
from archiveinterface.archivebackends.archive_backend_factory import \
    ArchiveBackendFactory

BACKEND_TYPE = getenv('PAI_BACKEND_TYPE', 'posix')
PREFIX = getenv('PAI_PREFIX', '/tmp')

ARCHIVEI_CONFIG = getenv('ARCHIVEI_CONFIG')
CP_CONFIG = getenv('CP_CONFIG')
if ARCHIVEI_CONFIG:
    set_config_name(ARCHIVEI_CONFIG)

# Get the specified Backend Archive
FACTORY = ArchiveBackendFactory()
BACKEND = FACTORY.get_backend_archive(
    BACKEND_TYPE,
    PREFIX
)

cherrypy.config.update({'error_page.default': error_page_default})
# pylint doesn't realize that application is actually a callable
# pylint: disable=invalid-name
application = cherrypy.Application(
    ArchiveInterfaceGenerator(BACKEND),
    '/',
    CP_CONFIG
)
# pylint: enable=invalid-name
