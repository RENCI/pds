#!/bin/bash

set -e

# git submodule update --init --recursive

if [ "$build" = "" ]; then
    build=build
fi

if [ ! -d $build ]; then
    mkdir -p $build
fi

cp -r test.system/tx-router $build
cp -r test.system/plugin $build/tx-router
cp test.system/env.pds $build/tx-router/env.txrouter
cp test.system/docker-compose.system.yml $build/tx-router/test
cp test.system/Dockerfile.system $build/tx-router/test
cp test.system/test_func.system.py $build/tx-router/test

cd $build/tx-router

set -o allexport
source env.TAG
source test/env.docker
INIT_PLUGIN_PATH=./plugin
set +o allexport

MONGO_INITDB_ROOT_PASSWORD=example MONGO_NON_ROOT_PASSWORD=collection JWT_SECRET=secret docker-compose -f docker-compose.yml -f nginx/unsecure/docker-compose.yml -f test/docker-compose.system.yml up --build -V -t 3000 # --exit-code-from=pdsaggregator-test


