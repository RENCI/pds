#!/bin/bash
set -e

docker-compose --env-file test/env.docker -f docker-compose.yml -f test/docker-compose.yml -f test/pds-server/docker-compose.yml up --build -V --exit-code-from pdsaggregator-test

TX_TAG=`git describe --exact-match --tags $(git log -n1 --pretty='%h')  2> /dev/null; `                                                                      
if [ "${TX_TAG}" == "" ] ; then TX_TAG='unstable'; fi                                                                                                        
echo "TX_TAG=${TX_TAG}" > env.TAG                                                                                                                            
export TX_TAG

docker-compose --env-file test/env.docker -f docker-compose.yml -f test/docker-compose.system.yml -f test/pds-server-system/docker-compose.yml up --build -V --exit-code-from pdsaggregator-test
