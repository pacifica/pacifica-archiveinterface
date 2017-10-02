"""Module used for testing a deployed archive interface."""
import os
import requests
import unittest

# url for the archive interface just deployed.
# Clean Local files will remove all the test file generated from where the script is run if true
# Clean archive files will remove the files from the archive, assuming that this process can access the
# path for the archive files
# archive prefix is only used if cleaning archive files generated by this test script
ARCHIVEURL = os.getenv('ARCHIVE_URL', 'http://127.0.0.1:8080/')
CLEANLOCALFILES = bool(os.getenv('CLEANLOCALFILES', True))
CLEANARCHIVEFILES = bool(os.getenv('CLEANARCHIVEFILES', False))
ARCHIVEPREFIX = os.getenv('ARCHIVEPREFIX', '/srv')
LOCALFILEPREFIX = os.getenv('LOCALFILEPREFIX', '/tmp')


class BasicArchiveTests(unittest.TestCase):
    """Class that contains basic text file tests."""

    local_files = {}
    archive_files = {}

    def test_simple_write(self):
        """Test writing a simple text file."""
        filename = os.path.join(LOCALFILEPREFIX, 'test_simple_write.txt')
        fileid = '1234'
        file1 = open(filename, 'w+')
        file1.write('Writing content for first file')
        file1.close()
        self.local_files[filename] = filename
        filesize = os.path.getsize(filename)
        f = open(filename, 'rb')
        resp = requests.put(str(ARCHIVEURL + fileid), data=f)
        f.close()
        self.assertEqual(resp.status_code, 201)
        self.archive_files[fileid] = fileid
        data = resp.json()
        self.assertEqual(int(data['total_bytes']), filesize)
        self.assertEqual(data['message'], 'File added to archive')

    def test_simple_status(self):
        """Test statusing a simple text file."""
        fileid = '1234'
        resp = requests.head(str(ARCHIVEURL + fileid))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.headers['x-pacifica-file-storage-media'], 'disk')
        self.assertEqual(resp.headers['content-length'], '30')
        self.assertEqual(resp.headers['x-pacifica-messsage'], 'File was found')

    def test_simple_stage(self):
        """test staging a simple text file."""
        fileid = '1234'
        resp = requests.post(str(ARCHIVEURL + fileid))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['message'], 'File was staged')

    def test_simple_read(self):
        """test reading a simple text file."""
        fileid = '1234'
        filename = os.path.join(LOCALFILEPREFIX, 'test_simple_read.txt')
        resp = requests.get(str(ARCHIVEURL + fileid), stream=True)
        myfile = open(filename, 'wb+')
        buf = resp.raw.read(1024)
        while buf:
            myfile.write(buf)
            buf = resp.raw.read(1024)
        myfile.close()
        self.local_files[filename] = filename
        filesize = os.path.getsize(filename)
        # know the simple file writtten is 30 bytes from archive
        self.assertEqual(filesize, 30)

    def test_file_rewrite(self):
        """Test trying to rewrite a file, rewrite should fail."""
        filename = os.path.join(LOCALFILEPREFIX, 'test_simple_write.txt')
        fileid = '1234'
        file1 = open(filename, 'w+')
        file1.write('Writing content for first file')
        file1.close()
        f = open(filename, 'rb')
        resp = requests.put(str(ARCHIVEURL + fileid), data=f)
        f.close()
        self.assertEqual(resp.status_code, 500)
        data = resp.json()
        error_msg = 'Can\'t open'
        # get error message length since the file path returned is unique per deploymnet while
        # the rest of the error message is not
        err_msg_length = len(error_msg)
        self.assertEqual(data['message'][:err_msg_length], error_msg)

    def test_simple_cleanup(self):
        """Clean up files that are created for testing."""
        if CLEANLOCALFILES:
            for filepath in self.local_files:
                os.remove(filepath)

        if CLEANARCHIVEFILES:
            for filepath in self.archive_files:
                os.remove(ARCHIVEPREFIX + filepath)
        self.assertEqual(True, True)


class BinaryFileArchiveTests(unittest.TestCase):
    """Class for testing binary files through the archive workflow."""

    local_files = {}
    archive_files = {}

    def test_binary_file_write(self):
        """Write a binary file to the archive."""
        filename = os.path.join(LOCALFILEPREFIX, 'binary_file')
        fileid = '4321'
        newFileBytes = [123, 3, 255, 0, 100]
        file1 = open(filename, 'wb+')
        newFileByteArray = bytearray(newFileBytes)
        file1.write(newFileByteArray)
        file1.close()
        self.local_files[filename] = filename
        filesize = os.path.getsize(filename)
        f = open(filename, 'rb')
        resp = requests.put(str(ARCHIVEURL + fileid), data=f)
        f.close()
        self.archive_files[fileid] = fileid
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(int(data['total_bytes']), filesize)
        self.assertEqual(data['message'], 'File added to archive')

    def test_binary_file_status(self):
        """Get a status for a binary file in the archive."""
        fileid = '4321'
        resp = requests.head(str(ARCHIVEURL + fileid))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.headers['x-pacifica-file-storage-media'], 'disk')
        self.assertEqual(resp.headers['content-length'], '5')
        self.assertEqual(resp.headers['x-pacifica-messsage'], 'File was found')

    def test_binary_file_stage(self):
        """test staging a binary file."""
        fileid = '4321'
        resp = requests.post(str(ARCHIVEURL + fileid))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['message'], 'File was staged')

    def test_binary_file_read(self):
        """test reading a binary file back form the archive."""
        fileid = '4321'
        filename = os.path.join(LOCALFILEPREFIX, 'test_binary_read')
        resp = requests.get(str(ARCHIVEURL + fileid), stream=True)
        myfile = open(filename, 'wb+')
        buf = resp.raw.read(1024)
        while buf:
            myfile.write(buf)
            buf = resp.raw.read(1024)
        myfile.close()
        self.local_files[filename] = filename
        filesize = os.path.getsize(filename)
        self.assertEqual(filesize, 5)

    def test_binary_file_rewrite(self):
        """Test trying to rewrite a file, rewrite should fail."""
        filename = os.path.join(LOCALFILEPREFIX, 'binary_file')
        fileid = '4321'
        newFileBytes = [123, 3, 255, 0, 100]
        file1 = open(filename, 'wb+')
        newFileByteArray = bytearray(newFileBytes)
        file1.write(newFileByteArray)
        file1.close()
        f = open(filename, 'rb')
        resp = requests.put(str(ARCHIVEURL + fileid), data=f)
        f.close()
        self.assertEqual(resp.status_code, 500)
        data = resp.json()
        error_msg = 'Can\'t open'
        # get error message length since the file path returned is unique per deploymnet while
        # the rest of the error message is not
        err_msg_length = len(error_msg)
        self.assertEqual(data['message'][:err_msg_length], error_msg)

    def test_binary_cleanup(self):
        """Clean up files that are created for testing."""
        if CLEANLOCALFILES:
            for filepath in self.local_files:
                os.remove(filepath)

        if CLEANARCHIVEFILES:
            for filepath in self.archive_files:
                os.remove(ARCHIVEPREFIX + filepath)
        self.assertEqual(True, True)


class LargeBinaryFileArchiveTests(unittest.TestCase):
    """Class that tests the writing and reading of a large binary file."""

    local_files = {}
    archive_files = {}
    filesize = {}

    def test_large_binary_file_write(self):
        """test writing a large binary file to the archive."""
        filename = os.path.join(LOCALFILEPREFIX, 'large_binary_file')
        fileid = '9999'
        file1 = open(filename, 'wb+')
        flag = 0
        while flag < 1000000:
            file1.write(os.urandom(1024))
            flag += 1
        file1.close()
        self.local_files[filename] = filename
        self.filesize['size'] = os.path.getsize(filename)
        f = open(filename, 'rb')
        try:
            resp = requests.put(str(ARCHIVEURL + fileid), data=f)
        except IOError, e:
            if e.errno == 32:
                # error for browser closing pipe
                print 'Browser Closed connection. Subsequent test will prove pass or fail'
                self.assertEqual(True, True)
                return

        f.close()
        self.archive_files[fileid] = fileid
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(int(data['total_bytes']), self.filesize['size'])
        self.assertEqual(data['message'], 'File added to archive')

    def test_large_binary_file_status(self):
        """test statusing a large binary file."""
        fileid = '9999'
        resp = requests.head(str(ARCHIVEURL + fileid))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.headers['x-pacifica-file-storage-media'], 'disk')
        self.assertEqual(resp.headers['content-length'], str(self.filesize['size']))
        self.assertEqual(resp.headers['x-pacifica-messsage'], 'File was found')

    def test_large_binary_file_stage(self):
        """test staging a large binary file."""
        fileid = '9999'
        resp = requests.post(str(ARCHIVEURL + fileid))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['message'], 'File was staged')

    def test_large_binary_file_read(self):
        """test reading a large binary file."""
        fileid = '9999'
        filename = os.path.join(LOCALFILEPREFIX, 'test_binary_read')
        resp = requests.get(str(ARCHIVEURL + fileid), stream=True)
        myfile = open(filename, 'wb+')
        buf = resp.raw.read(1024)
        while buf:
            myfile.write(buf)
            buf = resp.raw.read(1024)
        myfile.close()
        self.local_files[filename] = filename
        filesize = os.path.getsize(filename)
        self.assertEqual(filesize, self.filesize['size'])

    def test_large_binary_cleanup(self):
        """Clean up files that are created for testing."""
        if CLEANLOCALFILES:
            for filepath in self.local_files:
                os.remove(filepath)

        if CLEANARCHIVEFILES:
            for filepath in self.archive_files:
                os.remove(ARCHIVEPREFIX + filepath)
        self.assertEqual(True, True)


class ManyFileArchiveTests(unittest.TestCase):
    """Class that tests the writing of many files at once."""

    local_files = {}
    archive_files = {}

    def test_many_file_write(self):
        """test writing many files to the archive."""
        for i in range(3000, 4000):
            filename = os.path.join(LOCALFILEPREFIX, 'test_simple_write' + str(i) + '.txt')
            fileid = str(i)
            file1 = open(filename, 'w+')
            file1.write('Writing content for first file')
            file1.close()
            self.local_files[filename] = filename
            f = open(filename, 'rb')
            resp = requests.put(str(ARCHIVEURL + fileid), data=f)
            f.close()
            self.assertEqual(resp.status_code, 201)
            self.archive_files[fileid] = fileid
            data = resp.json()
            self.assertEqual(data['message'], 'File added to archive')

    def test_many_file_cleanup(self):
        """Clean up files that are created for testing."""
        if CLEANLOCALFILES:
            for filepath in self.local_files:
                os.remove(filepath)

        if CLEANARCHIVEFILES:
            for filepath in self.archive_files:
                os.remove(ARCHIVEPREFIX + filepath)
        self.assertEqual(True, True)


def suite():
    """create the test suite in order it so test run correctly."""
    suite = unittest.TestSuite()
    suite.addTest(BasicArchiveTests('test_simple_write'))
    suite.addTest(BasicArchiveTests('test_simple_status'))
    suite.addTest(BasicArchiveTests('test_simple_stage'))
    suite.addTest(BasicArchiveTests('test_simple_read'))
    suite.addTest(BasicArchiveTests('test_file_rewrite'))
    suite.addTest(BasicArchiveTests('test_simple_cleanup'))
    suite.addTest(BinaryFileArchiveTests('test_binary_file_write'))
    suite.addTest(BinaryFileArchiveTests('test_binary_file_status'))
    suite.addTest(BinaryFileArchiveTests('test_binary_file_stage'))
    suite.addTest(BinaryFileArchiveTests('test_binary_file_read'))
    suite.addTest(BinaryFileArchiveTests('test_binary_file_rewrite'))
    suite.addTest(BinaryFileArchiveTests('test_binary_cleanup'))
    suite.addTest(LargeBinaryFileArchiveTests('test_large_binary_file_write'))
    suite.addTest(LargeBinaryFileArchiveTests('test_large_binary_file_status'))
    suite.addTest(LargeBinaryFileArchiveTests('test_large_binary_file_stage'))
    suite.addTest(LargeBinaryFileArchiveTests('test_large_binary_file_read'))
    suite.addTest(LargeBinaryFileArchiveTests('test_large_binary_cleanup'))
    suite.addTest(ManyFileArchiveTests('test_many_file_write'))
    suite.addTest(ManyFileArchiveTests('test_many_file_cleanup'))
    return suite


if __name__ == '__main__':
    """builds and runs the test suite."""
    runner = unittest.TextTestRunner()
    runner.run(suite())
