"""File for setting up Archive Interface server responses"""
class Responses(object):
    """Method to support the archive interface exceptions"""
    def munging_filepath_exception(self, start_response,
                                   backend_type, path, ex):
        """Response for when there is an error getting the filepath"""
        start_response(
            '500 Internal Server Error',
            [('Content-Type', 'application/json')])
        self._response = {
            'message': 'Error with Munging filepath',
            'backend': backend_type,
            'path': path,
            'exception': str(ex)
        }
        return self._response

    def file_not_found_exception(self, start_response, filename, ex):
        """Response for when the file specified does not exists"""
        start_response('404 Not Found', [('Content-Type', 'application/json')])
        self._response = {
            'message': 'File not found',
            'file': str(filename),
            'exception': str(ex)
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

    def error_opening_file_exception(self, start_response, filename):
        """Response for when the file specified cant be opened"""
        start_response(
            '500 Internal Server Error',
            [('Content-Type', 'application/json')])
        self._response = {
            'message': 'Error opening file',
            'file': str(filename)
        }
        return self._response

    def unknown_request(self, start_response, request_method):
        """Response for when unknown request type given"""
        start_response('200 OK', [('Content-Type', 'application/json')])
        self._response = {
            'message': 'Unknown request method',
            'request_method': request_method
        }
        return self._response

    def unknown_exception(self, start_response):
        """Response when unknown exception occurs"""
        start_response('200 OK', [('Content-Type', 'application/json')])
        self._response = {
            'message': 'Unknown Exception Occured'
        }
        return self._response

    def file_disk_status(self, start_response, filename):
        """Response for when file is found on disk"""
        start_response('200 OK', [('Content-Type', 'application/json')])
        self._response = {
            'message': 'File was found on Disk',
            'file': str(filename)
        }
        return self._response

    def file_status(self, start_response, filename, status):
        """Response for when file is on the hpss system"""
        start_response('200 OK', [('Content-Type', 'application/json')])
        self._response = {
            'message': 'File was found',
            'file': str(filename),
            'filesize': str(status.filesize),
            'mtime': str(status.mtime),
            'ctime': str(status.ctime),
            'bytes_per_level': str(status.bytes_per_level),
            'file_storage_media': str(status.file_storage_media)
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

    def file_tape_status(self, start_response, filename):
        """Response for when the file is found on tape"""
        start_response('200 OK', [('Content-Type', 'application/json')])
        self._response = {
            'message': 'File was found on Tape',
            'file': str(filename)
        }
        return self._response

    def file_unknown_status(self, start_response, filename):
        """Response for an unknown file status"""
        start_response('200 OK', [('Content-Type', 'application/json')])
        self._response = {
            'message': 'File has an unknown status type',
            'file': str(filename)
        }
        return self._response

    def file_status_exception(self, start_response, filename, ex):
        """Response when there is an error getting the status"""
        start_response(
            '500 Internal Server Error',
            [('Content-Type', 'application/json')])
        self._response = {
            'message': 'Error getting file status',
            'file': str(filename),
            'exception': str(ex)
        }
        return self._response

    def file_stage_exception(self, start_response, filename, ex):
        """Response when there is an error getting the status"""
        start_response(
            '500 Internal Server Error',
            [('Content-Type', 'application/json')])
        self._response = {
            'message': 'Error with file stage',
            'file': str(filename),
            'exception': str(ex)
        }
        return self._response

    def http_modtime_exception(self, start_response):
        """Response when there is an error getting mtime on passed file"""
        start_response(
            '500 Internal Server Error',
            [('Content-Type', 'application/json')])
        self._response = {
            'message': 'Error with getting HTTP file mtime'
        }
        return self._response

    def __init__(self):
        self._response = None
