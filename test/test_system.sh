#!/bin/bash

set -e

# git submodule update --init --recursive

cp -r plugin tx-router
cp env.pds tx-router/env.txrouter
cd tx-router

set -o allexport
source env.TAG
source test/env.docker
INIT_PLUGIN_PATH=./plugin
set +o allexport

MONGO_INITDB_ROOT_PASSWORD=example MONGO_NON_ROOT_PASSWORD=collection JWT_SECRET=secret docker-compose -f docker-compose.yml up --build -V


