#!/bin/bash -xe

export PYTHONPATH=$PWD
coverage run \
    --include='archiveinterface/*' \
    --omit='archiveinterface/archivebackends/abstract/*' \
    archiveinterface/archive_interface_unit_tests.py -v
coverage report -m
codeclimate-test-reporter
