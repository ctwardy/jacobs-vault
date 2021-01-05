#!/bin/bash

# INPUT_GDB_DIR="/home/cmorris/vault/data/raw/AIS/Zone10_2013_01.gdb"
INPUT_GDB_DIR="/home/cmorris/vault/data/raw/AIS/Zone10_2009_01.gdb"
OUTPUT_LOCAL_GDB_DIR="/home/cmorris/vault/data/processed/gdb_fixed"
mkdir -p $OUTPUT_LOCAL_GDB_DIR

export PROJ_LIB=$INPUT_GDB_DIR
# export HADOOP_CONF_DIR=/etc/hadoop/conf
export HADOOP_CONF_DIR=/etc/spark/conf/yarn-conf/*:/etc/hive/conf:/etc/hive/conf

OUTPUT_GDB_TABLE="cmorris.gdb_ais_fixed"

HDFS_DIR='/user/cmorris/vault/gdb_fixed'
hdfs dfs -mkdir -p $HDFS_DIR

SPARK_OPTIONS="--driver-memory 14g --executor-memory 22g"
USECASE_PYSPARK_FILE=usecases/main.py

###### Only edit below here if you know what you are doing... ##############

LOGDIR=logs # log folder name, NOT absolute path, blank to output log in current directory
LOGFILE_NAME='dataetl_sparklog'

SPARK_SUBMIT_LOCATION=submit.sh

SPARK_SUBMIT_LOCATION=$(readlink -f ${SPARK_SUBMIT_LOCATION})
USECASE_PYSPARK_FILE=$(readlink -f ${USECASE_PYSPARK_FILE})

mkdir -p ${LOGDIR}

echo $SPARK_SUBMIT_LOCATION
echo $SPARK_OPTIONS
echo $USECASE_PYSPARK_FILE

nohup $SPARK_SUBMIT_LOCATION \
${SPARK_OPTIONS} \
${USECASE_PYSPARK_FILE} \
--input-gdb-dir $INPUT_GDB_DIR \
--output-local-gdb-dir $OUTPUT_LOCAL_GDB_DIR \
--output-gdb-table $OUTPUT_GDB_TABLE \
--hdfs-dir $HDFS_DIR \
&> ${LOGDIR}/${LOGFILE_NAME} &

