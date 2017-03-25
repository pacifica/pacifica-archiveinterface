#!/usr/bin/python
"""
Pacifica Archive Interface

This is the main program that starts the WSGI server.

The core of the server code is in archive_interface.py.

Any new Backends added need to have the type argument extended
to support the new Backend Archie type

"""
import os
from argparse import ArgumentParser
from wsgiref.simple_server import make_server
from archiveinterface.archive_interface import ArchiveInterfaceGenerator
from archiveinterface.archive_utils import set_config_name
from archiveinterface.archivebackends.archive_backend_factory import \
     ArchiveBackendFactory

PARSER = ArgumentParser(description='Run the archive interface.')

PARSER.add_argument('-p', '--port', metavar='PORT', type=int,
                    default=8080, dest='port',
                    help='port to listen on')
PARSER.add_argument('-a', '--address', metavar='ADDRESS',
                    default='localhost', dest='address',
                    help='address to listen on')
PARSER.add_argument('-t', '--type', dest='type', default='posix',
                    choices=['hpss', 'posix', 'hmssideband'],
                    help='use the typed backend')
PARSER.add_argument('--prefix', metavar='PREFIX', dest='prefix',
                    default='/tmp', help='prefix to save data at')
PARSER.add_argument('--config', metavar='CONFIG', dest='config',
                    default=None, help='config file location')

ARGS = PARSER.parse_args()

#set the config file global
if ARGS.config:
    set_config_name(ARGS.config)
else:
    ARCHIVEI_CONFIG = os.getenv('ARCHIVEI_CONFIG')
    if ARCHIVEI_CONFIG:
        set_config_name(ARCHIVEI_CONFIG)
#Get the specified Backend Archive
FACTORY = ArchiveBackendFactory()
BACKEND = FACTORY.get_backend_archive(
    ARGS.type,
    ARGS.prefix
)
#Create the archive interface
GENERATOR = ArchiveInterfaceGenerator(BACKEND)
SRV = make_server(ARGS.address, ARGS.port,
                  GENERATOR.pacifica_archiveinterface)

SRV.serve_forever()
