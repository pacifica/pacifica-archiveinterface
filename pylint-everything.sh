#!/bin/bash -xe

pylint setup
pylint setup_nohpss
pylint pacifica.archive_interface
pylint pacifica.uwsgi
pylint scripts.server
