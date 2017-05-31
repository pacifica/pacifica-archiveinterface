#!/usr/bin/python
"""Extended File Object Module.

Module that Extends the functionality of the base file object

to import:

>>> import ExtendedFile
>>> from extendedfile import ExtendedFile
>>> ExtendedFile(path, mode)
"""
import os
from archiveinterface.archivebackends.posix.posix_status import PosixStatus


class ExtendedFile(file):
    """Extending default file stuct to support additional methods."""

    def __init__(self, filepath, mode):
        """Set some additional attributes to support staging."""
        file.__init__(self, filepath, mode)
        self._path = filepath
        self._staged = True

    def status(self):
        """Return status of file. Since POSIX, will always return disk."""
        mtime = os.path.getmtime(self._path)
        ctime = os.path.getctime(self._path)
        bytes_per_level = (long(os.path.getsize(self._path)),)
        filesize = os.path.getsize(self._path)
        status = PosixStatus(mtime, ctime, bytes_per_level, filesize)
        status.set_filepath(self._path)

        return status

    def stage(self):
        """Stage a file. Since POSIX, essentially a no op."""
        self._staged = True

    def set_mod_time(self, mod_time):
        """Set the last modified time on the file."""
        os.utime(self._path, (mod_time, mod_time))

    def set_file_permissions(self):
        """Set the last modified time on the file."""
        os.chmod(self._path, 0444)
