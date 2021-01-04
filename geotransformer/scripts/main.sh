#!/bin/bash

# GEO_INPUT_TABLE="af_vault.tle_2015_2017"
GEO_INPUT_TABLE="cmorris.af_vault_tle"
# GEO_OUTPUT_TABLE="cmorris.tle_geo_test_w_sgp4_astropy_v2"
# GEO_OUTPUT_TABLE="af_vault.tle_2015_2017_geo_sgp4_astropy"
GEO_OUTPUT_TABLE="cmorris.af_vault_tle_params_fixed_v2"
SPARK_OPTIONS="--driver-memory 14g --executor-memory 20g" # --num-executors 10"
USECASE_PYSPARK_FILE=usecases/main.py

###### Only edit below here if you know what you are doing... ##############

LOGDIR=logs # log folder name, NOT absolute path, blank to output log in current directory
LOGFILE_NAME='geotransformer_sparklog'

SPARK_SUBMIT_LOCATION=submit.sh

SPARK_SUBMIT_LOCATION=$(readlink -f ${SPARK_SUBMIT_LOCATION})
USECASE_PYSPARK_FILE=$(readlink -f ${USECASE_PYSPARK_FILE})

mkdir -p ${LOGDIR}

nohup $SPARK_SUBMIT_LOCATION \
${SPARK_OPTIONS} \
${USECASE_PYSPARK_FILE} \
--geo-input-table $GEO_INPUT_TABLE \
--geo-output-table $GEO_OUTPUT_TABLE \
&> ${LOGDIR}/${LOGFILE_NAME} &

