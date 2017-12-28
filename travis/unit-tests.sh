#!/bin/bash -xe

export PYTHONPATH=$PWD
coverage run \
    --include='archiveinterface/*' \
    --omit='archiveinterface/archivebackends/abstract/*' \
    -m -p pytest -v archiveinterface/tests/archive_interface_unit_test.py archiveinterface/tests/archive_posix_unit_test.py archiveinterface/tests/archive_response_unit_test.py
coverage combine -a .coverage*
coverage report -m --fail-under 75
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
