#!/bin/bash
# TODO: promote to CI/CD.  Right now the container includes the git clone.
docker build --no-cache -t jacobs-vault:latest .
