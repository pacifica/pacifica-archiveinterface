def munging_filepath_exception(start_response, backend_type, path):
	start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
	res = {
		'message': 'Error with Munging filepath for backend type %s and path %s' %(backend_type, path)
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