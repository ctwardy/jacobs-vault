import sys
sys.path.append('..')

from osgeo import ogr

# from dataetl import DataETL
from dataetl.gdb import GDBETL
from dataetl.utilities import cli_arguments

from pyspark.sql import SparkSession

SINGLE_RECORD_SIZE = 100_000

# def main():
    
    # Parse in command line arguments
    args = cli_arguments()

    print("Instantiating etl object")

    etl = GDBETL(args, single_record_size=SINGLE_RECORD_SIZE)

    # Initiate a Spark session
    # spark = (
    #             SparkSession
    #                 .builder
    #                 .appName("gdb-data-etl")
    #                 .enableHiveSupport()
    #                 .getOrCreate()
    #         )



    # ETL the AIS data
    print("Running ETL object.")
    etl.run(layer_index=0)

    # spark.stop()

    print("GDB Process Complete")
    # ETL the TLE data


# if __name__ == "__main__":
#     main()
