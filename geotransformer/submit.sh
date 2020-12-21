#!/bin/bash

# This script is a stand-in for spark-submit preconfigured with the arguments
# necessary to run Spark jobs with a custom Conda environment. Pass all other
# spark-submit arguments to this script as you would normally do.

conda_env="environment"
project_namespace="geotransformer"
deploy_mode="client"

driver_python="${conda_env}/bin/python3"
archived_python="${conda_env}_zip/${driver_python}"
other_args="$@"

if [ "$deploy_mode" = "client" ]; then
    spark-submit \
    --deploy-mode client \
    --conf spark.pyspark.driver.python=${driver_python} \
    --conf spark.pyspark.python=${archived_python} \
    --archives ${conda_env}.zip#${conda_env}_zip \
    --py-files ${project_namespace}.zip \
    $other_args
elif [ "$deploy_mode" = "cluster" ]; then
    spark-submit \
    --deploy-mode cluster \
    --conf spark.pyspark.python=${archived_python} \
    --archives ${conda_env}.zip#${conda_env}_zip \
    --py-files ${project_namespace}.zip \
    $other_args
elif [ "$deploy_mode" = "local" ]; then
    spark-submit \
    --master local \
    --conf spark.pyspark.driver.python=${driver_python} \
    --conf spark.pyspark.python=${driver_python} \
    --py-files ${project_namespace}.zip \
    $other_args
else
    echo "Deploy mode not specified"
fi
