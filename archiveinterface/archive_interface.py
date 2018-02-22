#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Class for the archive interface.

Allows API to file interactions for passed in archive backends.
"""
import json
import cherrypy
from archiveinterface.archive_utils import get_http_modified_time
from archiveinterface.archive_interface_error import ArchiveInterfaceError
import archiveinterface.archive_interface_responses as interface_responses

BLOCK_SIZE = 1 << 20


class ArchiveInterfaceGenerator(object):
    """Archive Interface Generator.

    Defines the methods that can be used on files for request types.
    """

    def __init__(self, archive):
        """Create an archive interface generator."""
        self._archive = archive
        self._response = None
        print 'Pacifica Archive Interface Up and Running'

    def GET(self, *args):
        """Get a file from WSGI request.

        Gets a file specified in the request and writes back the data.
        """
        archivefile = None
        # if asking for / then return a message that the archive is working
        if not args:
            cherrypy.response.headers['Content-Type'] = 'application/json'
            return {'message': 'Pacifica Archive Interface Up and Running'}
        archivefile = self._archive.open(args[0], 'r')
        cherrypy.response.headers['Content-Type'] = 'application/octet-stream'

        def read():
            """Read the data from the file."""
            buf = archivefile.read(BLOCK_SIZE)
            while buf:
                yield buf
                buf = archivefile.read(BLOCK_SIZE)
        return read()

    @cherrypy.tools.json_out()
    def PUT(self, filepath):
        """Write a file from WSGI requests.

        Writes a file passed in the request to the archive.
        """
        archivefile = None
        resp = interface_responses.Responses()
        path_info = env['PATH_INFO']
        mod_time = get_http_modified_time(cherrypy.request.headers)
        stderr.flush()
        archivefile = self._archive.open(path_info, 'w')
        try:
            content_length = int(env['CONTENT_LENGTH'])
        except Exception as ex:
            raise ArchiveInterfaceError(
                "Can't get file content length with error: {}".format(str(ex))
            )
        while content_length > 0:
            if content_length > BLOCK_SIZE:
                buf = env['wsgi.input'].read(BLOCK_SIZE)
            else:
                buf = env['wsgi.input'].read(content_length)
            archivefile.write(buf)
            content_length -= len(buf)

        self._response = resp.successful_put_response(start_response,
                                                      env['CONTENT_LENGTH'])
        archivefile.close()
        archivefile.set_mod_time(mod_time)
        archivefile.set_file_permissions()
        return self.return_response()

    def HEAD(self, env, start_response):
        """Get the file status from WSGI request.

        Gets the status of a file specified in the request.
        """
        archivefile = None
        path_info = env['PATH_INFO']
        resp = interface_responses.Responses()
        stderr.flush()
        archivefile = self._archive.open(path_info, 'r')
        status = archivefile.status()
        self._response = resp.file_status(start_response, status)
        archivefile.close()
        return self.return_response()

    def POST(self, env, start_response):
        """Stage a file from WSGI request.

        Stage the file specified in the request to disk.
        """
        archivefile = None
        path_info = env['PATH_INFO']
        resp = interface_responses.Responses()
        stderr.flush()
        archivefile = self._archive.open(path_info, 'r')
        archivefile.stage()
        self._response = resp.file_stage(start_response, path_info)
        archivefile.close()
        return self.return_response()

    def PATCH(self, env, start_response):
        """Move a file from the original path to the new one specified."""
        resp = interface_responses.Responses()
        try:
            request_body_size = int(env.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0
        try:
            request_body = env['wsgi.input'].read(request_body_size)
            data = json.loads(request_body)
            file_path = data['path']
            file_id = env['PATH_INFO']
        except (IOError, ValueError):
            # is exception is probably from the read()
            self._response = resp.json_patch_error_response(start_response)
            return self.return_response()
        stderr.flush()
        self._archive.patch(file_id, file_path)
        self._response = resp.file_patch(start_response)
        return self.return_response()

    def return_response(self):
        """Print all responses in a nice fashion."""
        return json.dumps(self._response, sort_keys=True, indent=4)
