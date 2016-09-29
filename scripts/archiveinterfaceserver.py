#!/usr/bin/python
"""
Pacifica Archive Interface

This is the main program that starts the WSGI server.

The core of the server code is in archive_interface.py.

Any new Backends added need to have the type argument extended
to support the new Backend Archie type

"""
from argparse import ArgumentParser
from wsgiref.simple_server import make_server
from archiveinterface.archive_interface import ArchiveInterfaceGenerator
from archiveinterface.archivebackends.archive_backend_factory import \
     ArchiveBackendFactory

PARSER = ArgumentParser(description='Run the archive interface.')

PARSER.add_argument('-p', '--port', metavar='PORT', type=int,
                    default=8080, dest='port',
                    help="port to listen on")
PARSER.add_argument('-a', '--address', metavar='ADDRESS',
                    default='localhost', dest='address',
                    help="address to listen on")
PARSER.add_argument('-t', '--type', dest='type', default='posix',
                    choices=['hpss', 'posix'],
                    help='use the typed backend')
PARSER.add_argument('--prefix', metavar='PREFIX', dest='prefix',
                    default='/tmp', help='prefix to save data at')
PARSER.add_argument('-u', metavar='HPSSUSER', dest='user',
                    default=None, help='User Name for HPSS authentication')
PARSER.add_argument('--auth', metavar='AUTH', dest='auth', default=None,
                    help='KeyTab auth path for HPSS authentication')

ARGS = PARSER.parse_args()
#Get the specified Backend Archive
FACTORY = ArchiveBackendFactory()
BACKEND = FACTORY.get_backend_archive(
    ARGS.type,
    ARGS.prefix,
    ARGS.user,
    ARGS.auth
)
#Create the archive interface
GENERATOR = ArchiveInterfaceGenerator(BACKEND)
SRV = make_server(ARGS.address, ARGS.port,
                  GENERATOR.pacifica_archiveinterface)

SRV.serve_forever()
