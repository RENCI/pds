#!/bin/bash
docker build . -t pds-aggregator:0.1.0
docker tag pds-aggregator:0.1.0 zooh/pds-aggregator:0.1.0
docker push zooh/pds-aggregator:0.1.0
