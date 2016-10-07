#!/bin/bash

python ./scripts/archiveinterfaceserver.py \
  -t $PACIFICA_AAPI_BACKEND_TYPE \
  -p $PACIFICA_AAPI_PORT \
  -a $PACIFICA_AAPI_ADDRESS \
  --prefix $PACIFICA_AAPI_PREFIX \
  "$@"
