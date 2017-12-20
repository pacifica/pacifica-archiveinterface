#!/bin/bash -xe

export PYTHONPATH=$PWD
coverage run \
    --include='archiveinterface/*' \
    --omit='archiveinterface/archivebackends/abstract/*' \
    -m -p pytest -v archiveinterface/archive_interface_unit_tests.py archiveinterface/archive_posix_unit_tests.py
coverage report -m --fail-under 70
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
