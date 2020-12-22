from aisanalytics import VelocityCalculations
from aisanalytics.utilities import cli_arguments

from pyspark.sql import SparkSession

def main():
    # Initiate a Spark session
    spark = (
                SparkSession
                    .builder
                    .appName("ais-analytics")
                    .enableHiveSupport()
                    .getOrCreate()
            )

    args = cli_arguments()
    
    # Run package code
    message = VelocityCalculations().run()
    print(message)


if __name__ == "__main__":
    main()
