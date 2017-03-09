#!/usr/bin/python
"""Module that implements the abstract_backend_archive class for a posix
backend"""

import os
from archiveinterface.archive_utils import un_abs_path
from archiveinterface.archive_interface_error import ArchiveInterfaceError
from archiveinterface.archivebackends.posix.extendedfile import ExtendedFile
from archiveinterface.archivebackends.abstract.abstract_backend_archive \
    import AbstractBackendArchive

class PosixBackendArchive(AbstractBackendArchive):
    """Class that implements the abstract base class for the posix
    archive interface backend"""
    def __init__(self, prefix):
        super(PosixBackendArchive, self).__init__(prefix)
        self._prefix = prefix
        self._file = None

    def open(self, filepath, mode):
        """Open a posix file"""
        #want to close any open files first
        try:
            if self._file:
                self.close()
        except ArchiveInterfaceError as ex:
            err_str = "Can't close previous posix file before opening new "\
                      "one with error: " + str(ex)
            raise ArchiveInterfaceError(err_str)
        try:
            fpath = un_abs_path(filepath)
            filename = os.path.join(self._prefix, fpath)
            self._file = ExtendedFile(filename, mode)
            return self
        except Exception as ex:
            err_str = "Can't open posix file with error: " + str(ex)
            raise ArchiveInterfaceError(err_str)

    def close(self):
        """Close a posix file"""
        try:
            if self._file:
                self._file.close()
                self._file = None
        except Exception as ex:
            err_str = "Can't close posix file with error: " + str(ex)
            raise ArchiveInterfaceError(err_str)

    def read(self, blocksize):
        """Read a posix file"""
        try:
            if self._file:
                return self._file.read(blocksize)
        except Exception as ex:
            err_str = "Can't read posix file with error: " + str(ex)
            raise ArchiveInterfaceError(err_str)

    def write(self, buf):
        """Write a posix file to the archive"""
        try:
            if self._file:
                return self._file.write(buf)
        except Exception as ex:
            err_str = "Can't write posix file with error: " + str(ex)
            raise ArchiveInterfaceError(err_str)

    def set_mod_time(self, mod_time):
        """Set the mod time on a posix file"""
        try:
            if self._file:
                self._file.set_mod_time(mod_time)
        except Exception as ex:
            err_str = "Can't set posix file mod time with error: " + str(ex)
            raise ArchiveInterfaceError(err_str)

    def stage(self):
        """Stage a posix file (no-opt essentially)"""
        try:
            if self._file:
                return self._file.stage()
        except Exception as ex:
            err_str = "Can't stage posix file with error: " + str(ex)
            raise ArchiveInterfaceError(err_str)

    def status(self):
        """Get the status of a posix file"""
        try:
            if self._file:
                return self._file.status()
        except Exception as ex:
            err_str = "Can't get posix file status with error: " + str(ex)
            raise ArchiveInterfaceError(err_str)
