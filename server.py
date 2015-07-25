#!/usr/bin/python

from argparse import ArgumentParser
from archive_interface import myemsl_archiveinterface
from wsgiref.simple_server import make_server

parser = ArgumentParser(description='Run the archive interface.')

parser.add_argument('-p', '--port', metavar='PORT', type=int, 
    nargs=1, required=True, dest='port')
parser.add_argument('-a', '--address', metavar='PORT', nargs=1, 
    required=True, dest='address')

args = parser.parse_args()
srv = make_server(args.address[-1], args.port[-1], myemsl_archiveinterface)
srv.serve_forever()
