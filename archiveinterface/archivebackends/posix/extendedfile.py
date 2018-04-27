#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Extended File Object Module.

Module that Extends the functionality of the base file object

to import:

>>> import ExtendedFile
>>> from extendedfile import ExtendedFile
>>> ExtendedFile(path, mode)
"""
import os
from archiveinterface.archive_utils import file_type, int_type
from archiveinterface.archivebackends.posix.posix_status import PosixStatus


class ExtendedFile(file_type):
    """Extending default file stuct to support additional methods."""

    def __init__(self, filepath, mode):
        """Set some additional attributes to support staging."""
        file_type.__init__(self, filepath, mode)
        self._path = filepath
        self._staged = True

    def status(self):
        """Return status of file. Since POSIX, will always return disk."""
        mtime = os.path.getmtime(self._path)
        ctime = os.path.getctime(self._path)
        bytes_per_level = (int_type(os.path.getsize(self._path)),)
        filesize = os.path.getsize(self._path)
        status = PosixStatus(mtime, ctime, bytes_per_level, filesize)
        status.set_filepath(self._path)

        return status

    def stage(self):
        """Stage a file. Since POSIX, essentially a no op."""
        self._staged = True
