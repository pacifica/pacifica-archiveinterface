#!/usr/bin/python
"""Factory for returning a Archive backend. New Backends must be added to the
__share_classes list and that class needs to be imported in

Call the factory like the following:
FACTORY = ArchiveBackendFactory()
BACKEND = FACTORY.get_backend_archive(type, prefix, user, auth)
"""


class ArchiveBackendFactory(object):
    """Factory Class for Archive Backends """
    share_classes = {}

    def get_backend_archive(self, name, prefix, user, auth):
        """Method for creating an instance of the backend archive. """
        self.load_backend_archive(name)
        backend_class = self.share_classes.get(name.lower(), None)

        if backend_class:
            return backend_class(prefix, user, auth)
        raise NotImplementedError("The requested Archive Backend has not "\
            "been implemented")

    def load_backend_archive(self, name):
        """Method for loading in the correct backend type. Only want to
        load backend type being used"""
        if name == "hpss":
            from archiveinterface.archivebackends.hpss.hpss_backend_archive \
                import HpssBackendArchive
            self.share_classes = {"hpss": HpssBackendArchive}
        elif name == "posix":
            from archiveinterface.archivebackends.posix.posix_backend_archive \
                import PosixBackendArchive
            self.share_classes = {"posix": PosixBackendArchive}
