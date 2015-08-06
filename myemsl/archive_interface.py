#!/usr/bin/python

from json import dumps
from os import path
from sys import stderr
from hpss_ctypes import HPSSClient, HPSSFile
from id2filename import id2filename
from archive_interface_responses import *
from extendedfile import ExtendedFile

block_size = 1<<20

def path_info_munge(backend_type, path):
    """
    Munge the path_info environment variable based on the
    backend type.

    >>> path_info_munge('hpss', '1234')
    'd2/4d2'
    >>> path_info_munge('posix', '1234')
    '1234'
    """
    if backend_type == 'hpss':
        path = un_abs_path(id2filename(int(path)))
    return path

def backend_open(backend_type, path, mode):
    """
    Open the file based on the backend type

    >>> type(backend_open('posix', '/tmp/1234', 'w'))
    <class 'extendedfile.ExtendedFile'>
    """
    if backend_type == 'hpss':
        return CLIENT.open(path, mode)
    return ExtendedFile(path, mode)

def un_abs_path(path_name):
    if path.isabs(path_name):
        path_name = path_name[1:]
    return path_name


CLIENT = None

def archive_generator(backend_type, prefix, user, auth):
    global CLIENT
    if backend_type == 'hpss':
        CLIENT = HPSSClient(user = user, auth = auth)
    def get(env, start_response):
        myfile = None
        res = None
        path_info = un_abs_path(env['PATH_INFO'])

        try:
            filename = path.join(prefix, path_info_munge(backend_type, path_info))
        except:
            res = munging_filepath_exception(start_response, backend_type, path_info)
            return dumps(res)
        try:
            myfile = backend_open(backend_type, filename, "r")
            start_response('200 OK', [('Content-Type', 'application/octet-stream')])
            if 'wsgi.file_wrapper' in env:
                return env['wsgi.file_wrapper'](myfile, block_size)
            return iter(lambda: myfile.read(block_size), '')
        except:
            res = file_not_found_exception(start_response, filename)
            return dumps(res)

    def put(env, start_response):
        myfile = None
        res = None
        path_info = un_abs_path(env['PATH_INFO'])
        stderr.flush()

        try:
            filename = path.join(prefix, path_info_munge(backend_type, path_info))
        except:
            res = munging_filepath_exception(start_response, backend_type, path_info)
            return dumps(res)
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

            res = successful_put_response(start_response, env['CONTENT_LENGTH'])
            del myfile
            
        except Exception as ex:
            print >> stderr, ex
            res = error_opening_file_exception(start_response, filename)
        return dumps(res)

    def status(env,start_response):
        myfile = None
        res = None
        status = None
        path_info = un_abs_path(env['PATH_INFO'])
        try:
            filename = path.join(prefix, path_info_munge(backend_type, path_info))
        except:
            res = munging_filepath_exception(start_response, backend_type, path_info)
            return dumps(res)
        try:
            myfile = backend_open(backend_type, filename, "r")        
        except:
            res = file_not_found_exception(start_response, filename)
            return dumps(res)
        try:
            status = myfile.status()
            if status == 'disk':
                res = file_disk_status(start_response, filename)
        except:
            res = file_status_exception(start_response, filename)
        return dumps(res)

    def myemsl_archiveinterface(env, start_response):
        res = None
        if env['REQUEST_METHOD'] == 'GET':
            return get(env, start_response)
        elif env['REQUEST_METHOD'] == 'PUT':
            return put(env, start_response)
        elif env['REQUEST_METHOD'] == 'HEAD':
            return status(env, start_response)
        else:
            res = unknown_request(start_response, env['REQUEST_METHOD'])
        return dumps(res)
    return myemsl_archiveinterface

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

