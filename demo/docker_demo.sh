#!/bin/bash
#
#  Runs Jupyter Notebook in a the jacobs-vault Docker container that
#  contains all required dependencies for VAULT_Demo.ipynb 
#
#  The data volume is expected to be mounted in at ../data relative
#  to the directory containing this file.

docker run --rm -it -p 2080:2080 -v /share/nas2/data/airforce:/github.com/cmorris-jacobs/jacobs-vault/data jacobs-vault:latest 
