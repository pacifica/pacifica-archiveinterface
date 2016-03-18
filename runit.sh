#!/bin/bash -xe

server.py \
  --type $PACIFICA_AAPI_BACKEND_TYPE \
  --address $PACIFICA_AAPI_ADDRESS \
  --port $PACIFICA_AAPI_PORT \
  --prefix $PACIFICA_AAPI_PREFIX
