#!/usr/bin/python
"""
uWSGI server application generator.
"""
from pacifica.archive_interface import ArchiveGenerator
import ConfigParser
import os.path


def application(env, start_response):
    """
    read the config settings from the application.ini file
    """
    settings = ConfigParser.ConfigParser()
    settings.read(os.path.dirname(os.path.realpath(__file__))
                  +"/application.ini")
    typed = settings.get('BackendSettings', 'type')
    prefix = settings.get('BackendSettings', 'prefix')
    user = settings.get('BackendSettings', 'user')
    auth = settings.get('BackendSettings', 'auth')
    generator = ArchiveGenerator(typed, prefix, user, auth)
    return generator.pacifica_archiveinterface(env, start_response)
