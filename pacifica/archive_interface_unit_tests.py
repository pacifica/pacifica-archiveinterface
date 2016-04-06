"""
File used to unit test the pacifica archive interface
"""
import unittest
import os
from pacifica.archive_interface import un_abs_path, get_http_modified_time


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


if __name__ == '__main__':
    unittest.main()
