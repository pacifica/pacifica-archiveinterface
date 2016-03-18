# Pacifica Archive Interface
[![Build Status](https://travis-ci.org/EMSL-MSC/pacifica-archiveinterface.svg?branch=master)](https://travis-ci.org/EMSL-MSC/pacifica-archiveinterface)

This code is to provide the archive interface for the rest of the
Pacifica code base. This code consists of some very specific algorithms
and APIs to support data that might exist on tape or spinning disk.

# Building and Installing

This code depends on the following libraries and python modules:

HPSS Client 7.4.1p2
Python JSON
Python CTypes
Python DocTest

This is a standard python distutils build process.

```
python ./setup.py build
python ./setup.py install
```

# Running It

There are two ways of running the archive interface; POSIX and HPSS.

Posix File System Backend
```
python ./scripts/server.py -t posix -p 8080 -a 127.0.0.1 --prefix /path
```
HPSS Archive Backend
```
python ./scripts/server.py -t hpss -u hpss.unix --auth /var/hpss/etc/hpss.unix.keytab -p 8080 -a 127.0.0.1 --prefix /path
```

# API Examples

## Put a File

The path in the URL should be only an integer specifying a unique 
file in the archive. Sending a different file to the same URL will
over-write the contents of the previous file. Setting the Last-
Modified header sets the mtime of the file in the archive and is
required.

```
curl -X PUT -H 'Last-Modified: Sun, 06 Nov 1994 08:49:37 GMT' --upload-file /tmp/foo.txt http://127.0.0.1:8080/1
```

Sample output:
```
{
    "message": "Thanks for the data", 
    "total_bytes": "24"
}
```

## Get a File
The HTTP `GET` method is used to get the contents
of the specified file.
```
curl -o /tmp/foo.txt http://127.0.0.1:8080/1
```
Sample output (without -o option):
"Document Contents"

## Status a File

The HTTP ```HEAD``` method is used to get a JSON document describing the
status of the file. The status includes, but is not limited to, the
size, mtime, ctime, whether its on disk or tape.
```
curl -X HEAD http://127.0.0.1:8080/1
```
Sample output:
```
{
    "bytes_per_level": "(24L, 0L, 0L, 0L, 0L)", 
    "ctime": "1444938166", 
    "file": "/myemsl-dev/bundle/file.1", 
    "file_storage_media": "disk", 
    "filesize": "24", 
    "message": "File was found", 
    "mtime": "1444938166"
}
```

## Stage a File
The HTTP `POST` method is used to stage a file for use.  In posix this
equates to a no-op on hpss it stages the file to the disk drive.

```
curl -X POST http://127.0.0.1:8080/1
```

Sample Output:
```
{
    "file": "/myemsl-dev/bundle/file.1", 
    "message": "File was staged"
}
```
