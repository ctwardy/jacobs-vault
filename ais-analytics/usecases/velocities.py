from aisanalytics import VelocityCalculations
from aisanalytics.utilities import cli_arguments

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

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
    AIS_INPUT_TABLE = args.AIS_INPUT_TABLE
    VELOCITIES_OUTPUT_TABLE = args.VELOCITIES_OUTPUT_TABLE

    df = spark.table(AIS_INPUT_TABLE)
    # df = df.limit(300000)
    df.persist()

    # Uncomment this to get the expected output length, useful for sanity 
    # checks and debugging the main functions (note, if subsampling with df.limit, make
    # sure df.persist is uncommented, or else Spark may pull in a separate DF for each part
    initial_table_len = df.count()
    distinct_imo = df.select('imo').distinct().count()
    # num_with_1 = df.groupBy('imo').count().filter(F.col('count')==1).count()
    expected_output_lines = initial_table_len - distinct_imo
    print('Expected output length:',expected_output_lines)

    vel = VelocityCalculations(single_partition_length=10000)

    df = vel.compute_velocities(df)
    # df.persist()
    # initial_table_len = df.count()
    # distinct_imo = df.select('imo').distinct().count()
    # num_with_1 = df.groupBy('imo').count().filter(F.col('count')==1).count()
    # expected_output_lines = initial_table_len - distinct_imo - num_with_1
    # print('Expected length after processing:',expected_output_lines)


    # Uncomment this to compare to the expected output length above
    print('Length after processing:',df.count())

    df.write.saveAsTable(VELOCITIES_OUTPUT_TABLE)

    print('Velocity calculation completed')


if __name__ == "__main__":
    main()
