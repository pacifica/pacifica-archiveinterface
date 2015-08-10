#!/usr/bin/python

from json import dumps
from os import path
from sys import stderr
from myemsl.hpss_ctypes import HPSSClient
from myemsl.id2filename import id2filename
import myemsl.archive_interface_responses as archive_interface_responses
from myemsl.extendedfile import ExtendedFile

BLOCK_SIZE = 1<<20

def path_info_munge(backend_type, filepath):
    """
    Munge the path_info environment variable based on the
    backend type.

    >>> path_info_munge('hpss', '1234')
    'd2/4d2'
    >>> path_info_munge('posix', '1234')
    '1234'
    """
    return_path = filepath
    if backend_type == 'hpss':
        return_path = un_abs_path(id2filename(int(filepath)))
    return return_path

def backend_open(backend_type, filepath, mode):
    """
    Open the file based on the backend type

    >>> type(backend_open('posix', '/tmp/1234', 'w'))
    <class 'extendedfile.ExtendedFile'>
    """
    if backend_type == 'hpss':
        return CLIENT.open(filepath, mode)
    return ExtendedFile(filepath, mode)

def un_abs_path(path_name):
    if path.isabs(path_name):
        path_name = path_name[1:]
    return path_name


CLIENT = None

def archive_generator(backend_type, prefix, user, auth):
    """Defines the methods that can be used on files for request types"""
    if backend_type == 'hpss':
        CLIENT = HPSSClient(user=user, auth=auth)

    def get(env, start_response):
        """Gets a file passed in the request"""
        myfile = None
        res = None
        path_info = un_abs_path(env['PATH_INFO'])

        try:
            filename = path.join(prefix, path_info_munge(backend_type,
                                                         path_info))
        except:
            resp = archive_interface_responses.Responses()
            res = resp.munging_filepath_exception(start_response, backend_type,
                                                  path_info)
            return dumps(res)
        try:
            myfile = backend_open(backend_type, filename, "r")
            start_response('200 OK', [('Content-Type',
                                       'application/octet-stream')])
            if 'wsgi.file_wrapper' in env:
                return env['wsgi.file_wrapper'](myfile, BLOCK_SIZE)
            return iter(lambda: myfile.read(BLOCK_SIZE), '')
        except:
            resp = archive_interface_responses.Responses()
            res = resp.file_not_found_exception(start_response, filename)
            return dumps(res)

    def put(env, start_response):
        """Saves a file passed in the request"""
        myfile = None
        res = None
        path_info = un_abs_path(env['PATH_INFO'])
        stderr.flush()

        try:
            filename = path.join(prefix, path_info_munge(backend_type,
                                                         path_info))
        except:
            resp = archive_interface_responses.Responses()
            res = resp.munging_filepath_exception(start_response, backend_type,
                                                  path_info)
            return dumps(res)
        try:
            myfile = backend_open(backend_type, filename, "w")
            content_length = int(env['CONTENT_LENGTH'])
            while content_length > 0:
                if content_length > BLOCK_SIZE:
                    buf = env['wsgi.input'].read(BLOCK_SIZE)
                else:
                    buf = env['wsgi.input'].read(content_length)
                myfile.write(buf)
                content_length -= len(buf)

            resp = archive_interface_responses.Responses()
            res = resp.successful_put_response(start_response,
                                               env['CONTENT_LENGTH'])

        except Exception as ex:
            print >> stderr, ex
            res = resp.error_opening_file_exception(start_response, filename)
        return dumps(res)

    def status(env, start_response):
        """Gets the status of a file passed in the request"""
        myfile = None
        res = None
        status = None
        path_info = un_abs_path(env['PATH_INFO'])
        try:
            filename = path.join(prefix, path_info_munge(backend_type,
                                                         path_info))
        except:
            resp = archive_interface_responses.Responses()
            res = resp.munging_filepath_exception(start_response, backend_type,
                                                  path_info)
            return dumps(res)
        try:
            myfile = backend_open(backend_type, filename, "r")
        except:
            resp = archive_interface_responses.Responses()
            res = resp.file_not_found_exception(start_response, filename)
            return dumps(res)
        try:
            status = myfile.status()
            if status == 'disk':
                resp = archive_interface_responses.Responses()
                res = resp.file_disk_status(start_response, filename)
        except:
            resp = archive_interface_responses.Responses()
            res = resp.file_status_exception(start_response, filename)
        return dumps(res)

    def myemsl_archiveinterface(env, start_response):
        """Parses request method type"""
        res = None
        if env['REQUEST_METHOD'] == 'GET':
            return get(env, start_response)
        elif env['REQUEST_METHOD'] == 'PUT':
            return put(env, start_response)
        elif env['REQUEST_METHOD'] == 'HEAD':
            return status(env, start_response)
        else:
            resp = archive_interface_responses.responses()
            res = resp.unknown_request(start_response, env['REQUEST_METHOD'])
        return dumps(res)

    return myemsl_archiveinterface

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

