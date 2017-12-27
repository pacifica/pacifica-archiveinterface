#!/usr/bin/python
# -*- coding: utf-8 -*-
"""File used to unit test the pacifica archive interface responses."""
import unittest
import json
import archiveinterface.archive_interface_responses as interface_responses
from archiveinterface.archivebackends.posix.posix_status import PosixStatus


class TestInterfaceResponses(unittest.TestCase):
    """Test the Interface Responses Class."""

    @staticmethod
    def start_response(code, headers):
        """Method to mock start_response."""
        return [code, headers]

    def test_unknown_request(self):
        """Test response for unknown request."""
        resp = interface_responses.Responses()
        response = resp.unknown_request(self.start_response, 'badRequest')
        jsn = json.loads(json.dumps(response))
        self.assertEqual(jsn['message'], 'Unknown request method')
        self.assertEqual(jsn['request_method'], 'badRequest')

    def test_unknown_exception(self):
        """Test response for unknown exception."""
        resp = interface_responses.Responses()
        response = resp.unknown_exception(self.start_response)
        jsn = json.loads(json.dumps(response))
        self.assertEqual(jsn['message'], 'Unknown Exception Occured')

    def test_put_response(self):
        """Test response for successful put."""
        resp = interface_responses.Responses()
        response = resp.successful_put_response(self.start_response, 36)
        jsn = json.loads(json.dumps(response))
        self.assertEqual(jsn['message'], 'File added to archive')
        self.assertEqual(jsn['total_bytes'], 36)

    def test_patch_response(self):
        """Test response for successful patch."""
        resp = interface_responses.Responses()
        response = resp.file_patch(self.start_response)
        jsn = json.loads(json.dumps(response))
        self.assertEqual(jsn['message'], 'File Moved Successfully')

    def test_working_response(self):
        """Test response for successful archive working."""
        resp = interface_responses.Responses()
        response = resp.archive_working_response(self.start_response)
        jsn = json.loads(json.dumps(response))
        self.assertEqual(jsn['message'], 'Pacifica Archive Interface Up and Running')

    def test_file_stage(self):
        """Test response for successful stage."""
        resp = interface_responses.Responses()
        response = resp.file_stage(self.start_response, 'mytestfile.txt')
        jsn = json.loads(json.dumps(response))
        self.assertEqual(jsn['message'], 'File was staged')
        self.assertEqual(jsn['file'], 'mytestfile.txt')

    def test_patch_error(self):
        """Test response for patch error."""
        resp = interface_responses.Responses()
        response = resp.json_patch_error_response(self.start_response)
        jsn = json.loads(json.dumps(response))
        self.assertEqual(jsn['message'], 'JSON content could not be read')

    def test_archive_exception(self):
        """Test response for patch error."""
        resp = interface_responses.Responses()
        response = resp.archive_exception(self.start_response, 'random_error_message', 'notHEAD')
        jsn = json.loads(json.dumps(response))
        self.assertEqual(jsn['message'], 'random_error_message')
        resp = interface_responses.Responses()
        response = resp.archive_exception(self.start_response, 'random_error_message', 'HEAD')
        self.assertEqual(response, None)

    def test_file_status(self):
        """Test response for patch error."""
        resp = interface_responses.Responses()
        response = resp.file_status(self.start_response, None)
        self.assertEqual(response, '')
        status = PosixStatus(11, 11, 10, 10)
        status.set_filepath('fake_path')
        resp = interface_responses.Responses()
        response = resp.file_status(self.start_response, status)
        self.assertEqual(response, '')
