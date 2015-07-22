#!/usr/bin/python

from hpss_ctypes import HPSSClient, HPSSFile

CLIENT = HPSSClient(user="svc-myemsldev", auth="/home/dmlb2000/svc-myemsldev.keytab")
block_size = 1<<12

def myemsl_archiveinterface(env, start_response):
    if env['REQUEST_METHOD'] == 'GET':
        myfile = CLIENT.open("/myemsldev%s"%(env['PATH_INFO']), "r")
        start_response('200 OK', [('Content-Type','application/octet-stream')])
        if 'wsgi.file_wrapper' in env:
            return env['wsgi.file_wrapper'](myfile, block_size)
        else:
            return iter(lambda: myfile.read(block_size), '')
    else:
        start_response('200 OK', [('Content-Type','text/html')])
    return ""

def myemsl_test(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [ "%s=%s\n"%(k,env[k]) for k in env.keys() ]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, myemsl_archiveinterface)
    srv.serve_forever()
