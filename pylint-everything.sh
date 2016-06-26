#!/bin/bash -xe

pylint pacifica.archive_interface
pylint pacifica.uwsgi
pylint scripts.server
pylint pacifica.archive_interface_unit_tests
pylint pacifica.extendedfile
pylint pacifica.archive_interface_responses
pylint pacifica.hpss_ctypes
pylint pacifica.id2filename
coverage run -m pacifica.archive_interface_unit_tests -v
coverage report -m
