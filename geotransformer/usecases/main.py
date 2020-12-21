from geotransformer import GeoTransformer
from geotransformer.utilities import cli_arguments

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

def main():
    # Initiate a Spark session
    spark = (
                SparkSession
                    .builder
                    .appName("geotransformer")
                    .enableHiveSupport()
                    .getOrCreate()
            )

    args = cli_arguments()

    GEO_INPUT_TABLE = args.GEO_INPUT_TABLE
    GEO_OUTPUT_TABLE = args.GEO_OUTPUT_TABLE

    df = spark.table(GEO_INPUT_TABLE)
    # df = df.withColumn('')
    df.show()

    gt = GeoTransformer()
    
    df = gt.generate_lat_long(df)

    # df.show(truncate=False)

    df.write.saveAsTable(GEO_OUTPUT_TABLE, mode='overwrite')

    print("Geo extraction completed.")


if __name__ == "__main__":
    main()
