#!/bin/bash
if [ -z $COMMIT_MSG ]; then
    COMMIT_MSG=update
fi
if [ -z $IMAGE ]; then
    echo environment variable IMAGE not set
    exit 1
fi
if [ -z $VERSION ]; then
    echo environment variable VERSION not set
    exit 1
fi
docker build . -t $IMAGE:$VERSION
docker tag $IMAGE:0.1.0 zooh/$IMAGE:$VERSION
docker push zooh/$IMAGE:0.1.0
git add -u
git commit -m $COMMIT_MSG
git tag v$VERSION -f
git push
git push --tags -f
