#!/bin/bash -xe

export PYTHONPATH=$PWD
coverage run \
    --include='archiveinterface/*' \
    --omit='archiveinterface/archivebackends/abstract/*' \
    -m pytest archiveinterface/archive_interface_unit_tests.py -v
coverage report -m --fail-under 90
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
