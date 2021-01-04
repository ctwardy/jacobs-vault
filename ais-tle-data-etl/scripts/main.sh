#!/bin/bash

INPUT_AIS_DIR="/home/cmorris/vault/data/raw/AIS/AIS_ASCII_by_UTM_Month"
OUTPUT_AIS_TABLE="cmorris.af_vault_ais"

INPUT_TLE_DIR="/home/cmorris/vault/data/raw/TLE"
OUTPUT_TLE_TABLE="cmorris.af_vault_tle_2"

HDFS_DIR='/user/cmorris/vault'

SPARK_OPTIONS="--driver-memory 14g --executor-memory 22g"
USECASE_PYSPARK_FILE=usecases/main.py

###### Only edit below here if you know what you are doing... ##############

LOGDIR=logs # log folder name, NOT absolute path, blank to output log in current directory
LOGFILE_NAME='dataetl_sparklog'

SPARK_SUBMIT_LOCATION=submit.sh

SPARK_SUBMIT_LOCATION=$(readlink -f ${SPARK_SUBMIT_LOCATION})
USECASE_PYSPARK_FILE=$(readlink -f ${USECASE_PYSPARK_FILE})

mkdir -p ${LOGDIR}

nohup $SPARK_SUBMIT_LOCATION \
${SPARK_OPTIONS} \
${USECASE_PYSPARK_FILE} \
--input-ais-dir $INPUT_AIS_DIR \
--output-ais-table $OUTPUT_AIS_TABLE \
--input-tle-dir $INPUT_TLE_DIR \
--output-tle-table $OUTPUT_TLE_TABLE \
--hdfs-dir $HDFS_DIR \
&> ${LOGDIR}/${LOGFILE_NAME} &

