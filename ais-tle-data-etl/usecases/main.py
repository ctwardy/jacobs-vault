import os
import subprocess
import json
from time import perf_counter

from multiprocessing import Pool

import numpy as np
import pandas as pd

from osgeo import ogr

from dataetl import DataETL
# from dataetl.gdb import GDBETL
from dataetl.utilities import cli_arguments

from pyspark.sql import SparkSession
from pyspark.sql.types import *

SINGLE_RECORD_SIZE = 100_000

# def main():

args = cli_arguments()

print("Instantiating etl object")

# etl = GDBETL(args, single_record_size=SINGLE_RECORD_SIZE)





# # ETL the AIS data
# print("Running ETL object.")
# etl.run(layer_index=0)

# # spark.stop()

# print("GDB Process Complete")
# # ETL the TLE data

##############################################################################################

def process_dataset_part(start_index):
    driver = ogr.GetDriverByName("OpenFileGDB")
    ds = driver.Open(args.INPUT_GDB_DIR)
    # Get the current GDB layer we are working
    layer = ds.GetLayerByIndex(layer_index)

    # start_index, stop_index = index_pair
    print("Starting at index:", start_index)
    
    layer.SetNextByIndex(start_index)

    output = []
    for _ in range(SINGLE_RECORD_SIZE):
        data_point = layer.GetNextFeature()
        if data_point is None:
            break
        output.append(data_point.ExportToJson())

    df = pd.json_normalize([json.loads(x) for x in output])

    if 'geometry.coordinates' in df.columns:
        df['lon'] = df['geometry.coordinates'].map(lambda x: x[0])
        df['lat'] = df['geometry.coordinates'].map(lambda x: x[1])

        df = df.drop('geometry.coordinates', axis=1)

    current_output_file = os.path.join(local_out_dir, f'data_{start_index}.csv')
    df.to_csv(current_output_file, index=False)


print("Input GDB directory:", args.INPUT_GDB_DIR)

input_zone_name = os.path.basename(os.path.normpath(args.INPUT_GDB_DIR))
input_zone_name = input_zone_name.split('.')[0]

driver = ogr.GetDriverByName("OpenFileGDB")
ds = driver.Open(args.INPUT_GDB_DIR)

layer_counts = ds.GetLayerCount()
layer_strings = [(i, ds.GetLayerByIndex(i).GetDescription()) for i in range(layer_counts)]
layer_strings = [x[1].split('_')[-1] for x in layer_strings]
layer_indices = [i for i in range(layer_counts)]

print("Layers:")
print(layer_strings)

# layer_index = 0
# for layer_index in [0]:
# for layer_index in [1,2]:
for layer_index in layer_indices:
    start = perf_counter()

    layer_string = layer_strings[layer_index]#[1]

    # Create the name of the local output directory, make it if it doesn't exist
    local_out_dir = os.path.join(args.OUTPUT_LOCAL_GDB_DIR, input_zone_name, layer_string)
    if not os.path.exists(local_out_dir):
            os.makedirs(local_out_dir, exist_ok=True)

    layer = ds.GetLayerByIndex(layer_index)
    layer_size = layer.GetFeatureCount()
    # layer_size = 300_000

    print("Total layer size:", layer_size)
    print("Single record size:", SINGLE_RECORD_SIZE)

    # start_indices = [(start_index, start_index + SINGLE_RECORD_SIZE) for start_index in range(0, layer_size, SINGLE_RECORD_SIZE)]
    start_indices = [start_index for start_index in range(0, layer_size, SINGLE_RECORD_SIZE)]
    # start_indices[0] = 0

    agents = 20
    chunksize = 3

    with Pool(processes=agents) as pool:
        pool.map(process_dataset_part, start_indices, chunksize=chunksize)

    end = perf_counter()
    execution_time = (end - start)
    print("Execution time:", execution_time)

    def run_cmd(args_list):
        """
        run linux commands
        """
        # import subprocess
        print('Running system command: {0}'.format(' '.join(args_list)))
        proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        s_output, s_err = proc.communicate()
        s_return =  proc.returncode
        return s_return, s_output, s_err 

    hdfs_save_dir = os.path.join(args.HDFS_DIR, input_zone_name, layer_string)
    
    hdfs_zone_dir = os.path.join(args.HDFS_DIR, input_zone_name)

    subprocess.call(['hdfs', 'dfs', '-mkdir', '-p', hdfs_zone_dir])
    (ret, out, err)= run_cmd(['hdfs', 'dfs', '-put', local_out_dir, hdfs_zone_dir])
    print('ret',ret)
    print('out',out)
    print('err',err)

    # Initiate a Spark session
    spark = (
                SparkSession
                    .builder
                    .appName("gdb-data-etl")
                    .enableHiveSupport()
                    .getOrCreate()
            )

    # schema = StructType(
    #     [StructField('type', StringType(), True),
    #     StructField('id', StringType(), True),
    #     StructField('geometry.type', StringType(), True),
    #     StructField('properties.SOG', FloatType(), True),
    #     StructField('properties.COG', FloatType(), True),
    #     StructField('properties.Heading', FloatType(), True),
    #     StructField('properties.ROT', FloatType(), True),
    #     StructField('properties.BaseDateTime', StringType(), True),
    #     StructField('properties.Status', StringType(), True),
    #     StructField('properties.VoyageID', StringType(), True),
    #     StructField('properties.MMSI', StringType(), True),
    #     StructField('properties.ReceiverType', StringType(), True),
    #     StructField('properties.ReceiverID', StringType(), True),
    #     StructField('lon', FloatType(), True),
    #     StructField('lat', FloatType(), True)]
    # )

    df = spark.read.csv(hdfs_save_dir, header=True)#schema=schema, inferSchema=False)
    # df = spark.read.format("csv").option("header", "true").load(hdfs_save_dir)
    # for column in df.columns:
    #     df = df.withColumnRenamed(column, column.split('.')[-1])

    df.write.saveAsTable(f'{args.OUTPUT_GDB_TABLE}_{input_zone_name}_{layer_string}', mode='overwrite')

    print("GDB Process Complete")

    spark.stop()

# if __name__ == "__main__":
#     main()
