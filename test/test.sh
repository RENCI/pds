#!/bin/bash
set -e

set -o allexport
source env.TAG
source test/env.docker
set +o allexport

docker-compose --env-file test/env.docker -f docker-compose.yml -f test/docker-compose.yml -f test/docker-compose.mock.yml up --build -V --exit-code-from pdsaggregator-test

# docker-compose --env-file test/env.docker -f docker-compose.yml -f test/docker-compose.system.yml -f test/pds-server-system/docker-compose.yml up --build -V --exit-code-from pdsaggregator-test
