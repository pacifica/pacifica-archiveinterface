#!/usr/bin/python
"""File for setting up Archive Interface server responses"""
class Responses(object):
    """Class to support the archive interface exceptions"""

    def __init__(self):
        self._response = None


    def unknown_request(self, start_response, request_method):
        """Response for when unknown request type given"""
        start_response(
            '400 Bad Request',
            [('Content-Type', 'application/json')]
        )
        self._response = {
            'message': 'Unknown request method',
            'request_method': request_method
        }
        return self._response

    def unknown_exception(self, start_response):
        """Response when unknown exception occurs"""
        start_response(
            '500 Internal Server Error',
            [('Content-Type', 'application/json')]
        )
        self._response = {
            'message': 'Unknown Exception Occured'
        }
        return self._response

    def successful_put_response(self, start_response, total_bytes):
        """Response on a successful put"""
        start_response('200 OK', [('Content-Type', 'application/json')])
        self._response = {
            'message': 'Thanks for the data',
            'total_bytes': total_bytes
        }
        return self._response

    def file_stage(self, start_response, filename):
        """Response for when file is on the hpss system"""
        start_response('200 OK', [('Content-Type', 'application/json')])
        self._response = {
            'message': 'File was staged',
            'file': str(filename)
        }
        return self._response

    def file_status(self, start_response, status):
        """Response for when file is on the hpss system"""

        self._response = ''
        response_headers = [
            ('X-Pacifica-Messsage', 'File was found'),
            ('X-Pacifica-File', str(status.filepath)),
            ('Content-Length', str(status.filesize)),
            ('Last-Modified', str(status.mtime)),
            ('X-Pacifica-Ctime', str(status.ctime)),
            ('X-Pacifica-Bytes-Per-Level', str(status.bytes_per_level)),
            ('X-Pacifica-File-Storage-Media', str(status.file_storage_media)),
            ('Content-Type', 'application/json')
        ]
        start_response('200 OK', response_headers)
        return self._response

    def archive_exception(self, start_response, ex):
        """Response when unknown exception occurs"""
        start_response(
            '500 Internal Server Error',
            [('Content-Type', 'application/json')]
        )
        self._response = {
            'message': str(ex)
        }
        return self._response
