#!/bin/bash

python ./setup.py build
export PYTHONPATH=$PWD/build/lib.linux-x86_64-2.7
python ./scripts/server.py -u svc-myemsldev --auth /home/dmlb2000/svc-myemsldev.keytab -t hpss --prefix /myemsl-dev/bundle
