#!/usr/bin/python
"""Module that implements the Abstract Status class.

For the oracle hms sideband archive backend type.
"""

from ..abstract.abstract_status import AbstractStatus


class HmsSidebandStatus(AbstractStatus):
    """Class for handling hmsSideband status pieces.

    Needs mtime,ctime, bytes per level array
    """

    _disk = 'disk'
    _tape = 'tape'

    def __init__(self, mtime, ctime, bytes_per_level, filesize):
        """Constructor to build the object."""
        super(HmsSidebandStatus, self).__init__(
            mtime,
            ctime,
            bytes_per_level,
            filesize
        )
        self.mtime = mtime
        self.ctime = ctime
        self.bytes_per_level = bytes_per_level
        self.filesize = filesize
        self.filepath = None
        self.defined_levels = self.define_levels()
        self.file_storage_media = self.find_file_storage_media()

    def find_file_storage_media(self):
        """Get the file storage media.

        Should always be disk for hmsSideband.
        """
        level_array = self.defined_levels
        ret_val = None
        if self.bytes_per_level[0] == self.filesize:
            ret_val = level_array[0]
        else:
            ret_val = level_array[1]
        return ret_val

    def define_levels(self):
        """Set up what each level definition means."""
        # This defines hmsSideband integer levels.  First level disk, second is tape
        type_per_level = [self._disk, self._tape]
        return type_per_level

    def set_filepath(self, filepath):
        """Set the filepath that the status is for."""
        self.filepath = filepath
