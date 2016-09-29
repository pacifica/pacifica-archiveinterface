#!/usr/bin/python
"""Module that Extends the functionality of the base file object
    to import: import ExtendedFile
       or from extendedfile import ExtendedFile
    to invoke: ExtendedFile(path, mode)
"""
import os
from archiveinterface.archivebackends.posix.posix_status import PosixStatus

class ExtendedFile(file):
    """Extending default file stuct to support additional methods"""
    def __init__(self, filepath, mode):
        file.__init__(self, filepath, mode)
        self._path = filepath
        self._staged = True

    def status(self):
        """Returns status of file. Since POSIX, will always return disk"""

        mtime = os.path.getmtime(self._path)
        ctime = os.path.getctime(self._path)
        bytes_per_level = (long(os.path.getsize(self._path)),)
        filesize = os.path.getsize(self._path)
        status = PosixStatus(mtime, ctime, bytes_per_level, filesize)
        status.set_filepath(self._path)

        return status

    def stage(self):
        """Stages a file. Since POSIX, essentially a no op"""
        self._staged = True

    def set_mod_time(self, mod_time):
        """sets the last modified time on the file"""
        os.utime(self._path, (mod_time, mod_time))
