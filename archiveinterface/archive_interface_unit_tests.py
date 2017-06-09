#!/usr/bin/python
"""File used to unit test the pacifica archive interface."""
import unittest
import time
import os
from stat import ST_MODE
from archiveinterface.archive_utils import un_abs_path, get_http_modified_time, read_config_value, set_config_name
from archiveinterface.id2filename import id2filename
from archiveinterface.archivebackends.posix.extendedfile import ExtendedFile
from archiveinterface.archivebackends.posix.posix_status import PosixStatus
from archiveinterface.archivebackends.posix.posix_backend_archive import PosixBackendArchive
from archiveinterface.archive_interface_error import ArchiveInterfaceError


class TestArchiveUtils(unittest.TestCase):
    """Test the Archive utils class."""

    def test_utils_absolute_path(self):
        """Test the return of un_abs_path."""
        return_one = un_abs_path('tmp/foo.text')
        return_two = un_abs_path('/tmp/foo.text')
        return_three = un_abs_path('/tmp/foo.text')
        return_four = un_abs_path('foo.text')
        self.assertEqual(return_one, 'tmp/foo.text')
        self.assertEqual(return_two, 'tmp/foo.text')
        self.assertNotEqual(return_three, '/tmp/foo.text')
        self.assertEqual(return_four, 'foo.text')
        hit_exception = False
        try:
            un_abs_path(47)
        except ArchiveInterfaceError:
            hit_exception = True
        self.assertTrue(hit_exception)

    def test_get_http_modified_time(self):
        """Test to see if the path size of a directory is returned."""
        env = dict()
        env['HTTP_LAST_MODIFIED'] = 'SUN, 06 NOV 1994 08:49:37 GMT'
        mod_time = get_http_modified_time(env)
        self.assertEqual(mod_time, 784111777)
        env = dict()
        mod_time = get_http_modified_time(env)
        self.assertEqual(int(mod_time), int(time.time()))
        for thing in (None, [], 46):
            hit_exception = False
            try:
                env['HTTP_LAST_MODIFIED'] = thing
                get_http_modified_time(env)
            except ArchiveInterfaceError:
                hit_exception = True
            self.assertTrue(hit_exception)


class TestId2Filename(unittest.TestCase):
    """Test the id2filename method."""

    def test_id2filename_basic(self):
        """Test the correct creation of a basicfilename."""
        filename = id2filename(1234)
        self.assertEqual(filename, '/d2/4d2')

    def test_id2filename_negative(self):
        """Test the correct creation of a negative filename."""
        filename = id2filename(-1)
        self.assertEqual(filename, '/file.-1')

    def test_id2filename_zero(self):
        """Test the correct creation of a zero filename."""
        filename = id2filename(0)
        self.assertEqual(filename, '/file.0')

    def test_id2filename_simple(self):
        """Test the correct creation of a simple filename."""
        filename = id2filename(1)
        self.assertEqual(filename, '/file.1')

    def test_id2filename_u_shift_point(self):
        """Test the correct creation of an under shift point filename."""
        filename = id2filename((32*1024)-1)
        self.assertEqual(filename, '/ff/7fff')

    def test_id2filename_shift_point(self):
        """Test the correct creation of the shift point filename."""
        filename = id2filename((32*1024))
        self.assertEqual(filename, '/00/8000')

    def test_id2filename_o_shift_point(self):
        """Test the correct creation of an over shift point filename."""
        filename = id2filename((32*1024)+1)
        self.assertEqual(filename, '/01/8001')


class TestExtendedFile(unittest.TestCase):
    """Test the ExtendedFile Class."""

    def test_posix_file_status(self):
        """Test the correct values of a files status."""
        filepath = '/tmp/1234'
        mode = 'w'
        my_file = ExtendedFile(filepath, mode)
        status = my_file.status()
        self.assertTrue(isinstance(status, PosixStatus))
        self.assertEqual(status.filesize, 0)
        self.assertEqual(status.file_storage_media, 'disk')
        my_file.close()

    def test_posix_file_stage(self):
        """Test the correct staging of a posix file."""
        filepath = '/tmp/1234'
        mode = 'w'
        my_file = ExtendedFile(filepath, mode)
        my_file.stage()
        # easiest way to unit test is look at class variable
        # pylint: disable=protected-access
        self.assertTrue(my_file._staged)
        # pylint: enable=protected-access
        my_file.close()


class TestPosixStatus(unittest.TestCase):
    """Test the POSIXStatus Class."""

    def test_posix_status_object(self):
        """Test the correct creation of posix status object."""
        status = PosixStatus(036, 035, 15, 15)
        self.assertEqual(status.mtime, 036)
        self.assertEqual(status.ctime, 035)
        self.assertEqual(status.bytes_per_level, 15)
        self.assertEqual(status.filesize, 15)
        self.assertEqual(status.defined_levels, ['disk'])
        self.assertEqual(status.file_storage_media, 'disk')

    def test_posix_status_storage_media(self):
        """Test the correct finding of posix storage media."""
        status = PosixStatus(036, 035, 15, 15)
        value = status.find_file_storage_media()
        self.assertEqual(value, 'disk')

    def test_posix_status_levels(self):
        """Test the correct setting of file storage levels."""
        status = PosixStatus(036, 035, 15, 15)
        value = status.define_levels()
        self.assertEqual(value, ['disk'])


class TestPosixBackendArchive(unittest.TestCase):
    """Test the Posix backend archive."""

    def test_posix_backend_create(self):
        """Test creating a posix backend."""
        backend = PosixBackendArchive('/tmp')
        self.assertTrue(isinstance(backend, PosixBackendArchive))
        # easiest way to unit test is look at class variable
        # pylint: disable=protected-access
        self.assertEqual(backend._prefix, '/tmp')
        # pylint: enable=protected-access

    def test_posix_backend_open(self):
        """Test opening a file from posix backend."""
        filepath = '1234'
        mode = 'w'
        backend = PosixBackendArchive('/tmp')
        my_file = backend.open(filepath, mode)
        self.assertTrue(isinstance(my_file, PosixBackendArchive))
        # easiest way to unit test is look at class variable
        # pylint: disable=protected-access
        self.assertTrue(isinstance(backend._file, ExtendedFile))
        # pylint: enable=protected-access
        my_file.close()
        # opening twice in a row is okay
        my_file = backend.open(filepath, mode)
        my_file = backend.open(filepath, mode)

        # force a close to throw an error
        def close_error():
            raise ArchiveInterfaceError('this is an error')
        orig_close = backend._file.close
        backend._file.close = close_error
        hit_exception = False
        try:
            my_file = backend.open(filepath, mode)
        except ArchiveInterfaceError:
            hit_exception = True
        self.assertTrue(hit_exception)
        backend._file.close = orig_close
        hit_exception = False
        try:
            my_file = backend.open(47, mode)
        except ArchiveInterfaceError as ex:
            self.assertTrue('Cant remove absolute path' in str(ex))
            hit_exception = True
        self.assertTrue(hit_exception)

        my_file = backend.open('/a/b/d', mode)
        set_config_name('test_configs/posix-id2filename.cfg')
        backend = PosixBackendArchive('/tmp')
        my_file = backend.open(12345, mode)
        set_config_name('config.cfg')

    def test_posix_backend_close(self):
        """Test closing a file from posix backend."""
        filepath = '1234'
        mode = 'w'
        backend = PosixBackendArchive('/tmp/')
        my_file = backend.open(filepath, mode)
        # easiest way to unit test is look at class variable
        # pylint: disable=protected-access
        self.assertTrue(isinstance(backend._file, ExtendedFile))
        my_file.close()
        self.assertEqual(backend._file, None)
        # pylint: enable=protected-access

    def test_posix_backend_write(self):
        """Test writing a file from posix backend."""
        filepath = '1234'
        mode = 'w'
        backend = PosixBackendArchive('/tmp/')
        my_file = backend.open(filepath, mode)
        error = my_file.write('i am a test string')
        self.assertEqual(error, None)
        my_file.close()

    def test_posix_file_mod_time(self):
        """Test the correct setting of a file mod time."""
        filepath = '1234'
        mode = 'w'
        backend = PosixBackendArchive('/tmp/')
        my_file = backend.open(filepath, mode)
        my_file.close()
        my_file.set_mod_time(1000000)
        my_file = backend.open(filepath, 'r')
        status = my_file.status()
        my_file.close()
        self.assertEqual(status.mtime, 1000000)

    def test_posix_file_permissions(self):
        """Test the correct setting of a file mod time."""
        filepath = '12345'
        mode = 'w'
        backend = PosixBackendArchive('/tmp/')
        my_file = backend.open(filepath, mode)
        my_file.close()
        my_file.set_file_permissions()
        statinfo = oct(os.stat('/tmp/12345')[ST_MODE])[-3:]
        self.assertEqual(statinfo, '444')

    def test_posix_backend_failed_write(self):
        """Test writing to a failed file."""
        filepath = '1234'
        mode = 'w'
        backend = PosixBackendArchive('/tmp/')
        # test failed write
        backend.open(filepath, mode)

        def write_error():
            raise IOError('Unable to Write!')
        backend._file.write = write_error
        hit_exception = False
        try:
            backend.write('write stuff')
        except ArchiveInterfaceError as ex:
            hit_exception = True
            self.assertTrue("Can't write posix file with error" in str(ex))
        self.assertTrue(hit_exception)

    def test_posix_backend_read(self):
        """Test reading a file from posix backend."""
        self.test_posix_backend_write()
        filepath = '1234'
        mode = 'r'
        backend = PosixBackendArchive('/tmp/')
        my_file = backend.open(filepath, mode)
        buf = my_file.read(-1)
        self.assertEqual(buf, 'i am a test string')
        my_file.close()

    def test_read_config_file(self):
        """Test reading from config file."""
        port = read_config_value('hms_sideband', 'port')
        self.assertEqual(port, '3306')

    def test_read_config_bad_section(self):
        """Test reading from config file with bad section."""
        with self.assertRaises(ArchiveInterfaceError) as context:
            read_config_value('bad_section', 'port')
        self.assertTrue('Error reading config file, no section: bad_section', context.exception)

    def test_read_config_bad_field(self):
        """Test reading from config file with bad section."""
        with self.assertRaises(ArchiveInterfaceError) as context:
            read_config_value('hms_sideband', 'bad_field')
        self.assertTrue('Error reading config file, no field: bad_field in section: hms_sideband',
                        context.exception)


if __name__ == '__main__':
    unittest.main()
