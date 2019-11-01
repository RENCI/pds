#!/bin/bash
docker-compose -f docker-compose.yml -f test/docker-compose.yml -f test/pds-server/docker-compose.yml up --build -V --exit-code-from pdsaggregator-test
