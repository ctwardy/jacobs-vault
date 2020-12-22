from datetime import datetime
import math
from time import perf_counter

import numpy as np

import pyspark.sql.functions as F
from pyspark.sql.types import FloatType, ArrayType, StructType, StructField, StringType

import ephem

from sgp4.api import Satrec
from sgp4.api import SGP4_ERRORS
from astropy.time import Time
from astropy.coordinates import TEME, CartesianDifferential, CartesianRepresentation
from astropy import units as u
from astropy.coordinates import ITRS

# Increment this version number when there is a new release:
__author__  = 'Christopher Morris'
__email__   = 'christopher.morris@jacobs.com'
__version__ = '0.1.0'



class GeoTransformer:
    def __init__(self, single_partition_length=100):
        self.single_partition_length = single_partition_length

    def generate_lat_long_pyephem(self, df):
        def find_lat_long(linename, linedate, line1, line2):

            line1 = line1.replace('\\','')
            line2 = line2.replace('\\','')

            linedate = datetime.strptime(linedate, "%Y-%m-%d %H:%M:%S")

            try:
                tle_rec = ephem.readtle(linename, line1, line2)
                tle_rec.compute(linedate)
                lat, lon, elev, error = math.degrees(tle_rec.sublat), math.degrees(tle_rec.sublong), tle_rec.elevation, "No error"
            except ValueError as current_error:
                lat, lon, elev = 0.0, 0.0, 0.0
                error = "ValueError: " + str(current_error)
            except RuntimeError as current_error:
                lat, lon, elev = 0.0, 0.0, 0.0
                error = "RuntimeError: " + str(current_error)

            return (lat, lon, elev, error)

        schema = StructType([
            StructField("lat", FloatType(), True),
            StructField("lon", FloatType(), True),
            StructField("elev", FloatType(), True),
            StructField("error", StringType(), True) 
        ])
        find_lat_long_udf = F.udf(find_lat_long, schema)

        df = df.withColumn('combined_output', find_lat_long_udf('satellite', 'dt', 'line1', 'line2'))

        df = df.withColumn('lat', df['combined_output'].getItem('lat'))
        df = df.withColumn('lon', df['combined_output'].getItem('lon'))
        df = df.withColumn('elev', df['combined_output'].getItem('elev'))
        df = df.withColumn('error', df['combined_output'].getItem('error'))

        return df

    def generate_lat_long_astropy(self, df):
        
        def find_lat_long(linename_list, linedate_list, line1_list, line2_list):

            start = perf_counter()

            line1_list = [line1.replace('\\','') for line1 in line1_list]
            line2_list = [line2.replace('\\','') for line2 in line2_list]

            linedate_list = [linedate.replace(' ','T') + "Z" for linedate in linedate_list]

            satellites = [Satrec.twoline2rv(line1_list[i], line2_list[i]) for i, _ in enumerate(line1_list)]

            t = [Time(current_time, format='isot', scale='utc') for current_time in linedate_list]

            tv = [satellite.sgp4(t[i].jd1, t[i].jd2) for i, satellite in enumerate(satellites)]  # in km and km/s
            tv = [[elem[0], elem[1][0], elem[1][1], elem[1][2], elem[2][0], elem[2][0], elem[2][1], elem[2][2]] for elem in tv]
            tv = np.array(tv)

            teme_p = CartesianRepresentation(tv[:,1]*u.km, y=tv[:,2]*u.km, z=tv[:,3]*u.km)
            teme_v = CartesianDifferential(tv[:,4]*u.km/u.s, d_y=tv[:,4]*u.km/u.s, d_z=tv[:,4]*u.km/u.s)
            teme = TEME(teme_p.with_differentials(teme_v), obstime=t)

            itrs = teme.transform_to(ITRS(obstime=t))
            location = itrs.earth_location
            lat, lon, elev = location.lat.deg, location.lon.deg, location.height.value
            lat = [float(x) for x in lat]
            lon = [float(x) for x in lon]
            elev = [float(x) for x in elev]

            error_codes = tv[:,0]
            error_codes = ["No error" if error_code==0 else SGP4_ERRORS[error_code] for error_code in error_codes]
            
            end = perf_counter()

            execution_time = (end - start)

            return (lat, lon, elev, error_codes, execution_time)

        schema = StructType([
            StructField("lat", ArrayType(FloatType()), True),
            StructField("lon", ArrayType(FloatType()), True),
            StructField("elev", ArrayType(FloatType()), True),
            StructField("error", ArrayType(StringType()), True),
            StructField("execution_time", FloatType(), True),
        ])

        find_lat_long_udf = F.udf(find_lat_long, schema)

        df_len = df.count()
        num_groups = df_len // self.single_partition_length
        num_groups = max(num_groups, 1) # there must be at least one group

        # Randomly assign DataFrame rows to groups
        dfg = df.withColumn(
            "group_id",
            (num_groups * F.rand()).cast('int').cast('string')
        )

        dfg = dfg.repartition(num_groups)

        extra_columns_list = ['ts','satellite','dt','line1','line2']

        # Collapse the rows of the DataFrame into lists based on group_id.
        # Only include extra columns if specified.
        dfg = dfg.groupBy("group_id").agg(*[
            F.collect_list(column_name).alias(column_name)
            for column_name in (
                extra_columns_list
            )
        ])

        dfout = dfg.withColumn('combined_output', find_lat_long_udf('satellite', 'dt', 'line1', 'line2'))

        dfout = dfout.withColumn('lat', F.col('combined_output').getItem('lat'))
        dfout = dfout.withColumn('lon', F.col('combined_output').getItem('lon'))
        dfout = dfout.withColumn('elev', F.col('combined_output').getItem('elev'))
        dfout = dfout.withColumn('error', F.col('combined_output').getItem('error'))
        dfout = dfout.withColumn('execution_time', F.col('combined_output').getItem('execution_time'))
        dfout = dfout.drop('combined_output')

        output_columns = ["ts","satellite","dt","line1","line2","lat","lon","elev","error"]
        dfout = dfout.withColumn('tmp', F.arrays_zip(*output_columns))
        dfout = dfout.withColumn('tmp', F.explode('tmp'))
        dfout = dfout.drop(*output_columns)

        for output_column in output_columns:
            dfout = dfout.withColumn(output_column, F.col('tmp').getItem(output_column))

        dfout = dfout.drop('tmp')

        return dfout

    def extract_satellite(self, df):
        return df
