#!/bin/bash

AIS_TABLE='cmorris.ais_subset_1000_1200'
TLE_TABLE='cmorris.tle_2015_2017_subset_1000_1200'

SPARK_OPTIONS="--driver-memory 14g --executor-memory 5g"
USECASE_PYSPARK_FILE=usecases/main.py

###### Only edit below here if you know what you are doing... ##############

LOGDIR=logs # log folder name, NOT absolute path, blank to output log in current directory
LOGFILE_NAME='hitdetector_sparklog'

SPARK_SUBMIT_LOCATION=submit.sh

SPARK_SUBMIT_LOCATION=$(readlink -f ${SPARK_SUBMIT_LOCATION})
USECASE_PYSPARK_FILE=$(readlink -f ${USECASE_PYSPARK_FILE})

mkdir -p ${LOGDIR}

nohup $SPARK_SUBMIT_LOCATION \
${SPARK_OPTIONS} \
${USECASE_PYSPARK_FILE} \
--ais-table $AIS_TABLE \
--tle-table $TLE_TABLE \
&> ${LOGDIR}/${LOGFILE_NAME} &

