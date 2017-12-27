#!/usr/bin/python
# -*- coding: utf-8 -*-
"""File used to unit test the pacifica archive interface responses."""
import unittest
import json
import archiveinterface.archive_interface_responses as interface_responses


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


if __name__ == '__main__':
    unittest.main()
