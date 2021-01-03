''' VAULT Proposal python module for addressing Technical Scenario objective 1

    | 1) Determine the “hits” where a satellite has geodetic overlap of any vessel(s) 
    |    at any point(s) in time. For simplicity, it may be assumed that a satellite has 
    |    full view of half the earth (regardless of satellite type or its elevation above 
    |    the earth). However, additional accuracy models with rationale is allowed.

    We are using the additional accuracy of actual visiblity of satellite, which also
    happens to result in more interesting looking outputs and made the problem slightly
    more technically challenging
'''

from datetime import datetime
from dateutil import tz
from functools import partial
from skyfield.api import EarthSatellite
from skyfield.api import Topos, load
import json
import math
import pandas as pd
import numpy as np

# Day-File schema elements
COLUMNS = ['satellite', 'day_dt', 'day', 'tle_dt', 'tle_ts', 'line1', 'line2']
DTYPES = {'satellite': 'uint16', # observed values are ints in 5..41678, so 0..65535 is good
          'day_dt': 'str',       # here a single date, but generally datetime: PARSE
          'day': 'uint16',       # here a single value 6026, too big for uint8, but 16 is good
          'tle_dt': 'str',       # again, PARSE AS DATETIME
          'tle_ts': 'uint32',    # large ints, but < 4294967295. We could compress more, but... meh
          'line1': str,          # 12K unique 80-char strings...
          'line2': str}          # ...Category wd give some compression, but really need to be parsed.

dates = ['day_dt', 'tle_dt']

# DAY_FILE_PATH="../data/TLE_daily"
DAY_FILE_PATH="../data/VAULT_Data/TLE_daily"


# These numbers may seem upside down, but I like the default coloring in the polar plot when hit quality has these values.
QUALITY_EXCELLENT = 0
QUALITY_GOOD = 1
QUALITY_POOR = 2
QUALITY_STALE = 3

class HitTest:
    ''' Counts the satellites that are visible at a given point on the globe at a given time
        returns counts classified by data quality and latitude,azimuth,hit_quality,radius for visible satellites
    '''
    def __init__(self, dt, day_file_base_path=DAY_FILE_PATH):
        df_path = "%s/%4d/%02d/%02d.tab.gz"%(day_file_base_path, dt.year, dt.month, dt.day)
        print(f"Trying to load {df_path}")
        df = pd.read_csv(df_path,
                         names=COLUMNS, sep='\t', compression='gzip',
                         dtype=DTYPES,
                         parse_dates=dates,
                         infer_datetime_format=True) 
        self.df_day_tle = df
    #

    # e.g. satellite_alt_az_days(datetime(2016, 6, 30), 45.0, -176.0)
    def satellite_alt_az_days(self, dt, lat, lon):
        earth_position = Topos(lat, lon)

        ts = load.timescale()
        t = ts.utc(dt.replace(tzinfo=tz.tzutc()))

        def eval_tle(row):
            satellite = EarthSatellite(row["line1"], row["line2"], 'x', ts)
            delta_days = abs(dt - row['tle_dt']).days

            difference = satellite - earth_position

            topocentric = difference.at(t)
            alt, az, distance = topocentric.altaz()
            
            if delta_days <= 2.0:
                if alt.degrees > 0.0:
                    qvals = [QUALITY_EXCELLENT, math.nan]
                else:
                    qvals = [math.nan, QUALITY_EXCELLENT]
            elif delta_days <= 14.0:
                if alt.degrees > 0.0:
                    qvals = [QUALITY_GOOD, math.nan]
                else:
                    qvals = [math.nan, QUALITY_GOOD]
            elif delta_days <= 56.0:
                if alt.degrees > 0.0:
                    qvals = [QUALITY_POOR, math.nan]
                else:
                    qvals = [math.nan, QUALITY_POOR]
            else:
                qvals = [math.nan, QUALITY_STALE]
                
            return pd.Series([alt.degrees, az.degrees, delta_days] + qvals)
        
        df_alt_az_days = pd.DataFrame(self.df_day_tle.apply(eval_tle, axis=1, raw=False))
        df_alt_az_days.columns = ["altitude", "azimuth", "days", "hit", "miss"]
        return df_alt_az_days
    #

    def invoke(self, dt, lat, lon):
        ''' Main logic for satellite hit-testing service

            returns 2 DataFrames: 
             - df_hit_miss_table :       The hit,miss stats table
             - df_alt_az_days_visible :  The information on the visible satellites for star-map plotting
        '''
        df_alt_az_days = self.satellite_alt_az_days(dt, lat, lon)

        # "invert" altitude for polar plotting.  Doing this thousands of times 
        #  more than necessary (really just want R for the df_alt_az_days_visible slice)
        #  but pandas does not like apply on a slice.
        df_alt_az_days.loc["R"] = 90.0 - df_alt_az_days["altitude"]

        def apply_quality_str(row, col):
            q = ""
            if row[col] == QUALITY_EXCELLENT:
                q = "Excellent"
            elif row[col] == QUALITY_GOOD:
                q = "Good"
            elif row[col] == QUALITY_POOR:
                q = "Poor"
            elif row[col] == QUALITY_STALE:
                q = "Stale"
            # no-else ... leave the NaNs alone
            return q
        #

        df_hit_miss_table = pd.concat([
                df_alt_az_days.apply(partial(apply_quality_str, col="hit"), axis=1).value_counts(),
                df_alt_az_days.apply(partial(apply_quality_str, col="miss"), axis=1).value_counts()]
            , axis=1, sort=False)

        df_alt_az_days_visible = df_alt_az_days[df_alt_az_days["altitude"]>0]

        return df_hit_miss_table, df_alt_az_days_visible
    #

    def web_invoke(self, dt, lat, lon):
        ''' Main support function for satellite hit-testing service

            returns a json object having two objects:
            { 
                "hitmiss": The hit,miss stats table
                "visible": The information on the visible satellites
            }
        '''
        df_hit_miss_table, df_alt_az_days_visible = self.invoke(dt, lat, lon)
        result = {
            "hitmiss": df_hit_miss_table.to_dict(),
            "visible": df_alt_az_days_visible.to_dict()
        }
        return json.dumps(result)
    #

