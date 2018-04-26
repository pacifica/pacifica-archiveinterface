#!/bin/bash -xe

export PYTHONPATH=$PWD
coverage run \
    --include='archiveinterface/*' \
    --omit='archiveinterface/archivebackends/abstract/*' \
    -m -p pytest -v archiveinterface
coverage combine -a .coverage*
coverage report -m --fail-under 80
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
