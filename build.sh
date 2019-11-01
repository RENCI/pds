#!/bin/bash
if [ -z $1 ]; then
    COMMIT_MSG=update
else
    COMMIT_MSG=$1
fi
docker build . -t $IMAGE:$VERSION
docker tag $IMAGE:0.1.0 zooh/$IMAGE:$VERSION
docker push zooh/$IMAGE:0.1.0
git add -u
git commit -m $COMMIT_MSG
git tag v$VERSION -f
git push
git push --tags -f
