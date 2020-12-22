#!/bin/bash

SPARK_OPTIONS="--driver-memory 10g --executor-memory 10g"

###### Only edit below here if you know what you are doing... ##############

conda_env="environment"
project_namespace="aisanalytics"

driver_python="${conda_env}/bin/ipython"
archived_python="${conda_env}_zip/${conda_env}/bin/python"

pyspark \
--conf spark.pyspark.driver.python=${driver_python} \
--conf spark.pyspark.python=${archived_python} \
--archives ${conda_env}.zip#${conda_env}_zip \
--py-files ${project_namespace}.zip \
${SPARK_OPTIONS}