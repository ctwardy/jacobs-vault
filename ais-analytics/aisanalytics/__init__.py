from datetime import datetime
from time import perf_counter

from geopy import distance

from pyspark.sql.window import Window
import pyspark.sql.functions as F
from pyspark.sql.types import FloatType, ArrayType, StructType, StructField, StringType

# Increment this version number when there is a new release:
__author__  = 'Christopher Morris'
__email__   = 'christopher.morris@jacobs.com'
__version__ = '0.1.0'


class VelocityCalculations:
    def __init__(self, single_partition_length=100):
        self.single_partition_length = single_partition_length

    def compute_velocities(self, df, ):
        # Select the columns relevant for computation
        df = df.select('imo', 'basedatetime', 'lat', 'lon')

        # Pull lat and lon together into a tuple structure
        df = df.withColumn('latlon', F.struct('lat', 'lon'))

        # Create the Spark Window that allows the data to be ordered within each IMO
        w = Window.orderBy('basedatetime').partitionBy('imo')

        # These index columns help create groupings of latlons within an individual IMO
        df = df.withColumn('index', F.row_number().over(w))
        df = df.withColumn('index_previous', F.lag(df['index']).over(w))

        # Create lagged pairs of lat-lon and basedatetime
        df = df.withColumn('latlon_previous', F.lag(df['latlon']).over(w))
        df = df.withColumn('basedatetime_previous', F.lag(df['basedatetime']).over(w))

        df = df.withColumn('latlon_pair', F.struct(df['latlon_previous'], df['latlon']))
        df = df.withColumn('basedatetime_pair', F.struct(df['basedatetime_previous'], df['basedatetime']))

        # print(df.count())
        df = df.filter(df['latlon_previous'].isNotNull())
        # print(df.count())
        # should be a drop of 22 for this test table, which has 22 distinct vessels

        # Find the total volume for each IMO
        # dfg = df.groupBy('imo').agg(F.max('index_previous').alias('total_rows'))
        
        # Collect lists of these records, to make the PySpark UDF more efficient, as 
        # these UDFs operate more quickly the more data that can be pushed into a single instance
        df = df.withColumn('group_id', F.floor(df['index_previous'] / self.single_partition_length))

        # Create lists for faster operation in the UDF
        df = df.groupBy('imo', 'group_id').agg(F.collect_list(F.col('latlon_pair')).alias('latlon_pair'),
                                               F.collect_list(F.col('basedatetime_pair')).alias('basedatetime_pair'))
        num_partitions = df.count()
        df = df.repartition(num_partitions)
        # df.show()

        def dist_time_vel(latlon_previous, latlon, basedatetime_previous, basedatetime):
            """From lat-lon pairs at two timestamps, calculate the distnace,
            time, and average velocity traveled.
            """
            
            error = "No error"
            try:
                dist = distance.distance(latlon_previous, latlon).km
            except Exception as e:
                error = str(e)
                dist = float('NaN')

            try:
                t0 = datetime.fromisoformat(basedatetime_previous)
                t1 = datetime.fromisoformat(basedatetime)
                delta_hrs = (t1 - t0).total_seconds() / 60 / 60
            except Exception as e:
                error = str(e)
                delta_hrs = float('NaN')

            try:
                velocity = dist / delta_hrs
            except Exception as e:
                error = str(e)
                velocity = float('NaN')

            

            return (dist, delta_hrs, velocity, error)

        def dist_time_vel_list(latlon_pair_list, basedatetime_pair_list):
            """This function is set up as a PySpark UDF that operates
            over lists. This increases the function of the UDF, by purposefully
            bringing more data locally for each Spark executor.
            """
            start = perf_counter()
            
            dist_list, delta_hrs_list, velocity_list, error_list = [], [], [], []
            for i, _ in enumerate(latlon_pair_list):
                latlon_previous = latlon_pair_list[i][0]
                latlon = latlon_pair_list[i][1]
                basedatetime_previous = basedatetime_pair_list[i][0]
                basedatetime = basedatetime_pair_list[i][1]

                dist, delta_hrs, velocity, error = dist_time_vel(latlon_previous,
                                                                                 latlon,
                                                                                 basedatetime_previous,
                                                                                 basedatetime)

                

                dist_list.append(dist)
                delta_hrs_list.append(delta_hrs)
                velocity_list.append(velocity)
                error_list.append(error)

            end = perf_counter()
            execution_time = (end - start)

            return (dist_list, delta_hrs_list, velocity_list, error_list, execution_time)

        # Register the UDF and its schema
        schema = StructType([
                    StructField("distance_km", ArrayType(FloatType()), True),
                    StructField("delta_hrs", ArrayType(FloatType()), True),
                    StructField("velocities_kph", ArrayType(FloatType()), True),
                    StructField("error", ArrayType(StringType()), True),
                    StructField("execution_time", FloatType(), True),
                ])

        dist_time_vel_udf = F.udf(dist_time_vel_list, schema)

        # Compute the UDF value for each
        df = df.withColumn('combined_output', dist_time_vel_udf(
                                                                'latlon_pair',
                                                                'basedatetime_pair',
                                                            ))

        # Extract the desired columns, and undo the list creation from 
        # earlier that allowed for more efficient PySpark calculation
        extract_cols = ['distance_km', 'delta_hrs', 'velocities_kph', 'error']
        for column in extract_cols + ['execution_time']:
            df = df.withColumn(column, df['combined_output'].getItem(column))
            
        df = df.drop('lat','lon','combined_output')
        
        zipcols = extract_cols + ['latlon_pair', 'basedatetime_pair']
        df = df.withColumn('tmp', F.arrays_zip(*zipcols))
        df = df.withColumn('tmp', F.explode('tmp'))
        df = df.drop(*zipcols)

        for output_column in zipcols:
            df = df.withColumn(output_column, F.col('tmp').getItem(output_column))

        df = df.drop('tmp')

        df = df.withColumn('latlon_previous', df['latlon_pair'].getItem('latlon_previous'))
        df = df.withColumn('latlon', df['latlon_pair'].getItem('latlon'))
        df = df.withColumn('basedatetime_previous', df['basedatetime_pair'].getItem('basedatetime_previous'))
        df = df.withColumn('basedatetime', df['basedatetime_pair'].getItem('basedatetime'))

        df = df.withColumnRenamed('basedatetime_previous','t_start')
        df = df.withColumnRenamed('basedatetime','t_end')

        df = df.withColumn('lat_start', df['latlon_previous'].getItem('lat'))
        df = df.withColumn('lon_start', df['latlon_previous'].getItem('lon'))

        df = df.withColumn('lat_end', df['latlon'].getItem('lat'))
        df = df.withColumn('lon_end', df['latlon'].getItem('lon'))

        df = df.select(
                    'imo',
                    't_start',
                    't_end',
                    'lat_start',
                    'lon_start',
                    'lat_end',
                    'lon_end',
                    'distance_km',
                    'delta_hrs',
                    'velocities_kph',
                    'error',
                    'execution_time'
                    )

        return df
