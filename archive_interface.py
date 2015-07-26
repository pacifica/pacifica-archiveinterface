#!/usr/bin/python

from json import dumps
from os import path
from hpss_ctypes import HPSSClient, HPSSFile

CLIENT = HPSSClient(user="svc-myemsldev", auth="/home/dmlb2000/svc-myemsldev.keytab")
block_size = 1<<12

def path_info_munge(backend_type, path):
    return path

def backend_open(backend_type, path, mode):
    if backend_type == 'hpss':
        return CLIENT.open(path, mode)
    return open(path, mode)

def archive_generator(backend_type, prefix):
    def myemsl_archiveinterface(env, start_response):
        res = None
        if env['REQUEST_METHOD'] == 'GET':
            myfile = backend_open(backend_type, 
                path.join(prefix,
                    path_info_munge(backend_type, env['PATH_INFO'])
                ), "r")
            start_response('200 OK', [('Content-Type','application/octet-stream')])
            if 'wsgi.file_wrapper' in env:
                return env['wsgi.file_wrapper'](myfile, block_size)
            else:
                return iter(lambda: myfile.read(block_size), '')
        elif env['REQUEST_METHOD'] == 'PUT':
            myfile = backend_open(backend_type, path.join(prefix,env['PATH_INFO']), "w")
            buf = env['wsgi.input'].read(block_size)
            total = len(buf)
            while len(buf):
                myfile.write(buf)
                buf = env['wsgi.input'].read(block_size)
                total += len(buf)
            start_response('200 OK', [('Content-Type','application/json')])
            res = {
                'message' => 'Thanks for the data',
                'total_bytes' => str(total)
            }
        else:
            start_response('200 OK', [('Content-Type','application/json')])
            res = {
                'message' => 'Unknown request method',
                'request_method' => env['REQUEST_METHOD']
            }
        return dumps(res)
    return myemsl_archiveinterface
