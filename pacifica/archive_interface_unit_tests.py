"""
File used to unit test the pacifica archive interface
"""
import unittest
from pacifica.archive_interface import un_abs_path, get_http_modified_time, \
    ArchiveGenerator, ArchiveInterfaceError
from pacifica.extendedfile import ExtendedFile, POSIXStatus
from pacifica.id2filename import id2filename

class TestArchiveInterface(unittest.TestCase):
    """
    Contains all the tests for the Archive Interface
    """

    def test_un_abs_path(self):
        """test the correct creation of paths by removing absolute paths"""
        return_one = un_abs_path("tmp/foo.text")
        return_two = un_abs_path("/tmp/foo.text")
        return_three = un_abs_path("/tmp/foo.text")
        self.assertEqual(return_one, "tmp/foo.text")
        self.assertEqual(return_two, "tmp/foo.text")
        self.assertNotEqual(return_three, "/tmp/foo.text")


    def test_get_http_modified_time(self):
        """test to see if the path size of a directory is returned"""
        env = dict()
        env['HTTP_LAST_MODIFIED'] = 'SUN, 06 NOV 1994 08:49:37 GMT'
        mod_time = get_http_modified_time(env)
        self.assertEqual(mod_time, 784140577.0)

    def test_archive_generator_posix(self):
        """Test of trying to make a archive generator using POSIX backend"""
        user_name = None
        auth_path = None
        prefix = ""
        b_type = "posix"
        archiveposix = ArchiveGenerator(b_type, prefix, user_name, auth_path)
        self.assertTrue(isinstance(archiveposix.backend_open('/tmp/1234', 'w'),
                                   ExtendedFile))
        self.assertEqual(archiveposix.path_info_munge('1234'), '1234')

    def test_archive_generator_hpss(self):
        """Test of trying to make a archive generator using HPSS backend"""
        user_name = "svc-myemsldev"
        auth_path = "/var/hpss/etc/svc-myemsldev.keytab"
        prefix = "/myemsl-dev/bundle"
        b_type = "hpss"
        try:
            archive = ArchiveGenerator(b_type, prefix, user_name, auth_path)
            archive.backend_open('/myemsl-dev/bundle/test.txt', 'w')
            self.assertEqual(archive.path_info_munge('1234'), 'd2/4d2')
        except ArchiveInterfaceError:
            self.skipTest("HPSS Not Configured")

class TestExtendedFile(unittest.TestCase):
    """
    Contains all the tests for the ExtendedFile Class
    """

    def test_posix_file_status(self):
        """test the correct values of a files status"""
        filepath = '/tmp/1234'
        mode = 'w'
        my_file = ExtendedFile(filepath, mode)
        status = my_file.status()
        self.assertTrue(isinstance(status, POSIXStatus))
        self.assertEqual(status.filesize, 0)
        self.assertEqual(status.file_storage_media, 'disk')

    def test_posix_file_stage(self):
        """test the correct staging of a posix file"""
        filepath = '/tmp/1234'
        mode = 'w'
        my_file = ExtendedFile(filepath, mode)
        my_file.stage()
        #easiest way to unit test is look at class variable
        # pylint: disable=protected-access
        self.assertTrue(my_file._staged)
        # pylint: enable=protected-access

    def test_posix_file_mod_time(self):
        """test the correct setting of a file mod time"""
        filepath = '/tmp/1234'
        mode = 'w'
        my_file = ExtendedFile(filepath, mode)
        my_file.close()
        my_file.set_mod_time(036)
        status = my_file.status()
        self.assertEqual(status.mtime, 036)

class TestPOSIXStatus(unittest.TestCase):
    """
    Contains all the tests for the POSIXStatus Class
    """

    def test_posix_status_object(self):
        """test the correct creation of posix status object"""

        status = POSIXStatus(036, 035, 15, 15)
        self.assertEqual(status.mtime, 036)
        self.assertEqual(status.ctime, 035)
        self.assertEqual(status.bytes_per_level, 15)
        self.assertEqual(status.filesize, 15)
        self.assertEqual(status.defined_levels, ['disk'])
        self.assertEqual(status.file_storage_media, 'disk')

    def test_posix_status_storage_media(self):
        """test the correct finding of posix storage media"""

        status = POSIXStatus(036, 035, 15, 15)
        value = status.find_file_storage_media()
        self.assertEqual(value, 'disk')

    def test_posix_status_levels(self):
        """test the correct setting of file storage levels"""

        status = POSIXStatus(036, 035, 15, 15)
        value = status.define_levels()
        self.assertEqual(value, ['disk'])

class TestId2Filename(unittest.TestCase):
    """
    Contains all the tests for the id2filename method
    """

    def test_id2filename_basic(self):
        """test the correct creation of a basicfilename """

        filename = id2filename(1234)
        self.assertEqual(filename, '/d2/4d2')

    def test_id2filename_negative(self):
        """test the correct creation of a negative filename """

        filename = id2filename(-1)
        self.assertEqual(filename, '/ff/ff/ff/ffffffff')

    def test_id2filename_zero(self):
        """test the correct creation of a zero filename """

        filename = id2filename(0)
        self.assertEqual(filename, '/file.0')

    def test_id2filename_simple(self):
        """test the correct creation of a simple filename """

        filename = id2filename(1)
        self.assertEqual(filename, '/file.1')

    def test_id2filename_u_shift_point(self):
        """test the correct creation of an under shift point filename """

        filename = id2filename((32*1024)-1)
        self.assertEqual(filename, '/ff/7fff')

    def test_id2filename_shift_point(self):
        """test the correct creation of the shift point filename """

        filename = id2filename((32*1024))
        self.assertEqual(filename, '/00/8000')

    def test_id2filename_o_shift_point(self):
        """test the correct creation of an over shift point filename """

        filename = id2filename((32*1024)+1)
        self.assertEqual(filename, '/01/8001')

if __name__ == '__main__':
    unittest.main()
