#!/usr/bin/python
"""Class for the archive interface.  ALlows API to file interactions"""
from json import dumps
from os import path
from sys import stderr
from myemsl.hpss_ctypes import HPSSClient
from myemsl.hpss_ctypes import HPSSStatus
from myemsl.id2filename import id2filename
import myemsl.archive_interface_responses as archive_interface_responses
from myemsl.extendedfile import ExtendedFile

BLOCK_SIZE = 1<<20


def un_abs_path(path_name):
    """Removes absolute path piece"""
    if path.isabs(path_name):
        path_name = path_name[1:]
    return path_name


class ArchiveGenerator(object):
    """Defines the methods that can be used on files for request types
    doctest for the archive generator class

    HPSS Doc Tests
    >>> user_name = "svc-myemsldev"
    >>> auth_path = "/var/hpss/etc/svc-myemsldev.keytab"
    >>> prefix = "/myemsl-dev/bundle"
    >>> backend_type = "hpss"
    >>> archiveHpss = ArchiveGenerator(backend_type, prefix, user_name, auth_path)
    >>> type(archiveHpss.backend_open("/myemsl-dev/bundle/test.txt", 'w'))
    <class 'myemsl.hpss_ctypes.HPSSFile'>
    >>> archiveHpss.path_info_munge('1234')
    'd2/4d2'



    Posix file tests
    >>> u_name = None
    >>> a_path = None
    >>> prefix_posix = ""
    >>> backend_posix = "posix"
    >>> archivePosix = ArchiveGenerator(backend_posix, prefix_posix, u_name, a_path)

    >>> type(archivePosix.backend_open('/tmp/1234', 'w'))
    <class 'myemsl.extendedfile.ExtendedFile'>
    >>> archivePosix.path_info_munge('1234')
    '1234'
    >>> type(archivePosix.status())
    """
    def __init__(self, backend_type, prefix, user, auth):
        self._client = None
        self._backend_type = backend_type
        self._prefix = prefix

        if backend_type == 'hpss':
            self._client = HPSSClient(user=user, auth=auth)

    def get(self, env, start_response):
        """Gets a file passed in the request"""
        myfile = None
        res = None
        backend_type = self._backend_type
        prefix = self._prefix
        path_info = un_abs_path(env['PATH_INFO'])

        try:
            filename = path.join(prefix, self.path_info_munge(path_info))
        except:
            resp = archive_interface_responses.Responses()
            res = resp.munging_filepath_exception(start_response, backend_type,
                                                  path_info)
            return dumps(res)
        try:
            myfile = self.backend_open(filename, "r")
            start_response('200 OK', [('Content-Type',
                                       'application/octet-stream')])
            if 'wsgi.file_wrapper' in env:
                return env['wsgi.file_wrapper'](myfile, BLOCK_SIZE)
            return iter(lambda: myfile.read(BLOCK_SIZE), '')
        except:
            resp = archive_interface_responses.Responses()
            res = resp.file_not_found_exception(start_response, filename)
            return dumps(res)

    def put(self, env, start_response):
        """Saves a file passed in the request"""
        myfile = None
        res = None
        backend_type = self._backend_type
        prefix = self._prefix
        path_info = un_abs_path(env['PATH_INFO'])
        stderr.flush()

        try:
            filename = path.join(prefix, self.path_info_munge(path_info))
        except:
            resp = archive_interface_responses.Responses()
            res = resp.munging_filepath_exception(start_response, backend_type,
                                                  path_info)
            return dumps(res)
        try:
            myfile = self.backend_open(filename, "w")
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
            res = resp.error_opening_file_exception(start_response, filename)
        return dumps(res)

    def status(self, env, start_response):
        """Gets the status of a file passed in the request"""
        myfile = None
        res = None
        status = None
        backend_type = self._backend_type
        prefix = self._prefix
        path_info = un_abs_path(env['PATH_INFO'])
        resp = archive_interface_responses.Responses()
        try:
            filename = path.join(prefix, self.path_info_munge(path_info))
        except:
            res = resp.munging_filepath_exception(start_response, backend_type,
                                                  path_info)
            return dumps(res)
        try:
            myfile = self.backend_open(filename, "r")
        except:
            res = resp.file_not_found_exception(start_response, filename)
            return dumps(res)
        try:
            status = myfile.status()
            if status == 'disk':
                res = resp.file_disk_status(start_response, filename)
            elif isinstance(status, HPSSStatus) == True:
                res = resp.file_hpss_status(start_response, filename, status._mtime,
                                            status._ctime, status._bytes_per_level)
            else:
                res = resp.file_status_exception(start_response, type(status))


        except:
            resp = archive_interface_responses.Responses()
            res = resp.file_status_exception(start_response, filename)
        return dumps(res)


    def backend_open(self, filepath, mode):
        """
        Open the file based on the backend type
        """
        if self._backend_type == 'hpss':
            return self._client.open(filepath, mode)
        return ExtendedFile(filepath, mode)

    def path_info_munge(self, filepath):
        """
        Munge the path_info environment variable based on the
        backend type.
        """
        return_path = filepath
        if self._backend_type == 'hpss':
            return_path = un_abs_path(id2filename(int(filepath)))
        return return_path

    def myemsl_archiveinterface(self, env, start_response):
        """Parses request method type"""
        res = None
        if env['REQUEST_METHOD'] == 'GET':
            return self.get(env, start_response)
        elif env['REQUEST_METHOD'] == 'PUT':
            return self.put(env, start_response)
        elif env['REQUEST_METHOD'] == 'HEAD':
            return self.status(env, start_response)
        else:
            resp = archive_interface_responses.Responses()
            res = resp.unknown_request(start_response, env['REQUEST_METHOD'])
        return dumps(res)

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

