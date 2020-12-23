#!/bin/bash

# AIS_INPUT_TABLE="cmorris.ais_subset_1000_1100"
AIS_INPUT_TABLE="af_vault.ais"
VELOCITIES_OUTPUT_TABLE="af_vault.ais_velocities"

SPARK_OPTIONS="--driver-memory 14g --executor-memory 5g"
USECASE_PYSPARK_FILE=usecases/velocities.py

###### Only edit below here if you know what you are doing... ##############

LOGDIR=logs # log folder name, NOT absolute path, blank to output log in current directory
LOGFILE_NAME='aisanalytics_sparklog'

SPARK_SUBMIT_LOCATION=submit.sh

SPARK_SUBMIT_LOCATION=$(readlink -f ${SPARK_SUBMIT_LOCATION})
USECASE_PYSPARK_FILE=$(readlink -f ${USECASE_PYSPARK_FILE})

mkdir -p ${LOGDIR}

nohup $SPARK_SUBMIT_LOCATION \
${SPARK_OPTIONS} \
${USECASE_PYSPARK_FILE} \
--ais-input-table $AIS_INPUT_TABLE \
--velocities-output-table $VELOCITIES_OUTPUT_TABLE \
&> ${LOGDIR}/${LOGFILE_NAME} &

