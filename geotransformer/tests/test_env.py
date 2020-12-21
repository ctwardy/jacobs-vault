""""Test to see if the driver and executors are using the same environment"""
import argparse
from importlib import import_module
import os
import sys

from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType


def get_module_version(module_name):
    """Dynamically import a module and return its version if possible"""
    try:
        module = import_module(module_name)
        version = module.__version__
    except ModuleNotFoundError:
        version = "NULL"

    return version


def main():
    """Run all tests and display the results at the end"""

    # Parse command line arguments:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output-table",
        "-o",
        dest="OUTPUT_TABLE",
        default=None,
        help="If set, results will be written to HIVE at this location.",
    )

    args = parser.parse_args()

   # We will try to dynamically import the following list of modules:
    modules_to_test = [
        "numpy",
        "pandas",
        "sklearn",
        "geotransformer",
    ]

    # Get the versions of modules currently installed on the driver node:
    driver_versions = {}
    for module_name in modules_to_test:
        driver_versions.update({module_name: get_module_version(module_name)})

    # Defined a UDF to return the module versions installed on the executors:
    get_executor_module_version = udf(get_module_version, StringType())

    # Start Spark:
    spark = SparkSession.builder.enableHiveSupport().getOrCreate()
    context = SQLContext(spark.sparkContext)

    # Create a DataFrame with the modules and their versions on the driver:
    versions_df = context.createDataFrame(
        driver_versions.items(),
        ["module_name", "driver_version"],
    )

    # Run the UDF and store the executor versions in a new column:
    versions_df = versions_df.withColumn(
        "executor_version",
        get_executor_module_version(versions_df.module_name),
    )

    # Create a temporary DataFrame just for running other UDFs:
    temporary_df = context.createDataFrame([()], [])

    # Define a UDF to get the contents of the current directory on executors:
    get_executor_directory_contents = udf(
        lambda: " ".join(os.listdir(".")),
        StringType(),
    )

    # Run the UDF in order to see the results on the executor nodes:
    temporary_df = temporary_df.withColumn(
        "directory_contents",
        get_executor_directory_contents(),
    )

    # Bring the data back onto the driver to display:
    executor_directory_contents = temporary_df.collect()[0].directory_contents

    # Define a UDF to get the contents of the current directory on executors:
    get_executor_path_contents = udf(
        lambda: " ".join(sys.path),
        StringType(),
    )

    # Run the UDF in order to see the results on the executor nodes:
    temporary_df = temporary_df.withColumn(
        "path_contents",
        get_executor_path_contents(),
    )

    # Bring the data back onto the driver to display:
    executor_path_contents = temporary_df.collect()[0].path_contents

    # Display the results or write to a table:
    if args.OUTPUT_TABLE:
        versions_df.write.saveAsTable(args.OUTPUT_TABLE, mode="overwrite")
    else:
        print(f"Executor directory contents: {executor_directory_contents}\n")
        print(f"Executor path contents: {executor_path_contents}\n")
        versions_df.show(100, False)


if __name__ == "__main__":
    main()
