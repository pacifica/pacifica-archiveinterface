#!/usr/bin/python
# -*- coding: utf-8 -*-
"""File used to unit test the pacifica archive interface responses."""
import unittest
import json
import archiveinterface.archive_interface_responses as interface_responses
from archiveinterface.archive_interface_error import ArchiveInterfaceError


def start_response(code, headers):
    """Method to mock start_response"""
        return [code, headers]

class TestInterfaceResponses(unittest.TestCase):
    """Test the Interface Responses Class."""

    def test_unknown_request(self):
        """Test response for unknown request."""
        resp = interface_responses.Responses()
        response = resp.unknown_request(start_response, 'badRequest')
        jsn = json.loads(response)
        self.assertEqual(jsn['message'], 'Unknown request method')
        self.assertEqual(jsn['request_method'], 'badRequest')

if __name__ == '__main__':
    unittest.main()
