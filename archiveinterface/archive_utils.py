#!/usr/bin/python
"""Group of utility functions that are used in various parts of the
archive interface """
import email.utils as eut
import time
from os import path
from archiveinterface.archive_interface_error import ArchiveInterfaceError

def un_abs_path(path_name):
    """Removes absolute path piece"""
    try:
        if path.isabs(path_name):
            path_name = path_name[1:]
        return path_name
    except Exception as ex:
        raise ArchiveInterfaceError("Cant remove absolute path: " + str(ex))

def get_http_modified_time(env):
    """Gets the modified time from the request in unix timestamp.
    Returns current time if no time was passed"""
    try:
        mod_time = None
        if 'HTTP_LAST_MODIFIED' in env:
            mod_time = eut.mktime_tz(eut.parsedate_tz(env['HTTP_LAST_MODIFIED']))
        else:
            mod_time = time.time()
        return mod_time
    except Exception as ex:
        raise ArchiveInterfaceError("Cant parse the files modtime: " + str(ex))
