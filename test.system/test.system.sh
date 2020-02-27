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
cp env.TAG $build
cp test.system/env.pds $build/tx-router/env.txrouter
cp test.system/docker-compose.system.yml $build/tx-router/test
cp test.system/Dockerfile.system $build/tx-router/test
cp test.system/test_func.system.py $build/tx-router/test

cd $build

set -o allexport
source env.TAG
source tx-router/test/env.docker
INIT_PLUGIN_PATH=./plugin
set +o allexport

cd tx-router

if [ "$1" == "deploy" ]; then
    MONGO_INITDB_ROOT_PASSWORD=example MONGO_NON_ROOT_PASSWORD=collection JWT_SECRET=secret docker-compose -f docker-compose.yml -f nginx/unsecure/docker-compose.yml up --build -V -t 3000 -d
if [ "$1" == "down" ]; then
    MONGO_INITDB_ROOT_PASSWORD=example MONGO_NON_ROOT_PASSWORD=collection JWT_SECRET=secret docker-compose -f docker-compose.yml -f nginx/unsecure/docker-compose.yml down -t 3000
elif [ "$1" == "keep_containers" ]; then
    MONGO_INITDB_ROOT_PASSWORD=example MONGO_NON_ROOT_PASSWORD=collection JWT_SECRET=secret docker-compose -f docker-compose.yml -f nginx/unsecure/docker-compose.yml -f test/docker-compose.system.yml up --build -V -t 3000
else
    MONGO_INITDB_ROOT_PASSWORD=example MONGO_NON_ROOT_PASSWORD=collection JWT_SECRET=secret docker-compose -f docker-compose.yml -f nginx/unsecure/docker-compose.yml -f test/docker-compose.system.yml up --build -V -t 3000 --exit-code-from=pdsaggregator-test
fi


