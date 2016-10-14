#!/usr/bin/python
"""Converts an integer id to a filepath for storage system"""

import sys

def id2dirandfilename(fileid):
    """Algorithm for getting filepath from an integer id"""
    hexfileid = "%x" %(fileid)
    directories = ""
    while len(hexfileid) > 2:
        directories = "%s/%s" %(directories, hexfileid[-2:])
        hexfileid = hexfileid[:-2]
    if directories == "":
        filename = "file.%s" %(hexfileid)
        filepath = "/%s" %(filename)
        directories = "/"
    else:
        filename = "%x" %(fileid)
        filepath = "%s/%s" %(directories, filename)
    return filepath

def id2filename(fileid):
    """will return the filepath associated to passed fileid"""
    return id2dirandfilename(fileid)

if __name__ == '__main__': # pragma: no cover
    print id2filename(int(sys.argv[1]))
