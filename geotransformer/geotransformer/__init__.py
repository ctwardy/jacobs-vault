from datetime import datetime
import math
from time import perf_counter

import numpy as np

import pyspark.sql.functions as F
from pyspark.sql.types import FloatType, ArrayType, StructType, StructField, StringType, TimestampType

import ephem

from sgp4.api import Satrec
from sgp4.api import SGP4_ERRORS
from sgp4.conveniences import sat_epoch_datetime

from astropy.time import Time
from astropy.coordinates import TEME, CartesianDifferential, CartesianRepresentation
from astropy import units as u
from astropy.coordinates import ITRS

# Increment this version number when there is a new release:
__author__  = 'Christopher Morris'
__email__   = 'christopher.morris@jacobs.com'
__version__ = '0.1.0'



class GeoTransformer:
    def __init__(self, single_partition_length=100, extra_columns_list=['ts','satellite','dt','line1','line2']):
        self.single_partition_length = single_partition_length
        self.extra_columns_list = extra_columns_list

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

    def generate_orbital_parameters_astropy(self, df, spark):
        
        def find_orbital_parameters(line1_list, line2_list):

            start = perf_counter()

            # Clean up the lines
            line1_list = [line1.replace('\\','') for line1 in line1_list]
            line2_list = [line2.replace('\\','') for line2 in line2_list]

            # linedate_list = [linedate.replace(' ','T') + "Z" for linedate in linedate_list]

            satellites = [Satrec.twoline2rv(line1_list[i], line2_list[i]) for i, _ in enumerate(line1_list)]
            
            tle_datetimes = [sat_epoch_datetime(satellite) for satellite in satellites]
            tle_datetimes = [x.strftime("%Y-%m-%dT%H:%M:%SZ") for x in tle_datetimes]

            

            sat_numbers = [str(satellite.satnum) for satellite in satellites]
            sat_ndots   = [satellite.ndot for satellite in satellites]
            sat_nddots  = [satellite.nddot for satellite in satellites]
            sat_bstars  = [satellite.bstar for satellite in satellites]
            sat_incls   = [satellite.inclo for satellite in satellites]
            sat_rascs   = [satellite.nodeo for satellite in satellites]
            sat_eccos   = [satellite.ecco for satellite in satellites]
            sat_intls   = [str(satellite.intldesg) for satellite in satellites]
            
            t = [Time(current_time, format='isot', scale='utc') for current_time in tle_datetimes]
            tv = [satellite.sgp4(t[i].jd1, t[i].jd2) for i, satellite in enumerate(satellites)]  # in km and km/s
            tv = [[elem[0], elem[1][0], elem[1][1], elem[1][2], elem[2][0], elem[2][0], elem[2][1], elem[2][2]] for elem in tv]
            tv = np.array(tv)

            # teme_p = CartesianRepresentation(tv[:,1]*u.km, y=tv[:,2]*u.km, z=tv[:,3]*u.km)
            # teme_v = CartesianDifferential(tv[:,4]*u.km/u.s, d_y=tv[:,4]*u.km/u.s, d_z=tv[:,4]*u.km/u.s)
            # teme = TEME(teme_p.with_differentials(teme_v), obstime=t)

            # itrs = teme.transform_to(ITRS(obstime=t))
            # location = itrs.earth_location
            # lat, lon, elev = location.lat.deg, location.lon.deg, location.height.value
            # lat = [float(x) for x in lat]
            # lon = [float(x) for x in lon]
            # elev = [float(x) for x in elev]

            error_codes = tv[:,0]
            error_codes = ["No error" if error_code==0 else SGP4_ERRORS[error_code] for error_code in error_codes]
            
            end = perf_counter()

            execution_time = [(end - start) for i, _ in enumerate(line1_list)]

            # return (tle_datetimes, satellite_names, lat, lon, elev, error_codes, execution_time)
            return (tle_datetimes, 
                    sat_numbers, 
                    sat_ndots,
                    sat_nddots,
                    sat_bstars,
                    sat_incls,
                    sat_rascs,
                    sat_eccos,
                    sat_intls,
                    error_codes, 
                    execution_time)

        calculated_column_tuples = [('basedatetime', ArrayType(StringType())), 
                                    ('satellite', ArrayType(StringType())),
                                    ('ndot', ArrayType(FloatType())),
                                    ('nddots', ArrayType(FloatType())),
                                    ('bstar', ArrayType(FloatType())),
                                    ('inclination', ArrayType(FloatType())),
                                    ('right_asc', ArrayType(FloatType())),
                                    ('eccentricity', ArrayType(FloatType())),
                                    ('intnl_des', ArrayType(StringType())),
                                    ('error', ArrayType(StringType())), 
                                    ('execution_time', ArrayType(FloatType()))]
                                    # ('lat'ArrayType(FloatType())), 
                                    # ('lon'ArrayType(FloatType())), 
                                    # ('elev'ArrayType(FloatType())),
                                     
        calculated_columns = [x[0] for x in calculated_column_tuples]

        schema = StructType([StructField(*col_tup, True) for col_tup in calculated_column_tuples])
        # schema = StructType([
        #     StructField('basedatetime', ArrayType(StringType()), True),
        #     StructField('satellite', ArrayType(StringType()), True),
        #     StructField("lat", ArrayType(FloatType()), True),
        #     StructField("lon", ArrayType(FloatType()), True),
        #     StructField("elev", ArrayType(FloatType()), True),
        #     StructField("error", ArrayType(StringType()), True),
        #     StructField("execution_time", FloatType(), True),
        # ])

        find_orbital_parameters_udf = F.udf(find_orbital_parameters, schema)

        df_len = df.count()
        num_groups = df_len // self.single_partition_length
        num_groups = max(num_groups, 1) # there must be at least one group

        # Randomly assign DataFrame rows to groups
        dfg = df.withColumn(
            "group_id",
            (num_groups * F.rand()).cast('int').cast('string')
        )

        spark.conf.set('spark.default.parallellism', num_groups)
        dfg = dfg.repartition(num_groups)

        extra_columns_list = self.extra_columns_list#['ts','satellite','dt','line1','line2']

        # Collapse the rows of the DataFrame into lists based on group_id.
        # Only include extra columns if specified.
        dfg = dfg.groupBy("group_id").agg(*[
            F.collect_list(column_name).alias(column_name)
            for column_name in (
                extra_columns_list
            )
        ])

        dfg = dfg.withColumn('combined_output', find_orbital_parameters_udf('line1', 'line2'))

        # dfg.show()

        for column in calculated_columns:
            dfg = dfg.withColumn(column, F.col('combined_output').getItem(column))

        # dfg = dfg.withColumn('lon', F.col('combined_output').getItem('lon'))
        # dfg = dfg.withColumn('elev', F.col('combined_output').getItem('elev'))
        # dfg = dfg.withColumn('error', F.col('combined_output').getItem('error'))
        # dfg = dfg.withColumn('execution_time', F.col('combined_output').getItem('execution_time'))

        dfg = dfg.drop('combined_output')

        # dfg.show()

        output_columns = extra_columns_list + calculated_columns#["ts","satellite","dt","line1","line2","lat","lon","elev","error"]
        dfg = dfg.withColumn('tmp', F.arrays_zip(*output_columns))
        dfg = dfg.withColumn('tmp', F.explode('tmp'))
        dfg = dfg.drop(*output_columns)

        for output_column in output_columns:
            dfg = dfg.withColumn(output_column, F.col('tmp').getItem(output_column))

        dfg = dfg.drop('tmp')

        return dfg

    def extract_satellite(self, df):
        return df
