#!/bin/bash
# TODO: promote to CI/CD.  Right now the container includes the git clone.

# Docker can only copy files from the "context directory"
#   so we soft-link the data directory in
sudo docker build -t ke2jacobs/jacobs-vault-nb-with-data:latest .
#sudo docker build --no-cache -t ke2jacobs/jacobs-vault-nb-with-data:latest .
