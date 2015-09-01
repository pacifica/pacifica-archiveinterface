#!/bin/bash -xe

server.py \
  --type $MYEMSL_AAPI_BACKEND_TYPE \
  --address $MYEMSL_AAPI_ADDRESS \
  --port $MYEMSL_AAPI_PORT \
  --prefix $MYEMSL_AAPI_PREFIX
