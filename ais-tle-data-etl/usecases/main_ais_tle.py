

from dataetl import DataETL
from dataetl.utilities import cli_arguments


from pyspark.sql import SparkSession

def main():
    

    # Parse in command line arguments
    args = cli_arguments()
    
    print("Main running")
    # etl = DataETL(args)

    # # Initiate a Spark session
    # spark = (
    #             SparkSession
    #                 .builder
    #                 .appName("ais-tle-data-etl")
    #                 .enableHiveSupport()
    #                 .getOrCreate()
    #         )

    # # ETL the AIS data
    # # etl.etl_ais_data(spark)

    # # ETL the AIS data
    # etl.etl_tle_data(spark)

    # spark.stop()

    # # ETL the TLE data


if __name__ == "__main__":
    main()
