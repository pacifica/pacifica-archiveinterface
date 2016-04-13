"""Module that Extends the functionality of the base file object
    to import: import ExtendedFile
       or from extendedfile import ExtendedFile
    to invoke: ExtendedFile(path, mode)
"""

import os

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
        status = POSIXStatus(mtime, ctime, bytes_per_level, filesize)

        return status
    def stage(self):
        """Stages a file. Since POSIX, essentially a no op"""
        self._staged = True

    def set_mod_time(self, mod_time):
        """sets the last modified time on the file"""
        os.utime(self._path, (mod_time, mod_time))


class POSIXStatus(object):
    """Class for handling posix status pieces
    needs mtime,ctime, bytes per level array
    """
    _disk = "disk"
    def __init__(self, mtime, ctime, bytes_per_level, filesize):
        self.mtime = mtime
        self.ctime = ctime
        self.bytes_per_level = bytes_per_level
        self.filesize = filesize
        self.defined_levels = self.define_levels()
        self.file_storage_media = self.find_file_storage_media()

    def find_file_storage_media(self):
        """Get the file storage media.  Showed always be disk for posix"""
        level_array = self.defined_levels
        disk_level = 0
        return level_array[disk_level]

    def define_levels(self):
        """Sets up what each level definition means"""
        #This defines posix integer levels.  Always disk
        type_per_level = [self._disk]
        return type_per_level
