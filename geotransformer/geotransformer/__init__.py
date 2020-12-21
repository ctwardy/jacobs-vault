from datetime import datetime
import math

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
    def __init__(self):
        self.message = "Hello world!"

    def generate_lat_long(self, df):
        # def find_lat_long(linename, linedate, line1, line2):

        #     line1 = line1.replace('\\','')
        #     line2 = line2.replace('\\','')

        #     linedate = datetime.strptime(linedate, "%Y-%m-%d %H:%M:%S")

        #     try:
        #         tle_rec = ephem.readtle(linename, line1, line2)
        #         tle_rec.compute(linedate)
        #         lat, lon, elev, error = math.degrees(tle_rec.sublat), math.degrees(tle_rec.sublong), tle_rec.elevation, "No error"
        #     except ValueError as current_error:
        #         lat, lon, elev = 0.0, 0.0, 0.0
        #         error = "ValueError: " + str(current_error)
        #     except RuntimeError as current_error:
        #         lat, lon, elev = 0.0, 0.0, 0.0
        #         error = "RuntimeError: " + str(current_error)

        #     return (lat, lon, elev, error)

        def find_lat_long(linename, linedate, line1, line2):

            line1 = line1.replace('\\','')
            line2 = line2.replace('\\','')

            # linedate = datetime.strptime(linedate, "%Y-%m-%d %H:%M:%S")
            linedate = linedate.replace(' ','T') + "Z"
            error =  "No error"

            s = line1#'1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
            t = line2#'2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'
            satellite = Satrec.twoline2rv(s, t)

            t = Time(linedate, format='isot', scale='utc')
            error_code, teme_p, teme_v = satellite.sgp4(t.jd1, t.jd2)  # in km and km/s
            if error_code != 0:
                # raise RuntimeError(SGP4_ERRORS[error_code])
                error = SGP4_ERRORS[error_code]

            teme_p = CartesianRepresentation(teme_p*u.km)
            teme_v = CartesianDifferential(teme_v*u.km/u.s)
            teme = TEME(teme_p.with_differentials(teme_v), obstime=t)

            itrs = teme.transform_to(ITRS(obstime=t))  
            location = itrs.earth_location
            lat, lon, elev = location.lat.deg, location.lon.deg, location.height.value
            lat, lon, elev = float(lat), float(lon), float(elev)

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

        # df = df.withColumn('lat', df['combined_output'][0])
        # df = df.withColumn('lon', df['combined_output'][1])
        # df = df.withColumn('elev', df['combined_output'][2])

        return df

    def extract_satellite(self, df):
        return df
