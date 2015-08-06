def munging_filepath_exception(start_response, backend_type, path):
	start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
	res = {
		'message': 'Error with Munging filepath',
		'backend': backend_type,
		'path': path
	}
	return res

def file_not_found_exception(start_response, filename):
	start_response('404 Not Found', [('Content-Type', 'application/json')])
	res = {
		'message': 'File not found',
		'file': str(filename)
	}
	return res

def successful_put_response(start_response, total_bytes):
	start_response('200 OK', [('Content-Type', 'application/json')])
	res = {
		'message': 'Thanks for the data',
		'total_bytes': total_bytes
	}
	return res

def error_opening_file_exception(start_response, filename):
	start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
	res = {
		'message': 'Error opening file',
		'file': str(filename)
	}
	return res

def unknown_request(start_response, requestMethod):
	start_response('200 OK', [('Content-Type', 'application/json')])
	res = {
		'message': 'Unknown request method',
		'request_method': requestMethod
	}
	return res

def file_disk_status(start_response, filename):
	start_response('200 OK', [('Content-Type', 'application/json')])
	res = {
		'message': 'File was found on Disk',
		'file': str(filename)
	}
	return res

def file_tape_status(start_response, filename):
	start_response('200 OK', [('Content-Type', 'application/json')])
	res = {
		'message': 'File was found on Tape',
		'file': str(filename)
	}
	return res

def file_unknown_status(start_response, filename):
	start_response('200 OK', [('Content-Type', 'application/json')])
	res = {
		'message': 'File has an unknown status',
		'file': str(filename)
	}
	return res

def file_status_exception(start_response, filename):
	start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
	res = {
		'message': 'Error getting file status',
		'file': str(filename)
	}
	return res