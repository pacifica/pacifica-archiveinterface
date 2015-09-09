# MyEMSL Archive Interface

This code is to provide the archive interface for the rest of the
MyEMSL code base. This code consists of some very specific algorithms
and APIs to support data that might exist on tape or spinning disk.

# Building and Installing

This code depends on the following libraries and python modules:

HPSS Client 7.4.1p2
Python JSON
Python CTypes
Python DocTest

This is a standard python distutils build process.

`python ./setup.py build`
`python ./setup.py install`

# Running It

There are two ways of running the archive interface; POSIX and HPSS.

`python ./scripts/server.py -t posix -p 8080 -a 127.0.0.1`
`python ./scripts/server.py -t hpss -u hpss.unix --auth /var/hpss/etc/hpss.unix.keytab -p 8080 -a 127.0.0.1`

# API Examples

## Put a File

The path in the URL should be only an integer specifying a unique 
file in the archive. Sending a different file to the same URL will
over-write the contents of the previous file.

`curl -X PUT --upload-file /tmp/foo.txt http://127.0.0.1:8080/1`

## Get a File

`curl -o /tmp/foo.txt http://127.0.0.1:8080/1`

## Status a File

The HTTP `HEAD` method is used to get a JSON document describing the
status of the file. The status includes, but is not limited to, the
size, mtime, ctime, whether its on disk or tape.

`curl -X HEAD http://127.0.0.1:8080/1`
```
EXAMPLE CONTENT HERE
```
