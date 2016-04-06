#!/bin/bash -xe

#pylint setup
#pylint setup_nohpss
pylint pacifica.archive_interface
pylint pacifica.uwsgi
pylint scripts.server
pylint pacifica.archive_interface_unit_tests
pylint pacifica.extendedfile
pylint pacifica.arhcive_interface_responses
pylint pacifica.hpss_ctypes
pylint pacifica.id2filename
