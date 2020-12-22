#!/bin/bash

SRC_DIR=/share/nas2/data/vault/TLE
TGT_HDFS=/ingest/airforce/vault/tle_2015_2017_2
FILTER=/home/kenglish/repo/github.com/cmorris-jacobs/jacobs-vault/etl/IngestTLE.py

#lines per file -- shooting for 12 evenly divided files
LPF=1651784

hdfs dfs -mkdir ${TGT_HDFS}
mkdir ${SRC_DIR}_tmp

for Z in tle2015.txt.zip tle2016.txt.zip tle2017.txt.zip
do
    F="${Z%.*}"
    ./process_tle_2015_2017_.sh ${SRC_DIR} ${TGT_HDFS} $Z $F ${LPF} ${FILTER} &
done 

wait

cd ${SRC_DIR}_tmp

for G in *
do
    echo $G.gz
    gzip $G &
done
wait

for H in *
do
    echo ${TGT_HDFS}/$H
    hdfs dfs -put $H ${TGT_HDFS}/$H
done

rm -Rf ${SRC_DIR}_tmp
