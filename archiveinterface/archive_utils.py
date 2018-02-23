#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Group of utility functions.

Used in various parts of the archive interface.
"""
import email.utils as eut
import time
import ConfigParser
from os import path
from archiveinterface.archive_interface_error import ArchiveInterfaceError

# defaulting to this, but the global is set in the archiveinterfaceserver if different
# looks at command line first, then environment, and then falls back to config.cfg
CONFIG_FILE = 'config.cfg'


def file_status(status, response):
    """Response for when file is on the hpss system."""
    response_headers = [
        ('X-Pacifica-Messsage', 'File was found' if status else 'File Not found'),
        ('X-Pacifica-File', str(getattr(status, 'filepath', 'File Not Found'))),
        ('X-Content-Length', str(getattr(status, 'filesize', 'File Not Found'))),
        ('Last-Modified', str(getattr(status, 'mtime', 'File Not Found'))),
        ('X-Pacifica-Ctime', str(getattr(status, 'ctime', 'File Not Found'))),
        (
            'X-Pacifica-Bytes-Per-Level',
            str(getattr(status, 'bytes_per_level', 'File Not Found'))
        ),
        (
            'X-Pacifica-File-Storage-Media',
            str(getattr(status, 'file_storage_media', 'File Not Found'))
        ),
        ('Content-Type', 'application/json')
    ]
    response.status = '204 No Content' if status else '404 Not Found'
    for key, value in response_headers:
        response.headers[key] = value


def un_abs_path(path_name):
    """Remove absolute path piece."""
    try:
        if path.isabs(path_name):
            path_name = path_name[1:]
        return path_name
    except (AttributeError, TypeError) as ex:
        raise ArchiveInterfaceError('Cant remove absolute path: ' + str(ex))


def get_http_modified_time(env):
    """Get the modified time from the request in unix timestamp.

    Returns current time if no time was passed.
    """
    try:
        mod_time = None
        if 'HTTP_LAST_MODIFIED' in env:
            mod_time = eut.mktime_tz(
                eut.parsedate_tz(env['HTTP_LAST_MODIFIED']))
        else:
            mod_time = time.time()
        return mod_time
    except (TypeError, IndexError, AttributeError) as ex:
        raise ArchiveInterfaceError('Cant parse the files modtime: ' + str(ex))


def set_config_name(name):
    """Set the global config name."""
    # pylint: disable=global-statement
    global CONFIG_FILE
    # pylint: enable=global-statement
    CONFIG_FILE = name


def read_config_value(section, field):
    """Read the value from the config file if exists."""
    try:
        config = ConfigParser.RawConfigParser()
        dataset = config.read(CONFIG_FILE)
        if not dataset:
            raise ValueError(
                'Failed to open config file with name: {}'.format(str(CONFIG_FILE)))
        value = config.get(section, field)
        return value
    except ConfigParser.NoSectionError:
        raise ArchiveInterfaceError(
            'Error reading config file, no section: ' + section)
    except ConfigParser.NoOptionError:
        raise ArchiveInterfaceError('Error reading config file, no field: ' + field +
                                    ' in section: ' + section)
