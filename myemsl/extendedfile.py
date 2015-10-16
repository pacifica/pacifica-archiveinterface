"""Module that Extends the functionality of the base file object
    to import: import ExtendedFile
       or from extendedfile import ExtendedFile
    to invoke: ExtendedFile(path, mode)
"""

from os import path

class ExtendedFile(file):
    """Extending default file stuct to support additional methods"""
    def __init__(self, filepath, mode):
        file.__init__(self, filepath, mode)
        self._path = filepath
        self._staged = True

    def status(self):
        """Returns status of file. Since POSIX, will always return disk"""

        mtime = path.getmtime(self._path)
        ctime = path.getctime(self._path)
        bytes_per_level = (long(path.getsize(self._path)),)
        filesize = path.getsize(self._path)
        status = POSIXStatus(mtime, ctime, bytes_per_level, filesize)

        return status
    def stage(self):
        """Stages a file. Since POSIX, essentially a no op"""
        self._staged = True


class POSIXStatus(object):
    """Class for handling posix status pieces
    needs mtime,ctime, bytes per level array
    >>> status = POSIXStatus(42, 33, [33,36,22], 36)
    >>> type(status)
    <class '__main__.POSIXStatus'>
    >>> status.file_storage_media
    'disk'
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

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
