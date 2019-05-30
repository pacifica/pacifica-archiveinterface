#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module used for testing a deployed archive interface."""
import os
try:  # python 2 import
    from Queue import Queue
except ImportError:  # pragma: no cover
    from queue import Queue
from threading import Thread
import unittest
from six import PY2
import requests

# url for the archive interface just deployed.
# Clean Local files will remove all the test file generated from where the script is run if true
# Clean archive files will remove the files from the archive, assuming that this process can access the
# path for the archive files
# archive prefix is only used if cleaning archive files generated by this test script
ARCHIVEURL = os.getenv('ARCHIVE_URL', 'http://127.0.0.1:8080')


def unistr2binary(data_str):
    """Convert a string to binary in 2/3."""
    if PY2:  # pragma: no cover python 2 only
        return bytearray(data_str)
    return bytearray(data_str, 'utf8')  # pragma: no cover python 3 only


class BasicArchiveTests(unittest.TestCase):
    """Class that contains basic text file tests."""

    def test_simple_write(self):
        """Test writing a simple text file."""
        fileid = '1234'
        data = unistr2binary('Writing content for first file')
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 201)
        respdata = resp.json()
        self.assertEqual(int(respdata['total_bytes']), len(data))
        self.assertEqual(respdata['message'], 'File added to archive')

    def test_simple_status(self):
        """Test statusing a simple text file."""
        fileid = '1235'
        data = unistr2binary('Writing content for first file')
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 201)
        resp = requests.head('{}/{}'.format(ARCHIVEURL, fileid))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.headers['x-pacifica-file-storage-media'], 'disk')
        self.assertEqual(resp.headers['x-content-length'], '30')
        self.assertEqual(resp.headers['x-pacifica-messsage'], 'File was found')

    def test_simple_stage(self):
        """test staging a simple text file."""
        fileid = '1236'
        data = unistr2binary('Writing content for first file')
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 201)
        resp = requests.post('{}/{}'.format(ARCHIVEURL, fileid))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['message'], 'File was staged')

    def test_simple_read(self):
        """test reading a simple text file."""
        fileid = '1237'
        data = unistr2binary('Writing content for first file')
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 201)
        resp = requests.get('{}/{}'.format(ARCHIVEURL, fileid), stream=True)
        data = resp.raw.read()
        # the len of string 'Writing content for first file'
        self.assertEqual(len(data), 30)

    def test_simple_delete(self):
        """test reading a simple text file."""
        fileid = '1238'
        data = unistr2binary('Writing content for first file')
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 201)
        resp = requests.delete('{}/{}'.format(ARCHIVEURL, fileid), stream=True)
        # the len of string 'Writing content for first file'
        self.assertEqual(resp.status_code, 200)

    def test_file_rewrite(self):
        """Test trying to rewrite a file, rewrite should fail."""
        fileid = '1239'
        data = unistr2binary('Writing content for first file')
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 201)
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 500)
        data = resp.json()
        error_msg = 'Can\'t open'
        # get error message length since the file path returned is unique per deploymnet while
        # the rest of the error message is not
        self.assertTrue(error_msg in data['traceback'])


class BinaryFileArchiveTests(unittest.TestCase):
    """Class for testing binary files through the archive workflow."""

    def test_binary_file_write(self):
        """Write a binary file to the archive."""
        fileid = '4321'
        data = bytearray([123, 3, 255, 0, 100])
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 201)
        respdata = resp.json()
        self.assertEqual(int(respdata['total_bytes']), len(data))
        self.assertEqual(respdata['message'], 'File added to archive')

    def test_binary_file_status(self):
        """Get a status for a binary file in the archive."""
        fileid = '4322'
        data = bytearray([123, 3, 255, 0, 100])
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 201)
        resp = requests.head('{}/{}'.format(ARCHIVEURL, fileid))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.headers['x-pacifica-file-storage-media'], 'disk')
        self.assertEqual(resp.headers['x-content-length'], '5')
        self.assertEqual(resp.headers['x-pacifica-messsage'], 'File was found')

    def test_binary_file_stage(self):
        """test staging a binary file."""
        fileid = '4323'
        data = bytearray([123, 3, 255, 0, 100])
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 201)
        resp = requests.post('{}/{}'.format(ARCHIVEURL, fileid))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['message'], 'File was staged')

    def test_binary_file_read(self):
        """test reading a binary file back form the archive."""
        fileid = '4324'
        data = bytearray([123, 3, 255, 0, 100])
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 201)
        resp = requests.get('{}/{}'.format(ARCHIVEURL, fileid), stream=True)
        data = resp.raw.read()
        self.assertEqual(len(data), 5)

    def test_binary_file_rewrite(self):
        """Test trying to rewrite a file, rewrite should fail."""
        fileid = '4325'
        data = bytearray([123, 3, 255, 0, 100])
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 201)
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid), data=data)
        self.assertEqual(resp.status_code, 500)
        data = resp.json()
        error_msg = 'Can\'t open'
        # get error message length since the file path returned is unique per deploymnet while
        # the rest of the error message is not
        self.assertTrue(error_msg in data['traceback'])


# pylint: disable=too-few-public-methods
class RandomFile(object):
    """Random File Object."""

    def __init__(self, size):
        """Constructor for random file."""
        self.len = size
        self.bytes_read = 0

    def read(self, size):
        """Read some random data."""
        if self.bytes_read + size > self.len:
            size = self.len - self.bytes_read
        self.bytes_read += size
        return os.urandom(size)
# pylint: enable=too-few-public-methods


class LargeBinaryFileArchiveTests(unittest.TestCase):
    """Class that tests the writing and reading of a large binary file."""

    large_file_size = int(os.getenv('LARGE_FILE_SIZE', 1024 * 1024 * 1024))

    def test_large_binary_file_write(self):
        """test writing a large binary file to the archive."""
        fileid = '9999'
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid),
                            data=RandomFile(self.large_file_size))
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(int(data['total_bytes']), self.large_file_size)
        self.assertEqual(data['message'], 'File added to archive')

    def test_large_binary_file_status(self):
        """test statusing a large binary file."""
        fileid = '9998'
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid),
                            data=RandomFile(self.large_file_size))
        self.assertEqual(resp.status_code, 201)
        resp = requests.head('{}/{}'.format(ARCHIVEURL, fileid))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.headers['x-pacifica-file-storage-media'], 'disk')
        self.assertEqual(
            resp.headers['x-content-length'], str(self.large_file_size))
        self.assertEqual(resp.headers['x-pacifica-messsage'], 'File was found')

    def test_large_binary_file_stage(self):
        """test staging a large binary file."""
        fileid = '9997'
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid),
                            data=RandomFile(self.large_file_size))
        self.assertEqual(resp.status_code, 201)
        resp = requests.post('{}/{}'.format(ARCHIVEURL, fileid))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['message'], 'File was staged')

    def test_large_binary_file_read(self):
        """test reading a large binary file."""
        fileid = '9996'
        resp = requests.put('{}/{}'.format(ARCHIVEURL, fileid),
                            data=RandomFile(self.large_file_size))
        self.assertEqual(resp.status_code, 201)
        resp = requests.get('{}/{}'.format(ARCHIVEURL, fileid), stream=True)
        filesize = 0
        buf = resp.raw.read(1024)
        while buf:
            filesize += len(buf)
            buf = resp.raw.read(1024)
        self.assertEqual(filesize, self.large_file_size)


class ManyFileArchiveTests(unittest.TestCase):
    """Class that tests the writing of many files at once."""

    def test_many_file_write(self):
        """test writing many files to the archive."""
        num_worker_threads = 8
        job_id_queue = Queue()

        def worker_put():
            """Thread worker to send the test data."""
            work = job_id_queue.get()
            while work:
                data = unistr2binary('Writing content for first file')
                resp = requests.put(
                    '{}/{}'.format(ARCHIVEURL, work), data=data)
                self.assertEqual(resp.status_code, 201)
                data = resp.json()
                self.assertEqual(data['message'], 'File added to archive')
                job_id_queue.task_done()
                work = job_id_queue.get()
            job_id_queue.task_done()

        for i in range(num_worker_threads):
            new_thread = Thread(target=worker_put)
            new_thread.daemon = True
            new_thread.start()

        for i in range(3000, int(os.getenv('MANY_FILES_TEST_COUNT', 1000))+3000):
            job_id_queue.put(i)

        for i in range(num_worker_threads):
            job_id_queue.put(False)
        job_id_queue.join()

        def worker_get():
            """Thread worker to send the test data."""
            work = job_id_queue.get()
            while work:
                resp = requests.get(
                    '{}/{}'.format(ARCHIVEURL, work))
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(resp.content, unistr2binary('Writing content for first file'))
                job_id_queue.task_done()
                work = job_id_queue.get()
            job_id_queue.task_done()

        for i in range(num_worker_threads):
            new_thread = Thread(target=worker_get)
            new_thread.daemon = True
            new_thread.start()

        for i in range(3000, int(os.getenv('MANY_FILES_TEST_COUNT', 1000))+3000):
            job_id_queue.put(i)

        for i in range(num_worker_threads):
            job_id_queue.put(False)
        job_id_queue.join()
