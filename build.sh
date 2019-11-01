#!/bin/bash
docker build . -t pds-aggregator:$VERSION
docker tag pds-aggregator:0.1.0 zooh/pds-aggregator:$VERSION
docker push zooh/pds-aggregator:0.1.0
git add -u
git commit -m "update"
git tag v$VERSION -f
git push
git push --tags -f
