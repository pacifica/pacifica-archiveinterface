#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Pacifica Archive Interface.

Any new Backends added need to have the type argument extended
to support the new Backend Archie type

"""
from os import getenv, path
from time import sleep
from threading import Thread
from argparse import ArgumentParser, SUPPRESS
from json import dumps
import cherrypy
from archiveinterface.archive_interface import ArchiveInterfaceGenerator
from archiveinterface.archive_utils import set_config_name
from archiveinterface.archivebackends.archive_backend_factory import \
    ArchiveBackendFactory


def error_page_default(**kwargs):
    """The default error page should always enforce json."""
    cherrypy.response.headers['Content-Type'] = 'application/json'
    return dumps({
        'status': kwargs['status'],
        'message': kwargs['message'],
        'traceback': kwargs['traceback'],
        'version': kwargs['version']
    })


def stop_later(doit=False):
    """Used for unit testing stop after 60 seconds."""
    if not doit:  # pragma: no cover
        return

    def sleep_then_exit():
        """
        Sleep for 20 seconds then call cherrypy exit.

        Hopefully this is long enough for the end-to-end tests to finish
        """
        sleep(20)
        cherrypy.engine.exit()
    sleep_thread = Thread(target=sleep_then_exit)
    sleep_thread.daemon = True
    sleep_thread.start()


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
                        default='{}tmp'.format(os.path.sep), help='prefix to save data at')
    parser.add_argument('-c', '--config', metavar='CONFIG', dest='config',
                        default=getenv('ARCHIVEI_CONFIG'), help='config file location')
    parser.add_argument('--stop-after-a-moment', help=SUPPRESS,
                        default=False, dest='stop_later',
                        action='store_true')

    args = parser.parse_args()

    # set the config file global
    set_config_name(args.config)
    # Get the specified Backend Archive
    factory = ArchiveBackendFactory()
    backend = factory.get_backend_archive(args.type, args.prefix)
    stop_later(args.stop_later)
    cherrypy.config.update({'error_page.default': error_page_default})
    cherrypy.config.update({
        'server.socket_host': args.address,
        'server.socket_port': args.port
    })
    cherrypy.quickstart(
        ArchiveInterfaceGenerator(backend),
        '/',
        args.config
    )
