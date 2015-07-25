#!/usr/bin/python
"""
MyEMSL Archive Interface

This is the main program that starts the WSGI server.

The core of the server code is in archive_interface.py.
"""
from argparse import ArgumentParser
from archive_interface import myemsl_archiveinterface as hpss_srv
from posix_interface import myemsl_archiveinterface as posix_srv
from wsgiref.simple_server import make_server

# 
parser = ArgumentParser(description='Run the archive interface.')

parser.add_argument('-p', '--port', metavar='PORT', type=int, 
    nargs=1, default=8080, dest='port', 
    help="port to listen on")
parser.add_argument('-a', '--address', metavar='PORT', nargs=1, 
    default='localhost', dest='address', 
    help="address to listen on")
parser.add_argument('-t', '--test', dest='server', action='store_const',
    const=posix_srv, default=hpss_srv, 
    help='use the posix testing backend')

args = parser.parse_args()
srv = make_server(args.address[-1], args.port[-1], args.server)
srv.serve_forever()
