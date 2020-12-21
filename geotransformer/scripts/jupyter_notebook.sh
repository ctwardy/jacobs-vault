#!/bin/bash

SPARK_OPTIONS="--driver-memory 10g --executor-memory 10g"
JUPYTER_DEFAULT_PORT="8898"

###### Only edit below here if you know what you are doing... ##############

maindir=$(pwd)
conda_env="environment"
project_namespace="geotransformer"

driver_python="${conda_env}/bin/jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --port=${JUPYTER_DEFAULT_PORT}"
archived_python="${conda_env}_zip/${conda_env}/bin/python"

pyspark \
--conf spark.pyspark.driver.python=${driver_python} \
--conf spark.pyspark.python=${archived_python} \
--archives ${maindir}/${conda_env}.zip#${conda_env}_zip \
--py-files ${maindir}/${project_namespace}.zip \
${SPARK_OPTIONS}
