"""File for setting up Archive Interface server responses"""
def munging_filepath_exception(start_response, backend_type, path):
    """Response for when there is an error getting the filepath"""
    start_response(
        '500 Internal Server Error',
        [('Content-Type', 'application/json')])
    res = {
        'message': 'Error with Munging filepath',
        'backend': backend_type,
        'path': path
    }
    return res

def file_not_found_exception(start_response, filename):
    """Response for when the file specified does not exists"""
    start_response('404 Not Found', [('Content-Type', 'application/json')])
    res = {
        'message': 'File not found',
        'file': str(filename)
    }
    return res

def successful_put_response(start_response, total_bytes):
    """Response on a successful put"""
    start_response('200 OK', [('Content-Type', 'application/json')])
    res = {
        'message': 'Thanks for the data',
        'total_bytes': total_bytes
    }
    return res

def error_opening_file_exception(start_response, filename):
    """Response for when the file specified cant be opened"""
    start_response(
        '500 Internal Server Error',
        [('Content-Type', 'application/json')])
    res = {
        'message': 'Error opening file',
        'file': str(filename)
    }
    return res

def unknown_request(start_response, request_method):
    """Response for when unknow request type given"""
    start_response('200 OK', [('Content-Type', 'application/json')])
    res = {
        'message': 'Unknown request method',
        'request_method': request_method
    }
    return res

def file_disk_status(start_response, filename):
    """Response for when file is found on disk"""
    start_response('200 OK', [('Content-Type', 'application/json')])
    res = {
        'message': 'File was found on Disk',
        'file': str(filename)
    }
    return res

def file_tape_status(start_response, filename):
    """Response for when the file is found on tape"""
    start_response('200 OK', [('Content-Type', 'application/json')])
    res = {
        'message': 'File was found on Tape',
        'file': str(filename)
    }
    return res

def file_unknown_status(start_response, filename):
    """Response for an unknown file status"""
    start_response('200 OK', [('Content-Type', 'application/json')])
    res = {
        'message': 'File has an unknown status',
        'file': str(filename)
    }
    return res

def file_status_exception(start_response, filename):
    """Response when there is an error getting the status"""
    start_response(
        '500 Internal Server Error',
        [('Content-Type', 'application/json')])
    res = {
        'message': 'Error getting file status',
        'file': str(filename)
    }
    return res
