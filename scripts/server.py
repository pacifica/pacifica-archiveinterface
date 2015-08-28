#!/usr/bin/python
"""
MyEMSL Archive Interface

This is the main program that starts the WSGI server.

The core of the server code is in archive_interface.py.
"""
import sys
import os
from argparse import ArgumentParser
from myemsl.archive_interface import ArchiveGenerator
from wsgiref.simple_server import make_server

PARSER = ArgumentParser(description='Run the archive interface.')

PARSER.add_argument('-p', '--port', metavar='PORT', type=int,
                    default=8080, dest='port',
                    help="port to listen on")
PARSER.add_argument('-a', '--address', metavar='ADDRESS',
                    default='localhost', dest='address',
                    help="address to listen on")
PARSER.add_argument('-t', '--type', dest='type', default='hpss',
                    choices=['hpss', 'posix'],
                    help='use the typed backend')
PARSER.add_argument('--prefix', metavar='PREFIX', dest='prefix',
                    default='/tmp', help='prefix to save data at')
PARSER.add_argument('-u', metavar='HPSSUSER', dest='user',
                    default=None, help='User Name for HPSS authentication')
PARSER.add_argument('--auth', metavar='AUTH', dest='auth', default=None,
                    help='KeyTab auth path for HPSS authentication')

ARGS = PARSER.parse_args()
GENERATOR = ArchiveGenerator(ARGS.type, ARGS.prefix, ARGS.user, ARGS.auth)
SRV = make_server(ARGS.address, ARGS.port,
                  GENERATOR.myemsl_archiveinterface)
SRV.serve_forever()
