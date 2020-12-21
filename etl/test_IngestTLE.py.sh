#!/bin/bash

SRC_DIR=/share/nas2/data/vault/TLE
FILTER=/home/kenglish/repo/github.com/cmorris-jacobs/jacobs-vault/etl/IngestTLE.py
Z=tle2015.txt.zip

unzip -p ${SRC_DIR}/$Z | head -6 | python ${FILTER}

