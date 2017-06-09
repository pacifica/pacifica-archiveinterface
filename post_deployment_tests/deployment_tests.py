import os
import requests
import unittest

#url for the archive interface just deployed.
ARCHIVEURL = 'http://127.0.0.1:8080/'

class BasicArchiveTests(unittest.TestCase):
    def test_simple_write(self):
        filename = '/tmp/test_simple_write.txt'
        fileid = '1234'
        file1 = open(filename,'w+')
        file1.write('Writing content for first file')
        file1.close()
        filesize = os.path.getsize(filename)
        f = open(filename,'rb')
        resp = requests.put(str(ARCHIVEURL + fileid), data=f)
        f.close()
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.headers, True)

    def test_simple_status(self):
        fileid = '1234'
        resp = requests.head(str(ARCHIVEURL + fileid))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.headers, True)

    def test_simple_stage(self):
        fileid = '1234'
        resp = requests.post(str(ARCHIVEURL + fileid))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers, True)

    def test_simple_read(self):
        fileid = '1234'
        filename = '/tmp/test_simple_read.txt'
        resp = requests.get(str(ARCHIVEURL + fileid), stream=True)
        myfile = open(filename, 'wb+')
        buf = resp.raw.read(1024)
        while buf:
            myfile.write(buf)
            buf = resp.raw.read(1024)
        myfile.close()
        filesize = os.path.getsize(filename)
        #know the simple file writtten is 30 bytes from archive
        self.assertEqual(filesize, 30)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(BasicArchiveTests('test_simple_write'))
    suite.addTest(BasicArchiveTests('test_simple_status'))
    suite.addTest(BasicArchiveTests('test_simple_stage'))
    suite.addTest(BasicArchiveTests('test_simple_read'))
    return suite

if __name__ == "__main__":
    #trigger the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite())