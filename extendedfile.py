"""Module that Extends the functionality of the base file object
    to import: import ExtendedFile
       or from extendedfile import ExtendedFile
    to invoke: ExtendedFile(path, mode)
"""
class ExtendedFile(file):
    """Extending default file stuct to support additional methods"""
    def __init__(self, path, mode):
        file.__init__(self, path, mode)

    @classmethod
    def status(cls):
        """Returns status of file. Since POSIX, will always return disk"""
        return "disk"
