#!/usr/bin/python

from json import dumps
from os import path
from sys import stderr
from hpss_ctypes import HPSSClient, HPSSFile

CLIENT = HPSSClient(user="svc-myemsldev", auth="/home/dmlb2000/svc-myemsldev.keytab")
block_size = 1<<20

def path_info_munge(backend_type, path):
    """
    Munge the path_info environment variable based on the
    backend type.

    >>> path_info_munge('posix', '/1234')
    '/1234'
    """
    return path

def backend_open(backend_type, path, mode):
    """
    Open the file based on the backend type

    >>> type(backend_open('posix', '/tmp/1234', 'w'))
    <type 'file'>
    """
    if backend_type == 'hpss':
        return CLIENT.open(path, mode)
    return open(path, mode)

def archive_generator(backend_type, prefix):
    def get(env, start_response):
        path_info = None
        myfile = None
        if path.isabs(env['PATH_INFO']):
            path_info = env['PATH_INFO'][1:]
        else:
            path_info = env['PATH_INFO']
        filename = path.join(prefix, path_info_munge(backend_type, path_info))
        try:
            myfile = backend_open(backend_type, filename, "r")
            start_response('200 OK', [('Content-Type','application/octet-stream')])
            if 'wsgi.file_wrapper' in env:
                return env['wsgi.file_wrapper'](myfile, block_size)
            return iter(lambda: myfile.read(block_size), '')
        except:
            start_response('404 Not Found', [('Content-Type','application/json')])
            res = {
                'message': 'File not found',
                'file': str(myfile)
            }
            return dumps(res)

    def put(env, start_response):
        res = None
        path_info = None
        myfile = None
        stderr.flush()
        if path.isabs(env['PATH_INFO']):
            path_info = env['PATH_INFO'][1:]
        else:
            path_info = env['PATH_INFO']
        filename = path.join(prefix, path_info_munge(backend_type, path_info))
        try:
            myfile = backend_open(backend_type, filename, "w")
            content_length = int(env['CONTENT_LENGTH'])
            while content_length > 0:
                if content_length > block_size:
                    buf = env['wsgi.input'].read(block_size)
                else:
                    buf = env['wsgi.input'].read(content_length)
                myfile.write(buf)
                content_length -= len(buf)
            start_response('200 OK', [('Content-Type','application/json')])
            res = {
                'message': 'Thanks for the data',
                'total_bytes': env['CONTENT_LENGTH']
            }
        except Exception as ex:
            print >> stderr, ex
            start_response('500 Internal Server Error', [('Content-Type','application/json')])
            res = {
                'message': 'Error opening file',
                'file': str(myfile)
            }
        return dumps(res)

    def myemsl_archiveinterface(env, start_response):
        res = None
        if env['REQUEST_METHOD'] == 'GET':
            return get(env, start_response)
        elif env['REQUEST_METHOD'] == 'PUT':
            return put(env, start_response)
        else:
            start_response('200 OK', [('Content-Type','application/json')])
            res = {
                'message': 'Unknown request method',
                'request_method': env['REQUEST_METHOD']
            }
        return dumps(res)
    return myemsl_archiveinterface

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

