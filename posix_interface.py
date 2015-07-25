#!/usr/bin/python

block_size = 1<<12

def myemsl_archiveinterface(env, start_response):
    if env['REQUEST_METHOD'] == 'GET':
        myfile = open("/myemsldev%s"%(env['PATH_INFO']), "r")
        start_response('200 OK', [('Content-Type','application/octet-stream')])
        if 'wsgi.file_wrapper' in env:
            return env['wsgi.file_wrapper'](myfile, block_size)
        else:
            return iter(lambda: myfile.read(block_size), '')
    else:
        start_response('200 OK', [('Content-Type','text/html')])
    return ""

