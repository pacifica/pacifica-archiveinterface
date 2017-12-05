#!/usr/bin/python
"""
Pacifica Archive Interface.

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


def main():
    """Main method to start the wsgi ref server."""
    parser = ArgumentParser(description='Run the archive interface.')

    parser.add_argument('-p', '--port', metavar='PORT', type=int,
                        default=8080, dest='port',
                        help='port to listen on')
    parser.add_argument('-a', '--address', metavar='ADDRESS',
                        default='localhost', dest='address',
                        help='address to listen on')
    parser.add_argument('-t', '--type', dest='type', default='posix',
                        choices=['hpss', 'posix', 'hmssideband'],
                        help='use the typed backend')
    parser.add_argument('--prefix', metavar='PREFIX', dest='prefix',
                        default='/tmp', help='prefix to save data at')
    parser.add_argument('--config', metavar='CONFIG', dest='config',
                        default=None, help='config file location')

    args = parser.parse_args()

    # set the config file global
    if args.config:
        set_config_name(args.config)
    else:
        archivei_config = os.getenv('ARCHIVEI_CONFIG')
        if archivei_config:
            set_config_name(archivei_config)
    # Get the specified Backend Archive
    factory = ArchiveBackendFactory()
    backend = factory.get_backend_archive(
        args.type,
        args.prefix
    )
    # Create the archive interface
    generator = ArchiveInterfaceGenerator(backend)
    srv = make_server(args.address, args.port,
                      generator.pacifica_archiveinterface)

    srv.serve_forever()
