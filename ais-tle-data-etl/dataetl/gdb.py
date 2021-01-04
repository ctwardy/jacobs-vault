import os
import subprocess
import json

from multiprocessing import Pool

import numpy as np
import pandas as pd

from osgeo import ogr

from pyspark.sql.types import StructType, StructField, StringType

# Increment this version number when there is a new release:
__author__  = 'Christopher Morris'
__email__   = 'christopher.morris@jacobs.com'
__version__ = '0.1.0'


class GDBETL:
    def __init__(self, args, single_record_size=100_000):
        self.args = args

        self.single_record_size = single_record_size
        driver = ogr.GetDriverByName("OpenFileGDB")
        print("Input GDB directory:", args.INPUT_GDB_DIR)
        self.ds = driver.Open(args.INPUT_GDB_DIR)

        layer_counts = self.ds.GetLayerCount()
        self.layer_strings = [(i, self.ds.GetLayerByIndex(i).GetDescription()) for i in range(layer_counts)]

        print("Layers:")
        print(self.layer_strings)

        # self.broadcast = self.ds.GetLayerByIndex(0)
        # self.vessel    = self.ds.GetLayerByIndex(1)
        # self.voyage    = self.ds.GetLayerByIndex(2)

    def run(self, layer_index=0):
        # Get the current GDB layer we are working
        layer = self.ds.GetLayerByIndex(layer_index)
        layer_string = self.layer_strings[layer_index][1]

        # Create the name of the local output directory, make it if it doesn't exist
        local_out_dir = os.path.join(self.args.OUTPUT_LOCAL_GDB_DIR, layer_string)

        if not os.path.exists(local_out_dir):
            os.makedirs(local_out_dir, exist_ok=True)

        layer_size = layer.GetFeatureCount()
        layer_size = 300_000

        print("Total layer size:", layer_size)
        print("Single record size:", self.single_record_size)

        start_indices = [start_index for start_index in range(1, layer_size+1, self.single_record_size)]
        
        def process_dataset_part(start_index):
            print("Starting at index:", start_index)

            layer.SetNextByIndex(start_index)

            output = []
            for _ in range(self.single_record_size):
                data_point = layer.GetNextFeature()
                if data_point is None:
                    break
                output.append(data_point.ExportToJson())

            df = pd.json_normalize([json.loads(x) for x in output])

            df['lon'] = df['geometry.coordinates'].map(lambda x: x[0])
            df['lat'] = df['geometry.coordinates'].map(lambda x: x[1])

            df = df.drop('geometry.coordinates', axis=1)

            current_output_file = os.path.join(local_out_dir, f'data_{start_index}.csv')
            df.to_csv(current_output_file, index=False)

        # for start_index in range(1, layer_size+1, self.single_record_size):
        
        #     print("Starting at index:", start_index)

        #     layer.SetNextByIndex(start_index)

        #     output = []
        #     for _ in range(self.single_record_size):
        #         data_point = layer.GetNextFeature()
        #         if data_point is None:
        #             break
        #         output.append(data_point.ExportToJson())

        #     df = pd.json_normalize([json.loads(x) for x in output])

        #     df['lon'] = df['geometry.coordinates'].map(lambda x: x[0])
        #     df['lat'] = df['geometry.coordinates'].map(lambda x: x[1])

        #     df = df.drop('geometry.coordinates', axis=1)

        #     current_output_file = os.path.join(local_out_dir, f'data_{start_index}.csv')
        #     df.to_csv(current_output_file, index=False)