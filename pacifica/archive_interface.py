#!/usr/bin/python
"""Class for the archive interface.  ALlows API to file interactions"""
from json import dumps
from os import path
from sys import stderr
try:
    from pacifica.hpss_ctypes import HPSSClient
    from pacifica.hpss_ctypes import HPSSStatus
    HAVE_HPSS = True
except ImportError:
    HAVE_HPSS = False
from pacifica.id2filename import id2filename
import pacifica.archive_interface_responses as archive_interface_responses
from pacifica.extendedfile import ExtendedFile
from pacifica.extendedfile import POSIXStatus

import doctest

BLOCK_SIZE = 1<<20


class ArchiveInterfaceError(Exception):
    """
    ArchiveInterfaceError - basic exception class for this module.
    Will be used to throw exceptions up to the top level of the application
    >>> ArchiveInterfaceError()
    ArchiveInterfaceError()
    """
    pass


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
    >>> b_type = "hpss"
    >>> archiveHpss = ArchiveGenerator(b_type, prefix, user_name, auth_path)
    >>> type(archiveHpss.backend_open("/myemsl-dev/bundle/test.txt", 'w'))
    <class 'pacifia.hpss_ctypes.HPSSFile'>
    >>> archiveHpss.path_info_munge('1234')
    'd2/4d2'



    Posix file tests
    >>> u_name = None
    >>> a_path = None
    >>> prefix_posix = ""
    >>> b_posix = "posix"
    >>> archivePosix = ArchiveGenerator(b_posix, prefix_posix, u_name, a_path)
    >>> type(archivePosix.backend_open('/tmp/1234', 'w'))
    <class 'pacifica.extendedfile.ExtendedFile'>
    >>> archivePosix.path_info_munge('1234')
    '1234'
    """
    def __init__(self, backend_type, prefix, user, auth):
        self._client = None
        self._backend_type = backend_type
        self._prefix = prefix
        self._response = None

        if backend_type == 'hpss' and not HAVE_HPSS:
            raise ArchiveInterfaceError("type is hpss but we don't"
                                        +"have hpss loaded")
        if backend_type == 'hpss' and HAVE_HPSS:
            self._client = HPSSClient(user=user, auth=auth)

    def get(self, env, start_response):
        """Gets a file passed in the request"""
        myfile = None
        backend_type = self._backend_type
        prefix = self._prefix
        path_info = un_abs_path(env['PATH_INFO'])
        resp = archive_interface_responses.Responses()
        stderr.flush()

        try:
            filename = path.join(prefix, self.path_info_munge(path_info))
        except Exception as ex:
            self._response = resp.munging_filepath_exception(start_response,
                                                             backend_type,
                                                             path_info, ex)
            raise ArchiveInterfaceError()
        try:
            myfile = self.backend_open(filename, "r")
            start_response('200 OK', [('Content-Type',
                                       'application/octet-stream')])
            if 'wsgi.file_wrapper' in env:
                return env['wsgi.file_wrapper'](myfile, BLOCK_SIZE)
            return iter(lambda: myfile.read(BLOCK_SIZE), '')
        except Exception as ex:
            self._response = resp.file_not_found_exception(start_response,
                                                           filename, ex)
            raise ArchiveInterfaceError()

    def put(self, env, start_response):
        """Saves a file passed in the request"""
        myfile = None
        backend_type = self._backend_type
        prefix = self._prefix
        path_info = un_abs_path(env['PATH_INFO'])
        resp = archive_interface_responses.Responses()
        stderr.flush()

        try:
            filename = path.join(prefix, self.path_info_munge(path_info))
        except Exception as ex:
            self._response = resp.munging_filepath_exception(start_response,
                                                             backend_type,
                                                             path_info, ex)
            raise ArchiveInterfaceError()
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

            self._response = resp.successful_put_response(start_response,
                                                          env['CONTENT_LENGTH'])

        except Exception as ex:
            self._response = resp.error_opening_file_exception(start_response,
                                                               filename)
            raise ArchiveInterfaceError()

        myfile.close()
        myfile = None
        return self.return_response()

    def status(self, env, start_response):
        """Gets the status of a file passed in the request"""
        myfile = None
        status = None
        backend_type = self._backend_type
        prefix = self._prefix
        path_info = un_abs_path(env['PATH_INFO'])
        resp = archive_interface_responses.Responses()
        stderr.flush()
        try:
            filename = path.join(prefix, self.path_info_munge(path_info))
        except Exception as ex:
            self._response = resp.munging_filepath_exception(start_response,
                                                             backend_type,
                                                             path_info, ex)
            raise ArchiveInterfaceError()
        try:
            myfile = self.backend_open(filename, "r")
        except Exception as ex:
            self._response = resp.file_not_found_exception(start_response,
                                                           filename, ex)
            raise ArchiveInterfaceError()
        try:
            status = myfile.status()
            if (isinstance(status, POSIXStatus) or
                    isinstance(status, HPSSStatus)):
                self._response = resp.file_status(start_response, filename,
                                                  status)
            else:
                self._response = resp.file_unknown_status(start_response,
                                                          filename)


        except Exception as ex:
            self._response = resp.file_status_exception(start_response,
                                                        filename, ex)
            raise ArchiveInterfaceError()

        myfile.close()
        myfile = None
        return self.return_response()

    def stage(self, env, start_response):
        """Stage the file to disk"""
        myfile = None
        backend_type = self._backend_type
        prefix = self._prefix
        path_info = un_abs_path(env['PATH_INFO'])
        resp = archive_interface_responses.Responses()
        stderr.flush()
        try:
            filename = path.join(prefix, self.path_info_munge(path_info))
        except Exception as ex:
            self._response = resp.munging_filepath_exception(start_response,
                                                             backend_type,
                                                             path_info, ex)
            raise ArchiveInterfaceError()
        try:
            myfile = self.backend_open(filename, "r")
        except Exception as ex:
            self._response = resp.file_not_found_exception(start_response,
                                                           filename, ex)
            raise ArchiveInterfaceError()
        try:
            myfile.stage()
            self._response = resp.file_stage(start_response, filename)

        except Exception as ex:
            self._response = resp.file_stage_exception(start_response,
                                                       filename, ex)
            raise ArchiveInterfaceError()
        myfile.close()
        myfile = None
        return self.return_response()


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

    def return_response(self):
        """Prints all responses in a nice fashion"""
        return dumps(self._response, sort_keys=True, indent=4)


    def pacifica_archiveinterface(self, env, start_response):
        """Parses request method type"""
        try:
            if env['REQUEST_METHOD'] == 'GET':
                return self.get(env, start_response)
            elif env['REQUEST_METHOD'] == 'PUT':
                return self.put(env, start_response)
            elif env['REQUEST_METHOD'] == 'HEAD':
                return self.status(env, start_response)
            elif env['REQUEST_METHOD'] == 'POST':
                return self.stage(env, start_response)
            else:
                resp = archive_interface_responses.Responses()
                self._response = resp.unknown_request(start_response,
                                                      env['REQUEST_METHOD'])
            return self.return_response()
        except ArchiveInterfaceError:
            #catching application errors
            #all exceptions set the return response
            #if the response is not set, set it as unknown
            if self._response is None:
                resp = archive_interface_responses.Responses()
                self._response = resp.unknown_exception(start_response)
            return self.return_response()


if __name__ == "__main__":
    doctest.testmod(verbose=True)

