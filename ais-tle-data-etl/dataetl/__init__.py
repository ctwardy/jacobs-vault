import os
import subprocess

import numpy as np
import pandas as pd

from pyspark.sql.types import StructType, StructField, StringType

# Increment this version number when there is a new release:
__author__  = 'Christopher Morris'
__email__   = 'christopher.morris@jacobs.com'
__version__ = '0.1.0'


class DataETL:
    def __init__(self, args):
        self.args = args

    def etl_ais_data(self, spark):
        INPUT_AIS_DIR = self.args.INPUT_AIS_DIR
        HDFS_DIR = self.args.HDFS_DIR
        OUTPUT_AIS_TABLE = self.args.OUTPUT_AIS_TABLE

        df = pd.DataFrame()
        for rootdir, subdir, files in os.walk(INPUT_AIS_DIR):
            for filename in files:
                if '.csv' in filename:
                    # print(os.path.join(rootdir, filename))
                    current_csv = os.path.join(rootdir, filename)
                    pdf = pd.read_csv(current_csv)
                    pdf['filename'] = current_csv

                    df = pd.concat((df, pdf))

        for column in df.columns:
            df[column] = df[column].astype('str')

        print("Final df shape before spark:", df.shape)
        combined_csv_path = os.path.join(INPUT_AIS_DIR,'..','combined_ais.csv')
        combined_csv_path = os.path.abspath(combined_csv_path)

        df.to_csv(combined_csv_path, index=False)

        subprocess.call(['hdfs','dfs','-put',combined_csv_path, HDFS_DIR])

        sdf = spark.read.csv(os.path.join(HDFS_DIR, 'combined_ais.csv'), header=True)
        sdf.write.saveAsTable(OUTPUT_AIS_TABLE)

        # schema = StructType([StructField(colname, StringType(), True) for colname in df.columns])

        # sdf = spark.createDataFrame(df, schema)
        # sdf.write.saveAsTable(OUTPUT_AIS_TABLE)

    def etl_tle_data(self, spark):
        INPUT_TLE_DIR = self.args.INPUT_TLE_DIR
        HDFS_DIR = self.args.HDFS_DIR
        OUTPUT_TLE_TABLE = self.args.OUTPUT_TLE_TABLE

        df = pd.DataFrame()
        for rootdir, subdir, files in os.walk(INPUT_TLE_DIR):
            for filename in files:
                if '.txt' in filename:
                    # print(os.path.join(rootdir, filename))
                    current_file = os.path.join(rootdir, filename)
                    
                    with open(current_file, 'r', errors='replace') as f:
                        data = f.readlines()
                    
                    output = [data[2*i:2*i+2] for i in range(len(data)//2)]

                    pdf = pd.DataFrame(output, columns=['line1','line2'])

                    pdf['line1'] = pdf['line1'].map(lambda x: x.replace('\n','').replace('\\',''))
                    pdf['line2'] = pdf['line2'].map(lambda x: x.replace('\n','').replace('\\',''))

                    pdf['filename'] = current_file

                    print(current_file, pdf.shape)

                    df = pd.concat((df, pdf))

        for column in df.columns:
            df[column] = df[column].astype('str')

        print("Final df shape before spark:", df.shape)
        combined_csv_path = os.path.join(INPUT_TLE_DIR,'..','combined_tle.csv')
        combined_csv_path = os.path.abspath(combined_csv_path)
        
        df.to_csv(combined_csv_path, index=False)

        subprocess.call(['hdfs','dfs','-put',combined_csv_path, HDFS_DIR])

        sdf = spark.read.csv(os.path.join(HDFS_DIR, 'combined_tle.csv'), header=True)
        sdf = sdf.repartition(20)
        sdf.write.saveAsTable(OUTPUT_TLE_TABLE)

        # schema = StructType([StructField(colname, StringType(), True) for colname in df.columns])

        # sdf = spark.createDataFrame(df, schema)
        # sdf.write.saveAsTable(OUTPUT_AIS_TABLE)
